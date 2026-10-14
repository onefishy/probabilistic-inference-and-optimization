"""Convert the AM207 (Fall 2021) course repo into book chapters.

Usage:
    python scripts/convert_am207.py --src /path/to/am207 --labs /path/to/AM207_Lectures2020

Reads Lectures/, HW/ and weekN.md from the course repo and writes:
    chapters/NN-*.ipynb     one chapter per lecture (notes + summary + readings + exercises)
    chapters/impact-*.md    one "Applications and Broader Impact" chapter per part
    labs/lab-NN-*.ipynb     one page per lab (Lab_1 ... Lab_9 folders)
    figures/                images referenced by chapters (compressed)
    _static/figs/           images referenced from raw HTML, and videos
    data/                   datasets used by the notebooks
    _toc.yml

The converter is idempotent: generated directories are rebuilt from scratch on every run.
Phase 2 rewrites edit chapters/ directly, so do not re-run it after chapters have been
hand-edited unless you pass --only for chapters that are still untouched.
"""

import argparse
import collections
import copy
import re
import shutil
import subprocess
from pathlib import Path

import nbformat
from markdown_it import MarkdownIt
from PIL import Image

from am207_map import (HOMEWORK, LAB_DATA, LABS, LECTURE_DROP_CELLS, LECTURES, PARTS,
                       PRIVATE_LINK_MARKERS, READING_GROUPS, SKIP_OUTLINE, SUMMARY_CELLS,
                       SUMMARY_DROP_HEADINGS, TEXT_FIXES, CODE_FIXES, TYPO_FIXES)

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
LABS_DIR = ROOT / "labs"
FIGURES = ROOT / "figures"
STATIC_FIGS = ROOT / "_static" / "figs"
DATA = ROOT / "data"

MAX_IMAGE_WIDTH = 1600
LARGE_IMAGE_BYTES = 800_000
TEXT_WIDTH_PX = 740

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
IMG_RE = re.compile(r"<img\b[^>]*>", re.I)
MD_IMG_RE = re.compile(r"!\[([^\]]*)\]\((?!https?:)([^)\s]+)\)")
EMPTY_LINK_RE = re.compile(r"\[([^\]]*)\]\(\s*\)")
ATTR_RE = re.compile(r"""(\w+)\s*=\s*("([^"]*)"|'([^']*)')""")
MATH_SCAN_RE = re.compile(
    r"\$\$.*?\$\$"
    r"|\\begin\{(?P<env>aligned|align\*?|equation\*?|cases|array|eqnarray\*?)\}(?P<body>.*?)\\end\{(?P=env)\}"
    r"|(?<!\\)\$[^$\n]+?(?<!\\)\$",
    re.S)
VIDEO_RE = re.compile(r"""<source\s+src=["']fig/([^"']+)["']""")
IFRAME_RE = re.compile(r"""HTML\(\s*['"](<iframe.*?</iframe>)['"]\s*\)""", re.S)
DATA_FILES = ["HW0_data.csv", "HW6_data.csv", "HW8_data.csv", "kcancer.csv",
              "dataset_4_movie_names.txt", "dataset_4_ratings.txt", "birth_data.csv"]
DATA_FILES += [Path(p).name for p in LAB_DATA if Path(p).name not in DATA_FILES]


class Assets:
    """Tracks every image/video a chapter references and copies it into the book."""

    def __init__(self, src_dirs):
        self.src_dirs = src_dirs
        self.done = {}
        self.missing = []

    def _find(self, rel):
        rel = Path(rel)
        candidates = [rel] + [d / rel for d in self.src_dirs] + [d / rel.name for d in self.src_dirs]
        for p in candidates:
            if p.is_file():
                return p.resolve()
        self.missing.append(rel)
        return None

    def image(self, rel, dest_dir):
        """Copy (and compress) an image; return (book-relative path from chapters/, size) or None."""
        key = (rel, dest_dir)
        if key in self.done:
            return self.done[key]
        src = self._find(rel)
        if src is None:
            return None
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        size = compress_image(src, dest)
        result = (f"../{dest.relative_to(ROOT).as_posix()}", size)
        self.done[key] = result
        return result

    def video(self, name):
        src = self._find(Path("fig") / name)
        if src is None:
            return None
        STATIC_FIGS.mkdir(parents=True, exist_ok=True)
        dest = STATIC_FIGS / (Path(name).stem + ".mp4")
        if not dest.exists():
            transcode_video(src, dest)
        return f"../_static/figs/{dest.name}"

    def file(self, rel, dest_dir):
        src = self._find(rel)
        if src is None:
            return None
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)
        return f"../{(dest_dir / src.name).relative_to(ROOT).as_posix()}"


def compress_image(src, dest):
    """Copy an image, shrinking it if it is large. Returns its (width, height)."""
    with Image.open(src) as im:
        size = im.size
        if src.suffix.lower() == ".gif" or src.stat().st_size <= LARGE_IMAGE_BYTES:
            shutil.copy2(src, dest)
            return size
        im.load()
        if im.width > MAX_IMAGE_WIDTH:
            im = im.resize((MAX_IMAGE_WIDTH, round(im.height * MAX_IMAGE_WIDTH / im.width)),
                           Image.LANCZOS)
        if src.suffix.lower() == ".png":
            im.save(dest, optimize=True)
            if dest.stat().st_size > LARGE_IMAGE_BYTES:
                # Slides/screenshots survive palette quantization well.
                im.convert("RGBA").quantize(256, method=Image.FASTOCTREE).save(dest, optimize=True)
        else:
            im.convert("RGB").save(dest, quality=85, optimize=True)
        return size


def transcode_video(src, dest):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(src),
                    "-vf", "scale='min(960,iw)':-2", "-c:v", "libx264", "-crf", "28",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart",
                    str(dest)], check=True)


# ---------------------------------------------------------------------------
# Markdown transforms
# ---------------------------------------------------------------------------

def fix_math(text):
    """Wrap LaTeX environments that sit outside $...$ in $$...$$ so Sphinx renders them.

    Scans left to right so an environment is recognised before any $...$ nested
    inside it (e.g. \\text{since $U$ is uniform})."""
    def repl(m):
        if m.group("env") is None:
            return m.group(0)
        env, body = m.group("env"), m.group("body")
        if env.startswith(("align", "eqnarray")):
            env = "aligned"  # align cannot nest inside $$; aligned can
        elif env.startswith("equation"):
            return "$$" + _squash_blank_lines(body) + "$$"
        return "$$\\begin{%s}%s\\end{%s}$$" % (env, _squash_blank_lines(body), env)
    return MATH_SCAN_RE.sub(repl, text)


