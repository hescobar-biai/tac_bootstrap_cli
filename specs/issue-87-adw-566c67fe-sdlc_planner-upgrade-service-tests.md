# Feature: Crear tests comprehensivos para UpgradeService

## Metadata
issue_number: `87`
adw_id: `566c67fe`
issue_json: `{"number":87,"title":"TAREA 6: Crear tests para UpgradeService","body":"**Archivo**: tac_bootstrap_cli/tests/test_upgrade_service.py\n\n**Descripción**: Tests comprehensivos para el servicio de upgrade.\n\n**Código**: [contenido del issue completo]"}`

## Feature Description
Crear una suite comprehensiva de tests unitarios para el `UpgradeService` que validen todos los casos principales, edge cases, y comportamientos de error del servicio de upgrade. Los tests deben:

1. Validar la detección correcta de versiones actuales y target
2. Verificar la creación de backups y exclusión de código de usuario
3. Probar la lógica de comparación de versiones
4. Validar que el upgrade preserva código de usuario mientras actualiza Agentic Layer
5. Probar rollback desde backup cuando el upgrade falla
6. Cubrir edge cases como proyectos sin campo version, config corrupto, etc.
7. Verificar que config.yml se actualiza con la nueva versión después del upgrade

Este es un requisito crítico (TAREA 6) para asegurar la confiabilidad del upgrade system antes del release.

## User Story
As a TAC Bootstrap CLI developer
I want comprehensive unit tests for UpgradeService
So that I can ensure the upgrade functionality works correctly and safely in all scenarios without risking user data loss

## Problem Statement
El `UpgradeService` implementado en TAREA 3 es una funcionalidad crítica que modifica proyectos existentes de usuarios. Sin tests comprehensivos:

- No hay garantía de que el upgrade preserve correctamente código de usuario
- Los edge cases (proyectos sin version field, configs corruptos) pueden causar fallos en producción
- El rollback desde backup puede no funcionar correctamente si hay bugs
- Cambios futuros pueden romper funcionalidad existente sin detección
- La actualización de config.yml con nueva version puede no ejecutarse correctamente

Los tests deben cubrir tanto happy paths como edge cases identificados en las clarificaciones del issue.

## Solution Statement
Implementar `test_upgrade_service.py` con dos clases de tests:

1. **TestUpgradeService**: Tests principales para happy paths y funcionalidad core
   - Detección de versiones (con y sin campo version)
   - Comparación de versiones
   - Creación de backups con exclusión correcta de directorios
   - Preview de cambios
   - Carga de configuración existente
   - Upgrade exitoso preservando código de usuario
   - Verificación crítica de actualización de config.yml

2. **TestUpgradeServiceEdgeCases**: Tests para casos especiales
   - Config.yml inválido o corrupto
   - Directorios faltantes
   - Fallo durante el upgrade con rollback
   - Fallo en creación de backup
   - Eliminación de archivos viejos

Los tests usarán:
- `pytest` fixtures para crear proyectos mock con `tmp_path`
- `unittest.mock.patch` para mockear ScaffoldService y evitar I/O real
- Aserciones explícitas para verificar comportamientos críticos
- YAML real para simular config.yml de diferentes versiones

## Relevant Files
Archivos existentes necesarios:

- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - El servicio a testear (creado en TAREA 3)
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Para importar `__version__`
- `tac_bootstrap_cli/tests/test_upgrade_cli.py` - Tests CLI existentes como referencia de patrones
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests existentes como referencia de fixtures y mocking patterns
- `tac_bootstrap_cli/pyproject.toml` - Configuración de pytest

### New Files
- `tac_bootstrap_cli/tests/test_upgrade_service.py` - Suite completa de tests unitarios

## Implementation Plan

### Phase 1: Foundation
Crear el archivo de tests con imports, fixtures reutilizables, y estructura básica de clases.

### Phase 2: Core Implementation
Implementar tests principales para funcionalidad core del UpgradeService.

