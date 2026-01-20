# Feature: Implement Interactive Wizard with Rich

## Metadata
issue_number: `25`
adw_id: `ede93862`
issue_json: `{"number":25,"title":"TAREA 4.2: Implementar wizard interactivo con Rich","body":"# Prompt para Agente\n\n## Contexto\nLa CLI ya tiene los comandos basicos. Ahora necesitamos implementar el wizard\ninteractivo que guia al usuario para configurar el proyecto paso a paso.\n\nEl wizard usa Rich para:\n- Prompts interactivos con opciones\n- Colores y formateo bonito\n- Confirmacion antes de ejecutar\n\n## Objetivo\nCrear el modulo wizard.py con funciones para guiar la configuracion interactiva.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Interactive wizard for TAC Bootstrap configuration.\n\nUses Rich for beautiful terminal UI with prompts and selections.\n\"\"\"\nfrom pathlib import Path\nfrom typing import Optional\n\nfrom rich.console import Console\nfrom rich.panel import Panel\nfrom rich.prompt import Prompt, Confirm\nfrom rich.table import Table\n\nfrom tac_bootstrap.domain.models import (\n    TACConfig,\n    ProjectSpec,\n    PathsSpec,\n    CommandsSpec,\n    ClaudeConfig,\n    ClaudeSettings,\n    AgenticSpec,\n    Language,\n    Framework,\n    Architecture,\n    PackageManager,\n    ProjectMode,\n    get_frameworks_for_language,\n    get_package_managers_for_language,\n    get_default_commands,\n)\n\nconsole = Console()\n\n\ndef select_from_enum(prompt: str, enum_class, default=None, filter_fn=None) -> any:\n    \"\"\"Interactive selection from enum values.\n\n    Args:\n        prompt: Question to ask\n        enum_class: Enum class to select from\n        default: Default value\n        filter_fn: Optional function to filter valid options\n\n    Returns:\n        Selected enum value\n    \"\"\"\n    options = list(enum_class)\n    if filter_fn:\n        options = [o for o in options if filter_fn(o)]\n\n    # Build options table\n    table = Table(show_header=False, box=None, padding=(0, 2))\n    for i, opt in enumerate(options, 1):\n        is_default = opt == default\n        marker = \"[green]>[/green]\" if is_default else \" \"\n        table.add_row(f\"{marker} {i}.\", f\"[bold]{opt.value}[/bold]\")\n\n    console.print(f\"\\n[bold]{prompt}[/bold]\")\n    console.print(table)\n\n    # Get selection\n    default_num = options.index(default) + 1 if default in options else 1\n    choice = Prompt.ask(\n        \"Select option\",\n        default=str(default_num),\n        choices=[str(i) for i in range(1, len(options) + 1)]\n    )\n\n    return options[int(choice) - 1]\n\n\ndef run_init_wizard(\n    name: str,\n    language: Optional[Language] = None,\n    framework: Optional[Framework] = None,\n    package_manager: Optional[PackageManager] = None,\n    architecture: Optional[Architecture] = None,\n) -> TACConfig:\n    \"\"\"Run interactive wizard for project initialization.\n\n    Args:\n        name: Project name (already provided)\n        language: Pre-selected language (or None to ask)\n        framework: Pre-selected framework (or None to ask)\n        package_manager: Pre-selected package manager (or None to ask)\n        architecture: Pre-selected architecture (or None to ask)\n\n    Returns:\n        Configured TACConfig\n    \"\"\"\n    console.print(Panel.fit(\n        f\"[bold blue]Creating new project:[/bold blue] {name}\\n\\n\"\n        \"Let's configure your Agentic Layer!\",\n        title=\"🚀 TAC Bootstrap Wizard\"\n    ))\n\n    # Step 1: Language\n    if language is None:\n        language = select_from_enum(\n            \"What programming language?\",\n            Language,\n            default=Language.PYTHON\n        )\n    console.print(f\"  [green]✓[/green] Language: {language.value}\")\n\n    # Step 2: Framework\n    if framework is None:\n        valid_frameworks = get_frameworks_for_language(language)\n        framework = select_from_enum(\n            \"What framework?\",\n            Framework,\n            default=Framework.NONE,\n            filter_fn=lambda f: f in valid_frameworks\n        )\n    console.print(f\"  [green]✓[/green] Framework: {framework.value}\")\n\n    # Step 3: Package Manager\n    if package_manager is None:\n        valid_managers = get_package_managers_for_language(language)\n        package_manager = select_from_enum(\n            \"What package manager?\",\n            PackageManager,\n            default=valid_managers[0] if valid_managers else None,\n            filter_fn=lambda p: p in valid_managers\n        )\n    console.print(f\"  [green]✓[/green] Package Manager: {package_manager.value}\")\n\n    # Step 4: Architecture\n    if architecture is None:\n        architecture = select_from_enum(\n            \"What architecture pattern?\",\n            Architecture,\n            default=Architecture.SIMPLE\n        )\n    console.print(f\"  [green]✓[/green] Architecture: {architecture.value}\")\n\n    # Step 5: Commands (with smart defaults)\n    console.print(\"\\n[bold]Commands Configuration[/bold]\")\n    default_commands = get_default_commands(language, package_manager)\n\n    start_cmd = Prompt.ask(\n        \"  Start command\",\n        default=default_commands.get(\"start\", \"\")\n    )\n    test_cmd = Prompt.ask(\n        \"  Test command\",\n        default=default_commands.get(\"test\", \"\")\n    )\n    lint_cmd = Prompt.ask(\n        \"  Lint command (optional)\",\n        default=default_commands.get(\"lint\", \"\")\n    )\n\n    # Step 6: Worktrees\n    use_worktrees = Confirm.ask(\n        \"\\nEnable git worktrees for parallel workflows?\",\n        default=True\n    )\n\n    # Build config\n    config = TACConfig(\n        project=ProjectSpec(\n            name=name,\n            mode=ProjectMode.NEW,\n            language=language,\n            framework=framework,\n            architecture=architecture,\n            package_manager=package_manager,\n        ),\n        paths=PathsSpec(\n            app_root=\"src\" if architecture != Architecture.SIMPLE else \".\",\n        ),\n        commands=CommandsSpec(\n            start=start_cmd,\n            test=test_cmd,\n            lint=lint_cmd,\n        ),\n        agentic=AgenticSpec(\n            worktrees={\"enabled\": use_worktrees, \"max_parallel\": 5},\n        ),\n        claude=ClaudeConfig(\n            settings=ClaudeSettings(project_name=name)\n        ),\n    )\n\n    # Confirmation\n    console.print(\"\\n\")\n    _show_config_summary(config)\n\n    if not Confirm.ask(\"\\nProceed with this configuration?\", default=True):\n        console.print(\"[yellow]Aborted.[/yellow]\")\n        raise SystemExit(0)\n\n    return config\n\n\ndef run_add_agentic_wizard(\n    repo_path: Path,\n    detected: \"DetectedProject\",\n) -> TACConfig:\n    \"\"\"Run wizard for adding agentic layer to existing project.\n\n    Args:\n        repo_path: Path to existing repository\n        detected: Auto-detected project settings\n\n    Returns:\n        Configured TACConfig\n    \"\"\"\n    console.print(Panel.fit(\n        f\"[bold blue]Adding Agentic Layer to:[/bold blue] {repo_path.name}\\n\\n\"\n        \"Review detected settings and customize commands.\",\n        title=\"🔧 TAC Bootstrap Wizard\"\n    ))\n\n    # Confirm or change detected settings\n    language = select_from_enum(\n        \"Programming language (detected):\",\n        Language,\n        default=detected.language\n    )\n\n    framework = select_from_enum(\n        \"Framework (detected):\",\n        Framework,\n        default=detected.framework or Framework.NONE,\n        filter_fn=lambda f: f in get_frameworks_for_language(language)\n    )\n\n    package_manager = select_from_enum(\n        \"Package manager (detected):\",\n        PackageManager,\n        default=detected.package_manager,\n        filter_fn=lambda p: p in get_package_managers_for_language(language)\n    )\n\n    # Commands - most important for existing projects\n    console.print(\"\\n[bold]Configure Commands[/bold]\")\n    console.print(\"[dim]These commands will be used by Claude Code and ADW workflows[/dim]\\n\")\n\n    default_commands = get_default_commands(language, package_manager)\n\n    start_cmd = Prompt.ask(\n        \"  Start command\",\n        default=detected.commands.get(\"start\", default_commands.get(\"start\", \"\"))\n    )\n    test_cmd = Prompt.ask(\n        \"  Test command\",\n        default=detected.commands.get(\"test\", default_commands.get(\"test\", \"\"))\n    )\n    lint_cmd = Prompt.ask(\n        \"  Lint command\",\n        default=detected.commands.get(\"lint\", default_commands.get(\"lint\", \"\"))\n    )\n    build_cmd = Prompt.ask(\n        \"  Build command\",\n        default=detected.commands.get(\"build\", default_commands.get(\"build\", \"\"))\n    )\n\n    # Worktrees\n    use_worktrees = Confirm.ask(\n        \"\\nEnable git worktrees for parallel workflows?\",\n        default=True\n    )\n\n    # Build config\n    config = TACConfig(\n        project=ProjectSpec(\n            name=repo_path.name,\n            mode=ProjectMode.EXISTING,\n            repo_root=str(repo_path),\n            language=language,\n            framework=framework,\n            package_manager=package_manager,\n        ),\n        paths=PathsSpec(\n            app_root=detected.app_root or \"src\",\n        ),\n        commands=CommandsSpec(\n            start=start_cmd,\n            test=test_cmd,\n            lint=lint_cmd,\n            build=build_cmd,\n        ),\n        agentic=AgenticSpec(\n            worktrees={\"enabled\": use_worktrees, \"max_parallel\": 5},\n        ),\n        claude=ClaudeConfig(\n            settings=ClaudeSettings(project_name=repo_path.name)\n        ),\n    )\n\n    # Confirmation\n    console.print(\"\\n\")\n    _show_config_summary(config)\n\n    if not Confirm.ask(\"\\nProceed with this configuration?\", default=True):\n        console.print(\"[yellow]Aborted.[/yellow]\")\n        raise SystemExit(0)\n\n    return config\n\n\ndef _show_config_summary(config: TACConfig) -> None:\n    \"\"\"Display configuration summary table.\"\"\"\n    table = Table(title=\"Configuration Summary\", show_header=True)\n    table.add_column(\"Setting\", style=\"cyan\")\n    table.add_column(\"Value\", style=\"green\")\n\n    table.add_row(\"Project Name\", config.project.name)\n    table.add_row(\"Language\", config.project.language.value)\n    table.add_row(\"Framework\", config.project.framework.value)\n    table.add_row(\"Package Manager\", config.project.package_manager.value)\n    table.add_row(\"Architecture\", config.project.architecture.value)\n    table.add_row(\"Start Command\", config.commands.start)\n    table.add_row(\"Test Command\", config.commands.test)\n    table.add_row(\"Worktrees Enabled\", str(config.agentic.worktrees.enabled))\n\n    console.print(table)\n```\n\n## Criterios de Aceptacion\n1. [ ] select_from_enum muestra opciones numeradas\n2. [ ] run_init_wizard guia configuracion completa\n3. [ ] run_add_agentic_wizard usa valores detectados como defaults\n4. [ ] Tabla de resumen muestra configuracion final\n5. [ ] Confirmacion antes de proceder\n6. [ ] UI es clara y bonita con Rich\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\n\n# Test import\nuv run python -c \"\nfrom tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard\nfrom tac_bootstrap.domain.models import Language\nprint('Wizard module loaded successfully')\n\"\n\n# Test con init interactivo (manual)\n# uv run tac-bootstrap init test-project\n```\n\n## NO hacer\n- No implementar logica de scaffolding (FASE 5)\n- No implementar deteccion (FASE 6)"}`

