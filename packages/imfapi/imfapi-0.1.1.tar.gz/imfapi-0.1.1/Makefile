.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	@rm -fr build/
	@rm -fr dist/
	@rm -fr .eggs/
	@find . -name '*.egg-info' -exec rm -fr {} +
	@find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	@rm -fr .tox/
	@rm -f .coverage
	@rm -fr htmlcov/
	@rm -fr .pytest_cache

format: ## formats code with ruff
	@uvx ruff format .

lint: ## check style with ruff
	@uvx ruff check .

test: ## run tests quickly with the default Python
	@uv run pytest -vv --cov=src/imfapi --cov-report=term-missing

# requirements: requirements-dev ## creates requirements.txt and requirements-dev.txt from poetry.lock
# 	@poetry export -f requirements.txt --output requirements.txt --without-hashes

# requirements-dev: ## creates requirements-dev.txt from poetry.lock
# 	@poetry export -f requirements.txt --output requirements-dev.txt --only dev --without-hashes

# install: ## install the project locally
# 	@poetry install

build: clean ## builds source and wheel package
	@uv build

# patch:					## Bump version to next patch
# 	@poetry version patch

# minor:					## Bump version to next minor
# 	@poetry version minor

# major:					## Bump version to next major
# 	@poetry version major

# prerelease:					## Create prerelase version
# 	@poetry version prerelease

publish: build			## publish new version to pypi (private)
	@uv publish --token=$(UV_PUBLISH_TOKEN)
