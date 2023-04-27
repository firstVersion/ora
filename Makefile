.PHONY: tests clean cov
tests: ## run tests with poetry
	poetry run isort .
	poetry run black .
	poetry run flake8 .
	poetry run mypy src
	poetry run python -m pytest
clean:
	rm -r htmlcov
cov:
	poetry run python -m pytest --cov=src --cov-branch --cov-report=term-missing
htmlcov:
	poetry run python -m pytest -v --cov=src --cov-branch --cov-report=html