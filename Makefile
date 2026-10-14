AM207_SRC ?= ../am207
LABS_SRC ?= $(HOME)/Teaching/AM207_Lectures2020
HW_SRC ?= $(HOME)/Teaching/AM207_HW2020
RERUN_DIR ?= _build/solution-runs
RERUN_PY ?= .venv-solutions/bin/python

.PHONY: build convert solutions clean

build:
	jupyter-book build --all .

# Regenerate chapters from the original course repo (overwrites chapters/).
convert:
	python scripts/convert_am207.py --src $(AM207_SRC) --labs $(LABS_SRC)

# Insert worked solutions into chapters/ and labs/ (run again after `make convert`).
# Re-runs fixed solution code with $(RERUN_PY) when its cached run is out of date.
solutions:
	python scripts/add_solutions.py --hw $(HW_SRC) --labs $(LABS_SRC) --rerun-dir $(RERUN_DIR) --rerun $(RERUN_PY) --report

clean:
	jupyter-book clean --all .