def _squash_blank_lines(s):
    # A blank line would end the paragraph (and the math) in Markdown.
    return re.sub(r"\n\s*\n", "\n", s)


_COMMONMARK = MarkdownIt("commonmark")


def fix_indented_code(text):
    """Jupyter renders deeply indented list continuations as lists; CommonMark turns them
    into code blocks. The notes only use fenced code, so join any indented code block to
    the paragraph above it by dropping the blank line(s) that separate them."""
    for _ in range(10):
        lines = text.split("\n")
        blocks = [t.map for t in _COMMONMARK.parse(text) if t.type == "code_block" and t.map]
        if not blocks:
            return text
        start = blocks[0][0]
        j = start
        while j > 0 and not lines[j - 1].strip():
            j -= 1
        if j == start or j == 0:
            return text  # nothing above to join onto
        text = "\n".join(lines[:j] + lines[start:])
    return text


def parse_attrs(tag):
    return {m.group(1).lower(): (m.group(3) if m.group(3) is not None else m.group(4))
            for m in ATTR_RE.finditer(tag)}


def css_height(style):
    m = re.search(r"height\s*:\s*(\d+)\s*px", style or "")
    return int(m.group(1)) if m else None


def convert_images(text, assets, src_base, label_prefix, labels_used, fig_dir=FIGURES, static_dir=STATIC_FIGS):
    """Standalone <img> lines become {figure} directives; images inside other HTML
    (tables) keep a raw <img> pointing into _static/, which Sphinx copies verbatim."""
    # Local Markdown images get the same treatment as <img> tags.
    text = MD_IMG_RE.sub(lambda m: f'<img src="{m.group(2)}" alt="{m.group(1)}">', text)
    lines = text.split("\n")
    out = []
    table_depth = 0
    for line in lines:
        table_depth += len(re.findall(r"<table\b", line, re.I))
        in_table = table_depth > 0
        table_depth -= len(re.findall(r"</table>", line, re.I))
        tags = IMG_RE.findall(line)
        if not tags:
            out.append(line)
            continue
        standalone = len(tags) == 1 and line.strip() == tags[0].strip() and not in_table
        if standalone:
            # Keep the image's indentation so a figure inside a list item stays in the list.
            indent = line[:len(line) - len(line.lstrip())]
            fig = _figure_directive(tags[0], assets, src_base, label_prefix, labels_used, fig_dir)
            out.append("\n".join(indent + l if l else l for l in fig.split("\n")))
            continue
        for tag in tags:
            a = parse_attrs(tag)
            rel = src_base / a.get("src", "")
            if a.get("src", "").endswith("logos.jpg"):
                line = line.replace(tag, "")
                continue
            res = assets.image(rel, static_dir)
            if res is None:
                continue
            path, _ = res
            h = css_height(a.get("style"))
            style = f' style="max-width:100%;height:auto;max-height:{h}px"' if h else ' style="max-width:100%"'
            line = line.replace(tag, f'<img src="{path}" alt="{a.get("alt", "")}"{style}>')
        out.append(line)
    return "\n".join(out)


def _figure_directive(tag, assets, src_base, label_prefix, labels_used, fig_dir=FIGURES):
    a = parse_attrs(tag)
    src = a.get("src", "")
    if src.endswith("logos.jpg"):
        return ""
    if src.lower().endswith(".pdf"):
        path = assets.file(src_base / src, fig_dir)
        return f"{{download}}`Download the derivation (PDF) <{path}>`" if path else ""
    res = assets.image(src_base / src, fig_dir)
    if res is None:
        return f"<!-- missing image: {src} -->"
    path, (w, h) = res
    lines = [f"```{{figure}} {path}"]
    stem = re.sub(r"[^a-z0-9]+", "-", Path(src).stem.lower()).strip("-")
    label = f"{label_prefix}-{stem}"
    if label not in labels_used:
        labels_used.add(label)
        lines.append(f":name: {label}")
    if a.get("alt"):
        lines.append(f":alt: {a['alt']}")
    target_h = css_height(a.get("style")) or (int(a["height"]) if a.get("height", "").isdigit() else None)
    if target_h and h:
        width = round(target_h * w / h)
        lines.append(":width: 100%" if width >= TEXT_WIDTH_PX else f":width: {width}px")
    lines.append(":align: center")
    lines.append("```")
    # Blank lines keep the directive from merging into a surrounding paragraph/list.
    return "\n" + "\n".join(lines) + "\n"


def shift_headings(text, delta, min_level=2):
    def repl(m):
        level = min(6, max(min_level, len(m.group(1)) + delta))
        return "#" * level + " " + m.group(2)
    return HEADING_RE.sub(repl, text)


def headings_to_bold(text):
    return HEADING_RE.sub(lambda m: f"**{m.group(2).strip()}**", text)


def strip_private_links(text):
    kept = []
    for line in text.split("\n"):
        if any(marker in line for marker in PRIVATE_LINK_MARKERS):
            continue
        kept.append(line)
    return "\n".join(kept)


def clean_markdown(text, assets, src_base, label_prefix, labels_used, heading_delta=1,
                   fig_dir=FIGURES, static_dir=STATIC_FIGS):
    text = text.replace("\r\n", "\n")
    text = EMPTY_LINK_RE.sub(r"\1", text)  # a few links were left empty in the course notes
    text = fix_indented_code(text)
    text = fix_math(text)
    text = convert_images(text, assets, src_base, label_prefix, labels_used, fig_dir, static_dir)
    text = shift_headings(text, heading_delta)
    return text.strip()


DISPLAY_MATH_RE = re.compile(r"\$\$.*?\$\$", re.S)
LIST_MARKER_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])(\s+)")


