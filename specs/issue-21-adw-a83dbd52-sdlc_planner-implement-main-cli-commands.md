# Feature: Implement Main CLI Commands for TAC Bootstrap

## Metadata
issue_number: `21`
adw_id: `a83dbd52`
issue_json: `{"number":21,"title":"TAREA 4.1: Implementar comandos CLI principales","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos los modelos de dominio (TACConfig, ScaffoldPlan), el repositorio de templates,\ny los templates Jinja2. Ahora necesitamos implementar los comandos CLI que el usuario\nejecutara para generar la Agentic Layer.\n\nLos comandos principales son:\n- `init` - Crear proyecto nuevo con agentic layer\n- `add-agentic` - Inyectar agentic layer en repo existente\n- `doctor` - Validar setup existente\n- `render` - Re-generar desde config.yml\n\n## Objetivo\nImplementar los 4 comandos CLI usando Typer con opciones y argumentos apropiados."}`

## Feature Description

Implementar los 4 comandos CLI principales de TAC Bootstrap que los usuarios ejecutarán para generar y gestionar Agentic Layers en sus proyectos. Los comandos (`init`, `add-agentic`, `doctor`, `render`) proporcionan una interfaz completa para crear nuevos proyectos, inyectar la Agentic Layer en proyectos existentes, validar setups, y regenerar desde configuración.

Esta feature transforma TAC Bootstrap de una colección de modelos y templates en una herramienta CLI funcional y user-friendly con interfaz Rich, manejo de errores robusto, y opciones flexibles.

## User Story

As a **software developer or AI engineer**
I want to **use simple CLI commands to bootstrap Agentic Layers in my projects**
So that **I can quickly set up AI-assisted development workflows without manual configuration**

## Problem Statement

TAC Bootstrap tiene todos los componentes necesarios implementados:
- Modelos Pydantic para configuración (TACConfig, ProjectSpec, etc.)
- Modelos de plan de scaffolding (ScaffoldPlan, FileOperation)
- Repositorio de templates Jinja2 (TemplateRepository)
- Templates completos para Claude, ADWs, scripts, y configuración

Sin embargo, no existe una interfaz CLI user-friendly que permita a los usuarios:
1. Crear nuevos proyectos con Agentic Layer desde cero
2. Inyectar Agentic Layer en repositorios existentes con auto-detección
3. Validar y diagnosticar setups existentes
4. Regenerar archivos desde config.yml modificado

Necesitamos una CLI con comandos intuitivos, feedback visual rico, manejo de errores, y opciones de dry-run.

## Solution Statement

Implementar 4 comandos CLI usando Typer con Rich para output formateado:

1. **`init`**: Crea nuevo proyecto con Agentic Layer
   - Opciones para language, framework, package manager, architecture
   - Modo interactivo (wizard) vs no-interactivo
   - Dry-run para preview
   - Auto-detecta package manager si no se especifica

2. **`add-agentic`**: Inyecta Agentic Layer en repo existente
   - Auto-detección de language, framework, package manager
   - Wizard interactivo para confirmación/override
   - Force flag para overwrite de archivos existentes
   - Dry-run para preview

3. **`doctor`**: Valida setup existente
   - Checks de directorios requeridos
   - Validación de archivos de configuración
   - Reporte de issues con severidad (error, warning, info)
   - Auto-fix opcional para resolver issues

4. **`render`**: Regenera desde config.yml
   - Lee configuración existente
   - Reconstruye plan de scaffolding
   - Aplica cambios con force/dry-run options
   - Útil para actualizar tras modificar config.yml manualmente

Todos los comandos usan Rich para output formateado con colores, paneles, y mensajes claros de éxito/error.

## Relevant Files

Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py** - Archivo principal a modificar con los 4 comandos CLI
- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Modelos Pydantic (TACConfig, Language, Framework, etc.)
- **tac_bootstrap_cli/tac_bootstrap/domain/plan.py** - Modelos de ScaffoldPlan (usado en dry-run preview)
- **tac_bootstrap_cli/tac_bootstrap/__init__.py** - Contiene __version__ usado en comando version

### New Files

