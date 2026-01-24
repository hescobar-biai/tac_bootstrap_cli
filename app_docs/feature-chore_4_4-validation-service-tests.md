# Validation Service Tests

**ADW ID:** chore_4_4
**Date:** 2026-01-24
**Specification:** specs/issue-165-adw-chore_4_4-chore_planner-tests-validation-service.md

## Overview

Comprehensive unit test suite for ValidationService that validates TAC Bootstrap configurations across multiple layers (domain, template, filesystem, git). The test suite ensures all compatibility rules, template requirements, filesystem permissions, and git warnings are properly validated before scaffold generation.

## What Was Built

- Complete test coverage for ValidationService with 929 lines of tests
- Framework-language compatibility matrix testing (50+ combinations)
- Framework-architecture compatibility matrix testing (25+ combinations)
- Template validation tests (critical templates existence)
- Filesystem validation tests (permissions, conflicts, parent directories)
- Git validation tests (installation, uncommitted changes warnings)
- Multiple error accumulation tests
- ValidationResult helper method tests
- Entity specification validation tests

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_validation_service.py`: New comprehensive test suite with 10 test classes covering all validation layers
- `specs/issue-165-adw-chore_4_4-chore_planner-tests-validation-service.md`: Specification document
- `specs/issue-165-adw-chore_4_4-chore_planner-tests-validation-service-checklist.md`: Implementation checklist

### Key Changes

**Test Structure (10 Test Classes):**
1. `TestFrameworkLanguageCompatibility` - Tests framework-language compatibility matrix with positive and negative cases
2. `TestFrameworkArchitectureCompatibility` - Tests framework-architecture compatibility with all valid/invalid combinations
3. `TestTemplateValidation` - Tests critical template existence validation
4. `TestFilesystemValidation` - Tests directory permissions, parent directory access, and conflict detection
5. `TestGitValidation` - Tests git installation checks and uncommitted changes warnings
6. `TestMultipleErrors` - Tests error accumulation from multiple validation layers
7. `TestPreScaffoldValidation` - Tests complete pre-scaffold validation integration
8. `TestValidationResult` - Tests ValidationResult helper methods (errors(), warnings())
9. `TestEntityValidation` - Tests entity specification validation
10. `TestValidationEdgeCases` - Tests edge cases and boundary conditions

**Coverage Highlights:**
- Framework.NONE compatibility with all languages and only Architecture.SIMPLE
- Django restrictions (Python only, no DDD architecture)
- FastAPI flexibility (Python only, supports all architectures)
- NestJS constraints (TypeScript only, supports Layered/DDD/Clean)
- Express flexibility (TypeScript/JavaScript, limited architectures)
- Critical templates validation: `claude/settings.json.j2`, `claude/hooks/user_prompt_submit.py.j2`
- Filesystem validation: writable parent, no conflicts, proper permissions
- Git warnings that don't block execution (missing git, uncommitted changes)

**Mock Strategy:**
- `mock_template_repo` fixture for TemplateRepository
- `@patch` decorators for git and filesystem operations
- Inline test data for clarity
- Pytest `tmp_path` fixture for filesystem tests

## How to Use

### Running the Complete Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py -v --tb=short
```

### Running Specific Test Classes

```bash
# Framework-language compatibility tests
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py::TestFrameworkLanguageCompatibility -v

# Framework-architecture compatibility tests
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py::TestFrameworkArchitectureCompatibility -v

# Template validation tests
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py::TestTemplateValidation -v

# Filesystem validation tests
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py::TestFilesystemValidation -v

# Git validation tests
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py::TestGitValidation -v
```

### Running with Coverage

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_validation_service.py \
  --cov=tac_bootstrap.application.validation_service \
  --cov-report=term-missing \
  --cov-report=html
