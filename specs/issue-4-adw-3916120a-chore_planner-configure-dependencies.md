# Chore: Configure project dependencies

## Metadata
issue_number: `4`
adw_id: `3916120a`
issue_json: `{"number":4,"title":"chore: #3 - TAREA 1.2: Configurar dependencias del proyecto","body":"## Summary\n\nThis PR configures the project dependencies for the `tac-bootstrap` CLI package. The implementation updates `pyproject.toml` with all required production and development dependencies, following the specifications in issue #3.\n\n## Implementation Plan\n\nSee: [specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md](specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md)\n\n## Changes\n\n### Dependencies Added\n\n**Production:**\n- typer>=0.9.0 - CLI framework for commands and options\n- rich>=13.0.0 - Terminal UI with tables, panels, colors\n- jinja2>=3.0.0 - Template rendering engine\n- pydantic>=2.0.0 - Data validation and schemas\n- pyyaml>=6.0.0 - YAML parsing for config files\n- gitpython>=3.1.0 - Git operations integration\n\n**Development:**\n- pytest>=7.0.0 - Testing framework\n- pytest-cov>=4.0.0 - Code coverage reporting\n- mypy>=1.0.0 - Static type checking\n- ruff>=0.1.0 - Linting and formatting\n\n### Configuration\n\n- Added entry point script: `tac-bootstrap`\n- Configured build system with hatchling\n- Added tool configurations for ruff, mypy, and pytest\n- Set Python version requirement to >=3.10\n\n## Checklist\n\n- [x] Updated pyproject.toml with all production dependencies\n- [x] Added development dependencies\n- [x] Configured entry point script\n- [x] Set up build system configuration\n- [x] Added tool configurations (ruff, mypy, pytest)\n\n## Issue\n\nCloses #3\n\n## ADW Tracking\n\nADW ID: e29f22c3"}`

## Chore Description
This chore verifies that the project dependencies are already properly configured in `pyproject.toml`. Based on the issue description, all the required dependencies have been added to the project, including:

**Production dependencies:**
- typer>=0.9.0 - CLI framework
- rich>=13.0.0 - Terminal UI
- jinja2>=3.0.0 - Template engine
- pydantic>=2.0.0 - Data validation
- pyyaml>=6.0.0 - YAML parsing
- gitpython>=3.1.0 - Git operations
- packaging>=23.0 - Version comparison

**Development dependencies:**
- pytest>=7.0.0 - Testing framework
- pytest-cov>=4.0.0 - Coverage reporting
- mypy>=1.0.0 - Type checking
- ruff>=0.1.0 - Linting and formatting

The configuration is complete with entry points, build system, and tool configurations. This chore validates that everything is working correctly.

## Relevant Files
Files relevant to this chore:

- `tac_bootstrap_cli/pyproject.toml` - Contains all dependency configurations that need validation
- `config.yml` - Project configuration with commands to test
- `specs/issue-3-adw-e29f22c3-sdlc_planner-configure-dependencies.md` - Original implementation plan reference

### New Files
No new files required - this is a validation chore.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify dependency installation
- Navigate to `tac_bootstrap_cli/` directory
- Run `uv sync` to ensure all dependencies are installed correctly
- Verify that both production and dev dependencies are available
- Check for any missing or conflicting dependencies

### Task 2: Validate entry point configuration
- Test that the `tac-bootstrap` entry point is properly configured
- Run `uv run tac-bootstrap --help` to verify the CLI works
- Ensure the entry point resolves to `tac_bootstrap.interfaces.cli:app`

### Task 3: Verify tool configurations
- Check that ruff configuration is valid by running lint check
- Check that mypy configuration is valid (if source files exist)
- Check that pytest configuration is valid
- Ensure all tool settings in pyproject.toml are syntactically correct

### Task 4: Run validation commands
- Execute all validation commands listed below
- Verify zero regressions
- Confirm all checks pass

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv sync` - Install dependencies
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests (if tests exist)

## Notes
- This is a verification/validation chore since dependencies were already configured in issue #3
- The focus is on ensuring everything works correctly rather than making new changes
- If any validation fails, the specific issue should be identified and fixed
- The pyproject.toml file shows dependencies are already in place with correct versions
