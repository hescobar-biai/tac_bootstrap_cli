# Health Check

Verificar el estado del entorno de desarrollo de TAC Bootstrap CLI.

## Variables

TEST_COMMAND_TIMEOUT: 2 minutes

## Instructions

Ejecutar verificaciones del entorno de desarrollo para TAC Bootstrap CLI.

### Si tac_bootstrap_cli/ existe:

1. **Verificar estructura del CLI**
   - Command: `ls -la tac_bootstrap_cli/`
   - Debe existir: pyproject.toml, tac_bootstrap/

2. **Verificar dependencias instaladas**
   - Command: `cd tac_bootstrap_cli && uv sync --dry-run`
   - Si hay dependencias faltantes, reportar

3. **Verificar CLI funciona**
   - Command: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
   - Debe mostrar ayuda del CLI

4. **Verificar sintaxis Python**
   - Command: `cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/__init__.py`
   - No debe haber errores de sintaxis

5. **Verificar config.yml**
   - Leer config.yml y validar que es YAML válido
   - Verificar campos requeridos: project.name, project.language

### Si tac_bootstrap_cli/ NO existe:

1. **Verificar archivos de configuración base**
   - Command: `ls config.yml PLAN_TAC_BOOTSTRAP.md CLAUDE.md`
   - Deben existir estos archivos

2. **Informar estado**
   - El CLI aún no ha sido creado
   - Siguiente paso: Ejecutar TAREA 1.1 del PLAN_TAC_BOOTSTRAP.md

## Report

Reportar resultados como JSON:

```json
{
  "status": "healthy|warning|error",
  "cli_exists": boolean,
  "checks": [
    {
      "name": "string",
      "passed": boolean,
      "message": "string"
    }
  ],
  "next_steps": ["string"]
}
```
