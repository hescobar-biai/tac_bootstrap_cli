# Chore: Tests para templates de base classes

## Metadata
issue_number: `137`
adw_id: `feature_1.12`
issue_json: `{"number":137,"title":"Tarea 1.12: Tests para templates de base classes","body":"/chore\n/adw_sdlc_iso\n/adw_id feature_1.12\n\n***Tipo**: chore\n**Ganancia**: Garantia de que los templates renderizan correctamente y no se rompen en futuras modificaciones.\n\n**Instrucciones para el agente**:\n\n1. Crear `tac_bootstrap_cli/tests/test_base_classes_templates.py`\n2. Tests requeridos:\n   - `test_base_entity_renders` - Template renderiza Python valido\n   - `test_base_schema_renders` - Template renderiza con BaseCreate/Update/Response\n   - `test_base_service_renders` - Template renderiza con generics\n   - `test_base_repository_renders` - Template renderiza con Session\n   - `test_base_repository_async_renders` - Template renderiza con AsyncSession\n   - `test_database_renders_sync` - Template renderiza modo sync\n   - `test_database_renders_async` - Template renderiza modo async\n   - `test_exceptions_renders` - Template renderiza con exception handlers\n   - `test_responses_renders` - Template renderiza con PaginatedResponse\n   - `test_health_renders` - Template renderiza con endpoint\n   - `test_shared_included_for_ddd` - ScaffoldService incluye shared para DDD\n   - `test_shared_excluded_for_simple` - ScaffoldService NO incluye shared para simple\n3. Cada test debe:\n   - Crear un TACConfig con valores apropiados\n   - Renderizar el template con TemplateRepository\n   - Verificar que el output contiene las clases/funciones esperadas\n   - Verificar que es Python valido (compile() no falla)\n\n**Criterios de aceptacion**:\n- `uv run pytest tests/test_base_classes_templates.py` pasa al 100%\n- Coverage de los nuevos templates >90%"}`

## Chore Description
Esta chore crea una suite completa de tests unitarios para validar que los 10 templates de base classes en `tac_bootstrap_cli/tac_bootstrap/templates/shared/` renderizan correctamente y generan código Python válido. Los tests verificarán que los templates contienen las clases, funciones y estructuras esperadas según el tipo de proyecto (DDD vs simple, sync vs async).

Los tests actuarán como documentación ejecutable de los templates y garantizarán que futuras modificaciones no rompan la generación de código.

## Relevant Files
Archivos existentes para referencia:

- `tac_bootstrap_cli/tests/test_template_repo.py` - Tests existentes de TemplateRepository, sirven como referencia para patrones de testing de templates
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests de ScaffoldService, muestran cómo validar que templates se incluyen/excluyen según arquitectura
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository con método `render()` para renderizar templates
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Modelos Pydantic (TACConfig, ProjectSpec, etc.) usados como contexto para templates
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - ScaffoldService que decide qué templates incluir según arquitectura

Templates a testear (en `tac_bootstrap_cli/tac_bootstrap/templates/shared/`):
- `base_entity.py.j2` - Clase base para entidades DDD
- `base_schema.py.j2` - Clases base para schemas Pydantic (BaseCreate, BaseUpdate, BaseResponse)
- `base_service.py.j2` - Clase base para servicios con generics
- `base_repository.py.j2` - Repositorio base síncrono con SQLAlchemy Session
- `base_repository_async.py.j2` - Repositorio base asíncrono con AsyncSession
- `database.py.j2` - Configuración de database (sync y async)
- `exceptions.py.j2` - Excepciones personalizadas y exception handlers
- `responses.py.j2` - PaginatedResponse y helpers
- `dependencies.py.j2` - FastAPI dependencies
- `health.py.j2` - Endpoint /health

### New Files
- `tac_bootstrap_cli/tests/test_base_classes_templates.py` - Suite completa de tests para templates de base classes

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear fixture de configuración para tests
- Crear `tac_bootstrap_cli/tests/test_base_classes_templates.py`
- Importar dependencias necesarias:
  - `pytest`
  - `TACConfig, ProjectSpec, CommandsSpec, ClaudeConfig, ClaudeSettings` de `tac_bootstrap.domain.models`
  - `Language, PackageManager, Framework, Architecture` de `tac_bootstrap.domain.models`
  - `TemplateRepository` de `tac_bootstrap.infrastructure.template_repo`
  - `ScaffoldService` de `tac_bootstrap.application.scaffold_service`
