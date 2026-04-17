.PHONY: fmt lint test cov smoke clean install

install:
	pip install -e ".[dev]"
	pre-commit install

fmt:
	black .
	ruff check --fix .

lint:
	ruff check .
	black --check .
	mypy .
	bandit -r . -x tests,_legacy,data/cache

test:
	pytest -q

cov:
	pytest --cov --cov-report=term-missing --cov-fail-under=80

smoke:
	python -m backtest.engine --symbol BTCUSDT --start 2023-01-01 --end 2023-12-31 --smoke

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage build dist *.egg-info
