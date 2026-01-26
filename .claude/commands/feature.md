# Feature Planning

Crear un plan para implementar una nueva funcionalidad en TAC Bootstrap CLI siguiendo el formato especificado.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANTE: Estás creando un plan para implementar una nueva funcionalidad del TAC Bootstrap CLI.
- El plan se usará para guiar la implementación con agentic coding.
- CRITICAL: Crear el plan usando ruta RELATIVA `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/filename.md`, NO `/Users/.../specs/filename.md`
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

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it using RELATIVE PATH (e.g., `specs/filename.md`), then return ONLY the path

CRITICAL FILE CREATION RULES:
- When using the Write tool, use RELATIVE paths only: `specs/filename.md`
- NEVER use absolute paths like `/Users/.../specs/filename.md`
- The file will be created in the current working directory

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the RELATIVE path like:
```
specs/issue-37-adw-e4dc9574-sdlc_planner-feature-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I can see that...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines
- Absolute paths (starting with /)

ONLY output the bare RELATIVE path. This is machine-parsed.
