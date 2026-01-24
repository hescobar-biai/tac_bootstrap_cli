# Feature: Domain Compatibility Validators

## Metadata
issue_number: `160`
adw_id: `feature_4_2`
issue_json: `{"number":160,"title":"Tarea 4.2: Reglas de compatibilidad en domain","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_4_2\n\n****Tipo**: feature\n**Ganancia**: Previene combinaciones invalidas (e.g., Go + FastAPI, Rust + npm) con mensajes claros de que combinaciones son validas.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tac_bootstrap/domain/validators.py`\n2. Definir reglas de compatibilidad:\n   ```python\n   COMPATIBLE_FRAMEWORKS: dict[Language, list[Framework]] = {\n       Language.PYTHON: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE],\n       Language.TYPESCRIPT: [Framework.NEXTJS, Framework.EXPRESS, Framework.NESTJS, Framework.REACT, Framework.VUE, Framework.NONE],\n       # ... etc\n   }\n\n   COMPATIBLE_PACKAGE_MANAGERS: dict[Language, list[PackageManager]] = {\n       Language.PYTHON: [PackageManager.UV, PackageManager.POETRY, PackageManager.PIP, PackageManager.PIPENV],\n       # ... etc\n   }\n\n   ARCHITECTURES_REQUIRING_BASE_CLASSES = [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]\n   ```\n3. Funciones de validacion:\n   - `validate_framework_language(fw, lang) -> ValidationIssue | None`\n   - `validate_package_manager_language(pm, lang) -> ValidationIssue | None`\n   - `validate_architecture_framework(arch, fw) -> ValidationIssue | None`\n\n**Criterios de aceptacion**:\n- Todas las combinaciones invalidas producen mensajes claros\n- Sugerencias incluyen alternativas validas\n- \n# FASE 4: Multi-layer Validation\n\n**Objetivo**: Validar en multiples capas antes de aplicar cambios al filesystem.\n\n**Ganancia de la fase**: Errores detectados temprano con mensajes claros. Evita generar archivos parciales que luego fallan en runtime.\n\n---"}`

## Feature Description
This feature creates a domain-level validator module that defines explicit compatibility rules between languages, frameworks, package managers, and architectures. The module will contain comprehensive compatibility matrices and validation functions that return structured ValidationIssue objects with clear error messages and actionable suggestions. This provides early validation to prevent invalid configuration combinations (e.g., Go + FastAPI, Rust + npm) before scaffold generation.

## User Story
As a TAC Bootstrap user
I want to receive clear, immediate feedback when I configure incompatible combinations
So that I can fix configuration errors before scaffold generation starts, saving time and avoiding partial file generation

## Problem Statement
Currently, the ValidationService in tac_bootstrap/application/validation_service.py contains hardcoded compatibility matrices (FRAMEWORK_LANGUAGE_COMPATIBILITY, FRAMEWORK_ARCHITECTURE_COMPATIBILITY). This violates separation of concerns - domain validation rules belong in the domain layer, not the application layer. Additionally, there's no validation for package manager compatibility with languages, which can lead to runtime errors. Users may waste time with invalid configurations that fail during generation rather than during initial validation.

## Solution Statement
Create a new `tac_bootstrap/domain/validators.py` module that:
1. Defines a ValidationIssue Pydantic model with fields: message, field_name, invalid_value, and suggestions
2. Establishes comprehensive compatibility mappings for all supported languages (Python/TypeScript/Go/Rust/Java) with their valid frameworks and package managers
3. Implements three pairwise validation functions that check language-framework, language-package-manager, and architecture-framework compatibility
4. Returns None on success or ValidationIssue with helpful suggestions on failure
5. Includes a reference constant ARCHITECTURES_REQUIRING_BASE_CLASSES for template generation logic

The ValidationService will then be refactored to use these domain validators instead of maintaining its own matrices.

## Relevant Files
Files needed for implementing the feature:

### Existing Files to Read/Reference
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Contains Language, Framework, Architecture, PackageManager enums that validators will use
- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py` - Contains existing compatibility matrices to extract and refactor into domain layer; defines ValidationIssue model to reference
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - May need to export new validators module

### New Files
- `tac_bootstrap_cli/tac_bootstrap/domain/validators.py` - New module containing ValidationIssue model, compatibility mappings, and validation functions
- `tac_bootstrap_cli/tests/test_validators.py` - New unit tests for domain validators

## Implementation Plan

### Phase 1: Foundation
1. Read existing ValidationService to understand current ValidationIssue model structure
2. Read domain/models.py to verify all necessary enums exist (Language, Framework, Architecture, PackageManager)
3. Identify all framework values across all languages from models.py enums
4. Document the structure and fields needed for ValidationIssue Pydantic model

### Phase 2: Core Implementation
1. Create `tac_bootstrap_cli/tac_bootstrap/domain/validators.py` file
2. Define ValidationIssue Pydantic BaseModel with fields:
   - message: str
   - field_name: str
   - invalid_value: Any
   - suggestions: list[str] | None
3. Define COMPATIBLE_FRAMEWORKS mapping:
   - Python: FastAPI, Django, Flask, None
   - TypeScript: NextJS, Express, NestJS, React, Vue, None
   - JavaScript: NextJS, Express, React, Vue, None
   - Go: Gin, Echo, Fiber, Chi, None
   - Rust: Actix, Rocket, Axum, None
   - Java: Spring, Quarkus, Micronaut, None
4. Define COMPATIBLE_PACKAGE_MANAGERS mapping:
   - Python: UV, Poetry, pip, pipenv
   - TypeScript/JavaScript: npm, yarn, pnpm, bun
   - Go: go modules (single option)
   - Rust: cargo (single option)
   - Java: maven, gradle
5. Define ARCHITECTURES_REQUIRING_BASE_CLASSES constant:
   - List containing: DDD, Clean, Hexagonal
6. Implement validate_framework_language(framework, language) -> ValidationIssue | None:
   - Check if framework is valid for language
   - Return None on success
   - Return ValidationIssue with error message and suggestions listing valid frameworks on failure
7. Implement validate_package_manager_language(package_manager, language) -> ValidationIssue | None:
   - Check if package manager is valid for language
   - Return None on success
   - Return ValidationIssue with error message and suggestions listing valid package managers on failure
8. Implement validate_architecture_framework(architecture, framework) -> ValidationIssue | None:
   - Check if architecture has sufficient framework support
   - DDD/Clean/Hexagonal require substantial frameworks (not None)
   - Return None on success
   - Return ValidationIssue with error message and suggestions on failure

### Phase 3: Integration
1. Update `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` to export ValidationIssue and validation functions
2. Create comprehensive unit tests in `tac_bootstrap_cli/tests/test_validators.py`:
   - Test all valid combinations return None
   - Test all invalid combinations return ValidationIssue
   - Test ValidationIssue contains suggestions
   - Test edge cases (None framework, etc.)
3. Run validation commands to ensure no regressions

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Foundation - Read Existing Code
- Read tac_bootstrap_cli/tac_bootstrap/application/validation_service.py to understand ValidationIssue structure
- Read tac_bootstrap_cli/tac_bootstrap/domain/models.py to verify enums exist
- Document all framework enum values and their intended language mappings
- Document all package manager enum values and their intended language mappings

### Task 2: Create validators.py Module
- Create tac_bootstrap_cli/tac_bootstrap/domain/validators.py
- Add module docstring explaining purpose
- Import necessary types from domain.models (Language, Framework, Architecture, PackageManager)
- Import Pydantic BaseModel and Any from typing

### Task 3: Define ValidationIssue Model
- Create ValidationIssue as Pydantic BaseModel
- Add fields: message (str), field_name (str), invalid_value (Any), suggestions (list[str] | None)
- Add docstring with example usage

### Task 4: Define Compatibility Mappings
- Create COMPATIBLE_FRAMEWORKS: dict[Language, list[Framework]]
- Add mappings for Python, TypeScript, JavaScript, Go, Rust, Java
- Create COMPATIBLE_PACKAGE_MANAGERS: dict[Language, list[PackageManager]]
- Add mappings for all languages
- Create ARCHITECTURES_REQUIRING_BASE_CLASSES: list[Architecture]
- Add DDD, Clean, Hexagonal to the list

### Task 5: Implement validate_framework_language Function
- Function signature: validate_framework_language(framework: Framework, language: Language) -> ValidationIssue | None
- Check if language exists in COMPATIBLE_FRAMEWORKS[framework]
- Return None if valid
- Return ValidationIssue with message, field_name="framework", invalid_value=framework.value, suggestions=[list of valid frameworks] if invalid
- Add docstring and type hints

### Task 6: Implement validate_package_manager_language Function
- Function signature: validate_package_manager_language(package_manager: PackageManager, language: Language) -> ValidationIssue | None
- Check if language exists in COMPATIBLE_PACKAGE_MANAGERS
- Check if package_manager is in the list for that language
- Return None if valid
- Return ValidationIssue with message, field_name="package_manager", invalid_value=package_manager.value, suggestions=[list of valid package managers] if invalid
- Add docstring and type hints

### Task 7: Implement validate_architecture_framework Function
- Function signature: validate_architecture_framework(architecture: Architecture, framework: Framework) -> ValidationIssue | None
- Check if architecture is in ARCHITECTURES_REQUIRING_BASE_CLASSES
- If yes, check that framework is not Framework.NONE
- Return None if valid
- Return ValidationIssue with message explaining DDD/Clean/Hexagonal need substantial frameworks, suggestions listing recommended frameworks if invalid
- Add docstring and type hints

### Task 8: Update Domain __init__.py
- Read tac_bootstrap_cli/tac_bootstrap/domain/__init__.py
- Add exports for ValidationIssue and the three validation functions
- Ensure proper imports from validators module

### Task 9: Create Comprehensive Unit Tests
- Create tac_bootstrap_cli/tests/test_validators.py
- Import validators module and all necessary enums
- Write test_validate_framework_language_valid_combinations testing all valid language-framework pairs
- Write test_validate_framework_language_invalid_combinations testing invalid pairs (e.g., Go + FastAPI)
- Write test_validate_package_manager_language_valid_combinations testing all valid language-package manager pairs
- Write test_validate_package_manager_language_invalid_combinations testing invalid pairs (e.g., Python + npm)
- Write test_validate_architecture_framework_valid testing valid architecture-framework pairs
- Write test_validate_architecture_framework_invalid testing DDD/Clean/Hexagonal with Framework.NONE
- Write test_validation_issue_contains_suggestions verifying suggestions are populated
- Write test_validation_issue_structure verifying ValidationIssue has correct fields

### Task 10: Run Validation Commands
- Execute all validation commands to verify no regressions
- Fix any test failures or type errors
- Ensure all unit tests pass

## Testing Strategy

### Unit Tests
- **Valid Combinations**: Test all valid language-framework, language-package-manager, and architecture-framework combinations return None
- **Invalid Combinations**: Test invalid combinations return ValidationIssue with proper structure
- **Suggestions Present**: Verify all ValidationIssue objects contain non-empty suggestions lists
- **Field Population**: Verify ValidationIssue.field_name, invalid_value, and message are correctly populated
- **Edge Cases**: Test Framework.NONE with all languages, test architectures requiring base classes
- **Enum Coverage**: Ensure all enum values from domain/models.py are covered in mappings

### Edge Cases
- Framework.NONE with all languages (should be valid)
- Framework.NONE with DDD/Clean/Hexagonal architectures (should be invalid)
- Languages with single package manager option (Go, Rust)
- Package managers that support multiple languages (npm, yarn, pnpm, bun for TypeScript/JavaScript)
- Architecture.SIMPLE with any framework (should always be valid)

## Acceptance Criteria
1. `tac_bootstrap_cli/tac_bootstrap/domain/validators.py` exists with ValidationIssue Pydantic model
2. COMPATIBLE_FRAMEWORKS mapping covers all 6 languages (Python, TypeScript, JavaScript, Go, Rust, Java)
3. COMPATIBLE_PACKAGE_MANAGERS mapping covers all 6 languages with correct package managers
4. ARCHITECTURES_REQUIRING_BASE_CLASSES contains [DDD, Clean, Hexagonal]
5. validate_framework_language() returns None for valid combinations, ValidationIssue for invalid
6. validate_package_manager_language() returns None for valid combinations, ValidationIssue for invalid
7. validate_architecture_framework() returns None for valid combinations, ValidationIssue for invalid
8. All ValidationIssue objects contain clear error messages
9. All ValidationIssue objects contain suggestions listing valid alternatives
10. Invalid combinations produce messages like "Framework fastapi is not compatible with language go. Valid frameworks for go: gin, echo, fiber, chi, none"
11. All unit tests pass with 100% coverage of validation functions
12. No regressions in existing tests

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This feature is part of FASE 4: Multi-layer Validation from PLAN_TAC_BOOTSTRAP.md
- ValidationIssue model defined here may differ from the one in validation_service.py - this domain version is the source of truth
- After implementation, validation_service.py should be refactored to use these domain validators instead of maintaining its own matrices (future task)
- The ARCHITECTURES_REQUIRING_BASE_CLASSES constant is reference data for template generation, not a validation function
- Keep validators focused on pairwise validation rules - cross-cutting validation can be added later if needed
- Enum comparison should be case-insensitive by using enum values directly
- Design supports collecting multiple validation errors before failing (each function returns ValidationIssue | None, allowing accumulation)
- Follow existing Pydantic patterns from domain/models.py for consistency
