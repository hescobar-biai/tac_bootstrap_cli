# PLAN: TAC Bootstrap v0.3 - Version Robusta

## Objetivo

Evolucionar `tac_bootstrap_cli` de un generador de estructura agentic a una herramienta completa que tambien genera codigo de aplicacion (entidades CRUD con DDD), documentacion fractal automatica, y validacion multi-capa. Basado en los patrones documentados en `ai_docs/doc/create-crud-entity/`.

## Estructura del Plan

- **7 Fases**, **3 Iteraciones** de ejecucion
- Cada tarea tiene: tipo (feature/chore/bug), descripcion, ganancia, instrucciones, criterios de aceptacion
- Fases 1-5 (codigo) y Fases 6-7 (docs fractal) son independientes

## REGLA CRITICA: Dual Creation Pattern

**IMPORTANTE**: Este proyecto es TANTO el generador como un proyecto de referencia. Por lo tanto, cada tarea que cree un template DEBE crear DOS archivos:

1. **Template Jinja2** en `tac_bootstrap_cli/tac_bootstrap/templates/` → usado por el CLI para generar en OTROS proyectos
2. **Archivo renderizado** en la raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/`) → para que ESTE proyecto tambien lo tenga

### Mapeo de rutas (template → archivo en raiz):

| Template (tac_bootstrap_cli/tac_bootstrap/templates/) | Archivo en raiz (/Volumes/MAc1/Celes/tac_bootstrap/) |
|---|---|
| `shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |
| `shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |
| `shared/base_service.py.j2` | `src/shared/application/base_service.py` |
| `shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |
| `shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |
| `shared/database.py.j2` | `src/shared/infrastructure/database.py` |
| `shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |
| `shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |
| `shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |
| `shared/health.py.j2` | `src/shared/api/health.py` |
| `capabilities/crud_basic/domain_entity.py.j2` | *(se genera bajo demanda con `generate entity`)* |
| `capabilities/crud_basic/schemas.py.j2` | *(se genera bajo demanda)* |
| `capabilities/crud_basic/service.py.j2` | *(se genera bajo demanda)* |
| `capabilities/crud_basic/repository.py.j2` | *(se genera bajo demanda)* |
| `capabilities/crud_basic/routes.py.j2` | *(se genera bajo demanda)* |
| `capabilities/crud_basic/orm_model.py.j2` | *(se genera bajo demanda)* |
| `scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |
| `scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |
| `scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |
| `claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |
| `config/canonical_idk.yml.j2` | `canonical_idk.yml` |

### Excepcion: Templates de capabilities (crud_basic, crud_authorized)
Los templates de `capabilities/` NO se renderizan automaticamente en la raiz. Solo se generan cuando el usuario ejecuta `tac-bootstrap generate entity <name>`. Por eso no tienen archivo en raiz.

### Como implementar la dual creation:
1. Crear el template `.j2` con variables Jinja2
2. Renderizar el template con los valores del proyecto actual (tac_bootstrap)
3. Guardar el resultado en la ruta correspondiente de la raiz
4. Verificar que AMBOS archivos existen y son consistentes

---

# FASE 1: Templates de Base Classes

**Objetivo**: Generar infraestructura compartida (base classes DDD) en proyectos FastAPI con arquitectura ddd/clean/hexagonal.

**Ganancia de la fase**: Los proyectos generados tendran una base solida de clases reutilizables que eliminan ~80% del boilerplate en cada nueva entidad CRUD.

---

## Tarea 1.1: Template base_entity.py

**Tipo**: feature
**Ganancia**: Todas las entidades del proyecto heredan de una clase base con audit trail, soft delete, state management y versionado optimista. Evita repetir 50+ lineas por entidad.

**Instrucciones para el agente**:

1. Crear el template Jinja2: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2`
2. Crear el archivo renderizado en raiz: `src/shared/domain/base_entity.py` (renderizado con valores de este proyecto)
3. El archivo en raiz debe ser el resultado de renderizar el template con `config.project.name = "tac_bootstrap"`
2. El template debe generar una clase `Entity` con los siguientes campos:
   - `id: str` (UUID generado automaticamente)
   - `state: int` (0=inactive, 1=active, 2=deleted, default=1)
   - `version: int` (para optimistic locking, default=1)
   - `created_at: datetime` (auto-set en creacion)
   - `created_by: str | None`
   - `updated_at: datetime` (auto-set en cada update)
   - `updated_by: str | None`
   - `organization_id: str | None` (multi-tenancy opcional)
   - `type_discriminator: str` (para herencia de entidades)
3. Metodos requeridos:
   - `activate()` → state=1
   - `deactivate()` → state=0
   - `soft_delete()` → state=2
   - `restore()` → state=1
   - `is_active` → property bool
   - `is_deleted` → property bool
4. Usar Pydantic BaseModel como base
5. Variables Jinja2 disponibles: `{{ config.project.name }}`

**Criterios de aceptacion**:
- El archivo renderiza sin errores con un config basico
- La clase generada es importable sin errores de sintaxis
- Los metodos de estado transicionan correctamente
- Incluye docstring con patron IDK

---

## Tarea 1.2: Template base_schema.py

**Tipo**: feature
**Ganancia**: DTOs estandarizados (Create/Update/Response) que separan la capa API del dominio. Cada entidad nueva solo necesita heredar y agregar sus campos especificos.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_schema.py.j2`
2. Crear renderizado en raiz: `src/shared/domain/base_schema.py`
2. Definir 3 clases base Pydantic:
   - `BaseCreate`: campos comunes para creacion (ninguno por default, las entidades agregan los suyos)
   - `BaseUpdate`: todos los campos opcionales para partial updates
   - `BaseResponse`: campos de respuesta (id, state, version, created_at, updated_at, created_by, updated_by)
3. Configuracion `model_config = ConfigDict(from_attributes=True)` en BaseResponse
4. Agregar ejemplo en docstring de como heredar:
   ```python
   class ProductCreate(BaseCreate):
       name: str
       price: float
   ```

**Criterios de aceptacion**:
- BaseResponse puede instanciarse desde un ORM model (from_attributes=True)
- BaseUpdate tiene todos campos como Optional
- Renderiza sin errores

---

## Tarea 1.3: Template base_service.py

**Tipo**: feature
**Ganancia**: Servicio CRUD generico con generics tipados. Cada nueva entidad solo necesita `class ProductService(BaseService[ProductCreate, ProductUpdate, ProductResponse, ProductModel, Product])` para tener CRUD completo.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2`
2. Crear renderizado en raiz: `src/shared/application/base_service.py`
2. Definir `BaseService` con generics: `BaseService[TCreate, TUpdate, TResponse, TModel, TDomain]`
3. Metodos CRUD implementados:
   - `create(data: TCreate, user_id: str | None = None) -> TResponse`
   - `get_by_id(entity_id: str) -> TResponse` (raises 404 si no existe o state=2)
   - `get_all(page: int, page_size: int, filters: dict, sort_by: str, sort_order: str) -> PaginatedResponse[TResponse]`
   - `update(entity_id: str, data: TUpdate, user_id: str | None = None) -> TResponse`
   - `delete(entity_id: str, user_id: str | None = None) -> bool` (soft delete)
   - `hard_delete(entity_id: str) -> bool`
4. Cada metodo debe:
   - Excluir entidades con state=2 en queries
   - Setear audit fields (created_by, updated_by)
   - Incrementar version en updates
5. Recibe `repository` en constructor via dependency injection

**Criterios de aceptacion**:
- La clase es generica y tipada correctamente
- Soft delete seta state=2, no borra fisicamente
- get_all soporta paginacion, filtros y ordenamiento
- Raises HTTPException(404) cuando entidad no existe

---

## Tarea 1.4: Template base_repository.py

**Tipo**: feature
**Ganancia**: Repositorio generico que abstrae SQLAlchemy. Elimina queries repetitivas y garantiza que soft-deleted items no aparezcan por default.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/base_repository.py`
2. Definir `BaseRepository[TModel]` con SQLAlchemy Session
3. Metodos:
   - `get_by_id(entity_id: str) -> TModel | None` (excluye state=2)
   - `get_all(page, page_size, filters, sort_by, sort_order) -> tuple[list[TModel], int]`
   - `create(model: TModel) -> TModel`
   - `update(model: TModel) -> TModel`
   - `delete(entity_id: str) -> bool` (SET state=2)
   - `hard_delete(entity_id: str) -> bool` (DELETE fisico)
   - `exists(entity_id: str) -> bool`
   - `count(filters: dict) -> int`
4. Filtros dinamicos: recibe dict y aplica `==` por cada key/value
5. Ordenamiento: valida que sort_by es un campo del modelo

**Criterios de aceptacion**:
- Todas las queries excluyen state=2 por default
- Paginacion usa offset/limit correctamente
- Maneja session commit/rollback

---

## Tarea 1.5: Template base_repository_async.py

**Tipo**: feature
**Ganancia**: Version async del repositorio para proyectos que usen async SQLAlchemy (AsyncSession). Misma interfaz que sync pero con await.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository_async.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/base_repository_async.py`
2. Misma interfaz que base_repository.py pero con:
   - `AsyncSession` en lugar de `Session`
   - Todos los metodos son `async def`
   - Usa `await session.execute()` en lugar de `session.query()`
   - Usa `select()` statements (SQLAlchemy 2.0 style)
3. Agregar metodos adicionales async-friendly:
   - `bulk_create(models: list[TModel]) -> list[TModel]`
   - `bulk_update(models: list[TModel]) -> list[TModel]`

**Criterios de aceptacion**:
- Usa SQLAlchemy 2.0 async API
- Misma funcionalidad que sync repo
- bulk operations usan `session.add_all()`

---

## Tarea 1.6: Template database.py

**Tipo**: feature
**Ganancia**: Session management centralizado. Un solo lugar para configurar la conexion a BD, crear sesiones, y manejar el lifecycle.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/database.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/database.py`
2. Contenido:
   - `engine` = create_engine con URL desde config/env
   - `SessionLocal` = sessionmaker
   - `Base` = declarative_base()
   - `get_db()` generator para dependency injection en FastAPI
   - Soporte condicional para async:
     ```jinja2
     {% if config.project.async_mode | default(false) %}
     from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
     {% else %}
     from sqlalchemy import create_engine
     {% endif %}
     ```
