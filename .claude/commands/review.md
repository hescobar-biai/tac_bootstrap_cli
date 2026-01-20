# Review

Revisar trabajo realizado contra un archivo de especificación (specs/*.md) para asegurar que la implementación cumple los requerimientos.

## Variables

adw_id: $ARGUMENT
spec_file: $ARGUMENT
agent_name: $ARGUMENT si se proporciona, de lo contrario usar 'review_agent'
review_image_dir: `<absolute path to codebase>/agents/<adw_id>/<agent_name>/review_img/`

## Instructions

- Verificar branch actual con `git branch` para entender contexto
- Ejecutar `git diff origin/main` para ver cambios hechos en el branch actual
- Encontrar spec file buscando specs/*.md que coincida con el branch
- Leer el spec file para entender requerimientos

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

- IMPORTANTE: Retornar resultados exclusivamente como JSON array.
- `success` debe ser `true` si NO hay issues BLOCKING
- `success` debe ser `false` SOLO si hay issues BLOCKING

### Output Structure

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
            "issue_severity": "skippable|tech_debt|blocker"
        }
    ]
}
```
