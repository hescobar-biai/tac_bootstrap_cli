# Enable Scaffold Service Integration Tests

**ADW ID:** b408e27f
**Date:** 2026-01-21
**Specification:** specs/issue-48-adw-b408e27f-chore_planner-enable-scaffold-service-tests.md

## Overview

This chore enabled 10 previously skipped integration tests in `test_scaffold_service.py` that validate the `ScaffoldService` applying scaffold plans with real Jinja2 templates. These tests were originally marked with `@pytest.mark.skip(reason="Requires real templates - integration test")` but can now run because the template system with 44 .j2 templates is fully implemented.

## What Was Built

- **Enabled Integration Tests**: Removed `@skip` decorators from 10 tests covering:
  - Directory structure creation
  - Template rendering with configuration context
  - Script file executable permissions
  - File skip/overwrite logic
  - Operation counting and result reporting
  - Idempotency behavior
  - Force mode functionality
  - Error handling

- **Fixed Template Context**: Updated `scaffold_service.py` to pass `config` directly to template renderer instead of wrapping in dictionary, matching the template repository's expected interface.

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Removed 10 `@pytest.mark.skip` decorators from integration tests in `TestScaffoldServiceApplyPlan` class
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Fixed template context parameter from `{"config": config}` to `config` in tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:365

### Key Changes

1. **Test Enablement**: All integration tests that verify `apply_plan()` functionality are now active and running against real templates
2. **Template Context Fix**: Corrected the template rendering call to pass the config object directly, not wrapped in a dictionary
3. **Template Verification**: Confirmed all required templates exist in `tac_bootstrap/templates/` directory (44 .j2 files across 5 subdirectories)
4. **Coverage Improvement**: These tests significantly increase coverage of the `ScaffoldService.apply_plan()` method

### Tests Now Running

- `test_apply_plan_creates_structure` - Validates directory and file creation
- `test_apply_plan_creates_nested_directories` - Validates nested directory creation
- `test_apply_plan_renders_templates` - Validates Jinja2 template rendering with config
- `test_apply_plan_makes_scripts_executable` - Validates executable permissions on scripts
- `test_apply_plan_skips_existing_files` - Validates file skip behavior
- `test_apply_plan_counts_operations` - Validates operation counters in result
- `test_apply_plan_idempotent` - Validates running twice produces same result
- `test_apply_plan_with_force` - Validates force mode overwrites files
- `test_apply_plan_to_nonexistent_directory_creates_it` - Validates directory auto-creation
- `test_apply_plan_error_handling` - Validates error handling

## How to Use

These are integration tests that run automatically as part of the test suite. No user-facing changes.

### Running the Tests

```bash
# Run just the scaffold_service tests
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v

# Run with coverage report
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py --cov=tac_bootstrap.application.scaffold_service --cov-report=term
```

## Configuration

No configuration required. Tests use the existing template system in `tac_bootstrap_cli/tac_bootstrap/templates/`.

## Testing

All tests pass with the changes:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short
```

Expected result: All tests in `TestScaffoldServiceApplyPlan` class should pass, validating that the scaffold service correctly applies plans using real templates.

## Notes

- These tests were skipped during initial development because the template system was not yet complete
- Now that 44 Jinja2 templates are implemented, these integration tests validate end-to-end functionality
- Tests use Python's `tempfile` module to create isolated test environments
- The template context fix ensures templates receive config in the expected format: `{{ config.project.name }}` instead of requiring nested access
- These tests significantly improve coverage of the `ScaffoldService` class, particularly the `apply_plan()` method