def isolate_display_math(text):
    """Give every $$...$$ its own paragraph.

    Inline display math renders as a <div> inside a <p>; browsers then close the <p> early
    and the text after the equation escapes its container. Inside a collapsed dropdown that
    text stays visible. New paragraphs are indented to the enclosing list item's content
    column so list structure is preserved."""
    def line_bounds(i):
        start = text.rfind("\n", 0, i) + 1
        end = text.find("\n", i)
        return start, (len(text) if end < 0 else end)

    def is_blank_line_before(line_start):
        if line_start == 0:
            return True
        prev_start, prev_end = line_bounds(line_start - 1)
        return not text[prev_start:prev_end].strip()

    out, pos = [], 0
    for m in DISPLAY_MATH_RE.finditer(text):
        line_start, _ = line_bounds(m.start())
        # Content indent comes from the first line of the enclosing paragraph.
        para_start = line_start
        while not is_blank_line_before(para_start):
            para_start, _ = line_bounds(para_start - 1)
        first_line = text[para_start:line_bounds(para_start)[1]]
        marker = LIST_MARKER_RE.match(first_line)
        indent = " " * (len(marker.group(0)) if marker else len(first_line) - len(first_line.lstrip()))
        # In a list, the innermost item holding the math: its own line, or the nearest item above
        # whose marker sits left of the math line.
        math_line = text[line_start:line_bounds(line_start)[1]]
        k = len(math_line) - len(math_line.lstrip(" "))
        start = line_start
        while k and start > para_start:
            item = LIST_MARKER_RE.match(text[start:line_bounds(start)[1]])
            if item and (start == line_start or len(item.group(1)) < k):
                indent = " " * len(item.group(0))
                break
            start, _ = line_bounds(start - 1)

        if text[line_start:m.start()].strip():      # text before the math on the same line
            out.append(text[pos:m.start()].rstrip() + "\n\n")
        else:
            out.append(text[pos:line_start])
            if not is_blank_line_before(line_start):  # math continues a paragraph
                out.append("\n")
        out.append("\n".join(indent + l.strip() for l in m.group(0).split("\n")))

        _, math_line_end = line_bounds(m.end())
        tail = text[m.end():math_line_end]
        if tail.strip():                            # text after the math on the same line
            out.append("\n\n" + indent + tail.strip())
        pos = math_line_end
        next_start, next_end = (line_bounds(pos + 1) if pos < len(text) else (pos, pos))
        if pos < len(text) and text[next_start:next_end].strip():
            out.append("\n")                       # blank line before the paragraph continues
    out.append(text[pos:])
    return "".join(out)


TABLE_SEPARATOR_RE = re.compile(r"^([ \t]*)-[ \t]*\|[ \t|-]*$", re.M)
ZERO_LIST_RE = re.compile(r"^[ \t]{0,3}0[.)][ \t]")
LIST_ITEM_RE = re.compile(r"^[ \t]*(?:[-*+]|\d+[.)])[ \t]")
# Code fences and HTML tables are left alone by layout_fixes.
LAYOUT_PROTECTED_RE = re.compile(r"(^[ \t]*```.*?^[ \t]*```[ \t]*$|^[ \t]*<table\b.*?</table>[^\n]*$)", re.M | re.S)
# Two inline formulas written back to back ("$\quad$$\quad$") contain a "$$" that is not display math.
ADJACENT_INLINE_MATH_RE = re.compile(r"\$[^$\s][^$\n]*\$\$[^$\s][^$\n]*\$")


def separate_zero_lists(text):
    """CommonMark only lets a list that starts at 1 interrupt a paragraph, so a list starting at
    0 right after a line of text ("...algorithm:\\n0. Initialize ...") renders inline. Put a
    blank line before it."""
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        if i and ZERO_LIST_RE.match(line):
            block = []  # the paragraph lines directly above (a heading or blank line ends it)
            for prev in reversed(out):
                if not prev.strip() or prev.lstrip().startswith("#"):
                    break
                block.append(prev)
            if block and not any(LIST_ITEM_RE.match(b) for b in block):
                out.append("")
        out.append(line)
    return "\n".join(out)


_MYST_PARSER = None
_STRUCTURE_TOKENS = {"bullet_list_open", "ordered_list_open", "list_item_open", "code_block", "fence",
                     "table_open", "blockquote_open", "dl_open", "html_block"}


def myst_structure(text):
    """Lists (with start numbers), code blocks, tables and the number of inline formulas in the
    MyST parse of `text`, including the bodies of colon-fence directives (admonitions)."""
    global _MYST_PARSER
    if _MYST_PARSER is None:
        from markdown_it.renderer import RendererHTML
        from myst_parser.config.main import MdParserConfig
        from myst_parser.parsers.mdit import create_md_parser
        config = MdParserConfig(enable_extensions={"amsmath", "colon_fence", "deflist", "dollarmath",
                                                   "html_admonition", "linkify", "substitution"},
                                dmath_double_inline=True)
        _MYST_PARSER = create_md_parser(config, RendererHTML)
    out, inline_math = [], 0
    for t in _MYST_PARSER.parse(text):
        if t.type in _STRUCTURE_TOKENS:
            out.append((t.type, t.level, (t.attrs or {}).get("start")))
        elif t.type == "inline":
            # a total, since splitting a paragraph in two splits its formulas between two inlines
            inline_math += sum(c.type == "math_inline" for c in t.children or [])
        elif t.type == "colon_fence":
            body = "\n".join(l for l in t.content.split("\n") if not re.match(r"^:\w+:", l))
            out.append(("colon_fence", tuple(myst_structure(body))))
    return out + [("math_inline", inline_math)]


def isolate_display_math_safely(text):
    """isolate_display_math, one paragraph at a time, keeping a change only if the MyST parse of
    the text keeps its lists, code blocks, tables and inline math. Moving an equation out of a list
    item can otherwise end the list early or turn the indented lines after it into a code block."""
    blocks = re.split(r"(\n[ \t]*\n)", text)
    if not any("$$" in b for b in blocks[::2]):
        return text
    base = myst_structure(text)
    for i in range(0, len(blocks), 2):
        if "$$" not in blocks[i]:
            continue
        new = isolate_display_math(blocks[i])
        if new != blocks[i] and myst_structure("".join(blocks[:i] + [new] + blocks[i + 1:])) == base:
            blocks[i] = new
    return "".join(blocks)


ORDERED_ITEM_RE = re.compile(r"^ {0,3}\d{1,9}[.)] +(?=\S)")
ITEM_MARKER_RE = re.compile(r"^( *)([-*+]|\d{1,9}[.)])( +)(?=\S)")
UNINDENTED_BLOCK_START_RE = re.compile(r"^(?:#|:::|```|<(?!br\s*/?>))")  # "<br>text" is paragraph text


