# Feature: Template base_entity.py

## Metadata
issue_number: `111`
adw_id: `a1a5289c`
issue_json: `{"number":111,"title":"Tarea 1.1: Template base_entity.py","body":"/feature\n/adw_sdlc_zte_iso.py\n**Ganancia**: Todas las entidades del proyecto heredan de una clase base con audit trail, soft delete, state management y versionado optimista. Evita repetir 50+ lineas por entidad.\n\n**Instrucciones para el agente**:\n\n1. Crear el template Jinja2: `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2`\n2. Crear el archivo renderizado en raiz: `src/shared/domain/base_entity.py` (renderizado con valores de este proyecto)\n3. El archivo en raiz debe ser el resultado de renderizar el template con `config.project.name = \"tac_bootstrap\"`\n2. El template debe generar una clase `Entity` con los siguientes campos:\n   - `id: str` (UUID generado automaticamente)\n   - `state: int` (0=inactive, 1=active, 2=deleted, default=1)\n   - `version: int` (para optimistic locking, default=1)\n   - `created_at: datetime` (auto-set en creacion)\n   - `created_by: str | None`\n   - `updated_at: datetime` (auto-set en cada update)\n   - `updated_by: str | None`\n   - `organization_id: str | None` (multi-tenancy opcional)\n   - `type_discriminator: str` (para herencia de entidades)\n3. Metodos requeridos:\n   - `activate()` → state=1\n   - `deactivate()` → state=0\n   - `soft_delete()` → state=2\n   - `restore()` → state=1\n   - `is_active` → property bool\n   - `is_deleted` → property bool\n4. Usar Pydantic BaseModel como base\n5. Variables Jinja2 disponibles: `{{ config.project.name }}`\n\n**Criterios de aceptacion**:\n- El archivo renderiza sin errores con un config basico\n- La clase generada es importable sin errores de sintaxis\n- Los metodos de estado transicionan correctamente\n- Incluye docstring con patron IDK\n- Incluye docuemtacion adcional : /tac_bootstrap/ai_docs/doc/create-crud-entity"}`

## Feature Description
Crear un template Jinja2 que genere la clase base `Entity` para todos los modelos de dominio en proyectos generados por TAC Bootstrap. Esta clase base proporciona funcionalidad común de audit trail, soft delete, state management y versionado optimista, evitando repetir código en cada entidad.

El template seguirá el patrón de referencia documentado en `ai_docs/doc/create-crud-entity/shared/base_entity.py.md` y será renderizado tanto como template (`.j2`) como archivo concreto para uso en este proyecto.

## User Story
As a developer using TAC Bootstrap
I want to have a base Entity class with comprehensive audit and lifecycle functionality
So that I can create domain entities without repeating 50+ lines of boilerplate code per entity

## Problem Statement
Cada entidad de dominio requiere campos comunes para:
- Identidad única (UUID)
- Audit trail (created_at, created_by, updated_at, updated_by)
- Soft delete (state management)
- Versionado optimista (version field)
- Multi-tenancy (organization_id, project_id)
- Metadata de negocio (code, name, description, type)

Sin una clase base, estos campos y métodos se repiten en cada entidad, generando:
- Inconsistencias en implementación
- Mayor superficie de bugs
- Dificultad de mantenimiento
- Violación del principio DRY

## Solution Statement
Crear un template Jinja2 (`base_entity.py.j2`) que genere una clase `Entity` con:
1. Todos los campos de audit trail y metadata
2. Enum `EntityState` para state management
3. Métodos de lifecycle (activate, deactivate, delete)
4. Query methods (is_active, is_deleted, is_inactive)
5. Version tracking con `mark_updated()`
6. Docstrings completos con patrón IDK

El template seguirá la implementación de referencia en `ai_docs/doc/create-crud-entity/shared/base_entity.py.md` (~400 líneas) y será renderizado para uso en el proyecto tac_bootstrap.

## Relevant Files
Archivos necesarios para implementar la feature:

- `ai_docs/doc/create-crud-entity/shared/base_entity.py.md` - Implementación de referencia completa
- `ai_docs/doc/create-crud-entity/DOCUMENTATION_STANDARDS.md` - Estándares de docstrings IDK
- `tac_bootstrap_cli/tac_bootstrap/templates/` - Directorio de templates existentes
- `config.yml` - Configuración del proyecto (config.project.name = "tac_bootstrap")

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2` - Template Jinja2
- `src/shared/__init__.py` - Package init para shared kernel
- `src/shared/domain/__init__.py` - Package init para domain models
- `src/shared/domain/base_entity.py` - Archivo renderizado del template

## Implementation Plan

### Phase 1: Foundation
1. Crear estructura de directorios para templates shared
2. Crear estructura de directorios para src/shared/domain

