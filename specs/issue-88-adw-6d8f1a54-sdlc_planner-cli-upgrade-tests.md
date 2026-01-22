# Feature: Crear tests de integración para comando CLI upgrade

## Metadata
issue_number: `88`
adw_id: `6d8f1a54`
issue_json: `{"number":88,"title":"TAREA 7: Crear tests para comando CLI upgrade","body":"**Archivo**: `tac_bootstrap_cli/tests/test_cli_upgrade.py`\n\n**Descripción**: Tests de integración para el comando CLI.\n\n**Código**:\n\n```python\n\"\"\"Tests for CLI upgrade command.\"\"\"\n\nimport pytest\nfrom pathlib import Path\nfrom typer.testing import CliRunner\nfrom unittest.mock import patch, MagicMock\nimport yaml\n\nfrom tac_bootstrap.interfaces.cli import app\nfrom tac_bootstrap import __version__\n\n\nrunner = CliRunner()\n\n\n@pytest.fixture\ndef mock_project(tmp_path):\n    \"\"\"Create mock project for CLI tests.\"\"\"\n    config = {\n        \"version\": \"0.1.0\",\n        \"project\": {\"name\": \"test\", \"mode\": \"new\", \"language\": \"python\",\n                   \"framework\": \"none\", \"architecture\": \"simple\",\n                   \"package_manager\": \"uv\"},\n        \"paths\": {\"app_root\": \".\"},\n        \"commands\": {\"start\": \"\", \"test\": \"\"},\n        \"agentic\": {\"target_branch\": \"main\", \"worktrees\": {\"enabled\": False}},\n        \"claude\": {\"settings\": {\"project_name\": \"test\"}},\n    }\n    with open(tmp_path / \"config.yml\", \"w\") as f:\n        yaml.dump(config, f)\n\n    (tmp_path / \"adws\").mkdir()\n    (tmp_path / \".claude\").mkdir()\n\n    return tmp_path\n\n\nclass TestCliUpgrade:\n    \"\"\"Tests for tac upgrade command.\"\"\"\n\n    def test_upgrade_dry_run(self, mock_project):\n        \"\"\"Test --dry-run shows changes without applying.\"\"\"\n        result = runner.invoke(app, [\"upgrade\", str(mock_project), \"--dry-run\"])\n\n        assert result.exit_code == 0\n        assert \"Dry run\" in result.stdout\n        assert \"no changes made\" in result.stdout\n\n    def test_upgrade_no_config(self, tmp_path):\n        \"\"\"Test error when no config.yml exists.\"\"\"\n        result = runner.invoke(app, [\"upgrade\", str(tmp_path)])\n\n        assert result.exit_code == 1\n        assert \"No config.yml found\" in result.stdout\n\n    def test_upgrade_already_current(self, mock_project):\n        \"\"\"Test when project is already up to date.\"\"\"\n        # Update to current version\n        config_path = mock_project / \"config.yml\"\n        with open(config_path) as f:\n            config = yaml.safe_load(f)\n        config[\"version\"] = __version__\n        with open(config_path, \"w\") as f:\n            yaml.dump(config, f)\n\n        result = runner.invoke(app, [\"upgrade\", str(mock_project)])\n\n        assert result.exit_code == 0\n        assert \"already up to date\" in result.stdout\n\n    def test_upgrade_force(self, mock_project):\n        \"\"\"Test --force upgrades even when current.\"\"\"\n        # Update to current version\n        config_path = mock_project / \"config.yml\"\n        with open(config_path) as f:\n            config = yaml.safe_load(f)\n        config[\"version\"] = __version__\n        with open(config_path, \"w\") as f:\n            yaml.dump(config, f)\n\n        # Should show changes with --force\n        result = runner.invoke(app, [\"upgrade\", str(mock_project), \"--force\", \"--dry-run\"])\n\n        assert result.exit_code == 0\n        assert \"Changes to be made\" in result.stdout\n\n    def test_upgrade_shows_versions(self, mock_project):\n        \"\"\"Test that versions are displayed.\"\"\"\n        result = runner.invoke(app, [\"upgrade\", str(mock_project), \"--dry-run\"])\n\n        assert \"0.1.0\" in result.stdout  # Current\n        assert __version__ in result.stdout  # Target\n```\n\n**Criterios de Aceptación**:\n- [ ] Test `--dry-run` funciona\n- [ ] Test error sin config.yml\n- [ ] Test proyecto actualizado\n- [ ] Test `--force`\n- [ ] Test muestra versiones\n- [ ] Las respuestas para las preguntas de clarificación de TAREA 7:\n\n🔴 [requirements] Tests que verifiquen cambios de archivos cuando NO es --dry-run:\n\nSÍ - pero con mock del UpgradeService\nEl test debe verificar que UpgradeService.perform_upgrade fue llamado\nLos unit tests de TAREA 6 verifican la lógica real; CLI tests verifican integración\n🔴 [requirements] Tests de integración real (no mocked) verificando archivos en adws/, .claude/:\n\nNO para TAREA 7 - esos son los tests de TAREA 6\nTAREA 7 = tests del CLI (invocación, argumentos, output)\nTAREA 6 = tests del servicio (lógica de upgrade)\n🔴 [requirements] Tests verificando que config.yml version se actualiza:\n\nYa cubierto en TAREA 6 con test_perform_upgrade_updates_config_version\nCLI tests no necesitan duplicar esta verificación\n🟡 [requirements] Backup antes de aplicar cambios:\n\nSí, el UpgradeService crea backup por defecto\nTest para --no-backup ya existe implícitamente\nAgregar: test_upgrade_creates_backup verificando mensaje de backup\n🟡 [edge_case] Downgrade scenario (versión del proyecto > versión CLI):\n\nEl CLI muestra \"already up to date\" y no hace nada\nNO soporta downgrade\nAgregar test: test_upgrade_newer_project_version\n🟡 [edge_case] Partial upgrade failures:\n\nCubierto en TAREA 6 con rollback automático\nCLI tests no necesitan duplicar\n🟡 [requirements] Tests para confirmación/prompting:\n\nEl CliRunner de Typer puede simular input\nAgregar: test_upgrade_user_cancels (usuario dice \"no\" a confirmación)\n🟡 [edge_case] config.yml malformed/invalid YAML:\n\nYa testeado en TAREA 6: test_upgrade_invalid_config\nCLI tests solo verifican mensaje de error apropiado\n🟡 [edge_case] Directorio no writable:\n\nFuera de scope para MVP\nEl error de sistema se propagará naturalmente\n🟢 [requirements] Version migration paths específicos:\n\nNo necesario - la lógica es simple: current < target = upgrade\nCubierto con tests existentes\n🟢 [requirements] Verificar formato de diff en dry-run:\n\nSolo verificar que aparece \"Changes to be made\"\nNo verificar formato exacto del diff\n🟢 [edge_case] Concurrent upgrades o file locking:\n\nFuera de scope para MVP\nTests adicionales a agregar en TAREA 7:\n\ntest_upgrade_creates_backup_message - verificar mensaje de backup\ntest_upgrade_newer_project_version - proyecto con versión más nueva\ntest_upgrade_user_cancels - usuario cancela confirmación\ntest_upgrade_no_backup_flag - verificar --no-backup funciona\n\n"}`

## Feature Description
Crear tests de integración para el comando `tac-bootstrap upgrade` que validen la interfaz CLI, manejo de argumentos, mensajes de usuario, y la integración correcta con UpgradeService. A diferencia de TAREA 6 (tests unitarios del servicio), estos tests verifican que el CLI invoca correctamente el servicio y muestra mensajes apropiados al usuario.

Los tests complementan los de TAREA 6:
- **TAREA 6 (test_upgrade_service.py)**: Lógica de negocio, I/O real con archivos, edge cases del servicio
- **TAREA 7 (test_cli_upgrade.py)**: Invocación CLI, argumentos, mensajes al usuario, integración con servicio (mocked)

## User Story
As a TAC Bootstrap CLI developer
I want integration tests for the upgrade CLI command
So that I can ensure users get appropriate feedback, confirmation prompts work correctly, and CLI arguments are properly handled

## Problem Statement
El comando `tac-bootstrap upgrade` implementado en TAREA 3 expone funcionalidad crítica a usuarios finales. Los tests existentes en `test_upgrade_cli.py` ya cubren varios escenarios, pero faltan tests adicionales identificados en las clarificaciones del issue:

- Verificar que el backup crea mensaje apropiado al usuario
- Manejar escenario de proyecto con versión más nueva que el CLI (downgrade no soportado)
- Simular usuario cancelando confirmación durante upgrade
- Verificar flag `--no-backup`

Sin estos tests adicionales:
- Cambios en mensajes del CLI pueden romper UX sin detección
- Usuarios pueden ver mensajes confusos en edge cases
- La confirmación de usuario puede no funcionar correctamente
- Flags del CLI pueden no tener efecto esperado

## Solution Statement
Extender `test_upgrade_cli.py` con tests adicionales identificados en las clarificaciones del issue 88:

1. **test_upgrade_creates_backup_message**: Verificar que cuando backup=True (default), se muestra mensaje "Backup preserved"
2. **test_upgrade_newer_project_version**: Cuando proyecto tiene versión > CLI version, debe mostrar "already up to date" (no downgrade)
3. **test_upgrade_user_cancels**: Simular usuario cancelando upgrade en confirmación (input="n\n")
4. **test_upgrade_no_backup_flag**: Verificar que `--no-backup` pasa backup=False a UpgradeService

Los tests usarán:
- `CliRunner` de Typer para simular invocaciones del CLI
- `unittest.mock.patch` para mockear UpgradeService
- `input` parameter de CliRunner para simular respuestas de usuario
- Aserciones sobre stdout y exit codes
- NOTA: Los tests de TAREA 7 NO verifican I/O real de archivos - eso ya se cubre en TAREA 6

## Relevant Files
Archivos existentes necesarios:

- `tac_bootstrap_cli/tests/test_upgrade_cli.py` - Archivo existente con tests CLI (ya tiene 8 tests)
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py:624-708` - Implementación del comando upgrade
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - Servicio que se mockea
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Para importar `__version__`

