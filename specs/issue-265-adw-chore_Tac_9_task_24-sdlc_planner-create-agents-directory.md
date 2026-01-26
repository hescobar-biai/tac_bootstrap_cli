# Chore: Create agents directory structure in templates

## Metadata
issue_number: `265`
adw_id: `chore_Tac_9_task_24`
issue_json: `{"number":265,"title":"Create agents directory structure in templates","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_9_task_24\n\n**Description:**\nCreate the `agents/` directory in templates for agent definition files.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` (CREATE directory)"}`

## Chore Description
Create the `agents/` directory within the Claude templates structure. This directory will serve as the container for agent definition files that will be used during project generation. The directory should be created empty with a `.gitkeep` file to ensure git tracks the directory structure, allowing it to be copied during project generation.

This is a foundational chore task that establishes the directory structure for future agent-related features without prescribing specific file formats or agent definitions.

## Relevant Files
Files relevant to completing this chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/` - Parent directory where agents/ will be created. Already contains:
  - `commands/` - Command templates directory
  - `hooks/` - Hooks scripts directory
  - `output-styles/` - Output styling directory
  - `settings.json.j2` - Settings template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` - Directory to be created

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/.gitkeep` - Empty file to ensure git tracks the directory

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create agents directory
- Navigate to the templates/claude/ directory
- Create the `agents/` subdirectory

### Task 2: Add .gitkeep file
- Create an empty `.gitkeep` file inside `agents/` directory
- This ensures git tracks the empty directory structure

### Task 3: Verify directory structure
- List the contents of `templates/claude/` to confirm `agents/` directory exists
- Verify `.gitkeep` file is present in `agents/` directory

### Task 4: Validation
- Execute validation commands to ensure no regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a simple directory structure chore that requires no code changes
- The `agents/` directory is part of the template structure that will be copied during project generation
- No subdirectories, template files, or documentation are included initially per the auto-resolved clarifications
- The directory remains format-agnostic, allowing future tasks to define agent file formats (e.g., .py, .yaml, .json)
- This matches the existing pattern in the templates structure where `commands/`, `hooks/`, and `output-styles/` directories exist
