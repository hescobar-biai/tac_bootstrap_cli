# Feature: CLI Command `generate entity` for CRUD Entity Generation

## Metadata
issue_number: `146`
adw_id: `feature_2_4`
issue_json: `{"number":146,"title":"Tarea 2.4: Comando CLI generate","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_4\n\n**Tipo**: feature\n**Ganancia**: Los usuarios pueden generar entidades desde la terminal con un solo comando, con opcion interactiva para definir campos.\n\n**Instrucciones para el agente**:\n\n1. Modificar tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py\n2. Agregar subcomando generate con subcomando entity:\n   ```python\n   @app.command()\n   def generate(\n       subcommand: str,  # \"entity\"\n       name: str,  # PascalCase entity name\n       capability: Annotated[str, Option(\"--capability\", \"-c\")] = None,\n       fields: Annotated[str, Option(\"--fields\", \"-f\")] = None,\n       authorized: Annotated[bool, Option(\"--authorized\")] = False,\n       async_mode: Annotated[bool, Option(\"--async\")] = False,\n       with_events: Annotated[bool, Option(\"--with-events\")] = False,\n       interactive: Annotated[bool, Option(\"--interactive/--no-interactive\")] = True,\n       dry_run: Annotated[bool, Option(\"--dry-run\")] = False,\n       force: Annotated[bool, Option(\"--force\")] = False,\n   ):\n   ```\n3. Si --fields no se proporciona y --interactive, lanzar wizard para definir campos\n4. Formato de --fields para modo no-interactivo:\n   ```\n   --fields \"name:str:required,price:float:required,description:text,is_available:bool\"\n   ```\n5. Si --capability no se proporciona, usar el nombre de la entidad en kebab-case\n6. Output con Rich:\n   - Panel verde con resumen de lo generado\n   - Lista de archivos creados\n   - Instrucciones de siguiente paso (registrar router en main.py)\n\n**Criterios de aceptacion**:\n- tac-bootstrap generate entity Product -c catalog --no-interactive --fields \"name:str:required,price:float\" funciona\n- tac-bootstrap generate entity Product lanza wizard interactivo\n- --dry-run muestra lo que se crearia sin crear nada\n- Muestra error claro si no hay config.yml o si architecture!=ddd\n\n# FASE 2: Comando generate entity\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Feature Description
Implement a new CLI command `tac-bootstrap generate entity` that generates complete CRUD vertical slices for entities in DDD architecture projects. The command supports both interactive mode (wizard-based field definition) and non-interactive mode (CLI argument-based). It generates domain models, Pydantic schemas, service layer, repository layer, and API routes based on the entity specification.

The feature validates project configuration, entity naming conventions, and field definitions, then uses Jinja2 templates to generate consistent, production-ready code that follows best practices for FastAPI + SQLAlchemy projects with DDD architecture.

## User Story
As a developer using TAC Bootstrap for a DDD/FastAPI project
I want to run `tac-bootstrap generate entity Product` in my terminal
So that I can instantly scaffold a complete CRUD vertical slice (domain model, schemas, service, repository, API routes) without manually writing boilerplate code, ensuring consistency and following established patterns

## Problem Statement
Creating a new entity in a DDD architecture with FastAPI requires significant boilerplate across multiple layers:
1. Domain model with validation and business logic
2. Pydantic schemas for request/response DTOs
3. Service layer with CRUD operations
4. Repository layer for database access
5. API routes with proper HTTP methods and responses

Developers currently need to:
- Manually create files in multiple directories
- Copy/paste boilerplate from existing entities
- Adapt naming conventions across 5+ files
- Remember field definitions across all layers
- Ensure consistency between domain and API schemas

This manual process is error-prone, time-consuming, and inconsistent. A single command that generates all layers following established patterns would eliminate this friction and ensure code quality.

## Solution Statement
Implement a `generate` CLI command with an `entity` subcommand that:
1. Validates the project has architecture=ddd in config.yml
2. Collects entity specification via interactive wizard OR CLI arguments
3. Generates complete vertical slice using Jinja2 templates:
   - Domain entity model
   - Pydantic schemas (Create, Update, Response)
   - Service layer with CRUD operations
   - Repository layer (sync or async based on --async flag)
   - API routes with proper HTTP methods
   - Domain events (if --with-events flag is used)
4. Supports advanced flags for customization (--authorized, --async, --with-events)
5. Provides clear next-steps guidance (register router, run migrations, etc.)
6. Offers dry-run mode to preview generated files without creating them

The solution uses existing EntitySpec domain model for validation and leverages the template infrastructure already in place for consistent code generation.

## Relevant Files
Existing files to understand:

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Main CLI entry point, where generate command will be added
- `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` - EntitySpec, FieldSpec, FieldType models for validation
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig for project configuration
- `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py` - Existing wizard patterns for interactive mode
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering engine
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - File system operations
- `config.yml` - Project configuration file to validate architecture
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2` - Base entity reference for understanding patterns

### New Files
Files to be created for this feature:

**Application Layer:**
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py` - Service that orchestrates entity generation
  - Validates project configuration (config.yml exists, architecture=ddd)
  - Checks for conflicts (entity files already exist)
  - Builds generation plan with all files to create
  - Applies plan to filesystem using FileSystem operations
  - Returns generation result with created files list

**Interface Layer:**
- `tac_bootstrap_cli/tac_bootstrap/interfaces/entity_wizard.py` - Interactive wizard for entity definition
  - Wizard for field definition (name, type, required flag)
  - Loop-based: add fields until user says 'no' to "Add another field?"
  - Validates field names and types in real-time
  - Returns complete EntitySpec

**Templates:**
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/entity.py.j2` - Domain entity model template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/schemas.py.j2` - Pydantic schemas template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/service.py.j2` - Service layer template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/repository.py.j2` - Repository template (sync)
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/repository_async.py.j2` - Repository template (async)
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/routes.py.j2` - API routes template
- `tac_bootstrap_cli/tac_bootstrap/templates/entity/events.py.j2` - Domain events template (conditional)

**Tests:**
- `tac_bootstrap_cli/tests/test_entity_generator_service.py` - Tests for EntityGeneratorService
- `tac_bootstrap_cli/tests/test_entity_wizard.py` - Tests for entity wizard
- `tac_bootstrap_cli/tests/test_cli_generate.py` - Integration tests for generate command

## Implementation Plan

### Phase 1: Foundation
Create the entity generation service and wizard infrastructure before implementing the CLI command.

**Tasks:**
1. Create EntityGeneratorService in application layer
   - Implement validation: config.yml exists, load TACConfig, verify architecture=ddd
   - Implement conflict detection: check if entity files already exist
   - Implement plan building: determine which files to create based on flags
   - Implement plan application: use FileSystem to create directories and render templates
   - Return ApplyResult-like structure with files created count

2. Create entity field wizard in interfaces layer
   - Implement run_entity_field_wizard() function
   - Loop-based flow: prompt field name, type, required flag
   - Show supported types: str, int, float, bool, datetime, UUID, text
   - Validate field names against Python keywords and SQLAlchemy conflicts
   - Ask "Add another field?" until user says no
   - Return list of FieldSpec objects

### Phase 2: Core Implementation
Create the templates and implement the CLI command.

**Tasks:**
1. Create entity Jinja2 templates in templates/entity/
   - entity.py.j2: Domain model inheriting from BaseEntity with custom fields
   - schemas.py.j2: XCreate, XUpdate, XResponse schemas with proper field mappings
   - service.py.j2: Service class inheriting from BaseService with entity-specific logic
   - repository.py.j2: Sync repository inheriting from BaseRepository
   - repository_async.py.j2: Async repository inheriting from BaseRepositoryAsync
   - routes.py.j2: FastAPI router with CRUD endpoints (GET, POST, PUT, DELETE, LIST)
   - events.py.j2: Domain events (XCreated, XUpdated, XDeleted) if with_events=True

2. Implement generate command in cli.py
   - Add @app.command() for generate with all specified parameters
   - Validate subcommand == "entity" (show error with usage example if invalid)
   - Parse --fields string if provided: "name:type:required,name:type"
   - Convert PascalCase entity name to kebab-case capability if not provided
   - Call wizard if interactive mode and no --fields provided
   - Build EntitySpec from collected input
   - Call EntityGeneratorService to generate files
   - Handle --dry-run: show preview without creating files
   - Handle --force: allow overwriting existing files
   - Show Rich panel with success summary and next steps

### Phase 3: Integration
Add tests, documentation, and polish the feature.

**Tasks:**
1. Write comprehensive unit tests
   - Test EntityGeneratorService validation (missing config, wrong architecture)
   - Test conflict detection (entity already exists)
   - Test plan building with different flags (async, events, authorized)
   - Test wizard field collection
   - Test CLI command with various argument combinations
   - Test --dry-run mode (no files created)
   - Test --force mode (overwrite existing files)

2. Update documentation
   - Add generate command to CLI help text in main() callback
   - Update README.md with generate entity examples
   - Add usage examples to command docstring

3. Integration validation
   - Run full test suite to ensure no regressions
   - Test generate command on real project (manual smoke test)
   - Verify generated entity compiles (Python syntax check)
   - Verify next-steps instructions are accurate

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create EntityGeneratorService foundation
- Create `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py`
- Implement `__init__(self, template_repo, filesystem)` with dependency injection
- Implement `validate_project(self, target_dir: Path) -> TACConfig`
  - Check config.yml exists at target_dir / "config.yml"
  - Load YAML and parse to TACConfig
  - Validate architecture in [ddd, clean, hexagonal]
  - Raise clear error if validation fails
- Implement `check_conflicts(self, target_dir: Path, entity_spec: EntitySpec, force: bool) -> None`
  - Check if domain/{capability}/entities/{entity_name}.py exists
  - If exists and not force, raise error with clear message
  - Validate entity name not in Python keywords
- Implement `build_generation_plan(self, entity_spec: EntitySpec, config: TACConfig) -> List[FileOperation]`
  - Return list of files to create with paths and template names
  - Include: entity.py, schemas.py, service.py, repository.py (or repository_async.py), routes.py
  - Conditionally include events.py if with_events=True
- Implement `generate(self, entity_spec: EntitySpec, target_dir: Path, dry_run: bool, force: bool) -> GenerationResult`
  - Call validate_project, check_conflicts, build_generation_plan
  - If dry_run, return result with plan but don't create files
  - Otherwise, create directories and render templates using filesystem
  - Return GenerationResult with files_created list and success status

### Task 2: Create entity field wizard
- Create `tac_bootstrap_cli/tac_bootstrap/interfaces/entity_wizard.py`
- Import Rich components (Prompt, Confirm, Console)
- Define SUPPORTED_TYPES constant: ["str", "int", "float", "bool", "datetime", "UUID", "text"]
- Implement `run_entity_field_wizard() -> List[FieldSpec]`
  - Show welcome message: "Define entity fields (type 'done' to finish)"
  - Loop:
    - Prompt for field name (validate snake_case pattern)
    - Show numbered list of types and prompt for selection
    - Prompt for required flag (Y/n, default=Y)
    - Create FieldSpec and add to list
    - Ask "Add another field? (Y/n)" (default=Y)
    - Break loop if user says no
  - Validate at least one field was added
  - Return list of FieldSpec objects
- Handle Ctrl+C gracefully with try/except KeyboardInterrupt

### Task 3: Create entity templates (domain + schemas)
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/entity/`
- Create `entity.py.j2`:
  - Import BaseEntity from shared.domain.base_entity
  - Define {EntityName} class inheriting from BaseEntity
  - Add custom fields from entity_spec.fields
  - Map FieldType to SQLAlchemy Column types (String, Integer, Float, Boolean, DateTime, UUID, Text)
  - Add __tablename__ = "{{ entity_spec.table_name }}"
  - Include docstring with entity description
- Create `schemas.py.j2`:
  - Import BaseCreate, BaseUpdate, BaseResponse from shared.domain.base_schema
  - Define {EntityName}Create inheriting from BaseCreate with custom fields
  - Define {EntityName}Update inheriting from BaseUpdate with Optional custom fields
  - Define {EntityName}Response inheriting from BaseResponse with all fields
  - Use proper type hints: str, int, float, bool, datetime, UUID for fields

### Task 4: Create entity templates (service + repository)
- Create `repository.py.j2` (sync version):
  - Import BaseRepository from shared.infrastructure.base_repository
  - Import {EntityName} entity model
  - Define {EntityName}Repository(BaseRepository[{EntityName}])
  - Pass {EntityName} to __init__ superclass
- Create `repository_async.py.j2` (async version):
  - Import BaseRepositoryAsync from shared.infrastructure.base_repository_async
  - Import {EntityName} entity model
  - Define {EntityName}Repository(BaseRepositoryAsync[{EntityName}])
  - Pass {EntityName} to __init__ superclass
- Create `service.py.j2`:
  - Import BaseService from shared.application.base_service
  - Import schemas ({EntityName}Create, {EntityName}Update, {EntityName}Response)
  - Import {EntityName} entity and {EntityName}Repository
  - Define {EntityName}Service(BaseService[...]) with proper generics
  - Pass repository to __init__ and call superclass

### Task 5: Create entity templates (routes + events)
- Create `routes.py.j2`:
  - Import FastAPI (APIRouter, Depends, HTTPException)
  - Import schemas and service
  - Create router = APIRouter(prefix="/{{ entity_spec.plural_name }}", tags=["{{ entity_spec.plural_name }}"])
  - Define endpoints:
    - POST / -> create_{entity} (returns {EntityName}Response, status=201)
    - GET /{id} -> get_{entity} (returns {EntityName}Response)
    - GET / -> list_{entities} (returns PaginatedResponse[{EntityName}Response])
    - PUT /{id} -> update_{entity} (returns {EntityName}Response)
    - DELETE /{id} -> delete_{entity} (returns SuccessResponse)
  - Add @requires_auth decorator to create/update/delete if authorized=True
  - Use async def if async_mode=True
- Create `events.py.j2` (conditional template):
  - Define {EntityName}Created, {EntityName}Updated, {EntityName}Deleted event classes
  - Each inherits from BaseEvent (if exists) or simple dataclass
  - Include entity_id, timestamp, and entity snapshot data

### Task 6: Implement generate CLI command
- Modify `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- Add generate command with signature from issue requirements:
  ```python
  @app.command()
  def generate(
      subcommand: str,
      name: str,
      capability: Annotated[str, Option("--capability", "-c")] = None,
      fields: Annotated[str, Option("--fields", "-f")] = None,
      authorized: Annotated[bool, Option("--authorized")] = False,
      async_mode: Annotated[bool, Option("--async")] = False,
      with_events: Annotated[bool, Option("--with-events")] = False,
      interactive: Annotated[bool, Option("--interactive/--no-interactive")] = True,
      dry_run: Annotated[bool, Option("--dry-run")] = False,
      force: Annotated[bool, Option("--force")] = False,
  ) -> None:
  ```
- Validate subcommand == "entity" (raise typer.Exit(1) with error if not)
- Auto-generate capability from name if not provided (PascalCase -> kebab-case using regex)
- Parse --fields string if provided: split by comma, then split by colon (name:type:required)
- Call wizard if interactive and no --fields: fields_list = run_entity_field_wizard()
- Build EntitySpec from collected data
- Call EntityGeneratorService.generate()
- If dry_run, show preview Panel with list of files that would be created
- Otherwise show success Panel with:
  - Green border
  - List of created files
  - Next steps: 1) Register router in main.py, 2) Run migrations if DB, 3) Import events if --with-events
