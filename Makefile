.PHONY: tests
tests: ## run tests with poetry
	poetry run isort .
	poetry run black .
	poetry run flake8 .
	poetry run mypy src
	poetry run python -m pytest