3. Variable Jinja2: `{{ config.project.database_url | default("sqlite:///./app.db") }}`

**Criterios de aceptacion**:
- get_db() es un generator que cierra session en finally
- Soporta sqlite y postgresql via variable de entorno
- Base es exportable para que modelos hereden de ella

---

## Tarea 1.7: Template exceptions.py

**Tipo**: feature
**Ganancia**: Exceptions tipadas con HTTP handlers pre-registrados. Errores consistentes en toda la API sin repetir try/except en cada endpoint.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/exceptions.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/exceptions.py`
2. Clases de exception:
   - `EntityNotFoundError(entity_type: str, entity_id: str)` → 404
   - `DuplicateEntityError(entity_type: str, field: str, value: str)` → 409
   - `ValidationError(message: str, details: dict)` → 422
   - `UnauthorizedError(message: str)` → 401
   - `ForbiddenError(message: str)` → 403
   - `BusinessRuleError(message: str)` → 400
3. FastAPI exception handlers:
   - `register_exception_handlers(app: FastAPI)` que registra handler para cada exception
   - Cada handler retorna JSON con `{"error": {"type": "...", "message": "...", "details": {...}}}`

**Criterios de aceptacion**:
- Cada exception mapea a un HTTP status code especifico
- Los handlers retornan formato JSON consistente
- `register_exception_handlers()` se puede llamar en main.py

---

## Tarea 1.8: Template responses.py

**Tipo**: feature
**Ganancia**: Modelos de respuesta estandarizados. Todas las APIs retornan el mismo formato, facilitando integracion con frontends y documentacion OpenAPI.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/responses.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/responses.py`
2. Modelos Pydantic:
   - `PaginatedResponse[T]`:
     - `data: list[T]`
     - `total: int`
     - `page: int` (1-indexed)
     - `page_size: int` (1-100)
     - `pages: int` (total_pages calculado)
   - `SuccessResponse`:
     - `success: bool = True`
     - `message: str`
   - `ErrorResponse`:
     - `error: ErrorDetail`
   - `ErrorDetail`:
     - `type: str`
     - `message: str`
     - `details: dict | None`

**Criterios de aceptacion**:
- PaginatedResponse es generico (T)
- `pages` se calcula como ceil(total / page_size)
- page_size tiene validador: min=1, max=100

---

## Tarea 1.9: Template dependencies.py

**Tipo**: feature
**Ganancia**: Factory functions para dependency injection en FastAPI. Patron consistente para obtener servicios y repositorios en endpoints.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/dependencies.py.j2`
2. Crear renderizado en raiz: `src/shared/infrastructure/dependencies.py`
2. Contenido:
   - `get_db` reimportado de database.py (convenience)
   - Pattern para crear service factories:
     ```python
     def get_service(db: Session = Depends(get_db)):
         repository = Repository(db)
         return Service(repository)
     ```
   - Ejemplo comentado de como agregar auth dependency
3. El template debe ser extensible (los usuarios agregan sus propias factories)

**Criterios de aceptacion**:
- Patron Depends() de FastAPI usado correctamente
- Ejemplo funcional incluido en comentarios

---

## Tarea 1.10: Template health.py

**Tipo**: feature
**Ganancia**: Endpoint /health listo para monitoreo. Verifica conexion a BD y reporta version de la app.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/shared/health.py.j2`
2. Crear renderizado en raiz: `src/shared/api/health.py`
2. Contenido:
   - Router FastAPI con prefix="" o "/health"
   - `GET /health` retorna:
     ```json
     {
       "status": "healthy",
       "version": "{{ config.project.version | default('0.1.0') }}",
       "database": "connected" | "disconnected",
       "timestamp": "ISO8601"
     }
     ```
   - Intenta hacer `SELECT 1` a la BD para verificar conexion
   - Si falla la BD, retorna status "degraded" pero HTTP 200

**Criterios de aceptacion**:
- Endpoint responde en <100ms
- No expone informacion sensible
- Reporta estado de la BD

---

## Tarea 1.11: Integrar base classes en ScaffoldService

**Tipo**: feature
**Ganancia**: Al ejecutar `tac-bootstrap init` con `--architecture ddd` y `--framework fastapi`, el proyecto incluye automaticamente todas las base classes en `src/shared/`.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. En el metodo `build_plan()`, agregar logica condicional:
   ```python
   if config.project.architecture in [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]:
       if config.project.framework == Framework.FASTAPI:
           self._add_shared_infrastructure(plan, config)
   ```
3. Crear metodo `_add_shared_infrastructure(plan, config)` que agregue:
   - Directorio `src/shared/`
   - Directorio `src/shared/domain/`
   - Directorio `src/shared/infrastructure/`
   - Cada template de `templates/shared/*.py.j2` como FileOperation
4. Los archivos se generan en:
   - `src/shared/domain/base_entity.py`
   - `src/shared/domain/base_schema.py`
   - `src/shared/application/base_service.py`
   - `src/shared/infrastructure/base_repository.py`
   - `src/shared/infrastructure/base_repository_async.py`
   - `src/shared/infrastructure/database.py`
   - `src/shared/infrastructure/exceptions.py`
   - `src/shared/infrastructure/responses.py`
   - `src/shared/infrastructure/dependencies.py`
   - `src/shared/api/health.py`

5. **Dual creation**: Como parte de esta tarea, crear la estructura `src/shared/` completa en la raiz de este proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`) con los archivos renderizados de las tareas 1.1-1.10. Esto asegura que este proyecto sirve como referencia funcional.

**Criterios de aceptacion**:
- `tac-bootstrap init my-app -l python -f fastapi -a ddd --no-interactive` genera `src/shared/` con todos los archivos
- `tac-bootstrap init my-app -l python -f fastapi -a simple --no-interactive` NO genera `src/shared/`
- La raiz del proyecto (`/Volumes/MAc1/Celes/tac_bootstrap/src/shared/`) tiene todos los archivos renderizados
- Tests existentes siguen pasando
- Nuevo test verifica la inclusion condicional

---

## Tarea 1.12: Tests para templates de base classes

**Tipo**: chore
**Ganancia**: Garantia de que los templates renderizan correctamente y no se rompen en futuras modificaciones.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tests/test_base_classes_templates.py`
2. Tests requeridos:
   - `test_base_entity_renders` - Template renderiza Python valido
   - `test_base_schema_renders` - Template renderiza con BaseCreate/Update/Response
   - `test_base_service_renders` - Template renderiza con generics
   - `test_base_repository_renders` - Template renderiza con Session
   - `test_base_repository_async_renders` - Template renderiza con AsyncSession
   - `test_database_renders_sync` - Template renderiza modo sync
   - `test_database_renders_async` - Template renderiza modo async
   - `test_exceptions_renders` - Template renderiza con exception handlers
   - `test_responses_renders` - Template renderiza con PaginatedResponse
   - `test_health_renders` - Template renderiza con endpoint
   - `test_shared_included_for_ddd` - ScaffoldService incluye shared para DDD
   - `test_shared_excluded_for_simple` - ScaffoldService NO incluye shared para simple
3. Cada test debe:
   - Crear un TACConfig con valores apropiados
   - Renderizar el template con TemplateRepository
   - Verificar que el output contiene las clases/funciones esperadas
   - Verificar que es Python valido (compile() no falla)

**Criterios de aceptacion**:
- `uv run pytest tests/test_base_classes_templates.py` pasa al 100%
- Coverage de los nuevos templates >90%

---

# FASE 2: Comando `generate entity`

**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.

**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.

---

## Tarea 2.1: Modelo EntitySpec en domain

**Tipo**: feature
**Ganancia**: Modelo tipado que describe una entidad a generar: nombre, campos, tipos, relaciones. Sirve como contrato entre CLI, wizard y generador.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tac_bootstrap/domain/entity_config.py`
2. Definir modelos Pydantic:
   ```python
   class FieldType(str, Enum):
       STRING = "str"
       INTEGER = "int"
       FLOAT = "float"
       BOOLEAN = "bool"
       DATETIME = "datetime"
       UUID = "uuid"
       TEXT = "text"
       DECIMAL = "decimal"
       JSON = "json"

   class FieldSpec(BaseModel):
       name: str  # nombre del campo (snake_case)
       field_type: FieldType
       required: bool = True
       unique: bool = False
       indexed: bool = False
       default: Any = None
       description: str = ""
       max_length: int | None = None  # para strings

   class EntitySpec(BaseModel):
       name: str  # PascalCase (e.g., "Product")
       capability: str  # kebab-case (e.g., "catalog")
       fields: list[FieldSpec]
       authorized: bool = False  # generar con auth templates
       async_mode: bool = False  # usar async repository
       with_events: bool = False  # generar domain events

       @property
       def snake_name(self) -> str:
           """product"""
       @property
       def plural_name(self) -> str:
           """products"""
       @property
       def table_name(self) -> str:
           """products"""
   ```
3. Agregar validadores:
   - `name` debe ser PascalCase
   - `capability` debe ser kebab-case
   - `fields` no puede estar vacio
   - No se permiten campos con nombre `id`, `state`, `version`, `created_at`, `updated_at` (ya estan en BaseEntity)

**Criterios de aceptacion**:
- Validadores rechazan nombres invalidos con mensajes claros
- Properties generan nombres derivados correctamente
- Modelo es serializable a JSON/YAML

---

## Tarea 2.2: Templates CRUD basicos (capability)

**Tipo**: feature
**Ganancia**: Templates Jinja2 que generan una vertical slice completa. Cada archivo usa EntitySpec como contexto para generar codigo especifico a la entidad.

**Instrucciones para el agente**:

1. Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/`
2. Crear los siguientes templates:

**`domain_entity.py.j2`**:
- Importa Entity de shared
- Clase `{{ entity.name }}(Entity)`:
  - `type_discriminator = "{{ entity.snake_name }}"`
  - Un campo por cada FieldSpec
  - Metodos de negocio placeholder (validate, calculate)

**`schemas.py.j2`**:
- `{{ entity.name }}Create(BaseCreate)`: campos required
- `{{ entity.name }}Update(BaseUpdate)`: todos Optional
- `{{ entity.name }}Response(BaseResponse)`: todos los campos

**`service.py.j2`**:
- `{{ entity.name }}Service(BaseService[...])`:
  - Constructor con repository
  - Override de metodos si necesario
  - Metodos custom placeholder

**`repository.py.j2`**:
- `{{ entity.name }}Repository(BaseRepository[{{ entity.name }}Model])`:
  - Metodos custom de query (get_by_code, search, etc.)

**`orm_model.py.j2`**:
- Modelo SQLAlchemy `{{ entity.name }}Model(Base)`:
  - `__tablename__ = "{{ entity.table_name }}"`
  - Columnas mapeadas desde FieldSpec con tipos SQLAlchemy
  - Indexes en campos marcados como indexed

**`routes.py.j2`**:
- Router FastAPI:
  - `POST /{{ entity.plural_name }}/` → create (201)
  - `GET /{{ entity.plural_name }}/{id}` → get_by_id (200)
  - `GET /{{ entity.plural_name }}/` → get_all con paginacion (200)
  - `PUT /{{ entity.plural_name }}/{id}` → update (200)
  - `DELETE /{{ entity.plural_name }}/{id}` → soft_delete (200)

3. Variables Jinja2 disponibles: `{{ entity }}` (EntitySpec), `{{ config }}` (TACConfig)
4. Mapeo de FieldType a tipos SQLAlchemy:
   - str → String(max_length), int → Integer, float → Float
   - bool → Boolean, datetime → DateTime, uuid → String(36)
   - text → Text, decimal → Numeric, json → JSON

**Criterios de aceptacion**:
- Cada template renderiza Python valido con un EntitySpec de ejemplo
- Los imports entre archivos son correctos (domain importa de shared, service importa repo, etc.)
- Los tipos SQLAlchemy mapean correctamente desde FieldType

---

## Tarea 2.3: GenerateService

**Tipo**: feature
**Ganancia**: Servicio de aplicacion que orquesta la generacion de entidades. Recibe EntitySpec, valida precondiciones, genera plan de archivos, y los aplica al filesystem.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py`
2. Clase `GenerateService`:
   - Constructor: recibe `TemplateRepository` y `FileSystem`
   - Metodo principal `generate_entity(entity: EntitySpec, project_root: Path, config: TACConfig, force: bool = False) -> GenerateResult`
3. Logica de `generate_entity`:
   ```
   1. Validar que src/shared/ existe (base classes requeridas)
   2. Determinar output_dir: project_root / config.paths.app_root / entity.capability
   3. Crear estructura de directorios:
      - {capability}/domain/
      - {capability}/application/
      - {capability}/infrastructure/
      - {capability}/api/
   4. Renderizar cada template con context = {"entity": entity, "config": config}
   5. Escribir archivos:
      - domain/{entity.snake_name}.py
      - application/schemas.py
      - application/service.py
      - infrastructure/repository.py
      - infrastructure/models.py
      - api/routes.py
   6. Crear __init__.py en cada directorio
   7. Retornar GenerateResult con lista de archivos creados
   ```
4. Definir `GenerateResult`:
   ```python
   class GenerateResult(BaseModel):
       entity_name: str
       capability: str
       files_created: list[str]
       directory: str
   ```
5. Si `force=False` y los archivos ya existen, raise error

**Criterios de aceptacion**:
- Genera estructura completa de vertical slice
- Falla si base classes no existen
- Falla si archivos existen y force=False
- Retorna lista completa de archivos creados

---

## Tarea 2.4: Comando CLI `generate`

**Tipo**: feature
**Ganancia**: Los usuarios pueden generar entidades desde la terminal con un solo comando, con opcion interactiva para definir campos.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
2. Agregar subcomando `generate` con subcomando `entity`:
   ```python
   @app.command()
   def generate(
       subcommand: str,  # "entity"
       name: str,  # PascalCase entity name
       capability: Annotated[str, Option("--capability", "-c")] = None,
       fields: Annotated[str, Option("--fields", "-f")] = None,
       authorized: Annotated[bool, Option("--authorized")] = False,
       async_mode: Annotated[bool, Option("--async")] = False,
       with_events: Annotated[bool, Option("--with-events")] = False,
       interactive: Annotated[bool, Option("--interactive/--no-interactive")] = True,
       dry_run: Annotated[bool, Option("--dry-run")] = False,
       force: Annotated[bool, Option("--force")] = False,
   ):
   ```
3. Si `--fields` no se proporciona y `--interactive`, lanzar wizard para definir campos
4. Formato de `--fields` para modo no-interactivo:
   ```
   --fields "name:str:required,price:float:required,description:text,is_available:bool"
   ```
5. Si `--capability` no se proporciona, usar el nombre de la entidad en kebab-case
6. Output con Rich:
   - Panel verde con resumen de lo generado
   - Lista de archivos creados
   - Instrucciones de siguiente paso (registrar router en main.py)

**Criterios de aceptacion**:
- `tac-bootstrap generate entity Product -c catalog --no-interactive --fields "name:str:required,price:float"` funciona
- `tac-bootstrap generate entity Product` lanza wizard interactivo
- `--dry-run` muestra lo que se crearia sin crear nada
- Muestra error claro si no hay config.yml o si architecture!=ddd

---

## Tarea 2.5: Wizard interactivo para entity fields

**Tipo**: feature
**Ganancia**: Los usuarios pueden definir campos de la entidad de forma guiada, sin necesidad de memorizar la sintaxis de --fields.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`
2. Agregar funcion `run_entity_wizard() -> EntitySpec`:
   - Prompt para nombre de entidad (PascalCase)
   - Prompt para capability name (kebab-case, default = nombre en kebab)
   - Loop para agregar campos:
     - Nombre del campo (snake_case)
     - Tipo (seleccionar de FieldType enum)
     - Required? (y/n, default y)
     - Unique? (y/n, default n)
     - Indexed? (y/n, default n)
     - Max length? (solo para str, default None)
     - "Agregar otro campo?" (y/n)
   - Opciones adicionales:
     - Authorized templates? (y/n)
     - Async mode? (y/n)
     - Domain events? (y/n)
   - Mostrar resumen y confirmar
3. Usar Rich para formatear prompts y tabla de resumen

**Criterios de aceptacion**:
- Wizard guia al usuario paso a paso
- Muestra tabla resumen antes de confirmar
- Valida inputs en tiempo real (PascalCase, snake_case, etc.)
- Permite cancelar en cualquier momento

---

## Tarea 2.6: Templates CRUD authorized (opcional)

**Tipo**: feature
**Ganancia**: Variantes de los templates que incluyen verificacion de permisos a nivel de row (owner/organization). Para proyectos multi-tenant.

**Instrucciones para el agente**:

1. Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_authorized/`
2. Crear variantes de:
   - `routes_authorized.py.j2`: Endpoints que extraen user_id del token y lo pasan al service
   - `service_authorized.py.j2`: Service que filtra por owner/organization_id
   - `repository_authorized.py.j2`: Repository que agrega filtro de owner a todas las queries
3. Los templates authorized extienden los basicos agregando:
   - Dependency `get_current_user` en routes
   - Filtro `organization_id` en repository queries
   - Verificacion de ownership en update/delete

**Criterios de aceptacion**:
- `tac-bootstrap generate entity Product --authorized` genera con templates authorized
- Las queries filtran por organization_id del usuario autenticado
- DELETE solo permite al owner

---

## Tarea 2.7: Tests para generate entity

**Tipo**: chore
**Ganancia**: Cobertura de tests para el nuevo comando y servicio de generacion.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tests/test_generate_service.py`
2. Crear `tac_bootstrap_cli/tests/test_entity_config.py`
3. Tests para EntitySpec:
   - Validacion de PascalCase
   - Validacion de campos prohibidos
   - Properties (snake_name, plural_name, table_name)
   - Serializacion JSON
4. Tests para GenerateService:
   - Genera estructura completa
   - Falla sin base classes
   - Falla con archivos existentes (sin force)
   - Funciona con force=True
   - Genera authorized cuando flag activo
5. Tests para CLI:
   - Comando con --fields parseado correctamente
   - Dry-run no crea archivos
   - Error cuando no hay config.yml

**Criterios de aceptacion**:
- `uv run pytest tests/test_generate_service.py tests/test_entity_config.py` pasa
- Coverage >90% para generate_service y entity_config

---

# FASE 3: Audit Trail y Metadata

**Objetivo**: Registrar metadata de generacion en config.yml para trazabilidad.

**Ganancia de la fase**: Saber exactamente cuando se genero el proyecto, con que version del CLI, y cuando fue la ultima actualizacion. Util para upgrades y debugging.

---

## Tarea 3.1: Modelo BootstrapMetadata

