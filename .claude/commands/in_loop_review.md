# In-Loop Review

Quick checkout and review workflow for agent work validation in TAC Bootstrap CLI.

## Variables

branch: $ARGUMENTS

## Workflow

IMPORTANTE: Si no se proporciona branch, detener ejecución y reportar que el argumento branch es requerido.

### Step 1: Pull and Checkout Branch
- Ejecutar `git fetch origin` para obtener cambios remotos
- Ejecutar `git checkout {branch}` para cambiar al branch objetivo

### Step 2: Prepare Environment

**Si tac_bootstrap_cli/ existe:**
- Ejecutar `cd tac_bootstrap_cli && uv sync` para sincronizar dependencias
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help` para verificar CLI funciona

**Si tac_bootstrap_cli/ NO existe:**
- Informar que el CLI aún no ha sido creado

### Step 3: Run Validation
- Ejecutar `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` para correr tests
- Ejecutar `cd tac_bootstrap_cli && uv run ruff check .` para verificar linting

### Step 4: Manual Review
- El CLI está listo para revisión manual
- El ingeniero puede probar comandos directamente:
  ```bash
  cd tac_bootstrap_cli && uv run tac-bootstrap --help
  cd tac_bootstrap_cli && uv run tac-bootstrap init --help
  cd tac_bootstrap_cli && uv run tac-bootstrap doctor --help
  ```

## Report

Reportar pasos tomados para preparar el entorno para revisión.
