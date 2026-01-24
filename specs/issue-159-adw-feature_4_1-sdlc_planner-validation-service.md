# Feature: ValidationService - Multi-Layer Pre-Scaffold Validation

## Metadata
issue_number: `159`
adw_id: `feature_4_1`
issue_json: `{"number":159,"title":"Tarea 4.1: ValidationService","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_4_1\n\n**Tipo**: feature\n**Ganancia**: Servicio centralizado que ejecuta validaciones en orden y reporta todos los errores de una vez (no falla en el primero).\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py`\n2. Definir:\n   ```python\n   class ValidationLevel(str, Enum):\n       SCHEMA = \"schema\"\n       DOMAIN = \"domain\"\n       TEMPLATE = \"template\"\n       FILESYSTEM = \"filesystem\"\n       GIT = \"git\"\n\n   class ValidationIssue(BaseModel):\n       level: ValidationLevel\n       severity: str  # \"error\", \"warning\"\n       message: str\n       suggestion: str | None = None\n\n   class ValidationResult(BaseModel):\n       valid: bool\n       issues: list[ValidationIssue]\n       def errors(self) -> list[ValidationIssue]\n       def warnings(self) -> list[ValidationIssue]\n   ```\n3. Clase `ValidationService`:\n   - `validate_config(config: TACConfig) -> ValidationResult`\n   - `validate_entity(entity: EntitySpec, project_root: Path) -> ValidationResult`\n   - `validate_pre_scaffold(config: TACConfig, output_dir: Path) -> ValidationResult`\n4. Validaciones por capa:\n   - **SCHEMA**: Pydantic ya lo hace (campos requeridos, tipos)\n   - **DOMAIN**: framework compatible con language, architecture valida para framework\n   - **TEMPLATE**: templates referenciados existen en TemplateRepository\n   - **FILESYSTEM**: output_dir existe, es escribible, no tiene conflictos\n   - **GIT**: directorio es un repo git, no tiene cambios uncommitted (warning)\n\n**Criterios de aceptacion**:\n- Reporta TODOS los errores, no solo el primero\n- Incluye sugerencias de como resolver cada issue\n- Distingue entre errors (bloquean) y warnings (informan)\n# FASE 4: Multi-layer Validation\n\n**Objetivo**: Validar en multiples capas antes de aplicar cambios al filesystem.\n\n**Ganancia de la fase**: Errores detectados temprano con mensajes claros. Evita generar archivos parciales que luego fallan en runtime.\n\n---"}`

## Feature Description

This feature implements a centralized `ValidationService` that performs comprehensive multi-layer validation before TAC Bootstrap generates any files. The service validates configuration at multiple levels (domain, template, filesystem, git) and accumulates ALL validation issues before returning results. This approach prevents partial generations that fail mid-process and provides users with a complete report of all issues upfront.