**Tipo**: feature
**Ganancia**: Modelo tipado para la metadata de generacion. Previene datos inconsistentes en config.yml.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/domain/models.py`
2. Agregar modelo:
   ```python
   class BootstrapMetadata(BaseModel):
       generated_at: str  # ISO8601 timestamp
       generated_by: str  # "tac-bootstrap v{version}"
       last_upgrade: str | None = None  # ISO8601 timestamp
       schema_version: int = 2
       template_checksums: dict[str, str] = {}  # {template_name: md5}
   ```
3. Agregar campo `bootstrap: BootstrapMetadata | None = None` al modelo `TACConfig`

**Criterios de aceptacion**:
- TACConfig acepta seccion bootstrap opcional
- Timestamps son ISO8601 validos
- Modelo es serializable a YAML

---

## Tarea 3.2: Registrar metadata en scaffold

**Tipo**: feature
**Ganancia**: Cada vez que se genera o actualiza un proyecto, se registra automaticamente cuando y con que version se hizo.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. En `apply_plan()`, antes de escribir config.yml:
   ```python
   from datetime import datetime, timezone
   from tac_bootstrap import __version__

   config.bootstrap = BootstrapMetadata(
       generated_at=datetime.now(timezone.utc).isoformat(),
       generated_by=f"tac-bootstrap v{__version__}",
       schema_version=2,
   )
   ```
3. Modificar `templates/config/config.yml.j2` para incluir:
   ```yaml
   bootstrap:
     generated_at: "{{ config.bootstrap.generated_at }}"
     generated_by: "{{ config.bootstrap.generated_by }}"
     schema_version: {{ config.bootstrap.schema_version }}
   {% if config.bootstrap.last_upgrade %}
     last_upgrade: "{{ config.bootstrap.last_upgrade }}"
   {% endif %}
   ```

**Criterios de aceptacion**:
- `tac-bootstrap init` genera config.yml con seccion bootstrap
- Timestamps son UTC ISO8601
- `tac-bootstrap upgrade` actualiza last_upgrade

---

## Tarea 3.3: Tests para audit trail

**Tipo**: chore
**Ganancia**: Verificar que la metadata se registra correctamente en todos los flujos.

**Instrucciones para el agente**:

1. Agregar tests en `tac_bootstrap_cli/tests/test_scaffold_service.py`:
   - `test_init_generates_bootstrap_metadata` - config.yml tiene seccion bootstrap
   - `test_bootstrap_metadata_has_valid_timestamp` - ISO8601 parseable
   - `test_bootstrap_metadata_has_correct_version` - Coincide con __version__
   - `test_upgrade_updates_last_upgrade` - last_upgrade se actualiza

**Criterios de aceptacion**:
- Tests pasan
- Metadata presente en todos los flujos (init, upgrade)

---

# FASE 4: Multi-layer Validation

**Objetivo**: Validar en multiples capas antes de aplicar cambios al filesystem.

**Ganancia de la fase**: Errores detectados temprano con mensajes claros. Evita generar archivos parciales que luego fallan en runtime.

---

## Tarea 4.1: ValidationService

**Tipo**: feature
**Ganancia**: Servicio centralizado que ejecuta validaciones en orden y reporta todos los errores de una vez (no falla en el primero).

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py`
2. Definir:
   ```python
   class ValidationLevel(str, Enum):
       SCHEMA = "schema"
       DOMAIN = "domain"
       TEMPLATE = "template"
       FILESYSTEM = "filesystem"
       GIT = "git"

   class ValidationIssue(BaseModel):
       level: ValidationLevel
       severity: str  # "error", "warning"
       message: str
       suggestion: str | None = None

   class ValidationResult(BaseModel):
       valid: bool
       issues: list[ValidationIssue]
       def errors(self) -> list[ValidationIssue]
       def warnings(self) -> list[ValidationIssue]
   ```
3. Clase `ValidationService`:
   - `validate_config(config: TACConfig) -> ValidationResult`
   - `validate_entity(entity: EntitySpec, project_root: Path) -> ValidationResult`
   - `validate_pre_scaffold(config: TACConfig, output_dir: Path) -> ValidationResult`
4. Validaciones por capa:
   - **SCHEMA**: Pydantic ya lo hace (campos requeridos, tipos)
   - **DOMAIN**: framework compatible con language, architecture valida para framework
   - **TEMPLATE**: templates referenciados existen en TemplateRepository
   - **FILESYSTEM**: output_dir existe, es escribible, no tiene conflictos
   - **GIT**: directorio es un repo git, no tiene cambios uncommitted (warning)

**Criterios de aceptacion**:
- Reporta TODOS los errores, no solo el primero
- Incluye sugerencias de como resolver cada issue
- Distingue entre errors (bloquean) y warnings (informan)

---

## Tarea 4.2: Reglas de compatibilidad en domain

**Tipo**: feature
**Ganancia**: Previene combinaciones invalidas (e.g., Go + FastAPI, Rust + npm) con mensajes claros de que combinaciones son validas.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tac_bootstrap/domain/validators.py`
2. Definir reglas de compatibilidad:
   ```python
   COMPATIBLE_FRAMEWORKS: dict[Language, list[Framework]] = {
       Language.PYTHON: [Framework.FASTAPI, Framework.DJANGO, Framework.FLASK, Framework.NONE],
       Language.TYPESCRIPT: [Framework.NEXTJS, Framework.EXPRESS, Framework.NESTJS, Framework.REACT, Framework.VUE, Framework.NONE],
       # ... etc
   }

   COMPATIBLE_PACKAGE_MANAGERS: dict[Language, list[PackageManager]] = {
       Language.PYTHON: [PackageManager.UV, PackageManager.POETRY, PackageManager.PIP, PackageManager.PIPENV],
       # ... etc
   }

   ARCHITECTURES_REQUIRING_BASE_CLASSES = [Architecture.DDD, Architecture.CLEAN, Architecture.HEXAGONAL]
   ```
3. Funciones de validacion:
   - `validate_framework_language(fw, lang) -> ValidationIssue | None`
   - `validate_package_manager_language(pm, lang) -> ValidationIssue | None`
   - `validate_architecture_framework(arch, fw) -> ValidationIssue | None`

**Criterios de aceptacion**:
- Todas las combinaciones invalidas producen mensajes claros
- Sugerencias incluyen alternativas validas

---

## Tarea 4.3: Integrar validacion en scaffold

**Tipo**: feature
**Ganancia**: El CLI valida ANTES de generar archivos, evitando estados parciales.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. En `apply_plan()`, agregar al inicio:
   ```python
   validation = self.validation_service.validate_pre_scaffold(config, output_dir)
   if not validation.valid:
       raise ScaffoldValidationError(validation)
   if validation.warnings():
       for warning in validation.warnings():
           console.print(f"[yellow]Warning: {warning.message}[/yellow]")
   ```
3. Definir `ScaffoldValidationError` que formatea los issues en un mensaje legible

**Criterios de aceptacion**:
- Init con combinacion invalida muestra error ANTES de crear archivos
- Warnings se muestran pero no bloquean
- Error message incluye todas las issues y sugerencias

---

## Tarea 4.4: Tests para validation

**Tipo**: chore
**Ganancia**: Cobertura de todas las reglas de validacion.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tests/test_validation_service.py`
2. Tests:
   - Combinaciones validas pasan
   - Combinaciones invalidas fallan con mensaje correcto
   - Template validation detecta templates faltantes
   - Filesystem validation detecta directorio no-escribible
   - Multiples errores se reportan juntos
   - Warnings no bloquean

**Criterios de aceptacion**:
- `uv run pytest tests/test_validation_service.py` pasa
- Cada regla de compatibilidad tiene al menos un test positivo y uno negativo

---

# FASE 5: Value Objects y IDK Docstrings

**Objetivo**: Mejorar la calidad del codigo del CLI con value objects tipados y documentacion estandarizada.

**Ganancia de la fase**: Codigo mas mantenible, menos bugs por strings invalidos, y documentacion que facilita la busqueda semantica por agentes AI.

---

## Tarea 5.1: Value Objects

**Tipo**: chore
**Ganancia**: Validacion automatica en construccion. Un `ProjectName("Mi App!!")` falla inmediatamente en vez de propagar el string invalido por todo el sistema.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tac_bootstrap/domain/value_objects.py`
2. Value objects como Pydantic types con validacion:
   ```python
   class ProjectName(str):
       """Nombre de proyecto: lowercase, hyphens, no spaces, no special chars."""
       @classmethod
       def __get_validators__(cls):
           yield cls.validate
       @classmethod
       def validate(cls, v: str) -> "ProjectName":
           sanitized = v.strip().lower().replace(" ", "-")
           sanitized = re.sub(r"[^a-z0-9-]", "", sanitized)
           if not sanitized:
               raise ValueError("Project name cannot be empty after sanitization")
           return cls(sanitized)

   class TemplatePath(str):
       """Path relativo a un template que debe existir."""
       # Valida que no contiene '..' ni es absoluto

   class SemanticVersion(str):
       """Version semantica X.Y.Z con comparacion."""
       @property
       def tuple(self) -> tuple[int, int, int]:
           ...
       def __gt__(self, other): ...
       def __lt__(self, other): ...
   ```
3. No romper la API existente: los value objects se usan internamente, los validators de Pydantic los aceptan como str

**Criterios de aceptacion**:
- ProjectName sanitiza correctamente (spaces, special chars)
- TemplatePath rechaza paths peligrosos
- SemanticVersion compara correctamente (0.2.2 < 0.3.0)
- Tests existentes siguen pasando sin cambios

---

## Tarea 5.2: Aplicar IDK docstrings al CLI

**Tipo**: chore
**Ganancia**: Cada modulo del CLI tiene docstrings con Information Dense Keywords, facilitando que agentes AI encuentren el codigo relevante por busqueda semantica.

**Instrucciones para el agente**:

1. Agregar IDK docstrings a los modulos principales del CLI:
   - `scaffold_service.py`:
     ```python
     """
     IDK: scaffold-service, plan-builder, code-generation, template-rendering, file-operations
     Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem
     Invariants: Plans are idempotent, templates must exist, output directory must be writable
     """
     ```
   - `detect_service.py`:
     ```python
     """
     IDK: detect-service, auto-detection, tech-stack, language-detection, framework-detection
     Responsibility: Auto-detects project technology stack from existing files
     Invariants: Detection is read-only, never modifies files, returns confidence scores
     """
     ```
   - Aplicar a: `generate_service.py`, `validation_service.py`, `doctor_service.py`, `upgrade_service.py`, `template_repo.py`, `fs.py`, `git_adapter.py`
2. Formato IDK:
   - `IDK:` 5-12 keywords en kebab-case
   - `Responsibility:` 1 linea
   - `Invariants:` Condiciones que siempre se cumplen
3. NO agregar docstrings a funciones/metodos internos, solo a modulos y clases publicas

**Criterios de aceptacion**:
- Todos los modulos de application/ e infrastructure/ tienen IDK docstring
- Keywords son relevantes y no-redundantes
- No se modifico logica, solo docstrings

---

## Tarea 5.3: Tests para value objects

**Tipo**: chore
**Ganancia**: Garantia de que la validacion de value objects funciona correctamente.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tests/test_value_objects.py`
2. Tests para ProjectName:
   - `"My App"` → `"my-app"`
   - `"  Hello World  "` → `"hello-world"`
   - `"app@#$name"` → `"appname"`
   - `""` → raises ValueError
   - `"---"` → raises ValueError