- Crear fixtures:
  - `@pytest.fixture ddd_config()` - TACConfig con architecture=DDD, framework=FASTAPI
  - `@pytest.fixture simple_config()` - TACConfig con architecture=SIMPLE, framework=NONE
  - `@pytest.fixture async_config()` - TACConfig con database async habilitado
  - `@pytest.fixture repo()` - TemplateRepository con default templates dir

### Task 2: Tests para base_entity.py.j2
- Crear clase `TestBaseEntityTemplate`
- `test_base_entity_renders(repo, ddd_config)`:
  - Renderizar template `shared/base_entity.py.j2` con ddd_config
  - Verificar que output contiene `class BaseEntity`
  - Verificar que output contiene `id: UUID`
  - Verificar que output contiene `created_at` y `updated_at`
  - Verificar que es Python válido: `compile(output, '<string>', 'exec')` no falla
- `test_base_entity_has_domain_events(repo, ddd_config)`:
  - Verificar que output contiene `_domain_events` o similar
  - Verificar que tiene métodos para agregar/limpiar eventos

### Task 3: Tests para base_schema.py.j2
- Crear clase `TestBaseSchemaTemplate`
- `test_base_schema_renders(repo, ddd_config)`:
  - Renderizar template `shared/base_schema.py.j2`
  - Verificar que output contiene `class BaseCreate`
  - Verificar que output contiene `class BaseUpdate`
  - Verificar que output contiene `class BaseResponse`
  - Verificar que BaseResponse tiene `id: UUID`, `created_at`, `updated_at`
  - Compilar para validar Python válido

### Task 4: Tests para base_service.py.j2
- Crear clase `TestBaseServiceTemplate`
- `test_base_service_renders(repo, ddd_config)`:
  - Renderizar template `shared/base_service.py.j2`
  - Verificar que output contiene `class BaseService`
  - Verificar que usa generics: `Generic[TEntity, TCreate, TUpdate]` o similar
  - Verificar que tiene métodos CRUD: `create`, `get_by_id`, `list`, `update`, `delete`
  - Compilar para validar

### Task 5: Tests para base_repository.py.j2 (sync)
- Crear clase `TestBaseRepositoryTemplate`
- `test_base_repository_renders(repo, ddd_config)`:
  - Renderizar template `shared/base_repository.py.j2`
  - Verificar que output contiene `class BaseRepository`
  - Verificar que usa `Session` de SQLAlchemy (no AsyncSession)
  - Verificar que tiene métodos: `add`, `get`, `list`, `update`, `delete`
  - Compilar para validar

### Task 6: Tests para base_repository_async.py.j2
- Crear clase `TestBaseRepositoryAsyncTemplate`
- `test_base_repository_async_renders(repo, async_config)`:
  - Renderizar template `shared/base_repository_async.py.j2`
  - Verificar que output contiene `class BaseRepositoryAsync` o `BaseAsyncRepository`
  - Verificar que usa `AsyncSession`
  - Verificar que métodos son `async def`
  - Compilar para validar

### Task 7: Tests para database.py.j2
- Crear clase `TestDatabaseTemplate`
- `test_database_renders_sync(repo, ddd_config)`:
  - Configurar ddd_config sin async
  - Renderizar template `shared/database.py.j2`
  - Verificar que output contiene `create_engine` (sync)
  - Verificar que output contiene `sessionmaker` o `Session`
  - Compilar para validar
- `test_database_renders_async(repo, async_config)`:
  - Renderizar template con async_config
  - Verificar que output contiene `create_async_engine`
  - Verificar que output contiene `AsyncSession` o `async_sessionmaker`
  - Compilar para validar

### Task 8: Tests para exceptions.py.j2
- Crear clase `TestExceptionsTemplate`
- `test_exceptions_renders(repo, ddd_config)`:
  - Renderizar template `shared/exceptions.py.j2`
  - Verificar que output contiene excepciones personalizadas: `NotFoundException`, `ValidationException`, etc.
  - Verificar que contiene exception handlers para FastAPI si framework=FASTAPI
  - Compilar para validar