The service distinguishes between errors (which block generation) and warnings (which inform but don't block), and includes actionable suggestions for resolving each issue. Validation occurs at multiple layers: domain compatibility checks, template existence verification, filesystem safety checks, and git repository status validation.

## User Story

As a TAC Bootstrap user
I want to receive a complete validation report before any files are generated
So that I can fix all configuration issues upfront instead of encountering failures partway through scaffold generation

## Problem Statement

Currently, TAC Bootstrap may begin generating files only to fail when encountering invalid configurations, missing templates, or filesystem issues. This results in:
- Partial generations that leave the output directory in an inconsistent state
- Users discovering issues one at a time (fail on first error)
- Lack of guidance on how to resolve validation failures
- No distinction between blocking errors and informational warnings
- Manual cleanup required after failed generations

Without pre-scaffold validation, users waste time on failed generations and have no visibility into multiple configuration issues simultaneously.

## Solution Statement

We implement a `ValidationService` application service that performs comprehensive validation across four layers:

1. **SCHEMA Layer**: Handled implicitly by Pydantic validation (field types, required fields)
2. **DOMAIN Layer**: Validates framework/language compatibility, architecture validity for framework
3. **TEMPLATE Layer**: Verifies all referenced templates exist in TemplateRepository
4. **FILESYSTEM Layer**: Checks output directory exists/is writable, detects conflicts with existing .tac_config.yaml
5. **GIT Layer**: Validates git repository status, warns about uncommitted changes

The service uses dependency injection to receive a `TemplateRepository` instance and returns structured `ValidationResult` objects containing all accumulated issues. Each issue includes:
- The validation level where it occurred
- Severity (error or warning)
- Clear description of the problem
- Actionable suggestion for resolution

The service never raises exceptions - it always returns a result object, allowing callers to collect complete error reports before deciding whether to proceed.

## Relevant Files

Files that require modification:

- None (new service, no modifications to existing code required initially)

Files needed for reference:

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig, Language, Framework, Architecture enums
- `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` - EntitySpec validation patterns
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository API
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py` - Git operations (for git validation)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Integration point for validation

### New Files

- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py` - Complete ValidationService implementation

## Implementation Plan

### Phase 1: Foundation
1. Review existing validation patterns in `entity_config.py` to understand naming and field validation approaches
2. Study `models.py` to understand the compatibility helper functions (`get_frameworks_for_language`, etc.)
3. Review `TemplateRepository` interface in `template_repo.py` to understand template lookup methods
4. Review `git_adapter.py` to understand available git operations

### Phase 2: Core Implementation
1. Create `validation_service.py` with ValidationLevel enum, ValidationIssue model, ValidationResult model
2. Implement ValidationResult helper methods: `errors()`, `warnings()`
3. Define framework/language compatibility matrix as class constant
4. Define framework/architecture compatibility matrix as class constant
5. Implement `ValidationService` class with injected TemplateRepository dependency
6. Implement `validate_config()` for domain and template validations
7. Implement `validate_entity()` for entity-specific validations
8. Implement `validate_pre_scaffold()` as comprehensive pre-generation gate

### Phase 3: Integration
1. Add comprehensive docstrings to all classes and methods
2. Ensure all validation issues include actionable suggestions
3. Verify compatibility matrices align with existing helper functions in models.py

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review Existing Patterns
- Read `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` to understand field/entity validation patterns
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` lines 699-772 to understand compatibility helper functions
- Read `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` to understand template existence checks
- Read `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py` to understand git status operations

### Task 2: Create ValidationService Models
- Create `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py`
- Define `ValidationLevel` enum with SCHEMA, DOMAIN, TEMPLATE, FILESYSTEM, GIT levels
- Define `ValidationIssue` Pydantic model with level, severity, message, suggestion fields
- Define `ValidationResult` Pydantic model with valid bool, issues list, errors() method, warnings() method
- Add comprehensive docstrings explaining each model's purpose and usage

### Task 3: Implement Compatibility Matrices
- Define `FRAMEWORK_LANGUAGE_COMPATIBILITY` class constant dict mapping Framework -> set of Language values
  - FastAPI: {Python}
  - Django: {Python}
  - Flask: {Python}
  - Express: {TypeScript, JavaScript}
  - NestJS: {TypeScript}
  - NextJS: {TypeScript, JavaScript}
  - React: {TypeScript, JavaScript}
  - Vue: {TypeScript, JavaScript}
  - Gin: {Go}
  - Echo: {Go}
  - Axum: {Rust}
  - Actix: {Rust}
  - Spring: {Java}
  - None: {all languages}
- Define `FRAMEWORK_ARCHITECTURE_COMPATIBILITY` class constant dict mapping Framework -> set of Architecture values
  - FastAPI: {SIMPLE, LAYERED, DDD, CLEAN, HEXAGONAL}
  - Express: {SIMPLE, LAYERED, DDD, CLEAN}
  - NestJS: {LAYERED, DDD, CLEAN}
  - Django: {SIMPLE, LAYERED}
  - Flask: {SIMPLE, LAYERED, CLEAN}
  - All Go/Rust/Java frameworks: {SIMPLE, LAYERED, CLEAN}
  - None: {SIMPLE}

### Task 4: Implement ValidationService Class
- Define `ValidationService` class with `__init__(self, template_repo: TemplateRepository)` constructor
- Store template_repo as instance variable for template existence checks
- Add class-level docstring explaining service purpose and usage examples

### Task 5: Implement validate_config Method
- Implement `validate_config(self, config: TACConfig) -> ValidationResult`
- Create empty issues list to accumulate all problems
- **DOMAIN validation**:
  - Check framework/language compatibility using FRAMEWORK_LANGUAGE_COMPATIBILITY
  - Add error if incompatible with suggestion listing valid frameworks for the language
  - Check framework/architecture compatibility using FRAMEWORK_ARCHITECTURE_COMPATIBILITY
  - Add error if incompatible with suggestion listing valid architectures for the framework
- **TEMPLATE validation**:
  - Check that all command templates exist (.claude/commands/*.md.j2)
  - Check that ADW workflow templates exist (adws/*.py.j2)
  - Check that script templates exist (scripts/*.sh.j2)
  - Add error for each missing template with suggestion to check template path
- Return ValidationResult with valid=True if no errors, valid=False otherwise

### Task 6: Implement validate_entity Method
- Implement `validate_entity(self, entity: EntitySpec, project_root: Path) -> ValidationResult`
- Create empty issues list
- Validate entity name is valid Python/TypeScript identifier using regex
- Validate no duplicate field names exist
- Validate field names are non-empty
- Validate field types are appropriate for project language (check config.yml in project_root)
- Add errors with suggestions for each violation
- Return ValidationResult with accumulated issues

### Task 7: Implement validate_pre_scaffold Method
- Implement `validate_pre_scaffold(self, config: TACConfig, output_dir: Path) -> ValidationResult`
- Create empty issues list
- Run DOMAIN validations (call internal helper or inline)
- Run TEMPLATE validations (call internal helper or inline)
- **FILESYSTEM validation**:
  - Check if output_dir exists:
    - If exists: check if writable, check for .tac_config.yaml conflict
    - If not exists: check parent directory exists and is writable
  - Add error if not writable with suggestion to check permissions
  - Add error if .tac_config.yaml exists with suggestion to use different output_dir or --force flag
- **GIT validation**:
  - Check if git is available using `shutil.which('git')`
  - If git not available: add warning (not error)
  - If git available and output_dir is git repo:
    - Check for uncommitted changes
    - Add warning if changes exist (suggest committing before generation)
- Return ValidationResult with all accumulated issues

### Task 8: Add Helper Methods (Optional)
- Consider extracting `_validate_domain()`, `_validate_templates()`, `_validate_filesystem()`, `_validate_git()` as private methods
- This keeps `validate_pre_scaffold()` clean and readable
- Each helper returns list of ValidationIssue objects

### Task 9: Validation and Testing
- Run unit tests: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run type checking: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run linting: `cd tac_bootstrap_cli && uv run ruff check .`
- Verify smoke test: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests

Create `tests/application/test_validation_service.py` with comprehensive tests:

1. **ValidationResult Tests**
   - Test `errors()` filters only error severity issues
   - Test `warnings()` filters only warning severity issues
   - Test `valid` is False when any errors exist
   - Test `valid` is True when only warnings exist

2. **validate_config Tests - Domain Layer**
   - Test valid framework/language combination (FastAPI + Python) passes
   - Test invalid combination (FastAPI + TypeScript) fails with error and suggestion
   - Test valid framework/architecture combination (FastAPI + DDD) passes
   - Test invalid combination (Django + HEXAGONAL) fails with error and suggestion

3. **validate_config Tests - Template Layer**
   - Test all required templates exist passes
   - Test missing command template fails with error
   - Test missing ADW template fails with error
   - Mock TemplateRepository to simulate missing templates

4. **validate_entity Tests**
   - Test valid entity name passes
   - Test invalid entity name (starts with number) fails
   - Test duplicate field names fails with error
   - Test empty field names fails with error
   - Test valid field types for Python pass
   - Test invalid field types for language fail

5. **validate_pre_scaffold Tests - Filesystem Layer**
   - Test existing writable output_dir without .tac_config.yaml passes
   - Test existing output_dir with .tac_config.yaml fails with error
   - Test non-existent output_dir with writable parent passes
   - Test non-existent output_dir with non-existent parent fails
   - Test non-writable output_dir fails with error

6. **validate_pre_scaffold Tests - Git Layer**
   - Test git not installed returns warning (not error)
   - Test git repo with no uncommitted changes passes
   - Test git repo with uncommitted changes returns warning
   - Test non-git directory passes (no git validation)

7. **Integration Tests**
   - Test `validate_pre_scaffold()` accumulates ALL issues across layers
   - Test multiple errors from different layers are all reported
   - Test mix of errors and warnings correctly sets valid=False

### Edge Cases

1. **Empty template_checksums** - Should not affect validation
2. **Framework.NONE** - Should be compatible with all languages and SIMPLE architecture
3. **Multiple incompatibilities** - Should report all, not just first
4. **Git in subdirectory** - Should detect parent git repo
5. **Symbolic links in output_dir** - Should follow and validate actual target
6. **Very long suggestions** - Should remain readable and actionable
7. **Special characters in paths** - Should handle spaces, unicode correctly

## Acceptance Criteria

1. ✅ `ValidationService` class exists in `application/validation_service.py`
2. ✅ `ValidationLevel` enum has SCHEMA, DOMAIN, TEMPLATE, FILESYSTEM, GIT values
3. ✅ `ValidationIssue` model has level, severity, message, suggestion fields
4. ✅ `ValidationResult` model has valid bool, issues list, errors() method, warnings() method
5. ✅ `validate_config()` checks framework/language compatibility
6. ✅ `validate_config()` checks framework/architecture compatibility
7. ✅ `validate_config()` checks template existence
8. ✅ `validate_entity()` validates entity name is valid identifier
9. ✅ `validate_entity()` validates no duplicate field names
10. ✅ `validate_entity()` validates field types are appropriate for language
11. ✅ `validate_pre_scaffold()` runs DOMAIN, TEMPLATE, FILESYSTEM, GIT validations
12. ✅ `validate_pre_scaffold()` checks output directory write permissions
13. ✅ `validate_pre_scaffold()` detects .tac_config.yaml conflicts
14. ✅ `validate_pre_scaffold()` checks git availability and status
15. ✅ All validation issues include actionable suggestions
16. ✅ Service accumulates ALL errors before returning (no early exit)
17. ✅ Service distinguishes between errors (block) and warnings (inform)
18. ✅ Service never raises exceptions, always returns ValidationResult
19. ✅ All validation commands pass with zero regressions

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Auto-Resolved Clarifications Summary

The following design decisions were pre-resolved in the command args:

1. **Pydantic Schema Layer**: Let Pydantic errors propagate naturally. ValidationService focuses on domain, template, filesystem, and git validations only. Schema validation is implicit.

2. **Framework/Language Compatibility**: Use hardcoded matrix as class constant. Start simple, can externalize later. Based on PLAN_TAC_BOOTSTRAP.md examples.

3. **Framework/Architecture Compatibility**: Hardcoded dict as class constant. FastAPI supports DDD/Clean/Layered/Hexagonal, Express supports MVC/Clean/Layered.

4. **TemplateRepository Access**: Inject as constructor dependency following DDD/DI pattern. Makes service testable and decoupled.

5. **Filesystem Conflicts**: Check for .tac_config.yaml presence as primary conflict indicator. Simpler than checking every potential file.

6. **Git Availability**: Check with `shutil.which('git')` first, then repo status if available. Missing git is warning, not error (graceful degradation).

7. **Entity Validation**: Check entity name is valid Python/TS identifier, fields non-empty, field types valid for language, no duplicate field names.

8. **Pre-Scaffold Scope**: Run DOMAIN, TEMPLATE, FILESYSTEM, GIT validations. SCHEMA already done by Pydantic at config load.

9. **Suggestions Content**: Provide actionable fixes - suggest valid combinations for mismatches, check template path for missing templates, use --force for conflicts.

10. **Exception Handling**: Always return ValidationResult, never raise exceptions. Allows collecting all errors in one pass.

11. **Commands Validation**: No specific validation for commands section initially. Treat as freeform strings for template rendering.

12. **Parent Directory Permissions**: If output_dir doesn't exist, validate parent exists and is writable. Prevents cryptic errors during scaffold.

### Implementation Notes

- The service is designed to be non-invasive - it performs read-only checks without modifying any state
- Compatibility matrices should be kept in sync with helper functions in models.py
- Future enhancement: externalize matrices to YAML/JSON config for easier customization
- Git validation is intentionally lenient (warnings only) to support non-git workflows
- Template validation should check both .j2 template files and their expected output paths
- Consider adding a `--strict` mode in future that treats warnings as errors

### Integration Points

While this task creates a standalone service, future integration will involve:
- Calling `validate_pre_scaffold()` from CLI before `ScaffoldService.apply_plan()`
- Calling `validate_entity()` from entity generation command before template rendering
- Displaying validation results in Rich formatted tables for better UX
- Adding `--skip-validation` flag for advanced users who want to bypass checks
