# Chore: Tests for generate entity command

## Metadata
issue_number: `152`
adw_id: `feature_2_7`
issue_json: `{"number":152,"title":"Tarea 2.7: Tests para generate entity","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_7\n\n**Tipo**: chore\n**Ganancia**: Cobertura de tests para el nuevo comando y servicio de generacion.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tests/test_generate_service.py`\n2. Crear `tac_bootstrap_cli/tests/test_entity_config.py`\n3. Tests para EntitySpec:\n   - Validacion de PascalCase\n   - Validacion de campos prohibidos\n   - Properties (snake_name, plural_name, table_name)\n   - Serializacion JSON\n4. Tests para GenerateService:\n   - Genera estructura completa\n   - Falla sin base classes\n   - Falla con archivos existentes (sin force)\n   - Funciona con force=True\n   - Genera authorized cuando flag activo\n5. Tests para CLI:\n   - Comando con --fields parseado correctamente\n   - Dry-run no crea archivos\n   - Error cuando no hay config.yml\n\n**Criterios de aceptacion**:\n- `uv run pytest tests/test_generate_service.py tests/test_entity_config.py` pasa\n- Coverage >90% para generate_service y entity_config\n\n# FASE 2: Comando `generate entity`\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Chore Description

Create comprehensive test suite for the `generate entity` command, covering:
- **EntitySpec validation** (PascalCase, prohibited fields, derived properties)
- **GenerateService file generation** (5-file vertical slice, base class dependencies, force overwrite, authorized multi-tenant variant)
- **CLI parsing** (--fields format, dry-run, config.yml requirement)

The tests already exist for `test_entity_config.py` and `test_cli_generate.py`, but we need to create `test_generate_service.py` and verify/enhance existing tests to achieve >90% coverage.

## Relevant Files

### Existing Files to Test
- `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py` - EntitySpec, FieldSpec models with validators
- `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py` - GenerateService orchestration logic
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI generate command

### Existing Test Files
- `tac_bootstrap_cli/tests/test_entity_config.py` - Comprehensive tests for EntitySpec/FieldSpec (ALREADY EXISTS - appears complete)
- `tac_bootstrap_cli/tests/test_cli_generate.py` - Tests for CLI generate command (ALREADY EXISTS - appears complete)

### New Files
- `tac_bootstrap_cli/tests/test_generate_service.py` - NEW FILE - Tests for GenerateService (MISSING)

### Dependencies
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - FileSystem abstraction (used by GenerateService)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository (used by GenerateService)

## Step by Step Tasks

### Task 1: Analyze existing test coverage
- Read `test_entity_config.py` and verify it covers all EntitySpec validation requirements
- Read `test_cli_generate.py` and verify it covers CLI parsing requirements
- Identify gaps in test coverage based on the issue requirements

### Task 2: Create test_generate_service.py
- Create `tac_bootstrap_cli/tests/test_generate_service.py` with comprehensive tests
- Use pytest fixtures for:
  - Temporary project directory with config.yml (similar to `test_entity_generator_service.py`)
  - Mock FileSystem and TemplateRepository dependencies
- Cover test scenarios:
  - **Happy path**: Generate complete 5-file vertical slice (domain, schemas, service, repository, models, routes)
  - **Precondition failure**: Missing base classes (BaseModel, BaseSchema, BaseService, BaseRepository)
  - **File conflict**: Existing files without force=False raises FileExistsError
  - **Force overwrite**: force=True successfully overwrites existing files
  - **Authorized variant**: authorized=True includes tenant_id field and FilterByTenant dependency
  - **Validation errors**: Invalid EntitySpec (empty name, invalid capability format)
  - **Template rendering errors**: Template not found or rendering fails
  - **Filesystem errors**: I/O errors during file write

### Task 3: Verify existing test coverage
- Run pytest with coverage for `test_entity_config.py`:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py --cov=tac_bootstrap.domain.entity_config --cov-report=term-missing
  ```
- Verify coverage is >90% for entity_config.py
- If gaps exist, add missing test cases

### Task 4: Run all tests and verify coverage
- Run pytest for all three test files:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_cli_generate.py tests/test_generate_service.py -v --tb=short
  ```
- Run coverage analysis:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_generate_service.py --cov=tac_bootstrap.domain.entity_config --cov=tac_bootstrap.application.generate_service --cov-report=term-missing
  ```
- Verify >90% coverage for both `entity_config.py` and `generate_service.py`

### Task 5: Execute validation commands
- Run full test suite:
  ```bash
  cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
  ```
- Run linting:
  ```bash
  cd tac_bootstrap_cli && uv run ruff check .
  ```
- Run smoke test:
  ```bash
  cd tac_bootstrap_cli && uv run tac-bootstrap --help
  ```

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All tests pass
- `cd tac_bootstrap_cli && uv run pytest tests/test_entity_config.py tests/test_generate_service.py --cov=tac_bootstrap.domain.entity_config --cov=tac_bootstrap.application.generate_service --cov-report=term-missing` - Coverage >90%
- `cd tac_bootstrap_cli && uv run ruff check .` - No linting errors
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test passes

## Notes

### Key Testing Strategies

1. **Use tmp_path fixture** for filesystem isolation (pytest built-in fixture)
2. **Mock dependencies** (FileSystem, TemplateRepository) for unit testing GenerateService
3. **Test validation-first approach** - GenerateService validates before any filesystem writes
4. **Test all-or-nothing file generation** - Either all files created or none (no partial state)
5. **Test error messages** - Verify helpful error messages for validation failures

### Coverage Targets

- `entity_config.py`: >90% (likely already achieved by existing `test_entity_config.py`)
- `generate_service.py`: >90% (new tests in `test_generate_service.py`)
- `cli.py generate command`: Covered by existing `test_cli_generate.py`

### Test Data Patterns

Use realistic entity specs in tests:
```python
EntitySpec(
    name="Product",
    capability="catalog",
    fields=[
        FieldSpec(name="title", field_type=FieldType.STRING, max_length=200, required=True),
        FieldSpec(name="price", field_type=FieldType.DECIMAL, required=True),
        FieldSpec(name="description", field_type=FieldType.TEXT, required=False)
    ],
    authorized=True,
    async_mode=True
)
```

### Important: Existing Tests Status

Based on file reading:
- ✅ `test_entity_config.py` EXISTS and appears COMPLETE (762 lines, comprehensive coverage)
- ✅ `test_cli_generate.py` EXISTS and appears COMPLETE (500 lines, covers all CLI scenarios)
- ❌ `test_generate_service.py` MISSING - This is the primary file to create

The chore primarily involves creating the missing `test_generate_service.py` file and verifying coverage meets >90% threshold.
