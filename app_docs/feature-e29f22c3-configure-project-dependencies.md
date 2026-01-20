# Configure Project Dependencies

**ADW ID:** e29f22c3
**Date:** 2026-01-20
**Specification:** specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md

## Overview

Configured project dependencies for TAC Bootstrap CLI by adding missing dependencies and tool configurations to `pyproject.toml`. This chore ensures all required libraries are installed and development tools (ruff, mypy, pytest) are properly configured for consistent code quality.

## What Was Built

- Added `gitpython>=3.1.0` to production dependencies
- Configured ruff linting with explicit rule selection (E, F, I, N, W)
- Configured mypy with strict type checking settings
- Configured pytest with test discovery paths
- Enhanced CLI with callback to show help when no command is provided
- Added type hints to CLI functions for better type safety

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/pyproject.toml`: Added gitpython dependency and tool configurations (ruff, mypy, pytest)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py:7-14`: Added callback function to display help when no subcommand is invoked, added type hints to version command
- `tac_bootstrap_cli/tests/test_cli.py:2`: Added blank line for PEP 8 compliance
- `tac_bootstrap_cli/uv.lock`: Updated lockfile with gitpython and its transitive dependencies

### Key Changes

- **Dependency Addition**: Added gitpython>=3.1.0 for Git operations support, required for future template generation workflows
- **Linting Configuration**: Configured ruff with line length of 100, Python 3.10+ target, and explicit rule selection (errors, pyflakes, imports, naming, warnings)
- **Type Checking**: Enabled mypy strict mode with return type warnings and unused config warnings for comprehensive type safety
- **Test Configuration**: Set pytest to discover tests in `tests/` directory with `test_*.py` pattern
- **CLI UX Improvement**: Added callback to show help automatically when CLI is invoked without subcommands, improving discoverability

## How to Use

### Install Dependencies

After updating `pyproject.toml`, synchronize dependencies:

```bash
cd tac_bootstrap_cli && uv sync
```

### Verify Installation

Check that the CLI works correctly:

```bash
# Show help (will appear automatically when running tac-bootstrap with no args)
cd tac_bootstrap_cli && uv run tac-bootstrap

# Show version
cd tac_bootstrap_cli && uv run tac-bootstrap version
```

Expected output for version command:
```
tac-bootstrap v0.1.0
```

### Run Quality Checks

```bash
# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap

# Run tests
cd tac_bootstrap_cli && uv run pytest tests/ -v
```

## Configuration

### Ruff (Linter)
- **Line length**: 100 characters
- **Target version**: Python 3.10
- **Selected rules**:
  - E: pycodestyle errors
  - F: pyflakes
  - I: isort (import sorting)
  - N: pep8-naming
  - W: pycodestyle warnings

### Mypy (Type Checker)
- **Python version**: 3.10
- **Strict mode**: Enabled
- **Warnings**: Return types and unused configs

### Pytest (Test Runner)
- **Test paths**: `tests/`
- **Test file pattern**: `test_*.py`
- **Test function pattern**: `test_*`

## Testing

Run the full test suite with validation commands:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# CLI smoke tests
cd tac_bootstrap_cli && uv run tac-bootstrap --help
cd tac_bootstrap_cli && uv run tac-bootstrap version
```

All commands should pass with zero errors and zero regressions.

## Notes

- This was a configuration-only chore with no new feature implementation
- The CLI callback improvement (tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py:10-14) enhances UX by showing help automatically
- GitPython dependency prepares the project for future Git-based template generation features
- All tool configurations follow Python best practices and enable strict quality checks
- The lockfile (`uv.lock`) was automatically updated with gitpython's transitive dependencies (gitdb, smmap)
