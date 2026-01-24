# Domain Compatibility Validators

**ADW ID:** feature_4_2
**Date:** 2026-01-24
**Specification:** specs/issue-160-adw-feature_4_2-sdlc_planner-domain-compatibility-validators.md

## Overview

This feature implements domain-level validation rules for TAC Bootstrap configurations, providing explicit compatibility matrices between languages, frameworks, package managers, and architectures. The module prevents invalid configuration combinations (e.g., Go + FastAPI, Rust + npm) with clear error messages and actionable suggestions, enabling early validation before scaffold generation begins.

## What Was Built

- **ValidationIssue Model**: Pydantic model representing validation errors with message, field_name, invalid_value, and suggestions
- **Compatibility Matrices**: Comprehensive mappings for all supported languages (Python, TypeScript, JavaScript, Go, Rust, Java) with their valid frameworks and package managers
- **Validation Functions**: Three pairwise validation functions checking language-framework, language-package-manager, and architecture-framework compatibility
- **Reference Constants**: ARCHITECTURES_REQUIRING_BASE_CLASSES constant for template generation logic
- **Comprehensive Tests**: 525+ lines of unit tests covering all valid/invalid combinations and edge cases

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/validators.py`: New module with 317 lines containing ValidationIssue model, compatibility matrices, and three validation functions
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py`: Updated to export ValidationIssue and validation functions from validators module
- `tac_bootstrap_cli/tests/test_validators.py`: New test file with 525 lines covering all validation scenarios

### Key Changes

1. **ValidationIssue Model** (tac_bootstrap/domain/validators.py:46-73): Pydantic BaseModel with clear structure for validation errors, including actionable suggestions for users

2. **COMPATIBLE_FRAMEWORKS** (tac_bootstrap/domain/validators.py:81-117): Dictionary mapping each Language enum to list of compatible Framework enums, covering all 6 supported languages

3. **COMPATIBLE_PACKAGE_MANAGERS** (tac_bootstrap/domain/validators.py:120-148): Dictionary mapping each Language to list of valid PackageManager options, ensuring correct tooling for each language

4. **ARCHITECTURES_REQUIRING_BASE_CLASSES** (tac_bootstrap/domain/validators.py:151-155): Constant list containing DDD, Clean, and Hexagonal architectures that require substantial frameworks

5. **validate_framework_language()** (tac_bootstrap/domain/validators.py:163-206): Validates framework-language compatibility, returns None on success or ValidationIssue with suggestions on failure

6. **validate_package_manager_language()** (tac_bootstrap/domain/validators.py:209-258): Validates package manager-language compatibility with clear error messages

7. **validate_architecture_framework()** (tac_bootstrap/domain/validators.py:261-317): Validates that advanced architectures (DDD, Clean, Hexagonal) have substantial framework support

## How to Use

### Import Validators

```python
from tac_bootstrap.domain.validators import (
    validate_framework_language,
    validate_package_manager_language,
    validate_architecture_framework,
    ValidationIssue
)
from tac_bootstrap.domain.models import Language, Framework, PackageManager, Architecture
```

### Validate Framework-Language Compatibility

```python
# Check if FastAPI is compatible with Go
issue = validate_framework_language(Framework.FASTAPI, Language.GO)
if issue:
    print(f"ERROR: {issue.message}")
    print(f"Valid options: {', '.join(issue.suggestions)}")
    # Output:
    # ERROR: Framework fastapi is not compatible with language go. Valid frameworks for go: gin, echo, none
    # Valid options: gin, echo, none
```

### Validate Package Manager-Language Compatibility

```python
# Check if npm is compatible with Python
issue = validate_package_manager_language(PackageManager.NPM, Language.PYTHON)
if issue:
    print(f"ERROR: {issue.message}")
    print(f"Suggestions: {', '.join(issue.suggestions)}")
    # Output:
    # ERROR: Package manager npm is not compatible with language python. Valid package managers for python: uv, poetry, pip, pipenv
    # Suggestions: uv, poetry, pip, pipenv
```

