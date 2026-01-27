---
doc_type: feature
adw_id: ac5b5582
date: 2026-01-27
idk:
  - python-package
  - ddd-architecture
  - pyproject-toml
  - cli-entrypoint
  - domain-model
  - repository
tags:
  - feature
  - python
  - architecture
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/__init__.py
  - tac_bootstrap_cli/tests/test_value_objects.py
---

# Python Package Structure for TAC Bootstrap CLI

**ADW ID:** ac5b5582
**Date:** 2026-01-27
**Specification:** specs/issue-1-adw-ac5b5582-sdlc_planner-python-package-structure.md

## Overview

Established the foundational Python package structure for the TAC Bootstrap CLI following modern Python packaging standards (PEP 621) and Domain-Driven Design (DDD) architecture. This structure provides the scaffolding for building a CLI tool that generates Agentic Layers for Claude Code projects using TAC (Total Agentic Coding) patterns.

## What Was Built

- Complete DDD-based directory structure with domain, application, infrastructure, and interfaces layers
- Modern `pyproject.toml` configuration with hatchling build system
- CLI entry points for running as command (`tac-bootstrap`) or Python module (`python -m tac_bootstrap`)
- Templates directory for future Jinja2 templates
- Tests directory with initial test setup
- Version management system through `__init__.py`

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/__init__.py`: Added templates directory initialization with docstring
- `tac_bootstrap_cli/tests/test_value_objects.py`: Fixed semantic version comparison test (changed assertion from `v1 < "0.6.0"` to `v1 < "0.7.0"` for correct test logic)
- `specs/issue-1-adw-ac5b5582-sdlc_planner-python-package-structure.md`: Created comprehensive specification document
- `specs/issue-1-adw-ac5b5582-sdlc_planner-python-package-structure-checklist.md`: Created implementation checklist

### Key Changes

- **Package Structure**: Established DDD layers (domain, application, infrastructure, interfaces) with proper `__init__.py` files
- **Build Configuration**: Created `pyproject.toml` with PEP 621-compliant metadata, hatchling build backend, and CLI entry point
- **CLI Foundation**: Set up Typer-based CLI stub with version command at `tac_bootstrap/interfaces/cli.py`
- **Entry Points**: Configured both script entry point (`tac-bootstrap`) and module execution (`__main__.py`)
- **Test Fix**: Corrected semantic version comparison test that was comparing version to itself instead of testing less-than logic

## How to Use

1. Navigate to the CLI directory:
```bash
cd tac_bootstrap_cli
```

2. Install the package in development mode:
```bash
uv pip install -e .
```

3. Run the CLI to verify installation:
```bash
tac-bootstrap version
```

4. Alternatively, run as a Python module:
```bash
python -m tac_bootstrap version
```

5. View the package structure:
```bash
tree tac_bootstrap -I __pycache__ -I "*.pyc"
```

## Configuration

The package is configured through `pyproject.toml`:

- **Package Name**: `tac-bootstrap`
- **Version**: `0.1.0`
- **Python Requirement**: `>=3.10`
- **Build System**: hatchling
- **Dependencies**: typer (for CLI framework)
- **Entry Point**: `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`

## Testing

Verify the package structure:

```bash
tree tac_bootstrap_cli -I __pycache__ -I "*.pyc"
```

Validate pyproject.toml is parseable:

```bash
python -c "import tomllib; tomllib.load(open('tac_bootstrap_cli/pyproject.toml', 'rb'))"
```

Run existing tests to ensure no regressions:

```bash
uv run pytest tac_bootstrap_cli/tests/test_value_objects.py -v
```

Verify package version:

```bash
cat tac_bootstrap_cli/tac_bootstrap/__init__.py
```

Check all layer initializations:

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/*/
```

## Notes

- This is TASK 1.1 from the main implementation plan (PLAN_TAC_BOOTSTRAP.md)
- The DDD architecture separates concerns: domain (business models), application (use cases), infrastructure (I/O, templates), and interfaces (CLI)
- The templates directory is prepared for future Jinja2 template files that will generate Agentic Layer structures
- No business logic is implemented yet - this is purely structural scaffolding
- Future tasks will add domain models, template rendering services, and CLI commands
- The version comparison test fix ensures proper semantic version ordering validation
