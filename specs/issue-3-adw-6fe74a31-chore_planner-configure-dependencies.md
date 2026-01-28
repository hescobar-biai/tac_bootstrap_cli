# Chore: Configure Dependencies for TAC Bootstrap CLI

## Metadata
issue_number: `3`
adw_id: `6fe74a31`
issue_json: `{"number":3,"title":"TAREA 1.2: Configurar dependencias del proyecto","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar\nlas dependencias del proyecto para poder usar las librerias necesarias.\n\n## Objetivo\nActualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.\n\n## Archivo a Modificar\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`\n\n## Dependencias Requeridas\n\n### Dependencias de Produccion\n```toml\ndependencies = [\n    \"typer>=0.9.0\",        # CLI framework - maneja comandos, argumentos, opciones\n    \"rich>=13.0.0\",        # UI terminal - tablas, paneles, colores, progress bars\n    \"jinja2>=3.0.0\",       # Templates - renderizado de archivos parametrizables\n    \"pydantic>=2.0.0\",     # Validacion - schemas para config.yml y modelos\n    \"pyyaml>=6.0.0\",       # YAML - lectura/escritura de config.yml\n    \"gitpython>=3.1.0\",    # Git - operaciones git init, commit, etc.\n]\n```\n\n### Dependencias de Desarrollo\n```toml\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",       # Testing framework\n    \"pytest-cov>=4.0.0\",   # Coverage reports\n    \"mypy>=1.0.0\",         # Type checking\n    \"ruff>=0.1.0\",         # Linting y formatting\n]\n```\n\n### Entry Points\n```toml\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n```\n\n### Build System\n```toml\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n```\n\n## Acciones a Ejecutar\n\n1. Actualizar `pyproject.toml` con el contenido completo\n2. Ejecutar `uv sync` para instalar dependencias\n3. Verificar que `tac-bootstrap --help` funciona\n\n## pyproject.toml Completo\n\n```toml\n[project]\nname = \"tac-bootstrap\"\nversion = \"0.1.0\"\ndescription = \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\nreadme = \"README.md\"\nrequires-python = \">=3.10\"\nlicense = {text = \"MIT\"}\nauthors = [\n    {name = \"TAC Team\"}\n]\nkeywords = [\"cli\", \"claude\", \"agentic\", \"tac\", \"bootstrap\"]\n\ndependencies = [\n    \"typer>=0.9.0\",\n    \"rich>=13.0.0\",\n    \"jinja2>=3.0.0\",\n    \"pydantic>=2.0.0\",\n    \"pyyaml>=6.0.0\",\n    \"gitpython>=3.1.0\",\n]\n\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",\n    \"pytest-cov>=4.0.0\",\n    \"mypy>=1.0.0\",\n    \"ruff>=0.1.0\",\n]\n\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py310\"\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"N\", \"W\"]\n\n[tool.mypy]\npython_version = \"3.10\"\nwarn_return_any = true\nwarn_unused_configs = true\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\npython_files = [\"test_*.py\"]\n```\n\n## Criterios de Aceptacion\n1. [ ] `pyproject.toml` actualizado con todas las dependencias\n2. [ ] `uv sync` ejecuta sin errores\n3. [ ] `uv run tac-bootstrap --help` muestra ayuda\n4. [ ] `uv run tac-bootstrap version` muestra \"tac-bootstrap v0.1.0\"\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv sync\nuv run tac-bootstrap --help\nuv run tac-bootstrap version\n```\n\n## NO hacer\n- No implementar comandos adicionales aun\n- No crear tests aun"}`

## Chore Description

Update `tac_bootstrap_cli/pyproject.toml` to ensure all required dependencies are properly configured and installed. The existing pyproject.toml already contains dependencies at version 0.6.0, but the task requires verifying that all dependencies from version 0.1.0 requirements are present and that the CLI commands work correctly.

The task focuses on:
1. Verifying the current pyproject.toml has all required dependencies
2. Ensuring the CLI entry point is correctly configured
3. Running `uv sync` to install/update dependencies
4. Validating that basic CLI commands (`--help`, `version`) work

## Current State Analysis

The existing `tac_bootstrap_cli/pyproject.toml` already has:
- All required production dependencies (typer, rich, jinja2, pydantic, pyyaml, gitpython)
- All required dev dependencies (pytest, pytest-cov, mypy, ruff)
- Correct entry point: `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`
- Build system configured with hatchling
- Proper tool configurations for ruff, mypy, pytest

The package structure exists at `tac_bootstrap_cli/tac_bootstrap/` with subdirectories:
- application/
- domain/
- infrastructure/
- interfaces/

## Relevant Files

- `tac_bootstrap_cli/pyproject.toml` - Already exists with v0.6.0 configuration, needs verification against v0.1.0 requirements
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI entry point, needs to exist with basic commands
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Package initialization
- `tac_bootstrap_cli/README.md` - Package documentation (if missing, create minimal version)

### New Files
None required - all files already exist. May need to verify/update:
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - Ensure it has version command

## Step by Step Tasks

### Task 1: Verify CLI Implementation
- Read `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` to check if `app` (Typer instance) and `version` command exist
- If missing or incomplete, implement minimal CLI with:
  - Typer app instance
  - `version` command that prints "tac-bootstrap v0.6.0" (current version)
  - Auto --help support from Typer

### Task 2: Verify pyproject.toml Configuration
- Read current `tac_bootstrap_cli/pyproject.toml`
- Confirm all dependencies from issue requirements are present (they already are)
- Verify entry point matches: `tac-bootstrap = "tac_bootstrap.interfaces.cli:app"`
- Version is already 0.6.0 (more recent than required 0.1.0)

### Task 3: Install Dependencies
- Run `cd tac_bootstrap_cli && uv sync` to ensure all dependencies are installed
- Verify installation completes without errors

### Task 4: Validate CLI Commands
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - should show help text
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap version` - should show version
- If version command doesn't exist, verify from Task 1 implementation

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Version command

## Notes

- The current pyproject.toml is at version 0.6.0, which is more recent than the required 0.1.0
- All dependencies in the issue are already present in the current configuration
- The main work is ensuring the CLI interface is properly implemented and commands work
- The package structure already exists under `tac_bootstrap_cli/tac_bootstrap/`
- No new files need to be created, only verification and potential updates to existing files
- Python version requirement (>=3.10) is already met in current configuration
- Additional dependency `packaging>=23.0` is present in current config (for version comparison)