def myst_counts(text):
    """Counts of list items, code blocks, tables, HTML blocks and formulas in the MyST parse of
    `text`, including the bodies of colon-fence directives."""
    myst_structure("")  # builds the parser
    counts = collections.Counter()
    for t in _MYST_PARSER.parse(text):
        if t.type in ("list_item_open", "code_block", "fence", "table_open", "html_block"):
            counts[t.type] += 1
        elif t.type.startswith("math_block") or t.type == "amsmath":
            counts["math"] += 1
        elif t.type == "inline":
            counts["math"] += sum(c.type.startswith("math_inline") for c in t.children or [])
        elif t.type == "colon_fence":
            counts += myst_counts("\n".join(l for l in t.content.split("\n") if not re.match(r"^:\w+:", l)))
    return counts


def _numbered_items(lines):
    """(start, end) line ranges of unindented numbered items: from the item to its next sibling, or
    to the first unindented line, other than a list item, after a blank line (or to a heading,
    fence or HTML)."""
    items, i = [], 0
    while i < len(lines):
        m = ORDERED_ITEM_RE.match(lines[i])
        if not m:
            i += 1
            continue
        indent = len(lines[i]) - len(lines[i].lstrip(" "))
        j, prev_blank = i + 1, False
        while j < len(lines):
            line = lines[j]
            if ORDERED_ITEM_RE.match(line) and len(line) - len(line.lstrip(" ")) <= indent:
                break
            if line[:1].strip() and not ITEM_MARKER_RE.match(line) and \
                    (prev_blank or UNINDENTED_BLOCK_START_RE.match(line)):
                break
            prev_blank = not line.strip()
            j += 1
        items.append((i, j))
        i = j
    return items


def _renest(lines):
    """Re-indent list lines the way the notebooks' original renderer read them: a line indented
    past an item's marker (a sub-item: at least two spaces past) belongs to that item, so it moves
    to at least the item's text column (CommonMark needs the full column; 2 spaces under '1. '
    renders flush left)."""
    out, stack = [], []  # (marker indent, text column, bullet?) in the source, text column in the output
    fence_shift = None  # inside a code fence, every line moves with the opening line
    prev_blank = True
    for line in lines:
        s = len(line) - len(line.lstrip(" "))
        if fence_shift is not None:
            out.append(" " * fence_shift + line if fence_shift >= 0 else line[min(-fence_shift, s):])
            if line.lstrip().startswith("```"):
                fence_shift = None
            continue
        m = ITEM_MARKER_RE.match(line)
        if not line.strip():
            out.append(line)
            prev_blank = True
            continue
        if s == 0 and not m:  # an unindented line continuing the text above (a "lazy" line)
            out.append(" " * stack[-1][3] + line if stack else line)
            continue
        bullet = bool(m) and m.group(2) in "-*+"
        # Text straight after a line of text continues the innermost item (CommonMark reads it as
        # a lazy continuation whatever its indent); otherwise the indent decides. An item one space
        # deeper than an item of the same kind is its sibling.
        while stack and (m or prev_blank) and \
                (s <= stack[-1][0] or (m and s == stack[-1][0] + 1 and bullet == stack[-1][2])):
            stack.pop()
        prev_blank = False
        dst = stack[-1][3] + max(0, s - stack[-1][1]) if stack else s
        if m:
            spaces = len(m.group(3))
            width = len(m.group(2)) + (spaces if spaces <= 4 else 1)
            stack.append((s, s + width, bullet, dst + width))
        elif line.lstrip().startswith("```"):
            fence_shift = dst - s
        out.append(" " * dst + line.lstrip(" "))
    return out


def indent_list_continuations(text):
    """Re-indent each numbered item (_renest), so follow-on paragraphs, hints and sub-lists stay
    inside it instead of rendering flush left or as run-on text. An item is changed only if
    the MyST parse keeps its tables, HTML and formulas and loses no list items (indented-code
    blocks may only go away: those were lines that rendered as code by accident)."""
    lines = text.split("\n")
    base = myst_counts(text)
    for start, end in reversed(_numbered_items(lines)):
        region = lines[start:end]
        if any(l.lstrip().startswith("#") for l in region):
            continue
        trial = lines[:start] + _renest(region) + lines[end:]
        if trial == lines:
            continue
        after = myst_counts("\n".join(trial))
        if all(after[k] == base[k] for k in ("fence", "table_open", "html_block")) and \
                after["list_item_open"] >= base["list_item_open"] and \
                after["code_block"] <= base["code_block"] and after["math"] >= base["math"]:
            lines, base = trial, after
    return "\n".join(lines)


def layout_fixes(text):
    """Fix Markdown that MyST renders wrongly: display math inside a paragraph (the text after it
    escapes the paragraph), numbered lists starting at 0 right after text (rendered inline),
    table separator rows written '- | -' (parsed as a bullet), and numbered items whose follow-on
    lines are indented too little to stay inside the item."""
    for _ in range(5):  # each fix can enable another (an equation moved into a list item, ...)
        parts = LAYOUT_PROTECTED_RE.split(indent_list_continuations(text))
        for i in range(0, len(parts), 2):
            t = TABLE_SEPARATOR_RE.sub(lambda m: m.group(1) + " | ".join("---" for _ in m.group(0).split("|")), parts[i])
            t = separate_zero_lists(t)
            parts[i] = t if ADJACENT_INLINE_MATH_RE.search(t) else isolate_display_math_safely(t)
        if "".join(parts) == text:
            break
        text = "".join(parts)
    return text


def fence(n):
    return ":" * n


def admonition(title, body, cls=None, depth=4):
    lines = [f"{fence(depth)}{{admonition}} {title}"]
    if cls:
        lines.append(f":class: {cls}")
    if cls == "dropdown":
        body = isolate_display_math(body)
    lines += ["", body.strip(), fence(depth)]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Chapter assembly
# ---------------------------------------------------------------------------

def md(text, **meta):
    cell = nbformat.v4.new_markdown_cell(text)
    cell.metadata.update(meta)
    return cell