### Phase 3: Edge Cases & Critical Tests
Agregar tests críticos identificados en las clarificaciones (actualización de version, rollback, backup failures).

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo con estructura básica y fixture principal
- Crear `tac_bootstrap_cli/tests/test_upgrade_service.py`
- Agregar docstring del módulo
- Agregar imports necesarios:
  - `pytest`, `pathlib.Path`, `unittest.mock` (patch, MagicMock)
  - `yaml`, `shutil`
  - `tac_bootstrap.application.upgrade_service.UpgradeService`
  - `tac_bootstrap.__version__`
- Crear fixture `mock_project(tmp_path)` que:
  - Crea config.yml con version "0.1.0" y configuración completa
  - Crea directorios `adws/`, `.claude/`, `scripts/` con archivos dummy
  - Crea directorio `src/` con código de usuario (main.py)
  - Retorna el `tmp_path`

### Task 2: Implementar tests de detección de versión
Crear clase `TestUpgradeService` con tests:
- `test_get_current_version` - Verifica lectura correcta desde config.yml
- `test_get_current_version_missing_file` - Retorna None si no existe config.yml
- `test_get_current_version_no_version_field` - Retorna "0.1.0" para proyectos pre-0.2.0 sin campo version
- `test_needs_upgrade_true` - Detecta cuando upgrade es necesario
- `test_needs_upgrade_false_same_version` - Detecta cuando ya está actualizado

### Task 3: Implementar tests de backup
- `test_create_backup` - Verifica que backup incluye adws/, .claude/, scripts/, config.yml
- Verificar que backup NO incluye src/ (código de usuario)
- Verificar que backup existe en `.tac-backup-{timestamp}/`

### Task 4: Implementar tests de preview y config loading
- `test_get_changes_preview` - Verifica lista de cambios a aplicar
- `test_load_existing_config` - Verifica carga y actualización de version a target

### Task 5: Implementar tests de upgrade exitoso
- `test_perform_upgrade_preserves_user_code` - Mock scaffold_service, verificar que src/main.py persiste
- `test_perform_upgrade_with_backup` - Verificar que backup se crea
- **CRÍTICO**: `test_perform_upgrade_updates_config_version` - Verificar que config.yml tiene version == __version__ después del upgrade

### Task 6: Implementar clase TestUpgradeServiceEdgeCases
- `test_upgrade_invalid_config` - Config.yml corrupto retorna None en load_existing_config
- `test_upgrade_missing_directories` - Muestra "Create" en preview para directorios faltantes
- **CRÍTICO**: `test_perform_upgrade_rollback_on_failure` - Mock scaffold_project para que lance excepción, verificar restauración desde backup
- **CRÍTICO**: `test_perform_upgrade_aborts_on_backup_failure` - Mock create_backup para que falle, verificar que upgrade aborta
- `test_perform_upgrade_removes_old_files` - Crear archivo dummy en adws/, verificar que no existe después del upgrade

### Task 7: Verificar argumentos pasados a scaffold_service
- En tests con mocks, agregar verificaciones de que scaffold_project fue llamado correctamente
- Usar `assert_called_with` o verificar `call_args` para validar TACConfig pasado