## Feature Description

Implementar un wizard interactivo completo usando Rich que guía al usuario paso a paso en la configuración de proyectos TAC Bootstrap. El wizard proporciona una experiencia CLI user-friendly con opciones numeradas, defaults inteligentes basados en contexto del lenguaje seleccionado, tablas visuales de resumen, y confirmación antes de proceder con la operación.

Esta feature transforma la experiencia CLI de comandos con múltiples flags a una conversación interactiva guiada que reduce errores de configuración, mejora la usabilidad para usuarios nuevos, y provee contexto visual durante el proceso de configuración.

## User Story

As a **developer setting up TAC Bootstrap for a new or existing project**
I want to **be guided through configuration interactively with clear visual prompts**
So that **I don't need to memorize CLI flags, can make informed decisions with context, and see a preview before committing to the configuration**

## Problem Statement

Los comandos CLI `init` y `add-agentic` actualmente tienen modo `--interactive` implementado como placeholder que muestra mensaje de "not yet implemented". Los usuarios deben:

1. Conocer todos los flags disponibles (`--language`, `--framework`, `--package-manager`, `--architecture`)
2. Recordar qué frameworks son válidos para cada lenguaje (ej: FastAPI para Python, NextJS para TypeScript)
3. Saber qué package managers están disponibles para su stack (ej: uv/poetry para Python, pnpm/npm/yarn para JS/TS)
4. Configurar comandos manualmente sin ver defaults contextuales basados en sus selecciones
5. No tienen preview visual de la configuración completa antes de proceder