### Task 9: Tests para responses.py.j2
- Crear clase `TestResponsesTemplate`
- `test_responses_renders(repo, ddd_config)`:
  - Renderizar template `shared/responses.py.j2`
  - Verificar que output contiene `class PaginatedResponse` o `PaginatedList`
  - Verificar que tiene campos: `items`, `total`, `page`, `page_size`
  - Verificar que usa `Generic[T]` para tipado
  - Compilar para validar

### Task 10: Tests para health.py.j2
- Crear clase `TestHealthTemplate`
- `test_health_renders(repo, ddd_config)`:
  - Renderizar template `shared/health.py.j2`
  - Verificar que output contiene endpoint `/health` o router health
  - Verificar que usa FastAPI imports si framework=FASTAPI
  - Verificar que retorna status OK
  - Compilar para validar

### Task 11: Tests de integración con ScaffoldService
- Crear clase `TestScaffoldServiceSharedTemplates`
- `test_shared_included_for_ddd(ddd_config)`:
  - Crear ScaffoldService
  - Ejecutar `service.build_plan(ddd_config)`
  - Verificar que plan.files incluye templates de shared/:
    - `src/shared/domain/base_entity.py`
    - `src/shared/domain/base_schema.py`
    - `src/shared/application/base_service.py`
    - `src/shared/infrastructure/base_repository.py`
- `test_shared_excluded_for_simple(simple_config)`:
  - Ejecutar `service.build_plan(simple_config)` con architecture=SIMPLE
  - Verificar que plan.files NO incluye templates de shared/ (o incluye versión simplificada)
  - Este comportamiento depende de la lógica de ScaffoldService, ajustar según implementación

### Task 12: Ejecutar y validar todos los tests
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py -v --tb=short`
- Verificar que todos los tests pasan
- Si algún test falla, corregir el test o el template según corresponda
- Ejecutar con coverage: `uv run pytest tests/test_base_classes_templates.py --cov=tac_bootstrap.templates --cov-report=term`
- Verificar que coverage de templates sea >90%

### Task 13: Ejecutar suite completa de tests y linting
- Ejecutar Validation Commands (ver sección siguiente)
- Asegurar cero regresiones en tests existentes

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_base_classes_templates.py -v --tb=short` - Tests nuevos de templates
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Suite completa
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Consideraciones de diseño
1. **Validación de sintaxis Python**: Usar `compile(output, '<string>', 'exec')` para verificar que el código generado es Python válido sin necesidad de importar dependencias externas (FastAPI, SQLAlchemy)
2. **Fixtures reutilizables**: Crear fixtures separadas para DDD, SIMPLE y ASYNC para facilitar tests parametrizados
3. **Tests de contenido vs compilación**: Cada test debe verificar TANTO el contenido esperado (clases, métodos) COMO la validez sintáctica
4. **Independencia de framework**: Los tests no deben instalar FastAPI/SQLAlchemy, solo verifican que el código renderizado es válido

### Patrones a seguir (extraídos de test_template_repo.py)
```python
# Patrón de test básico
def test_template_renders(repo, config):
    result = repo.render("shared/base_entity.py.j2", config)
    assert "class BaseEntity" in result
    compile(result, '<string>', 'exec')  # Validar sintaxis

# Patrón de test condicional
def test_database_async_conditional(repo, async_config):
    result = repo.render("shared/database.py.j2", async_config)
    if async_config.database.async_enabled:
        assert "AsyncSession" in result
    else:
        assert "Session" in result
```

### Referencia de arquitecturas
- **DDD (architecture=ddd)**: Debe incluir todos los templates de shared/
- **SIMPLE (architecture=simple)**: Puede excluir o simplificar templates de shared/
- La lógica exacta de inclusión/exclusión está en ScaffoldService.build_plan()

### Coverage target
- Objetivo: >90% de coverage en templates de shared/
- Esto garantiza que cada sección condicional de los templates Jinja2 se ejecuta al menos una vez
