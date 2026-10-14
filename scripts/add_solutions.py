"""Insert worked solutions into the problem sets and labs as collapsed dropdowns.

Usage:
    python scripts/add_solutions.py --hw ~/Teaching/AM207_HW2020 \
        --labs ~/Teaching/AM207_Lectures2020 --rerun-dir /tmp/solution-runs \
        [--rerun .venv-solutions/bin/python] [--only 06 lab-02] [--report]

Every answer comes from the author's solution notebooks; `scripts/solutions_map.py` says
which source cells answer which question. Each question gets one markdown cell, tagged
`solution`, holding a `::::{admonition} Solution: ...` dropdown with the prose, the code
(as a static block), its text output and its plots (saved under figures/solutions/).

Pages listed in RERUN have their code executed again (after bug fixes) in a separate
Python environment (scripts/requirements-solutions.txt); the code and outputs shown are
taken from that run. Executed notebooks are cached in --rerun-dir and reused until the
code changes; pass --rerun PYTHON to execute them.

The script is idempotent: it first removes every cell tagged `solution` (and the old lab
answer cells in LAB_REMOVE), then inserts the solutions again. Run it after
`make convert`, which rebuilds chapters/ and labs/ without solutions.
"""

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import nbformat

from am207_map import HOMEWORK, LECTURES
from convert_am207 import (CHAPTERS, FIGURES, LABS_DIR, ROOT, STATIC_FIGS, TEXT_WIDTH_PX, Assets,
                           book_chapter_numbers, clean_code_cell, clean_markdown, compress_image,
                           fence, headings_to_bold, isolate_display_math, problem_set_keys,
                           resolve_xrefs)
from solutions_map import GAPS, LAB_REMOVE, PROMPT_EDITS, RERUN, SOLUTIONS, SOURCES

SOLUTION_TAG = "solution"
SOLUTION_FIGS = FIGURES / "solutions"
MAX_OUTPUT_LINES = 30

# Course-specific references that must not reach the book (code is checked too).
LINT_RE = re.compile(
    r"Lecture\s*#?\d|\bHW\s*#?\d(?!_data)|Homework\s*#?\d|\bin class\b|\bin lecture\b|last week"
    r"|\bLab\s*#\d|Long Form|Fall 20\d\d|/Users/|/anaconda3|some of you|(?-i:\bNEED|\bTFs?\b)",
    re.I)
# Output reprs that carry no information for a reader.
NOISE_RE = re.compile(r"^(\[?<matplotlib|<Figure|Text\(|<[\w.]+ (object )?at 0x|\[<|<AxesSubplot|"
                      r"\(<Figure|\(-?\d[\d.e+-]*, -?\d[\d.e+-]*\)$|<graphviz)")
ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
CODE_FENCE_RE = re.compile(r"^(```.*?^```[ \t]*)$", re.M | re.S)


class Context:
    def __init__(self, hw, labs, rerun_dir, rerun_python):
        self.roots = {"hw": hw, "labs": labs}
        self.rerun_dir = rerun_dir
        self.rerun_python = rerun_python
        self.notebooks = {}
        self.runs = {}
        chapter_numbers = book_chapter_numbers()
        ps_keys = problem_set_keys()
        self.xref = {"chapters": chapter_numbers,
                     "ps_chapter": {ps_keys[k]: chapter_numbers[LECTURES[lec][0]]
                                    for k, lec in HOMEWORK.items()}}

    def source_path(self, src):
        root, rel = SOURCES[src]
        return self.roots[root] / rel

    def source(self, src):
        if src not in self.notebooks:
            self.notebooks[src] = nbformat.read(self.source_path(src), as_version=4)
        return self.notebooks[src]


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_path(page):
    return (LABS_DIR if page.startswith("lab-") else CHAPTERS) / f"{page}.ipynb"


def resolve_page(prefix):
    matches = sorted({e["page"] for e in SOLUTIONS} | set(PROMPT_EDITS) | set(LAB_REMOVE))
    hits = [p for p in matches if p == prefix or p.startswith(prefix + "-")]
    if len(hits) != 1:
        raise SystemExit(f"--only {prefix!r} matches {hits or 'no page'}")
    return hits[0]


# ---------------------------------------------------------------------------
# Segments -> markdown blocks
# ---------------------------------------------------------------------------

