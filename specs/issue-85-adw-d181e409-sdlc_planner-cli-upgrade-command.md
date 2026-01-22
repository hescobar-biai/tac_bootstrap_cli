# Feature: CLI `tac-bootstrap upgrade` Command

## Metadata
issue_number: `85`
adw_id: `d181e409`
issue_json: `{"number":85,"title":"TAREA 4: Crear comando CLI `tac-bootstrap upgrade`","body":"**Archivo**: `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`\n\n**Descripción**: Agregar comando `upgrade` al CLI de Typer.\n\n**Código**:\n\n```python\nfrom tac_bootstrap.application.upgrade_service import UpgradeService\n\n@app.command()\ndef upgrade(\n    path: Path = typer.Argument(\n        Path(\".\"),\n        help=\"Path to project to upgrade\",\n        exists=True,\n        file_okay=False,\n        dir_okay=True,\n    ),\n    dry_run: bool = typer.Option(\n        False,\n        \"--dry-run\",\n        \"-n\",\n        help=\"Show what would be changed without making changes\",\n    ),\n    backup: bool = typer.Option(\n        True,\n        \"--backup/--no-backup\",\n        help=\"Create backup before upgrading (default: enabled)\",\n    ),\n    force: bool = typer.Option(\n        False,\n        \"--force\",\n        \"-f\",\n        help=\"Force upgrade even if versions match\",\n    ),\n):\n    \"\"\"Upgrade agentic layer to latest TAC Bootstrap version.\n\n    This command updates the adws/, .claude/, and scripts/ directories\n    to the latest templates while preserving your project configuration.\n\n    Examples:\n        tac-bootstrap upgrade                    # Upgrade current directory\n        tac-bootstrap upgrade ./my-project       # Upgrade specific project\n        tac-bootstrap upgrade --dry-run          # Preview changes\n        tac-bootstrap upgrade --no-backup        # Upgrade without backup\n    \"\"\"\n    project_path = path.resolve()\n\n    # Verify it's a TAC project\n    config_file = project_path / \"config.yml\"\n    if not config_file.exists():\n        console.print(\"[red]Error: No config.yml found. Is this a TAC Bootstrap project?[/red]\")\n        raise typer.Exit(1)\n\n    service = UpgradeService(project_path)\n\n    # Check versions\n    needs_upgrade, current_ver, target_ver = service.needs_upgrade()\n\n    console.print(f\"\\n[bold]TAC Bootstrap Upgrade[/bold]\")\n    console.print(f\"  Current version: [yellow]{current_ver}[/yellow]\")\n    console.print(f\"  Target version:  [green]{target_ver}[/green]\")\n\n    if not needs_upgrade and not force:\n        console.print(\"\\n[green]Project is already up to date![/green]\")\n        raise typer.Exit(0)\n\n    # Show changes preview\n    console.print(\"\\n[bold]Changes to be made:[/bold]\")\n    for change in service.get_changes_preview():\n        console.print(f\"  • {change}\")\n\n    if dry_run:\n        console.print(\"\\n[yellow]Dry run - no changes made[/yellow]\")\n        raise typer.Exit(0)\n\n    # Confirm upgrade\n    if not typer.confirm(\"\\nProceed with upgrade?\", default=True):\n        console.print(\"[yellow]Upgrade cancelled[/yellow]\")\n        raise typer.Exit(0)\n\n    # Perform upgrade\n    console.print(\"\\n[bold]Upgrading...[/bold]\")\n    success, message = service.perform_upgrade(backup=backup)\n\n    if success:\n        console.print(f\"\\n[green]✓ {message}[/green]\")\n        if backup:\n            console.print(\"[dim]Backup preserved. Delete manually when confirmed working.[/dim]\")\n    else:\n        console.print(f\"\\n[red]✗ {message}[/red]\")\n        raise typer.Exit(1)\n```\n\n**Criterios de Aceptación**:\n- [ ] Comando `tac-bootstrap upgrade` disponible\n- [ ] `--dry-run` muestra cambios sin aplicar\n- [ ] `--no-backup` desactiva backup\n- [ ] `--force` fuerza upgrade aunque versiones coincidan\n- [ ] Muestra versión actual y target\n- [ ] Pide confirmación antes de proceder\n- [ ] Mensajes claros de éxito/error🔴 [requirements] Archivos/directorios a preservar:\n\nSe actualizan: adws/, .claude/, scripts/ (se reemplazan completamente)\nSe preservan: src/, código de usuario, archivos custom\nconfig.yml se preserva pero se actualiza el campo version\n🔴 [technical_decision] Manejo de conflictos:\n\nEstrategia: overwrite con backup. No hay merge.\nLos directorios adws/, .claude/, scripts/ se eliminan y regeneran completamente desde templates\nEl backup permite restauración manual si el usuario tenía customizaciones importantes\n🔴 [missing_info] Dónde se guarda la versión:\n\nCampo version en config.yml\nProyectos sin campo version se asumen como \"0.1.0\" (default para proyectos legacy)\n🟡 [technical_decision] Estrategia de backup:\n\nUbicación: .tac-backup-{timestamp}/ en el root del proyecto\nNaming: YYYYMMDD_HHMMSS timestamp\nCleanup: Manual - usuario borra cuando confirma que upgrade funciona\n🟡 [edge_case] Si upgrade falla:\n\nSí hay rollback automático desde backup (ver perform_upgrade() en TAREA 3)\nSi falla después de eliminar directorios, restaura desde backup automáticamente\n🟡 [technical_decision] get_changes_preview():\n\nLista cambios a nivel de directorio: \"Update adws/\" o \"Create adws/\"\nNo compara contenido de archivos, solo verifica existencia de directorios\n🟡 [edge_case] Validar estructura existente:\n\nSolo valida que config.yml exista\nSi faltan directorios, se crean durante upgrade\n🟢 [requirements] Pre/post upgrade hooks:\n\nNo implementados en v0.2.0\nSuficiente para MVP, se puede agregar después si hay demanda\n🟢 [edge_case] Cambios git sin commit:\n\nNo se valida por ahora\nEl backup protege de pérdida de datos\n🟢 [requirements] Upgrade a versión específica:\n\nSolo latest por ahora - suficiente para MVP\nSe puede agregar --target-version en futuras versiones"}`

## Feature Description
Agregar el comando `upgrade` al CLI de TAC Bootstrap para actualizar proyectos existentes a la última versión del CLI. Este comando permite a los usuarios actualizar la Agentic Layer (directorios `.claude/`, `adws/`, `scripts/`) mientras preservan su código y configuración del proyecto. Incluye funcionalidad de dry-run, backup automático con rollback, y confirmación antes de proceder.

## User Story
As a TAC Bootstrap user with an existing project
I want to upgrade my Agentic Layer to the latest version
So that I can get new features, bug fixes, and improvements without manually recreating my project

## Problem Statement
Los proyectos generados con versiones anteriores de TAC Bootstrap necesitan una forma segura y conveniente de actualizar la Agentic Layer (comandos slash, workflows ADW, hooks, scripts) a las últimas versiones sin perder su código de aplicación, configuración personalizada, o datos del proyecto. Actualmente, los usuarios tendrían que regenerar manualmente su proyecto o copiar archivos selectivamente, lo cual es propenso a errores y tedioso.

## Solution Statement
Implementar un comando `tac-bootstrap upgrade` que:
1. Detecta la versión actual del proyecto desde `config.yml` y la compara con la versión del CLI
2. Muestra un preview de los cambios que se realizarán
3. Crea un backup automático de los directorios a actualizar (`.tac-backup-{timestamp}/`)
4. Regenera los directorios `adws/`, `.claude/`, `scripts/` usando `ScaffoldService` con las últimas templates
5. Preserva el código del usuario (`src/`, `tac_bootstrap_cli/`, etc.) y actualiza solo el campo `version` en `config.yml`
6. Incluye rollback automático si algo falla durante el upgrade
7. Soporta modo dry-run para preview sin modificar archivos
8. Permite desactivar el backup con `--no-backup` para usuarios avanzados
9. Permite forzar upgrade con `--force` aunque las versiones coincidan (útil para re-aplicar templates)

## Relevant Files
Archivos necesarios para implementar la feature:

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Agregar comando `upgrade` con todos los argumentos/opciones
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` - Ya implementado en issue #82, contiene toda la lógica de negocio
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contiene `__version__` que se usa como target version
- `config.yml` - Configuración del proyecto, contiene el campo `version` a actualizar
- `.claude/commands/conditional_docs.md` - Documentación de referencia sobre UpgradeService

### New Files
- Ninguno (todos los archivos necesarios ya existen)

## Implementation Plan

### Phase 1: Foundation
Verificar que todos los componentes necesarios estén en su lugar:
- `UpgradeService` ya implementado en `application/upgrade_service.py` (issue #82)
- `ScaffoldService` ya implementado y probado
- `__version__` centralizado en `tac_bootstrap/__init__.py` (issue #81)
- Campo `version` en `TACConfig` schema (issue #79)
- Dependencia `packaging` instalada (issue #86)

### Phase 2: Core Implementation
Implementar el comando CLI `upgrade` en `cli.py`:
- Agregar imports necesarios (`UpgradeService`, `Path`, `typer`)
- Definir función `upgrade()` con decorador `@app.command()`
- Configurar argumentos y opciones (path, dry_run, backup, force)
- Implementar flujo completo:
  1. Validar que `config.yml` existe
  2. Instanciar `UpgradeService`
  3. Verificar versiones con `needs_upgrade()`
  4. Mostrar versiones actual y target
  5. Exit si no necesita upgrade y no hay `--force`
  6. Mostrar preview de cambios con `get_changes_preview()`
  7. Exit si `--dry-run`
  8. Confirmar con usuario (typer.confirm)
  9. Ejecutar `perform_upgrade(backup=backup)`
  10. Mostrar resultado y sugerencia sobre backup

### Phase 3: Integration
Integrar el nuevo comando con el resto del CLI:
- Actualizar el welcome panel en `main()` para incluir el comando `upgrade`
- Verificar que el comando aparece en `tac-bootstrap --help`
- Probar integración con `UpgradeService` y `ScaffoldService`

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verificar Dependencias
- Leer `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py` para verificar implementación
- Leer `tac_bootstrap_cli/tac_bootstrap/__init__.py` para confirmar `__version__`
- Verificar que `packaging` está en `pyproject.toml` dependencies

### Task 2: Implementar Comando `upgrade`
- Abrir `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- Agregar import: `from tac_bootstrap.application.upgrade_service import UpgradeService`
- Agregar función `upgrade()` con decorador `@app.command()` después del comando `render()`
- Implementar argumentos:
  - `path: Path` con default `Path(".")`, help, exists=True, file_okay=False, dir_okay=True
- Implementar opciones:
  - `dry_run: bool` con default False, flags `--dry-run` y `-n`
  - `backup: bool` con default True, flags `--backup/--no-backup`
  - `force: bool` con default False, flags `--force` y `-f`
- Agregar docstring completo con ejemplos de uso

### Task 3: Implementar Lógica del Comando
- Resolver `project_path` a absolute path
- Validar existencia de `config.yml`, exit con error si no existe
- Instanciar `UpgradeService(project_path)`
- Llamar `needs_upgrade()` para obtener tupla (needs, current_ver, target_ver)
- Mostrar versiones con Rich formatting (yellow para current, green para target)
- Si no necesita upgrade y no hay `--force`, mostrar mensaje y exit con código 0
- Obtener preview con `get_changes_preview()` y mostrar lista de cambios
- Si `--dry-run`, mostrar mensaje y exit con código 0
- Pedir confirmación con `typer.confirm()`, default=True
- Si usuario cancela, mostrar mensaje y exit con código 0
- Llamar `perform_upgrade(backup=backup)` y capturar resultado
- Si success, mostrar mensaje verde con versión y nota sobre backup
- Si failure, mostrar mensaje rojo con error y exit con código 1

### Task 4: Actualizar Welcome Panel
- En función `main()`, agregar línea para comando `upgrade` en welcome_text:
  ```
  [green]upgrade[/green]      Upgrade to latest TAC Bootstrap version
  ```
- Colocar después de `render` y antes de `version`

### Task 5: Escribir Tests Unitarios
- Crear `tac_bootstrap_cli/tests/test_upgrade_cli.py`
- Test `test_upgrade_command_no_config()`: verificar error si no existe config.yml
- Test `test_upgrade_command_already_up_to_date()`: verificar exit 0 cuando versiones coinciden
- Test `test_upgrade_command_dry_run()`: verificar que dry-run no modifica archivos
- Test `test_upgrade_command_user_cancels()`: verificar exit cuando usuario cancela confirmación
- Test `test_upgrade_command_success()`: verificar upgrade exitoso con backup
- Test `test_upgrade_command_no_backup()`: verificar upgrade sin backup cuando se usa --no-backup
- Test `test_upgrade_command_force()`: verificar que --force permite upgrade cuando versiones coinciden
- Test `test_upgrade_command_failure()`: verificar manejo de errores cuando upgrade falla
- Usar fixtures de `tmp_path` para crear estructuras de proyecto temporales
- Usar `CliRunner` de Typer para ejecutar el comando
- Mockear `UpgradeService` cuando sea necesario para edge cases

### Task 6: Validación
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py -v --tb=short`
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help` y verificar que `upgrade` aparece
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap upgrade --help` y verificar help completo
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .`
- Ejecutar `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Ejecutar todos los Validation Commands al final

## Testing Strategy

### Unit Tests
1. **Test de validación de proyecto TAC**:
   - Verificar error cuando `config.yml` no existe
   - Verificar error cuando `path` no es un directorio

2. **Test de detección de versiones**:
   - Verificar exit 0 cuando proyecto está actualizado
   - Verificar que muestra versiones correctas (current vs target)

3. **Test de modo dry-run**:
   - Verificar que no modifica archivos
   - Verificar que muestra preview de cambios
   - Verificar exit 0

4. **Test de confirmación de usuario**:
   - Verificar exit cuando usuario cancela
   - Verificar que continúa cuando usuario acepta

5. **Test de upgrade exitoso**:
   - Verificar que llama a `perform_upgrade(backup=True)`
   - Verificar mensaje de éxito
   - Verificar nota sobre backup

6. **Test de upgrade sin backup**:
   - Verificar que llama a `perform_upgrade(backup=False)` con `--no-backup`
   - Verificar que no muestra nota sobre backup

7. **Test de modo force**:
   - Verificar que permite upgrade cuando versiones coinciden con `--force`
   - Verificar que llama a `perform_upgrade()`

8. **Test de manejo de errores**:
   - Verificar mensaje de error cuando `perform_upgrade()` falla
   - Verificar exit con código 1

### Edge Cases
- **Proyecto sin campo version en config.yml**: UpgradeService maneja esto retornando "0.1.0" como default
- **Usuario cancela upgrade**: typer.confirm retorna False, se muestra mensaje y exit
- **Upgrade falla durante ejecución**: UpgradeService tiene rollback automático, CLI muestra error
- **Dry-run con proyecto actualizado**: Debe mostrar versiones y preview aunque no necesite upgrade
- **Force con versiones iguales**: Debe proceder con upgrade aunque versiones coincidan
- **Path no existe**: Typer valida con `exists=True` antes de ejecutar función
- **Path es archivo no directorio**: Typer valida con `dir_okay=True, file_okay=False`

## Acceptance Criteria
1. ✓ Comando `tac-bootstrap upgrade` está disponible en el CLI
2. ✓ Comando acepta argumento `path` opcional (default: directorio actual)
3. ✓ Opción `--dry-run / -n` muestra preview sin modificar archivos
4. ✓ Opción `--backup/--no-backup` controla creación de backup (default: enabled)
5. ✓ Opción `--force / -f` permite upgrade forzado cuando versiones coinciden
6. ✓ Muestra versión actual y target del proyecto con colores apropiados
7. ✓ Muestra lista de cambios que se realizarán antes de proceder
8. ✓ Pide confirmación al usuario antes de ejecutar upgrade
9. ✓ Mensajes claros de éxito con checkmark verde y versión actualizada
10. ✓ Mensajes claros de error con X roja y descripción del problema
11. ✓ Nota sobre backup cuando está habilitado (user debe borrar manualmente)
12. ✓ Exit con código 0 cuando proyecto ya está actualizado (sin --force)
13. ✓ Exit con código 0 en dry-run mode
14. ✓ Exit con código 0 cuando usuario cancela
15. ✓ Exit con código 1 cuando ocurre error
16. ✓ Error claro cuando `config.yml` no existe
17. ✓ Comando aparece en `tac-bootstrap --help` y welcome panel
18. ✓ Comando tiene help completo con `tac-bootstrap upgrade --help`
19. ✓ Todos los tests unitarios pasan
20. ✓ Código pasa linting (ruff) y type checking (mypy)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap upgrade --help` - Verificar help del comando

## Notes

### Decisiones Técnicas
- **Overwrite strategy**: Los directorios `adws/`, `.claude/`, `scripts/` se eliminan completamente y regeneran desde templates. No hay merge de archivos individuales.
- **Backup location**: `.tac-backup-{timestamp}/` en root del proyecto, cleanup manual por el usuario
- **Rollback automático**: Si falla después de eliminar directorios, `UpgradeService.perform_upgrade()` restaura desde backup automáticamente
- **Preview granularity**: `get_changes_preview()` trabaja a nivel de directorio ("Update adws/", "Create scripts/"), no compara contenido de archivos individuales
- **Version comparison**: Usa `packaging.version.parse()` para comparación semántica correcta

### Preservación de Archivos
- **Se actualizan (overwrite completo)**: `adws/`, `.claude/`, `scripts/`
- **Se preservan intactos**: `src/`, `tac_bootstrap_cli/`, código de usuario, archivos custom
- **Se actualiza parcialmente**: `config.yml` solo actualiza campo `version`, todo lo demás se preserva

### Edge Cases Manejados
- Proyectos legacy sin campo `version`: Se asume "0.1.0" como default
- Directorios faltantes: Se crean durante upgrade (no es error)
- Solo se valida existencia de `config.yml`, no estructura completa

### Futuras Mejoras (NO implementar ahora)
- Pre/post upgrade hooks: No en v0.2.0, agregar si hay demanda
- Upgrade a versión específica (`--target-version`): Solo latest por ahora
- Validación de cambios git sin commit: El backup protege de pérdida de datos, suficiente para MVP
- Dry-run con diff detallado: Por ahora solo lista de directorios, suficiente para MVP

### Referencias
- Issue #82: Implementación de `UpgradeService`
- Issue #79: Campo `version` en schema de `TACConfig`
- Issue #81: Constante `__version__` centralizada
- Issue #86: Dependencia `packaging` para version comparison
- `app_docs/feature-c928f831-upgrade-service.md`: Documentación completa del UpgradeService
