# Probabilistic Inference & Optimization

An online textbook adapted from [AM207: Stochastic Methods for Data Analysis, Inference and Optimization](https://github.com/onefishy/am207) (Harvard, Fall 2021), built with [Jupyter Book](https://jupyterbook.org) v1.

Published at https://onefishy.github.io/probabilistic-inference-and-optimization/

## Building locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-book.txt
make build            # jupyter-book build --all .
open _build/html/index.html
```

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the book and publishes `_build/html` to the `gh-pages` branch. In the repository settings, set Pages to deploy from the `gh-pages` branch.

## Layout

| Path | Contents |
|---|---|
| `chapters/NN-*.ipynb` | One chapter per original lecture: notes, summary, exercises, further reading |
| `chapters/impact-*.md` | The "Applications and Broader Impact" chapter that closes each part (drafts) |
| `labs/lab-NN-*.ipynb` | Lab 1–9, from the AM207 `Lab_N` folders; worked solutions collapsed |
| `figures/solutions/` | Plots shown in the worked solutions (written by `scripts/add_solutions.py`) |
| `figures/` | Images used by `{figure}` directives |
| `_static/figs/` | Videos, and images embedded in raw HTML tables |
| `data/` | Datasets used by the chapters and exercises |
| `scripts/convert_am207.py` | One-time converter from the course repo |
| `scripts/am207_map.py` | Every editorial mapping the converter uses (which summary cell goes where, and so on) |
| `scripts/add_solutions.py` | Inserts the worked solutions into the problem sets and labs |
| `scripts/solutions_map.py` | Which solution-notebook cells answer which question, and every edit made to them |
| `scripts/requirements-solutions.txt` | Environment for re-running the corrected solution code |

## How the chapters were generated (Phase 1)

`make convert AM207_SRC=/path/to/am207 LABS_SRC=/path/to/AM207_Lectures2020` regenerates `chapters/`, `labs/`, `figures/`, `_static/figs/`, `data/` and `_toc.yml` from a checkout of the course repo and the folder of `Lab_1` … `Lab_9` notebooks. For each lecture, the converter:

- turns the RISE slide notebook into a chapter: it strips slide metadata, the course header and logo, and repeated slide titles, and makes the outline an "In this chapter" box;
- renders cells that were hidden from the slides (`skip`) as collapsible "Going deeper" boxes;
- makes bare `\begin{aligned}`/`align` blocks render by wrapping them in `$$`, and converts standalone `<img>` tags to `{figure}` directives;
- fixes Markdown that MyST renders wrongly (`layout_fixes`): lines under a numbered item are re-indented to the item's text column, so follow-on paragraphs and sub-lists written with two-space indents stay inside the item instead of rendering flush left; display equations inside a paragraph get their own paragraph; numbered lists starting at 0 get a blank line before them; and `- | -` table rows become `--- | ---`. A change is kept only if it leaves the page's lists, code blocks and equations intact;
- removes links with no text and drops the link (not the title) from readings behind the Harvard library proxy;
- appends the lecture summary, the week's reading list, and the matching homework problems. Starter code is kept; solutions are added afterwards (see [Worked solutions](#worked-solutions));
- transcodes the `.mov` animations to small H.264 `.mp4` files and shrinks oversized images.

Summary cells and reading groups are routed through the tables in `scripts/am207_map.py`, which also records what was dropped as course logistics. That file also holds:

- `LABS`: which notebook each lab comes from, and which of its cells are worked answers. `scripts/add_solutions.py` later merges them into one collapsed dropdown per question.
- `TEXT_FIXES`: exact-text edits applied after conversion. They point references to homework, in-class exercises, lectures and labs at the matching problem set, lab or chapter, and reword course framing ("this class", "today", "last week", "Problem 2") for a book. Links are written as placeholders (`[[ps:4b]]`, `[[lab:6]]`, `[[ch:14]]`, where `ch` takes the lecture number), which the converter turns into links with the right chapter numbers. The converter stops if a fix no longer matches exactly. `CODE_FIXES` does the same for code cells.
- `TYPO_FIXES`: misspelled words and their corrections. They are applied to prose only, never to code, math or URLs, both here and in the worked solutions.

**Do not re-run the converter once chapters have been edited by hand.** It rebuilds `chapters/` from scratch. `--only N ...` regenerates just the listed lectures. After a conversion, run `make solutions` to put the worked solutions back.

## Worked solutions

Every problem-set and lab question that has an answer in the author's solution notebooks (`~/Teaching/AM207_HW2020` and the lab folders) gets one collapsed "Solution" dropdown right after the question. It holds the prose, the code (as a static block), the text output and the plots (saved under `figures/solutions/`).

`make solutions` (re)inserts them; it is idempotent. `scripts/solutions_map.py` records which source cells each dropdown comes from and every edit made to them:

- Only the author's own answers are used. Questions without one get no dropdown; `python scripts/add_solutions.py ... --report` lists them (`GAPS`). Partial answers end with a "*Not covered here: …*" line.
- Bugs in the source solutions are fixed and the affected code is re-run (`RERUN`), so the code, numbers and plots agree. Sentences that the corrected output contradicts are left out rather than rewritten.
- Re-runs use a separate environment: `python3.11 -m venv .venv-solutions && .venv-solutions/bin/pip install -r scripts/requirements-solutions.txt`. Executed notebooks are cached in `_build/solution-runs` and reused until the code changes. Code that needs `pymc3` is not re-run; its saved outputs are shown.

## Revising a chapter (Phase 2)

One chapter per pull request:

1. Rewrite the slide-style prose as book prose. Open with Context / Challenge / Outline.
2. Port the code from `autograd`/`pymc3` to JAX/NumPyro, and move shared helpers into a common module.
3. Re-execute the notebook so its saved outputs come from the new code. Once every chapter is ported, set `execute_notebooks: cache` in `_config.yml`.
4. Replace bare links with `{cite}` entries in `references.bib`, and use `{numref}` for figures. Every figure already has a `name:` label.
5. Remove references to in-class exercises that are not part of the book.

## License

[CC BY-NC-SA 4.0](LICENSE)
