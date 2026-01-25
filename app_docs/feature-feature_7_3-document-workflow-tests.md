---
doc_type: feature
adw_id: feature_7_3
date: 2026-01-25
idk:
  - pytest
  - template-validation
  - fractal-docs
  - yaml-frontmatter
  - ast-parsing
  - backward-compatibility
  - non-blocking-workflow
tags:
  - feature
  - testing
  - validation
related_code:
  - tac_bootstrap_cli/tests/test_fractal_docs_templates.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2
---

# Document Workflow Tests

**ADW ID:** feature_7_3
**Date:** 2026-01-25
**Specification:** specs/issue-186-adw-feature_7_3-chore_planner-document-workflow-tests.md

## Overview

Added comprehensive test coverage for the document workflow improvements introduced in Tasks 7.1 and 7.2. These tests verify that the enhanced `/document` command template includes IDK frontmatter and that the document workflow integrates fractal docs generation in a non-blocking manner.

## What Was Built

This feature adds three new test cases to validate document workflow templates:

- **test_document_command_has_idk_frontmatter**: Validates that the `/document` command template includes proper YAML frontmatter with IDK fields
- **test_adw_document_includes_fractal_step**: Ensures the document workflow template includes fractal docs generation step
- **test_adw_document_fractal_is_non_blocking**: Verifies the fractal docs step is wrapped in try-except for non-blocking behavior

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_fractal_docs_templates.py`: Added new test class `TestDocumentWorkflowTemplates` with 143 lines of test code

### Key Changes

- **IDK Frontmatter Validation**: Tests parse rendered templates to verify presence of required YAML fields (`doc_type`, `adw_id`, `date`, `idk`, `tags`, `related_code`) and validate YAML structure
- **Fractal Docs Integration**: Tests verify the document workflow template includes the correct slash command (`/generate_fractal_docs`), arguments (`["changed"]`), and agent name (`fractal_docs_generator`)
- **Non-Blocking Error Handling**: Tests verify fractal docs calls are wrapped in try-except blocks with `logger.warning` (not `raise`) to prevent workflow interruption
- **AST Validation**: All Python template rendering is validated using `ast.parse()` to ensure syntactically correct code generation
- **Template Rendering**: Uses `TemplateRepository.render()` to render Jinja2 templates with test configuration

## How to Use

These tests run as part of the standard test suite. To execute them:

1. Run the specific test class:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestDocumentWorkflowTemplates -v --tb=short
```

2. Or run the entire test suite:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

3. Verify linting:
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

4. Smoke test the CLI:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Configuration

No additional configuration required. Tests use the standard pytest fixtures:
- `template_repo`: Provides access to Jinja2 template rendering
- `python_config`: Sample TACConfig instance for template context

## Testing

Run the validation commands to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestDocumentWorkflowTemplates -v --tb=short
```

Verify all tests pass with specific assertions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_fractal_docs_templates.py::TestDocumentWorkflowTemplates::test_document_command_has_idk_frontmatter -v
```

## Notes

**Context**: This is a verification chore (7.3) for features implemented in Tasks 7.1 and 7.2:
- Task 7.1: Added IDK frontmatter to `document.md.j2` template
- Task 7.2: Integrated fractal docs in `adw_document_iso.py` workflow

**Backward Compatibility**: Templates are copied at project generation time, so these improvements only affect new projects created with tac-bootstrap. Existing projects maintain their original templates without requiring migration.

**Test Patterns**:
- Template rendering validation (content checks, structure verification)
- AST parsing for Python code syntax validation
- YAML structure validation for frontmatter
- Non-blocking error handling verification (try-except with logger.warning)
