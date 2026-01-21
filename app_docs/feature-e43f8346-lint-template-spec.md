# Lint Template Specification

**ADW ID:** e43f8346
**Date:** 2026-01-21
**Specification:** specs/issue-42-adw-e43f8346-sdlc_planner-create-lint-template.md

## Overview

This feature creates a comprehensive specification document for the `/lint` command template in TAC Bootstrap. The spec defines requirements for a Jinja2 template that generates slash commands to execute project-specific linters in agentic workflows.

## What Was Built

- Detailed specification document for the lint.md.j2 template
- Verification plan for existing template implementation
- Testing strategy covering edge cases and template rendering
- Acceptance criteria aligned with TAC Bootstrap command patterns

## Technical Implementation

### Files Modified

- `specs/issue-42-adw-e43f8346-sdlc_planner-create-lint-template.md`: New specification document created with complete requirements

### Key Changes

- Created comprehensive specification defining how the `/lint` command template should work
- Documented required Jinja2 variables: `config.commands.lint`, `config.project.name`, `config.project.language`
- Established testing strategy for template rendering and edge cases
- Defined validation commands to ensure zero regressions
- Documented that this is a verification task (template already exists) rather than creation task

## How to Use

This specification serves as a guide for:

1. **Verifying** the existing lint template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
2. **Testing** that the template renders correctly with various configurations
3. **Validating** that the template follows established patterns from test.md.j2 and build.md.j2
4. **Ensuring** proper error handling when lint command is not configured

## Configuration

The lint template uses these configuration variables from TAC Bootstrap's config system:

- `config.commands.lint` - The linter command to execute (e.g., "ruff check .", "eslint .")
- `config.project.name` - Project name for context
- `config.project.language` - Programming language (python, javascript, etc.)

## Testing

Run validation commands to ensure the specification is met:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This specification documents a verification task rather than a creation task
- The lint.md.j2 template already exists in the codebase
- The spec provides a structured approach to validate the existing implementation
- Future consideration: Add automated tests to verify all command templates render correctly
- The template must handle cases where no lint command is configured gracefully
