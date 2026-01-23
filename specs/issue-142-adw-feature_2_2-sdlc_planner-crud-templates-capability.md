# Feature: Templates CRUD basicos (capability)

## Metadata
issue_number: `142`
adw_id: `feature_2_2`
issue_json: `{"number":142,"title":"Tarea 2.2: Templates CRUD basicos (capability)","body":"/feature\n/adw_sdlc_iso\n/adw_id: feature_2_2\n\n***Tipo**: feature\n**Ganancia**: Templates Jinja2 que generan una vertical slice completa. Cada archivo usa EntitySpec como contexto para generar codigo especifico a la entidad.\n\n**Instrucciones para el agente**:\n\n1. Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/`\n2. Crear los siguientes templates:\n\n**`domain_entity.py.j2`**:\n- Importa Entity de shared\n- Clase `{{ entity.name }}(Entity)`:\n  - `type_discriminator = \"{{ entity.snake_name }}\"`\n  - Un campo por cada FieldSpec\n  - Metodos de negocio placeholder (validate, calculate)\n\n**`schemas.py.j2`**:\n- `{{ entity.name }}Create(BaseCreate)`: campos required\n- `{{ entity.name }}Update(BaseUpdate)`: todos Optional\n- `{{ entity.name }}Response(BaseResponse)`: todos los campos\n\n**`service.py.j2`**:\n- `{{ entity.name }}Service(BaseService[...])`:\n  - Constructor con repository\n  - Override de metodos si necesario\n  - Metodos custom placeholder\n\n**`repository.py.j2`**:\n- `{{ entity.name }}Repository(BaseRepository[{{ entity.name }}Model])`:\n  - Metodos custom de query (get_by_code, search, etc.)\n\n**`orm_model.py.j2`**:\n- Modelo SQLAlchemy `{{ entity.name }}Model(Base)`:\n  - `__tablename__ = \"{{ entity.table_name }}\"`\n  - Columnas mapeadas desde FieldSpec con tipos SQLAlchemy\n  - Indexes en campos marcados como indexed\n\n**`routes.py.j2`**:\n- Router FastAPI:\n  - `POST /{{ entity.plural_name }}/` → create (201)\n  - `GET /{{ entity.plural_name }}/{id}` → get_by_id (200)\n  - `GET /{{ entity.plural_name }}/` → get_all con paginacion (200)\n  - `PUT /{{ entity.plural_name }}/{id}` → update (200)\n  - `DELETE /{{ entity.plural_name }}/{id}` → soft_delete (200)\n\n3. Variables Jinja2 disponibles: `{{ entity }}` (EntitySpec), `{{ config }}` (TACConfig)\n4. Mapeo de FieldType a tipos SQLAlchemy:\n   - str → String(max_length), int → Integer, float → Float\n   - bool → Boolean, datetime → DateTime, uuid → String(36)\n   - text → Text, decimal → Numeric, json → JSON\n\n**Criterios de aceptacion**:\n- Cada template renderiza Python valido con un EntitySpec de ejemplo\n- Los imports entre archivos son correctos (domain importa de shared, service importa repo, etc.)\n- Los tipos SQLAlchemy mapean correctamente desde FieldType\n\n# FASE 2: Comando `generate entity`\n\n**Objetivo**: Agregar un nuevo comando CLI que genera entidades CRUD completas siguiendo la vertical slice architecture.\n\n**Ganancia de la fase**: Los desarrolladores pueden crear entidades completas (domain, schemas, service, repo, routes) con un solo comando, eliminando el trabajo manual de copiar y adaptar boilerplate.\n"}`

## Feature Description

Esta feature crea un conjunto de templates Jinja2 en `templates/capabilities/crud_basic/` que generan una vertical slice completa para entidades CRUD. Los templates transforman un `EntitySpec` (especificación de entidad con nombre, campos y metadatos) en código Python para FastAPI + SQLAlchemy que incluye:

- Domain entity (hereda de Entity base class)
- Pydantic schemas (Create, Update, Response)
- Service layer (hereda de BaseService)
- Repository layer (hereda de BaseRepository)
- ORM model (SQLAlchemy)
- FastAPI routes (CRUD endpoints)

Los templates son el corazón del generador de código del CLI. Permiten crear entidades completas con un solo comando, siguiendo consistentemente los patrones de arquitectura DDD y vertical slicing.

## User Story

As a developer using TAC Bootstrap
I want to generate a complete CRUD entity from a specification
So that I can quickly scaffold new features without manually writing boilerplate code

## Problem Statement

Crear una nueva entidad CRUD requiere escribir manualmente 6 archivos (domain, schemas, service, repository, ORM model, routes) con código altamente repetitivo que sigue patrones consistentes. Este proceso manual es:
- Propenso a errores de tipeo y inconsistencias
- Lento (15-30 minutos por entidad)
- Requiere recordar imports correctos y patrones de arquitectura
- Dificulta mantener consistencia entre entidades

Se necesita un sistema de templates que automatice la generación de estos archivos, usando EntitySpec como entrada.

## Solution Statement

Crear 6 templates Jinja2 en `templates/capabilities/crud_basic/` que reciban un EntitySpec y generen código Python válido para cada capa de la vertical slice. Los templates:

1. Mapean FieldSpec a tipos de Pydantic y SQLAlchemy
2. Generan imports correctos entre capas
3. Crean métodos de repositorio condicionales basados en campos indexados
4. Usan base classes compartidas para reducir código duplicado
5. Incluyen type hints completos y docstrings mínimas

El approach es template-first: los templates son la fuente de verdad para la estructura de código. EntitySpec proporciona metadatos (nombre, campos, tipos) y los templates aplican los patrones arquitecturales.

## Relevant Files

Archivos existentes para referencia:

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig y otros modelos Pydantic
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2` - Base Entity template como ejemplo de template bien estructurado
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_schema.py.j2` - Base schemas (BaseCreate, BaseUpdate, BaseResponse)
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_service.py.j2` - Base service con generics
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_repository.py.j2` - Base repository con SQLAlchemy
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository que renderiza templates
- `ai_docs/doc/PLAN_TAC_V03_ROBUST.md` - Plan maestro con definiciones de EntitySpec y FieldSpec (líneas 504-620)
- `config.yml` - Configuración del proyecto TAC Bootstrap

### New Files

Templates a crear:
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/domain_entity.py.j2` - Domain entity class
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/schemas.py.j2` - Pydantic schemas (Create, Update, Response)
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/service.py.j2` - Service layer
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/repository.py.j2` - Repository layer
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/orm_model.py.j2` - SQLAlchemy ORM model
- `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/routes.py.j2` - FastAPI routes

Tests:
- `tac_bootstrap_cli/tests/test_crud_templates.py` - Tests de renderizado de templates

## Implementation Plan

### Phase 1: Foundation - EntitySpec y estructura
Crear el directorio para templates y definir el modelo EntitySpec en domain si no existe (según PLAN_TAC_V03_ROBUST.md). Verificar que las propiedades derivadas (snake_name, plural_name, table_name) funcionan correctamente.

### Phase 2: Core Implementation - Templates individuales
Crear cada uno de los 6 templates en orden de dependencias:
1. domain_entity.py.j2 (no depende de otros)
2. schemas.py.j2 (depende de domain entity)
3. orm_model.py.j2 (independiente, solo SQLAlchemy)
4. repository.py.j2 (depende de orm_model)
5. service.py.j2 (depende de repository y domain)
6. routes.py.j2 (depende de schemas y service)

Cada template debe:
- Generar Python válido con type hints completos
- Incluir docstrings mínimas para clases y métodos públicos
- Usar imports relativos dentro del módulo, absolutos para shared
- Manejar condicionales (indexed fields, nullable, max_length)

### Phase 3: Integration - Tests y validación
Crear tests que rendericen cada template con un EntitySpec de ejemplo y validen:
- Python es sintácticamente válido (compile())
- Contiene las clases/funciones esperadas
- Los imports son correctos
- El mapeo de tipos es correcto

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear directorio y verificar EntitySpec
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/`
- Leer `ai_docs/doc/PLAN_TAC_V03_ROBUST.md` líneas 504-620 para entender EntitySpec y FieldSpec
- Verificar si EntitySpec ya existe en `tac_bootstrap_cli/tac_bootstrap/domain/models.py`
- Si no existe, crear modelos EntitySpec y FieldSpec según especificación:
  ```python
  class FieldType(str, Enum):
      STR = "str"
      INT = "int"
      FLOAT = "float"
      BOOL = "bool"
      DATETIME = "datetime"
      UUID = "uuid"
      TEXT = "text"
      DECIMAL = "decimal"
      JSON = "json"

  class FieldSpec(BaseModel):
      name: str
      type: FieldType
      nullable: bool = False
      indexed: bool = False
      max_length: int | None = None
      default: Any | None = None

  class EntitySpec(BaseModel):
      name: str  # PascalCase
      capability: str  # kebab-case
      fields: list[FieldSpec]

      @property
      def snake_name(self) -> str:
          """Convert PascalCase to snake_case"""
          ...

      @property
      def plural_name(self) -> str:
          """Simple pluralization (name + s)"""
          ...

      @property
      def table_name(self) -> str:
          """Database table name (plural_name)"""
          ...
  ```