Esto crea fricción especialmente para usuarios nuevos que no están familiarizados con todas las opciones del ecosistema TAC Bootstrap, y resulta en configuraciones incorrectas o subóptimas.

## Solution Statement

Implementar módulo completo `wizard.py` con funciones interactivas usando Rich para proporcionar experiencia guided configuration:

1. **`select_from_enum()`**: Función helper reutilizable para selección interactiva de enums
   - Muestra opciones numeradas (1, 2, 3...) en tabla Rich formateada sin header
   - Soporta valores default con indicador visual verde `>`
   - Permite filtrado dinámico de opciones válidas por contexto (ej: solo frameworks compatibles con lenguaje seleccionado)
   - Valida input del usuario contra choices permitidos
   - Retorna enum value tipado correctamente

2. **`run_init_wizard()`**: Wizard completo para proyectos nuevos
   - Panel de bienvenida con emoji y título claro
   - Secuencia de 6 pasos guiados:
     - Language selection (default: Python)
     - Framework selection (filtrado por lenguaje, default: None)
     - Package manager selection (filtrado por lenguaje, default: primer válido)
     - Architecture pattern selection (default: Simple)
     - Commands configuration con defaults inteligentes basados en lenguaje + package manager
     - Worktrees preference con explicación contextual
   - Checkmarks verdes (✓) después de cada selección para feedback visual de progreso
   - Tabla de resumen con configuración completa antes de confirmar
   - Confirmación Yes/No con opción de abortar limpiamente

