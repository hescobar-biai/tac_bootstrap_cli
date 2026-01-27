# Chore: Configure Project Dependencies

## Metadata
issue_number: `3`
adw_id: `8ec7c5ed`
issue_json: `{"number":3,"title":"TAREA 1.2: Configurar dependencias del proyecto","body":"# Prompt para Agente\n\n## Contexto\nYa tenemos la estructura base del paquete `tac_bootstrap_cli`. Ahora necesitamos configurar\nlas dependencias del proyecto para poder usar las librerias necesarias.\n\n## Objetivo\nActualizar `pyproject.toml` con todas las dependencias necesarias e instalarlas con `uv`.\n\n## Archivo a Modificar\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`\n\n## Dependencias Requeridas\n\n### Dependencias de Produccion\n```toml\ndependencies = [\n    \"typer>=0.9.0\",        # CLI framework - maneja comandos, argumentos, opciones\n    \"rich>=13.0.0\",        # UI terminal - tablas, paneles, colores, progress bars\n    \"jinja2>=3.0.0\",       # Templates - renderizado de archivos parametrizables\n    \"pydantic>=2.0.0\",     # Validacion - schemas para config.yml y modelos\n    \"pyyaml>=6.0.0\",       # YAML - lectura/escritura de config.yml\n    \"gitpython>=3.1.0\",    # Git - operaciones git init, commit, etc.\n]\n```\n\n### Dependencias de Desarrollo\n```toml\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",       # Testing framework\n    \"pytest-cov>=4.0.0\",   # Coverage reports\n    \"mypy>=1.0.0\",         # Type checking\n    \"ruff>=0.1.0\",         # Linting y formatting\n]\n```\n\n### Entry Points\n```toml\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n```\n\n### Build System\n```toml\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n```\n\n## Acciones a Ejecutar\n\n1. Actualizar `pyproject.toml` con el contenido completo\n2. Ejecutar `uv sync` para instalar dependencias\n3. Verificar que `tac-bootstrap --help` funciona\n\n## pyproject.toml Completo\n\n```toml\n[project]\nname = \"tac-bootstrap\"\nversion = \"0.1.0\"\ndescription = \"CLI to bootstrap Agentic Layer for Claude Code with TAC patterns\"\nreadme = \"README.md\"\nrequires-python = \">=3.10\"\nlicense = {text = \"MIT\"}\nauthors = [\n    {name = \"TAC Team\"}\n]\nkeywords = [\"cli\", \"claude\", \"agentic\", \"tac\", \"bootstrap\"]\n\ndependencies = [\n    \"typer>=0.9.0\",\n    \"rich>=13.0.0\",\n    \"jinja2>=3.0.0\",\n    \"pydantic>=2.0.0\",\n    \"pyyaml>=6.0.0\",\n    \"gitpython>=3.1.0\",\n]\n\n[project.optional-dependencies]\ndev = [\n    \"pytest>=7.0.0\",\n    \"pytest-cov>=4.0.0\",\n    \"mypy>=1.0.0\",\n    \"ruff>=0.1.0\",\n]\n\n[project.scripts]\ntac-bootstrap = \"tac_bootstrap.interfaces.cli:app\"\n\n[build-system]\nrequires = [\"hatchling\"]\nbuild-backend = \"hatchling.build\"\n\n[tool.ruff]\nline-length = 100\ntarget-version = \"py310\"\n\n[tool.ruff.lint]\nselect = [\"E\", \"F\", \"I\", \"N\", \"W\"]\n\n[tool.mypy]\npython_version = \"3.10\"\nwarn_return_any = true\nwarn_unused_configs = true\n\n[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\npython_files = [\"test_*.py\"]\n```\n\n## Criterios de Aceptacion\n1. [ ] `pyproject.toml` actualizado con todas las dependencias\n2. [ ] `uv sync` ejecuta sin errores\n3. [ ] `uv run tac-bootstrap --help` muestra ayuda\n4. [ ] `uv run tac-bootstrap version` muestra \"tac-bootstrap v0.1.0\"\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv sync\nuv run tac-bootstrap --help\nuv run tac-bootstrap version\n```\n\n## NO hacer\n- No implementar comandos adicionales aun\n- No crear tests aun"}`