### Task 8: Ejecutar validation commands
- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v --tb=short`
- Verificar que TODOS los tests pasan (mínimo 15 tests)
- Ejecutar `uv run ruff check .` para linting
- Ejecutar `uv run mypy tac_bootstrap/` para type checking

## Testing Strategy

### Unit Tests
Tests unitarios puros usando mocks para evitar I/O real del ScaffoldService:

1. **Detección de versión**:
   - Con version field en config.yml
   - Sin version field (default 0.1.0)
   - Config.yml inexistente
   - Config.yml corrupto

2. **Comparación de versiones**:
   - Current < Target → needs_upgrade = True
   - Current == Target → needs_upgrade = False

3. **Backup**:
   - Creación exitosa con timestamp
   - Inclusión de directorios correctos
   - Exclusión de código de usuario

4. **Upgrade exitoso**:
   - Preservación de código de usuario
   - Actualización de config.yml version (CRÍTICO)
   - Regeneración de Agentic Layer
   - Creación de backup

5. **Rollback**:
   - Restauración cuando scaffold falla
   - Abort cuando backup falla

### Edge Cases
Casos especiales identificados en clarificaciones:

1. **Proyecto sin campo version**: Debe asumir "0.1.0"
2. **Config.yml corrupto**: load_existing_config retorna None
3. **Directorios faltantes**: Preview muestra "Create" en lugar de "Update"
4. **Scaffold lanza excepción**: Trigger rollback desde backup
5. **Backup falla**: Abort upgrade sin proceder
6. **Archivos viejos**: Eliminados durante upgrade (verificar que adws/old_file.py desaparece)

## Acceptance Criteria
- [ ] Tests cubren casos principales (version detection, needs_upgrade, backup, upgrade, config loading)
- [ ] Tests cubren edge cases (no version field, corrupt config, missing dirs, failures)
- [ ] Test CRÍTICO `test_perform_upgrade_updates_config_version` implementado y pasando
- [ ] Tests de backup verifican exclusión de código de usuario (src/ no en backup)
- [ ] Tests de preservación de código usuario verifican que src/main.py persiste después de upgrade
- [ ] Test de rollback verifica restauración cuando scaffold_project falla
- [ ] Test de abort verifica que upgrade no procede si create_backup falla
- [ ] Test de eliminación de archivos viejos verifica que adws/old_file.py desaparece
- [ ] Todos los tests pasan con pytest (mínimo 15 tests)
- [ ] Coverage de métodos principales: get_current_version, needs_upgrade, create_backup, load_existing_config, perform_upgrade, get_changes_preview
- [ ] Tests usan mocks apropiadamente para evitar I/O real del scaffold_service
- [ ] Tests usan tmp_path para filesystem operations seguras

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v --tb=short` - Tests unitarios del UpgradeService
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Todos los tests del proyecto
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py --cov=tac_bootstrap.application.upgrade_service` - Coverage report (opcional)

## Notes

### Clarificaciones importantes del issue:

**🔴 Crítico - Tests requeridos**:
1. `test_perform_upgrade_updates_config_version` - Verificar que config.yml tiene version == __version__ después del upgrade
2. `test_perform_upgrade_rollback_on_failure` - Mock scaffold para que falle, verificar restauración desde backup
3. `test_perform_upgrade_aborts_on_backup_failure` - Verificar que upgrade aborta si backup falla

**🟡 Importante**:
- Test de preservación de código usuario solo debe verificar que src/main.py existe y tiene contenido correcto
- Test de backup debe verificar que src/ NO está en el backup
- Test de eliminación de archivos viejos debe crear dummy file en adws/ y verificar que desaparece
- Mocks de scaffold_project impiden verificar templates reales (suficiente para unit tests)

**🟢 Fuera de scope para MVP**:
- Upgrades concurrentes (no manejado)
- Espacio en disco insuficiente (OSError será capturado)
- Permisos del backup (shutil.copytree los preserva automáticamente)
- Colisión de nombres de backup (timestamp incluye segundos, improbable)

### Patrón de testing:
Seguir patrones existentes en `test_scaffold_service.py` y `test_upgrade_cli.py`:
- Usar fixtures de pytest para setup
- Usar `tmp_path` para operaciones de filesystem
- Usar `unittest.mock.patch` para mockear dependencias externas
- Usar aserciones explícitas y descriptivas
- Agrupar tests relacionados en clases

### Relación con otras tareas:
- TAREA 3: UpgradeService implementation (prerequisito)
- TAREA 4: CLI upgrade command (usa este servicio)
- TAREA 5: Tests CLI upgrade (testa la integración CLI-Service)
- TAREA 7: Tests de integración e2e (validará comportamiento real end-to-end)