3. **`run_add_agentic_wizard()`**: Wizard para proyectos existentes
   - Panel explicativo sobre inyección de Agentic Layer
   - Muestra valores auto-detectados como defaults en cada prompt
   - Permite override de detección con selección interactiva
   - Enfoque especial en configuración de comandos (start, test, lint, build) que son críticos para proyectos existentes
   - Similar flujo de confirmación que init wizard

4. **`_show_config_summary()`**: Helper privado para resumen visual
   - Tabla Rich con título "Configuration Summary"
   - Dos columnas: Setting (cyan) | Value (green)
   - Muestra todos los settings clave: name, language, framework, package manager, architecture, commands, worktrees
   - Formato consistente con .value para enums y str() para booleans

El wizard usa Rich para proporcionar UI de terminal moderna:
- Paneles con bordes coloridos y títulos para secciones importantes
- Tablas sin bordes para opciones numeradas
- Tablas con bordes para resumen final
- Prompts con defaults claros y validación
- Confirmaciones Yes/No con defaults sensibles
- Checkmarks (✓) para feedback de progreso
- Mensajes coloridos: green=success, yellow=warning, red=error, cyan=info, dim=secondary text

## Relevant Files

Archivos clave para implementar esta feature:

- **tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py** - Módulo principal del wizard (YA EXISTE - revisar implementación actual)
- **tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py** - Comandos CLI que invocan el wizard cuando `--interactive=True`
- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Modelos Pydantic y helper functions que el wizard utiliza
- **tac_bootstrap_cli/pyproject.toml** - Verificar dependencias (rich>=13.7.0 debe estar instalado)