def apply_fixes(text, fixes, where):
    for fix in fixes:
        old, new = fix[:2]
        expected = fix[2] if len(fix) > 2 else 1
        hits = text.count(old)
        if hits != expected:
            raise SystemExit(f"{where}: expected {expected} match(es), found {hits}: {old!r}")
        text = text.replace(old, new)
    return text


def slice_text(text, start, end, where):
    if start is not None:
        i = text.find(start)
        if i < 0:
            raise SystemExit(f"{where}: start marker not found: {start!r}")
        text = text[i + len(start):]
    if end is not None:
        j = text.find(end)
        if j < 0:
            raise SystemExit(f"{where}: end marker not found: {end!r}")
        text = text[:j]
    return text


def prose(text, ctx, page, src, assets, labels):
    """Book-style markdown from a source markdown cell; code fences are left untouched."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"<a\s+(?:id|name)=['\"][^'\"]*['\"]\s*>\s*</a>", "", text)
    text = re.sub(r"^\s*-{3,}\s*$", "", text, flags=re.M)
    src_base = ctx.source_path(src).parent if src else ROOT
    parts = CODE_FENCE_RE.split(text)
    for i in range(0, len(parts), 2):
        t = clean_markdown(parts[i], assets, src_base, f"fig-{page.split('-')[0]}-sol", labels,
                           heading_delta=0, fig_dir=SOLUTION_FIGS / page, static_dir=STATIC_FIGS / "solutions" / page)
        parts[i] = headings_to_bold(t)
    return "\n\n".join(p.strip() for p in parts if p.strip())


def code_block(source):
    lines = [l for l in source.rstrip().split("\n") if not l.lstrip().startswith("%")]
    body = "\n".join(lines).strip("\n")
    return f"```python\n{body}\n```" if body.strip() else ""


def text_block(text):
    text = ANSI_RE.sub("", text).rstrip()
    lines = text.split("\n")
    if len(lines) > MAX_OUTPUT_LINES:
        head, tail = lines[:MAX_OUTPUT_LINES - 6], lines[-5:]
        lines = head + [f"[... {len(lines) - len(head) - len(tail)} lines omitted ...]"] + tail
    text = "\n".join(lines)
    ticks = "````" if "```" in text else "```"
    return f"{ticks}text\n{text}\n{ticks}"


def output_blocks(outputs, page, figkey, counter):
    """Markdown for a code cell's outputs: text in ```text blocks, PNGs as {image} files."""
    blocks, stream = [], []

    def flush():
        if "".join(stream).strip():
            blocks.append(text_block("".join(stream)))
        stream.clear()

    for o in outputs:
        kind = o.get("output_type")
        if kind == "stream":
            if o.get("name") == "stdout":
                stream.append(o.get("text", ""))
            continue
        if kind == "error":
            raise SystemExit(f"{page}/{figkey}: a source cell has an error output ({o.get('ename')})")
        data = o.get("data", {})
        if "image/png" in data:
            flush()
            counter[0] += 1
            blocks.append(save_png(data["image/png"], page, f"{figkey}-{counter[0]}"))
        elif "text/plain" in data:
            text = data["text/plain"]
            text = text if isinstance(text, str) else "".join(text)
            if not NOISE_RE.match(text.strip()):
                stream.append(text.rstrip("\n") + "\n")
    flush()
    return blocks


def save_png(b64, page, stem):
    dest_dir = SOLUTION_FIGS / page
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{stem}.png"
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / f"{stem}.png"
        raw.write_bytes(base64.b64decode(b64 if isinstance(b64, str) else "".join(b64)))
        width, _ = compress_image(raw, dest)
    lines = [f"```{{image}} ../figures/solutions/{page}/{dest.name}", f":alt: {stem.replace('-', ' ')}"]
    if width >= TEXT_WIDTH_PX:
        lines.append(":width: 100%")
    lines.append(":align: center")
    lines.append("```")
    return "\n".join(lines)


def figkey(title):
    key = re.sub(r"^Solution:?\s*", "", title)
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-") or "solution"


