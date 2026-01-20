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
- Crear el patch plan en `specs/patch/` con filename: `patch-adw-{adw_id}-{descriptive-name}.md`
- IMPORTANTE: Esto es un PATCH - mantener el scope mínimo. Solo arreglar lo descrito en `review_change_request`.
- Ejecutar `git diff --stat` para entender cambios existentes.
- Pensar sobre la forma más eficiente de implementar con cambios mínimos.
- Basar la validación en los pasos de validación del `spec_path` si se proporciona.
- Reemplazar cada <placeholder> en el formato con detalles específicos.

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

- IMPORTANTE: Retornar exclusivamente el path al archivo de patch plan creado.
