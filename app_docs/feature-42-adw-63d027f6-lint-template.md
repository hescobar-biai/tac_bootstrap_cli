# Lint Command Template

**ADW ID:** 42-adw-63d027f6
**Date:** 2026-01-20
**Specification:** specs/issue-42-adw-63d027f6-sdlc_planner-create-lint-template.md

## Overview

Created a new Jinja2 template for the `/lint` slash command that enables Claude agents to run linting tools consistently in TAC Bootstrap-generated projects. This template provides standardized instructions for code quality checking and error reporting.

## What Was Built

- Jinja2 template for `/lint` slash command
- Conditional handling for projects with/without lint configuration
- Structured error reporting format
- Auto-fix suggestion capability

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`: New template file for lint command

### Key Changes

- Created template following the same structure as existing commands (test.md.j2, build.md.j2)
- Uses `{{ config.commands.lint }}` variable to support different linters across projects
- Includes conditional block that handles projects without lint commands configured
- Provides clear instructions for agents on error analysis and reporting
- Explicitly instructs agents NOT to auto-fix unless requested by user

## How to Use

This template is used internally by TAC Bootstrap CLI when generating agentic layers for target projects:

1. When users run `tac-bootstrap init` or similar commands, the template repository renders this template
2. The rendered `/lint` command file is placed in the target project's `.claude/commands/` directory
3. In the target project, users or agents can then invoke `/lint` to run linting tools

Example in a generated project:
```bash
/lint                    # Run linter on entire project
/lint src/main.py        # Run linter on specific file
/lint --fix              # Run linter with auto-fix (if supported)
```

## Configuration

The template uses these Jinja2 variables from the config object:

- `{{ config.commands.lint }}`: The lint command for the target project (e.g., `ruff check .`, `eslint`, `pylint`)

These variables are defined in the target project's `config.yml` when TAC Bootstrap generates the agentic layer.

## Testing

Validation was done through:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2
```

## Notes

- This is a template file, not executable code - it generates instructions that agents read
- The template follows the TAC Bootstrap architecture where templates are infrastructure components
- Actual linting happens in target projects, not in TAC Bootstrap itself
- Part of FASE 3 (Templates System) in the TAC Bootstrap implementation roadmap
- Designed to work with any linting tool by using configurable commands