- Handle all exceptions with clear error messages

### Task 7: Write EntityGeneratorService tests
- Create `tac_bootstrap_cli/tests/test_entity_generator_service.py`
- Test validate_project():
  - Test missing config.yml -> raises error
  - Test invalid YAML -> raises error
  - Test architecture != ddd -> raises error
  - Test valid config -> returns TACConfig
- Test check_conflicts():
  - Test entity already exists, force=False -> raises error
  - Test entity already exists, force=True -> no error
  - Test entity name is Python keyword -> raises error
  - Test new entity -> no error
- Test build_generation_plan():
  - Test with async_mode=False -> includes repository.py
  - Test with async_mode=True -> includes repository_async.py
  - Test with with_events=False -> excludes events.py
  - Test with with_events=True -> includes events.py
  - Test all plans include: entity.py, schemas.py, service.py, routes.py
- Test generate() end-to-end:
  - Test dry_run=True -> no files created, returns plan
  - Test dry_run=False -> files created, success=True
  - Test force=True -> overwrites existing files

### Task 8: Write wizard and CLI tests
- Create `tac_bootstrap_cli/tests/test_entity_wizard.py`
- Mock Rich Prompt, Confirm components
- Test run_entity_field_wizard():
  - Test adding single field -> returns [FieldSpec]
  - Test adding multiple fields -> returns list
  - Test user cancels (Ctrl+C) -> raises SystemExit or returns empty
  - Test invalid field name -> re-prompts
  - Test invalid type selection -> re-prompts
