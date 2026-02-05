# Bug Planning

Crear un plan para resolver un bug en TAC Bootstrap CLI usando el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

🚨 **YOU ARE IN THE PLANNING PHASE** 🚨

**CRITICAL - READ THIS FIRST:**
- You are creating a PLAN, NOT fixing the bug
- DO NOT create any final files (code, docs, configs, etc.)
- ONLY create ONE file: the plan in `specs/` directory
- The plan will be executed later by another agent

**Planning Instructions:**
- IMPORTANTE: Estás escribiendo un plan para resolver un bug del TAC Bootstrap CLI.
- El plan debe ser preciso para arreglar la causa raíz y prevenir regresiones.
- CRITICAL: Crear el plan usando ruta RELATIVA `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/filename.md`, NO `/Users/.../specs/filename.md`
- CRITICAL: DO NOT use Write tool for any other files besides the plan in specs/
- Investigar el codebase para entender el bug, reproducirlo y crear un plan de fix.
- IMPORTANTE: Reemplazar cada <placeholder> en el formato con valores reales.
- Usar el reasoning model: pensar cuidadosamente sobre la causa raíz.
- IMPORTANTE: Ser quirúrgico - resolver el bug específico sin desviarse.

**⚡ TOKEN OPTIMIZATION RULES (CRITICAL):**
- **DO NOT repeat bug description** - Already in `issue_json`, reference by ID only
- **Keep plan under 600 tokens** - Bug fixes should be surgical and brief
- **Focus on root cause** - Skip verbose explanations, state facts only
- **Minimal reproduction** - Only essential steps to reproduce
- **Short fix description** - One paragraph maximum per file change
- IMPORTANTE: Mínimo número de cambios para resolver el bug.
- Mantener simplicidad.
- Si necesitas una nueva librería, usar `uv add` y reportarlo en Notes.

## Relevant Files

Archivos clave para TAC Bootstrap CLI:

- `PLAN_TAC_BOOTSTRAP.md` - Plan maestro del proyecto
- `CLAUDE.md` - Guía para agentes
- `config.yml` - Configuración del proyecto
- `tac_bootstrap_cli/` - Código fuente del CLI
  - `tac_bootstrap/domain/` - Modelos Pydantic
  - `tac_bootstrap/application/` - Servicios
  - `tac_bootstrap/infrastructure/` - Templates, FS
  - `tac_bootstrap/interfaces/` - CLI, Wizard
  - `tests/` - Tests unitarios

Leer `.claude/commands/conditional_docs.md` para documentación adicional.

## Plan Format

```md
# Bug: <nombre del bug>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Bug Description
<describir el bug en detalle, incluyendo síntomas y comportamiento esperado vs actual>

## Problem Statement
<definir claramente el problema específico a resolver>

## Solution Statement
<describir el approach propuesto para arreglar el bug>

## Steps to Reproduce
<listar pasos exactos para reproducir el bug>

## Root Cause Analysis
<analizar y explicar la causa raíz del bug>

## Relevant Files
Archivos para arreglar el bug:

<listar archivos relevantes con descripción de por qué son relevantes>

### New Files
<listar archivos nuevos si se requieren>

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: <nombre>
- <detalle>

### Task 2: <nombre>
- <detalle>

<El último paso debe ejecutar Validation Commands>

## Validation Commands
Ejecutar todos los comandos para validar el fix con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
<notas adicionales o contexto relevante>
```

## Bug
Extraer detalles del bug de la variable `issue_json` (parsear JSON y usar campos title y body).

## Report

🚨 **CRITICAL OUTPUT FORMAT** 🚨

YOU ARE BEING CALLED FROM AN AUTOMATED WORKFLOW. YOUR OUTPUT IS MACHINE-PARSED.

**STEP 1: Check for existing plan**
- Look in `specs/` for files matching: `issue-{issue_number}-adw-{adw_id}-*.md`
- If found: Output ONLY the path and STOP. Do not create new files.

**STEP 2: Create plan file (if not exists)**
- Use Write tool with RELATIVE path: `specs/issue-{issue_number}-adw-{adw_id}-bug_planner-{name}.md`
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
specs/issue-123-adw-bug-fix-auth-bug_planner-fix-auth-issue.md
```

❌ WRONG OUTPUT (will cause workflow failure):
```
Perfect! I created the plan at specs/issue-123...
```

❌ WRONG OUTPUT (will cause workflow failure):
```
The plan file can be found at: specs/issue-123...
```

**THIS IS MACHINE-PARSED. ANY TEXT OTHER THAN THE PATH WILL BREAK THE WORKFLOW.**
