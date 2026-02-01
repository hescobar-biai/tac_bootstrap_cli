# Chore: Create .claude/data/sessions directory with .gitkeep

## Metadata
issue_number: `487`
adw_id: `chore_Tac_12_task_35`
issue_json: Task 35/49 - CHORE - Create .claude/data/sessions directory with .gitkeep

## Chore Description

Create a new directory structure for session data in the TAC Bootstrap project. This involves:
1. Creating the `.claude/data/sessions/` directory in the base repository with a `.gitkeep` file
2. Creating a Jinja2 template for the `.gitkeep` file that will be used by the CLI generator
3. Updating `scaffold_service.py` to include this directory creation in the scaffolding process

The sessions directory will be used to store session-related data for the Claude Code workflow, part of Wave 5 - Status Line & Data Directories.

## Relevant Files

### Existing Files
- `.claude/` - Base Claude configuration directory (template base)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that builds and applies scaffold plans
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template repository managing Jinja2 templates
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Data models for scaffold plans

### New Files
- `.claude/data/sessions/.gitkeep` - Base repository gitkeep file
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/.gitkeep.j2` - Jinja2 template for CLI generation

## Step by Step Tasks

### Task 1: Create base repository directory and gitkeep file
- Create `.claude/data/` directory if it doesn't exist
- Create `.claude/data/sessions/` directory
- Create `.claude/data/sessions/.gitkeep` file (empty file to preserve directory in git)
- Verify directory structure exists

### Task 2: Create Jinja2 template file
- Navigate to `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/`
- Create the directory structure if it doesn't exist
- Create `.gitkeep.j2` template file (empty Jinja2 template, identical to base file)
- Verify template file exists and is empty

### Task 3: Verify scaffold_service.py configuration
- Check if `scaffold_service.py` already includes empty directory creation logic
- If not, review how other similar directories are handled in the configuration
- Document findings (no changes needed if empty directories are automatically handled by template structure)

### Task 4: Validation
- Verify `.claude/data/sessions/` directory exists in base repository
- Verify `.gitkeep` file exists in that directory
- Verify template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/.gitkeep.j2`
- Run validation commands below

## Validation Commands
Execute all commands to validate with zero regressions:

- `git status` - Verify new files are tracked
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- The `.gitkeep` file is a convention used to preserve empty directories in git repositories
- Since this is a template-based system, the directory structure in `tac_bootstrap_cli/tac_bootstrap/templates/structure/` mirrors the structure that will be generated in new projects
- Both the base `.claude/data/sessions/.gitkeep` and the template `.gitkeep.j2` should be present
- If scaffold_service.py needs updates, they should preserve idempotency as noted in the service's documentation
