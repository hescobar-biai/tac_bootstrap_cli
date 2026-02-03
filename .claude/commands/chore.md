# Chore Planning

Crear un plan para resolver una tarea de mantenimiento (chore) en TAC Bootstrap CLI usando el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

🚨 **YOU ARE IN THE PLANNING PHASE** 🚨

**CRITICAL - READ THIS FIRST:**
- You are creating a PLAN, NOT implementing the chore
- DO NOT create any final files (code, docs, configs, etc.)
- ONLY create ONE file: the plan in `specs/` directory
- The plan will be executed later by another agent

**Planning Instructions:**
- IMPORTANTE: Estás escribiendo un plan para resolver una chore del TAC Bootstrap CLI.
- El plan debe ser simple pero preciso para no desperdiciar tiempo.
- CRITICAL: Crear el plan usando ruta RELATIVA `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/filename.md`, NO `/Users/.../specs/filename.md`
- CRITICAL: DO NOT use Write tool for any other files besides the plan in specs/
- Investigar el codebase y crear un plan para completar la chore.
- IMPORTANTE: Reemplazar cada <placeholder> en el formato con valores reales.
- Usar el reasoning model: pensar cuidadosamente sobre los pasos.
- `adws/*.py` son scripts uv single-file. Ejecutar con `uv run <script_name>`.

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
- `scripts/` - Scripts de desarrollo
- `adws/` - AI Developer Workflows

Leer `.claude/commands/conditional_docs.md` para documentación adicional.

## Plan Format

```md
# Chore: <nombre de la chore>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Chore Description
<describir la chore en detalle>

## Relevant Files
Archivos para completar la chore:

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
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
<notas adicionales o contexto relevante>
```

## Chore
Extraer detalles de la chore de la variable `issue_json` (parsear JSON y usar campos title y body).

## Report

🚨 **CRITICAL OUTPUT FORMAT** 🚨

YOU ARE BEING CALLED FROM AN AUTOMATED WORKFLOW. YOUR OUTPUT IS MACHINE-PARSED.

**STEP 1: Check for existing plan**
- Look in `specs/` for files matching: `issue-{issue_number}-adw-{adw_id}-*.md`
- If found: Output ONLY the path and STOP. Do not create new files.

**STEP 2: Create plan file (if not exists)**
- Use Write tool with RELATIVE path: `specs/issue-{issue_number}-adw-{adw_id}-chore_planner-{name}.md`
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
specs/issue-563-adw-chore-Tac-13-Task-1-chore_planner-tac13-concepts.md
```

❌ WRONG OUTPUT (will cause workflow failure):
```
Perfect! I created the plan at specs/issue-563...
```

❌ WRONG OUTPUT (will cause workflow failure):
```
The plan file can be found at: specs/issue-563...
```

**THIS IS MACHINE-PARSED. ANY TEXT OTHER THAN THE PATH WILL BREAK THE WORKFLOW.**
