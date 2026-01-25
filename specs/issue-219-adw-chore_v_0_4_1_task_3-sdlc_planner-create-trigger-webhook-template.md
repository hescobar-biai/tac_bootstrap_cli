# Chore: Create trigger_webhook.py.j2 template (sync from root)

## Metadata
issue_number: `219`
adw_id: `chore_v_0_4_1_task_3`
issue_json: `{"number":219,"title":"[CHORE] Create trigger_webhook.py.j2 template (sync from root)","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_0_4_1_task_3\n\n**Description:**\nCreate the missing Jinja2 template for `trigger_webhook.py`. The root file already exists with user assignment validation logic. Copy content to create the template.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_webhook.py` (SOURCE - read only)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2` (CREATE)\n\n**Implementation:**\n- Copy the full content from the root `trigger_webhook.py` to create `trigger_webhook.py.j2`\n- The template will include:\n  - `get_current_gh_user()` import\n  - `is_issue_assigned_to_me()` import\n  - `assign_issue_to_me()` import\n  - User assignment validation before workflow execution\n  - Startup message showing current user"}`

## Chore Description
The root directory contains a functional `trigger_webhook.py` file in `adws/adw_triggers/` with complete webhook functionality including user assignment validation. However, the corresponding Jinja2 template is missing in the `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/` directory. This means when the CLI generates a new project, this trigger file will not be created.

The task is to copy the full content from the root `trigger_webhook.py` and create the corresponding `.j2` template file so it can be included when generating new TAC Bootstrap projects.

## Relevant Files
Files needed to complete this chore:

- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_webhook.py` - SOURCE file containing the complete webhook implementation (361 lines) with all necessary imports and logic
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2` - TARGET template file to be created
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/__init__.py.j2` - Existing template for reference on template structure
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` - Existing template for reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2` - The new template file

## Step by Step Tasks

### Task 1: Copy source file to create template
- Read the source file at `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_webhook.py`
- Create the template file at `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_webhook.py.j2`
- Copy the complete content (361 lines) including:
  - Shebang and script dependencies
  - All imports (fastapi, uvicorn, dotenv, subprocess, sys)
  - GitHub user validation imports (`get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me`)
  - All utility imports from adw_modules
  - Configuration (PORT, DEPENDENT_WORKFLOWS, etc.)
  - FastAPI app definition
  - Webhook endpoint `/gh-webhook` with complete logic
  - Health check endpoint `/health`
  - Main block with startup messages showing current user

### Task 2: Verify template file was created correctly
- Verify the template file exists at the correct path
- Verify file has 361 lines matching the source
- Verify all key functionality is present:
  - User assignment validation (lines 135-144 in source)
  - Startup message with current user (lines 353-356 in source)
  - All GitHub helper function imports (lines 34-37 in source)

### Task 3: Run validation commands
- Execute all validation commands to ensure no regressions
- Verify tests pass
- Verify linting passes
- Verify CLI smoke test passes

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a straightforward copy operation - the source file is already complete and tested
- No modifications or Jinja2 variables are needed as this file does not use configuration templating
- The template directory already exists and contains other trigger templates (trigger_cron.py.j2, trigger_issue_chain.py.j2)
- The source file is 361 lines and contains critical user assignment validation logic that must be preserved exactly
