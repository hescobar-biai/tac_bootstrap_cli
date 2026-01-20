# Chore: Configurar dependencias del proyecto

## Metadata
issue_number: `3`
adw_id: `e29f22c3`
issue_json: `{"number":3,"title":"TAREA 1.2: Configurar dependencias del proyecto","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar\nlas dependencias del proyecto para poder usar las librerias necesarias.\n\n## Objetivo\nActualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.\n\n..."}`

## Chore Description
Actualizar la configuración de dependencias del proyecto TAC Bootstrap CLI en `pyproject.toml`. La estructura base del paquete ya existe con la arquitectura DDD establecida (domain, application, infrastructure, interfaces).

Esta chore consiste en:
1. Agregar gitpython>=3.1.0 a las dependencias de producción (actualmente falta)
2. Agregar configuraciones adicionales para ruff, mypy y pytest
3. Sincronizar las dependencias con `uv sync`
4. Verificar que el CLI funciona correctamente con el comando `version`

El objetivo es tener todas las dependencias necesarias instaladas para poder continuar con la implementación del CLI generador de Agentic Layers.

## Relevant Files
Archivos para completar la chore:

### Archivos Existentes
- `tac_bootstrap_cli/pyproject.toml` - Configuración del proyecto que necesita actualización
  - Actualmente tiene typer, rich, jinja2, pydantic, pyyaml
  - Falta: gitpython>=3.1.0
  - Falta: configuraciones de herramientas (ruff.lint, mypy, pytest)

- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Define __version__ usado por el comando version

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Entry point del CLI con comando version implementado

### New Files
Ningún archivo nuevo requerido. Solo modificación de `pyproject.toml`.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar pyproject.toml con dependencia faltante
- Agregar `gitpython>=3.1.0` a la lista de dependencias de producción
- Agregar configuraciones de herramientas:
  - `[tool.ruff.lint]` con select = ["E", "F", "I", "N", "W"]
  - Mantener configuraciones existentes de ruff, mypy y pytest
- Verificar que el formato TOML es correcto

### Task 2: Sincronizar dependencias con uv
- Ejecutar `cd tac_bootstrap_cli && uv sync` para instalar todas las dependencias
- Verificar que la instalación completa sin errores
- Confirmar que gitpython y todas las dependencias dev están instaladas

### Task 3: Verificar funcionamiento del CLI
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verificar que muestra la ayuda correctamente
- Ejecutar `cd tac_bootstrap_cli && uv run tac-bootstrap version`
- Confirmar que muestra "tac-bootstrap v0.1.0"

### Task 4: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Confirmar cero regresiones y cero errores

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test para ayuda
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Smoke test para comando version

## Notes
- El archivo pyproject.toml ya tiene la mayoría de dependencias configuradas (typer, rich, jinja2, pydantic, pyyaml)
- Solo falta agregar gitpython>=3.1.0 y las configuraciones adicionales de herramientas
- No implementar comandos adicionales en esta tarea
- No crear tests nuevos en esta tarea
- Esta es una tarea de configuración, no de implementación de features
- El CLI ya tiene el comando `version` implementado en cli.py:10-14
