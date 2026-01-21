# Bug Planning

Crear un plan para resolver un bug en TAC Bootstrap CLI usando el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANTE: Estás escribiendo un plan para resolver un bug del TAC Bootstrap CLI.
- El plan debe ser preciso para arreglar la causa raíz y prevenir regresiones.
- Crear el plan en `specs/` con filename: `issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- Investigar el codebase para entender el bug, reproducirlo y crear un plan de fix.
- IMPORTANTE: Reemplazar cada <placeholder> en el formato con valores reales.
- Usar el reasoning model: pensar cuidadosamente sobre la causa raíz.
- IMPORTANTE: Ser quirúrgico - resolver el bug específico sin desviarse.
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

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it following the Plan Format, then return ONLY the path

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the path like:
```
specs/issue-37-adw-e4dc9574-bug_planner-bug-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I found...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines

ONLY output the bare path. This is machine-parsed.
