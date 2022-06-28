all: check coverage tests

.PHONY: \
	check \
	clean \
	format \
	mutants \
	setup \
	tests

check:
		black --check --line-lenght 100 src
		black --check --line-length 100 tests
		flake8 --max-line-length 100 src
		flake8 --max-line-length 100 tests
		mypy src
		mypy tests

clean:
		rm --force --recursive .*_cache
		rm --force --recursive tests/__pycache__
		rm --force .mutmut-_cache
		rm --force coverage.xml

format: 
		black --line-lenght 100 src
		black --line-lenght 100 tests

mutants: setup tests
		mutmut --paths-to-mutate src

setup: clean
		pip install --editable .

tests: 
		pytests --verbose
