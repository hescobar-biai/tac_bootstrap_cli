---
doc_type: feature
adw_id: chore_Tac_10_task_8
date: 2026-01-27
idk:
  - unit-test
  - template-rendering
  - fixture
  - jinja2
  - validation
  - pytest
  - hooks
  - settings-json
tags:
  - feature
  - testing
  - templates
related_code:
  - tac_bootstrap_cli/tests/test_new_tac10_templates.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/t_metaprompt_workflow.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_w_report.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2
---

# Test Validation for TAC-10 Templates

**ADW ID:** chore_Tac_10_task_8
**Date:** 2026-01-27
**Specification:** specs/issue-321-adw-chore_Tac_10_task_8-sdlc_planner-update-tests-new-templates.md

## Overview

Comprehensive unit test suite for validating TAC-10 template rendering. Tests verify that new command templates (parallel_subagents, t_metaprompt_workflow, build_w_report, cc_hook_expert_improve) and updated settings.json.j2 with 9 new hooks render correctly without errors and produce valid structured output.

## What Was Built

- **Test file**: `test_new_tac10_templates.py` with 249 lines of test code
- **Test fixtures**: Reusable `python_config` and `template_repo` fixtures for minimal test configuration
- **Command template tests**: Validation for 4 new slash command templates (parallel_subagents, t_metaprompt_workflow, build_w_report, cc_hook_expert_improve)
- **Settings validation tests**: 3 test methods validating settings.json.j2 structure, hook presence, and script references
- **Hook validation**: Comprehensive verification that all 9 hooks (PreToolUse, PostToolUse, Stop, UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd) are present and reference correct scripts

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_new_tac10_templates.py`: New test file with 5 test classes covering command templates, expert templates, and settings.json validation

### Key Changes

- Implemented pytest fixtures following the pattern from `test_fractal_docs_templates.py` for minimal TACConfig setup
- Created 5 test classes organized by template type: command templates (3 classes), expert template (1 class), settings template (1 class)
- Verified markdown structure for command templates by checking for standard sections (Variables, Instructions, Workflow)
- Validated settings.json.j2 produces valid JSON with all 9 expected hooks
- Implemented helper function `get_hook_command()` to extract and validate hook script references
- Verified PostToolUse and UserPromptSubmit reference `context_bundle_builder.py`
- Verified 7 hooks reference `universal_hook_logger.py` (PreToolUse, Stop, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd)

## How to Use

### Running the New Tests

Execute the new test file to validate TAC-10 templates:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_new_tac10_templates.py -v --tb=short
```

### Running Full Test Suite

Verify zero regressions across all tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Linting Validation

Ensure code quality standards are met:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### CLI Smoke Test

Verify the CLI still works after changes:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Configuration

No additional configuration required. Tests use minimal `TACConfig` with:
- `ProjectSpec` with name="test-python-app", language=PYTHON, package_manager=UV
- `CommandsSpec` with basic start and test commands
- `ClaudeConfig` with minimal settings

This follows the established pattern from existing test files.

## Testing

All validation commands were executed successfully:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_new_tac10_templates.py -v --tb=short
```

Expected output: 7 tests passing (4 command template tests, 1 expert template test, 3 settings.json tests)

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Expected output: All existing tests plus 7 new tests passing with zero regressions

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Expected output: No linting errors

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Expected output: CLI help text displays correctly

## Notes

### Test Design Philosophy

Tests follow the principle of validating happy path without over-engineering edge cases. Each test verifies:
1. Template renders without errors
2. Output has valid structure (markdown sections or JSON parsing)
3. Key content is present (hooks, script references)

### Hook Validation Strategy

The settings.json validation uses a helper function to extract hook commands from the nested JSON structure. This approach allows precise verification of script references without brittle string matching.

### Template Rendering Pattern

All tests use the same pattern:
```python
content = template_repo.render("path/to/template.j2", config)
assert len(content.strip()) > threshold  # Not empty
# Specific validation (JSON parsing, markdown sections, etc.)
```

This consistent pattern makes tests easy to understand and maintain.
