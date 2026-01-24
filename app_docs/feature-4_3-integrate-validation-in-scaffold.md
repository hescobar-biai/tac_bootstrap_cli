# Integrate Pre-Scaffold Validation in ScaffoldService

**ADW ID:** feature_4_3
**Date:** 2026-01-24
**Specification:** specs/issue-161-adw-feature_4_3-sdlc_planner-integrate-validation-in-scaffold.md

## Overview

This feature integrates multi-layer validation into the ScaffoldService before any files are created on disk. The ValidationService (implemented in feature_4_2) now acts as a validation gate at the start of `apply_plan()`, ensuring that configuration errors, template incompatibilities, filesystem issues, and git problems are detected and reported BEFORE any scaffold operations begin. This prevents partial project generation and provides clear, actionable error messages to users.

## What Was Built

- **Application Exception Module** (`application/exceptions.py`):
  - `ApplicationError` - Base exception class for application layer
  - `ScaffoldValidationError` - Custom exception that formats ValidationResult into user-friendly multi-line error messages with numbered issues, severity/level tags, and actionable suggestions

- **Validation Integration in ScaffoldService**:
  - Added `validation_service` parameter to constructor (auto-created if not provided)
  - Integrated validation gate at start of `apply_plan()` method
  - Errors block execution with ScaffoldValidationError
  - Warnings are displayed in yellow but don't block execution

- **Comprehensive Test Suite**:
  - 7 unit tests for ScaffoldValidationError formatting (single/multiple errors, suggestions, severity levels)
  - 5 integration tests verifying validation blocking behavior, error messages, and filesystem protection

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/exceptions.py` - NEW: Added application exception module with ScaffoldValidationError that formats ValidationResult into clear multi-line error messages
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:42-57` - Added validation_service constructor parameter with auto-creation fallback
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:585-602` - Integrated pre-scaffold validation gate with error/warning handling
- `tac_bootstrap_cli/tests/test_application_exceptions.py` - NEW: 7 unit tests for exception formatting
- `tac_bootstrap_cli/tests/test_scaffold_service.py:1061-1222` - NEW: 5 integration tests for validation blocking

### Key Changes

1. **ScaffoldValidationError Design**:
   - Accepts ValidationResult in constructor
   - Implements `__str__()` to format errors in numbered list with level tags ([DOMAIN], [TEMPLATE], [FILESYSTEM], [GIT])
   - Includes suggestions section when available
   - Only formats errors, not warnings (warnings() method filters by severity)

2. **Validation Gate Pattern**:
   - Executes `validation_service.validate_pre_scaffold(config, output_dir)` at start of apply_plan()
   - Raises ScaffoldValidationError if `not validation.valid`
   - Prints warnings to Rich Console in yellow but continues execution
   - Validation happens BEFORE any filesystem operations or metadata registration

3. **Dependency Injection**:
   - ValidationService is now a required dependency of ScaffoldService
   - Auto-created with TemplateRepository if not provided
   - Enables easy mocking in tests for isolated testing

4. **Fail-Fast Design**:
   - All validation layers (DOMAIN, TEMPLATE, FILESYSTEM, GIT) execute before first file write
   - Invalid configs detected before any side effects
   - Output directory remains clean on validation failure

5. **Test Coverage**:
   - Unit tests verify error message formatting for various ValidationResult combinations
   - Integration tests verify real validation blocking with invalid framework/language combos (FastAPI+Rust, Django+Rust, Flask+TypeScript)
   - Tests verify no files created when validation fails
   - Tests verify warnings display but don't block execution

## How to Use

This feature is transparent to end users - validation now happens automatically during scaffolding.

### User Experience with Invalid Config

When running `tac-bootstrap init` with incompatible settings:

```bash
# Example: Trying to use FastAPI (Python-only) with Rust
tac-bootstrap init my-project --language rust --framework fastapi
```

**Before this feature**: Files would start being created, then fail mid-generation, leaving partial project structure.

**After this feature**: Clear error message BEFORE any files are created:

```
Validation failed with 1 error(s):

1. [DOMAIN] Framework fastapi is not compatible with language rust
   → Use one of these languages with fastapi: python

Suggestions:
- Use one of these languages with fastapi: python
```

### Warnings vs Errors

- **Errors** (validation.valid == False): Block execution completely, no files created
- **Warnings** (validation.warnings()): Displayed in yellow, execution continues

Example warning (git not available):
```
Warning: Git not available - some features may be limited
```

### Developer Experience

When creating ScaffoldService in code:

```python
# ValidationService auto-created
service = ScaffoldService()

# Or inject for testing
mock_validator = Mock(spec=ValidationService)
service = ScaffoldService(validation_service=mock_validator)
```

## Configuration

No configuration required. Validation automatically uses:
- Domain compatibility rules (framework/language/architecture combinations)
- Template availability checks (templates must exist for chosen framework/architecture)
- Filesystem permission checks (output directory must be writable)
- Git availability checks (warning only, doesn't block)

## Testing

Run the full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "test_scaffold_validation_error or TestScaffoldServiceValidation"
```

### Test Coverage

**Unit Tests** (`test_application_exceptions.py`):
- Single error formatting
- Multiple errors formatting
- Suggestions section inclusion
- Severity/level tags display
- Warning filtering (only errors in message)
- Errors without suggestions
- Exception hierarchy verification

**Integration Tests** (`test_scaffold_service.py`):
- `test_apply_plan_fails_on_invalid_framework_language` - FastAPI+Rust blocked
- `test_apply_plan_shows_warnings_but_continues` - Git warnings don't block
- `test_apply_plan_error_includes_all_issues` - Multiple errors all shown
- `test_apply_plan_no_files_created_on_validation_failure` - Filesystem protection
- `test_apply_plan_with_valid_config_passes_validation` - Valid configs work normally

## Notes

- This feature completes FASE 4 (Multi-layer Validation) of the TAC Bootstrap implementation plan
- Builds on feature_4_2 (Domain Compatibility Validators) which implemented ValidationService
- ScaffoldValidationError is an application layer concern (translates domain ValidationResult to user-facing format)
- No logging added (YAGNI) - only console output for warnings
- Error format is human-readable only (CLI tool, no JSON needed)
- Validation order: DOMAIN → TEMPLATE → FILESYSTEM → GIT (fail-fast on cheapest checks first)
- All 671 lines of changes include comprehensive test coverage (183 lines for exception tests, 163 lines for integration tests)