- Create `tac_bootstrap_cli/tests/test_cli_generate.py`
- Use CliRunner to test generate command
- Test non-interactive mode:
  - Test with all args provided -> success
  - Test with --fields parsing -> creates entity
  - Test missing config.yml -> error message
  - Test wrong architecture -> error message
- Test interactive mode:
  - Mock wizard to return FieldSpec list
  - Test success flow
- Test --dry-run:
  - Test no files created
  - Test preview shown in output
- Test invalid subcommand:
  - Test "tac-bootstrap generate foo" -> error
- Test auto-capability generation:
  - Test "ProductCategory" -> "product-category"

### Task 9: Update documentation and run validation
- Update `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`:
  - Add "generate" to Available Commands in welcome panel
- Update docstring of generate command with examples:
  - Interactive: `tac-bootstrap generate entity Product`
  - Non-interactive: `tac-bootstrap generate entity Product -c catalog --no-interactive --fields "name:str:required,price:float"`
  - Dry-run: `tac-bootstrap generate entity Product --dry-run`
- Run all validation commands (see Validation Commands section)
- Fix any test failures or linting issues
- Perform manual smoke test:
  - Create test project with architecture=ddd
  - Run `tac-bootstrap generate entity Product -c catalog --fields "name:str:required,price:float" --dry-run`
  - Verify preview shows correct files
  - Run without --dry-run
  - Verify files are created
  - Verify generated Python code compiles (python -m py_compile)