def clean_code_cell(cell, tags=()):
    cell = copy.deepcopy(cell)
    cell.metadata = {k: v for k, v in cell.metadata.items() if k not in ("slideshow", "scrolled", "collapsed")}
    if tags:
        cell.metadata["tags"] = sorted(set(cell.metadata.get("tags", [])) | set(tags))
    src = cell.source
    src = re.sub(r"""(['"])(?:\./)?(?:\.\./)?(?:Labs/)?datasets/""", r"\1../data/", src)
    for name in DATA_FILES:
        src = re.sub(rf"""(['"])(?:\./)?{re.escape(name)}""", rf"\1../data/{name}", src)
    cell.source = src
    return cell


def slide_type(cell):
    return cell.get("metadata", {}).get("slideshow", {}).get("slide_type")


def is_logo_cell(text):
    return "logos.jpg" in text and len(IMG_RE.sub("", text).replace("#", "").strip()) == 0


def convert_lecture_notes(n, src, assets, video_url):
    slug, title, _, _ = LECTURES[n]
    nb = nbformat.read(src / "Lectures" / f"lecture_{n}_notes.ipynb", as_version=4)
    label_prefix = f"fig-{slug.split('-', 1)[0]}"
    labels = set()
    cells = [md(f"# {title}")]
    intro = []
    if video_url:
        intro.append(f"This chapter is adapted from AM207 (Harvard, Fall 2021). "
                     f"[Watch the recorded lecture]({video_url}).")
    else:
        intro.append("This chapter is adapted from AM207 (Harvard, Fall 2021).")
    cells.append(md("\n\n".join(intro)))

    prev_heading = None
    outline_done = False
    deferred = []
    for i, cell in enumerate(nb.cells):
        text = cell.source
        if i in LECTURE_DROP_CELLS.get(n, ()):
            continue
        if cell.cell_type == "markdown":
            if i == 0 or is_logo_cell(text) or not text.strip():
                continue
            if not outline_done and re.match(r"^\s*#+\s*Outline", text):
                body = HEADING_RE.sub("", text, count=1).strip()
                if n not in SKIP_OUTLINE:
                    cells.append(md(admonition("In this chapter", body, cls="tip")))
                cells += deferred  # hidden setup cells read better after the outline
                deferred = []
                outline_done = True
                continue
            body = clean_markdown(text, assets, src / "Lectures", label_prefix, labels)
            if slide_type(cell) in ("skip", "notes"):
                m = HEADING_RE.match(body)
                aside_title = m.group(2) if m else "Aside"
                aside_body = headings_to_bold(HEADING_RE.sub("", body, count=1) if m else body)
                if aside_body.strip():
                    cells.append(md(admonition(f"Going deeper: {aside_title}", aside_body, cls="dropdown")))
                continue
            # Consecutive slides often repeat the same title; keep it once.
            m = HEADING_RE.match(body)
            if m and m.group(2).strip() == prev_heading:
                body = body[m.end():].strip()
            for h in HEADING_RE.finditer(body):
                prev_heading = h.group(2).strip()
            if body:
                cells.append(md(body))
        elif cell.cell_type == "code":
            if not text.strip():
                continue
            videos = VIDEO_RE.findall(text) if "<video" in text else []
            if videos:
                for v in videos:
                    path = assets.video(v)
                    if path:
                        cells.append(md(f'<video controls muted playsinline style="max-width:100%;max-height:440px">'
                                        f'<source src="{path}" type="video/mp4"></video>'))
                continue
            iframe = IFRAME_RE.search(text)
            if iframe:
                html = iframe.group(1).replace("&amp;", "&")
                cells.append(md(f'<div style="text-align:center">{html}</div>'))
                continue
            if "Import basic libraries" in text or re.match(r"^\s*(import|from)\s", text) and not cell.get("outputs"):
                (cells if outline_done else deferred).append(clean_code_cell(cell, ["hide-cell"]))
            elif slide_type(cell) == "skip":
                cells.append(clean_code_cell(cell, ["hide-input"] if cell.get("outputs") else ["hide-cell"]))
            else:
                cells.append(clean_code_cell(cell))
    cells[2:2] = deferred  # no outline cell: setup code goes right after the intro
    return nb, cells, labels


def summary_cells(src, assets):
    """Return {lecture: [(kind, title, markdown)]} and {part: [markdown]} from summary notebooks."""
    per_lecture, impact = {}, {}
    for (stem, idx), action in SUMMARY_CELLS.items():
        nb = nbformat.read(src / "Lectures" / f"{stem}.ipynb", as_version=4)
        text = nb.cells[idx].source
        labels = set()
        if action[0] == "drop":
            continue
        # Strip logistics subsections.
        for h in SUMMARY_DROP_HEADINGS:
            text = re.sub(rf"^(#+)\s*{re.escape(h)}.*?(?=^#+\s)", "", text, flags=re.S | re.M)
        if action[0] == "impact":
            body = clean_markdown(text, assets, src / "Lectures", "fig-impact", labels, heading_delta=0)
            impact.setdefault(action[1], []).append(body)
            continue
        lec = action[1]
        prefix = f"fig-{LECTURES[lec][0].split('-', 1)[0]}-summary"
        if action[0] == "recap":
            # Drop the "Lecture #N Summary" heading; the chapter supplies its own.
            text = re.sub(r"^\s*#+\s*(Lecture #\d+ Summary|Summary of Lecture #\d+|Overview of Lecture #\d+)\s*:?\s*\n",
                          "", text.lstrip())
            body = clean_markdown(text, assets, src / "Lectures", prefix, labels, heading_delta=0)
            body = shift_headings(body, 0, min_level=3)
            per_lecture.setdefault(lec, []).append(("recap", None, body))
        else:
            section_title = action[2]
            text = re.sub(r"^\s*#+\s*Lecture #\d+ Summary:?\s*\n", "", text.lstrip())
            body = clean_markdown(text, assets, src / "Lectures", prefix, labels, heading_delta=0)
            if section_title:
                body = HEADING_RE.sub("", body, count=1).strip() if body.lstrip().startswith("#") and \
                    section_title.lower() in body.split("\n", 1)[0].lower() else body
                body = shift_headings(body, 0, min_level=3)
                per_lecture.setdefault(lec, []).append(("section", section_title, body))
            else:
                body = shift_headings(body, 1, min_level=3)
                per_lecture.setdefault(lec, []).append(("section-cont", None, body))
    return per_lecture, impact


# ---------------------------------------------------------------------------
# Weekly pages: video links and reading lists
# ---------------------------------------------------------------------------