### Task 2: Crear template domain_entity.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/domain_entity.py.j2`
- Template debe generar:
  - Import: `from {{ config.project.package_name }}.shared.domain.base_entity import Entity`
  - Clase `{{ entity.name }}(Entity)` con:
    - Docstring con IDK pattern
    - `type: str = Field(default="{{ entity.snake_name }}", description="Entity type discriminator")`
    - Un campo Pydantic por cada FieldSpec en entity.fields:
      - Nombre: `{{ field.name }}`
      - Tipo: mapeo de FieldType a tipos Python (str, int, float, bool, datetime, UUID, etc.)
      - nullable: `{{ field.name }}: {{ python_type }} | None = None` si nullable=True
      - max_length: `Field(..., max_length={{ field.max_length }})` para strings
      - default: `Field(default={{ field.default }})` si default provisto
    - Métodos placeholder con pass y docstrings:
      - `def validate(self) -> None:` - Validación de negocio
      - `def calculate_totals(self) -> None:` - Cálculos de negocio
- Usar filtros Jinja2 para mapeo de tipos:
  ```jinja2
  {% set type_map = {
      'str': 'str',
      'int': 'int',
      'float': 'float',
      'bool': 'bool',
      'datetime': 'datetime',
      'uuid': 'UUID',
      'text': 'str',
      'decimal': 'Decimal',
      'json': 'dict[str, Any]'
  } %}
  ```

### Task 3: Crear template schemas.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/schemas.py.j2`
- Template debe generar:
  - Imports:
    - `from pydantic import BaseModel, Field`
    - `from {{ config.project.package_name }}.shared.schemas.base_schema import BaseCreate, BaseUpdate, BaseResponse`
    - Tipos necesarios (UUID, datetime, Decimal, etc.)
  - `class {{ entity.name }}Create(BaseCreate)`:
    - Docstring
    - Campos required de FieldSpec (nullable=False)
    - Con validadores Field() para max_length, defaults
  - `class {{ entity.name }}Update(BaseUpdate)`:
    - Docstring
    - Todos los campos como Optional
  - `class {{ entity.name }}Response(BaseResponse)`:
    - Docstring
    - Todos los campos de FieldSpec
    - Heredados de BaseResponse (id, created_at, updated_at, etc.)