```

### Running All Tests to Verify No Regressions

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Configuration

No additional configuration required. Tests use:
- Pytest fixtures for dependency injection
- Mock objects for external dependencies
- Temporary directories for filesystem tests
- Patch decorators for git operations

## Testing

### Test Coverage by Validation Layer

**Domain Validation (Lines 160-211 in validation_service.py):**
- ✅ Framework-language compatibility matrix (8 frameworks × 6 languages = 48 combinations)
- ✅ Framework-architecture compatibility matrix (8 frameworks × 5 architectures = 40 combinations)
- ✅ Special cases: Framework.NONE accepts all languages, only Architecture.SIMPLE
- ✅ Error messages include framework, language/architecture names
- ✅ Suggestions include valid options

**Template Validation:**
- ✅ Critical templates exist (claude/settings.json.j2, claude/hooks/user_prompt_submit.py.j2)
- ✅ Missing single template generates error
- ✅ Missing multiple templates generate multiple errors
- ✅ Error messages include template path and suggestion

**Filesystem Validation:**
- ✅ Non-existent directory with writable parent passes
- ✅ Non-writable directory fails
- ✅ Existing directory with .tac_config.yaml fails (conflict)
- ✅ Non-existent parent directory fails
- ✅ Non-writable parent directory fails
- ✅ Error messages include path and suggestion

**Git Validation:**
- ✅ Git not installed generates warning (not error)
- ✅ Uncommitted changes generate warning (not error)
- ✅ Clean repo generates no warnings
- ✅ Warnings don't block validation (result.valid remains True)

**Multiple Errors:**
- ✅ Errors from different layers accumulate
- ✅ Multiple domain errors accumulate
- ✅ ValidationResult includes all error levels
- ✅ Each error has correct level, severity, message

**ValidationResult Helpers:**
- ✅ errors() filters only error-severity issues
- ✅ warnings() filters only warning-severity issues
- ✅ Mixed list of 3 errors + 2 warnings filters correctly

### Example Test Output

```
tests/test_validation_service.py::TestFrameworkLanguageCompatibility::test_compatible_framework_language_passes PASSED
tests/test_validation_service.py::TestFrameworkLanguageCompatibility::test_incompatible_framework_language_fails PASSED
tests/test_validation_service.py::TestFrameworkLanguageCompatibility::test_multiple_valid_language_combinations PASSED
tests/test_validation_service.py::TestFrameworkLanguageCompatibility::test_multiple_invalid_language_combinations PASSED
tests/test_validation_service.py::TestFrameworkLanguageCompatibility::test_framework_none_accepts_all_languages PASSED
tests/test_validation_service.py::TestFrameworkArchitectureCompatibility::test_compatible_framework_architecture_passes PASSED
tests/test_validation_service.py::TestFrameworkArchitectureCompatibility::test_incompatible_framework_architecture_fails PASSED
tests/test_validation_service.py::TestFrameworkArchitectureCompatibility::test_multiple_valid_architecture_combinations PASSED
tests/test_validation_service.py::TestFrameworkArchitectureCompatibility::test_multiple_invalid_architecture_combinations PASSED
tests/test_validation_service.py::TestFrameworkArchitectureCompatibility::test_framework_none_only_accepts_simple PASSED
tests/test_validation_service.py::TestTemplateValidation::test_critical_templates_exist_passes PASSED
tests/test_validation_service.py::TestTemplateValidation::test_missing_critical_template_fails PASSED
tests/test_validation_service.py::TestTemplateValidation::test_multiple_missing_templates_generates_multiple_issues PASSED
tests/test_validation_service.py::TestFilesystemValidation::test_nonexistent_directory_with_writable_parent_passes PASSED
tests/test_validation_service.py::TestFilesystemValidation::test_non_writable_directory_fails PASSED
tests/test_validation_service.py::TestFilesystemValidation::test_existing_directory_with_tac_config_fails PASSED
tests/test_validation_service.py::TestFilesystemValidation::test_parent_directory_not_writable_fails PASSED
tests/test_validation_service.py::TestGitValidation::test_git_not_installed_generates_warning PASSED
tests/test_validation_service.py::TestGitValidation::test_uncommitted_changes_generates_warning PASSED
tests/test_validation_service.py::TestGitValidation::test_git_installed_repo_clean_no_warnings PASSED
tests/test_validation_service.py::TestMultipleErrors::test_multiple_errors_accumulate PASSED
tests/test_validation_service.py::TestPreScaffoldValidation::test_complete_validation_passes PASSED
tests/test_validation_service.py::TestPreScaffoldValidation::test_validation_fails_with_multiple_layers PASSED
tests/test_validation_service.py::TestPreScaffoldValidation::test_validation_includes_git_warnings PASSED
tests/test_validation_service.py::TestValidationResult::test_errors_filters_only_errors PASSED
tests/test_validation_service.py::TestValidationResult::test_warnings_filters_only_warnings PASSED
tests/test_validation_service.py::TestValidationResult::test_mixed_errors_and_warnings PASSED
```

## Notes

### Compatibility Matrices Tested

**Framework-Language (validation_service.py:160-182):**
- FASTAPI → Python ✅
- DJANGO → Python ✅
- EXPRESS → TypeScript, JavaScript ✅
- NESTJS → TypeScript ✅
- GIN → Go ✅
- AXUM → Rust ✅
- SPRING → Java ✅
- NONE → All languages ✅

**Framework-Architecture (validation_service.py:185-211):**
- FASTAPI → SIMPLE, LAYERED, DDD, CLEAN, HEXAGONAL ✅
- DJANGO → SIMPLE, LAYERED (NO DDD) ✅
- NESTJS → LAYERED, DDD, CLEAN ✅
- EXPRESS → SIMPLE, LAYERED ✅
- GIN → SIMPLE, LAYERED, CLEAN ✅
- AXUM → SIMPLE, LAYERED, CLEAN ✅
- SPRING → SIMPLE, LAYERED, DDD, CLEAN, HEXAGONAL ✅
- NONE → SIMPLE only ✅

### Critical Templates Validated
- `claude/settings.json.j2` - Claude configuration
- `claude/hooks/user_prompt_submit.py.j2` - User prompt hook

### Test Pattern
Tests follow the existing pattern from `test_template_repo.py`:
- Fixtures for infrastructure (repos, directories)
- Inline test data for clarity
- Organized in classes by functional category
- Descriptive names with comprehensive docstrings
- Assert error messages include relevant context
- Verify suggestions are provided for errors

### Benefits
- Early error detection prevents partial scaffold generation
- Clear error messages with suggestions guide users to fixes
- Warnings don't block execution but inform users of potential issues
- Multiple errors reported together for efficient debugging
- Comprehensive test coverage ensures validation reliability