### Phase 2: Core Implementation
1. Crear template `base_entity.py.j2` siguiendo la referencia completa
2. Incluir EntityState IntEnum
3. Incluir Entity class con todos los campos de la referencia
4. Incluir todos los métodos de lifecycle y query methods
5. Agregar docstrings IDK completos

### Phase 3: Integration
1. Renderizar el template para uso en tac_bootstrap (src/shared/domain/base_entity.py)
2. Crear archivos __init__.py necesarios
3. Validar que el archivo renderizado es importable sin errores
4. Verificar que los métodos de state transition funcionan correctamente

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear estructura de directorios para templates
- Crear directorio `tac_bootstrap_cli/tac_bootstrap/templates/shared/`
- Verificar que el directorio existe

### Task 2: Crear estructura de directorios para src/shared/domain
- Crear directorio `src/shared/domain/` con todos los padres necesarios
- Crear `src/shared/__init__.py` con docstring básico
- Crear `src/shared/domain/__init__.py` preparado para exportar Entity y EntityState

### Task 3: Crear template base_entity.py.j2
- Leer el archivo de referencia `ai_docs/doc/create-crud-entity/shared/base_entity.py.md`
- Crear `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2`
- Copiar la implementación completa de la referencia (lines 7-396)
- El template NO necesita parametrización Jinja2 - es un template estático que se copia tal cual
- Incluir EntityState IntEnum completo
- Incluir Entity class con todos los campos:
  - id, code, name, description, type
  - created_at, created_by, updated_at, updated_by
  - state, status, version
  - organization_id, project_id, owner
- Incluir todos los métodos:
  - sync_updated_at validator
  - mark_updated(), deactivate(), activate(), delete()
  - is_active(), is_deleted(), is_inactive()
  - __str__(), __repr__()
- Todos los docstrings con patrón IDK completo

### Task 4: Renderizar template para uso en tac_bootstrap
- Crear directorio `src/shared/domain/` si no existe
- Copiar el contenido del template a `src/shared/domain/base_entity.py`
- Como el template es estático (sin variables Jinja2), simplemente copiar el contenido

### Task 5: Actualizar __init__.py files
- Actualizar `src/shared/__init__.py` con docstring apropiado
- Actualizar `src/shared/domain/__init__.py` para exportar Entity y EntityState:
  ```python
  """Shared domain models."""
  from .base_entity import Entity, EntityState

  __all__ = ["Entity", "EntityState"]
  ```

### Task 6: Validación
- Verificar que `src/shared/domain/base_entity.py` es importable:
  ```python
  from src.shared.domain.base_entity import Entity, EntityState
  ```
- Crear un test rápido de state transitions:
  ```python
  entity = Entity(code="TEST-001", name="Test Entity")
  assert entity.is_active()
  entity.deactivate()
  assert entity.is_inactive()
  entity.activate()
  assert entity.is_active()
  entity.delete()
  assert entity.is_deleted()
  ```
- Verificar que el template renderiza sin errores

### Task 7: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo

## Testing Strategy

### Unit Tests
No se requieren tests unitarios formales en esta tarea. La validación se hará mediante:
1. Importación exitosa del módulo
2. Test manual de state transitions
3. Verificación de sintaxis con linting/type checking

### Edge Cases
- Entity con valores mínimos requeridos (solo code y name)
- Entity con todos los campos opcionales poblados
- Llamadas idempotentes (activate() en entity ya activa, delete() en entity ya deleted)
- Version increment en mark_updated()

## Acceptance Criteria
1. ✅ Existe `tac_bootstrap_cli/tac_bootstrap/templates/shared/base_entity.py.j2`
2. ✅ Existe `src/shared/domain/base_entity.py` (archivo renderizado)
3. ✅ El archivo renderizado es importable sin errores de sintaxis
4. ✅ Los métodos de estado transicionan correctamente (activate, deactivate, delete)
5. ✅ Todos los docstrings usan patrón IDK
6. ✅ EntityState IntEnum está presente con valores 0, 1, 2
7. ✅ Entity class tiene todos los campos de la referencia (id, code, name, description, type, audit fields, etc.)
8. ✅ mark_updated() incrementa version correctamente
9. ✅ El template sigue exactamente la implementación de referencia en base_entity.py.md
10. ✅ Pasa todos los Validation Commands con cero errores

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `python -c "from src.shared.domain.base_entity import Entity, EntityState; print('Import successful')"` - Import validation

## Notes
- El template es prácticamente estático - copia la referencia tal cual sin parametrización
- Esto es "dogfooding" - tac_bootstrap usa sus propios templates
- La implementación de referencia tiene ~400 líneas - no omitir ninguna parte
- El campo se llama `type` (no `type_discriminator`) según la referencia
- Todos los métodos de lifecycle aceptan `user_id: str | None = None`
- ConfigDict debe tener `validate_assignment=True` para validar mutaciones
- El archivo renderizado sirve tanto de validación como de uso real en tac_bootstrap