### Task 4: Crear template orm_model.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/orm_model.py.j2`
- Template debe generar:
  - Imports:
    - `from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, JSON, Numeric, Index`
    - `from sqlalchemy.orm import declarative_base` o `from {{ config.project.package_name }}.shared.database import Base`
    - `from datetime import datetime, UTC`
    - `from uuid import uuid4`
  - `class {{ entity.name }}Model(Base)`:
    - Docstring con IDK
    - `__tablename__ = "{{ entity.table_name }}"`
    - Columnas por cada FieldSpec:
      - Mapeo de FieldType a tipos SQLAlchemy:
        - str → `Column(String({{ field.max_length or 255 }}), nullable={{ field.nullable }})`
        - int → `Column(Integer, nullable={{ field.nullable }})`
        - float → `Column(Float, nullable={{ field.nullable }})`
        - bool → `Column(Boolean, nullable={{ field.nullable }})`
        - datetime → `Column(DateTime(timezone=True), nullable={{ field.nullable }})`
        - uuid → `Column(String(36), nullable={{ field.nullable }})`
        - text → `Column(Text, nullable={{ field.nullable }})`
        - decimal → `Column(Numeric(precision=10, scale=2), nullable={{ field.nullable }})`
        - json → `Column(JSON, nullable={{ field.nullable }})`
    - `__table_args__` con indexes condicionales:
      ```jinja2
      {% set indexed_fields = entity.fields | selectattr('indexed', 'equalto', true) | list %}
      {% if indexed_fields %}
      __table_args__ = (
          {% for field in indexed_fields %}
          Index('ix_{{ entity.table_name }}_{{ field.name }}', '{{ field.name }}'),
          {% endfor %}
      )
      {% endif %}
      ```

### Task 5: Crear template repository.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/repository.py.j2`
- Template debe generar:
  - Imports:
    - `from sqlalchemy.orm import Session`
    - `from {{ config.project.package_name }}.shared.repositories.base_repository import BaseRepository`
    - `from .orm_model import {{ entity.name }}Model`
    - `from typing import Optional, List`
  - `class {{ entity.name }}Repository(BaseRepository[{{ entity.name }}Model])`:
    - Docstring
    - Constructor que pasa el modelo a super()
    - Métodos condicionales basados en campos indexados:
      ```jinja2
      {% for field in entity.fields | selectattr('indexed', 'equalto', true) %}
      def get_by_{{ field.name }}(self, {{ field.name }}: {{ field.type }}) -> Optional[{{ entity.name }}Model]:
          """Get {{ entity.name }} by {{ field.name }}."""
          return self.session.query({{ entity.name }}Model).filter(
              {{ entity.name }}Model.{{ field.name }} == {{ field.name }}
          ).first()
      {% endfor %}
      ```
    - Método `search()` si hay campos string:
      ```jinja2
      {% set string_fields = entity.fields | selectattr('type', 'in', ['str', 'text']) | list %}
      {% if string_fields %}
      def search(self, query: str, skip: int = 0, limit: int = 100) -> List[{{ entity.name }}Model]:
          """Search {{ entity.name }} by text fields."""
          filters = [
              {% for field in string_fields %}
              {{ entity.name }}Model.{{ field.name }}.ilike(f"%{query}%"),
              {% endfor %}
          ]
          return self.session.query({{ entity.name }}Model).filter(
              or_(*filters)
          ).offset(skip).limit(limit).all()
      {% endif %}
      ```

### Task 6: Crear template service.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/service.py.j2`
- Template debe generar:
  - Imports:
    - `from {{ config.project.package_name }}.shared.services.base_service import BaseService`
    - `from .domain import {{ entity.name }}`
    - `from .schemas import {{ entity.name }}Create, {{ entity.name }}Update, {{ entity.name }}Response`
    - `from .repository import {{ entity.name }}Repository`
    - `from typing import List, Optional`
  - `class {{ entity.name }}Service(BaseService[{{ entity.name }}, {{ entity.name }}Create, {{ entity.name }}Update])`:
    - Docstring
    - Constructor:
      ```python
      def __init__(self, repository: {{ entity.name }}Repository):
          super().__init__(repository)
          self.repository = repository
      ```
    - Métodos placeholder con docstrings:
      ```python
      def apply_business_rules(self, entity: {{ entity.name }}) -> {{ entity.name }}:
          """Apply business rules before saving."""
          entity.validate()
          entity.calculate_totals()
          return entity
      ```

