AM207_SRC ?= ../am207
LABS_SRC ?= $(HOME)/Teaching/AM207_Lectures2020

.PHONY: build convert clean

build:
	jupyter-book build --all .

# Regenerate chapters from the original course repo (overwrites chapters/).
convert:
	python scripts/convert_am207.py --src $(AM207_SRC) --labs $(LABS_SRC)

clean:
	jupyter-book clean --all .
