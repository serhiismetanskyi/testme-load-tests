.PHONY: help install test test-html lint format format-check fix clean all \
	docker-build docker-test docker-test-html docker-shell docker-clean

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

test: ## Run Locust load tests (without HTML/CSV reports)
	mkdir -p logs
	uv run python -m locust --config=config.yml

test-html: ## Run Locust load tests with HTML and CSV reports
	mkdir -p reports logs
	rm -rf reports/* 2>/dev/null || true
	uv run python -m locust --config=config.yml --html=reports/report.html --csv=reports/stats

lint: ## Run linter
	uv run ruff check .

fix: ## Fix linting issues automatically
	uv run ruff check --fix .
	uv run ruff format .

format: ## Format code
	uv run ruff format .

format-check: ## Check formatting without modifying files
	uv run ruff format --check .

clean: ## Remove cache artifacts, reports, and logs
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .ruff_cache
	rm -rf .vscode
	rm -rf reports
	rm -rf logs
	@echo "Cleanup complete!"

all: install format lint test

docker-build: ## Build Docker image
	mkdir -p logs
	docker compose build

docker-test: ## Run load tests in Docker (without HTML/CSV reports)
	mkdir -p logs
	docker compose run --rm -v $(CURDIR)/logs:/app/logs -v $(CURDIR)/data:/app/data tests uv run python -m locust --config=config.yml

docker-test-html: ## Run load tests in Docker with HTML and CSV reports
	mkdir -p reports logs
	rm -rf reports/* 2>/dev/null || true
	docker compose run --rm -v $(CURDIR)/logs:/app/logs -v $(CURDIR)/reports:/app/reports -v $(CURDIR)/data:/app/data tests uv run python -m locust --config=config.yml --html=reports/report.html --csv=reports/stats

docker-shell: ## Open shell in Docker container
	mkdir -p logs
	docker compose run --rm -v $(CURDIR)/logs:/app/logs -v $(CURDIR)/data:/app/data tests /bin/bash

docker-clean: ## Remove Docker containers and images
	docker compose down --rmi local --volumes --remove-orphans || true

