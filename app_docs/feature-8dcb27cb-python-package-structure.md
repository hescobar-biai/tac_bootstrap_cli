---
doc_type: feature
adw_id: 8dcb27cb
date: 2026-01-27
idk:
  - python-package
  - ddd-architecture
  - pyproject-toml
  - mit-license
  - dependency-management
  - cli-entry-point
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/pyproject.toml
  - tac_bootstrap_cli/LICENSE
  - tac_bootstrap_cli/tac_bootstrap/__init__.py
---

# Python Package Base Structure

**ADW ID:** 8dcb27cb
**Date:** 2026-01-27
**Specification:** specs/issue-2-adw-8dcb27cb-sdlc_planner-python-package-structure.md

## Overview

This feature finalizes the base Python package structure for TAC Bootstrap CLI, implementing TAREA 1.1 from the master plan. It verifies and completes the foundational package configuration following Domain-Driven Design (DDD) architecture with proper licensing, dependency management, and Python version constraints.

## What Was Built

- MIT License file with 2026 copyright
- Updated Python version constraint to >=3.10,<4.0 in pyproject.toml
- Verified DDD architecture layer structure (domain, application, infrastructure, interfaces)
- Completed package configuration for the tac-bootstrap CLI tool
- Specification and checklist documents for implementation tracking

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/LICENSE`: Added MIT License with TAC Bootstrap Team as copyright holder
- `tac_bootstrap_cli/pyproject.toml`: Updated Python version constraint from `>=3.10` to `>=3.10,<4.0` for explicit upper bound
- `specs/issue-2-adw-8dcb27cb-sdlc_planner-python-package-structure.md`: Created detailed specification document
- `specs/issue-2-adw-8dcb27cb-sdlc_planner-python-package-structure-checklist.md`: Implementation checklist

### Key Changes

- **License Addition**: Created MIT License file ensuring open-source compliance and legal clarity for the package
- **Version Constraint Update**: Tightened Python version requirement to exclude Python 4.x, preventing potential breaking changes
- **Package Verification**: Audited existing DDD structure against specifications to ensure proper layer separation
- **Documentation**: Established comprehensive specification describing package structure, dependencies, and acceptance criteria
- **Test Structure**: Verified test directory mirrors source structure for maintainable test organization

## How to Use

The package structure is now ready for business logic implementation. To work with the package:

1. Navigate to the package directory:
   ```bash
   cd tac_bootstrap_cli
   ```

2. Install the package in development mode:
   ```bash
   uv pip install -e .
   ```

3. Verify the CLI entry point works:
   ```bash
   uv run tac-bootstrap --help
   ```

4. Import the package in Python:
   ```bash
   uv run python -c "import tac_bootstrap; print(tac_bootstrap.__version__)"
   ```

## Configuration

### Package Metadata (pyproject.toml)

- **Package name**: `tac-bootstrap`
- **Python version**: `>=3.10,<4.0`
- **License**: MIT
- **Core dependencies**: Typer, Rich, Jinja2, Pydantic, PyYAML
- **Dev dependencies**: pytest, mypy, ruff, pytest-cov
- **CLI entry point**: `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`

### Directory Structure

```
tac_bootstrap_cli/
├── LICENSE                     # MIT License
├── pyproject.toml             # Package configuration
├── README.md                  # Package documentation
├── tac_bootstrap/             # Main package
│   ├── __init__.py           # Version: 0.6.0
│   ├── __main__.py           # Module entry point
│   ├── domain/               # Domain models (DDD)
│   ├── application/          # Business logic (DDD)
│   ├── infrastructure/       # External services (DDD)
│   └── interfaces/           # CLI interface (DDD)
└── tests/                    # Test suite
    ├── test_domain/
    ├── test_application/
    ├── test_infrastructure/
    └── test_interfaces/
```

## Testing

Verify the package structure and configuration:

```bash
cd tac_bootstrap_cli && tree -I __pycache__ -L 3
```

Test package import and version:

```bash
cd tac_bootstrap_cli && uv run python -c "import tac_bootstrap; print(tac_bootstrap.__version__)"
```

Run the CLI help command:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Execute test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting checks:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Execute type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

- This implementation completes TAREA 1.1 from PLAN_TAC_BOOTSTRAP.md
- The package follows DDD architecture with clean layer separation
- Next task (TAREA 1.2) will add domain models and business logic to the layers
- The structure is template-ready: files in this package will be used as Jinja2 templates for generating agentic layers in other projects
- Python version upper bound (<4.0) ensures compatibility and prevents unexpected breaking changes
- All acceptance criteria from the specification have been met