### New Files
Ninguno - se extiende archivo existente `test_upgrade_cli.py`

## Implementation Plan

### Phase 1: Análisis de Tests Existentes
Revisar tests existentes en `test_upgrade_cli.py` para entender patrones de mocking y fixtures.

### Phase 2: Implementación de Tests Adicionales
Agregar los 4 tests faltantes identificados en las clarificaciones del issue.

### Phase 3: Validación
Ejecutar todos los tests y verificar que pasan sin regresiones.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Revisar tests existentes y estructura
- Leer `tac_bootstrap_cli/tests/test_upgrade_cli.py` completo
- Identificar patrones de mocking de UpgradeService
- Verificar que fixture `mock_project` y otros helpers están disponibles
- Confirmar que imports necesarios están presentes

### Task 2: Implementar test_upgrade_creates_backup_message
- Agregar test que simula upgrade exitoso con backup=True (default)
- Verificar que stdout contiene "Backup preserved"
- Mockear UpgradeService.perform_upgrade para retornar éxito
- Simular input="y\n" para confirmar upgrade

### Task 3: Implementar test_upgrade_newer_project_version
- Crear proyecto con versión > __version__ (simular downgrade scenario)
- Mockear needs_upgrade para retornar (False, "0.9.0", "0.2.0")
- Verificar que CLI muestra "already up to date"
- Verificar exit_code == 0

