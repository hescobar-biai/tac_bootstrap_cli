# ValidationService - Multi-Layer Pre-Scaffold Validation

**ADW ID:** feature_4_1
**Date:** 2026-01-24
**Specification:** specs/issue-159-adw-feature_4_1-sdlc_planner-validation-service.md

## Overview

ValidationService is a centralized validation service that performs comprehensive multi-layer validation before TAC Bootstrap generates any files. The service validates configurations at domain, template, filesystem, and git layers, accumulating ALL validation issues before returning results. This prevents partial generations that fail mid-process and provides users with complete error reports upfront.

## What Was Built

- `ValidationLevel` enum defining 5 validation layers (SCHEMA, DOMAIN, TEMPLATE, FILESYSTEM, GIT)
- `ValidationIssue` Pydantic model representing individual validation problems with actionable suggestions
- `ValidationResult` Pydantic model containing validation status and accumulated issues
- `ValidationService` class implementing multi-layer validation logic with three public methods:
  - `validate_config()` - Domain and template validation for TACConfig
  - `validate_entity()` - Entity-specific validations for EntitySpec
  - `validate_pre_scaffold()` - Comprehensive pre-generation gate checking all layers
- Framework/Language compatibility matrix (13 frameworks × 6 languages)
- Framework/Architecture compatibility matrix (13 frameworks × 5 architectures)
- Helper methods for each validation layer: domain, template, filesystem, git

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py`: Complete 559-line implementation with comprehensive validation logic across all layers

### Key Changes

**Data Models (lines 57-126)**:
- `ValidationLevel` enum with 5 validation layers
- `ValidationIssue` model with level, severity, message, suggestion fields
- `ValidationResult` model with valid bool, issues list, errors() and warnings() filter methods

**Compatibility Matrices (lines 159-211)**:
- `FRAMEWORK_LANGUAGE_COMPATIBILITY` dict mapping Framework → set of compatible Languages
- `FRAMEWORK_ARCHITECTURE_COMPATIBILITY` dict mapping Framework → set of compatible Architectures
- Based on TAC Bootstrap framework support (FastAPI, Django, Flask, Express, NestJS, NextJS, React, Vue, Gin, Echo, Axum, Actix, Spring)

**ValidationService Class (lines 213-559)**:
- Constructor accepts `TemplateRepository` dependency injection for template existence checks
- `validate_config()` performs domain (framework/language/architecture compatibility) and template (existence) checks
- `validate_entity()` validates entity names as valid identifiers, field name uniqueness, field types for language
- `validate_pre_scaffold()` runs comprehensive validation across domain, template, filesystem, and git layers
- Private helper methods `_validate_domain()`, `_validate_templates()`, `_validate_filesystem()`, `_validate_git()` for layer-specific logic

**Domain Layer Validation (lines 433-498)**:
- Framework/language compatibility check with suggestions listing valid frameworks
- Framework/architecture compatibility check with suggestions listing valid architectures

**Template Layer Validation (lines 500-523)**:
- Checks existence of required command templates (.claude/commands/*.md.j2)
- Checks ADW workflow templates (adws/*.py.j2)
- Checks script templates (scripts/*.sh.j2)
- Reports missing templates with suggestions to verify template paths

**Filesystem Layer Validation (lines 525-559)**:
- Checks if output_dir exists and is writable
- Detects .tac_config.yaml conflicts (prevents overwriting existing TAC projects)
- Validates parent directory existence and writability for non-existent output_dir
- Provides suggestions on permissions and --force flag usage

**Git Layer Validation (lines 378-431)**:
- Checks git availability with `shutil.which('git')`
- Validates git repository status if available
- Warns (not errors) about uncommitted changes
- Gracefully degrades if git not installed (warning only)

## How to Use

### Basic Usage

```python
from tac_bootstrap.application.validation_service import ValidationService
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.models import TACConfig
from pathlib import Path

# Initialize service with template repository
template_repo = TemplateRepository()
validator = ValidationService(template_repo)

# Validate config for domain/template issues
result = validator.validate_config(config)
if not result.valid:
    for error in result.errors():
        print(f"ERROR: {error.message}")
        if error.suggestion:
            print(f"  → {error.suggestion}")
```

### Pre-Scaffold Validation

```python
# Comprehensive validation before generation
result = validator.validate_pre_scaffold(config, output_dir)

if result.valid:
    print("✓ All validations passed")
else:
    print(f"✗ Found {len(result.errors())} errors, {len(result.warnings())} warnings")

    # Show all errors
    for error in result.errors():
        print(f"[{error.level.upper()}] {error.message}")
        if error.suggestion:
            print(f"    Suggestion: {error.suggestion}")

    # Show warnings
    for warning in result.warnings():
        print(f"[WARNING] {warning.message}")
```

### Entity Validation

```python
from tac_bootstrap.domain.entity_config import EntitySpec

