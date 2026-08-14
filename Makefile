.PHONY: help install test test-watch test-cov lint clean run

help:
	@echo "Available commands:"
	@echo "  make install     Install dependencies into the venv"
	@echo "  make test        Run the full test suite once"
	@echo "  make test-watch  Auto-run tests on every file save (TDD loop)"
	@echo "  make test-cov    Run tests with a coverage report"
	@echo "  make lint        Check code style (flake8)"
	@echo "  make clean       Remove caches and temp files"
	@echo "  make run         Start the bot"

install:
	pip install -r requirements.txt

test:
	pytest -v

test-watch:
	ptw -- -v

test-cov:
	pytest --cov=bot --cov=db --cov-report=term-missing

lint:
	flake8 bot db tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov

run:
	python -m bot.main

terminal:
	python -m terminal_ui.terminal_main