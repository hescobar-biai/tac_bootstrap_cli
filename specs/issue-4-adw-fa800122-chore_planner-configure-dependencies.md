# Chore: Configurar archivos de configuración MCP para Playwright

## Metadata
issue_number: `4`
adw_id: `fa800122`
issue_json: `{"number":4,"title":"chore: #3 - TAREA 1.2: Configurar dependencias del proyecto","body":"## Summary\n\nThis PR configures the project dependencies for the `tac-bootstrap` CLI package. The implementation updates `pyproject.toml` with all required production and development dependencies, following the specifications in issue #3.\n\n## Implementation Plan\n\nSee: [specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md](specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md)\n\n## Changes\n\n### Dependencies Added\n\n**Production:**\n- typer>=0.9.0 - CLI framework for commands and options\n- rich>=13.0.0 - Terminal UI with tables, panels, colors\n- jinja2>=3.0.0 - Template rendering engine\n- pydantic>=2.0.0 - Data validation and schemas\n- pyyaml>=6.0.0 - YAML parsing for config files\n- gitpython>=3.1.0 - Git operations integration\n\n**Development:**\n- pytest>=7.0.0 - Testing framework\n- pytest-cov>=4.0.0 - Code coverage reporting\n- mypy>=1.0.0 - Static type checking\n- ruff>=0.1.0 - Linting and formatting\n\n### Configuration\n\n- Added entry point script: `tac-bootstrap`\n- Configured build system with hatchling\n- Added tool configurations for ruff, mypy, and pytest\n- Set Python version requirement to >=3.10\n\n## Checklist\n\n- [x] Updated pyproject.toml with all production dependencies\n- [x] Added development dependencies\n- [x] Configured entry point script\n- [x] Set up build system configuration\n- [x] Added tool configurations (ruff, mypy, pytest)\n\n## Issue\n\nCloses #3\n\n## ADW Tracking\n\nADW ID: e29f22c3"}`

## Chore Description
Esta chore consiste en limpiar y normalizar las rutas absolutas en los archivos de configuración de MCP (Model Context Protocol) para Playwright. Los archivos `.mcp.json` y `playwright-mcp-config.json` contienen rutas absolutas que son específicas del árbol de trabajo ADW actual (`/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/fa800122/`).

El problema es que estas rutas absolutas:
1. No son portables - solo funcionan en la máquina actual
2. No funcionarán en otros árboles de trabajo ADW
3. Deberían usar rutas relativas para mayor flexibilidad

La solución es convertir las rutas absolutas a rutas relativas o usar variables de entorno que puedan ser configuradas dinámicamente.

## Relevant Files
Archivos para completar la chore:

### Archivos Existentes
- `.mcp.json` - Configuración del servidor MCP para Playwright
  - Línea 9: Contiene ruta absoluta a `playwright-mcp-config.json`
  - Necesita cambiarse a ruta relativa: `./playwright-mcp-config.json`

- `playwright-mcp-config.json` - Configuración de Playwright con opciones de browser
  - Línea 9: Contiene ruta absoluta al directorio de videos
  - Necesita cambiarse a ruta relativa: `./videos`

### New Files
Ningún archivo nuevo requerido. Solo modificación de archivos existentes.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Actualizar .mcp.json con ruta relativa
- Cambiar la línea 9 de `.mcp.json`
- Convertir ruta absoluta a ruta relativa
- De: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/fa800122/playwright-mcp-config.json`
- A: `./playwright-mcp-config.json`
- Verificar que el formato JSON sigue siendo válido

### Task 2: Actualizar playwright-mcp-config.json con ruta relativa
- Cambiar la línea 9 de `playwright-mcp-config.json`
- Convertir ruta absoluta del directorio de videos a ruta relativa
- De: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/fa800122/videos`
- A: `./videos`
- Verificar que el formato JSON sigue siendo válido

### Task 3: Validar que los archivos JSON son válidos
- Ejecutar validación de sintaxis JSON
- Confirmar que ambos archivos tienen formato correcto
- Verificar que las rutas relativas son correctas

### Task 4: Ejecutar Validation Commands
- Ejecutar todos los comandos de validación listados abajo
- Confirmar que las rutas relativas funcionan correctamente
- Confirmar cero regresiones

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `python -m json.tool .mcp.json > /dev/null && echo "✓ .mcp.json is valid JSON"` - Validar JSON
- `python -m json.tool playwright-mcp-config.json > /dev/null && echo "✓ playwright-mcp-config.json is valid JSON"` - Validar JSON

## Notes
- Esta es una chore de limpieza y normalización, no de implementación de features
- El issue #4 hace referencia a dependencias de pyproject.toml que ya están completadas (issue #3)
- Los archivos modificados (`.mcp.json` y `playwright-mcp-config.json`) están listados en el git status como modificados
- Las rutas relativas harán que la configuración sea más portable y funcione en cualquier árbol de trabajo ADW
- No es necesario crear tests nuevos para esta chore