def render_segments(entry, ctx, assets, labels):
    page, title = entry["page"], entry["title"]
    where = f"{page} / {title}"
    blocks = []
    counter = [0]
    key = entry.get("key") or figkey(title)
    for seg in entry["segments"]:
        kind = seg[0]
        if kind == "md":
            _, src, cell, start, end, fixes = seg
            c = ctx.source(src).cells[cell]
            if c.cell_type != "markdown":
                raise SystemExit(f"{where}: {src} cell {cell} is not markdown")
            text = slice_text(c.source.replace("\r\n", "\n"), start, end, f"{where} ({src} c{cell})")
            text = apply_fixes(text, fixes, f"{where} ({src} c{cell})")
            blocks.append(("prose", prose(text, ctx, page, src, assets, labels)))
        elif kind == "code":
            _, src, cell, show_out, fixes = seg
            c = ctx.source(src).cells[cell]
            if c.cell_type != "code":
                raise SystemExit(f"{where}: {src} cell {cell} is not code")
            source = clean_code_cell(c).source
            source = apply_fixes(source, fixes, f"{where} ({src} c{cell})")
            blocks.append(("code", code_block(source)))
            if show_out:
                blocks += [("out", b) for b in output_blocks(c.get("outputs", []), page, key, counter)]
        elif kind == "ran":
            _, step, show_code, show_out = seg
            source, outputs = ctx.runs[page][step]
            if show_code:
                blocks.append(("code", code_block(source)))
            if show_out:
                blocks += [("out", b) for b in output_blocks(outputs, page, key, counter)]
        elif kind == "text":
            blocks.append(("prose", prose(seg[1], ctx, page, None, assets, labels)))
        elif kind == "note":
            blocks.append(("prose", f"*Not covered here: {seg[1]}*"))
        else:
            raise SystemExit(f"{where}: unknown segment kind {kind!r}")
    parts = []
    for kind, text in blocks:
        if not text.strip():
            continue
        if kind == "prose":
            text = isolate_display_math(text)
        parts.append(text.strip())
    body = "\n\n".join(parts)
    lint(body, where)
    body = resolve_xrefs(body, ctx.xref)
    depth = 5 if re.search(r"^::::", body, re.M) else 4
    return "\n".join([f"{fence(depth)}{{admonition}} {title}", ":class: dropdown", "", body, fence(depth)])


def lint(text, where):
    hits = sorted({m.group(0) for m in LINT_RE.finditer(text)})
    if hits:
        raise SystemExit(f"{where}: course-specific text left in the solution: {hits}")


# ---------------------------------------------------------------------------
# Re-runs
# ---------------------------------------------------------------------------

RUN_SETUP = """\
%matplotlib inline
%config InlineBackend.figure_format = 'png'
import warnings
warnings.filterwarnings('ignore')
import numpy as np
np.random.seed(207)"""

EXECUTE = """\
import sys, nbformat
from nbclient import NotebookClient
nb = nbformat.read(sys.argv[1], as_version=4)
NotebookClient(nb, timeout=None, kernel_name='python3', resources={'metadata': {'path': sys.argv[2]}}).execute()
nbformat.write(nb, sys.argv[1])
"""


def run_program(page, ctx, book):
    """The (key, source) cells to execute for a page, in order."""
    cells = [(None, RUN_SETUP)]
    for step in RERUN[page]:
        kind = step[0]
        if kind == "book":
            matches = [c for c in book.cells if c.get("id") == step[1]]
            if len(matches) != 1:
                raise SystemExit(f"RERUN {page}: no book cell with id {step[1]}")
            cells.append((None, matches[0].source))
        elif kind == "src":
            _, key, src, cell, fixes = step
            c = ctx.source(src).cells[cell]
            source = apply_fixes(clean_code_cell(c).source, fixes, f"RERUN {page} {key} ({src} c{cell})")
            cells.append((key, source))
        elif kind == "lit":
            cells.append((step[1], step[2]))
        else:
            raise SystemExit(f"RERUN {page}: unknown step {kind!r}")
    keys = [k for k, _ in cells if k]
    if len(keys) != len(set(keys)):
        raise SystemExit(f"RERUN {page}: duplicate step keys")
    return cells