### Task 7: Crear template routes.py.j2
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/routes.py.j2`
- Template debe generar:
  - Imports:
    - `from fastapi import APIRouter, Depends, HTTPException, status`
    - `from {{ config.project.package_name }}.shared.dependencies import get_db`
    - `from .schemas import {{ entity.name }}Create, {{ entity.name }}Update, {{ entity.name }}Response`
    - `from .service import {{ entity.name }}Service`
    - `from .repository import {{ entity.name }}Repository`
    - `from typing import List`
  - Router:
    ```python
    router = APIRouter(prefix="/{{ entity.plural_name }}", tags=["{{ entity.plural_name }}"])
    ```
  - Endpoints:
    - `POST /{{ entity.plural_name }}/` → create (status 201)
    - `GET /{{ entity.plural_name }}/{id}` → get_by_id (status 200)
    - `GET /{{ entity.plural_name }}/` → list con paginación (query params: skip, limit)
    - `PUT /{{ entity.plural_name }}/{id}` → update (status 200)
    - `DELETE /{{ entity.plural_name }}/{id}` → soft_delete (status 200)
  - Usar FastAPI's automatic validation (422 responses)
  - No incluir auth decorators (endpoints sin protección)

### Task 8: Crear tests para templates
- Crear `tac_bootstrap_cli/tests/test_crud_templates.py`
- Fixtures:
  - `@pytest.fixture entity_spec()` → EntitySpec de ejemplo con 4-5 campos de tipos variados
  - `@pytest.fixture tac_config()` → TACConfig básico
  - `@pytest.fixture template_repo()` → TemplateRepository
- Tests por template:
  - `test_domain_entity_renders(template_repo, entity_spec, tac_config)`
    - Renderizar template con entity y config
    - Verificar que contiene `class {{ entity.name }}(Entity)`
    - Verificar que tiene los campos definidos
    - Compilar para validar sintaxis: `compile(output, '<string>', 'exec')`
  - `test_schemas_renders(template_repo, entity_spec, tac_config)`
    - Verificar que contiene Create, Update, Response classes
    - Verificar herencia de Base classes
  - `test_orm_model_renders(template_repo, entity_spec, tac_config)`
    - Verificar `__tablename__`
    - Verificar que columnas mapean correctamente desde FieldSpec
  - `test_repository_renders(template_repo, entity_spec, tac_config)`
    - Verificar BaseRepository herencia
    - Verificar métodos condicionales (get_by_X para indexed fields)
  - `test_service_renders(template_repo, entity_spec, tac_config)`
    - Verificar BaseService herencia con generics
  - `test_routes_renders(template_repo, entity_spec, tac_config)`
    - Verificar router definition
    - Verificar 5 endpoints CRUD

### Task 9: Ejecutar validation commands
- Ejecutar todos los comandos de validación:
  - `cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py -v --tb=short`
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Si hay errores, corregirlos antes de continuar
- Confirmar que todos los tests pasan

## Testing Strategy

### Unit Tests

Cada template debe tener al menos 2 tests:
1. Test de renderizado básico - verifica que genera Python válido
2. Test de contenido - verifica que contiene elementos estructurales esperados

Tests adicionales para casos especiales:
- Template con campos indexados → verifica generación de métodos get_by_X
- Template con campos string → verifica generación de método search()
- Template con campos nullable → verifica `| None` en tipos
- Template con max_length → verifica Field(..., max_length=X)

### Edge Cases

- EntitySpec sin campos adicionales (solo los heredados de Entity)
- EntitySpec con todos los tipos de FieldType
- EntitySpec con campos nullable=True
- EntitySpec con campos indexed=True
- EntitySpec con campos con max_length
- EntitySpec con campos con default values
- Nombres de entidades con caracteres especiales (sanitización en snake_name, plural_name)

## Acceptance Criteria

- [x] Directorio `tac_bootstrap_cli/tac_bootstrap/templates/capabilities/crud_basic/` creado
- [x] 6 templates creados (domain_entity, schemas, orm_model, repository, service, routes)
- [x] Cada template renderiza Python sintácticamente válido
- [x] EntitySpec con 5 campos de tipos variados renderiza correctamente en todos los templates
- [x] Imports entre archivos son correctos:
  - domain_entity importa de shared.domain.base_entity
  - schemas importa de shared.schemas.base_schema
  - orm_model importa de shared.database o define Base
  - repository importa de shared.repositories.base_repository
  - service importa de shared.services.base_service
  - routes importa de shared.dependencies
- [x] Mapeo de FieldType a tipos SQLAlchemy es correcto:
  - str → String(max_length)
  - int → Integer
  - float → Float
  - bool → Boolean
  - datetime → DateTime(timezone=True)
  - uuid → String(36)
  - text → Text
  - decimal → Numeric
  - json → JSON
- [x] Repository genera métodos condicionales get_by_X solo para campos indexed=True
- [x] Repository genera método search() solo si hay campos string/text
- [x] ORM model genera indexes solo para campos indexed=True
- [x] Schemas manejan nullable correctamente (Optional en Update, required en Create)
- [x] Routes generan 5 endpoints CRUD con status codes correctos
- [x] Todos los tests en `tests/test_crud_templates.py` pasan
- [x] `uv run pytest tests/ -v --tb=short` pasa sin errores
- [x] `uv run ruff check .` pasa sin errores
- [x] `uv run mypy tac_bootstrap/` pasa sin errores

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_crud_templates.py -v --tb=short` - Tests de templates CRUD
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Suite completa de tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test del CLI

