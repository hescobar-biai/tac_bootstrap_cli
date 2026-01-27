# Chore: Create security_logs directory structure in base repository

## Metadata
issue_number: `330`
adw_id: `chore_Tac_11_task_9`
issue_json: `{"number":330,"title":"Create security_logs directory structure in base repository*","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_11_task_9\n\nCreate the directory structure for security audit logs from the dangerous_command_blocker hook.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/security_logs/.gitkeep`\n\n**Implementation details:**\n- Create `agents/security_logs/` directory\n- Add `.gitkeep` file to preserve directory in git\n- This directory will store blocked command audit logs\n"}`

## Chore Description
Create the directory structure for security audit logs from the dangerous_command_blocker hook. This is a simple infrastructure task to ensure the `agents/security_logs/` directory exists in the repository and is tracked by git, even when empty.

The dangerous_command_blocker hook will write audit logs to this directory when potentially dangerous commands are blocked. The directory needs to exist in the base repository structure so that when TAC Bootstrap generates new projects, this directory structure is included.

## Relevant Files
Files for completing the chore:

### Existing Files
- `.claude/hooks/dangerous_command_blocker.py` - Hook that will write logs to this directory
- `PLAN_TAC_BOOTSTRAP.md` - Project plan to understand context
- `CLAUDE.md` - Agent guidelines

### New Files
- `agents/security_logs/.gitkeep` - Empty file to preserve directory in git

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create directory structure
- Create `agents/security_logs/` directory if it doesn't exist
- Verify directory path is relative to repository root

### Task 2: Add .gitkeep file
- Create empty `.gitkeep` file in `agents/security_logs/`
- This ensures the directory is tracked by git even when no logs exist

### Task 3: Verify structure
- Confirm directory exists at `agents/security_logs/`
- Confirm `.gitkeep` file exists
- Check that git will track the directory

### Task 4: Run validation commands
- Execute all validation commands to ensure no regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `ls -la agents/security_logs/` - Verify directory and .gitkeep exist
- `git status` - Confirm new files are tracked
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a simple infrastructure chore with no code changes
- The directory structure is needed for the dangerous_command_blocker hook to function properly
- The `.gitkeep` file is a convention to preserve empty directories in git
- This directory will be part of the template structure when TAC Bootstrap generates new projects
