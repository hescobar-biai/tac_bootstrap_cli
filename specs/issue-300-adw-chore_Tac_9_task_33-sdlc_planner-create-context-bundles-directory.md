# Chore: Create agents/context_bundles directory in root

## Metadata
issue_number: `300`
adw_id: `chore_Tac_9_task_33`
issue_json: `{"number":300,"title":"Create agents/context_bundles directory in root","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_9_task_33\n\n**Description:**\nCreate the directory for storing context bundle JSONL files at runtime.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/context_bundles/` (CREATE directory)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/context_bundles/.gitkeep` (CREATE)\n\n"}`

## Chore Description
Create the directory structure for storing context bundle JSONL files at runtime. This directory will be used by the TAC Bootstrap CLI to store generated context bundles that agents can load. The directory needs to exist in the root of the project with a `.gitkeep` file to ensure it's tracked by git even when empty.

## Relevant Files
Files needed to complete this chore:

- `agents/context_bundles/` - Directory to create for storing context bundle JSONL files
- `agents/context_bundles/.gitkeep` - Empty file to ensure directory is tracked by git

### New Files
- `agents/context_bundles/.gitkeep` - Marker file to keep empty directory in git

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create agents directory structure
- Create `agents/` directory if it doesn't exist
- Create `agents/context_bundles/` subdirectory

### Task 2: Add .gitkeep file
- Create empty `.gitkeep` file in `agents/context_bundles/` directory
- This ensures the directory is tracked by git even when empty

### Task 3: Validate directory creation
- Verify that `agents/context_bundles/` directory exists
- Verify that `.gitkeep` file exists in the directory
- Run validation commands to ensure no regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `ls -la agents/context_bundles/` - Verify directory and .gitkeep exist

## Notes
- This is a simple infrastructure setup task
- The directory will be used by future features that generate context bundles
- The `.gitkeep` file is a convention to keep empty directories in git
- No code changes are required, only directory/file creation
