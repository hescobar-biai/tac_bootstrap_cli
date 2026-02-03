# Feature Planning

Crear un plan para implementar una nueva funcionalidad en TAC Bootstrap CLI siguiendo el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

🚨 **YOU ARE IN THE PLANNING PHASE** 🚨

**CRITICAL - READ THIS FIRST:**
- You are creating a PLAN, NOT implementing the feature
- DO NOT create any final files (code, docs, configs, etc.)
- ONLY create ONE file: the plan in `specs/` directory
- The plan will be executed later by another agent

**Planning Instructions:**
- IMPORTANTE: Estás creando un plan para implementar una nueva funcionalidad del TAC Bootstrap CLI.
- El plan se usará para guiar la implementación con agentic coding.
- CRITICAL: Crear el plan usando ruta RELATIVA `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/filename.md`, NO `/Users/.../specs/filename.md`
- CRITICAL: DO NOT use Write tool for any other files besides the plan in specs/
- Investigar el codebase para entender patrones existentes antes de planificar.
- IMPORTANTE: Reemplazar cada <placeholder> en el formato con valores reales.
- Usar el reasoning model: pensar cuidadosamente sobre requerimientos y approach.
- Seguir patrones y convenciones existentes del proyecto.
- Si necesitas una nueva librería, usar `uv add` y reportarlo en Notes.
- Mantener simplicidad - no usar decoradores innecesarios.

## Relevant Files

Archivos clave para TAC Bootstrap CLI:

- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro con todas las tareas
- `CLAUDE.md` - Guía para agentes
- `config.yml` - Configuración del proyecto
- `tac_bootstrap_cli/` - Código fuente del CLI (si existe)
  - `tac_bootstrap/domain/` - Modelos Pydantic
  - `tac_bootstrap/application/` - Servicios
  - `tac_bootstrap/infrastructure/` - Templates, FS
  - `tac_bootstrap/interfaces/` - CLI, Wizard
- `prompts/templates/` - Templates de prompts

Leer `.claude/commands/conditional_docs.md` para documentación adicional requerida.

## Plan Format

```md
# Feature: <nombre de la feature>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Feature Description
<describir la feature en detalle, su propósito y valor>

## User Story
As a <tipo de usuario>
I want to <acción/objetivo>
So that <beneficio/valor>

## Problem Statement
<definir claramente el problema u oportunidad que esta feature aborda>

## Solution Statement
<describir el approach propuesto y cómo resuelve el problema>

## Relevant Files
Archivos necesarios para implementar la feature:

<listar archivos relevantes con descripción de por qué son relevantes>

### New Files
<listar archivos nuevos que se crearán>

## Implementation Plan

### Phase 1: Foundation
<trabajo fundacional antes de implementar la feature principal>

### Phase 2: Core Implementation
<implementación principal de la feature>

### Phase 3: Integration
<integración con funcionalidad existente>

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: <nombre>
- <detalle>
- <detalle>

### Task 2: <nombre>
- <detalle>

<El último paso debe ejecutar Validation Commands>

## Testing Strategy

### Unit Tests
<tests unitarios necesarios>

### Edge Cases
<casos edge a probar>

## Acceptance Criteria
<criterios específicos y medibles para considerar la feature completa>

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
<notas adicionales, consideraciones futuras, o contexto relevante>
```

## Feature
Extraer detalles de la feature de la variable `issue_json` (parsear JSON y usar campos title y body).

## Report

🚨 **CRITICAL OUTPUT FORMAT** 🚨

YOU ARE BEING CALLED FROM AN AUTOMATED WORKFLOW. YOUR OUTPUT IS MACHINE-PARSED.

**STEP 1: Check for existing plan**
- Look in `specs/` for files matching: `issue-{issue_number}-adw-{adw_id}-*.md`
- If found: Output ONLY the path and STOP. Do not create new files.

**STEP 2: Create plan file (if not exists)**
- Use Write tool with RELATIVE path: `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{name}.md`
- NEVER use absolute paths starting with `/Users/` or `/home/`
- The file WILL be created in the CURRENT WORKING DIRECTORY
- DO NOT try to create files in other directories like `ai_docs/`, `adws/`, etc.

**STEP 3: Output ONLY the path**

YOUR FINAL OUTPUT **MUST** BE:
- Exactly ONE line
- ONLY the relative path
- NO markdown formatting
- NO explanations or commentary
- NO phrases like "Perfect!", "Done!", "Here is..."

✅ CORRECT OUTPUT:
```
specs/issue-564-adw-feature-Tac-13-Task-2-sdlc_planner-expertise-docs.md
```

❌ WRONG OUTPUT (will cause workflow failure):
```
Perfect! I created the plan at specs/issue-564...
```

❌ WRONG OUTPUT (will cause workflow failure):
```
The plan file can be found at: specs/issue-564...
```

**THIS IS MACHINE-PARSED. ANY TEXT OTHER THAN THE PATH WILL BREAK THE WORKFLOW.**
