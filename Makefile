all: format

.PHONY: \
		all \
		check \
		clean \
		format

define checkDirectories
mkdir --parents $(@D)
endef

check:
	black --check --line-length 100 src
	flake8 --max-line-length 100 src
	mypy src

clean:
	rm --force --recursive .*_cache

format:
	black --line-length 100 src

reports/figures/ValoresNulos2016.pdf:
	$(checkDirectories)
	python data_cleaning.py
