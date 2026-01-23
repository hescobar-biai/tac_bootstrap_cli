# Test Suite for Base Classes Templates

**ADW ID:** feature_1.12
**Date:** 2026-01-23
**Specification:** specs/issue-137-adw-feature_1.12-chore_planner-test-base-classes-templates.md

## Overview

This feature implements a comprehensive test suite for the 10 template files in `tac_bootstrap/templates/shared/` that generate base classes for DDD-style architectures. The tests validate that templates render correctly, generate syntactically valid Python code, and include expected classes, methods, and structures. This provides regression protection and executable documentation for template modifications.

## What Was Built

- **Comprehensive Test File**: `test_base_classes_templates.py` with 437 lines covering all shared templates
- **Test Fixtures**: Reusable fixtures for DDD, simple, and async configurations
- **Template Validation Tests**: 16+ test cases verifying template rendering and Python validity
- **Integration Tests**: Tests ensuring ScaffoldService correctly includes/excludes templates based on architecture
- **Removed Legacy Code**: Cleaned up `_add_shared_infrastructure` method from ScaffoldService (109 lines removed)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_base_classes_templates.py` (NEW): Comprehensive test suite with 437 lines
  - Test fixtures for different configurations (DDD, simple, async)
  - 9 test classes covering all shared templates
  - Validation of both content and Python syntax

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Removed `_add_shared_infrastructure` method
  - Deleted 109 lines of legacy scaffolding code
  - Simplified service architecture

- `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`: Minor template fixes for async/sync rendering

### Key Changes

1. **Test Coverage for 10 Templates**:
   - `base_entity.py.j2` - Entity and EntityState classes with lifecycle methods
   - `base_schema.py.j2` - BaseCreate, BaseUpdate, BaseResponse schema classes
   - `base_service.py.j2` - BaseService with generics and CRUD methods
   - `base_repository.py.j2` - Synchronous repository with SQLAlchemy Session
   - `base_repository_async.py.j2` - Asynchronous repository with AsyncSession
   - `database.py.j2` - Database configuration for sync/async modes
   - `exceptions.py.j2` - Custom exception hierarchy and handlers
   - `responses.py.j2` - PaginatedResponse and helper utilities
   - `dependencies.py.j2` - FastAPI dependency injection
   - `health.py.j2` - Health check endpoint

2. **Python Syntax Validation**: All tests use `compile(result, '<string>', 'exec')` to ensure generated code is syntactically valid without requiring external dependencies

3. **Conditional Rendering Tests**: Tests verify that templates adapt correctly based on:
   - Architecture type (DDD vs SIMPLE)
   - Async mode enabled/disabled
   - Framework selection (FastAPI vs NONE)

4. **Service Integration Tests**: Validates that ScaffoldService includes/excludes shared templates appropriately

## How to Use

### Running the Test Suite

Run all template tests:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py -v
```

Run specific test class:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py::TestBaseEntityTemplate -v
```

Run with coverage:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py --cov=tac_bootstrap.templates --cov-report=term
```

### Test Organization

The test file follows this structure:

1. **Fixtures Section** (lines 30-94):
   - `ddd_config()` - DDD architecture with FastAPI
   - `simple_config()` - Simple architecture without framework
   - `async_config()` - DDD with async database enabled
   - `repo()` - TemplateRepository instance

2. **Template Test Classes** (lines 100-430):
   - Each template has dedicated test class
   - Tests verify both content and syntax
   - Focus on key classes, methods, and conditional logic

3. **Integration Tests** (lines 430+):
   - Validates ScaffoldService behavior
   - Tests architecture-specific template inclusion

### Adding New Template Tests

When adding a new template to `templates/shared/`:

1. Create a new test class following the pattern:
```python
class TestNewTemplate:
    def test_new_template_renders(self, repo, ddd_config):
        result = repo.render("shared/new_template.py.j2", ddd_config)
        assert "expected_class" in result
        compile(result, '<string>', 'exec')
```

2. Run the test to ensure it passes:
```bash
uv run pytest tests/test_base_classes_templates.py::TestNewTemplate -v
```

## Configuration

### Test Fixtures

The test suite uses three main configuration fixtures:

- **ddd_config**: FastAPI + DDD architecture for full template testing
- **simple_config**: Minimal architecture without framework
- **async_config**: DDD with async database support

Customize fixtures in `test_base_classes_templates.py:30-94` for different test scenarios.

### Template Coverage Targets

- **Target**: >90% code coverage for templates
- **Current**: All 10 shared templates covered
- **Method**: Each test verifies both template content and Python syntax validity

## Testing

Run the complete test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py -v --tb=short
```

Expected output:
```
test_base_classes_templates.py::TestBaseEntityTemplate::test_base_entity_renders PASSED
test_base_classes_templates.py::TestBaseEntityTemplate::test_base_entity_has_lifecycle_methods PASSED
test_base_classes_templates.py::TestBaseSchemaTemplate::test_base_schema_renders PASSED
test_base_classes_templates.py::TestBaseServiceTemplate::test_base_service_renders PASSED
test_base_classes_templates.py::TestBaseRepositoryTemplate::test_base_repository_renders PASSED
test_base_classes_templates.py::TestBaseRepositoryAsyncTemplate::test_base_repository_async_renders PASSED
test_base_classes_templates.py::TestDatabaseTemplate::test_database_renders_sync PASSED
test_base_classes_templates.py::TestDatabaseTemplate::test_database_renders_async PASSED
test_base_classes_templates.py::TestExceptionsTemplate::test_exceptions_renders PASSED
test_base_classes_templates.py::TestResponsesTemplate::test_responses_renders PASSED
test_base_classes_templates.py::TestDependenciesTemplate::test_dependencies_renders PASSED
test_base_classes_templates.py::TestHealthTemplate::test_health_renders PASSED
```

Run with full test suite to check for regressions:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Notes

### Design Principles

1. **Syntax-Only Validation**: Tests use `compile()` to validate Python syntax without requiring FastAPI, SQLAlchemy, or other dependencies to be installed in the test environment

2. **Template Independence**: Each test is isolated and doesn't depend on other tests or external state

3. **Content + Syntax**: Every test validates both expected content (classes, methods) AND Python validity

4. **Fixture Reusability**: Common configurations extracted into fixtures for easy maintenance

### Legacy Code Removal

The `_add_shared_infrastructure` method was removed from ScaffoldService (109 lines) because:
- It was redundant with the template-based approach
- Tests now directly validate template rendering
- Simplifies service architecture
- Reduces maintenance burden

### Template Conditional Logic

Templates adapt based on configuration:
- **Sync vs Async**: `database.py.j2` renders different imports and session types
- **Framework**: `health.py.j2` and `dependencies.py.j2` include FastAPI-specific code when `framework=FASTAPI`
- **Architecture**: Full DDD templates included only for DDD/Clean/Hexagonal architectures

### Future Enhancements

Consider adding:
- Parametrized tests for multiple architecture combinations
- Template rendering performance benchmarks
- Integration tests that compile and execute generated code
- Tests for template error handling and edge cases