## Notes

**Decisiones de diseño**:

1. **Imports relativos vs absolutos**: Usar imports relativos (`.domain`, `.schemas`) dentro del módulo generado para que sea portable. Imports absolutos con `{{ config.project.package_name }}` solo para shared infrastructure.

2. **Base classes**: Todos los templates asumen que base classes existen en `shared/`. El CLI debe validar que shared/ está presente antes de generar entidades.

3. **Type hints**: Usar type hints completos en todos los templates. Los tipos importados (UUID, datetime, Decimal) deben estar en los imports del template.

4. **Docstrings**: Docstrings mínimas en formato Google style. Solo para clases y métodos públicos. Métodos privados/internos no requieren docstrings.

5. **Validation**: FastAPI maneja validación Pydantic automáticamente (422 responses). No incluir try-catch en routes templates.

6. **Auth**: Routes sin decoradores de auth. Auth es cross-cutting y se agrega globalmente o por proyecto.

7. **Transactions**: Service templates no incluyen `@transactional`. BaseService maneja transacciones internamente.

8. **Soft delete**: Usar `BaseRepository.soft_delete()` que marca `deleted_at` timestamp en lugar de eliminar físicamente.

9. **Pagination**: GET /entities/ usa simple limit/offset con query params `skip` y `limit`.

10. **Conditional generation**: Repository methods (get_by_X, search) se generan condicionalmente basados en propiedades de campos (indexed, type). Esto hace el código generado más útil y específico a la entidad.

**Dependencias nuevas**: Ninguna. Los templates usan solo las librerías ya declaradas en pyproject.toml (Jinja2, Pydantic, SQLAlchemy, FastAPI).

**Siguientes pasos después de esta feature**:
- Tarea 2.3: GenerateService que orquesta la generación usando estos templates
- Tarea 2.4: Comando CLI `tac-bootstrap generate entity` que invoca GenerateService
- Tarea 2.5: Entity wizard interactivo que construye EntitySpec desde prompts
