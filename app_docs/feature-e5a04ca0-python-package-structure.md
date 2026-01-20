# Python Package Base Structure

**ADW ID:** e5a04ca0
**Date:** 2026-01-20
**Specification:** specs/issue-1-adw-e5a04ca0-sdlc_planner-python-package-structure.md

## Overview

This feature establishes the foundational Python package structure for the TAC Bootstrap CLI tool. It creates a well-organized, modern Python package layout following Domain-Driven Design (DDD) architecture principles with clear separation of concerns across domain, application, infrastructure, and interface layers.

## What Was Built

- Complete Python package structure under `tac_bootstrap_cli/`
- Modern `pyproject.toml` configuration following PEP 621 standards
- DDD architecture with four distinct layers: domain, application, infrastructure, interfaces
- Minimal CLI interface using Typer framework
- Test infrastructure with pytest
- Package versioning system
- Entry point configuration for multiple invocation methods

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/pyproject.toml`: Project metadata, dependencies, and build configuration
- `tac_bootstrap_cli/tac_bootstrap/__init__.py`: Package initialization with version string
- `tac_bootstrap_cli/tac_bootstrap/__main__.py`: Module entry point for `python -m tac_bootstrap`
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Typer-based CLI with version command
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py`: Domain layer initialization (empty)
- `tac_bootstrap_cli/tac_bootstrap/application/__init__.py`: Application layer initialization (empty)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/__init__.py`: Infrastructure layer initialization (empty)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/__init__.py`: Interface layer initialization (empty)
- `tac_bootstrap_cli/tests/__init__.py`: Tests directory initialization (empty)
- `tac_bootstrap_cli/tests/test_version.py`: Version verification tests
- `tac_bootstrap_cli/tests/test_cli.py`: CLI smoke tests
- `tac_bootstrap_cli/README.md`: Basic package documentation
- `tac_bootstrap_cli/uv.lock`: Dependency lock file

### Key Changes

- **DDD Architecture**: Created four-layer architecture (domain, application, infrastructure, interfaces) for clear separation of concerns and maintainability
- **Modern Python Packaging**: Used `pyproject.toml` with hatchling build backend following PEP 621 standards
- **Dependency Management**: Configured core dependencies (typer, rich, jinja2, pydantic, pyyaml) and dev dependencies (pytest, pytest-cov, mypy, ruff)
- **Multiple Entry Points**: Configured CLI to work as `tac-bootstrap`, `python -m tac_bootstrap`, or `uv run tac-bootstrap`
- **Version Management**: Centralized version in `__init__.py` and accessible via CLI command

## How to Use

### Installation

From the `tac_bootstrap_cli/` directory:

```bash
# Install in development mode with uv
uv pip install -e .

# Or install with dev dependencies
uv pip install -e ".[dev]"
```

### Running the CLI

```bash
# Show version
tac-bootstrap version

# Or using module syntax
python -m tac_bootstrap version

# Or using uv run
uv run tac-bootstrap version
```

### Running Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v
```

## Configuration

### Package Configuration (pyproject.toml)

- **Name**: `tac-bootstrap`
- **Version**: `0.1.0`
- **Python Requirement**: `>=3.10`
- **License**: MIT
- **Build System**: hatchling

### Dependencies

**Core Dependencies:**
- `typer>=0.9.0` - CLI framework
- `rich>=13.7.0` - Terminal formatting
- `jinja2>=3.1.2` - Template engine
- `pydantic>=2.5.0` - Data validation
- `pyyaml>=6.0.1` - YAML parsing

**Development Dependencies:**
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `mypy>=1.7.0` - Type checking
- `ruff>=0.1.0` - Linting and formatting

## Testing

```bash
# Run all tests
cd tac_bootstrap_cli && uv run pytest tests/ -v

# Run specific test
cd tac_bootstrap_cli && uv run pytest tests/test_version.py -v

# Run with coverage
cd tac_bootstrap_cli && uv run pytest tests/ -v --cov=tac_bootstrap
```

## Architecture

The package follows Domain-Driven Design (DDD) principles:

```
tac_bootstrap/
├── domain/          # Business models and entities (Pydantic models)
├── application/     # Use cases and business logic services
├── infrastructure/  # External systems (file I/O, templates, etc.)
├── interfaces/      # User interaction layer (CLI commands)
└── templates/       # Jinja2 templates for code generation
```

## Notes

- This is TAREA 1.1 from `PLAN_TAC_BOOTSTRAP.md` (Phase 1: Setup del Proyecto)
- The structure provides a solid foundation for incremental development
- Templates directory intentionally omits `__init__.py` as it's a data directory
- The CLI currently only has a version command; additional commands will be added in subsequent features
- Next step (TAREA 1.2) will implement core CLI commands and generation logic
- Entry point is configured for three invocation methods: direct command, module execution, and uv run
