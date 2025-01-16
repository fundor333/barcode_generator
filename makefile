include .env

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the stuff
	@poetry install
	@poetry run pre-commit install
	@poetry run pre-commit autoupdate


run: ## Run example
	@poetry run python bcgenerator.py 3148957871155 example
	@poetry run python bcgenerator_pdf.py example.csv example.pdf