### New Files

Esta tarea NO crea archivos nuevos - el archivo wizard.py YA EXISTE en:
`tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`

La tarea consiste en:
1. **Revisar** la implementación actual del wizard.py
2. **Verificar** que cumple con todos los criterios de aceptación del issue
3. **Refinar/Completar** cualquier aspecto faltante si es necesario
4. **Integrar** el wizard con los comandos CLI (remover placeholders)

### Dependencies on Helper Functions

El wizard depende de helper functions existentes en `domain/models.py`:
- `get_frameworks_for_language(language: Language) -> List[Framework]` - Retorna frameworks válidos para un lenguaje
- `get_package_managers_for_language(language: Language) -> List[PackageManager]` - Retorna package managers válidos
- `get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]` - Retorna comandos default contextuales

### Type Handling for DetectedProject

El wizard usa tipo `"DetectedProject"` como string literal type hint porque DetectService no está implementado aún (FASE 6). Esto permite que el código pase type checking sin implementar el servicio completo.

## Implementation Plan

### Phase 1: Review and Validation
Revisar implementación actual de wizard.py y verificar que cumple con especificaciones del issue #25

### Phase 2: Integration with CLI
Remover placeholders en cli.py e integrar wizard con comandos `init` y `add-agentic`

### Phase 3: Testing and Refinement
Ejecutar validation commands, crear/actualizar tests unitarios, verificar UX y feedback visual

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review Current Wizard Implementation
- Leer archivo existente `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`
- Comparar implementación actual con especificación del issue #25
- Identificar diferencias entre código actual y código esperado en el issue
- Verificar que todas las funciones están implementadas:
  - `select_from_enum()` con signature correcta y type hints
  - `run_init_wizard()` con flujo completo de 6 pasos
  - `run_add_agentic_wizard()` con soporte para detected settings
  - `_show_config_summary()` para tabla de resumen
- Verificar imports y dependencias de Rich
- Verificar uso correcto de helper functions de domain/models.py

### Task 2: Verify AgenticSpec Construction
- Revisar cómo se construye `AgenticSpec` en ambos wizards
- ISSUE CRÍTICO: El issue muestra `worktrees={"enabled": use_worktrees, "max_parallel": 5}` (dict)
- REALIDAD: Debe ser `worktrees=WorktreeConfig(enabled=use_worktrees, max_parallel=5)` (Pydantic model)
- Verificar que la implementación actual usa WorktreeConfig correctamente
- Si usa dict, corregir a usar WorktreeConfig model

### Task 3: Integrate Wizard with CLI Commands
- Abrir `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`
- Localizar función `init()` - encontrar sección de interactive mode (línea ~124)
- Reemplazar placeholder con llamada a `run_init_wizard()`:
  ```python
  if interactive:
      from tac_bootstrap.interfaces.wizard import run_init_wizard
      config = run_init_wizard(
          name=name,
          language=language,
          framework=framework,
          package_manager=package_manager,
          architecture=architecture,
      )
  ```
- Localizar función `add_agentic()` - encontrar sección de interactive mode (línea ~285)
- Reemplazar placeholder con llamada a `run_add_agentic_wizard()`:
  ```python
  if interactive:
      from tac_bootstrap.interfaces.wizard import run_add_agentic_wizard
      config = run_add_agentic_wizard(repo_path, detected)
  ```
- IMPORTANTE: DetectService no está implementado, así que add_agentic seguirá fallando con ImportError, pero el código wizard estará integrado para cuando DetectService exista

### Task 4: Verify Rich UI Consistency
- Revisar que todos los mensajes usan Rich markup correcto:
  - `[bold]...[/bold]` para énfasis
  - `[green]...[/green]` para success
  - `[yellow]...[/yellow]` para warnings
  - `[red]...[/red]` para errors
  - `[cyan]...[/cyan]` para info
  - `[dim]...[/dim]` para texto secundario
- Verificar que Panel.fit() se usa correctamente con title parameter
- Verificar que Table se construye con parámetros apropiados (show_header, box, padding)
- Verificar que checkmarks (✓) aparecen después de cada selección en run_init_wizard

