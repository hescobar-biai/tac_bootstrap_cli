# Feature: Crear servicio UpgradeService

## Metadata
issue_number: `82`
adw_id: `c928f831`
issue_json: `{"number":82,"title":"TAREA 3: Crear servicio UpgradeService","body":"*Archivo**: tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py\n\n**Descripción**: Servicio que maneja la lógica de actualización de proyectos.\n\n**Código**:\n\n```python\n\"\"\"Upgrade service for TAC Bootstrap projects.\"\"\"\n\nfrom __future__ import annotations\n\nimport shutil\nfrom datetime import datetime\nfrom pathlib import Path\nfrom typing import Optional, Tuple, List\nfrom packaging import version as pkg_version\n\nimport yaml\nfrom rich.console import Console\n\nfrom tac_bootstrap import __version__\nfrom tac_bootstrap.domain.models import TACConfig\nfrom tac_bootstrap.application.scaffold_service import ScaffoldService\n\nconsole = Console()\n\n\nclass UpgradeService:\n    \"\"\"Service for upgrading TAC Bootstrap projects to newer versions.\"\"\"\n\n    # Directorios que se actualizan (no código del usuario)\n    UPGRADEABLE_DIRS = [\"adws\", \".claude\", \"scripts\"]\n\n    # Archivos que se actualizan en root\n    UPGRADEABLE_FILES = [\"config.yml\"]\n\n    def __init__(self, project_path: Path):\n        \"\"\"Initialize upgrade service.\n\n        Args:\n            project_path: Path to the project to upgrade\n        \"\"\"\n        self.project_path = project_path\n        self.config_path = project_path / \"config.yml\"\n        self.scaffold_service = ScaffoldService()\n\n    def get_current_version(self) -> Optional[str]:\n        \"\"\"Get current project version from config.yml.\n\n        Returns:\n            Version string or None if not found/invalid\n        \"\"\"\n        if not self.config_path.exists():\n            return None\n\n        try:\n            with open(self.config_path) as f:\n                config_data = yaml.safe_load(f)\n               * return config_data.get(\"version\", \"0.1.0\")  # Default for old projects\n        except Exception:\n            return None\n\n    def get_target_version(self) -> str:\n        \"\"\"Get target version (current CLI version).\"\"\"\n        return __version__\n\n    def needs_upgrade(self) -> Tuple[bool, str, str]:\n        \"\"\"Check if project needs upgrade.\n\n        Returns:\n            Tuple of (needs_upgrade, current_version, target_version)\n        \"\"\"\n        current = self.get_current_version()\n        target = self.get_target_version()\n\n        if current is None:\n            return False, \"unknown\", target\n\n        try:\n            needs = pkg_version.parse(current) < pkg_version.parse(target)\n            return needs, current, target\n        except Exception:\n            return False, current, target\n\n    def load_existing_config(self) -> Optional[TACConfig]:\n        \"\"\"Load existing project configuration.\n\n        Returns:\n            TACConfig or None if invalid\n        \"\"\"\n        if not self.config_path.exists():\n            return None\n\n        try:\n            with open(self.config_path) as f:\n                config_data = yaml.safe_load(f)\n\n            # Actualizar version al target\n            config_data[\"version\"] = self.get_target_version()\n\n            return TACConfig(**config_data)\n        except Exception as e:\n            console.print(f\"[red]Error loading config: {e}[/red]\")\n            return None\n\n    def create_backup(self) -> Path:\n        \"\"\"Create backup of upgradeable directories.\n\n        Returns:\n            Path to backup directory\n        \"\"\"\n        timestamp = datetime.now().strftime(\"%Y%m%d_%H%M%S\")\n        backup_dir = self.project_path / f\".tac-backup-{timestamp}\"\n        backup_dir.mkdir(exist_ok=True)\n\n        for dir_name in self.UPGRADEABLE_DIRS:\n            source = self.project_path / dir_name\n            if source.exists():\n                shutil.copytree(source, backup_dir / dir_name)\n\n        # Backup config.yml\n        if self.config_path.exists():\n            shutil.copy2(self.config_path, backup_dir / \"config.yml\")\n\n        return backup_dir\n\n    def get_changes_preview(self) -> List[str]:\n        \"\"\"Get list of changes that will be made.\n\n        Returns:\n            List of change descriptions\n        \"\"\"\n        changes = []\n\n        for dir_name in self.UPGRADEABLE_DIRS:\n            dir_path = self.project_path / dir_name\n            if dir_path.exists():\n                changes.append(f\"Update {dir_name}/ directory\")\n            else:\n                changes.append(f\"Create {dir_name}/ directory\")\n\n        changes.append(\"Update version in config.yml\")\n\n        return changes\n\n    def perform_upgrade(self, backup: bool = True) -> Tuple[bool, str]:\n        \"\"\"Perform the upgrade.\n\n        Args:\n            backup: Whether to create backup before upgrading\n\n        Returns:\n            Tuple of (success, message)\n        \"\"\"\n        # Load existing config\n        config = self.load_existing_config()\n        if config is None:\n            return False, \"Could not load existing configuration\"\n\n        # Create backup if requested\n        backup_path = None\n        if backup:\n            backup_path = self.create_backup()\n            console.print(f\"[green]Created backup at: {backup_path}[/green]\")\n\n        try:\n            # Remove old directories\n            for dir_name in self.UPGRADEABLE_DIRS:\n                dir_path = self.project_path / dir_name\n                if dir_path.exists():\n                    shutil.rmtree(dir_path)\n\n            # Regenerate using scaffold service with updated config\n            self.scaffold_service.scaffold_project(config, self.project_path)\n\n            return True, f\"Successfully upgraded to v{self.get_target_version()}\"\n\n        except Exception as e:\n            # Restore from backup if available\n            if backup_path and backup_path.exists():\n                console.print(\"[yellow]Restoring from backup...[/yellow]\")\n                for dir_name in self.UPGRADEABLE_DIRS:\n                    backup_source = backup_path / dir_name\n                    if backup_source.exists():\n                        target = self.project_path / dir_name\n                        if target.exists():\n                            shutil.rmtree(target)\n                        shutil.copytree(backup_source, target)\n\n            return False, f\"Upgrade failed: {e}\"\n```\n\n**Criterios de Aceptación**:\n- [ ] UpgradeService creado con métodos documentados\n- [ ] Detecta versión actual del proyecto\n- [ ] Compara versiones correctamente\n- [ ] Crea backups antes de actualizar\n- [ ] Regenera solo directorios de agentic layer\n- [ ] Preserva configuración del usuario\n- [ ] Restaura backup si falla\n## Respuestas Clarificaciones\n\n### Respuestas rápidas:\n\n1. **Sin config.yml**: Retornar error \"Not a TAC Bootstrap project\" - ya está en el código.\n\n2. **Customizaciones usuario (CRÍTICA)**: **SOBRESCRIBIR COMPLETAMENTE**. El backup existe para esto. Los usuarios pueden copiar sus customizaciones del backup después. El upgrade regenera desde templates limpios.\n\n3. **Downgrade (version actual > target)**: No permitir upgrade, mostrar mensaje \"Project version is newer than CLI version\".\n\n4. **Limpieza de backups**: NO automática. El usuario decide cuándo borrar. Agregar nota: \"Delete backup manually when confirmed working\".\n\n5. **Fallo de backup**: **ABORTAR** el upgrade. Sin backup = sin red de seguridad.\n\n6. **Upgrades concurrentes**: Fuera de scope. Asumir single-threaded.\n\n7. **Dry-run**: Sí, el CLI ya lo tiene con `--dry-run`. El service tiene `get_changes_preview()`.\n\n8. **Versiones malformadas**: Usar comparación de strings simple. Si falla parsing, asumir que necesita upgrade.\n\n9. **Validar templates antes de borrar (CRÍTICA)**: NO. Confiar en ScaffoldService. Si falla, restaurar desde backup.\n\n10. **Scripts personalizados**: **SOBRESCRITOS**. El backup los preserva.\n\n11. **Rollback**: Solo manual desde backup. No hay comando tac rollback.\n\n12. **Logging**: Sí, usar Rich console para output visible al usuario.\n\n### Confirmación:\n✅ Assumptions son correctas:\n- Customizaciones se pierden (backup las preserva)\n- Versión default 0.1.0\n- Restauración best-effort\n- Single-threaded\n- No migration scripts"}`

## Feature Description
Crear el servicio `UpgradeService` que maneja la lógica de actualización de proyectos TAC Bootstrap a versiones más recientes del CLI. Este servicio es responsable de:

1. Detectar la versión actual del proyecto (desde config.yml)
2. Comparar con la versión del CLI para determinar si necesita upgrade
3. Crear backups automáticos de los directorios del Agentic Layer
4. Regenerar los directorios `.claude/`, `adws/`, y `scripts/` desde templates actualizados
5. Preservar la configuración del usuario en config.yml
6. Restaurar desde backup si el upgrade falla

Este servicio es parte de la TAREA 3 del plan de upgrade y será utilizado por el comando CLI `tac-bootstrap upgrade` en tareas posteriores.

## User Story
As a TAC Bootstrap user with an existing project
I want the CLI to upgrade my Agentic Layer to the latest version
So that I can benefit from new features, fixes, and improvements without losing my project configuration

## Problem Statement
Los proyectos generados con versiones anteriores de TAC Bootstrap necesitan ser actualizados cuando el CLI evoluciona con nuevas features, comandos slash, workflows ADW, o mejoras en templates. Actualmente no existe un mecanismo automatizado para:

- Detectar qué versión del Agentic Layer tiene un proyecto
- Comparar versiones para saber si necesita upgrade
- Actualizar de forma segura (con backup) solo los directorios del Agentic Layer
- Preservar la configuración del usuario durante el upgrade
- Recuperarse de errores restaurando desde backup

Esto obliga a los usuarios a regenerar manualmente o perder las nuevas features del CLI.

## Solution Statement
Implementar `UpgradeService` como un servicio de aplicación (application layer) que encapsula toda la lógica de upgrade:

1. **Detección de versión**: Leer config.yml para obtener la versión actual del proyecto
2. **Comparación**: Usar `packaging.version` para comparar versiones semánticamente
3. **Backup seguro**: Crear `.tac-backup-{timestamp}/` con copia de `.claude/`, `adws/`, `scripts/`, y `config.yml`
4. **Regeneración selectiva**: Eliminar y regenerar solo directorios del Agentic Layer usando ScaffoldService
5. **Preservación de config**: Cargar config.yml existente, actualizar solo el campo version, y regenerar
6. **Recuperación de errores**: Si falla el upgrade, restaurar automáticamente desde backup
7. **Preview de cambios**: Proveer `get_changes_preview()` para dry-run en el CLI

El servicio sigue el patrón arquitectónico DDD del proyecto y reutiliza ScaffoldService para la regeneración.

## Relevant Files
Archivos existentes que serán utilizados:

- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contiene `__version__ = "0.2.0"` que se usará como target version
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model para cargar/validar configuración
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - ScaffoldService para regenerar estructura
- `tac_bootstrap_cli/pyproject.toml` - Ya tiene `packaging` en dependencies

### New Files
Archivo nuevo a crear:

- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - El servicio de upgrade completo (código provisto en issue)

## Implementation Plan

### Phase 1: Foundation
Crear el archivo del servicio con estructura básica, imports, y constantes.

### Phase 2: Core Implementation
Implementar todos los métodos del UpgradeService según la especificación del issue.

### Phase 3: Integration
Asegurar que el servicio funcione correctamente con ScaffoldService y valide todos los edge cases.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Crear archivo con estructura básica
- Crear `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py`
- Agregar docstring del módulo
- Agregar imports necesarios:
  - `from __future__ import annotations`
  - `import shutil`, `datetime`, `pathlib`
  - `from typing import Optional, Tuple, List`
  - `from packaging import version as pkg_version`
  - `import yaml`
  - `from rich.console import Console`
  - `from tac_bootstrap import __version__`
  - `from tac_bootstrap.domain.models import TACConfig`
  - `from tac_bootstrap.application.scaffold_service import ScaffoldService`
- Crear instancia global `console = Console()`
- Definir constantes de clase `UPGRADEABLE_DIRS` y `UPGRADEABLE_FILES`

### Task 2: Implementar `__init__` y métodos de detección de versión
- Implementar `__init__(self, project_path: Path)` que inicializa:
  - `self.project_path`
  - `self.config_path = project_path / "config.yml"`
  - `self.scaffold_service = ScaffoldService()`
- Implementar `get_current_version() -> Optional[str]`:
  - Verificar que config.yml existe
  - Cargar YAML y retornar campo `version` (default "0.1.0" para proyectos viejos)
  - Manejar excepciones retornando None
- Implementar `get_target_version() -> str`:
  - Retornar `__version__` del módulo
- Implementar `needs_upgrade() -> Tuple[bool, str, str]`:
  - Obtener current y target versions
  - Si current es None, retornar `(False, "unknown", target)`
  - Usar `pkg_version.parse()` para comparar semánticamente
  - Retornar `(needs, current, target)`
  - Manejar excepciones de parsing retornando `(False, current, target)`

### Task 3: Implementar carga de configuración
- Implementar `load_existing_config() -> Optional[TACConfig]`:
  - Verificar que config.yml existe
  - Cargar YAML a diccionario
  - **IMPORTANTE**: Actualizar `config_data["version"]` al target version antes de crear TACConfig
  - Crear y retornar `TACConfig(**config_data)` para validación con Pydantic
  - Si hay error, mostrar mensaje con Rich console y retornar None

### Task 4: Implementar sistema de backup
- Implementar `create_backup() -> Path`:
  - Generar timestamp con formato `"%Y%m%d_%H%M%S"`
  - Crear directorio `.tac-backup-{timestamp}` en project_path
  - Para cada directorio en `UPGRADEABLE_DIRS`:
    - Si existe, copiarlo con `shutil.copytree()` al backup dir
  - Copiar `config.yml` con `shutil.copy2()` al backup dir
  - Retornar Path al backup directory

### Task 5: Implementar preview de cambios
- Implementar `get_changes_preview() -> List[str]`:
  - Crear lista vacía de cambios
  - Para cada directorio en `UPGRADEABLE_DIRS`:
    - Si existe: agregar "Update {dir}/ directory"
    - Si no existe: agregar "Create {dir}/ directory"
  - Agregar "Update version in config.yml"
  - Retornar lista de cambios

### Task 6: Implementar perform_upgrade (método principal)
- Implementar `perform_upgrade(self, backup: bool = True) -> Tuple[bool, str]`:
  - Cargar config existente con `load_existing_config()`
  - Si config es None, retornar `(False, "Could not load existing configuration")`
  - Si `backup=True`:
    - Crear backup con `create_backup()`
    - Mostrar mensaje con Rich console: "Created backup at: {backup_path}"
  - Dentro de try/except:
    - Para cada directorio en `UPGRADEABLE_DIRS`:
      - Si existe, eliminarlo con `shutil.rmtree()`
    - **CRÍTICO**: Regenerar usando `scaffold_service.build_plan()` y `scaffold_service.apply_plan()`
      - `plan = self.scaffold_service.build_plan(config, existing_repo=True)`
      - `result = self.scaffold_service.apply_plan(plan, self.project_path, config)`
      - Verificar `result.success`, si es False lanzar excepción
    - Retornar `(True, f"Successfully upgraded to v{self.get_target_version()}")`
  - En excepción:
    - Si existe backup_path:
      - Mostrar "[yellow]Restoring from backup...[/yellow]"
      - Para cada directorio en UPGRADEABLE_DIRS del backup:
        - Si existe en target, eliminarlo
        - Copiarlo desde backup con `shutil.copytree()`
    - Retornar `(False, f"Upgrade failed: {e}")`

### Task 7: Verificar que `packaging` esté instalado
- Ejecutar `cd tac_bootstrap_cli && uv pip list | grep packaging`
- Verificar que está instalado (versión 25.0 o superior)
- Si no está, agregar a dependencies en pyproject.toml

### Task 8: Ejecutar Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios (deben pasar sin regresiones)
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting (debe pasar sin errores)
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check (debe pasar sin errores)
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test (debe funcionar)

## Testing Strategy

### Unit Tests
En tarea posterior (TAREA 4) se crearán tests para:
- `test_get_current_version()` - con config.yml válido, sin versión, sin archivo
- `test_get_target_version()` - debe retornar `__version__`
- `test_needs_upgrade()` - comparar versiones viejas, iguales, y nuevas
- `test_load_existing_config()` - cargar config válido, actualizar version field
- `test_create_backup()` - crear backup, verificar estructura
- `test_get_changes_preview()` - preview con dirs existentes y faltantes
- `test_perform_upgrade()` - upgrade exitoso, con backup, con fallo y rollback

### Edge Cases
- Sin config.yml → `get_current_version()` retorna None
- Config.yml sin campo version → Usar default "0.1.0"
- Versión malformada → Comparación simple o asumir que necesita upgrade
- Downgrade (current > target) → `needs_upgrade()` retorna False
- Fallo durante upgrade → Restaurar desde backup automáticamente
- Fallo al crear backup → El método `perform_upgrade()` debe abortar si backup=True

## Acceptance Criteria
- [ ] UpgradeService creado con todos los métodos documentados según especificación
- [ ] Detecta versión actual del proyecto desde config.yml (default "0.1.0" si falta)
- [ ] Compara versiones correctamente usando `packaging.version` (semántico)
- [ ] Crea backups antes de actualizar en directorio `.tac-backup-{timestamp}/`
- [ ] Regenera solo directorios de agentic layer (`.claude/`, `adws/`, `scripts/`)
- [ ] Preserva configuración del usuario cargando config.yml existente y actualizando solo version
- [ ] Restaura backup automáticamente si falla el upgrade
- [ ] Método `get_changes_preview()` retorna lista de cambios para dry-run
- [ ] Todos los métodos tienen type hints completos
- [ ] Todos los métodos tienen docstrings con formato Google style
- [ ] Código pasa linting (`ruff check`) sin errores
- [ ] Código pasa type checking (`mypy`) sin errores
- [ ] No hay regresiones en tests existentes

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Decisiones de diseño importantes:

1. **Sobrescritura completa de Agentic Layer**: El upgrade elimina y regenera completamente `.claude/`, `adws/`, y `scripts/`. Cualquier customización del usuario se pierde (el backup las preserva para copia manual).

2. **Backup obligatorio**: Si `backup=True` (default), el upgrade DEBE crear backup exitosamente antes de proceder. Si falla el backup, abortar el upgrade.

3. **No hay rollback automático programático**: Solo restauración desde backup si falla el upgrade. No existe comando `tac rollback`.

4. **Versión default 0.1.0**: Proyectos sin campo version en config.yml se asumen como 0.1.0 (primera versión).

5. **Regeneración con ScaffoldService**: El upgrade usa `build_plan(config, existing_repo=True)` y `apply_plan()` del ScaffoldService existente, reutilizando toda la lógica de templates.

6. **Limpieza de backups manual**: Los backups NO se eliminan automáticamente. El usuario debe borrarlos manualmente cuando confirme que el upgrade funcionó.

7. **Logging con Rich console**: Todos los mensajes al usuario usan Rich console para output formateado y colorizado.

8. **Single-threaded**: No se soportan upgrades concurrentes. Asumir que solo un proceso upgrade corre a la vez.

### Dependencias:

- `packaging` library - Ya está instalado en el proyecto (versión 25.0)
- `yaml` (PyYAML) - Ya está en dependencies
- `rich` - Ya está en dependencies
- `shutil`, `datetime` - Stdlib de Python

### Próximas tareas:

- TAREA 4: Tests unitarios para UpgradeService
- TAREA 5: Comando CLI `tac-bootstrap upgrade` que usa este servicio
- TAREA 6: Documentación del comando upgrade