### Task 4: Verificar test_upgrade_user_cancels existe
- Confirmar que test ya existe en archivo (fue implementado previamente)
- Si no existe, agregarlo simulando input="n\n"
- Verificar que stdout contiene "Upgrade cancelled"
- Verificar que perform_upgrade NO fue llamado

### Task 5: Verificar test_upgrade_no_backup_flag existe
- Confirmar que test ya existe en archivo (fue implementado previamente)
- Si no existe, agregarlo con flag `--no-backup`
- Verificar que perform_upgrade fue llamado con backup=False
- Verificar que stdout NO contiene "Backup preserved"

### Task 6: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Verificar que no hay regresiones
- Confirmar que todos los nuevos tests pasan

## Testing Strategy

### Unit Tests
Los tests a agregar o verificar son:

1. **test_upgrade_creates_backup_message**:
   - Mock: UpgradeService retorna éxito
   - Input: "y\n" para confirmar
   - Assert: "Backup preserved" en stdout

2. **test_upgrade_newer_project_version**:
   - Mock: needs_upgrade retorna (False, "0.9.0", "0.2.0")
   - Assert: "already up to date" en stdout, exit_code == 0

3. **test_upgrade_user_cancels** (ya existe):
   - Input: "n\n" para cancelar
   - Assert: "Upgrade cancelled" en stdout, perform_upgrade NOT called

