---
doc_type: feature
adw_id: 6fe74a31
date: 2026-01-27
idk:
  - dependency-injection
  - configuration
  - pyproject
  - uv
  - validation
  - cli
tags:
  - feature
  - chore
related_code:
  - tac_bootstrap_cli/pyproject.toml
  - .mcp.json
  - playwright-mcp-config.json
---

# Configure Dependencies for TAC Bootstrap CLI

**ADW ID:** 6fe74a31
**Date:** 2026-01-27
**Specification:** specs/issue-3-adw-6fe74a31-chore_planner-configure-dependencies.md

## Overview

This chore verified that the TAC Bootstrap CLI project has all required dependencies properly configured in `pyproject.toml` and that the CLI commands work correctly. The task focused on validating the existing dependency configuration rather than implementing new changes.

## What Was Built

- Validated dependency configuration in `pyproject.toml`
- Updated MCP configuration paths for the new worktree
- Created specification and checklist documentation
- Verified CLI entry points and basic commands work correctly

## Technical Implementation

### Files Modified

- `.mcp.json`: Updated Playwright MCP config path from `ac5b5582` to `6fe74a31` worktree
- `playwright-mcp-config.json`: Updated video recording directory path to new worktree
- `specs/issue-3-adw-6fe74a31-chore_planner-configure-dependencies.md`: Created specification document
- `specs/issue-3-adw-6fe74a31-chore_planner-configure-dependencies-checklist.md`: Created validation checklist

### Key Changes

- The existing `tac_bootstrap_cli/pyproject.toml` (version 0.6.0) already contained all required dependencies from the original specification (version 0.1.0 requirements)
- Production dependencies verified: typer, rich, jinja2, pydantic, pyyaml, gitpython
- Development dependencies verified: pytest, pytest-cov, mypy, ruff
- CLI entry point confirmed: `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`
- All validation commands pass: tests (690 passed), linting, smoke tests, version command

## How to Use

The TAC Bootstrap CLI is now properly configured with all dependencies. To work with it:

1. Navigate to the CLI package directory:
```bash
cd tac_bootstrap_cli
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Run the CLI to see available commands:
```bash
uv run tac-bootstrap --help
```

4. Check the installed version:
```bash
uv run tac-bootstrap version
```

## Configuration

The `pyproject.toml` includes:

**Production Dependencies:**
- `typer>=0.9.0` - CLI framework for commands and arguments
- `rich>=13.0.0` - Terminal UI with tables, panels, colors
- `jinja2>=3.0.0` - Template rendering engine
- `pydantic>=2.0.0` - Data validation and settings
- `pyyaml>=6.0.0` - YAML file parsing
- `gitpython>=3.1.0` - Git operations
- `packaging>=23.0` - Version comparison utilities

**Development Dependencies:**
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Test coverage reporting
- `mypy>=1.0.0` - Static type checking
- `ruff>=0.1.0` - Fast linting and formatting

**CLI Entry Point:**
```toml
[project.scripts]
tac-bootstrap = "tac_bootstrap.interfaces.cli:app"
```

## Testing

Validate the dependency configuration with these commands:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify linting passes:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Test CLI smoke test:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verify version command:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap version
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports
```

## Notes

- The existing pyproject.toml was already at version 0.6.0, which exceeds the 0.1.0 requirements from the original specification
- No changes to `pyproject.toml` were needed as all dependencies were already properly configured from previous work
- The main value of this task was validation: confirming all acceptance criteria are met and documenting the current state
- MCP configuration paths were updated to reflect the new worktree (`6fe74a31`) used for this isolated ADW workflow
- All 690 unit tests pass successfully, confirming zero regressions
