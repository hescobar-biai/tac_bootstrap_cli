# Makefile for Development Commands

**ADW ID:** 16866919
**Date:** 2026-01-21
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/16866919/specs/issue-49-adw-16866919-chore_planner-crear-makefile.md

## Overview

A comprehensive Makefile was added to `tac_bootstrap_cli/` to provide convenient development commands for installation, linting, testing, building, and CLI operations. The Makefile uses `uv` as the package manager and follows best practices with proper variable definitions and `.PHONY` declarations.

## What Was Built

- Complete Makefile with 18 commands organized into 6 categories
- Installation commands for dependencies
- Development workflow commands (lint, format, typecheck)
- Testing commands with coverage and watch mode support
- Build and clean commands
- CLI example commands
- Comprehensive help system

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/Makefile`: New 119-line Makefile with all development commands
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`: Code formatting improvements (173 lines changed)
- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`: Minor formatting adjustments
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`: Code formatting
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Minor update
- `tac_bootstrap_cli/tests/test_plan.py`: Test cleanup
- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Test improvements

### Key Changes

- **Variables Defined**: `PYTHON`, `PYTEST`, `CLI`, `RUFF`, `MYPY` set to use `uv run` prefix for all commands
- **Default Target**: Set to `help` so running `make` without arguments shows available commands
- **Smart Clean**: Uses `find` commands with error suppression (`2>/dev/null || true`) to safely remove cache directories
- **Test Watch**: Includes check for `pytest-watch` installation with helpful error message
- **Organized Help**: Custom help message categorizes commands into logical groups
- **All Phony**: Proper `.PHONY` declaration for all 18 targets to prevent conflicts with files

## How to Use

### Installation

```bash
cd tac_bootstrap_cli
make install          # Install basic dependencies
make install-dev      # Install with dev dependencies
```

### Development Workflow

```bash
make lint             # Check code with ruff
make lint-fix         # Auto-fix linting issues
make format           # Format code with ruff
make typecheck        # Run mypy type checking
```

### Testing

```bash
make test             # Run all tests
make test-v           # Verbose test output
make test-cov         # Run with coverage report
make test-watch       # Watch mode (requires pytest-watch)
```

### Building

```bash
make build            # Build wheel package
make clean            # Remove all cache and build files
```

### CLI Examples

```bash
make cli-help         # Show CLI help
make cli-version      # Show version
make cli-init-dry     # Example init dry-run
make cli-doctor       # Example doctor command
```

### Getting Help

```bash
make help             # Show all available commands
make                  # Same as 'make help' (default)
```

## Configuration

No additional configuration required. The Makefile works out-of-the-box with:
- `uv` package manager (required)
- Standard Python project structure
- `pyproject.toml` with configured tools (ruff, mypy, pytest)

## Testing

Validation was performed on all commands:

```bash
cd tac_bootstrap_cli && make help
cd tac_bootstrap_cli && make lint
cd tac_bootstrap_cli && make test
cd tac_bootstrap_cli && make cli-help
```

All commands executed successfully with no regressions.

## Notes

- The Makefile is compatible with GNU Make
- Commands use `@` prefix on echo statements to hide the command itself in output
- Clean commands gracefully handle missing directories
- Test-watch provides helpful installation instructions if `pytest-watch` is not available
- CLI example commands (`cli-init-dry`, `cli-doctor`) provide guidance on usage rather than executing potentially disruptive operations
- All paths are relative and work when `make` is executed from `tac_bootstrap_cli/` directory
- The `doctor_service.py` received significant formatting improvements as part of this work, applying consistent code style across the codebase
