# Chore: Create expert agents directory structure in templates

## Metadata
issue_number: `269`
adw_id: `chore_Tac_9_task_28`
issue_json: `{"number":269,"title":"Create expert agents directory structure in templates","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_9_task_28\n\n**Description:**\nCreate the `commands/experts/cc_hook_expert/` directory structure in templates for expert agent commands.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/` (CREATE directory)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/` (CREATE directory)\n"}`

## Chore Description
Create the directory structure `templates/claude/commands/experts/cc_hook_expert/` within the TAC Bootstrap CLI template system. This structure will organize expert agent commands, starting with the `cc_hook_expert` subdirectory. Since git doesn't track empty directories, .gitkeep files will be added to ensure the directory structure is preserved in version control and generated projects.

## Relevant Files

### Existing Files to Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` - Existing commands directory with 36 command templates (background.md.j2, bug.md.j2, chore.md.j2, etc.)
  - **Why relevant**: Shows current template structure pattern to maintain consistency

- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template repository that manages Jinja2 template loading and rendering
  - **Why relevant**: Handles template discovery via `list_templates()` method; will discover files in new directory structure

- `tac_bootstrap_cli/tests/test_template_repo.py` - Tests for template repository functionality
  - **Why relevant**: Need to add test validation for new directory structure

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/.gitkeep` - Ensures `experts/` directory is tracked in git
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/.gitkeep` - Ensures `cc_hook_expert/` subdirectory is tracked in git

## Step by Step Tasks

### Task 1: Create experts directory structure with .gitkeep files
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/` directory
- Add `.gitkeep` file in `experts/` directory
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/` subdirectory
- Add `.gitkeep` file in `cc_hook_expert/` directory
- Verify directories are created with standard permissions (755)

### Task 2: Add test validation for directory structure
- Add test case in `tests/test_template_repo.py` to verify `list_templates()` discovers the new directory structure
- Test should verify that templates can be listed from the `claude/commands/experts/` path
- Ensure test validates that the directory structure exists in template repository

### Task 3: Validate with all validation commands
- Run pytest to ensure no regressions
- Run ruff linting to ensure code quality
- Run smoke test to verify CLI still works

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Following YAGNI principle: only creating `cc_hook_expert` subdirectory as specified, no additional expert types
- Using `.gitkeep` convention to preserve empty directory structure in git
- No special permissions needed - using standard directory permissions (755/default)
- Directory follows existing pattern: `commands/{category}/{subcategory}/` where names use snake_case
- Template repository's `list_templates()` method will automatically discover files in this new structure
- This is infrastructure work - no functional template files needed yet (those will come in future feature tasks)
