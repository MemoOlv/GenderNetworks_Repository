all: reports/figures/ValoresNulos2016.pdf

.PHONY: \
		all \
		check \
		clean \
		format

define checkDirectories
mkdir --parents $(@D)
endef

check:
	black --check --line-length 100 .*py
	flake8 --max-line-length 100 .*py
	mypy src

clean:
	rm --force --recursive .*_cache

format:
	black --line-length 100 *.py

reports/figures/ValoresNulos2016.pdf:
	$(checkDirectories)
	python data_cleaning.py