3. Tests para TemplatePath:
   - `"claude/commands/test.md.j2"` → valido
   - `"../../../etc/passwd"` → raises ValueError
   - `"/absolute/path"` → raises ValueError
4. Tests para SemanticVersion:
   - `"0.2.2" < "0.3.0"` → True
   - `"1.0.0" > "0.99.99"` → True
   - `"abc"` → raises ValueError

**Criterios de aceptacion**:
- `uv run pytest tests/test_value_objects.py` pasa
- Edge cases cubiertos

---

# FASE 6: Documentacion Fractal como Skill

**Objetivo**: Incluir los generadores de documentacion fractal como parte de los proyectos generados, con slash command para invocacion facil.

**Ganancia de la fase**: Proyectos generados incluyen herramientas de documentacion automatica que mantienen docs sincronizados con el codigo, usando LLM local o remoto.

---

## Tarea 6.1: Template gen_docstring_jsdocs.py

**Tipo**: feature
**Ganancia**: Los proyectos generados incluyen un script que enriquece el codigo con docstrings IDK-first automaticamente, reduciendo el esfuerzo de documentar.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docstring_jsdocs.py.j2`
2. Crear renderizado en raiz: `scripts/gen_docstring_jsdocs.py` (con permisos de ejecucion)
3. Tomar como base el script existente en `ai_docs/doc/create-crud-entity/generating-fractal-docs/scripts/gen_docstring_jsdocs.py`
3. Adaptarlo como template Jinja2 con las siguientes variables:
   - `{{ config.project.language }}` → determina que lenguajes procesar por default
   - `{{ config.project.name }}` → nombre del proyecto en docstrings generados
   - `{{ config.paths.app_root | default("src") }}` → directorio raiz a procesar
4. El script generado debe:
   - Soportar Python y TypeScript (AST parsing para Python, regex para TS)
   - Usar API compatible con OpenAI (configurable: Ollama local, Anthropic, OpenAI)
   - Modo `add` (solo si no existe), `complement` (agregar secciones faltantes), `overwrite`
   - Flag `--changed-only` para procesar solo archivos con cambios en git
   - Flag `--dry-run` para preview
   - Generar docstrings con formato IDK:
     ```
     IDK: keyword1, keyword2, keyword3
     Responsibility: ...
     Invariants: ...
     Inputs: ...
     Outputs: ...
     Failure Modes: ...
     ```
5. Dependencias requeridas en el script header:
   ```python
   # /// script
   # dependencies = ["openai", "python-dotenv"]
   # ///
   ```

**Criterios de aceptacion**:
- Template renderiza sin errores con config basico
- Script generado es ejecutable con `uv run`
- Procesa archivos Python correctamente (AST parsing)
- Respeta --changed-only y --dry-run
- Funciona con Ollama local (default) y APIs remotas

---

## Tarea 6.2: Template gen_docs_fractal.py

**Tipo**: feature
**Ganancia**: Proyectos generados incluyen un generador de documentacion en arbol (un .md por carpeta) que da vision completa de la arquitectura.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/gen_docs_fractal.py.j2`
2. Crear renderizado en raiz: `scripts/gen_docs_fractal.py` (con permisos de ejecucion)
3. Tomar como base `ai_docs/doc/create-crud-entity/generating-fractal-docs/scripts/gen_docs_fractal.py`
3. Adaptarlo con variables Jinja2:
   - `{{ config.paths.app_root | default("src") }}` → `--include-root` default
   - `{{ config.project.name }}` → domain en frontmatter
   - `{{ config.project.language }}` → determina que archivos leer (*.py, *.ts, etc.)
4. El script generado debe:
   - Leer docstrings de Python y JSDoc de TypeScript
   - Generar un markdown por carpeta en `docs/`
   - Nombre del markdown: path concatenado (e.g., `docs/src/catalog/domain.md`)
   - Procesamiento bottom-up (carpetas mas profundas primero)
   - Frontmatter con: doc_type, domain, owner, level, tags, idk, related_code, children
   - Secciones requeridas: Overview, Responsibilities, Key APIs, Invariants, Side Effects, Operational Notes
   - Modo `complement` que preserva body existente y solo actualiza frontmatter
   - Carga vocabulario IDK canonico desde `canonical_idk.yml` si existe
5. Dependencias:
   ```python
   # /// script
   # dependencies = ["openai", "python-dotenv", "pyyaml"]
   # ///
   ```

**Criterios de aceptacion**:
- Template renderiza sin errores
- Script genera docs/ con estructura correcta
- Bottom-up: procesa hojas antes que padres
- Respeta modo complement (no borra body existente)
- Frontmatter YAML es valido

---

## Tarea 6.3: Template run_generators.sh

**Tipo**: feature
**Ganancia**: Script orquestador que ejecuta los generadores en orden correcto con checks de seguridad (git dirty, paths validos).

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`
2. Crear renderizado en raiz: `scripts/run_generators.sh` (con permisos de ejecucion)
2. Contenido del script generado:
   ```bash
   #!/usr/bin/env bash
   set -euo pipefail

   # Configuracion
   REPO_ROOT="{{ config.paths.app_root | default('.') }}"
   SCRIPTS_DIR="$(dirname "$0")"
   DOCS_DIR="docs"

   # Preflight checks
   command -v python3 >/dev/null || { echo "Error: python3 required"; exit 1; }
   command -v uv >/dev/null || { echo "Error: uv required"; exit 1; }

   # Parse flags
   DRY_RUN=""
   CHANGED_ONLY=""
   for arg in "$@"; do
       case $arg in
           --dry-run) DRY_RUN="--dry-run" ;;
           --changed-only) CHANGED_ONLY="--changed-only" ;;
       esac
   done

   # Step 1: Generate/update docstrings
   echo "=== Step 1: Enriching docstrings ==="
   uv run "$SCRIPTS_DIR/gen_docstring_jsdocs.py" \
       --root "$REPO_ROOT" \
       --mode complement \
       --languages {{ config.project.language }} \
       $CHANGED_ONLY $DRY_RUN

   # Step 2: Generate fractal docs
   echo "=== Step 2: Generating fractal documentation ==="
   uv run "$SCRIPTS_DIR/gen_docs_fractal.py" \
       --repo . \
       --docs-root "$DOCS_DIR" \
       --include-root "$REPO_ROOT" \
       --mode complement \
       $DRY_RUN

   echo "=== Done ==="
   ```
3. El script debe ser ejecutable (chmod +x en scaffold)

**Criterios de aceptacion**:
- Template renderiza bash valido
- Script falla limpiamente si faltan dependencias
- --dry-run se propaga a ambos generadores
- --changed-only se propaga al generador de docstrings

---

## Tarea 6.4: Slash command /generate_fractal_docs

**Tipo**: feature
**Ganancia**: Los usuarios pueden invocar la generacion de docs fractal como slash command de Claude Code, integrandolo en su workflow de desarrollo.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2`
2. Crear renderizado en raiz: `.claude/commands/generate_fractal_docs.md`
2. Contenido del command:
   ```markdown
   # Generate Fractal Documentation

   Generate or update the fractal documentation tree for this project.

   ## Arguments
   - $SCOPE: Scope of generation. Options: "full" (all files), "changed" (only git-changed files). Default: "changed"

   ## Instructions

   1. Run the fractal documentation generator:
      ```bash
      {% if SCOPE == "full" %}
      bash scripts/run_generators.sh
      {% else %}
      bash scripts/run_generators.sh --changed-only
      {% endif %}
      ```

   2. Review the generated documentation in `docs/` directory

   3. If new files were created, verify:
      - Frontmatter has valid YAML
      - IDK keywords are relevant to the module
      - Overview section accurately describes the folder contents

   4. Commit the documentation changes:
      ```bash
      git add docs/ && git commit -m "docs: update fractal documentation"
      ```

   ## Expected Output
   - Updated/created markdown files in `docs/` directory
   - One file per folder in `{{ config.paths.app_root | default("src") }}/`
   - Each file has frontmatter with IDK keywords and structured body sections
   ```

**Criterios de aceptacion**:
- Template renderiza markdown valido
- Comando es invocable como `/generate_fractal_docs` en Claude Code
- Soporta argumento SCOPE (full/changed)

---

## Tarea 6.5: Template canonical_idk.yml

**Tipo**: feature
**Ganancia**: Vocabulario controlado de keywords por dominio. Los generadores usan estos terminos para mantener consistencia terminologica en toda la documentacion del proyecto.

**Instrucciones para el agente**:

1. Crear template: `tac_bootstrap_cli/tac_bootstrap/templates/config/canonical_idk.yml.j2`
2. Crear renderizado en raiz: `canonical_idk.yml`
2. Contenido segun el lenguaje/framework del proyecto:
   ```yaml
   # Canonical IDK Vocabulary for {{ config.project.name }}
   # Used by fractal documentation generators to maintain consistent terminology

   domains:
   {% if config.project.language == "python" %}
     backend:
       - api-gateway, routing, middleware, authentication, authorization
       - database, repository, orm, migration, session-management
       - service-layer, use-case, business-logic, domain-model
       - validation, serialization, dto, schema
       - error-handling, exception, http-status
       - dependency-injection, factory, singleton
     testing:
       - unit-test, integration-test, fixture, mock, assertion
       - test-coverage, parametrize, conftest
   {% endif %}
   {% if config.project.language == "typescript" %}
     frontend:
       - component, hook, state-management, context, reducer
       - routing, navigation, page, layout
       - rendering, virtual-dom, reconciliation, hydration
       - styling, css-modules, tailwind, theme
     backend:
       - controller, middleware, guard, interceptor, pipe
       - module, provider, injectable, decorator
       - dto, entity, repository, service
   {% endif %}
     infrastructure:
       - deployment, ci-cd, docker, kubernetes
       - monitoring, logging, metrics, alerting
       - configuration, environment, secrets
     documentation:
       - docstring, jsdoc, fractal-docs, idk-keywords
       - readme, changelog, api-reference
   ```

