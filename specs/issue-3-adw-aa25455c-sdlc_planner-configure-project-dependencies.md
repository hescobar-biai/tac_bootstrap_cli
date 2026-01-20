# Chore: Configure Project Dependencies

## Metadata
issue_number: `3`
adw_id: `aa25455c`
issue_json: `{"number":3,"title":"TAREA 1.2: Configurar dependencias del proyecto","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar\nlas dependencias del proyecto para poder usar las librerias necesarias.\n\n## Objetivo\nActualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.\n\n## Archivo a Modificar\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`\n\n## Dependencias Requeridas\n\n### Dependencias de Produccion\n```toml\ndependencies = [\n    \"typer>=0.9.0\",        # CLI framework - maneja comandos, argumentos, opciones\n    \"rich>=13.0.0\",        # UI terminal - tablas, paneles, colores, progress bars\n    \"jinja2>=3.0.0\",       # Templates - renderizado de archivos parametrizables\n    \"pydantic>=2.0.0\",     # Validacion - schemas para config.yml y modelos\n    \"pyyaml>=6.0.0\",       # YAML - lectura/escritura de config.yml\n    \"gitpython>=3.1.0\",    # Git - operaciones git init, commit, etc.\n]\n```\n\n### Dependencias de Desarrollo\n```toml\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",       # Testing framework\n    \"pytest-cov>=4.0.0\",   # Coverage reports\n    \"mypy>=1.0.0\",         # Type checking\n    \"ruff>=0.1.0\",         # Linting y formatting\n]\n```\n\n### Entry Points\n```toml\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n```\n\n### Build System\n```toml\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n```\n\n## Acciones a Ejecutar\n\n1. Actualizar `pyproject.toml` con el contenido completo\n2. Ejecutar `uv sync` para instalar dependencias\n3. Verificar que `tac-bootstrap --help` funciona\n\n## pyproject.toml Completo\n\n```toml\n[project]\nname = \"tac-bootstrap\"\nversion = \"0.1.0\"\ndescription = \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\nreadme = \"README.md\"\nrequires-python = \">=3.10\"\nlicense = {text = \"MIT\"}\nauthors = [\n    {name = \"TAC Team\"}\n]\nkeywords = [\"cli\", \"claude\", \"agentic\", \"tac\", \"bootstrap\"]\n\ndependencies = [\n    \"typer>=0.9.0\",\n    \"rich>=13.0.0\",\n    \"jinja2>=3.0.0\",\n    \"pydantic>=2.0.0\",\n    \"pyyaml>=6.0.0\",\n    \"gitpython>=3.1.0\",\n]\n\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",\n    \"pytest-cov>=4.0.0\",\n    \"mypy>=1.0.0\",\n    \"ruff>=0.1.0\",\n]\n\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py310\"\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"N\", \"W\"]\n\n[tool.mypy]\npython_version = \"3.10\"\nwarn_return_any = true\nwarn_unused_configs = true\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\npython_files = [\"test_*.py\"]\n```\n\n## Criterios de Aceptacion\n1. [ ] `pyproject.toml` actualizado con todas las dependencias\n2. [ ] `uv sync` ejecuta sin errores\n3. [ ] `uv run tac-bootstrap --help` muestra ayuda\n4. [ ] `uv run tac-bootstrap version` muestra \"tac-bootstrap v0.1.0\"\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv sync\nuv run tac-bootstrap --help\nuv run tac-bootstrap version\n```\n\n## NO hacer\n- No implementar comandos adicionales aun\n- No crear tests aun"}`

## Chore Description
Update the `pyproject.toml` file to include all required dependencies for the TAC Bootstrap CLI. The project currently has most dependencies configured, but is missing `gitpython` which is needed for Git operations. Also need to add tool configurations for `ruff`, `mypy`, and `pytest` to ensure consistent code quality standards.

The CLI already has the basic structure and can run the `version` command, but needs:
1. GitPython dependency for future Git operations
2. Tool configurations for linting, type checking, and testing
3. Verification that all dependencies install correctly with `uv sync`

## Relevant Files
Files to complete this chore:

- `tac_bootstrap_cli/pyproject.toml` - Main configuration file that needs to be updated with GitPython dependency and tool configurations
- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI entrypoint, verify it works after dependency updates
- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contains `__version__` variable used by version command

### New Files
No new files required for this chore.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Update pyproject.toml with GitPython dependency
- Add `gitpython>=3.1.0` to the dependencies list in `pyproject.toml`
- Currently the file has: typer, rich, jinja2, pydantic, pyyaml
- Need to add: gitpython>=3.1.0

### Task 2: Add tool configurations to pyproject.toml
- Add `[tool.ruff]` section with `line-length = 100` and `target-version = "py310"`
- Add `[tool.ruff.lint]` section with `select = ["E", "F", "I", "N", "W"]`
- Add `[tool.mypy]` section with `python_version = "3.10"`, `warn_return_any = true`, `warn_unused_configs = true`
- Add `[tool.pytest.ini_options]` section with `testpaths = ["tests"]` and `python_files = ["test_*.py"]`

### Task 3: Install dependencies with uv sync
- Run `cd tac_bootstrap_cli && uv sync` to install all dependencies including the new GitPython
- Verify no errors occur during installation
- This will update the lock file and virtual environment

### Task 4: Verify CLI functionality
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap --help` to verify the CLI works
- Run `cd tac_bootstrap_cli && uv run tac-bootstrap version` to verify version command outputs "tac-bootstrap v0.1.0"
- Both commands should execute without errors

### Task 5: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Verify tests, linting, and smoke tests pass

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Verify version output

## Notes
- The pyproject.toml already has most of the required structure from TAREA 1.1
- Only missing dependency is `gitpython>=3.1.0` and tool configurations
- The CLI infrastructure is already in place and working (version command exists)
- No need to implement additional commands or create tests in this chore
- Focus is purely on dependency management and configuration