def parse_week(path):
    """Return (videos {lecture: url}, groups [(title, [items])])."""
    text = path.read_text()
    videos = {}
    for m in re.finditer(r"Lecture #(\d+):[^\n]*\n\s*-\s*\[Lecture Video\]\(([^)]+)\)", text):
        videos[int(m.group(1))] = m.group(2)
    groups = []
    reading = text.split("### Reading", 1)[1] if "### Reading" in text else ""
    current = None
    for line in reading.split("\n"):
        s = line.strip()
        if not s:
            continue
        header = re.fullmatch(r"\*\*(.+?):?\*\*:?|([A-Z][^\[\]()]*?):", s)
        if header:
            current = (header.group(1) or header.group(2)).strip().rstrip(":").strip()
            groups.append((current, []))
            continue
        item = re.match(r"^(?:\d+\.|-)\s+(.*)$", s)
        if item and groups:
            groups[-1][1].append(item.group(1).strip())
    return videos, groups


def readings(src):
    videos, per_lecture, impact, unmapped = {}, {}, {}, []
    for week in range(1, 12):
        v, groups = parse_week(src / f"week{week}.md")
        videos.update(v)
        for title, items in groups:
            items = [i for i in items if not any(mk in i for mk in PRIVATE_LINK_MARKERS)]
            if not items:
                continue
            key = next((k for k in READING_GROUPS if k[0] == week and title.lower().startswith(k[1].lower())), None)
            if key is None:
                unmapped.append((week, title))
                continue
            target = READING_GROUPS[key]
            if target is None:
                continue
            bucket = impact.setdefault(target[1], []) if isinstance(target, tuple) \
                else per_lecture.setdefault(target, [])
            bucket.append((title, items))
    if unmapped:
        raise SystemExit(f"Unmapped reading groups (add them to READING_GROUPS): {unmapped}")
    return videos, per_lecture, impact


# A reading linked through the Harvard library proxy (the URL carries a personal access token)
# keeps its title but loses the link.
PROXY_LINK_RE = re.compile(r"\[([^\]]+)\]\(https?://[^)\s]*\.hul\.harvard\.edu/[^)\s]*\)")


def reading_markdown(groups, heading="## Further Reading"):
    merged = {}
    for title, items in groups:
        merged.setdefault(title, []).extend(i for i in items if i not in merged.get(title, []))
    parts = [heading, ""]
    for title, items in merged.items():
        parts.append(f"**{title}**\n")
        parts += ["- " + PROXY_LINK_RE.sub(r"\1", i) for i in items]
        parts.append("")
    return "\n".join(parts).strip()


# ---------------------------------------------------------------------------
# Homework -> exercises
# ---------------------------------------------------------------------------

def homework_segments(src, hw, assets):
    """Split a homework notebook into problem segments of cells (header/instructions removed)."""
    nb = nbformat.read(src / "HW" / f"AM207_HW{hw}.ipynb", as_version=4)
    title_m = re.search(r"^##\s+(.+)$", nb.cells[0].source, re.M)
    hw_title = title_m.group(1).strip().replace("Stastistical", "Statistical") if title_m else f"Problem Set {hw}"
    body = nb.cells[3:]  # 0: title, 1: name/collaborators, 2: instructions
    segments = [[]]
    for cell in body:
        if cell.cell_type == "markdown" and re.search(r"^#\s+Problem Description", cell.source, re.M) and segments[-1] \
                and any(c.cell_type == "markdown" for c in segments[-1]):
            segments.append([])
        segments[-1].append(cell)
    return hw_title, segments


def exercise_cells(src, hw, seg_cells, hw_title, assets, label_prefix, labels):
    cells = []
    for cell in seg_cells:
        if cell.cell_type == "code":
            if cell.source.strip():
                c = clean_code_cell(cell, ["hide-cell"])
                c.outputs = []
                c.execution_count = None
                cells.append(c)
            continue
        text = cell.source.replace("\r\n", "\n").strip()
        text = re.sub(r"^-{3,}\s*$", "", text, flags=re.M).strip()
        if not text:
            continue
        text = fix_math(fix_indented_code(EMPTY_LINK_RE.sub(r"\1", text)))
        text = convert_images(text, assets, src / "HW", label_prefix, labels)
        # Split into (heading, body) chunks; Parts become exercise admonitions.
        chunks = re.split(r"^(#{1,6}\s+.*)$", text, flags=re.M)
        out = []
        if chunks[0].strip():
            out.append(chunks[0].strip())
        for h, b in zip(chunks[1::2], chunks[2::2]):
            htext = HEADING_RE.match(h).group(2).strip().rstrip(":")
            b = headings_to_bold(b).strip()
            if re.match(r"(Part\b|Exercise\b)", htext):
                out.append(admonition(f"Exercise: {htext}", b or "&nbsp;"))
            elif re.match(r"\(Material covered", htext):
                out.append(f"*{htext}*\n\n{b}".strip())
            else:
                htext = re.sub(r"^Problem Description:?\s*", "", htext) or "Problem Description"
                out.append(b if htext == hw_title else f"#### {htext}\n\n{b}".strip())
        cells.append(md("\n\n".join(out)))
    return cells


# ---------------------------------------------------------------------------
# Labs
# ---------------------------------------------------------------------------

def write_notebook(cells, path, id_prefix):
    out = nbformat.v4.new_notebook()
    for i, c in enumerate(cells):
        c.id = f"{id_prefix}-{i:03d}"
    out.cells = cells
    out.metadata = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
    }
    nbformat.write(out, path)


