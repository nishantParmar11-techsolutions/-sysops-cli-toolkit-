# ==============================================================================
# SysOps CLI Toolkit - Elite Enterprise Automation Makefile
# ==============================================================================

.PHONY: help setup test lint format typecheck clean

# Environment Paths & Binaries
PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip
PYTEST = ./venv/bin/pytest
FLAKE8 = ./venv/bin/flake8
RUFF = ./venv/bin/ruff
MYPY = ./venv/bin/mypy
BLACK = ./venv/bin/black

default: help

help:
	@echo "=================================================="
	@echo " SysOps CLI Toolkit - Enterprise Command Reference"
	@echo "=================================================="
	@echo "  make setup     - Create venv and install pinned dependencies"
	@echo "  make test      - Run PyTest suite with coverage metrics"
	@echo "  make lint      - Run Flake8 and Ruff static code analysis"
	@echo "  make format    - Auto-format code with Black and Ruff"
	@echo "  make typecheck - Run strict Mypy type analysis"
	@echo "  make clean     - Purge cache files, build artifacts, and venv"
	@echo "=================================================="

setup:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✨ Enterprise virtual environment and dependencies successfully configured!"

test:
	$(PYTEST) -v --cov=. --cov-report=term-missing --tb=short

lint:
	$(FLAKE8) . --count --select=E9,F63,F7,F82 --show-source
	$(RUFF) check .

format:
	$(BLACK) .
	$(RUFF) format .
	$(RUFF) check --fix .
	@echo "✨ Code formatting and auto-fixes applied successfully!"

typecheck:
	$(MYPY) main.py test_main.py

clean:
	rm -rf __pycache__ .pytest_cache .coverage .mypy_cache htmlcov venv
	find . -type f -name "*.pyc" -delete
	@echo "🧹 Workspace and virtual environment wiped clean!"
