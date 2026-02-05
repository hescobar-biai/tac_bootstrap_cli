# Patch Plan

Crear un **plan de patch enfocado** para resolver un issue específico en TAC Bootstrap CLI basado en el `review_change_request`.

## Variables

adw_id: $1
review_change_request: $2
spec_path: $3 si se proporciona, de lo contrario dejar en blanco
agent_name: $4 si se proporciona, de lo contrario usar 'patch_agent'
issue_screenshots: $5 (opcional) - lista de paths a screenshots separados por coma

## Instructions

- IMPORTANTE: Estás creando un patch plan para arreglar un issue específico. Mantener cambios pequeños y enfocados.
- Leer la especificación original (spec) en `spec_path` si se proporciona.
- IMPORTANTE: Usar `review_change_request` para entender exactamente qué necesita ser arreglado.
- Si `issue_screenshots` se proporcionan, examinarlos para entender el contexto visual.
- CRITICAL: Crear el patch plan usando ruta RELATIVA `specs/patch/patch-adw-{adw_id}-{descriptive-name}.md`
- CRITICAL: NUNCA uses rutas absolutas (que empiezan con /). SIEMPRE usa rutas relativas al directorio actual.
- CRITICAL: Al usar la herramienta Write, usa SOLO `specs/patch/filename.md`, NO `/Users/.../specs/patch/filename.md`
- IMPORTANTE: Esto es un PATCH - mantener el scope mínimo. Solo arreglar lo descrito en `review_change_request`.
- Ejecutar `git diff --stat` para entender cambios existentes.
- Pensar sobre la forma más eficiente de implementar con cambios mínimos.
- Basar la validación en los pasos de validación del `spec_path` si se proporciona.
- Reemplazar cada <placeholder> en el formato con detalles específicos.

**⚡ TOKEN OPTIMIZATION RULES (CRITICAL):**
- **DO NOT repeat review findings** - They're in `review_change_request`, reference by ID
- **Keep patch plan under 400 tokens** - Patches should be surgical and minimal
- **One line per change** - File + exact change needed, nothing more
- **No context repetition** - The review already provided it
- **Minimal validation** - Only test what changed, skip redundant checks

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
# Patch: <título conciso del patch>

## Metadata
adw_id: `{adw_id}`
review_change_request: `{review_change_request}`

## Issue Summary
**Original Spec:** <spec_path>
**Issue:** <descripción breve del issue basado en `review_change_request`>
**Solution:** <descripción breve del approach basado en `review_change_request`>

## Files to Modify
Archivos a modificar para implementar el patch:

<listar solo los archivos que necesitan cambios - ser específico y mínimo>

## Implementation Steps
IMPORTANTE: Ejecutar cada paso en orden.

<listar 2-5 pasos enfocados. Cada paso debe ser una acción concreta.>

### Step 1: <acción específica>
- <detalle de implementación>
- <detalle de implementación>

### Step 2: <acción específica>
- <detalle de implementación>

<continuar según sea necesario, pero mantenerlo mínimo>

## Validation
Ejecutar comandos para validar el patch con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Patch Scope
**Lines of code to change:** <estimación>
**Risk level:** <low|medium|high>
**Testing required:** <descripción breve>
```

## Report

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/patch/` matching pattern: `patch-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it using RELATIVE PATH (e.g., `specs/patch/filename.md`), then return ONLY the path

CRITICAL FILE CREATION RULES:
- When using the Write tool, use RELATIVE paths only: `specs/patch/filename.md`
- NEVER use absolute paths like `/Users/.../specs/patch/filename.md`
- The file will be created in the current working directory

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the RELATIVE path like:
```
specs/patch/patch-adw-e4dc9574-patch-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I found...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines
- Absolute paths (starting with /)

ONLY output the bare RELATIVE path. This is machine-parsed.