def convert_lab(n, labs_src, assets):
    """One lab notebook -> a book page. Worked answers (LABS[n][3]) are collapsed."""
    rel, slug, title, answers = LABS[n]
    path = labs_src / rel
    nb = nbformat.read(path, as_version=4)
    fig_dir, static_dir = FIGURES / "labs" / slug, STATIC_FIGS / "labs" / slug
    labels = set()
    intro = "This lab is adapted from AM207 (Harvard). Data files are in the book's `data/` folder."
    if answers:
        intro += " Worked solutions are collapsed: try each exercise before expanding them."
    cells = [md(f"# Lab {n}: {title}"), md(intro)]
    deferred, outline_done = [], False
    for i, cell in enumerate(nb.cells):
        text = cell.source
        if cell.cell_type == "markdown":
            if re.match(r"^\s*#\s*Lab\s*#\s*\d+", text) or is_logo_cell(text) \
                    or re.fullmatch(r"\s*(-{3,})?\s*", text):
                continue
            if not outline_done and re.match(r"^\s*#+\s*Outline", text):
                body = HEADING_RE.sub("", text, count=1).strip()
                cells.append(md(admonition("In this lab", body, cls="tip")))
                cells += deferred
                deferred, outline_done = [], True
                continue
            body = clean_markdown(text, assets, path.parent, f"fig-lab{n}", labels, heading_delta=0,
                                  fig_dir=fig_dir, static_dir=static_dir)
            # A "**Solution:**" marker can also sit partway through a prompt cell.
            parts = re.split(r"\*\*Solution:?\*\*:?", body, maxsplit=1)
            prompt, solution = parts if len(parts) == 2 else (body, "")
            if i in answers and len(parts) == 1:
                prompt, solution = "", body
            if prompt.strip():
                cells.append(md(prompt.strip()))
            if solution.strip():
                cells.append(md(admonition("Solution", headings_to_bold(solution.strip()), cls="dropdown")))
        elif cell.cell_type == "code":
            if not text.strip() or text.lstrip().startswith("!pip"):
                continue
            if i in answers:
                cells.append(clean_code_cell(cell, ["hide-input"] if cell.get("outputs") else ["hide-cell"]))
            elif "Import basic libraries" in text or re.match(r"^\s*(import|from)\s", text) and not cell.get("outputs"):
                (cells if outline_done else deferred).append(clean_code_cell(cell, ["hide-cell"]))
            else:
                cells.append(clean_code_cell(cell))
    cells[2:2] = deferred  # no outline cell: setup code goes right after the intro
    return slug, cells


# ---------------------------------------------------------------------------
# Cross-references
# ---------------------------------------------------------------------------

XREF_RE = re.compile(r"\[\[(ps|lab|ch):(\w+)(?:\|([^\]]+))?\]\]")


def book_chapter_numbers():
    """Chapter numbers as they appear in the book (lectures plus one impact chapter per part)."""
    numbers, k = {}, 0
    for p, (_, _, impact_slug) in enumerate(PARTS):
        for n, (slug, _, part, _) in LECTURES.items():
            if part == p:
                k += 1
                numbers[slug] = k
        k += 1
        numbers[impact_slug] = k
    return numbers


def problem_set_keys():
    """Homework segment -> cross-reference key: '4b' for split homeworks, else '4'."""
    splits = {hw for (hw, seg) in HOMEWORK if seg > 0}
    return {(hw, seg): f"{hw}{'ab'[seg]}" if hw in splits else str(hw) for (hw, seg) in HOMEWORK}


def resolve_xrefs(text, xref):
    """Replace [[ps:KEY]], [[lab:N]] and [[ch:LECTURE]] placeholders (optionally [[...|text]])."""
    def repl(m):
        kind, key, label = m.groups()
        if kind == "ps":
            if key not in xref["ps_chapter"]:
                raise SystemExit(f"Unknown problem set in TEXT_FIXES: {key}")
            label = label or f"Chapter {xref['ps_chapter'][key]} problem set"
            return f"{{ref}}`{label} <ps-hw{key}>`"
        if kind == "lab":
            if int(key) not in LABS:
                raise SystemExit(f"Unknown lab in TEXT_FIXES: {key}")
            label = label or f"Lab {key}"
            return f"{{doc}}`{label} </labs/{LABS[int(key)][1]}>`"
        slug = LECTURES[int(key)][0]
        label = label or f"Chapter {xref['chapters'][slug]}"
        return f"{{doc}}`{label} </chapters/{slug}>`"
    return XREF_RE.sub(repl, text)


# Spans fix_typos leaves alone: code fences (and fenced directives), math, inline code and roles,
# link targets, URLs and HTML tags.
TYPO_PROTECTED_RE = re.compile(
    r"^[ \t]*(`{3,}|~{3,}).*?^[ \t]*\1[ \t]*$|\$\$.*?\$\$|\$[^$\n]+\$|\\begin\{(\w+\*?)\}.*?\\end\{\2\}"
    r"|`[^`\n]*`|\]\([^)\s]*\)|https?://\S+|<[^>\n]+>",
    re.M | re.S)
TYPO_WORD_RE = re.compile(r"(?<![\w'])[A-Za-z]+(?:'[a-z]+)?(?![\w'])")


def _fix_words(text):
    def repl(m):
        word = m.group(0)
        new = TYPO_FIXES.get(word.lower())
        if new is None:
            return word
        if word.isupper() and len(word) > 1:
            return new.upper()
        return new[0].upper() + new[1:] if word[0].isupper() and new == new.lower() else new
    return TYPO_WORD_RE.sub(repl, text)


def fix_typos(text):
    """Correct the misspellings in TYPO_FIXES in the prose of `text`."""
    out, pos = [], 0
    for m in TYPO_PROTECTED_RE.finditer(text):
        out += [_fix_words(text[pos:m.start()]), m.group(0)]
        pos = m.end()
    return "".join(out + [_fix_words(text[pos:])])


# Links with no text ("[](url)") are invisible on the page.
TEXTLESS_LINK_RE = re.compile(r"\[\]\([^()\s]*\)")


def fix_markdown_cells(slug, cells, xref):
    md_cells = [c for c in cells if c.cell_type == "markdown"]
    for c, fixed in zip(md_cells, apply_text_fixes(slug, [c.source for c in md_cells], xref)):
        c.source = layout_fixes(TEXTLESS_LINK_RE.sub("", fix_typos(fixed)))
    code_cells = [c for c in cells if c.cell_type == "code"]
    for c, fixed in zip(code_cells, apply_text_fixes(slug, [c.source for c in code_cells], None, CODE_FIXES)):
        c.source = fixed


def apply_text_fixes(slug, sources, xref, fixes=TEXT_FIXES):
    """Apply TEXT_FIXES (or `fixes`) for one page to a list of sources; returns the new list.
    Cross-reference placeholders are resolved unless `xref` is None."""
    sources = list(sources)
    for fix in fixes:
        prefix, old, new = fix[:3]
        expected = fix[3] if len(fix) > 3 else 1
        if not slug.startswith(prefix):
            continue
        hits = sum(s.count(old) for s in sources)
        if hits != expected:
            raise SystemExit(f"TEXT_FIXES: expected {expected} match(es) in {slug}, found {hits}: {old!r}")
        sources = [s.replace(old, new) for s in sources]
    return sources if xref is None else [resolve_xrefs(s, xref) for s in sources]


