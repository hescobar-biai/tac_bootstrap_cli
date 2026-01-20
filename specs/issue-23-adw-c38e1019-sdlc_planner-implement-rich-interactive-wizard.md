# Feature: Implement Rich Interactive Wizard for TAC Bootstrap Configuration

## Metadata
issue_number: `23`
adw_id: `c38e1019`
issue_json: `{"number":23,"title":"TAREA 4.2: Implementar wizard interactivo con Rich","body":" Prompt para Agente\n\n## Contexto\nLa CLI ya tiene los comandos basicos. Ahora necesitamos implementar el wizard\ninteractivo que guia al usuario para configurar el proyecto paso a paso.\n\nEl wizard usa Rich para:\n- Prompts interactivos con opciones\n- Colores y formateo bonito\n- Confirmacion antes de ejecutar\n\n## Objetivo\nCrear el modulo wizard.py con funciones para guiar la configuracion interactiva.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`"}`

## Feature Description

Implementar un módulo wizard interactivo que guía a los usuarios paso a paso en la configuración de proyectos TAC Bootstrap. El wizard usa Rich para crear una experiencia de terminal hermosa y user-friendly con:
- Selección interactiva de opciones enumeradas con highlighting
- Prompts contextuales con defaults inteligentes basados en language/framework
- Tabla de resumen de configuración con formato atractivo
- Confirmación final antes de ejecutar acciones
- Manejo de valores pre-seleccionados vs valores a solicitar

El wizard soporta dos flujos:
1. **Init Wizard**: Configuración completa para nuevos proyectos
2. **Add Agentic Wizard**: Configuración guiada para proyectos existentes con valores auto-detectados como defaults

## User Story

As a **developer using TAC Bootstrap CLI**
I want to **be guided through project configuration with an interactive wizard**
So that **I can easily configure my Agentic Layer without memorizing CLI flags or config options**

## Problem Statement

Los comandos CLI `init` y `add-agentic` actualmente solo funcionan en modo no-interactivo (requieren `--no-interactive` flag). Esto obliga a los usuarios a:
1. Conocer todas las opciones disponibles de antemano
2. Recordar flags y valores válidos para language, framework, package manager, architecture
3. Especificar todo en la línea de comandos, haciendo comandos largos y propensos a errores
4. No ver preview de la configuración antes de ejecutar

La mayoría de los usuarios prefieren un wizard interactivo que:
- Les muestra las opciones disponibles con descripciones
- Les sugiere defaults inteligentes basados en sus elecciones previas
- Les permite confirmar la configuración completa antes de crear archivos
- Proporciona una UI atractiva y clara en terminal con colores y formato

## Solution Statement

Crear el módulo `tac_bootstrap/interfaces/wizard.py` con funciones wizard que usan Rich para:

1. **`select_from_enum()`**: Helper genérico para selección interactiva desde enums
   - Muestra opciones numeradas en una tabla Rich
   - Marca el default con indicador visual (">")
   - Soporta filtrado de opciones (e.g., solo frameworks válidos para un language)
   - Valida selección numérica del usuario

2. **`run_init_wizard()`**: Wizard para comando `init`
   - Panel de bienvenida con título y descripción
   - Flujo paso a paso: Language → Framework → Package Manager → Architecture → Commands → Worktrees
   - Checkmarks visuales (✓) al completar cada paso
   - Defaults inteligentes usando `get_default_commands()` helper
   - Tabla de resumen de configuración final
   - Confirmación antes de proceder

3. **`run_add_agentic_wizard()`**: Wizard para comando `add-agentic`
   - Panel informativo sobre proyecto detectado
   - Pre-población de valores desde `DetectedProject`
   - Permite override de valores detectados
   - Foco especial en configuración de comandos (start, test, lint, build)
   - Misma UX de resumen y confirmación