**Criterios de aceptacion**:
- Template genera YAML valido para Python y TypeScript
- Keywords son relevantes al ecosistema del lenguaje
- Vocabulario es extensible (usuarios pueden agregar sus propios terminos)

---

## Tarea 6.6: Actualizar conditional_docs template

**Tipo**: feature
**Ganancia**: Los agentes AI saben cuando consultar la documentacion fractal, cerrando el loop entre generacion y consumo de docs.

**Instrucciones para el agente**:

1. Modificar template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/conditional_docs.md.j2`
2. Actualizar renderizado en raiz: `.claude/commands/conditional_docs.md`
2. Agregar las siguientes reglas condicionales al final del archivo:
   ```markdown
   ## Fractal Documentation

   - When working with documentation or understanding code structure:
     - Read `docs/` directory for fractal documentation of each module
     - Each file in `docs/` corresponds to a folder in `{{ config.paths.app_root | default("src") }}/`

   - When creating new modules or capabilities:
     - After implementation, run `/generate_fractal_docs changed` to update documentation
     - Ensure new modules have IDK docstrings before generating fractal docs

   - When refactoring or moving files:
     - Run `/generate_fractal_docs full` to regenerate all documentation
     - Review `docs/` for outdated references

   - When looking for canonical terminology:
     - Read `canonical_idk.yml` for approved domain keywords
     - Use these keywords in docstrings and documentation
   ```

**Criterios de aceptacion**:
- Reglas agregadas no rompen el formato existente del template
- Condiciones son claras y actionables
- Referencias a paths usan variables Jinja2

---

## Tarea 6.7: Integrar scripts fractal en ScaffoldService

**Tipo**: feature
**Ganancia**: Los scripts de documentacion fractal se incluyen automaticamente al generar proyectos, sin que el usuario tenga que agregarlos manualmente.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. En `build_plan()`, agregar metodo `_add_fractal_docs_scripts(plan, config)`:
   ```python
   def _add_fractal_docs_scripts(self, plan: ScaffoldPlan, config: TACConfig):
       """Add fractal documentation generation scripts."""
       # Scripts
       plan.add_file(
           template="scripts/gen_docstring_jsdocs.py.j2",
           output="scripts/gen_docstring_jsdocs.py",
           action=FileAction.CREATE,
           executable=True,
       )
       plan.add_file(
           template="scripts/gen_docs_fractal.py.j2",
           output="scripts/gen_docs_fractal.py",
           action=FileAction.CREATE,
           executable=True,
       )
       plan.add_file(
           template="scripts/run_generators.sh.j2",
           output="scripts/run_generators.sh",
           action=FileAction.CREATE,
           executable=True,
       )
       # Canonical IDK vocabulary
       plan.add_file(
           template="config/canonical_idk.yml.j2",
           output="canonical_idk.yml",
           action=FileAction.CREATE,
       )
       # Slash command
       plan.add_file(
           template="claude/commands/generate_fractal_docs.md.j2",
           output=".claude/commands/generate_fractal_docs.md",
           action=FileAction.CREATE,
       )
       # Docs directory
       plan.add_directory("docs")
   ```
3. Llamar `_add_fractal_docs_scripts()` siempre (no es condicional, todos los proyectos lo tienen)

**Criterios de aceptacion**:
- `tac-bootstrap init my-app` genera scripts/ con los 3 scripts fractal
- `canonical_idk.yml` se genera en la raiz del proyecto
- `.claude/commands/generate_fractal_docs.md` existe
- Directorio `docs/` se crea vacio
- Scripts tienen permisos de ejecucion

---

## Tarea 6.8: Tests para documentacion fractal

**Tipo**: chore
**Ganancia**: Verificar que los templates de docs fractal renderizan correctamente para distintas configuraciones de proyecto.

**Instrucciones para el agente**:

1. Crear `tac_bootstrap_cli/tests/test_fractal_docs_templates.py`
2. Tests:
   - `test_gen_docstring_renders_for_python` - Template con language=python renderiza
   - `test_gen_docstring_renders_for_typescript` - Template con language=typescript
   - `test_gen_docs_fractal_renders` - Template genera script valido
   - `test_run_generators_renders` - Bash script valido
   - `test_canonical_idk_renders_python` - YAML valido con keywords Python
   - `test_canonical_idk_renders_typescript` - YAML valido con keywords TS
   - `test_generate_fractal_docs_command_renders` - Slash command valido
   - `test_scaffold_includes_fractal_scripts` - ScaffoldService incluye scripts
   - `test_conditional_docs_includes_fractal_rules` - Reglas agregadas correctamente

**Criterios de aceptacion**:
- `uv run pytest tests/test_fractal_docs_templates.py` pasa
- Todos los templates generan contenido parseable (Python compilable, YAML parseable, Bash ejecutable)

---

# FASE 7: Document Workflow Mejorado

**Objetivo**: Mejorar el template existente de /document para incluir frontmatter IDK y integracion con docs fractal.

**Ganancia de la fase**: La documentacion de features generada automaticamente es mas rica, consistente, y encontrable por agentes AI.

---

## Tarea 7.1: Mejorar template /document con frontmatter IDK

**Tipo**: feature
**Ganancia**: Las feature docs generadas incluyen frontmatter con keywords IDK, haciendo que sean indexables y buscables semanticamente.

**Instrucciones para el agente**:

1. Modificar template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/document.md.j2`
2. Actualizar renderizado en raiz: `.claude/commands/document.md`
2. Agregar al formato de documentacion generada un frontmatter:
   ```markdown
   ---
   doc_type: feature
   adw_id: {adw_id}
   date: {YYYY-MM-DD}
   idk:
     - keyword1
     - keyword2
   tags:
     - feature
     - {capability}
   related_code:
     - src/{files_modified}
   ---
   ```
3. Agregar instruccion al prompt del command para que el agente:
   - Extraiga 5-8 IDK keywords del codigo implementado
   - Use vocabulario de `canonical_idk.yml` si existe
   - Incluya seccion "Testing" con comandos ejecutables
4. Agregar paso final: "Update conditional_docs.md with entry for this new documentation"

**Criterios de aceptacion**:
- Template renderiza correctamente
- Instrucciones son claras para el agente que ejecuta /document
- Frontmatter incluye IDK keywords

---

## Tarea 7.2: Integrar fractal docs en adw_document_iso.py

**Tipo**: feature
**Ganancia**: El workflow automatizado de documentacion (ADW) tambien actualiza los docs fractal, manteniendo ambos tipos de docs sincronizados con cada cambio.

**Instrucciones para el agente**:

1. Modificar template: `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2`
2. Actualizar renderizado en raiz: `adws/adw_document_iso.py`
2. En la funcion `generate_documentation()`, despues de ejecutar `/document`, agregar:
   ```python
   # Step 2: Update fractal documentation for changed files
   logger.info("Updating fractal documentation...")
   fractal_result = execute_template(
       AgentTemplateRequest(
           command="generate_fractal_docs",
           args=["changed"],
           ...
       )
   )
   if fractal_result.success:
       logger.info("Fractal documentation updated successfully")
   else:
       logger.warning(f"Fractal docs update failed (non-blocking): {fractal_result.error}")
   ```
3. La actualizacion de docs fractal debe ser **non-blocking**: si falla, logea warning pero no falla el workflow completo
4. Agregar los archivos generados en `docs/` al commit de documentacion

**Criterios de aceptacion**:
- Template renderiza correctamente
- Fractal docs se actualizan despues de feature docs
- Fallo en fractal docs no bloquea el workflow
- Archivos en docs/ se incluyen en el commit

---

## Tarea 7.3: Tests para document workflow mejorado

**Tipo**: chore
**Ganancia**: Verificar que las mejoras al workflow de documentacion no rompen el flujo existente.

**Instrucciones para el agente**:

1. Agregar tests en `tac_bootstrap_cli/tests/test_fractal_docs_templates.py`:
   - `test_document_command_has_idk_frontmatter` - Template incluye instrucciones de frontmatter
   - `test_adw_document_includes_fractal_step` - Workflow template incluye paso de fractal docs
   - `test_adw_document_fractal_is_non_blocking` - Fallo no bloquea workflow
2. Verificar que el template de /document es compatible con el formato actual (no rompe proyectos existentes)

**Criterios de aceptacion**:
- Tests pasan
- Templates son backward-compatible

---

# FASE 8: Documentacion y Release

**Objetivo**: Actualizar README con guias de los nuevos comandos y features, y crear CHANGELOG con todos los cambios de la v0.3.

**Ganancia de la fase**: Los usuarios encuentran documentacion completa de las nuevas funcionalidades sin tener que leer el codigo. El CHANGELOG da visibilidad de todo lo que cambio respecto a v0.2.x.

---

## Tarea 8.1: Actualizar README.md con nuevos comandos y guias

**Tipo**: chore
**Ganancia**: Los usuarios nuevos y existentes tienen documentacion completa de `generate entity`, documentacion fractal, base classes, y validacion multi-capa sin buscar en el codigo.

**Instrucciones para el agente**:

1. Modificar `tac_bootstrap_cli/README.md`
2. Agregar las siguientes secciones NUEVAS:

