# Feature: GenerateService - Entity Generation Orchestration

## Metadata
issue_number: `143`
adw_id: `feature_2_3`
issue_json: `{"number":143,"title":"Tarea 2.3: GenerateService","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_3\n\n**Tipo**: feature\n**Ganancia**: Servicio de aplicacion que orquesta la generacion de entidades. Recibe EntitySpec, valida precondiciones, genera plan de archivos, y los aplica al filesystem.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py`\n2. Clase `GenerateService`:\n   - Constructor: recibe `TemplateRepository` y `FileSystem`\n   - Metodo principal `generate_entity(entity: EntitySpec, project_root: Path, config: TACConfig, force: bool = False) -> GenerateResult`\n3. Logica de `generate_entity`:\n   ```\n   1. Validar que src/shared/ existe (base classes requeridas)\n   2. Determinar output_dir: project_root / config.paths.app_root / entity.capability\n   3. Crear estructura de directorios:\n      - {capability}/domain/\n      - {capability}/application/\n      - {capability}/infrastructure/\n      - {capability}/api/\n   4. Renderizar cada template con context = {\"entity\": entity, \"config\": config}\n   5. Escribir archivos:\n      - domain/{entity.snake_name}.py\n      - application/schemas.py\n      - application/service.py\n      - infrastructure/repository.py\n      - infrastructure/models.py\n      - api/routes.py\n   6. Crear __init__.py en cada directorio\n   7. Retornar GenerateResult con lista de archivos creados\n   ```\n4. Definir `GenerateResult`:\n   ```python\n   class GenerateResult(BaseModel):\n       entity_name: str\n       capability: str\n       files_created: list[str]\n       directory: str\n   ```\n5. Si `force=False` y los archivos ya existen, raise error\n\n**Criterios de aceptacion**:\n- Genera estructura completa de vertical slice\n- Falla si base classes no existen\n- Falla si archivos existen y force=False\n- Retorna lista completa de archivos creados\n# FASE 2: Comando `generate entity`\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Feature Description

This feature implements the GenerateService, a core application service that orchestrates the generation of CRUD entities following the vertical slice architecture pattern. The service validates preconditions, renders entity templates, manages filesystem operations, and ensures safe, idempotent entity generation with comprehensive error handling.

**Value**: Enables developers to generate complete vertical slices (domain, application, infrastructure, API layers) for new entities with a single service call, dramatically reducing boilerplate and ensuring architectural consistency across the codebase.

## User Story

As a developer using TAC Bootstrap
I want to generate a complete CRUD entity with all layers (domain, schemas, service, repository, routes)
So that I can quickly scaffold new features following vertical slice architecture without manual boilerplate

## Problem Statement

Creating a new CRUD entity in a DDD/vertical slice architecture requires:
1. Creating directory structure for 4 layers (domain, application, infrastructure, api)
2. Writing 6+ files with proper imports and base class inheritance
3. Ensuring naming conventions are consistent (snake_case, PascalCase)
4. Wiring up dependencies between layers
5. Adding __init__.py files for Python packages

This is repetitive, error-prone, and time-consuming. A single typo can break imports. Developers need an automated service that handles the orchestration, validation, and safe generation of entities.

## Solution Statement

Implement GenerateService as the application layer orchestrator for entity generation. The service will:

1. **Validate First**: Check EntitySpec format and verify base classes exist before any filesystem writes
2. **All-or-Nothing**: Fail fast if ANY target file exists (when force=False) to prevent partial/corrupted state
3. **Generate Safely**: Use validation-first approach with custom exception hierarchy for clear error handling
4. **Create Structure**: Generate complete vertical slice with all layers and __init__.py files
5. **Return Metadata**: Provide GenerateResult with full list of created files for downstream processing

