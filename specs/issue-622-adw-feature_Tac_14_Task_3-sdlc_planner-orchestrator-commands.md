# Feature: Implementar Orchestrator Commands (BASE + TEMPLATES)

## Metadata
issue_number: `622`
adw_id: `feature_Tac_14_Task_3`
issue_json: `{"number": 622, "title": "Implementar Orchestrator Commands (BASE + TEMPLATES)", "body": "..."}`

## Feature Description
Crear 5 comandos slash de orquestación multi-agente en BASE (.claude/commands/) y sus templates Jinja2 correspondientes en el CLI (tac_bootstrap/templates/). Estos comandos permitirán workflows de orquestación avanzados siguiendo patrones TAC-10 Level 4 (Delegation Prompt) para:
- Plan with Scouts + Build + Review workflow completo
- Scout and Build workflow simplificado
- One-shot agent execution
- Parallel builds delegation
- Parallel subagents orchestration

Los comandos se integrarán con las nuevas agent definitions creadas en Tarea 2 y seguirán las convenciones existentes de YAML frontmatter y estructura de comandos.

## User Story
As a developer using TAC Bootstrap CLI
I want to have orchestrator commands for multi-agent workflows
So that I can leverage complex delegation patterns and parallel execution strategies in my Claude Code projects

## Problem Statement
El TAC Bootstrap CLI actualmente carece de comandos de orquestación multi-agente avanzados. Los patrones TAC-10 Level 4 requieren workflows complejos que coordinen múltiples agentes (scout, plan, build, review) de forma secuencial o paralela. Sin estos comandos, los usuarios deben orquestar manualmente cada fase, perdiendo eficiencia y consistencia.

Los comandos de orquestación existen en el repositorio TAC-14 original pero no están disponibles en:
1. BASE: El repositorio tac_bootstrap local (.claude/commands/)
2. TEMPLATES: Los templates del CLI para generación en nuevos proyectos

## Solution Statement
Implementar 5 comandos de orquestación siguiendo un patrón dual:

1. **Fase BASE**: Crear archivos .md en `.claude/commands/` del repositorio actual
   - Intentar copiar desde fuente original si existe: `/Volumes/MAc1/Celes/TAC/tac-14/.claude/commands/`
   - Si fuente no accesible, crear desde patrones existentes en este repo
   - Adaptar referencias a nueva estructura `.claude/agents/`
   - Validar YAML frontmatter (name, description, category, model, allowed-tools)

2. **Fase TEMPLATES**: Crear templates Jinja2 en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
   - Convertir cada .md a .md.j2
   - Parametrizar valores project-specific con `{{ config.* }}`
   - Mantener lógica de orquestación como contenido estático
   - Registrar en `scaffold_service.py::_add_claude_files()`

## Relevant Files
Archivos necesarios para implementar la feature:

### Existing Files
- `.claude/commands/build_in_parallel.md` - Patrón de parallel build delegation existente
- `.claude/commands/parallel_subagents.md` - Patrón de parallel subagents existente
- `.claude/commands/scout_plan_build.md` - Patrón de orchestration existente
- `.claude/commands/expert-orchestrate.md` - Patrón de expert workflow orchestration
- `.claude/agents/*.md` - Agent definitions para referencias
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:291-377` - Método `_add_claude_files()` para registro
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/*.md.j2` - Templates existentes como referencia

### New Files
**BASE** (.claude/commands/):
- `orch_plan_w_scouts_build_review.md` - Workflow completo: scout → plan → build → review
- `orch_scout_and_build.md` - Workflow simplificado: scout → build
- `orch_one_shot_agent.md` - One-shot agent execution pattern

**TEMPLATES** (tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/):
- `orch_plan_w_scouts_build_review.md.j2` - Template Jinja2 del workflow completo
- `orch_scout_and_build.md.j2` - Template Jinja2 del workflow simplificado
- `orch_one_shot_agent.md.j2` - Template Jinja2 del one-shot pattern

