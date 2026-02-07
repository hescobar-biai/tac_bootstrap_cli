# Makefile for TAC Bootstrap CLI Development
# Provides convenient commands for development, testing, and building

# Variables
PYTHON := uv run python
PYTEST := uv run pytest
CLI := uv run tac-bootstrap
RUFF := uv run ruff
MYPY := uv run mypy

# Default target
.DEFAULT_GOAL := help

# Installation commands
install:  ## Install dependencies
	uv sync

install-dev:  ## Install with development dependencies
	uv sync --all-extras

# Development commands
dev:  ## Run CLI in development mode (smoke test)
	$(CLI) --help

lint:  ## Run ruff linter
	$(RUFF) check .

lint-fix:  ## Run ruff linter with auto-fix
	$(RUFF) check --fix .

format:  ## Format code with ruff
	$(RUFF) format .

typecheck:  ## Run mypy type checker
	$(MYPY) tac_bootstrap

# Testing commands
test:  ## Run all tests
	$(PYTEST) tests/

test-v:  ## Run tests with verbose output
	$(PYTEST) tests/ -v

test-cov:  ## Run tests with coverage report
	$(PYTEST) tests/ --cov=tac_bootstrap --cov-report=term-missing

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	@command -v ptw >/dev/null 2>&1 || { echo "pytest-watch not installed. Install with: uv pip install pytest-watch"; exit 1; }
	uv run ptw tests/

# Build commands
build:  ## Build package wheel
	uv build

clean:  ## Clean generated files and caches
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	@rm -rf dist/ build/ 2>/dev/null || true
	@echo "Cleaned all cache and build files"

# CLI example commands
cli-help:  ## Show CLI help
	$(CLI) --help

cli-version:  ## Show CLI version
	$(CLI) version

cli-init-dry:  ## Example: Run init command with dry-run
	@echo "Example dry-run of init command:"
	@echo "$(CLI) init my-project --dry-run"
	@echo ""
	@echo "Run the above command to test init in dry-run mode"

cli-doctor:  ## Example: Run doctor command
	@echo "Example doctor command:"
	@echo "$(CLI) doctor"
	@echo ""
	@echo "Note: Adjust based on actual CLI commands available"

# Orchestrator commands (TAC-14)
ORCH_BACKEND := apps/orchestrator_3_stream/backend
ORCH_FRONTEND := apps/orchestrator_3_stream/frontend
ORCH_DB_SCRIPT := scripts/setup_database.sh

orch-install:  ## Install orchestrator backend dependencies
	pip install fastapi uvicorn[standard] asyncpg psycopg2-binary pydantic

orch-install-frontend:  ## Install orchestrator frontend dependencies
	cd $(ORCH_FRONTEND) && npm install

orch-setup-db:  ## Run PostgreSQL migrations
	uv run apps/orchestrator_db/run_migrations.py

orch-gen-env:  ## Generate frontend .env from config.yml
	@python3 -c "\
	import yaml; \
	c = yaml.safe_load(open('config.yml'))['orchestrator']; \
	lines = [ \
	  f\"VITE_API_BASE_URL={c['api_base_url']}\", \
	  f\"VITE_WEBSOCKET_URL={c['ws_base_url']}/ws\", \
	  f\"VITE_PORT={c['frontend_port']}\", \
	  f\"VITE_POLLING_INTERVAL={c['polling_interval']}\", \
	]; \
	open('$(ORCH_FRONTEND)/.env', 'w').write('\n'.join(lines) + '\n'); \
	print('Generated $(ORCH_FRONTEND)/.env from config.yml')"

orch-dev:  ## Start orchestrator backend with hot reload
	@PORT=$$(python3 -c "import yaml; print(yaml.safe_load(open('config.yml')).get('orchestrator',{}).get('websocket_port',8000))" 2>/dev/null || echo 8000); \
	echo "Starting backend on port $$PORT"; \
	cd $(ORCH_BACKEND) && uvicorn main:app --reload --host 0.0.0.0 --port $$PORT

orch-dev-frontend:  ## Start orchestrator frontend dev server
	cd $(ORCH_FRONTEND) && npm run dev

orch-health:  ## Check orchestrator backend health
	@PORT=$$(python3 -c "import yaml; print(yaml.safe_load(open('config.yml')).get('orchestrator',{}).get('websocket_port',8000))" 2>/dev/null || echo 8000); \
	curl -s http://localhost:$$PORT/health | python3 -m json.tool 2>/dev/null || echo "Backend not running. Start with: make orch-dev"

# Utilities
help:  ## Show this help message
	@echo "TAC Bootstrap CLI - Available Make Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install             - Install dependencies"
	@echo "  make install-dev         - Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make dev                 - Run CLI in development mode (smoke test)"
	@echo "  make lint                - Run ruff linter"
	@echo "  make lint-fix            - Run ruff linter with auto-fix"
	@echo "  make format              - Format code with ruff"
	@echo "  make typecheck           - Run mypy type checker"
	@echo ""
	@echo "Testing:"
	@echo "  make test                - Run all tests"
	@echo "  make test-v              - Run tests with verbose output"
	@echo "  make test-cov            - Run tests with coverage report"
	@echo "  make test-watch          - Run tests in watch mode"
	@echo ""
	@echo "Build:"
	@echo "  make build               - Build package wheel"
	@echo "  make clean               - Clean generated files and caches"
	@echo ""
	@echo "CLI Examples:"
	@echo "  make cli-help            - Show CLI help"
	@echo "  make cli-version         - Show CLI version"
	@echo "  make cli-init-dry        - Example of init with dry-run"
	@echo "  make cli-doctor          - Example of doctor command"
	@echo ""
	@echo "Orchestrator (TAC-14):"
	@echo "  make orch-install        - Install backend dependencies"
	@echo "  make orch-install-frontend - Install frontend dependencies"
	@echo "  make orch-setup-db       - Initialize SQLite database"
	@echo "  make orch-gen-env        - Generate frontend .env from config.yml"
	@echo "  make orch-dev            - Start backend (port from config.yml)"
	@echo "  make orch-dev-frontend   - Start frontend dev server"
	@echo "  make orch-health         - Check backend health endpoint"
	@echo ""
	@echo "Utilities:"
	@echo "  make help                - Show this help message"

# Declare all targets as phony (not files)
.PHONY: install install-dev dev lint lint-fix format typecheck test test-v test-cov test-watch build clean cli-help cli-version cli-init-dry cli-doctor orch-install orch-install-frontend orch-setup-db orch-gen-env orch-dev orch-dev-frontend orch-health help
