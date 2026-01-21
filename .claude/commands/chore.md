# Chore Planning

Crear un plan para resolver una tarea de mantenimiento (chore) en TAC Bootstrap CLI usando el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANTE: Estás escribiendo un plan para resolver una chore del TAC Bootstrap CLI.
- El plan debe ser simple pero preciso para no desperdiciar tiempo.
- Crear el plan en `specs/` con filename: `issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
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

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it following the Plan Format, then return ONLY the path

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the path like:
```
specs/issue-37-adw-e4dc9574-chore_planner-chore-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I found...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines

ONLY output the bare path. This is machine-parsed.
