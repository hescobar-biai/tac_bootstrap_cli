# Chore: Create scout_files directory template

## Metadata
issue_number: `343`
adw_id: `chore_Tac_11_task_12`
issue_json: `{"number":343,"title":"Create scout_files directory template","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_12\n\nCreate the template for scout_files directory in generated projects.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2`\n\n**Implementation details:**\n- Create empty .gitkeep.j2 template\n- Ensures scout_files directory is created in generated projec"}`

## Chore Description
Create a `.gitkeep.j2` template file in the `scout_files` directory structure so that generated projects will have this directory created. The `scout_files` directory is used by the `/scout` slash command to store exploration outputs. This follows the same pattern as existing `context_bundles` and `hook_logs` directories in the agents folder.

## Relevant Files
Archivos relevantes para completar esta chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2` - NEW FILE to be created (empty template)
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/context_bundles/.gitkeep.j2` - Reference example (existing similar file)
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/hook_logs/.gitkeep.j2` - Reference example (existing similar file)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering system (context only)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2` - Empty Jinja2 template file to ensure directory creation

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create scout_files directory
- Create directory `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/`
- This ensures the directory structure exists in the templates

### Task 2: Create .gitkeep.j2 template file
- Create empty file `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2`
- This file should be empty (no content)
- The .j2 extension ensures Jinja2 processes it during project generation
- The .gitkeep ensures Git tracks the directory even when empty

### Task 3: Verify directory structure
- Verify the new directory matches the pattern of existing agent directories
- Check that `agents/scout_files/` now exists alongside `agents/context_bundles/` and `agents/hook_logs/`

### Task 4: Run validation commands
- Execute all validation commands to ensure zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a simple structural change to support the `/scout` slash command
- The directory follows the same pattern as `context_bundles` and `hook_logs`
- No code changes required, only directory and file creation
- The .gitkeep.j2 file should remain empty to serve its purpose of tracking an otherwise empty directory
