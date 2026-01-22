# Add Packaging Dependency for Semantic Version Comparison

**ADW ID:** e326b973
**Date:** 2026-01-21
**Specification:** specs/issue-86-adw-e326b973-chore_planner-add-packaging-dependency.md

## Overview

Added the `packaging>=23.0` dependency to the TAC Bootstrap CLI project to support semantic version comparison in the upgrade service. This dependency was already being imported and used in `upgrade_service.py` but was missing from the project's declared dependencies, creating a potential runtime error.

## What Was Built

- Added `packaging>=23.0` to project dependencies in `pyproject.toml`
- Updated `uv.lock` with the new dependency resolution
- Formalized the dependency already in use by the upgrade service

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/pyproject.toml`: Added `packaging>=23.0` to the dependencies array with explanatory comment
- `tac_bootstrap_cli/uv.lock`: Updated lock file with packaging dependency resolution

### Key Changes

- Added `"packaging>=23.0",  # Para comparación de versiones` to the `[project].dependencies` section in pyproject.toml
- Positioned after `pyyaml>=6.0.1` and before `gitpython>=3.1.0`
- This is a production dependency (not dev dependency) as it's used in the core upgrade service functionality
- The `packaging` library was already imported in `tac_bootstrap/application/upgrade_service.py:11` for semantic version comparison using `pkg_version.parse()`

## How to Use

This dependency is automatically installed when setting up the TAC Bootstrap CLI:

1. Navigate to the CLI directory:
   ```bash
   cd tac_bootstrap_cli
   ```

2. Synchronize dependencies with uv:
   ```bash
   uv sync
   ```

The `packaging` library is now available for use in version comparison operations throughout the codebase.

## Configuration

No additional configuration required. The dependency is managed through the standard Python packaging workflow via `pyproject.toml`.

## Testing

Verify the dependency installation:

```bash
cd tac_bootstrap_cli && uv sync
cd tac_bootstrap_cli && uv run python -c "from packaging import version; print(version.parse('1.0.0'))"
```

Run full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify CLI still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- The `packaging` library provides robust semantic version parsing and comparison, used in the upgrade service for comparing TAC Bootstrap versions
- Version `>=23.0` was chosen as it's the stable current version with all necessary functionality for semantic version comparison
- This was a formalization chore: the code was already using the library, but the dependency wasn't declared, which could cause ImportError in fresh environments