# Validate entity before generation
entity = EntitySpec(
    name="User",
    fields=["id:int", "name:str", "email:str"]
)

result = validator.validate_entity(entity, project_root)
if not result.valid:
    print("Entity validation failed:")
    for error in result.errors():
        print(f"  - {error.message}")
```

## Configuration

No configuration required. The ValidationService uses:
- **Injected Dependencies**: `TemplateRepository` for template existence checks
- **Hardcoded Compatibility Matrices**: Framework/language and framework/architecture compatibility rules
- **System Checks**: git availability via `shutil.which('git')`
- **Filesystem Checks**: Standard Python `pathlib.Path` operations for permissions

## Testing

```bash
cd tac_bootstrap_cli && uv run pytest tests/application/test_validation_service.py -v
```

### Test Coverage

The implementation includes comprehensive test scenarios:

1. **ValidationResult Tests** - Filtering errors vs warnings, valid flag computation
2. **validate_config Domain Tests** - Framework/language/architecture compatibility checks
3. **validate_config Template Tests** - Missing template detection with mocked TemplateRepository
4. **validate_entity Tests** - Entity name validation, field uniqueness, field type validation
5. **validate_pre_scaffold Filesystem Tests** - Directory permissions, .tac_config.yaml conflicts
6. **validate_pre_scaffold Git Tests** - Git availability, uncommitted changes warnings
7. **Integration Tests** - Multiple errors accumulated across layers, error/warning mix

### Edge Cases Covered

- Framework.NONE compatible with all languages and SIMPLE architecture
- Git not installed (warning, not error)
- Git repo with uncommitted changes (warning only)
- Multiple incompatibilities reported simultaneously
- Symbolic links in output_dir paths
- Non-existent parent directories
- Read-only filesystem detection

## Notes

### Design Decisions

**No Exceptions**: The service never raises exceptions - it always returns a `ValidationResult` for structured error handling. This allows callers to collect complete error reports before deciding whether to proceed.

**Accumulates All Issues**: Unlike fail-fast validation, ValidationService accumulates ALL validation issues across all layers before returning. Users see everything wrong at once.

**Errors vs Warnings**: The service distinguishes between:
- **Errors** (severity="error"): Block generation, set `valid=False`
- **Warnings** (severity="warning"): Informational only, don't affect `valid` flag

**Actionable Suggestions**: Every validation issue includes a `suggestion` field with concrete guidance on resolution (e.g., "Use FastAPI or Django for Python projects", "Check template path in repository").

**Dependency Injection**: Uses constructor injection for `TemplateRepository` following DDD principles. Makes the service testable and decoupled from infrastructure concerns.

**Graceful Degradation**: Git validation is lenient - missing git or uncommitted changes produce warnings, not errors. Supports non-git workflows.

### Compatibility Matrices

The hardcoded compatibility matrices align with TAC Bootstrap's framework support:

**Framework → Language**:
- Python: FastAPI, Django, Flask
- TypeScript/JavaScript: Express, NestJS, NextJS, React, Vue
- Go: Gin, Echo
- Rust: Axum, Actix
- Java: Spring

**Framework → Architecture**:
- FastAPI: SIMPLE, LAYERED, DDD, CLEAN, HEXAGONAL (most flexible)
- Django: SIMPLE, LAYERED (opinionated MVC)
- Flask: SIMPLE, LAYERED, CLEAN
- Express: SIMPLE, LAYERED, DDD, CLEAN
- NestJS: LAYERED, DDD, CLEAN (enterprise-focused)
- Go/Rust/Java: SIMPLE, LAYERED, CLEAN

### Future Enhancements

1. **Externalize Matrices**: Move compatibility rules to YAML/JSON config for easier customization
2. **Strict Mode**: Add `--strict` flag to treat warnings as errors
3. **Custom Validators**: Plugin system for project-specific validation rules
4. **Performance**: Cache template existence checks for repeated validations
5. **Rich Formatting**: Integration with Rich library for colorized terminal output

### Integration Points

While this task creates a standalone service, future integration involves:
- Calling `validate_pre_scaffold()` from CLI `tac-bootstrap init` before `ScaffoldService.apply_plan()` (tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py:150)
- Calling `validate_entity()` from `tac-bootstrap generate entity` before template rendering (tac_bootstrap_cli/tac_bootstrap/application/generate_service.py:80)
- Displaying validation results in Rich formatted tables for better UX
- Adding `--skip-validation` flag for advanced users who want to bypass checks

### Alignment with Existing Code

The ValidationService integrates seamlessly with existing TAC Bootstrap patterns:
- Uses same `TACConfig`, `EntitySpec` domain models (tac_bootstrap_cli/tac_bootstrap/domain/models.py:1)
- Leverages existing `TemplateRepository` infrastructure (tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py:1)
- References `GitAdapter` for git operations (tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py:1)
- Follows application service pattern like `ScaffoldService`, `GenerateService` (tac_bootstrap_cli/tac_bootstrap/application/)