### Task 5: Execute Validation Commands
- Ejecutar todos los comandos de verificación del issue:
  ```bash
  cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

  # Test 1: Verificar imports
  uv run python -c "
  from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard
  from tac_bootstrap.domain.models import Language
  print('Wizard module loaded successfully')
  "

  # Test 2: Unit tests
  uv run pytest tests/ -v --tb=short

  # Test 3: Linting
  uv run ruff check .

  # Test 4: Type checking
  uv run mypy tac_bootstrap/

  # Test 5: CLI smoke test
  uv run tac-bootstrap --help
  ```
- Si algún test falla, identificar y resolver issues
- Si hay errores de mypy relacionados con "DetectedProject", verificar que se usa string literal type hint
- Si hay errores de ruff, aplicar fixes automáticos con `uv run ruff check --fix .`

## Testing Strategy

### Unit Tests

Tests necesarios (crear/actualizar en `tests/interfaces/test_wizard.py`):

1. **Test `select_from_enum()`**:
   - Mock `console.print` y `Prompt.ask` para simular user input
   - Test con default value - verificar que default_num se calcula correctamente
   - Test con filter_fn - verificar que opciones se filtran correctamente
   - Test con selección válida - verificar que retorna enum correcto
   - Test edge case: filter resulta en lista vacía - debe raise ValueError

2. **Test `run_init_wizard()`**:
   - Mock todos los Rich prompts (Prompt.ask, Confirm.ask)
   - Mock console.print para evitar output real
   - Test flujo completo con todos los parámetros None - verificar que pregunta todo
   - Test con parámetros pre-seleccionados - verificar que no pregunta lo que ya está configurado
   - Test confirmación = No - verificar SystemExit(0)
   - Test confirmación = Yes - verificar que retorna TACConfig válido
   - Verificar construcción correcta de WorktreeConfig (NO dict)

3. **Test `run_add_agentic_wizard()`**:
   - Mock detected object con atributos esperados (language, framework, package_manager, commands, app_root)
   - Test que detected values se usan como defaults en prompts
   - Test que mode=EXISTING y repo_root se configuran correctamente
   - Test que incluye build_cmd (adicional vs init)

4. **Test `_show_config_summary()`**:
   - Mock console.print
   - Crear TACConfig de prueba
   - Verificar que tabla contiene todas las filas esperadas
   - Verificar formato correcto: .value para enums, str() para booleans

### Edge Cases

1. **Todos los parámetros pre-seleccionados**: Wizard debe usar valores sin preguntar
2. **Filter_fn resulta en lista vacía**: Debe manejar caso de cero opciones válidas
3. **Usuario cancela confirmación**: SystemExit(0) limpio sin stacktrace
4. **Comandos opcionales vacíos**: lint y build pueden ser strings vacíos
5. **Framework NONE**: Es válido y debe manejarse sin errores
6. **Language sin frameworks válidos**: Debe manejar lista vacía de get_frameworks_for_language()

### Manual Testing

Tests interactivos (no automatizados):

```bash
# Test wizard completo con init
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run tac-bootstrap init test-wizard-project --interactive

# Flujo de prueba:
# 1. Seleccionar TypeScript
# 2. Seleccionar NextJS
# 3. Seleccionar pnpm
# 4. Seleccionar DDD
# 5. Verificar defaults de comandos son correctos para pnpm
# 6. Aceptar worktrees=Yes
# 7. Revisar tabla de summary
# 8. Confirmar o cancelar

# Test aborto:
# Repetir test pero responder "No" a confirmación final
# Verificar mensaje amarillo y exit limpio
```

## Acceptance Criteria