Esta tarea NO crea archivos nuevos. Modifica exclusivamente:
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`

### Placeholder Dependencies

Los siguientes servicios NO se implementan en esta tarea (se implementarán en tareas futuras):

- **ScaffoldService** (`tac_bootstrap.application.scaffold_service`)
  - `build_plan(config, existing_repo=False) -> ScaffoldPlan`
  - `apply_plan(plan, target_dir, config, force=False) -> ApplyResult`

- **DetectService** (`tac_bootstrap.application.detect_service`) - FASE 6
  - `detect(repo_path) -> DetectedProject`

- **DoctorService** (`tac_bootstrap.application.doctor_service`) - FASE 7
  - `diagnose(repo_path) -> HealthReport`
  - `fix(repo_path, report) -> FixResult`

- **Wizard Functions** (`tac_bootstrap.interfaces.wizard`)
  - `run_init_wizard(...) -> TACConfig`
  - `run_add_agentic_wizard(...) -> TACConfig`

## Implementation Plan

### Phase 1: Foundation
1. Importar dependencias necesarias (Typer, Rich, Path, Optional, sys)
2. Importar modelos de dominio (enums, TACConfig, ProjectSpec, CommandsSpec, etc.)
3. Configurar console de Rich y app de Typer con metadata
4. Implementar callback principal y comando version con Rich formatting

### Phase 2: Core Implementation
1. Implementar comando `init` con todas las opciones y argumentos
2. Implementar comando `add-agentic` con auto-detección y wizard
3. Implementar comando `doctor` con health checks y reporting
4. Implementar comando `render` con carga de YAML y regeneración

### Phase 3: Integration
1. Integrar con servicios placeholder (imports que fallarán gracefully)
2. Agregar manejo de errores robusto con Rich error messages
3. Validar que todos los comandos soporten --dry-run
4. Verificar output consistente con Rich panels y formateo de colores

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Setup CLI Foundation
- Reemplazar el contenido actual minimal de `cli.py`
- Importar todas las dependencias necesarias:
  - `import sys` para exit codes
  - `from pathlib import Path` para manejo de paths
  - `from typing import Optional` para type hints
  - `import typer` para CLI framework
  - `from rich.console import Console` y `from rich.panel import Panel` para output
  - Todos los modelos de dominio necesarios
- Configurar `app = typer.Typer()` con metadata apropiada
- Crear instancia global de Rich Console

### Task 2: Implement Main Callback and Version Command
- Implementar `main()` callback con check de `invoked_subcommand`
- Mostrar Panel de bienvenida bonito con versión cuando no hay subcommando
- Implementar comando `version()` que muestra versión formateada con Rich
- Usar `__version__` importado de `tac_bootstrap`

### Task 3: Implement Init Command
- Crear función `init()` con todos los argumentos y opciones:
  - `name: str` (Argument, requerido)
  - `output_dir: Optional[Path]` (Option, --output/-o)
  - `language: Language` (Option, --language/-l, default=PYTHON)
  - `framework: Framework` (Option, --framework/-f, default=NONE)
  - `package_manager: Optional[PackageManager]` (Option, --package-manager/-p)
  - `architecture: Architecture` (Option, --architecture/-a, default=SIMPLE)
  - `interactive: bool` (Option, --interactive/--no-interactive)
  - `dry_run: bool` (Option, --dry-run)
- Implementar lógica de branching para wizard vs no-interactive
- En modo no-interactive, construir TACConfig con defaults
- Auto-detectar package_manager si es None usando `get_package_managers_for_language()`
- Llamar a ScaffoldService.build_plan() y apply_plan()
- En dry-run mode, mostrar preview con Panel y listar dirs/files
- En success, mostrar Panel de éxito con stats y next steps
- Manejar errores con mensajes Rich y `raise typer.Exit(1)`

### Task 4: Implement Add-Agentic Command
- Crear función `add_agentic()` con argumentos:
  - `repo_path: Path` (Argument, default=".")
  - `interactive: bool` (Option, --interactive/--no-interactive)
  - `dry_run: bool` (Option, --dry-run)
  - `force: bool` (Option, --force/-f)
- Validar que repo_path existe
- Llamar a DetectService para auto-detectar project settings
- Mostrar Panel de auto-detection results con Rich
- Usar wizard en modo interactive, construir config manualmente en no-interactive
- Llamar a build_plan() con `existing_repo=True`
- En dry-run, mostrar preview con file actions
- Aplicar plan con force flag
- Mostrar success/error con Rich panels

### Task 5: Implement Doctor Command
- Crear función `doctor()` con argumentos:
  - `repo_path: Path` (Argument, default=".")
  - `fix: bool` (Option, --fix)
- Resolver repo_path a absolute path
- Llamar a DoctorService.diagnose()
- Si healthy, mostrar success panel
- Si unhealthy, mostrar error panel con count de issues
- Iterar sobre issues y mostrar cada uno con color según severity:
  - error: red
  - warning: yellow
  - info: blue
- Mostrar suggestion si existe (dim text)
- Si fix flag está presente, llamar a DoctorService.fix() y reportar
- `raise typer.Exit(1)` si unhealthy

### Task 6: Implement Render Command
- Crear función `render()` con argumentos:
  - `config_file: Path` (Argument, default="config.yml")
  - `output_dir: Optional[Path]` (Option, --output/-o)
  - `dry_run: bool` (Option, --dry-run)
  - `force: bool` (Option, --force/-f)
- Validar que config_file existe
- Cargar YAML con try/except para manejar parse errors:
  - `import yaml`
  - `raw_config = yaml.safe_load(f)`
  - `config = TACConfig(**raw_config)`
- Determinar target_dir (output_dir or config_file.parent)
- Build plan con `existing_repo=True`
- En dry-run, mostrar preview
- Aplicar plan con force
- Mostrar success/error con stats

### Task 7: Add Error Handling and Polish
- Revisar todos los comandos para manejo robusto de errores
- Asegurar que todos los errores usan Rich para formatting
- Verificar que todos los success cases muestran Panels bonitos
- Agregar docstrings completos con Examples en cada comando
- Validar que todos los comandos soportan --dry-run correctamente

### Task 8: Validation and Testing
- Ejecutar todos los comandos de verificación listados en Validation Commands
- Verificar que CLI carga sin errores de import
- Probar `--help` en cada comando para verificar docstrings
- Smoke test del comando version
- Verificar que no hay errores de type checking con mypy
- Verificar que ruff check pasa

## Testing Strategy

### Unit Tests

No se requieren unit tests en esta tarea porque:
1. Los servicios (ScaffoldService, DetectService, DoctorService, Wizard) son placeholders
2. Los tests reales se escribirán cuando se implementen los servicios
3. Esta tarea se enfoca en la interfaz CLI y estructura de comandos

### Manual Testing

```bash
# Test 1: Help messages
uv run tac-bootstrap --help
uv run tac-bootstrap init --help
uv run tac-bootstrap add-agentic --help
uv run tac-bootstrap doctor --help
uv run tac-bootstrap render --help