4. **test_upgrade_no_backup_flag** (ya existe):
   - Flag: `--no-backup`
   - Assert: perform_upgrade llamado con backup=False
   - Assert: "Backup preserved" NO en stdout

### Edge Cases
Los edge cases ya están cubiertos por tests existentes y TAREA 6:
- Config.yml faltante → test_upgrade_command_no_config
- Proyecto actualizado → test_upgrade_command_already_up_to_date
- Dry run → test_upgrade_command_dry_run
- Force upgrade → test_upgrade_command_force
- Upgrade failure → test_upgrade_command_failure

## Acceptance Criteria
- [ ] Test `test_upgrade_creates_backup_message` agregado y pasa
- [ ] Test `test_upgrade_newer_project_version` agregado y pasa
- [ ] Test `test_upgrade_user_cancels` existe y pasa (verificar)
- [ ] Test `test_upgrade_no_backup_flag` existe y pasa (verificar)
- [ ] Todos los tests existentes en test_upgrade_cli.py siguen pasando
- [ ] No hay regresiones en suite completa de tests
- [ ] Coverage del CLI upgrade command es completo para escenarios principales

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py -v --tb=short` - Tests CLI upgrade
- `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_service.py -v --tb=short` - Verificar no regresiones en servicio
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Suite completa
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check

## Notes

### División de Responsabilidades
Es importante entender que TAREA 6 y TAREA 7 tienen roles complementarios:

**TAREA 6 (test_upgrade_service.py)**: Tests unitarios del servicio
- Lógica de negocio del upgrade
- I/O real con sistema de archivos (tmp_path)
- Creación de backups, exclusión de directorios
- Rollback en caso de fallo
- Actualización de config.yml version
- Edge cases de servicio (config corrupto, backup failures)

**TAREA 7 (test_upgrade_cli.py)**: Tests de integración del CLI
- Invocación del comando CLI con argumentos
- Mensajes mostrados al usuario
- Manejo de confirmaciones (prompts)
- Integración con UpgradeService (mocked)
- Exit codes apropiados
- Edge cases de CLI (flags, combinaciones de argumentos)

### Tests Ya Existentes
El archivo `test_upgrade_cli.py` ya tiene 8 tests implementados:
1. test_upgrade_command_no_config
2. test_upgrade_command_already_up_to_date
3. test_upgrade_command_dry_run
4. test_upgrade_command_user_cancels
5. test_upgrade_command_success
6. test_upgrade_command_no_backup
7. test_upgrade_command_force
8. test_upgrade_command_failure

Esta tarea verifica que existan los tests faltantes identificados en las clarificaciones.

### Mocking Strategy
Todos los tests de TAREA 7 deben mockear UpgradeService para:
- Evitar I/O real de archivos (eso se testea en TAREA 6)
- Aislar comportamiento del CLI
- Simular diferentes respuestas del servicio (éxito, fallo, versiones)
- Mantener tests rápidos y determinísticos