## Chore Description

This chore involves verifying and documenting that the project dependencies in `pyproject.toml` are already properly configured. The current state shows that:

1. All required production dependencies are present and with appropriate versions
2. Development dependencies are configured in both `[project.optional-dependencies]` and `[dependency-groups]` sections
3. The CLI entry point `tac-bootstrap` is correctly configured
4. Build system using `hatchling` is in place
5. Tool configurations for `ruff`, `mypy`, and `pytest` are properly set up

The actual configuration is MORE complete than the issue requirements, including additional dependencies like `packaging` and `types-PyYAML`, and the version is already at 0.6.0 (not 0.1.0 as in the requirements).

## Relevant Files

Files relevant to this chore:

- `tac_bootstrap_cli/pyproject.toml` - Main project configuration file that already contains all required dependencies and more. Current version is 0.6.0 with enhanced configuration including packaging and type stubs.

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py` - CLI entry point that the `tac-bootstrap` script command points to. Already functional and tested.

### New Files
No new files required - all configuration is already in place.

## Step by Step Tasks

### Task 1: Verify Current Configuration
- Read `tac_bootstrap_cli/pyproject.toml` to confirm all dependencies are present
- Verify the current configuration meets or exceeds the requirements in the issue
- Document any discrepancies between the issue requirements and current state

### Task 2: Test Dependencies Installation
- Execute `cd tac_bootstrap_cli && uv sync` to verify dependencies install correctly
- Confirm no errors occur during dependency resolution

### Task 3: Validate CLI Functionality
- Execute `cd tac_bootstrap_cli && uv run tac-bootstrap --help` to verify CLI works
- Execute `cd tac_bootstrap_cli && uv run tac-bootstrap version` to check version output
- Note that the current version is 0.6.0, not 0.1.0 as mentioned in the issue

### Task 4: Run Validation Commands
Execute all validation commands to ensure zero regressions.

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv sync` - Install/verify dependencies
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI help
- `cd tac_bootstrap_cli && uv run tac-bootstrap version` - Verify version command
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting

## Notes

**CURRENT STATE ANALYSIS:**

The dependencies are already configured and exceed the requirements from the issue:

**Production Dependencies (ALL PRESENT):**
- ✅ `typer>=0.9.0` (configured)
- ✅ `rich>=13.0.0` (configured as 13.7.0)
- ✅ `jinja2>=3.0.0` (configured as 3.1.2)
- ✅ `pydantic>=2.0.0` (configured as 2.5.0)
- ✅ `pyyaml>=6.0.0` (configured as 6.0.1)
- ✅ `gitpython>=3.1.0` (configured)
- ➕ `packaging>=23.0` (additional - for version comparison)

**Dev Dependencies (ALL PRESENT):**
- ✅ `pytest>=7.0.0` (configured as 7.4.0 and 9.0.2 in dependency-groups)
- ✅ `pytest-cov>=4.0.0` (configured as 4.1.0 and 7.0.0)
- ✅ `mypy>=1.0.0` (configured as 1.7.0 and 1.19.1)
- ✅ `ruff>=0.1.0` (configured as 0.1.0 and 0.14.13)
- ➕ `types-PyYAML>=6.0.0` (additional - for type checking)

**Configuration (ALL PRESENT):**
- ✅ Entry point `tac-bootstrap` correctly mapped
- ✅ Build system using `hatchling`
- ✅ Tool configurations for ruff, mypy, pytest
- ➕ Enhanced mypy with `strict = true`

**VERSION DISCREPANCY:**
The issue mentions version 0.1.0, but the project is already at 0.6.0, indicating this is a more mature state than the issue originally targeted.

**CONCLUSION:**
This chore is essentially **ALREADY COMPLETED**. The task is to verify functionality and document that all requirements are met (and exceeded).
