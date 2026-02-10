# Review

Revisar trabajo realizado contra un archivo de especificación (specs/*.md) para asegurar que la implementación cumple los requerimientos.

## Variables

adw_id: $ARGUMENT
spec_file: $ARGUMENT
agent_name: $ARGUMENT si se proporciona (OPCIONAL), de lo contrario usar 'review_agent'
review_image_dir: `<absolute path to codebase>/agents/<adw_id>/<agent_name>/review_img/` (crea si no existe)

## Instructions

- Verificar branch actual con `git branch` para entender contexto
- Ejecutar `git diff origin/main` para ver cambios hechos en el branch actual
- Encontrar spec file buscando specs/*.md que coincida con el branch
- Leer el spec file para entender requerimientos

**⚡ TOKEN OPTIMIZATION RULES (CRITICAL):**
- **DO NOT re-explain the spec** - Reference it, don't repeat it
- **Keep findings under 600 tokens** - Prioritize issues by severity
- **Table format for issues** - File | Issue | Severity | Fix (one line each)
- **Only critical findings** - Skip minor style issues or non-blockers
- **No verbose test output** - Show only failures, not all test results

### Para TAC Bootstrap CLI

Si los cambios son en `tac_bootstrap_cli/`:

1. **Verificar sintaxis y tipos**
   ```bash
   cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/**/*.py
   cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports
   ```

2. **Verificar linting**
   ```bash
   cd tac_bootstrap_cli && uv run ruff check .
   ```

3. **Ejecutar tests**
   ```bash
   cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
   ```

4. **Verificar CLI funciona**
   ```bash
   cd tac_bootstrap_cli && uv run tac-bootstrap --help
   ```

### Severidad de Issues

- `skippable` - No bloquea release pero es un problema
- `tech_debt` - No bloquea release pero creará deuda técnica
- `blocker` - Bloquea release, debe resolverse inmediatamente

## Report

Después de completar la validación, generar DOS outputs:

### 1. JSON Report (compatible con versión anterior)

- IMPORTANTE: Retornar resultados exclusivamente como JSON array.
- `success` debe ser `true` si NO hay issues BLOCKING
- `success` debe ser `false` SOLO si hay issues BLOCKING

```json
{
    "success": "boolean - true si no hay issues BLOCKING",
    "review_summary": "string - 2-4 oraciones describiendo qué se construyó y si cumple la spec",
    "validation_results": {
        "syntax_check": "passed|failed",
        "type_check": "passed|failed",
        "linting": "passed|failed",
        "tests": "passed|failed",
        "cli_smoke": "passed|failed"
    },
    "review_issues": [
        {
            "review_issue_number": "number",
            "issue_description": "string",
            "issue_resolution": "string",
            "issue_severity": "skippable|tech_debt|blocker",
            "screenshot_path": "null or string (OPTIONAL)",
            "screenshot_url": "null or string (OPTIONAL)"
        }
    ]
}
```

### 2. Validation Checklist (NUEVO)

Generar un archivo markdown de checklist de validación y guardarlo junto al archivo spec.

**Instrucciones para Generar el Checklist:**

1. Parsear el archivo spec para extraer:
   - Nombre/título del feature desde el primer encabezado
   - Todos los ítems de la sección `## Acceptance Criteria` (líneas que empiezan con `- [ ]`)
   - Todos los comandos de la sección `## Validation Commands`
   - Nombre del branch git actual
   - Fecha actual

2. Mapear `validation_results` a ítems del checklist con estados apropiados:
   - `passed` → `- [x] <nombre del check> - PASSED`
   - `failed` → `- [ ] <nombre del check> - FAILED`

3. Generar checklist markdown en este formato exacto:

```markdown
# Validation Checklist: <Nombre del Feature>

**Spec:** `<ruta_del_archivo_spec>`
**Branch:** `<branch_actual>`
**Review ID:** `<adw_id>`
**Date:** `<fecha_actual>`

## Automated Technical Validations

- [x] Syntax and type checking - <PASSED|FAILED>
- [x] Linting - <PASSED|FAILED>
- [x] Unit tests - <PASSED|FAILED>
- [x] Application smoke test - <PASSED|FAILED>

## Acceptance Criteria

<!-- Extraído de la sección "## Acceptance Criteria" del spec -->
<copiar todas las líneas que empiezan con "- [ ]" de la sección Acceptance Criteria del spec>

## Validation Commands Executed

```bash
<copiar todos los comandos de la sección "## Validation Commands" del spec>
```

## Review Summary

<review_summary del output JSON>

## Review Issues

<formatear todos los issues del array review_issues con su severidad>

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
```

4. Guardar el checklist en:
   - Ruta del archivo: `<directorio_del_spec>/<nombre_base_del_spec>-checklist.md`
   - Ejemplo: si el spec es `specs/issue-64-adw-xyz-feature.md`, guardar en `specs/issue-64-adw-xyz-feature-checklist.md`

5. Reportar al usuario:
   - "Validation checklist guardado en: `<ruta_del_archivo_checklist>`"
   - "Puedes copiar este checklist en comentarios de GitHub PR"

**Casos Edge:**
- Si el spec no tiene sección "## Acceptance Criteria", usar lista vacía o notar "No se encontraron criterios de aceptación en el spec"
- Si falta la sección de comandos de validación, notar "No se especificaron comandos de validación"
- Asegurar escapado apropiado de markdown para caracteres especiales en el texto de criterios
- Preservar el formato exacto de los criterios de aceptación del spec

## Orchestration Patterns

Los workflows de orquestación completos incluyen fases de revisión automática con agentes especializados que validan el código contra especificaciones y criterios de aceptación. Consulta los comandos de orquestación para workflows multi-agente que incluyen revisión integrada:

- [orch_plan_w_scouts_build_review](./orch_plan_w_scouts_build_review.md) - Workflow completo que incluye fase de revisión automática