### Validate Architecture-Framework Compatibility

```python
# Check if DDD architecture works with Framework.NONE
issue = validate_architecture_framework(Architecture.DDD, Framework.NONE)
if issue:
    print(f"ERROR: {issue.message}")
    for suggestion in issue.suggestions:
        print(f"  - {suggestion}")
    # Output:
    # ERROR: Architecture ddd requires a substantial framework. Framework 'none' is not sufficient. DDD/Clean/Hexagonal architectures need frameworks that support dependency injection and layering.
    #   - Use Architecture.SIMPLE or Architecture.LAYERED with Framework.NONE
    #   - Choose a substantial framework (FastAPI, NestJS, Spring, etc.) for advanced architectures
```

### Use in ValidationService

```python
# Example integration in application layer
def validate_config(config: ProjectConfig) -> list[ValidationIssue]:
    issues = []

    # Validate framework-language
    issue = validate_framework_language(config.framework, config.language)
    if issue:
        issues.append(issue)

    # Validate package manager-language
    issue = validate_package_manager_language(config.package_manager, config.language)
    if issue:
        issues.append(issue)

    # Validate architecture-framework
    issue = validate_architecture_framework(config.architecture, config.framework)
    if issue:
        issues.append(issue)

    return issues
```

## Configuration

No additional configuration required. The validators use the domain model enums directly from `tac_bootstrap.domain.models`.

### Supported Languages

- Python (UV, Poetry, pip, pipenv)
- TypeScript (npm, yarn, pnpm, bun)
- JavaScript (npm, yarn, pnpm, bun)
- Go (go modules)
- Rust (cargo)
- Java (Maven, Gradle)

### Supported Frameworks by Language

- **Python**: FastAPI, Django, Flask, None
- **TypeScript**: NextJS, Express, NestJS, React, Vue, None
- **JavaScript**: NextJS, Express, React, Vue, None
- **Go**: Gin, Echo, None
- **Rust**: Axum, Actix, None
- **Java**: Spring, None

### Architecture Requirements

- **Simple/Layered**: Work with any framework including None
- **DDD/Clean/Hexagonal**: Require substantial frameworks (not None)

## Testing

Run all validator tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_validators.py -v
```

Run specific test classes:

```bash
# Test framework-language validation
cd tac_bootstrap_cli && uv run pytest tests/test_validators.py::TestValidateFrameworkLanguage -v

# Test package manager-language validation
cd tac_bootstrap_cli && uv run pytest tests/test_validators.py::TestValidatePackageManagerLanguage -v

# Test architecture-framework validation
cd tac_bootstrap_cli && uv run pytest tests/test_validators.py::TestValidateArchitectureFramework -v

# Test edge cases
cd tac_bootstrap_cli && uv run pytest tests/test_validators.py::TestEdgeCases -v
```

### Test Coverage

- 100% coverage of validation functions
- All valid combinations tested (return None)
- All invalid combinations tested (return ValidationIssue)
- Edge cases: Framework.NONE with all languages/architectures
- Boundary cases: Single package manager languages (Go, Rust)
- TypeScript/JavaScript shared package manager compatibility

## Notes

- This is part of **FASE 4: Multi-layer Validation** from PLAN_TAC_BOOTSTRAP.md
- The ValidationIssue model in this domain module is the source of truth for domain validation
- The existing ValidationService in `application/validation_service.py` should be refactored to use these domain validators (future task)
- All validation functions return None on success or ValidationIssue on failure, enabling validation error accumulation
- The ARCHITECTURES_REQUIRING_BASE_CLASSES constant is reference data for template generation logic, not used directly in validation
- Validators are focused on pairwise validation rules - cross-cutting validation can be added later if needed
- All enum comparisons use enum values directly for consistent case handling
