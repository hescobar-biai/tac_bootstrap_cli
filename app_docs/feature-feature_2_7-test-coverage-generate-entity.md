# Test Coverage for Generate Entity Command

**ADW ID:** feature_2_7
**Date:** 2026-01-23
**Specification:** specs/issue-152-adw-feature_2_7-chore_planner-tests-generate-entity.md

## Overview

Comprehensive test suite for the `generate entity` command, achieving >90% coverage for entity generation orchestration. Tests cover EntitySpec validation, GenerateService file generation, base class dependency checking, file conflict detection, template rendering, and force overwrite behavior.

## What Was Built

- **test_generate_service.py** - 789 lines of comprehensive unit tests for GenerateService application service
- **pytest-cov dependency** - Added pytest-cov>=7.0.0 for test coverage reporting

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_generate_service.py`: NEW FILE - Complete test suite for GenerateService orchestration logic
- `tac_bootstrap_cli/pyproject.toml`: Added pytest-cov dependency for coverage analysis
- `tac_bootstrap_cli/uv.lock`: Updated lock file with pytest-cov>=7.0.0

### Key Changes

- **TestValidateEntitySpec**: Tests for entity specification validation (PascalCase names, snake_case capabilities)
- **TestCheckBaseClasses**: Tests for base class precondition checks (BaseModel, BaseSchema, BaseService, BaseRepository existence)
- **TestCheckExistingFiles**: Tests for file conflict detection (all-or-nothing approach, force overwrite behavior)
- **TestRenderTemplates**: Tests for Jinja2 template rendering (6 templates, context injection, error handling)
- **TestWriteFiles**: Tests for filesystem operations (file writing, __init__.py creation, relative path handling)
- **TestGenerateEntity**: Integration tests for complete entity generation flow (success, validation failures, precondition errors, authorized entities)

## How to Use

### Run the New Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_generate_service.py -v
```

### Run with Coverage Analysis

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_generate_service.py \
  --cov=tac_bootstrap.application.generate_service \
  --cov-report=term-missing
```

### Run All Entity Generation Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_generate_service.py -v
```

### Check Coverage for All Entity Generation Modules

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_generate_service.py \
  --cov=tac_bootstrap.domain.entity_config \
  --cov=tac_bootstrap.application.generate_service \
  --cov-report=term-missing
```

## Configuration

No configuration required. The test suite uses:
- **pytest fixtures** for dependency mocking (mock_fs, mock_template_repo)
- **tmp_path fixture** for isolated filesystem testing
- **Mock objects** to test GenerateService in isolation without filesystem side effects

## Testing

The test suite itself validates:

1. **Entity Validation**: EntitySpec with invalid capability format raises ValidationError
2. **Precondition Checks**: Missing base classes (base_entity.py, base_repository.py, base_schema.py, base_service.py) raise PreconditionError
3. **File Conflicts**: Existing entity files without force=False raise FileExistsError with helpful message
4. **Force Overwrite**: force=True allows overwriting existing files
5. **Template Rendering**: 6 templates rendered (domain, schemas, service, repository, models, routes) with correct context
6. **Filesystem Operations**: Files written to correct paths, __init__.py files created, relative paths returned
7. **Integration Flow**: Complete generation succeeds when all preconditions met, fails fast with validation errors
8. **Authorized Entities**: authorized=True includes tenant_id in template context
9. **Phase Ordering**: Validation happens before any filesystem writes (fail-fast approach)

### Run All Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Verify Coverage Threshold

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_generate_service.py \
  --cov=tac_bootstrap.domain.entity_config \
  --cov=tac_bootstrap.application.generate_service \
  --cov-report=term-missing \
  --cov-fail-under=90
```

## Notes

### Test Architecture

- **Unit tests** use mocked dependencies (FileSystem, TemplateRepository) to test GenerateService in isolation
- **Fixtures** provide reusable test data (sample_entity_spec, authorized_entity_spec, mock_config)
- **Parametric side effects** simulate different filesystem states (base classes exist/missing, entity files exist/don't exist)
- **Integration tests** verify complete end-to-end flow without mocking orchestration logic

### Coverage Targets Achieved

- `entity_config.py`: >90% (existing test_entity_config.py)
- `generate_service.py`: >90% (new test_generate_service.py)
- Combined coverage: >90% for all entity generation modules

### Test Data Patterns

Tests use realistic entity specifications:
```python
EntitySpec(
    name="Product",
    capability="catalog",
    fields=[
        FieldSpec(name="title", field_type=FieldType.STRING, max_length=200, required=True),
        FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
    ],
    authorized=False,
    async_mode=False
)
```

### Key Testing Insights

1. **Validation-first approach**: GenerateService validates EntitySpec and checks preconditions before any filesystem writes
2. **All-or-nothing file generation**: Either all 10 files created (6 templates + 4 __init__.py) or none (prevents partial state)
3. **Helpful error messages**: FileExistsError includes list of conflicting files and suggests force=True
4. **Template context injection**: All templates rendered with entity and config context
5. **Authorized entity support**: authorized=True changes template context for multi-tenant CRUD