**MODIFIED**:
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Agregar registro de 3 nuevos templates (los 2 parallel ya existen)

## Implementation Plan

### Phase 1: Análisis y Preparación
- Leer comandos existentes de orquestación para entender patrones
- Verificar acceso a fuente original en `/Volumes/MAc1/Celes/TAC/tac-14/.claude/commands/`
- Analizar estructura de agent definitions en `.claude/agents/`
- Identificar pattern de YAML frontmatter de comandos existentes

### Phase 2: Crear Comandos BASE
- Crear 3 nuevos comandos .md en `.claude/commands/` (parallel_subagents y build_in_parallel ya existen)
- Adaptar referencias de agent invocations a `.claude/agents/` structure
- Validar YAML frontmatter consistency
- Asegurar patrones de orquestación correctos (sequential vs parallel)

### Phase 3: Crear Templates CLI
- Convertir 5 comandos a templates .md.j2 en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
- Parametrizar con variables `{{ config.project.name }}`, `{{ config.agentic.* }}`, etc.
- Mantener lógica de workflow estática
- Registrar en `scaffold_service.py::_add_claude_files()`

## Step by Step Tasks

### Task 1: Analizar Patrones Existentes
- Leer `.claude/commands/scout_plan_build.md` para entender orchestration pattern
- Leer `.claude/commands/expert-orchestrate.md` para expert workflow pattern
- Leer `.claude/commands/build_in_parallel.md` para parallel delegation pattern
- Leer `.claude/commands/parallel_subagents.md` para parallel subagents pattern
- Leer 2-3 templates `.md.j2` para identificar YAML frontmatter pattern
- Documentar: required fields (name, description, category, model, allowed-tools)

### Task 2: Verificar Estructura de Agents
- Listar archivos en `.claude/agents/` para confirmar agent definitions disponibles
- Identificar agent invocation syntax desde comandos existentes
- Documentar agentes disponibles: build-agent, planner, scout-report-suggest, etc.

### Task 3: Crear orch_plan_w_scouts_build_review.md en BASE
- Intentar leer desde `/Volumes/MAc1/Celes/TAC/tac-14/.claude/commands/orch_plan_w_scouts_build_review.md`
- Si no existe, crear desde scratch siguiendo pattern de `scout_plan_build.md`
- YAML frontmatter: name, description, category: "Orchestrator Commands", model, allowed-tools
- Workflow: Phase 1 (Scout) → Phase 2 (Plan) → Phase 3 (Build) → Phase 4 (Review)
- Adaptar referencias a `.claude/agents/scout-report-suggest.md`, `.claude/agents/planner.md`, `.claude/agents/build-agent.md`
- Usar Task tool con subagent_type para invocaciones
- Escribir archivo en `.claude/commands/orch_plan_w_scouts_build_review.md`

### Task 4: Crear orch_scout_and_build.md en BASE
- Intentar leer desde fuente original
- Si no existe, crear workflow simplificado: Scout → Build (sin Plan ni Review)
- YAML frontmatter siguiendo pattern establecido
- Workflow: Phase 1 (Scout) → Phase 2 (Build)
- Referencias a `.claude/agents/scout-report-suggest.md`, `.claude/agents/build-agent.md`
- Escribir archivo en `.claude/commands/orch_scout_and_build.md`

### Task 5: Crear orch_one_shot_agent.md en BASE
- Crear comando para one-shot agent execution pattern
- YAML frontmatter siguiendo pattern establecido
- Variables: AGENT_TYPE, TASK_DESCRIPTION
- Workflow: Validate agent type → Launch single agent → Report results
- Incluir validación de agent types disponibles
- Escribir archivo en `.claude/commands/orch_one_shot_agent.md`