The service will use a strict validation-first approach with no rollback logic (fail fast), keep logic pure (no logging - that's CLI layer), and create app_root if missing (user-friendly mkdir -p behavior).

## Relevant Files

### Files to Create

- **tac_bootstrap_cli/tac_bootstrap/application/generate_service.py** (NEW)
  - Main implementation: GenerateService class with generate_entity() method
  - Custom exception classes: ValidationError, PreconditionError, FileSystemError
  - GenerateResult Pydantic model

### Files to Reference

- **tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py** (template_repo.py:153-369)
  - TemplateRepository for rendering Jinja2 templates
  - Methods: render(), template_exists(), list_templates()

- **tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py** (fs.py:24-223)
  - FileSystem for safe, idempotent filesystem operations
  - Methods: ensure_directory(), write_file(), file_exists()

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** (models.py:1-668)
  - TACConfig model with paths.app_root configuration
  - PathsSpec with app_root field

### Files to Test

- **tac_bootstrap_cli/tests/test_generate_service.py** (NEW)
  - Unit tests for all validation scenarios
  - Tests for happy path, edge cases, error conditions

### New Files

- **tac_bootstrap_cli/tac_bootstrap/application/generate_service.py** (service implementation)

## Implementation Plan

### Phase 1: Foundation - Models and Exceptions

Define the core models and custom exceptions that the service will use.

**Tasks:**
1. Create generate_service.py with module docstring
2. Import dependencies (Path, BaseModel, TACConfig, TemplateRepository, FileSystem)
3. Define custom exception hierarchy (ValidationError, PreconditionError, FileSystemError)
4. Define GenerateResult Pydantic model with fields (entity_name, capability, files_created, directory)
5. Add docstrings explaining each exception type and when it's raised

### Phase 2: Core Implementation - GenerateService Class

Implement the GenerateService class with constructor and main orchestration method.

**Tasks:**
1. Define GenerateService class with docstring
2. Implement __init__ accepting TemplateRepository and FileSystem
3. Create method signature for generate_entity(entity: EntitySpec, project_root: Path, config: TACConfig, force: bool = False) -> GenerateResult
4. Add comprehensive docstring documenting parameters, return value, exceptions raised
5. Implement validation-first approach skeleton

### Phase 3: Validation Logic

Implement strict validation before any filesystem operations.

**Tasks:**
1. Add _validate_entity_spec() private method
2. Validate entity name is valid Python identifier
3. Validate capability is valid package name (lowercase, alphanumeric + underscore, starts with letter, max 50 chars)
4. Validate required EntitySpec fields are non-empty
5. Add _check_base_classes() private method
6. Check for specific base class files: base_entity.py, base_repository.py, base_schema.py, base_service.py
7. Raise PreconditionError if any base class is missing
8. Add _check_existing_files() private method with all-or-nothing logic
9. Raise FileExistsError if ANY target file exists when force=False

### Phase 4: Directory and File Generation

Implement the core generation logic after validation passes.

**Tasks:**
1. Determine output_dir: project_root / config.paths.app_root / entity.capability
2. Create app_root directory if it doesn't exist (mkdir -p behavior)
3. Create vertical slice directory structure (domain/, application/, infrastructure/, api/)
4. Implement _render_templates() private method
5. Define template mapping: domain/{entity.snake_name}.py, application/schemas.py, application/service.py, infrastructure/repository.py, infrastructure/models.py, api/routes.py
6. Render each template with context = {"entity": entity, "config": config}
7. Implement _write_files() private method
8. Write rendered content to filesystem using FileSystem.write_file()
9. Create empty __init__.py files in each directory using FileSystem.write_file()
10. Collect list of created file paths (relative to project_root)

### Phase 5: Result Assembly and Error Handling

Complete the service with result assembly and error handling.

**Tasks:**
1. Construct GenerateResult with entity_name, capability, files_created, directory
2. Add comprehensive error handling for template rendering failures (TemplateRenderError)
3. Add comprehensive error handling for filesystem I/O failures (FileSystemError)
4. Ensure no logging or events in service (keep it pure business logic)
5. Add inline comments explaining key decisions
6. Review code for edge cases and defensive programming

## Step by Step Tasks

### Task 1: Create Module Structure and Imports
- Create file tac_bootstrap_cli/tac_bootstrap/application/generate_service.py
- Add module docstring explaining the service's purpose
- Import required types: Path from pathlib, BaseModel from pydantic
- Import TACConfig from tac_bootstrap.domain.models
- Import TemplateRepository from tac_bootstrap.infrastructure.template_repo
- Import FileSystem from tac_bootstrap.infrastructure.fs
- Import re for validation regex patterns

### Task 2: Define Custom Exceptions
- Create ValidationError exception class inheriting from Exception
- Add docstring: "Raised when EntitySpec validation fails"
- Create PreconditionError exception class inheriting from Exception
- Add docstring: "Raised when required preconditions are not met (e.g., missing base classes)"
- Create FileSystemError exception class inheriting from Exception
- Add docstring: "Raised when filesystem operations fail"
- Note: Reuse built-in FileExistsError for existing files scenario

### Task 3: Define GenerateResult Model
- Create GenerateResult class inheriting from BaseModel
- Add field: entity_name: str with description
- Add field: capability: str with description
- Add field: files_created: List[str] with description (relative paths)
- Add field: directory: str with description (absolute path to generated capability)
- Add docstring: "Result of entity generation operation"

### Task 4: Create GenerateService Class
- Define GenerateService class
- Add class docstring explaining orchestration role
- Implement __init__(self, template_repo: TemplateRepository, fs: FileSystem)
- Store template_repo and fs as instance variables
- Add docstring for constructor

### Task 5: Implement generate_entity Method Signature
- Define generate_entity(self, entity: EntitySpec, project_root: Path, config: TACConfig, force: bool = False) -> GenerateResult
- Add comprehensive docstring:
  - Parameters explanation (entity, project_root, config, force)
  - Return value explanation (GenerateResult)
  - Raises section (ValidationError, PreconditionError, FileExistsError, FileSystemError)
  - Example usage in docstring

### Task 6: Implement EntitySpec Validation
- Create private method _validate_entity_spec(self, entity: EntitySpec) -> None
- Validate entity.name is valid Python identifier using str.isidentifier()
- Validate entity.capability matches pattern: ^[a-z][a-z0-9_]{0,49}$ (lowercase, alphanumeric + underscore, starts with letter, max 50 chars)
- Validate entity.name is non-empty
- Validate entity.capability is non-empty
- Raise ValidationError with descriptive message for each validation failure
- Add docstring explaining validation rules

### Task 7: Implement Base Classes Check
- Create private method _check_base_classes(self, project_root: Path, config: TACConfig) -> None
- Determine shared_dir = project_root / config.paths.app_root / "shared"
- Check for existence of base_entity.py in shared_dir / "domain"
- Check for existence of base_repository.py in shared_dir / "infrastructure"
- Check for existence of base_schema.py in shared_dir / "domain"
- Check for existence of base_service.py in shared_dir / "application"
- If ANY base class file is missing, raise PreconditionError with list of missing files
- Use FileSystem.file_exists() for checks
- Add docstring explaining precondition

### Task 8: Implement Existing Files Check
- Create private method _check_existing_files(self, output_dir: Path, entity: EntitySpec, force: bool) -> None
- If force=True, return early (no check needed)
- Build list of target file paths:
  - output_dir / "domain" / f"{entity.snake_name}.py"
  - output_dir / "application" / "schemas.py"
  - output_dir / "application" / "service.py"
  - output_dir / "infrastructure" / "repository.py"
  - output_dir / "infrastructure" / "models.py"
  - output_dir / "api" / "routes.py"
- Check if ANY file exists using FileSystem.file_exists()
- If ANY file exists, raise FileExistsError with list of existing files and suggestion to use force=True
- Add docstring explaining all-or-nothing approach

### Task 9: Implement Directory Structure Creation
- In generate_entity(), after validation passes:
- Determine output_dir = project_root / config.paths.app_root / entity.capability
- Create app_root if it doesn't exist: FileSystem.ensure_directory(project_root / config.paths.app_root)
- Create capability directory: FileSystem.ensure_directory(output_dir)
- Create subdirectories: domain/, application/, infrastructure/, api/
- Use FileSystem.ensure_directory() for each subdirectory

### Task 10: Implement Template Rendering
- Create private method _render_templates(self, entity: EntitySpec, config: TACConfig) -> Dict[str, str]
- Define template mapping dictionary:
  - "domain/{snake_name}.py": "entity/domain.py.j2"
  - "application/schemas.py": "entity/schemas.py.j2"
  - "application/service.py": "entity/service.py.j2"
  - "infrastructure/repository.py": "entity/repository.py.j2"
  - "infrastructure/models.py": "entity/models.py.j2"
  - "api/routes.py": "entity/routes.py.j2"
- Create template context: {"entity": entity, "config": config}
- For each template, render using TemplateRepository.render()
- Replace {snake_name} in output path with entity.snake_name
- Return dictionary mapping output paths to rendered content
- Add error handling for template rendering failures (catch TemplateRenderError, wrap in FileSystemError)
- Add docstring

### Task 11: Implement File Writing
- Create private method _write_files(self, output_dir: Path, rendered_templates: Dict[str, str]) -> List[str]
- Initialize files_created list
- For each output_path, content in rendered_templates:
  - Construct full_path = output_dir / output_path
  - Write content using FileSystem.write_file(full_path, content)
  - Append relative path (str(full_path.relative_to(project_root))) to files_created
- Create empty __init__.py files in domain/, application/, infrastructure/, api/ subdirectories
- Use FileSystem.write_file(output_dir / subdir / "__init__.py", "")
- Append __init__.py paths to files_created
- Return files_created list
- Add error handling for I/O failures (catch exceptions, wrap in FileSystemError)
- Add docstring

### Task 12: Complete generate_entity Orchestration
- In generate_entity(), call _validate_entity_spec(entity)
- Call _check_base_classes(project_root, config)
- Determine output_dir
- Call _check_existing_files(output_dir, entity, force)
- Create directory structure (domain/, application/, infrastructure/, api/)
- Call _render_templates(entity, config)
- Call _write_files(output_dir, rendered_templates)
- Construct GenerateResult with:
  - entity_name=entity.name
  - capability=entity.capability
  - files_created=files_created (relative paths)
  - directory=str(output_dir)
- Return GenerateResult

### Task 13: Run Validation Commands
- Execute: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Execute: `cd tac_bootstrap_cli && uv run ruff check .`
- Execute: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Execute: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify all commands pass with zero errors

## Testing Strategy

### Unit Tests

All tests in tac_bootstrap_cli/tests/test_generate_service.py:

1. **test_generate_entity_success**: Happy path with valid EntitySpec, base classes exist, no existing files
2. **test_generate_entity_invalid_entity_name**: Raises ValidationError for invalid Python identifier (starts with number, contains spaces)
3. **test_generate_entity_invalid_capability_name**: Raises ValidationError for invalid package name (uppercase, starts with number, special chars)
4. **test_generate_entity_missing_base_classes**: Raises PreconditionError when base_entity.py or other base classes missing
5. **test_generate_entity_files_exist_no_force**: Raises FileExistsError when ANY target file exists and force=False
6. **test_generate_entity_files_exist_with_force**: Succeeds and overwrites when force=True
7. **test_generate_entity_creates_app_root**: Creates app_root directory if it doesn't exist
8. **test_generate_entity_creates_init_files**: Verifies __init__.py files are created in all subdirectories
9. **test_generate_entity_renders_templates**: Verifies templates are rendered with correct context
10. **test_generate_entity_returns_correct_result**: Verifies GenerateResult contains accurate metadata

### Edge Cases

1. **Empty EntitySpec fields**: Validates non-empty constraints
2. **Capability name edge cases**: Max length (50 chars), starts with letter, underscore positions
3. **Partial existing files**: ALL files must not exist (all-or-nothing)
4. **Template rendering failure**: Handles TemplateRenderError gracefully
5. **Filesystem I/O failure**: Handles write permission errors
6. **Missing app_root parent**: Creates parent directories as needed

## Acceptance Criteria

- GenerateService class exists in tac_bootstrap_cli/tac_bootstrap/application/generate_service.py
- GenerateResult Pydantic model with entity_name, capability, files_created, directory fields
- Custom exceptions: ValidationError, PreconditionError, FileSystemError
- generate_entity() method validates EntitySpec (name is Python identifier, capability is valid package name)
- generate_entity() checks for base classes (base_entity.py, base_repository.py, base_schema.py, base_service.py)
- generate_entity() raises FileExistsError if ANY file exists when force=False (all-or-nothing)
- generate_entity() creates vertical slice structure (domain/, application/, infrastructure/, api/)
- generate_entity() renders 6 templates with context = {"entity": entity, "config": config}
- generate_entity() writes 6 files + 4 __init__.py files
- generate_entity() creates app_root directory if missing (mkdir -p behavior)
- generate_entity() returns GenerateResult with complete list of created files
- Service has no logging (pure business logic)
- All unit tests pass
- Code passes ruff, mypy checks

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- This is the orchestration service for FASE 2 (Comando `generate entity`)
- EntitySpec model will be defined in a separate task (2.1 or 2.2)
- Entity templates (domain.py.j2, schemas.py.j2, etc.) will be created in separate tasks
- This service provides the foundation for the CLI command that will be added later
- Service is designed to be testable in isolation with mocked dependencies
- No rollback logic: fail fast and let partial directories remain (users can clean up or re-run with force=True)
- Validation-first approach prevents most failure scenarios before any filesystem writes
- Force flag enables overwriting for iterative development workflows