# Test 2: Version command
uv run tac-bootstrap version

# Test 3: Main callback (no command)
uv run tac-bootstrap
```

### Edge Cases

1. **Import errors de servicios placeholder**: CLI debe fallar gracefully con mensaje claro
2. **Paths que no existen**: Validar y mostrar error apropiado
3. **Config.yml inválido**: Catch parse errors de YAML y Pydantic
4. **Missing required arguments**: Typer maneja esto automáticamente
5. **Invalid enum values**: Typer valida automáticamente usando enums

## Acceptance Criteria

1. ✅ Comando `init` implementado con todas las opciones (language, framework, package_manager, architecture, interactive, dry_run, output_dir)
2. ✅ Comando `add-agentic` implementado con auto-detección (placeholder), interactive mode, force, dry_run
3. ✅ Comando `doctor` implementado con health checks (placeholder), fix option, severity-based reporting
4. ✅ Comando `render` implementado con YAML loading, config validation, dry_run, force
5. ✅ Todos los comandos soportan `--dry-run` flag
6. ✅ Output usa Rich para formateo bonito (Panels, colores, etc.)
7. ✅ Main callback muestra Panel de bienvenida cuando no hay subcommando
8. ✅ Comando `version` muestra versión formateada
9. ✅ Manejo robusto de errores con mensajes Rich y exit codes apropiados
10. ✅ Todos los comandos tienen docstrings completos con Examples
11. ✅ CLI pasa type checking (mypy)
12. ✅ CLI pasa linting (ruff check)
13. ✅ Help messages son claros y útiles para cada comando

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

```bash
# Change to CLI directory
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test CLI loads without errors
uv run tac-bootstrap --help
uv run tac-bootstrap init --help
uv run tac-bootstrap add-agentic --help
uv run tac-bootstrap doctor --help
uv run tac-bootstrap render --help

# Smoke test version
uv run tac-bootstrap version

# Type checking
uv run mypy tac_bootstrap/

# Linting
uv run ruff check .

# Format check
uv run ruff format --check .
```

## Notes

### Design Decisions

1. **Typer para CLI**: Framework moderno con auto-generación de help, validación de tipos, y excelente UX
2. **Rich para Output**: Proporciona formatting bonito, colores, panels, y mejor UX que print simple
3. **Dry-run Universal**: Todos los comandos destructivos soportan --dry-run para preview seguro
4. **Interactive by Default**: Los comandos usan wizard interactivo por default, se puede deshabilitar con --no-interactive
5. **Graceful Degradation**: Imports de servicios placeholder fallarán en runtime cuando se invoquen, con mensajes claros

### Placeholder Services

Esta tarea implementa la INTERFAZ CLI, no la lógica de negocio. Los servicios se implementarán en tareas futuras:
- **TAREA 4.2**: ScaffoldService
- **FASE 6**: DetectService
- **FASE 7**: DoctorService
- **TAREA 4.3**: Wizard interactivo

Por ahora, los imports están presentes pero las llamadas fallarán con `ImportError` o `ModuleNotFoundError` cuando se ejecuten.

### Future Enhancements

- Agregar comando `update` para actualizar Agentic Layer a nueva versión de templates
- Agregar comando `list` para listar proyectos con Agentic Layer
- Support para custom template directories
- Plugin system para extensiones de comandos

### NO Hacer en Esta Tarea

- ❌ No implementar ScaffoldService (TAREA 4.2)
- ❌ No implementar DetectService (FASE 6)
- ❌ No implementar DoctorService (FASE 7)
- ❌ No implementar wizard interactivo (TAREA 4.3)
- ❌ No escribir unit tests (se escribirán cuando servicios estén implementados)
- ❌ No modificar modelos de dominio
- ❌ No modificar templates