### Task 6: Verificar Parallel Commands Existentes
- Confirmar que `build_in_parallel.md` existe en `.claude/commands/`
- Confirmar que `parallel_subagents.md` existe en `.claude/commands/`
- Validar YAML frontmatter consistency
- Si necesitan ajustes a nueva estructura, aplicar adaptaciones

### Task 7: Crear Templates Jinja2 (5 archivos)
- Copiar `.claude/commands/orch_plan_w_scouts_build_review.md` → `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/orch_plan_w_scouts_build_review.md.j2`
- Copiar `.claude/commands/orch_scout_and_build.md` → `.md.j2` equivalente
- Copiar `.claude/commands/orch_one_shot_agent.md` → `.md.j2` equivalente
- Copiar `.claude/commands/build_in_parallel.md` → `.md.j2` equivalente (si no existe)
- Copiar `.claude/commands/parallel_subagents.md` → `.md.j2` equivalente (si no existe)
- Parametrizar project-specific references:
  - `{{ config.project.name }}` donde aplique
  - `{{ config.agentic.* }}` para configuraciones de agentes
  - `{{ config.commands.* }}` para comandos
- Mantener workflow logic estática (no parametrizar orchestration steps)

### Task 8: Registrar Templates en scaffold_service.py
- Abrir `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Ubicar método `_add_claude_files()` (línea ~291)
- Ubicar lista `commands` (línea ~310)
- Verificar si `build_in_parallel` y `parallel_subagents` ya están registrados
- Agregar 3 nuevos comandos a la lista:
  ```python
  "orch_plan_w_scouts_build_review",
  "orch_scout_and_build",
  "orch_one_shot_agent",
  ```
- Asegurar orden alfabético o lógico en la lista
- El loop existente (`for cmd in commands:`) generará automáticamente los file operations

### Task 9: Validación Final
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .`
- Ejecutar `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Verificar manualmente que los 5 archivos .md existen en `.claude/commands/`
- Verificar que los 5 templates .md.j2 existen en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
- Verificar que scaffold_service.py tiene las 3 nuevas entradas en la lista

## Testing Strategy

### Unit Tests
- No se requieren nuevos tests unitarios (templates son contenido estático)
- Tests existentes de `scaffold_service.py` validarán template rendering
- Tests de `template_repo.py` validarán que templates son válidos Jinja2

### Manual Verification Tests
1. **Verificar archivos BASE**:
   ```bash
   ls -la .claude/commands/orch_*.md
   ls -la .claude/commands/build_in_parallel.md
   ls -la .claude/commands/parallel_subagents.md
   ```
   - Esperar 5 archivos listados

2. **Verificar templates CLI**:
   ```bash
   ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/orch_*.md.j2
   ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2
   ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2
   ```
   - Esperar 5 archivos listados

3. **Verificar YAML frontmatter**:
   ```bash
   head -n 10 .claude/commands/orch_plan_w_scouts_build_review.md
   ```
   - Validar que tiene formato:
     ```yaml
     ---
     name: ...
     description: ...
     category: Orchestrator Commands
     model: ...
     allowed-tools: ...
     ---
     ```

4. **Verificar registration en scaffold_service.py**:
   ```bash
   grep -A 5 "orch_plan_w_scouts_build_review" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
   ```
   - Debe aparecer en la lista de commands

### Edge Cases
- **Caso 1: Fuente original no disponible**
  - Verificar que comandos se crean desde patrones existentes
  - Comandos deben ser funcionales aunque no sean copia exacta

- **Caso 2: Agent definitions renombradas**
  - Si `.claude/agents/scout-report-suggest.md` tiene otro nombre
  - Adaptar referencias según estructura real

- **Caso 3: Templates ya existen**
  - Verificar que no se sobrescriben templates existentes
  - Si `build_in_parallel.md.j2` ya existe, no crear duplicado

- **Caso 4: YAML frontmatter inválido**
  - Validar con Claude Code que los comandos son reconocidos
  - Formato debe ser exactamente `---\nkey: value\n---`

## Acceptance Criteria
- ✅ 5 archivos .md creados en `.claude/commands/`:
  - `orch_plan_w_scouts_build_review.md`
  - `orch_scout_and_build.md`
  - `orch_one_shot_agent.md`
  - `build_in_parallel.md` (ya existe o se valida)
  - `parallel_subagents.md` (ya existe o se valida)
- ✅ YAML frontmatter válido en todos (name, description, category, model, allowed-tools)
- ✅ Referencias a agents correctas apuntando a `.claude/agents/*.md`
- ✅ 5 templates .md.j2 creados en `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
- ✅ Templates parametrizados con `{{ config.* }}` variables
- ✅ Lógica de workflow estática (sin parametrización de orchestration steps)
- ✅ Registro completo en `scaffold_service.py::_add_claude_files()`
- ✅ Tests pasan: pytest, ruff, mypy
- ✅ Comandos funcionan en Claude Code (verificación manual con `/orch_plan_w_scouts_build_review --help` o similar)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `ls -la .claude/commands/orch_*.md .claude/commands/build_in_parallel.md .claude/commands/parallel_subagents.md` - Verificar BASE files (5 archivos)
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/orch_*.md.j2 tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build_in_parallel.md.j2 tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Verificar templates (5 archivos)

## Notes

### Implementation Strategy
- **Prioritize copying from source**: Si `/Volumes/MAc1/Celes/TAC/tac-14/.claude/commands/` es accesible, copiar archivos directamente
- **Fallback to pattern-based creation**: Si fuente no disponible, crear desde scratch usando patrones de `scout_plan_build.md` y `expert-orchestrate.md`
- **Agent references adaptation**: Critical que referencias apunten a `.claude/agents/` nueva estructura
- **Template parameterization**: Solo parametrizar project-specific values, no orchestration logic

### Orchestration Patterns
Los 5 comandos representan diferentes patrones de orquestación:
1. **orch_plan_w_scouts_build_review**: Full pipeline (TAC-10 Level 4 completo)
2. **orch_scout_and_build**: Simplified pipeline (skip plan/review)
3. **orch_one_shot_agent**: Single agent delegation
4. **build_in_parallel**: Parallel file creation (ya existe)
5. **parallel_subagents**: Parallel agent orchestration (ya existe)

### YAML Frontmatter Pattern
Basado en análisis de comandos existentes:
```yaml
---
name: command-name
description: Brief description of what the command does
category: Orchestrator Commands
model: claude-sonnet-4-5-20250929
allowed-tools: [Task, Read, Write, TodoWrite, AskUserQuestion]
argument-hint: "[arg1] [arg2]"  # opcional
---
```

### Agent Invocation Pattern
```markdown
Use Task tool:
- `subagent_type: "scout-report-suggest"` (from .claude/agents/scout-report-suggest.md)
- `subagent_type: "planner"` (from .claude/agents/planner.md)
- `subagent_type: "build-agent"` (from .claude/agents/build-agent.md)
```

### Template Jinja2 Variables
Variables disponibles para parametrización:
- `{{ config.project.name }}`
- `{{ config.project.language }}`
- `{{ config.project.framework }}`
- `{{ config.agentic.provider }}`
- `{{ config.agentic.model_policy }}`
- `{{ config.commands.* }}` (start, build, test, etc.)
- `{{ config.paths.* }}` (app, adws, specs, etc.)

### Dependencies
- **Tarea 2 (Agent Definitions)**: Los comandos dependen de las agent definitions en `.claude/agents/`
- Si Tarea 2 no completada, los comandos fallarán al invocar agentes
- Verificar que `.claude/agents/` contiene: build-agent.md, planner.md, scout-report-suggest.md

### Future Enhancements
- Agregar más orchestrator commands según patrones TAC emerjan
- Implementar orchestrator command validator (YAML frontmatter, agent refs)
- Crear tests end-to-end que ejecuten workflows completos
