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
| `figures/` | Images used by `{figure}` directives |
| `_static/figs/` | Videos, and images embedded in raw HTML tables |
| `data/` | Datasets used by the chapters and exercises |
| `scripts/convert_am207.py` | One-time converter from the course repo |
| `scripts/am207_map.py` | Every editorial mapping the converter uses (which summary cell goes where, and so on) |

## How the chapters were generated (Phase 1)

`make convert AM207_SRC=/path/to/am207 LABS_SRC=/path/to/AM207_Lectures2020` regenerates `chapters/`, `labs/`, `figures/`, `_static/figs/`, `data/` and `_toc.yml` from a checkout of the course repo and the folder of `Lab_1` … `Lab_9` notebooks. For each lecture, the converter:

- turns the RISE slide notebook into a chapter: it strips slide metadata, the course header and logo, and repeated slide titles, and makes the outline an "In this chapter" box;
- renders cells that were hidden from the slides (`skip`) as collapsible "Going deeper" boxes;
- makes bare `\begin{aligned}`/`align` blocks render by wrapping them in `$$`, and converts standalone `<img>` tags to `{figure}` directives;
- appends the lecture summary, the week's reading list, and the matching homework problems. Starter code is kept; solutions are never included;
- transcodes the `.mov` animations to small H.264 `.mp4` files and shrinks oversized images.

Summary cells and reading groups are routed through the tables in `scripts/am207_map.py`, which also records what was dropped as course logistics. That file also holds:

- `LABS`: which notebook each lab comes from, and which of its cells are worked answers (collapsed in the book). Lab solution notebooks and `Lab_8/alpha_hmc.py` are not included.
- `TEXT_FIXES`: exact-text edits applied after conversion. They point references to homework, in-class exercises and labs at the matching problem set, lab or chapter. Links are written as placeholders (`[[ps:4b]]`, `[[lab:6]]`, `[[ch:14]]`), which the converter turns into links with the right chapter numbers. The converter stops if a fix no longer matches exactly.

**Do not re-run the converter once chapters have been edited by hand.** It rebuilds `chapters/` from scratch. `--only N ...` regenerates just the listed lectures.

## Revising a chapter (Phase 2)

One chapter per pull request:

1. Rewrite the slide-style prose as book prose. Open with Context / Challenge / Outline.
2. Port the code from `autograd`/`pymc3` to JAX/NumPyro, and move shared helpers into a common module.
3. Re-execute the notebook so its saved outputs come from the new code. Once every chapter is ported, set `execute_notebooks: cache` in `_config.yml`.
4. Replace bare links with `{cite}` entries in `references.bib`, and use `{numref}` for figures. Every figure already has a `name:` label.
5. Remove references to in-class exercises that are not part of the book.

## License

[CC BY-NC-SA 4.0](LICENSE)
