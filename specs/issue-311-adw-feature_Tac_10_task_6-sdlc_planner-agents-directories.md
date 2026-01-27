# Feature: Crear directorios para agents/hook_logs y agents/context_bundles

## Metadata
issue_number: `311`
adw_id: `feature_Tac_10_task_6`
issue_json: `{"number":311,"title":"Actualizar scaffold_service.py para crear directorios de agents","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_6\n\n- **Descripción**: Modificar el servicio de scaffolding para crear los directorios necesarios para logs de hooks y context bundles.\n- **Archivo**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n- **Cambios**:\n  - En la función `build_plan()`, agregar DirectoryOperation para `agents/hook_logs/`\n  - Agregar DirectoryOperation para `agents/context_bundles/`\n  - Agregar .gitkeep files en ambos directorios\n\n\n"}`

## Feature Description

Agregar soporte en el scaffolding para crear directorios dedicados para almacenar logs de hooks y context bundles generados por agents. Estos directorios son necesarios para que los hooks y agents puedan persistir información durante su ejecución. Los directorios deben crearse automáticamente al generar un nuevo proyecto con TAC Bootstrap.

## User Story

As a developer using TAC Bootstrap
I want the scaffold to create agents/hook_logs/ and agents/context_bundles/ directories automatically
So that hooks and agents can persist logs and context information without runtime errors

## Problem Statement

Actualmente, el scaffold_service crea un directorio `agents/` (línea 119 del archivo scaffold_service.py), pero no crea los subdirectorios necesarios para organizar los archivos que generan los hooks y agents durante su ejecución. Esto puede causar errores cuando los hooks intenten escribir logs o cuando los agents intenten guardar context bundles, ya que los directorios padres no existen.

## Solution Statement

Modificar `scaffold_service.py` para agregar dos DirectoryOperation adicionales en la función `build_plan()`:
- `agents/hook_logs/` - para almacenar logs de hooks
- `agents/context_bundles/` - para almacenar bundles de contexto

Además, agregar archivos `.gitkeep` vacíos en ambos subdirectorios para asegurar que Git rastree estas carpetas incluso cuando estén vacías. Esto sigue la convención estándar de Git y el patrón existente en el proyecto.

## Relevant Files

Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Servicio principal donde se agregaran las operaciones de directorio (línea 104-127, función `_add_directories`)
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Define las clases DirectoryOperation y FileOperation que se usarán
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests existentes que validarán el comportamiento

### New Files

No se crearán archivos nuevos, solo se modificará scaffold_service.py.

## Implementation Plan

### Phase 1: Foundation
No requiere trabajo fundacional, ya que:
- La clase DirectoryOperation existe y está probada
- El patrón para agregar directorios está establecido en `_add_directories()`
- La infraestructura de filesystem existe

### Phase 2: Core Implementation
Modificar la función `_add_directories()` en scaffold_service.py para agregar:
1. DirectoryOperation para `agents/hook_logs/`
2. DirectoryOperation para `agents/context_bundles/`
3. FileOperation para `agents/hook_logs/.gitkeep` (archivo vacío)
4. FileOperation para `agents/context_bundles/.gitkeep` (archivo vacío)

### Phase 3: Integration
Validar que:
- Los directorios se crean correctamente en el filesystem
- Los archivos .gitkeep se crean vacíos
- Los tests existentes pasan sin regresiones
- El contador de directorios y archivos en ApplyResult es correcto

## Step by Step Tasks

### Task 1: Modificar _add_directories() para agregar subdirectorios de agents
- Ubicar la línea 119 en scaffold_service.py donde se agrega el directorio "agents"
- Después de esa línea, agregar dos tuplas adicionales a la lista `directories`:
  - `("agents/hook_logs", "Hook execution logs")`
  - `("agents/context_bundles", "Agent context bundles")`
- Estos seguirán el mismo patrón que los demás directorios

### Task 2: Agregar archivos .gitkeep en los subdirectorios
- Después de la sección de directorios en `build_plan()`, agregar dos llamadas a `plan.add_file()`:
  - `plan.add_file("agents/hook_logs/.gitkeep", action=FileAction.CREATE, content="", reason="Keep empty directory in Git")`
  - `plan.add_file("agents/context_bundles/.gitkeep", action=FileAction.CREATE, content="", reason="Keep empty directory in Git")`
- Usar `FileAction.CREATE` para evitar sobrescribir si ya existen

### Task 3: Ejecutar tests y validación
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v`
- Ejecutar todos los Validation Commands listados abajo
- Verificar que no hay regresiones
- Verificar que los nuevos directorios aparecen en el plan

## Testing Strategy

### Unit Tests

Los tests existentes en test_scaffold_service.py ya validan:
- Que `build_plan()` retorna un ScaffoldPlan válido
- Que los directorios se cuentan correctamente
- Que `apply_plan()` crea los directorios en el filesystem

No se requieren nuevos tests específicos, pero debemos verificar:
- `plan.total_directories` incrementa en 2 (de ~15 a ~17)
- `plan.total_files` incrementa en 2 por los .gitkeep
- Los directorios aparecen en `plan.directories`

### Edge Cases

1. **Directorio agents/ ya existe**: DirectoryOperation es idempotente, no debe fallar
2. **Archivos .gitkeep ya existen**: FileAction.CREATE los omite sin error
3. **Permisos del filesystem**: Usar permisos por defecto del sistema operativo
4. **Git tracking**: Los .gitkeep vacíos fuerzan a Git a trackear carpetas vacías

## Acceptance Criteria

- [ ] Los directorios `agents/hook_logs/` y `agents/context_bundles/` se agregan al ScaffoldPlan
- [ ] Los archivos `.gitkeep` vacíos se agregan en ambos subdirectorios
- [ ] Cuando se ejecuta `apply_plan()`, los directorios se crean en el filesystem
- [ ] Los archivos .gitkeep se crean vacíos (0 bytes)
- [ ] Todos los tests existentes pasan sin regresiones
- [ ] El contador `directories_created` en ApplyResult se incrementa correctamente
- [ ] El contador `files_created` en ApplyResult incluye los .gitkeep
- [ ] El código sigue el estilo y patrones existentes en scaffold_service.py

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- Esta feature es parte de TAC-10 que agrega soporte para agents en proyectos generados
- Los directorios siguen la estructura jerárquica: `agents/` como padre, con `hook_logs/` y `context_bundles/` como hijos
- Los .gitkeep son archivos vacíos estándar en Git para preservar directorios vacíos
- No se requiere lógica condicional: estos directorios se crean para todos los proyectos
- La implementación debe ser compatible con el sistema de permisos existente en FileSystem
- DirectoryOperation ya maneja idempotencia (no falla si el directorio existe)
