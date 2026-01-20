# Application Validation Test Suite

Ejecutar tests comprehensivos para TAC Bootstrap CLI, retornando resultados en formato JSON.

## Purpose

Validar el CLI de TAC Bootstrap antes de hacer cambios:
- Detectar errores de sintaxis y tipos
- Identificar tests rotos
- Verificar que el build funciona
- Asegurar calidad del código

## Variables

TEST_COMMAND_TIMEOUT: 5 minutes

## Instructions

- Ejecutar cada test en secuencia
- Capturar resultado (passed/failed) y mensajes de error
- IMPORTANTE: Retornar SOLO el JSON array con resultados
- Si un test pasa, omitir el campo error
- Si un test falla, incluir mensaje de error
- Ejecutar todos los tests aunque algunos fallen
- Timeout de comandos: `TEST_COMMAND_TIMEOUT`

## Test Execution Sequence

### TAC Bootstrap CLI Tests (tac_bootstrap_cli/)

**Si tac_bootstrap_cli/ existe:**

1. **Python Syntax Check**
   - Command: `cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/**/*.py`
   - test_name: "python_syntax_check"
   - test_purpose: "Valida sintaxis Python compilando archivos fuente"

2. **Code Quality Check**
   - Command: `cd tac_bootstrap_cli && uv run ruff check .`
   - test_name: "backend_linting"
   - test_purpose: "Valida calidad de código Python"

3. **Type Check**
   - Command: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports`
   - test_name: "type_check"
   - test_purpose: "Valida tipos con mypy"

4. **Unit Tests**
   - Command: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
   - test_name: "unit_tests"
   - test_purpose: "Ejecuta todos los tests unitarios"

5. **CLI Smoke Test**
   - Command: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
   - test_name: "cli_smoke_test"
   - test_purpose: "Verifica que el CLI arranca correctamente"

**Si tac_bootstrap_cli/ NO existe:**

1. **Structure Check**
   - Command: `ls tac_bootstrap_cli/pyproject.toml`
   - test_name: "structure_check"
   - test_purpose: "Verifica que existe la estructura del CLI"
   - Note: Este test fallará indicando que el CLI aún no existe

### App de Ejemplo Tests (app/) - Opcional

Solo si se está trabajando en la app de ejemplo:

1. **Backend Tests**
   - Command: `cd app/server && uv run pytest tests/ -v --tb=short`
   - test_name: "app_backend_tests"

2. **Frontend Build**
   - Command: `cd app/client && bun run build`
   - test_name: "app_frontend_build"

## Report

- IMPORTANTE: Retornar resultados como JSON array
- Ordenar con tests fallidos primero
- Incluir todos los tests en el output

### Output Structure

```json
[
  {
    "test_name": "string",
    "passed": boolean,
    "execution_command": "string",
    "test_purpose": "string",
    "error": "optional string"
  }
]
```

### Example Output

```json
[
  {
    "test_name": "unit_tests",
    "passed": false,
    "execution_command": "cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short",
    "test_purpose": "Ejecuta todos los tests unitarios",
    "error": "AssertionError: Expected X but got Y"
  },
  {
    "test_name": "python_syntax_check",
    "passed": true,
    "execution_command": "cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/**/*.py",
    "test_purpose": "Valida sintaxis Python compilando archivos fuente"
  }
]
```