## Testing Strategy

### Unit Tests

**EntityGeneratorService Tests:**
- validate_project() with various config scenarios
- check_conflicts() with existing/new entities
- build_generation_plan() with all flag combinations
- generate() dry-run vs real execution

**Entity Wizard Tests:**
- Field collection loop (1 field, multiple fields)
- Field validation (invalid names, types)
- User cancellation handling
- Type selection from numbered list

**CLI Command Tests:**
- Argument parsing (fields string, capability auto-generation)
- Subcommand validation ("entity" vs invalid)
- Interactive vs non-interactive mode
- Error handling (missing config, wrong architecture)
- Dry-run vs real execution
- Force mode (overwrite existing)

### Integration Tests
- Full workflow: CLI command -> EntityGeneratorService -> Template rendering -> Files created
- Verify generated code compiles (syntax validation)
- Verify all expected files exist after generation
- Verify --dry-run creates no files
- Verify --force overwrites existing files

### Edge Cases
- Entity name with numbers: "OAuth2Client" -> "o_auth2_client"
- Empty fields string: --fields "" -> error
- Malformed fields string: --fields "name:str:invalid" -> error
- Field name conflicts: field named "id" -> error (reserved)
- Field name is Python keyword: field named "class" -> error
- Missing config.yml -> clear error message
- Architecture=simple -> clear error message
- Capability with invalid characters -> error
- Entity already exists, no --force -> error
- Very long entity name -> handles gracefully
- Special characters in entity name -> validation error