4. **`_show_config_summary()`**: Helper privado para mostrar tabla de configuración
   - Formato consistente con columnas "Setting" y "Value"
   - Colores cyan para settings, green para valores
   - Usado por ambos wizards antes de confirmación

El módulo integra perfectamente con:
- Domain models (Language, Framework, Architecture, PackageManager enums)
- Helper functions (`get_frameworks_for_language`, `get_package_managers_for_language`, `get_default_commands`)
- CLI commands (llamados desde `init()` y `add_agentic()` cuando `interactive=True`)

## Relevant Files

Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Enums y helper functions que usa el wizard (Language, Framework, Architecture, PackageManager, get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- **tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py** - Comandos CLI que invocarán las funciones del wizard cuando interactive=True (líneas 123-126, 284-287)
- **tac_bootstrap_cli/pyproject.toml** - Verifica que Rich esté en dependencies (ya está: rich>=13.7.0)

### New Files

- **tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py** - Módulo principal con funciones wizard interactivas

### Dependencies

El wizard depende de servicios/tipos que NO se implementan en esta tarea:

- **DetectedProject** type (usado en `run_add_agentic_wizard`)
  - Será implementado en FASE 6 (DetectService)
  - Para esta tarea, usar type hint con string: `detected: "DetectedProject"`
  - Asumir que tiene atributos: `language`, `framework`, `package_manager`, `commands` (dict), `app_root`, `name`

- **ScaffoldService** (NO necesario para wizard)
  - El wizard solo construye `TACConfig`
  - Los comandos CLI usan el config retornado para llamar ScaffoldService

## Implementation Plan

### Phase 1: Foundation
1. Crear archivo `tac_bootstrap/interfaces/wizard.py`
2. Importar dependencias necesarias (Rich, domain models)
3. Crear console global Rich para output

### Phase 2: Core Implementation
1. Implementar `select_from_enum()` helper function
2. Implementar `_show_config_summary()` private helper
3. Implementar `run_init_wizard()` con flujo completo de configuración
4. Implementar `run_add_agentic_wizard()` con valores detectados

### Phase 3: Integration
1. Verificar importación desde CLI commands (no modificar CLI en esta tarea)
2. Validar que todos los enums y helpers se usen correctamente
3. Verificar manejo de SystemExit cuando usuario cancela

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create wizard.py module structure
- Crear archivo `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`
- Agregar docstring del módulo explicando propósito (usar Rich para wizard interactivo)
- Importar todas las dependencias necesarias:
  - `from pathlib import Path`
  - `from typing import Optional`
  - Rich imports: `Console, Panel, Prompt, Confirm, Table`
  - Domain model imports: todas las clases y enums necesarias de `tac_bootstrap.domain.models`
- Crear instancia global `console = Console()` para usar en todas las funciones

### Task 2: Implement select_from_enum() helper function
- Crear función `select_from_enum(prompt: str, enum_class, default=None, filter_fn=None) -> any`
- Docstring completo con descripción de parámetros y retorno
- Lógica:
  1. Construir lista de opciones desde enum_class
  2. Aplicar filter_fn si está presente (para filtrar frameworks/package managers válidos)
  3. Crear tabla Rich sin headers, con padding (0, 2)
  4. Iterar opciones con enumerate(options, 1) para numeración 1-indexed
  5. Marcar default con "[green]>[/green]" vs " "
  6. Imprimir prompt en bold y tabla
  7. Solicitar selección numérica con Prompt.ask, validando choices
  8. Retornar opción seleccionada (options[int(choice) - 1])

### Task 3: Implement _show_config_summary() private helper
- Crear función `_show_config_summary(config: TACConfig) -> None`
- Docstring explicando que muestra resumen en tabla Rich
- Crear Table con title="Configuration Summary", show_header=True
- Agregar columnas: "Setting" (cyan), "Value" (green)
- Agregar rows con config.project.name, language.value, framework.value, package_manager.value, architecture.value, commands (start, test), worktrees enabled
- Imprimir tabla con console.print(table)

### Task 4: Implement run_init_wizard() function
- Crear función con signature: `run_init_wizard(name: str, language: Optional[Language] = None, framework: Optional[Framework] = None, package_manager: Optional[PackageManager] = None, architecture: Optional[Architecture] = None) -> TACConfig`
- Docstring completo explicando parámetros opcionales (None = ask user, value = skip asking)
- Panel de bienvenida usando Panel.fit con título "🚀 TAC Bootstrap Wizard" y mensaje personalizado con nombre del proyecto
- Flujo paso a paso:
  1. Language (si None): `select_from_enum` con default=Language.PYTHON, luego print checkmark
  2. Framework (si None): `select_from_enum` con filter_fn=lambda f: f in get_frameworks_for_language(language), default=Framework.NONE
  3. Package Manager (si None): `select_from_enum` con filter_fn para managers válidos, default=first valid manager
  4. Architecture (si None): `select_from_enum` con default=Architecture.SIMPLE
  5. Commands: print header "[bold]Commands Configuration[/bold]", obtener defaults con get_default_commands(), hacer Prompt.ask para start/test/lint con defaults
  6. Worktrees: Confirm.ask con default=True
- Construir TACConfig con todos los valores recopilados
- Llamar `_show_config_summary(config)`
- Confirmación final con Confirm.ask("Proceed with this configuration?", default=True)
- Si no confirma: print "[yellow]Aborted.[/yellow]" y raise SystemExit(0)
- Retornar config

### Task 5: Implement run_add_agentic_wizard() function
- Crear función con signature: `run_add_agentic_wizard(repo_path: Path, detected: "DetectedProject") -> TACConfig`
- Docstring explicando que usa valores detectados como defaults
- Panel informativo usando Panel.fit con título "🔧 TAC Bootstrap Wizard" y mensaje sobre agregar a proyecto existente
- Flujo de configuración:
  1. Language: `select_from_enum` con default=detected.language y prompt "(detected)"
  2. Framework: `select_from_enum` con default=detected.framework, filtrado por language
  3. Package Manager: `select_from_enum` con default=detected.package_manager, filtrado
  4. Commands: print header + hint sobre uso en Claude Code/ADW
     - Obtener default_commands con get_default_commands()
     - Prompt para start: default=detected.commands.get("start", default_commands.get("start", ""))
     - Prompt para test, lint, build con misma lógica
  5. Worktrees: Confirm.ask con default=True
- Construir TACConfig con mode=ProjectMode.EXISTING, repo_root=str(repo_path), name=repo_path.name, app_root=detected.app_root or "src"
- Llamar `_show_config_summary(config)`
- Confirmación final igual que init wizard
- Retornar config

### Task 6: Validate module imports and type hints
- Verificar que todos los imports estén correctos
- Verificar que type hints sean precisos (usar "DetectedProject" en string para forward reference)
- Verificar que no hay errores de sintaxis con: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard, run_add_agentic_wizard; print('OK')"`

### Task 7: Run validation commands
- Ejecutar todos los comandos de validación para asegurar cero regresiones
- Si hay errores de type checking, ajustar según sea necesario
- Verificar que el módulo se puede importar sin errores

## Testing Strategy

### Unit Tests

Esta tarea NO requiere tests unitarios formales porque:
- Las funciones wizard son principalmente interactivas (requieren input de usuario)
- La validación real ocurre cuando los comandos CLI llaman al wizard
- Testing manual es más apropiado para UX/UI interactiva

### Manual Testing

Para testing manual (DESPUÉS de implementar ScaffoldService en TAREA 5):
```bash
# Test init wizard
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
uv run tac-bootstrap init test-project

# Test add-agentic wizard (después de FASE 6 DetectService)
# uv run tac-bootstrap add-agentic /path/to/repo
```

### Edge Cases

Casos edge a considerar en implementación:
1. **Usuario cancela wizard**: Debe hacer SystemExit(0) limpiamente con mensaje yellow
2. **Enum vacío después de filtrado**: No debe ocurrir si helpers son correctos (get_frameworks_for_language siempre retorna al menos [Framework.NONE])
3. **Default no está en opciones filtradas**: select_from_enum debe manejar con default_num = 1 si default not in options
4. **Valores None en detected.commands**: Usar dict.get() con fallback a default_commands.get() con fallback a ""

## Acceptance Criteria

✓ `select_from_enum()` muestra opciones numeradas en tabla Rich con marker visual para default
✓ `select_from_enum()` valida que selección numérica esté en rango de opciones
✓ `select_from_enum()` soporta filter_fn para filtrar opciones válidas
✓ `run_init_wizard()` guía flujo completo: Language → Framework → Package Manager → Architecture → Commands → Worktrees
✓ `run_init_wizard()` muestra checkmarks (✓) después de cada paso completado
✓ `run_init_wizard()` usa defaults inteligentes de `get_default_commands()` para commands
✓ `run_init_wizard()` respeta valores pre-seleccionados (skip asking si no es None)
✓ `run_add_agentic_wizard()` usa valores detectados como defaults en todos los prompts
✓ `run_add_agentic_wizard()` permite override de valores detectados
✓ `run_add_agentic_wizard()` construye config con mode=EXISTING y repo_root correcto
✓ `_show_config_summary()` muestra tabla formateada con colores (cyan/green)
✓ Ambos wizards muestran confirmación final antes de retornar config
✓ Si usuario no confirma, wizards hacen SystemExit(0) con mensaje yellow "Aborted."
✓ UI es clara, bonita, y user-friendly con Rich (paneles, colores, tablas)
✓ Módulo se importa sin errores

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

```bash
# Navigate to CLI directory
cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli

# Test import
uv run python -c "
from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard, run_add_agentic_wizard
from tac_bootstrap.domain.models import Language
print('Wizard module loaded successfully')
"

# Run unit tests
uv run pytest tests/ -v --tb=short

# Run linting
uv run ruff check .

# Run type checking
uv run mypy tac_bootstrap/

# Smoke test CLI
uv run tac-bootstrap --help
```

## Notes

### Implementation Notes

1. **NO implementar en esta tarea**:
   - Lógica de scaffolding (FASE 5 - ScaffoldService)
   - Lógica de detección (FASE 6 - DetectService)
   - Modificaciones a CLI commands (ya están preparados para llamar wizard)

2. **Type hint forward reference**:
   - Usar `detected: "DetectedProject"` en string para evitar import circular
   - DetectedProject será definido en FASE 6

3. **Rich best practices**:
   - Usar Panel.fit para mensajes de bienvenida (auto-size)
   - Usar Table sin headers para listas de opciones (más limpio)
   - Usar colores consistentes: cyan para labels, green para valores/success, yellow para warnings
   - Usar emojis moderadamente en títulos (🚀, 🔧, ✓)

4. **Default selection logic**:
   ```python
   # Correcto: maneja cuando default no está en opciones filtradas
   default_num = options.index(default) + 1 if default in options else 1
   ```

5. **Command defaults fallback chain**:
   ```python
   # Correcto: triple fallback para robustez
   detected.commands.get("start", default_commands.get("start", ""))
   ```

### Future Enhancements (NO para esta tarea)

- Multi-select para features opcionales (testing frameworks, CI/CD, etc.)
- Validación async de comandos (verificar que existen en PATH)
- Preview de estructura de directorios antes de crear
- Wizard navigation (back/forward entre pasos)
- Guardar presets de configuración para re-uso

### Dependencies Summary

**Production dependencies** (ya instaladas):
- `rich>=13.7.0` - Para UI de terminal (Console, Panel, Prompt, Confirm, Table)
- `pydantic>=2.5.0` - Para modelos de dominio (TACConfig, enums)

**NO requiere nuevas dependencias**.