### Seccion: Comando `generate entity`
Agregar despues de la seccion "Utility Commands":
```markdown
### Entity Generation (DDD Projects)

Generate complete CRUD entities with vertical slice architecture:

\`\`\`bash
# Interactive wizard (recommended)
tac-bootstrap generate entity Product

# Non-interactive with fields
tac-bootstrap generate entity Product \
  --capability catalog \
  --fields "name:str:required,price:float:required,description:text,is_available:bool" \
  --no-interactive

# With authorization (row-level security)
tac-bootstrap generate entity Order \
  --capability orders \
  --fields "total:decimal:required,status:str:required" \
  --authorized \
  --no-interactive

# Preview without creating files
tac-bootstrap generate entity User --dry-run

# Force overwrite existing entity
tac-bootstrap generate entity Product -c catalog --force
\`\`\`

#### Available Options for `generate entity`

| Option | Short | Description |
|--------|-------|-------------|
| `--capability` | `-c` | Capability/module name (default: entity name in kebab-case) |
| `--fields` | `-f` | Field definitions: "name:type[:required]" comma-separated |
| `--authorized` | | Generate with row-level security templates |
| `--async` | | Use async repository (AsyncSession) |
| `--with-events` | | Generate domain events |
| `--interactive` | | Interactive wizard (default) |
| `--dry-run` | | Preview without creating files |
| `--force` | | Overwrite existing entity files |

#### Field Types

| Type | Python Type | SQLAlchemy Type |
|------|------------|-----------------|
| `str` | `str` | `String(max_length)` |
| `int` | `int` | `Integer` |
| `float` | `float` | `Float` |
| `bool` | `bool` | `Boolean` |
| `datetime` | `datetime` | `DateTime` |
| `uuid` | `str` | `String(36)` |
| `text` | `str` | `Text` |
| `decimal` | `Decimal` | `Numeric` |
| `json` | `dict` | `JSON` |

#### Generated Structure

\`\`\`
src/{capability}/
├── domain/
│   └── {entity}.py          # Domain model (extends BaseEntity)
├── application/
│   ├── schemas.py            # Create/Update/Response DTOs
│   └── service.py            # CRUD service (extends BaseService)
├── infrastructure/
│   ├── models.py             # SQLAlchemy ORM model
│   └── repository.py         # Data access (extends BaseRepository)
└── api/
    └── routes.py             # FastAPI CRUD endpoints
\`\`\`

> **Requirement**: Entity generation requires `--architecture ddd|clean|hexagonal` and `--framework fastapi`. The shared base classes in `src/shared/` must exist (generated automatically with `init`).
```

### Seccion: Base Classes (DDD)
Agregar despues de "Generated Structure":
```markdown
### Shared Base Classes (DDD Architecture)

When using `--architecture ddd` with `--framework fastapi`, the CLI generates shared infrastructure in `src/shared/`:

| File | Purpose |
|------|---------|
| `domain/base_entity.py` | Entity base with audit trail, soft delete, state management |
| `domain/base_schema.py` | BaseCreate, BaseUpdate, BaseResponse DTOs |
| `application/base_service.py` | Generic CRUD service with typed generics |
| `infrastructure/base_repository.py` | Generic SQLAlchemy repository (sync) |
| `infrastructure/base_repository_async.py` | Generic async repository |
| `infrastructure/database.py` | SQLAlchemy session management |
| `infrastructure/exceptions.py` | Typed exceptions with HTTP handlers |
| `infrastructure/responses.py` | PaginatedResponse, ErrorResponse models |
| `infrastructure/dependencies.py` | FastAPI dependency injection factories |
| `api/health.py` | Health check endpoint |

These classes eliminate ~80% of boilerplate per entity. Each new entity inherits from them.
```

### Seccion: Fractal Documentation
Agregar despues de "ADW" section:
```markdown
## Fractal Documentation

Projects include automatic documentation generation tools:

### Generate Documentation

\`\`\`bash
# Run fractal documentation generators
bash scripts/run_generators.sh

# Only process changed files
bash scripts/run_generators.sh --changed-only

# Preview without writing
bash scripts/run_generators.sh --dry-run
\`\`\`

### What It Does

1. **Step 1: Docstring Enrichment** (`gen_docstring_jsdocs.py`)
   - Adds IDK-first docstrings to Python/TypeScript files
   - Keywords, Responsibility, Invariants, Failure Modes

2. **Step 2: Fractal Docs** (`gen_docs_fractal.py`)
   - Generates one markdown per folder in `docs/`
   - Bottom-up processing (deeper folders first)
   - Frontmatter with IDK keywords, tags, and relationships

### Slash Command

Use `/generate_fractal_docs` in Claude Code:
\`\`\`
/generate_fractal_docs changed   # Only changed files
/generate_fractal_docs full      # All files
\`\`\`

### Canonical IDK Vocabulary

Edit `canonical_idk.yml` to define approved keywords for your domain. The generators use this vocabulary for consistent terminology across all documentation.
```

### Seccion: Validation
Agregar en la seccion de Commands:
```markdown
### Multi-layer Validation

The CLI validates configurations in multiple layers before generating:

1. **Schema** - Pydantic type validation
2. **Domain** - Framework/language compatibility rules
3. **Template** - Referenced templates exist
4. **Filesystem** - Output directory writable, no conflicts
5. **Git** - Repository state warnings
```

3. Actualizar la tabla de "Requirements" para incluir nuevas dependencias opcionales:
```markdown
## Requirements

- Python 3.10+
- Git
- Claude Code CLI
- SQLAlchemy (for generated DDD projects)
- FastAPI (for generated API projects)

### Optional (for Fractal Documentation)

- OpenAI-compatible API (Ollama local recommended)
- `OPENAI_BASE_URL` and `OPENAI_API_KEY` environment variables
```

4. Actualizar la version mencionada en el README de `v0.2.2` a `v0.3.0`

**Criterios de aceptacion**:
- README tiene seccion de `generate entity` con ejemplos completos
- README tiene seccion de base classes con tabla de archivos
- README tiene seccion de fractal documentation con uso
- README tiene seccion de validacion multi-capa
- Todas las versiones actualizadas a 0.3.0
- Ejemplos de comandos son copy-pasteable y funcionales

---

## Tarea 8.2: Crear/Actualizar CHANGELOG.md

**Tipo**: chore
**Ganancia**: Registro historico de cambios que permite a usuarios entender que cambio entre versiones y decidir si actualizar. Sigue formato Keep a Changelog.

**Instrucciones para el agente**:

1. Crear o actualizar `/Volumes/MAc1/Celes/tac_bootstrap/CHANGELOG.md`
2. Usar formato [Keep a Changelog](https://keepachangelog.com/en/1.1.0/):

```markdown
# Changelog

All notable changes to TAC Bootstrap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - YYYY-MM-DD

### Added

#### Entity Generation (Fase 2)
- New command `tac-bootstrap generate entity <name>` for CRUD entity generation
- Interactive wizard for defining entity fields
- Support for field types: str, int, float, bool, datetime, uuid, text, decimal, json
- `--authorized` flag for row-level security templates
- `--async` flag for async repository generation
- `--with-events` flag for domain events
- Vertical slice architecture: domain, application, infrastructure, api layers

#### Shared Base Classes (Fase 1)
- `base_entity.py` - Entity base with audit trail, soft delete, state management, optimistic locking
- `base_schema.py` - BaseCreate, BaseUpdate, BaseResponse DTOs
- `base_service.py` - Generic typed CRUD service with soft delete
- `base_repository.py` - Generic SQLAlchemy sync repository
- `base_repository_async.py` - Generic async repository with bulk operations
- `database.py` - SQLAlchemy session management (sync/async)
- `exceptions.py` - Typed exceptions with FastAPI HTTP handlers
- `responses.py` - PaginatedResponse, SuccessResponse, ErrorResponse
- `dependencies.py` - FastAPI dependency injection factories
- `health.py` - Health check endpoint with DB connectivity check
- Auto-included when `--architecture ddd|clean|hexagonal` and `--framework fastapi`

#### Fractal Documentation (Fase 6)
- `scripts/gen_docstring_jsdocs.py` - Automatic IDK-first docstring generation
- `scripts/gen_docs_fractal.py` - Fractal documentation tree generator
- `scripts/run_generators.sh` - Orchestrator script
- Slash command `/generate_fractal_docs` for Claude Code integration
- `canonical_idk.yml` - Domain-specific keyword vocabulary
- Bottom-up documentation: one markdown per folder in `docs/`
- Support for Python and TypeScript

#### Document Workflow Improvements (Fase 7)
- IDK frontmatter in generated feature documentation
- Fractal docs integration in `adw_document_iso.py`
- Automatic conditional_docs.md updates for new documentation

#### Multi-layer Validation (Fase 4)
- ValidationService with 5 validation layers
- Framework/language compatibility rules
- Template existence verification
- Filesystem permission and conflict checks
- Git state warnings
- All errors reported at once with fix suggestions

#### Audit Trail (Fase 3)
- `bootstrap` section in config.yml with generation metadata
- Tracks: generated_at, generated_by, last_upgrade, schema_version
- Automatic timestamp recording on init and upgrade

#### Code Quality (Fase 5)
- Value Objects: ProjectName, TemplatePath, SemanticVersion
- IDK-first docstrings on all application and infrastructure modules

### Changed
- `conditional_docs.md` template includes fractal documentation rules
- `document.md` template generates docs with IDK frontmatter
- `adw_document_iso.py` template includes fractal docs step (non-blocking)
- `config.yml` template includes bootstrap metadata section
- Scaffold service includes shared base classes for DDD projects
- Scaffold service includes fractal documentation scripts

### Fixed
- (none in this release)

## [0.2.2] - 2024-XX-XX

### Added
- Webhook trigger setup documentation in README
- `gh extension install cli/gh-webhook` instructions

### Fixed
- Upgrade config normalization (issue #106)

## [0.2.1] - 2024-XX-XX

### Added
- Initial `upgrade` command
- Backup creation before upgrades

## [0.2.0] - 2024-XX-XX

### Added
- `add-agentic` command for existing repositories
- Auto-detection of language, framework, package manager
- `doctor` command with auto-fix
- `render` command for regeneration from config.yml

## [0.1.0] - 2024-XX-XX

### Added
- Initial release
- `init` command with interactive wizard
- Support for Python, TypeScript, Go, Rust, Java
- 25+ slash commands templates
- ADW workflow templates
- Hook scripts
```

3. Reemplazar `YYYY-MM-DD` con la fecha actual de release
4. Ajustar las fechas de versiones anteriores si se conocen (consultar git log)

**Criterios de aceptacion**:
- CHANGELOG.md existe en la raiz del proyecto
- Sigue formato Keep a Changelog
- v0.3.0 lista TODOS los cambios de las 7 fases
- Cada cambio referencia la fase correspondiente
- Secciones: Added, Changed, Fixed
- Versiones anteriores listadas (aunque sea con fechas placeholder)
- Es parseable por herramientas automaticas de changelog

---

# RESUMEN DE EJECUCION

## Iteracion 1: Fundamentos (Fases 1 + 3 + 5)
| # | Tarea | Tipo | Template (.j2) | Renderizado en raiz |
|---|-------|------|----------------|---------------------|
| 1.1 | base_entity.py | feature | `templates/shared/base_entity.py.j2` | `src/shared/domain/base_entity.py` |
| 1.2 | base_schema.py | feature | `templates/shared/base_schema.py.j2` | `src/shared/domain/base_schema.py` |
| 1.3 | base_service.py | feature | `templates/shared/base_service.py.j2` | `src/shared/application/base_service.py` |
| 1.4 | base_repository.py | feature | `templates/shared/base_repository.py.j2` | `src/shared/infrastructure/base_repository.py` |
| 1.5 | base_repository_async.py | feature | `templates/shared/base_repository_async.py.j2` | `src/shared/infrastructure/base_repository_async.py` |
| 1.6 | database.py | feature | `templates/shared/database.py.j2` | `src/shared/infrastructure/database.py` |
| 1.7 | exceptions.py | feature | `templates/shared/exceptions.py.j2` | `src/shared/infrastructure/exceptions.py` |
| 1.8 | responses.py | feature | `templates/shared/responses.py.j2` | `src/shared/infrastructure/responses.py` |
| 1.9 | dependencies.py | feature | `templates/shared/dependencies.py.j2` | `src/shared/infrastructure/dependencies.py` |
| 1.10 | health.py | feature | `templates/shared/health.py.j2` | `src/shared/api/health.py` |
| 1.11 | Integrar en ScaffoldService | feature | - | `application/scaffold_service.py` |
| 1.12 | Tests base classes | chore | - | `tests/test_base_classes_templates.py` |
| 3.1 | BootstrapMetadata model | feature | - | `domain/models.py` |
| 3.2 | Registrar metadata | feature | `templates/config/config.yml.j2` | `application/scaffold_service.py` |
| 3.3 | Tests audit trail | chore | - | `tests/test_scaffold_service.py` |
| 5.1 | Value Objects | chore | - | `domain/value_objects.py` |
| 5.2 | IDK Docstrings | chore | - | `application/*.py`, `infrastructure/*.py` |
| 5.3 | Tests value objects | chore | - | `tests/test_value_objects.py` |

## Iteracion 2: Generacion de Entidades (Fases 2 + 4)
| # | Tarea | Tipo | Template (.j2) | Renderizado en raiz |
|---|-------|------|----------------|---------------------|
| 2.1 | EntitySpec model | feature | - | `domain/entity_config.py` |
| 2.2 | Templates CRUD basicos | feature | `templates/capabilities/crud_basic/*.j2` | *(bajo demanda con generate)* |
| 2.3 | GenerateService | feature | - | `application/generate_service.py` |
| 2.4 | Comando CLI generate | feature | - | `interfaces/cli.py` |
| 2.5 | Wizard entity fields | feature | - | `interfaces/wizard.py` |
| 2.6 | Templates CRUD authorized | feature | `templates/capabilities/crud_authorized/*.j2` | *(bajo demanda con generate)* |
| 2.7 | Tests generate entity | chore | - | `tests/test_generate_service.py`, `tests/test_entity_config.py` |
| 4.1 | ValidationService | feature | - | `application/validation_service.py` |
| 4.2 | Reglas de compatibilidad | feature | - | `domain/validators.py` |
| 4.3 | Integrar validacion | feature | - | `application/scaffold_service.py` |
| 4.4 | Tests validation | chore | - | `tests/test_validation_service.py` |

## Iteracion 3: Documentacion Fractal (Fases 6 + 7)
| # | Tarea | Tipo | Template (.j2) | Renderizado en raiz |
|---|-------|------|----------------|---------------------|
| 6.1 | gen_docstring_jsdocs.py | feature | `templates/scripts/gen_docstring_jsdocs.py.j2` | `scripts/gen_docstring_jsdocs.py` |
| 6.2 | gen_docs_fractal.py | feature | `templates/scripts/gen_docs_fractal.py.j2` | `scripts/gen_docs_fractal.py` |
| 6.3 | run_generators.sh | feature | `templates/scripts/run_generators.sh.j2` | `scripts/run_generators.sh` |
| 6.4 | /generate_fractal_docs | feature | `templates/claude/commands/generate_fractal_docs.md.j2` | `.claude/commands/generate_fractal_docs.md` |
| 6.5 | canonical_idk.yml | feature | `templates/config/canonical_idk.yml.j2` | `canonical_idk.yml` |
| 6.6 | Actualizar conditional_docs | feature | `templates/claude/commands/conditional_docs.md.j2` | `.claude/commands/conditional_docs.md` |
| 6.7 | Integrar en ScaffoldService | feature | - | `application/scaffold_service.py` |
| 6.8 | Tests fractal docs | chore | - | `tests/test_fractal_docs_templates.py` |
| 7.1 | Mejorar /document con IDK | feature | `templates/claude/commands/document.md.j2` | `.claude/commands/document.md` |
| 7.2 | Integrar en adw_document_iso | feature | `templates/adws/adw_document_iso.py.j2` | `adws/adw_document_iso.py` |
| 7.3 | Tests document mejorado | chore | - | `tests/test_fractal_docs_templates.py` |

## Fase Final: Documentacion y Release (Fase 8)
| # | Tarea | Tipo | Template (.j2) | Renderizado en raiz |
|---|-------|------|----------------|---------------------|
| 8.1 | Actualizar README.md | chore | - | `tac_bootstrap_cli/README.md` |
| 8.2 | Crear CHANGELOG.md | chore | - | `CHANGELOG.md` |

---

## Metricas de Exito

- **32 tareas** en total (22 features, 10 chores)
- Tests: `uv run pytest` pasa con >90% coverage en codigo nuevo
- Backward compatible: proyectos generados con v0.2.x siguen funcionando
- Nuevo comando: `tac-bootstrap generate entity` disponible
- Docs fractal: proyectos nuevos incluyen generadores funcionales
- Zero breaking changes en CLI existente (init, add-agentic, doctor, upgrade, render)

## Validacion Dual Creation (este proyecto como referencia)

Despues de completar todas las tareas, verificar que ESTE proyecto tiene:

```
/Volumes/MAc1/Celes/tac_bootstrap/
├── src/shared/                              # Fase 1
│   ├── domain/
│   │   ├── base_entity.py                   # Tarea 1.1
│   │   └── base_schema.py                   # Tarea 1.2
│   ├── application/
│   │   └── base_service.py                  # Tarea 1.3
│   ├── infrastructure/
│   │   ├── base_repository.py               # Tarea 1.4
│   │   ├── base_repository_async.py         # Tarea 1.5
│   │   ├── database.py                      # Tarea 1.6
│   │   ├── exceptions.py                    # Tarea 1.7
│   │   ├── responses.py                     # Tarea 1.8
│   │   └── dependencies.py                  # Tarea 1.9
│   └── api/
│       └── health.py                        # Tarea 1.10
├── scripts/
│   ├── gen_docstring_jsdocs.py              # Tarea 6.1
│   ├── gen_docs_fractal.py                  # Tarea 6.2
│   └── run_generators.sh                    # Tarea 6.3
├── .claude/commands/
│   ├── generate_fractal_docs.md             # Tarea 6.4
│   ├── conditional_docs.md                  # Tarea 6.6 (actualizado)
│   └── document.md                          # Tarea 7.1 (actualizado)
├── canonical_idk.yml                        # Tarea 6.5
├── adws/
│   └── adw_document_iso.py                  # Tarea 7.2 (actualizado)
├── docs/                                    # Directorio para fractal docs
├── CHANGELOG.md                             # Tarea 8.2
└── tac_bootstrap_cli/
    └── README.md                            # Tarea 8.1 (actualizado)
```

Y que el CLI tiene los templates correspondientes:
```
tac_bootstrap_cli/tac_bootstrap/templates/
├── shared/                                  # Fase 1
│   ├── base_entity.py.j2
│   ├── base_schema.py.j2
│   ├── base_service.py.j2
│   ├── base_repository.py.j2
│   ├── base_repository_async.py.j2
│   ├── database.py.j2
│   ├── exceptions.py.j2
│   ├── responses.py.j2
│   ├── dependencies.py.j2
│   └── health.py.j2
├── capabilities/                            # Fase 2
│   ├── crud_basic/
│   │   ├── domain_entity.py.j2
│   │   ├── schemas.py.j2
│   │   ├── service.py.j2
│   │   ├── repository.py.j2
│   │   ├── orm_model.py.j2
│   │   └── routes.py.j2
│   └── crud_authorized/
│       ├── routes_authorized.py.j2
│       ├── service_authorized.py.j2
│       └── repository_authorized.py.j2
├── scripts/                                 # Fase 6
│   ├── gen_docstring_jsdocs.py.j2
│   ├── gen_docs_fractal.py.j2
│   └── run_generators.sh.j2
├── config/
│   └── canonical_idk.yml.j2                # Fase 6
└── claude/commands/
    └── generate_fractal_docs.md.j2          # Fase 6
```