## Acceptance Criteria
1. **Non-interactive mode with fields works:**
   - Command: `tac-bootstrap generate entity Product -c catalog --no-interactive --fields "name:str:required,price:float"`
   - Creates all 5 files: entity.py, schemas.py, service.py, repository.py, routes.py
   - Files compile without syntax errors
   - Shows success panel with files created list

2. **Interactive mode launches wizard:**
   - Command: `tac-bootstrap generate entity Product`
   - Prompts for capability (suggests "product")
   - Launches field wizard
   - Collects fields interactively
   - Generates entity after wizard completion

3. **Dry-run shows preview without creating files:**
   - Command: `tac-bootstrap generate entity Product --dry-run`
   - Shows preview panel with list of files that would be created
   - Shows file paths relative to project root
   - Does NOT create any files or directories
   - Exit code 0

4. **Clear error messages for invalid configurations:**
   - Missing config.yml: "Error: No config.yml found. Run this command from a TAC Bootstrap project root."
   - Wrong architecture: "Error: Entity generation requires architecture=ddd in config.yml. Current architecture: simple"
   - Entity exists: "Error: Entity 'Product' already exists at domain/catalog/entities/product.py. Use --force to overwrite."
   - Invalid subcommand: "Error: Unknown subcommand 'foo'. Use 'entity'. Example: tac-bootstrap generate entity Product"

