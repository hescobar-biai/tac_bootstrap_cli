# Feature: Actualizar settings.json.j2 con hooks adicionales integrados

## Metadata
issue_number: `310`
adw_id: `feature_Tac_10_task_5`
issue_json: `{"number":310,"title":"Actualizar settings.json.j2 con hooks adicionales integrados","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_10_task_5\n\n- **Descripción**: Modificar el template de settings.json para incluir todos los hooks de TAC-10 integrados con universal_hook_logger y context_bundle_builder.\n- **Archivos**:\n  - Template Jinja2: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`\n  - Archivo directo: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`\n- **Cambios**:\n  - Agregar hook UserPromptSubmit con context_bundle_builder --type user_prompt\n  - Agregar hook SubagentStop con universal_hook_logger\n  - Agregar hook Notification con universal_hook_logger\n  - Agregar hook PreCompact con universal_hook_logger\n  - Agregar hook SessionStart con universal_hook_logger\n  - Agregar hook SessionEnd con universal_hook_logger\n  - Modificar PreToolUse para incluir universal_hook_logger antes de pre_tool_use.py\n  - Modificar PostToolUse para incluir context_bundle_builder con matcher \"Read|Write\"\n  - Modificar Stop para incluir universal_hook_logger antes de stop.py\n- **Nota**: Aplicar cambios en ambos archivos simultáneamente\n\n"}`

## Feature Description
Esta feature actualiza el sistema de hooks en TAC Bootstrap para integrar dos nuevas herramientas de logging y tracking: `universal_hook_logger` y `context_bundle_builder`. Estas herramientas permiten:

1. **universal_hook_logger**: Registra TODOS los eventos de hooks en archivos JSONL para auditoría, debugging y análisis de workflows
2. **context_bundle_builder**: Rastrea operaciones de archivos (Read, Write, Edit) para recuperación de contexto entre sesiones

Los cambios deben aplicarse tanto al template Jinja2 (`settings.json.j2`) que se usa para generar proyectos nuevos, como al archivo directo `.claude/settings.json` que controla el comportamiento del propio repositorio TAC Bootstrap.

## User Story
As a TAC Bootstrap user
I want comprehensive logging and context tracking for all Claude Code sessions
So that I can debug workflows, audit agent actions, and maintain session context for recovery

## Problem Statement
El sistema actual de hooks en TAC Bootstrap tiene logging fragmentado:
- Algunos hooks tienen logging personalizado (e.g., `stop.py --chat`)
- No hay logging centralizado de eventos de hooks
- No hay tracking automático de operaciones de archivos
- Dificulta el debugging de workflows complejos
- No hay forma de recuperar contexto de sesiones anteriores

## Solution Statement
Integrar `universal_hook_logger` y `context_bundle_builder` en todos los hooks relevantes mediante:

1. **Chaining de comandos**: Usar `&&` para ejecutar múltiples scripts en un solo hook
2. **Event identification**: Pasar `--event <HookName>` a universal_hook_logger para identificar el evento
3. **Matcher patterns**: Usar `--matcher "Read|Write"` en context_bundle_builder para filtrar tools
4. **Dual updates**: Aplicar cambios idénticos a `.claude/settings.json` y `settings.json.j2`

Esta solución preserva la funcionalidad existente mientras agrega logging/tracking transparente.

## Relevant Files
Archivos necesarios para implementar la feature:

- `.claude/settings.json` (líneas 1-102) - Configuración de hooks del repositorio actual
  - **Por qué es relevante**: Archivo directo que se debe actualizar con los nuevos hooks
  - **Estado actual**: Tiene hooks PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` (líneas 1-58) - Template para proyectos generados
  - **Por qué es relevante**: Template Jinja2 que genera settings.json en proyectos nuevos
  - **Estado actual**: Versión mínima con solo PreToolUse, PostToolUse, Stop
  - **Nota**: Usa variable `{{ config.project.package_manager.value }}` para package manager

- `.claude/hooks/universal_hook_logger.py` (líneas 0-49+) - Script de logging universal
  - **Por qué es relevante**: Script que se ejecutará en los hooks para logging
  - **Recibe**: `--event <HookName>` como argumento para identificar el evento

- `.claude/hooks/context_bundle_builder.py` (líneas 0-49+) - Script de tracking de archivos
  - **Por qué es relevante**: Script que rastrea operaciones de archivos
  - **Recibe**: `--type <type>` y `--matcher <pattern>` como argumentos

### New Files
No se crean archivos nuevos. Solo se modifican archivos existentes.

## Implementation Plan

### Phase 1: Foundation
1. Leer ambos archivos settings completamente para entender estructura actual
2. Verificar que scripts universal_hook_logger.py y context_bundle_builder.py existan
3. Identificar diferencias entre settings.json y settings.json.j2

### Phase 2: Core Implementation
4. Actualizar `.claude/settings.json` con todos los hooks integrados
5. Actualizar `settings.json.j2` con hooks idénticos pero usando variables Jinja2

### Phase 3: Integration
6. Validar sintaxis JSON de ambos archivos
7. Verificar que paths relativos sean correctos
8. Confirmar que comandos usen sintaxis correcta de chaining

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and Analyze Current State
- Leer `.claude/settings.json` completo
- Leer `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` completo
- Verificar existencia de `.claude/hooks/universal_hook_logger.py`
- Verificar existencia de `.claude/hooks/context_bundle_builder.py`
- Documentar diferencias estructurales entre ambos archivos

### Task 2: Update .claude/settings.json with Integrated Hooks
Modificar `.claude/settings.json` aplicando los siguientes cambios:

**Modificar hooks existentes:**
- **PreToolUse**: Agregar chaining para ejecutar `universal_hook_logger --event PreToolUse &&` antes de `pre_tool_use.py`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
  ```

- **PostToolUse**: Modificar para incluir `context_bundle_builder` con matcher "Read|Write"
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type post_tool_use --matcher \"Read|Write\" && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py || true"
  ```

- **Stop**: Agregar chaining para ejecutar `universal_hook_logger --event Stop &&` antes de `stop.py`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event Stop && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/stop.py --chat || true"
  ```

**Agregar/modificar hooks nuevos:**
- **UserPromptSubmit**: Modificar para usar `context_bundle_builder --type user_prompt` EN LUGAR de `user_prompt_submit.py --log-only`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type user_prompt || true"
  ```

- **SubagentStop**: Modificar para agregar `universal_hook_logger --event SubagentStop &&` antes de `subagent_stop.py`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SubagentStop && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/subagent_stop.py || true"
  ```

- **Notification**: Modificar para agregar `universal_hook_logger --event Notification &&` antes de `notification.py`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event Notification && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/notification.py --notify || true"
  ```

- **PreCompact**: Modificar para agregar `universal_hook_logger --event PreCompact &&` antes de `pre_compact.py`
  ```json
  "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreCompact && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_compact.py || true"
  ```

- **SessionStart** (NUEVO): Agregar hook con solo `universal_hook_logger --event SessionStart`
  ```json
  "SessionStart": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SessionStart || true"
        }
      ]
    }
  ]
  ```

- **SessionEnd** (NUEVO): Agregar hook con solo `universal_hook_logger --event SessionEnd`
  ```json
  "SessionEnd": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SessionEnd || true"
        }
      ]
    }
  ]
  ```

### Task 3: Update settings.json.j2 Template with Same Hooks
Modificar `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` con los MISMOS hooks que Task 2, pero usando la variable Jinja2 `{{ config.project.package_manager.value }}` en lugar de `uv`.

**Ejemplo de conversión:**
```json
// settings.json usa:
"command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"

// settings.json.j2 debe usar:
"command": "{{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && {{ config.project.package_manager.value }} run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
```

Agregar TODOS los hooks de Task 2 al template (PreToolUse, PostToolUse, Stop, UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd).

### Task 4: Validate JSON Syntax
- Validar sintaxis JSON de `.claude/settings.json` usando `python -m json.tool`
- Validar que `settings.json.j2` sea JSON válido (ignorando sintaxis Jinja2)
- Confirmar que todos los hooks tengan estructura correcta:
  - Cada hook tiene `matcher`, `hooks`, `type`, `command`
  - Comandos terminan con `|| true` para error handling
  - Escapado correcto de comillas en `--matcher \"Read|Write\"`

