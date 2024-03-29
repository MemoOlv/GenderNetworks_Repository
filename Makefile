all: check coverage tests

module = gender_energy_networks

.PHONY: \
	check \
	clean \
	coverage \
	format \
	mutants \
	setup \
	tests

check:
		black --check --line-length 100 src
		black --check --line-length 100 tests
		black --check --line-length 100 ${module}
		flake8 --max-line-length 100 src
		flake8 --max-line-length 100 tests
		flake8 --max-line-length 100 ${module}
		mypy src
		mypy tests
		mypy ${module}

clean:
		rm --force --recursive .*_cache
		rm --force --recursive tests/__pycache__
		rm --force .mutmut-_cache
		rm --force coverage.xml

coverage: setup
		pytest --cov=${module} --cov-report=term-missing --verbose


format: 
		black --line-length 100 src
		black --line-length 100 tests
		black --line-length 100 ${module}

mutants: setup tests
		mutmut --paths-to-mutate src
		mutmut --paths-to-mutate ${module}

setup: clean
		pip install --editable .

tests: setup
		pytest --verbose