1. ✓ Archivo `wizard.py` existe y se puede importar sin errores
2. ✓ `select_from_enum()` muestra tabla Rich con opciones numeradas
3. ✓ `select_from_enum()` marca default con `[green]>[/green]` visualmente
4. ✓ `select_from_enum()` filtra opciones usando filter_fn correctamente
5. ✓ `run_init_wizard()` ejecuta secuencia de 6 pasos interactivos
6. ✓ `run_init_wizard()` usa helper functions para defaults contextuales (get_default_commands basado en language + package_manager)
7. ✓ `run_init_wizard()` construye TACConfig válido con WorktreeConfig (NO dict)
8. ✓ `run_init_wizard()` muestra checkmarks (✓) después de cada selección
9. ✓ `run_add_agentic_wizard()` usa detected settings como defaults en prompts
10. ✓ `run_add_agentic_wizard()` incluye build_cmd en commands
11. ✓ `run_add_agentic_wizard()` configura mode=EXISTING y repo_root
12. ✓ `_show_config_summary()` muestra tabla clara con todas las settings clave
13. ✓ Confirmación final permite abortar con SystemExit(0) limpiamente
14. ✓ UI usa Rich correctamente: panels, tables, colors, markup
15. ✓ Wizard está integrado en cli.py (placeholders removidos)
16. ✓ Todos los validation commands pasan: imports, pytest, ruff, mypy, CLI smoke test

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

```bash
# Test 1: Verificar imports y carga del módulo
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run python -c "
from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard
from tac_bootstrap.domain.models import Language
print('✓ Wizard module loaded successfully')
"

# Test 2: Unit tests
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run pytest tests/ -v --tb=short

# Test 3: Linting
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run ruff check .

# Test 4: Type checking
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run mypy tac_bootstrap/

# Test 5: CLI smoke test
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run tac-bootstrap --help

# Test 6 (Manual - opcional): Test wizard interactivo
# cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
# uv run tac-bootstrap init test-wizard-project --interactive
```

## Notes

### Critical Issue: AgenticSpec Construction

El issue #25 muestra construcción INCORRECTA de AgenticSpec:
```python
# INCORRECTO (del issue):
agentic=AgenticSpec(
    worktrees={"enabled": use_worktrees, "max_parallel": 5},
)

# CORRECTO (debe ser):
agentic=AgenticSpec(
    worktrees=WorktreeConfig(enabled=use_worktrees, max_parallel=5),
)
```

La implementación actual en wizard.py DEBE usar WorktreeConfig model, NO dict.

### Integration Status

Después de esta tarea:
- ✓ Wizard completamente implementado en wizard.py
- ✓ CLI integrado para modo --interactive
- ✗ DetectService aún no implementado (FASE 6) - add_agentic wizard funcionará cuando exista
- ✗ ScaffoldService puede no estar completo (FASE 5) - wizard construye config pero scaffolding real depende de otro servicio

### Rich UI Best Practices

El wizard sigue estas prácticas:
- **Paneles** con Panel.fit() para secciones importantes (bienvenida, resumen)
- **Tablas sin header** para opciones (box=None, padding=(0, 2))
- **Tablas con header** para resumen final (show_header=True)
- **Colores semánticos**: green=success, yellow=warning, red=error, cyan=info, dim=secondary
- **Checkmarks (✓)** para feedback de progreso
- **Defaults claros** en cada Prompt.ask()
- **Confirmación final** antes de retornar config

### Future Enhancements

Mejoras futuras (out of scope):
1. Modo `--expert` con preguntas avanzadas (safety config, model policy, logging level)
2. Guardar configuración del usuario en `~/.tac-bootstrap/defaults.yml` para reusar
3. Wizard para `doctor --fix` que pregunta cómo resolver cada issue
4. Preview de templates que se renderizarán antes de confirmación
5. Wizard para comando `render` que permite editar config.yml interactivamente

### Dependencies Not Implemented Yet

Esta tarea NO requiere implementar:
- **ScaffoldService** (FASE 5) - El wizard solo construye TACConfig
- **DetectService** (FASE 6) - run_add_agentic_wizard usa type hint string literal
- **DoctorService** (FASE 7) - No usado por wizard

### What NOT to Do

- **NO implementar scaffolding logic** - eso es ScaffoldService
- **NO implementar auto-detection** - eso es DetectService
- **NO crear E2E integration tests** - solo unit tests mocking Rich
- **NO agregar comandos CLI nuevos** - solo integrar wizard con comandos existentes
- **NO modificar domain models** - usar lo que existe en models.py
- **NO cambiar signatures de helper functions** - confiar en get_frameworks_for_language, get_package_managers_for_language, get_default_commands tal como están