### Task 5: Test Hook Execution (Manual Verification)
- Verificar que paths relativos `.claude/hooks/*.py` sean accesibles
- Confirmar que `$CLAUDE_PROJECT_DIR` se expanda correctamente
- Revisar que orden de ejecución sea correcto (logger primero, luego script original)

### Task 6: Run Validation Commands
Ejecutar los siguientes comandos para validar sin regresiones:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verificar que:
- Todos los tests pasen (0 failures)
- No haya errores de linting
- No haya errores de type checking
- El CLI funcione sin errores

## Testing Strategy

### Unit Tests
No se requieren nuevos unit tests porque:
- Los cambios son configuración JSON/Jinja2, no código Python
- Los scripts `universal_hook_logger.py` y `context_bundle_builder.py` ya existen y tienen sus propios tests
- La validación se hace mediante JSON syntax check y smoke test del CLI

### Edge Cases
1. **Escapado de comillas**: Verificar que `--matcher \"Read|Write\"` se preserve correctamente en JSON
2. **Chaining de comandos**: Confirmar que `&&` funcione para ejecutar múltiples scripts
3. **Error handling**: Verificar que `|| true` permita que hooks fallen sin bloquear workflow
4. **Variables Jinja2**: Confirmar que `{{ config.project.package_manager.value }}` se renderice correctamente
5. **Hooks nuevos**: Verificar que SessionStart y SessionEnd no causen conflictos

## Acceptance Criteria
1. `.claude/settings.json` contiene TODOS los hooks especificados (9 total: PreToolUse, PostToolUse, Stop, UserPromptSubmit, SubagentStop, Notification, PreCompact, SessionStart, SessionEnd)
2. `settings.json.j2` contiene los MISMOS hooks con sintaxis Jinja2 para package manager
3. Hooks modificados (PreToolUse, PostToolUse, Stop) ejecutan universal_hook_logger ANTES del script original
4. UserPromptSubmit usa context_bundle_builder con `--type user_prompt`
5. PostToolUse usa context_bundle_builder con `--matcher "Read|Write"`
6. Hooks nuevos (SubagentStop, Notification, PreCompact) ejecutan universal_hook_logger + script original
7. Hooks SessionStart y SessionEnd ejecutan SOLO universal_hook_logger
8. Ambos archivos tienen JSON sintácticamente válido
9. Todos los validation commands pasan sin errores
10. No hay regresiones en tests existentes

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `python -m json.tool .claude/settings.json > /dev/null` - JSON validation
- `cat tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2 | grep -v "{{" | python -m json.tool > /dev/null || echo "Template válido"` - Template validation

## Notes

### Decisiones de Implementación
1. **Chaining vs Separate Hooks**: Se decidió usar `&&` para encadenar comandos en lugar de múltiples hook entries porque garantiza orden de ejecución y simplifica la configuración.

2. **Event Identification**: Cada llamada a `universal_hook_logger` incluye `--event <HookName>` para identificar el evento en los logs, facilitando debugging.

3. **Package Manager Abstraction**: El template `settings.json.j2` usa `{{ config.project.package_manager.value }}` para soportar múltiples package managers (uv, npm, etc.).

4. **UserPromptSubmit Change**: Se reemplaza `user_prompt_submit.py --log-only` por `context_bundle_builder.py --type user_prompt` porque el nuevo builder ofrece mejor tracking de contexto.

5. **Error Handling**: Todos los hooks terminan con `|| true` para asegurar que fallos en logging no bloqueen el workflow del usuario.

### Consideraciones Futuras
- Evaluar agregar hook `SessionResume` si Claude Code lo soporta en el futuro
- Considerar agregar `--verbose` flag a universal_hook_logger para debugging
- Posible configuración de paths de output para logs (actualmente hardcoded en scripts)

### Referencias
- Auto-Resolved Clarifications: Decisiones sobre paths relativos, chaining, argumentos CLI
- `.claude/hooks/universal_hook_logger.py`: Implementación del logger universal
- `.claude/hooks/context_bundle_builder.py`: Implementación del builder de contexto
