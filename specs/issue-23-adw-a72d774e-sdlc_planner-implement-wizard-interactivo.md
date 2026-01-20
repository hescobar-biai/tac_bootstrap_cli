# Feature: Implement Interactive Wizard with Rich

## Metadata
issue_number: `23`
adw_id: `a72d774e`
issue_json: `{"number":23,"title":"TAREA 4.2: Implementar wizard interactivo con Rich","body":" Prompt para Agente\n\n## Contexto\nLa CLI ya tiene los comandos basicos. Ahora necesitamos implementar el wizard\ninteractivo que guia al usuario para configurar el proyecto paso a paso.\n\nEl wizard usa Rich para:\n- Prompts interactivos con opciones\n- Colores y formateo bonito\n- Confirmacion antes de ejecutar\n\n## Objetivo\nCrear el modulo wizard.py con funciones para guiar la configuracion interactiva.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`"}`

## Feature Description

Implementar un wizard interactivo usando Rich que guía al usuario paso a paso en la configuración de proyectos TAC Bootstrap. El wizard proporciona una experiencia user-friendly con opciones numeradas, defaults inteligentes basados en detección automática, tablas visuales de resumen, y confirmación antes de proceder.

Esta feature transforma la experiencia CLI de comandos con flags a una conversación guiada que reduce errores de configuración y mejora la usabilidad para usuarios nuevos.

## User Story

As a **developer using TAC Bootstrap for the first time**
I want to **be guided through project configuration interactively**
So that **I don't need to memorize all CLI flags and can make informed decisions with visual context**

## Problem Statement

Los comandos CLI `init` y `add-agentic` actualmente tienen modo `--interactive` que está implementado como placeholder. Los usuarios deben:
1. Conocer todos los flags disponibles (`--language`, `--framework`, `--package-manager`, etc.)
2. Recordar qué frameworks son válidos para cada lenguaje
3. Saber qué package managers están disponibles para su stack
4. Configurar comandos manualmente sin defaults contextuales
5. No tienen preview visual de la configuración antes de proceder

Esto crea fricción especialmente para usuarios nuevos que no están familiarizados con todas las opciones disponibles.

## Solution Statement

Implementar módulo `wizard.py` con funciones interactivas usando Rich:

1. **`select_from_enum()`**: Función helper para selección interactiva de enums
   - Muestra opciones numeradas en tabla formateada
   - Soporta valores default con indicador visual
   - Permite filtrado de opciones válidas por contexto
   - Valida input del usuario y retorna enum value

2. **`run_init_wizard()`**: Wizard para proyectos nuevos
   - Panel de bienvenida con título y descripción
   - Selección guiada de language → framework → package manager → architecture
   - Prompts para comandos con defaults inteligentes basados en selecciones previas
   - Pregunta sobre worktrees con explicación
   - Tabla de resumen de configuración final
   - Confirmación antes de proceder

3. **`run_add_agentic_wizard()`**: Wizard para proyectos existentes
   - Panel explicativo sobre inyección de Agentic Layer
   - Muestra valores detectados automáticamente como defaults
   - Permite override de detección con selección interactiva
   - Enfoque especial en configuración de comandos (crítico para proyectos existentes)
   - Tabla de resumen y confirmación

4. **`_show_config_summary()`**: Helper privado para mostrar resumen
   - Tabla Rich con configuración completa
   - Columnas: Setting | Value
   - Formato consistente y fácil de leer

El wizard usa Rich para:
- Paneles con títulos y bordes de colores
- Tablas formateadas para opciones y resumen
- Prompts con defaults claros
- Confirmaciones (Yes/No)
- Checkmarks (✓) para pasos completados
- Mensajes de error/warning coloridos

## Relevant Files

Archivos necesarios para implementar la feature:

- **tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py** - Comandos CLI que invocarán el wizard cuando `--interactive=True`
- **tac_bootstrap_cli/tac_bootstrap/domain/models.py** - Modelos Pydantic (TACConfig, Language, Framework, enums) y helper functions (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
- **tac_bootstrap_cli/pyproject.toml** - Verificar que `rich>=13.7.0` está instalado

### New Files

Esta tarea crea un archivo nuevo:
- `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py` - Módulo de wizard interactivo

### Dependencies on Helper Functions

El wizard depende de helper functions existentes en `domain/models.py`:
- `get_frameworks_for_language(language: Language) -> List[Framework]` - Filtra frameworks válidos
- `get_package_managers_for_language(language: Language) -> List[PackageManager]` - Filtra package managers válidos
- `get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]` - Obtiene comandos default contextuales

### Type Stub for DetectedProject

El wizard usa un tipo `DetectedProject` que NO existe aún (se implementará en FASE 6). Para esta tarea, usar type hint como string:
```python
def run_add_agentic_wizard(
    repo_path: Path,
    detected: "DetectedProject",
) -> TACConfig:
    ...
```

Esto permite que el type checker acepte el código sin implementar DetectService.

## Implementation Plan

### Phase 1: Foundation
1. Crear archivo `wizard.py` en `tac_bootstrap_cli/tac_bootstrap/interfaces/`
2. Importar dependencias necesarias de Rich y domain models
3. Crear instancia global de Rich Console
4. Implementar función helper `select_from_enum()` con tabla formateada

### Phase 2: Core Implementation
1. Implementar `run_init_wizard()` para nuevos proyectos
   - Wizard completo paso a paso con todos los prompts
   - Construcción de TACConfig desde respuestas
   - Integración con helper functions para defaults
2. Implementar `run_add_agentic_wizard()` para proyectos existentes
   - Similar a init pero con detected settings como defaults
   - Enfoque en comandos que son críticos para proyectos existentes
3. Implementar `_show_config_summary()` para preview visual

### Phase 3: Integration
1. Verificar que todos los parámetros opcionales tienen defaults apropiados
2. Agregar manejo de abort (SystemExit(0)) cuando usuario cancela confirmación
3. Validar que el output es claro y user-friendly con Rich
4. Verificar integración con modelos de dominio (TACConfig construction)

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create Wizard Module and Helper Function
- Crear archivo `tac_bootstrap_cli/tac_bootstrap/interfaces/wizard.py`
- Agregar docstring del módulo explicando propósito y uso de Rich
- Importar todas las dependencias necesarias:
  - `from pathlib import Path`
  - `from typing import Optional`
  - `from rich.console import Console`
  - `from rich.panel import Panel`
  - `from rich.prompt import Prompt, Confirm`
  - `from rich.table import Table`
  - Todos los modelos de dominio y helper functions
- Crear instancia global `console = Console()`
- Implementar `select_from_enum()`:
  - Recibe: prompt (str), enum_class, default (optional), filter_fn (optional)
  - Convierte enum a lista y aplica filter_fn si existe
  - Construye tabla Rich sin header con opciones numeradas
  - Marca default con indicador visual `[green]>[/green]`
  - Imprime prompt y tabla
  - Usa `Prompt.ask()` con validación de choices
  - Retorna enum value seleccionado

### Task 2: Implement Init Wizard
- Implementar función `run_init_wizard()` con signature:
  ```python
  def run_init_wizard(
      name: str,
      language: Optional[Language] = None,
      framework: Optional[Framework] = None,
      package_manager: Optional[PackageManager] = None,
      architecture: Optional[Architecture] = None,
  ) -> TACConfig:
  ```
- Imprimir Panel de bienvenida con Rich formatting
- Implementar flujo de 6 pasos:
  1. **Language**: Si `None`, llamar `select_from_enum()` con default=PYTHON, sino usar valor provisto
     - Imprimir checkmark verde después de selección
  2. **Framework**: Si `None`, llamar `select_from_enum()` filtrando con `get_frameworks_for_language()`
     - Usar default=NONE
  3. **Package Manager**: Si `None`, llamar `select_from_enum()` filtrando con `get_package_managers_for_language()`
     - Usar primer válido como default
  4. **Architecture**: Si `None`, llamar `select_from_enum()` con default=SIMPLE
  5. **Commands Configuration**:
     - Obtener `default_commands = get_default_commands(language, package_manager)`
     - Usar `Prompt.ask()` para start, test, lint con defaults apropiados
  6. **Worktrees**: Usar `Confirm.ask()` preguntando si enable worktrees (default=True)
- Construir objeto `TACConfig` con todos los valores recolectados
- Llamar `_show_config_summary(config)`
- Usar `Confirm.ask()` para confirmación final
- Si usuario no confirma, imprimir warning amarillo y ejecutar `raise SystemExit(0)`
- Si confirma, retornar `config`

### Task 3: Implement Add Agentic Wizard
- Implementar función `run_add_agentic_wizard()` con signature:
  ```python
  def run_add_agentic_wizard(
      repo_path: Path,
      detected: "DetectedProject",
  ) -> TACConfig:
  ```
- Imprimir Panel de bienvenida explicando inyección en proyecto existente
- Implementar flujo similar a init pero usando `detected` como defaults:
  1. **Language**: Llamar `select_from_enum()` con `default=detected.language`
  2. **Framework**: Llamar `select_from_enum()` con `default=detected.framework or Framework.NONE`
  3. **Package Manager**: Llamar `select_from_enum()` con `default=detected.package_manager`
  4. **Commands Configuration** (más completo que init):
     - Imprimir header explicando importancia de comandos
     - Prompts para: start, test, lint, build
     - Usar `detected.commands.get(key, default)` como fallback a `get_default_commands()`
  5. **Worktrees**: Similar a init
- Construir `TACConfig` con `mode=ProjectMode.EXISTING` y `repo_root=str(repo_path)`
- Usar `app_root=detected.app_root or "src"`
- Llamar `_show_config_summary()` y confirmación
- Retornar config o abortar

### Task 4: Implement Config Summary Helper
- Implementar función privada `_show_config_summary(config: TACConfig) -> None`
- Crear tabla Rich con título "Configuration Summary"
- Agregar columnas: "Setting" (cyan) y "Value" (green)
- Agregar rows para:
  - Project Name
  - Language (usar .value)
  - Framework (usar .value)
  - Package Manager (usar .value)
  - Architecture (usar .value)
  - Start Command
  - Test Command
  - Worktrees Enabled (convertir bool a str)
- Imprimir tabla con `console.print(table)`

### Task 5: Validate and Test Module
- Verificar que todos los imports son correctos
- Verificar que type hints usan string literal para `"DetectedProject"`
- Verificar que Rich formatting es consistente (colores, panels, tables)
- Verificar que defaults funcionan correctamente con helper functions
- Ejecutar validation commands (último paso):
  - `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.interfaces.wizard import select_from_enum, run_init_wizard; from tac_bootstrap.domain.models import Language; print('Wizard module loaded successfully')"`
  - `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
  - `cd tac_bootstrap_cli && uv run ruff check .`
  - `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
  - `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests

Tests unitarios necesarios (a crear en `tests/interfaces/test_wizard.py`):

1. **Test `select_from_enum()`**:
   - Mock `console.print` y `Prompt.ask` para simular input
   - Verificar que retorna enum correcto basado en selección numérica
   - Verificar que filtrado funciona correctamente con filter_fn
   - Verificar que default se marca visualmente en tabla

2. **Test `run_init_wizard()`**:
   - Mock todos los prompts de Rich
   - Verificar que TACConfig se construye correctamente con valores ingresados
   - Verificar que defaults se usan cuando parámetros son None
   - Verificar que confirmación=No resulta en SystemExit(0)

3. **Test `run_add_agentic_wizard()`**:
   - Similar a init pero con detected settings como mocks
   - Verificar que mode=EXISTING y repo_root se configuran correctamente

4. **Test `_show_config_summary()`**:
   - Mock console.print
   - Verificar que tabla contiene todas las filas esperadas
   - Verificar formato de valores (.value para enums)

### Edge Cases

Casos edge a probar:

1. **Todos los parámetros pre-seleccionados**: Wizard no debe preguntar lo que ya está configurado
2. **Usuario selecciona opción inválida**: Prompt.ask debe validar choices y rechazar input malo
3. **Filter resulta en lista vacía**: Manejar caso donde no hay opciones válidas (no debería ocurrir con helpers correctos)
4. **Confirmación cancelada**: Usuario dice No → SystemExit(0) limpio
5. **Comandos vacíos**: Algunos comandos opcionales pueden ser string vacío (lint, build)
6. **Framework NONE**: Es válido y debe manejarse correctamente

### Manual Testing

Pruebas manuales interactivas (no automatizadas):

```bash
# Test wizard completo en modo init
cd tac_bootstrap_cli
uv run tac-bootstrap init test-project --interactive

# Probar selecciones:
# - Language: TypeScript
# - Framework: NextJS
# - Package Manager: pnpm
# - Architecture: Layered
# - Verificar que defaults de comandos son correctos para pnpm

# Test wizard en add-agentic requerirá DetectService (FASE 6)
```

## Acceptance Criteria

1. ✓ `select_from_enum()` muestra opciones numeradas en tabla Rich formateada
2. ✓ `select_from_enum()` marca el default visualmente con `[green]>[/green]`
3. ✓ `select_from_enum()` filtra opciones correctamente usando filter_fn
4. ✓ `run_init_wizard()` guía paso a paso con 6 prompts secuenciales
5. ✓ `run_init_wizard()` usa helper functions para defaults inteligentes basados en selecciones previas
6. ✓ `run_init_wizard()` construye TACConfig válido con todos los valores
7. ✓ `run_add_agentic_wizard()` usa valores detectados como defaults en cada prompt
8. ✓ `run_add_agentic_wizard()` incluye prompt para build command (adicional vs init)
9. ✓ `run_add_agentic_wizard()` configura mode=EXISTING y repo_root correctamente
10. ✓ `_show_config_summary()` muestra tabla clara con todos los settings clave
11. ✓ Confirmación final permite abortar limpiamente con SystemExit(0)
12. ✓ UI es clara, colorida, y user-friendly con Rich panels y tables
13. ✓ Checkmarks (✓) aparecen después de cada selección para feedback visual
14. ✓ Mensajes de warning/error usan colores apropiados ([yellow], [red])
15. ✓ Type hints correctos incluyendo string literal para "DetectedProject"
16. ✓ Module pasa mypy, ruff, y pytest sin errores

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

# Test 6: Verificar que wizard funciona con init (manual test recomendado pero opcional)
# cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli
# uv run tac-bootstrap init test-wizard-project --interactive
```

## Notes

### Integration with CLI Commands

Una vez implementado wizard.py, los comandos CLI necesitarán actualización para invocar el wizard:

En `cli.py`, actualizar:
```python
# ANTES (placeholder):
if interactive:
    console.print("[yellow]Interactive wizard not yet implemented[/yellow]")
    raise typer.Exit(1)

# DESPUÉS:
if interactive:
    from tac_bootstrap.interfaces.wizard import run_init_wizard
    config = run_init_wizard(
        name=name,
        language=language if language != Language.PYTHON else None,
        framework=framework if framework != Framework.NONE else None,
        package_manager=package_manager,
        architecture=architecture if architecture != Architecture.SIMPLE else None,
    )
    # Continuar con config...
```

Esta integración puede hacerse en una tarea de seguimiento o inmediatamente después de implementar wizard.py.

### Rich UI Best Practices

El wizard sigue estas prácticas para UX óptima:
- **Paneles** para secciones importantes (bienvenida, resumen)
- **Tablas** para opciones y configuración final
- **Colores semánticos**: green=success, yellow=warning, red=error, cyan=info, dim=secondary
- **Checkmarks** para feedback de progreso
- **Defaults claros** en cada prompt
- **Confirmación final** antes de acciones destructivas

### Future Enhancements

Mejoras futuras (fuera de scope de esta tarea):
1. Agregar modo `--expert` que hace preguntas avanzadas (safety config, model policy)
2. Guardar configuración común del usuario en `~/.tac-bootstrap/defaults.yml`
3. Wizard para comando `doctor --fix` que pregunta cómo resolver cada issue
4. Preview de archivos que se crearán antes de confirmación final
5. Integración con PlainTextFiles MCP para preview de templates renderizados

### Dependencies Not Implemented Yet

Esta tarea NO requiere implementar:
- **ScaffoldService** (FASE 5) - El wizard solo construye TACConfig
- **DetectService** (FASE 6) - `run_add_agentic_wizard()` usa type hint string literal
- **DoctorService** (FASE 7) - No usado por wizard

El wizard es independiente de estos servicios y puede implementarse completamente ahora.

### No Hacer

- **NO implementar lógica de scaffolding** (generación de archivos) - eso es responsabilidad de ScaffoldService
- **NO implementar detección automática** (DetectService) - el wizard recibe detected settings como parámetro
- **NO crear tests de integración E2E** - solo tests unitarios mocking Rich prompts
- **NO agregar opciones CLI nuevas** - solo implementar el módulo wizard.py
- **NO modificar modelos de dominio** - usar lo que ya existe en models.py

### Documentation Updates Needed

Después de implementar esta tarea, actualizar:
- `app_docs/` con documento `feature-a72d774e-wizard-interactivo.md` explicando el wizard
- `.claude/commands/conditional_docs.md` agregando condiciones para leer wizard docs
- README principal mencionando modo interactivo como feature destacada

Estas actualizaciones pueden hacerse en tarea de seguimiento.