# ---------------------------------------------------------------------------
# Impact chapters, TOC, landing assets
# ---------------------------------------------------------------------------

def impact_chapter(part_idx, summary_bits, reading_groups):
    numeral, part_title, slug = PARTS[part_idx]
    lines = [
        f"# Applications and Broader Impact: {part_title}",
        "",
        ":::{admonition} Draft chapter",
        ":class: warning",
        "This chapter collects the broader-impact discussion and readings that accompanied "
        f"Part {numeral} in AM207 (Harvard, Fall 2021). It will be expanded into a full chapter.",
        ":::",
        "",
    ]
    for bit in summary_bits:
        lines += [shift_headings(bit, 0, min_level=2), ""]
    if reading_groups:
        lines += [reading_markdown(reading_groups, heading="## Readings"), ""]
    return slug, "\n".join(lines)


def write_toc(impact_slugs, lab_slugs):
    lines = ["format: jb-book", "root: index", "defaults:", "  titlesonly: true", "parts:"]
    for p, (numeral, title, _) in enumerate(PARTS):
        lines += [f"  - caption: \"Part {numeral}: {title}\"", "    numbered: 2", "    chapters:"]
        for n, (slug, _, part, _) in LECTURES.items():
            if part == p:
                lines.append(f"    - file: chapters/{slug}")
        lines.append(f"    - file: chapters/{impact_slugs[p]}")
    lines += ["  - caption: Labs", "    chapters:"]
    lines += [f"    - file: labs/{slug}" for slug in lab_slugs]
    (ROOT / "_toc.yml").write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, type=Path, help="path to a checkout of onefishy/am207")
    ap.add_argument("--labs", required=True, type=Path,
                    help="folder holding Lab_1 ... Lab_9 (e.g. ~/Teaching/AM207_Lectures2020)")
    ap.add_argument("--only", type=int, nargs="*", help="lecture numbers to (re)generate")
    args = ap.parse_args()
    src = args.src.resolve()
    labs_src = args.labs.expanduser().resolve()
    only = set(args.only) if args.only else None

    if only is None:
        for d in (CHAPTERS, LABS_DIR, FIGURES, STATIC_FIGS, DATA):
            if d.exists():
                shutil.rmtree(d)
    for d in (CHAPTERS, LABS_DIR, FIGURES, STATIC_FIGS, DATA):
        d.mkdir(parents=True, exist_ok=True)

    assets = Assets([src / "Lectures", src / "HW", src / "Lectures" / "fig", src])
    for name in DATA_FILES:
        for sub in ("HW", "Lectures/datasets", "Labs/datasets"):
            p = src / sub / name
            if p.exists():
                shutil.copy2(p, DATA / name)
                break
    for rel in LAB_DATA:
        shutil.copy2(labs_src / rel, DATA / Path(rel).name)

    videos, lecture_readings, impact_readings = readings(src)
    lecture_summaries, impact_summaries = summary_cells(src, assets)

    chapter_numbers = book_chapter_numbers()
    ps_keys = problem_set_keys()
    ps_chapter = {ps_keys[k]: chapter_numbers[LECTURES[lec][0]] for k, lec in HOMEWORK.items()}
    xref = {"chapters": chapter_numbers, "ps_chapter": ps_chapter}

    hw_by_lecture = {}
    for (hw, seg), lec in HOMEWORK.items():
        hw_title, segments = homework_segments(src, hw, assets)
        if len(segments) > 1:
            # Split homeworks are titled by the problem each segment holds.
            for c in segments[seg]:
                m = re.search(r"^#\s+Problem Description:\s*(.+?)\s*$", c.source, re.M)
                if c.cell_type == "markdown" and m:
                    hw_title = m.group(1)
                    break
        hw_by_lecture.setdefault(lec, []).append((hw, ps_keys[(hw, seg)], hw_title, segments[seg]))

    for n, (slug, title, part, week) in LECTURES.items():
        if only and n not in only:
            continue
        nb, cells, labels = convert_lecture_notes(n, src, assets, videos.get(n))
        extras = lecture_summaries.get(n, [])
        recaps = [b for k, _, b in extras if k == "recap"]
        if recaps:
            cells.append(md("## Summary\n\n" + "\n\n".join(recaps)))
        for kind, sec_title, body in extras:
            if kind == "section":
                cells.append(md(f"## {sec_title}\n\n{body}"))
            elif kind == "section-cont":
                cells.append(md(body))
        if n in hw_by_lecture:
            cells.append(md("## Exercises\n\nThese problems were originally assigned as homework. "
                             "Data files are in the book's `data/` folder."))
            for hw, ps_key, hw_title, seg_cells in hw_by_lecture[n]:
                cells.append(md(f"(ps-hw{ps_key})=\n### Problem Set: {hw_title}"))
                cells += exercise_cells(src, hw, seg_cells, hw_title, assets,
                                        f"fig-{slug.split('-', 1)[0]}-hw{hw}", labels)
        if n in lecture_readings:
            cells.append(md(reading_markdown(lecture_readings[n])))

        fix_markdown_cells(slug, cells, xref)
        write_notebook(cells, CHAPTERS / f"{slug}.ipynb", slug.split("-", 1)[0])

    lab_assets = Assets([labs_src])
    lab_slugs = []
    for n in LABS:
        slug, cells = convert_lab(n, labs_src, lab_assets)
        fix_markdown_cells(slug, cells, xref)
        write_notebook(cells, LABS_DIR / f"{slug}.ipynb", slug)
        lab_slugs.append(slug)

    impact_slugs = {}
    for p in range(len(PARTS)):
        slug, text = impact_chapter(p, impact_summaries.get(p, []), impact_readings.get(p, []))
        text = fix_typos(apply_text_fixes(slug, [text], xref)[0])
        impact_slugs[p] = slug
        if only is None:
            (CHAPTERS / f"{slug}.md").write_text(text)
    write_toc(impact_slugs, lab_slugs)

    missing = assets.missing + lab_assets.missing
    if missing:
        print("Missing assets:", sorted(set(map(str, missing))))
    print(f"Wrote {len(list(CHAPTERS.glob('*')))} chapters and {len(lab_slugs)} labs")


if __name__ == "__main__":
    main()