5. **Auto-capability generation works:**
   - "Product" -> "product"
   - "ProductCategory" -> "product-category"
   - "OAuth2Client" -> "o-auth2-client"

6. **Flags work correctly:**
   - `--async`: Generates repository_async.py instead of repository.py
   - `--with-events`: Creates events.py with 3 event classes
   - `--authorized`: Adds @requires_auth to create/update/delete endpoints
   - `--force`: Overwrites existing files without error

7. **Next steps guidance is shown:**
   - Success panel includes: "Next Steps:"
   - Step 1: Register router in main.py
   - Step 2 (if DB detected): Run database migrations
   - Step 3 (if --with-events): Import and register events

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run pytest tests/test_entity_generator_service.py -v` - Entity generator tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_entity_wizard.py -v` - Wizard tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_cli_generate.py -v` - CLI generate tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test (verify generate command appears)
- `cd tac_bootstrap_cli && uv run tac-bootstrap generate entity --help` - Command help text

## Notes

**Design Decisions:**
1. **Subcommand parameter**: Using positional `subcommand: str` instead of nested Typer apps for simplicity. Hardcode validation to "entity" for Phase 2.4. Future phases can add "service", "repo", etc. without refactoring.

2. **Field type mapping**: Phase 2.4 supports basic types (str, int, float, bool, datetime, UUID, text). Advanced types (Decimal, Enum, relationships) are out of scope. Users can manually edit generated files for advanced needs.

3. **Template location**: Templates go in `templates/entity/` separate from `templates/shared/` because entity templates are for generation, not scaffolding shared infrastructure.

4. **Wizard simplicity**: Phase 2.4 wizard only collects name, type, required flag. Advanced features (validators, defaults, relationships, descriptions) are future enhancements.

5. **Capability auto-generation**: Using regex to convert PascalCase to kebab-case. Pattern: `re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()`. Simple and handles most cases correctly.

6. **Conflict detection**: Only check domain entity file existence. If entity exists, assume all related files exist. Prevents partial overwrites which would be inconsistent.

7. **Authorization pattern**: Assumes `@requires_auth` decorator exists or will be imported from common auth module. Users adapt to their auth system.

8. **Events pattern**: Domain events are dataclasses with entity_id, timestamp, and snapshot. Simple pattern suitable for event sourcing or message bus integration.

**Future Enhancements (not in scope for Phase 2.4):**
- Generate database migration files (Alembic)
- Support for relationships (foreign keys, many-to-many)
- Support for validators and defaults in wizard
- Generate test files for entity
- Support for other architectures (simple, hexagonal)
- Support for other frameworks (Django, Flask)
- Entity spec YAML files for reusable definitions
- Bulk generation from spec file

**Dependencies:**
- No new dependencies required
- Uses existing: Typer, Rich, Pydantic, Jinja2, pathlib
- Reuses existing infrastructure: TemplateRepository, FileSystem, EntitySpec

**Risk Mitigation:**
- Comprehensive unit tests for all components
- Dry-run mode for safe preview
- Clear error messages for validation failures
- Force flag requires explicit opt-in for overwrites
- Generated code is syntax-validated in tests