def load_run(page, ctx, book):
    cells = run_program(page, ctx, book)
    digest = hashlib.sha256(json.dumps(cells).encode()).hexdigest()
    path = ctx.rerun_dir / f"{page}.ipynb"
    nb = nbformat.read(path, as_version=4) if path.exists() else None
    if nb is None or nb.metadata.get("solutions_digest") != digest:
        if not ctx.rerun_python:
            raise SystemExit(f"{page}: no up-to-date run in {ctx.rerun_dir}; pass --rerun PYTHON")
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_code_cell(src) for _, src in cells]
        nb.metadata["solutions_digest"] = digest
        nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
        ctx.rerun_dir.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, path)
        print(f"  executing {path.name} ...", flush=True)
        subprocess.run([str(ctx.rerun_python), "-c", EXECUTE, str(path), str(page_path(page).parent)],
                       check=True)
        nb = nbformat.read(path, as_version=4)
    for c in nb.cells:
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                raise SystemExit(f"{page}: run failed: {o.get('ename')}: {o.get('evalue')}")
    ctx.runs[page] = {key: (src, nb.cells[i].get("outputs", []))
                      for i, (key, src) in enumerate(cells) if key}


# ---------------------------------------------------------------------------
# Notebook edits
# ---------------------------------------------------------------------------

def apply_prompt_edits(page, nb):
    for old, new in PROMPT_EDITS.get(page, []):
        cells = [c for c in nb.cells if c.cell_type == "markdown"]
        if any(new in c.source for c in cells):
            continue  # already applied
        hits = [c for c in cells if old in c.source]
        if len(hits) != 1 or hits[0].source.count(old) != 1:
            raise SystemExit(f"PROMPT_EDITS {page}: expected exactly one match for {old!r}")
        hits[0].source = hits[0].source.replace(old, new)


def find_anchor(nb, page, anchor):
    hits = [i for i, c in enumerate(nb.cells) if anchor in c.source
            and SOLUTION_TAG not in c.metadata.get("tags", [])]
    if len(hits) != 1:
        raise SystemExit(f"{page}: anchor {anchor!r} matches {len(hits)} cells")
    return hits[0]


def process_page(page, ctx):
    path = page_path(page)
    nb = nbformat.read(path, as_version=4)
    remove = set(LAB_REMOVE.get(page, []))
    nb.cells = [c for c in nb.cells if SOLUTION_TAG not in c.metadata.get("tags", [])
                and c.get("id") not in remove]
    apply_prompt_edits(page, nb)
    if page in RERUN:
        load_run(page, ctx, nb)

    shutil.rmtree(SOLUTION_FIGS / page, ignore_errors=True)
    shutil.rmtree(STATIC_FIGS / "solutions" / page, ignore_errors=True)
    assets = Assets([])
    labels = set()
    by_anchor = {}
    for entry in (e for e in SOLUTIONS if e["page"] == page):
        idx = find_anchor(nb, page, entry["after"])
        by_anchor.setdefault(idx, []).append(render_segments(entry, ctx, assets, labels))
    if assets.missing:
        raise SystemExit(f"{page}: missing images {assets.missing}")

    cells = []
    for i, c in enumerate(nb.cells):
        cells.append(c)
        for k, text in enumerate(by_anchor.get(i, []), start=1):
            cell = nbformat.v4.new_markdown_cell(text)
            cell.metadata["tags"] = [SOLUTION_TAG]
            cell.id = f"{c.id}-s{k}"
            cells.append(cell)
    nb.cells = cells
    nbformat.validate(nb)
    nbformat.write(nb, path)
    return sum(len(v) for v in by_anchor.values())


def report():
    print("\nQuestions without a worked solution:")
    for page, items in GAPS.items():
        print(f"  {page}: {'; '.join(items)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hw", required=True, type=Path, help="folder holding HW_0 ... HW_9 (with solutions)")
    ap.add_argument("--labs", required=True, type=Path, help="folder holding Lab_1 ... Lab_9")
    ap.add_argument("--rerun-dir", required=True, type=Path, help="where executed re-run notebooks are cached")
    ap.add_argument("--rerun", type=Path, help="Python with scripts/requirements-solutions.txt installed")
    ap.add_argument("--only", nargs="*", help="page prefixes to process, e.g. 06 lab-02")
    ap.add_argument("--report", action="store_true", help="list the questions without solutions")
    args = ap.parse_args()
    ctx = Context(args.hw.expanduser().resolve(), args.labs.expanduser().resolve(),
                  args.rerun_dir.expanduser().resolve(), args.rerun)
    pages = sorted({e["page"] for e in SOLUTIONS} | set(PROMPT_EDITS) | set(LAB_REMOVE))
    if args.only:
        pages = [resolve_page(p) for p in args.only]
    for page in pages:
        n = process_page(page, ctx)
        print(f"{page}: {n} solution(s)")
    if args.report:
        report()


if __name__ == "__main__":
    main()
