# Chore: Synchronize trigger_cron.py.j2 template with root (user validation)

## Metadata
issue_number: `220`
adw_id: `chore_v_0_4_1_task_4`
issue_json: `{"number":220,"title":"Synchronize trigger_cron.py.j2 template with root (user validation)","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_0_4_1_task_4\n\n**Description:**\nThe root `trigger_cron.py` already has user assignment validation. Update the template to match the root file exactly.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_cron.py` (SOURCE - read only)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` (UPDATE)\n\n**Changes required in template:**\n- Add imports: `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me`\n- Add user validation check in `check_and_process_issues()` before processing each issue\n- Add `assign_issue_to_me()` call in `trigger_workflow()`\n- Add current user display in `main()` startup messages"}`

## Chore Description
The root `trigger_cron.py` has been updated with user assignment validation logic to ensure that only issues assigned to the current GitHub user are processed. The Jinja2 template version (`trigger_cron.py.j2`) needs to be synchronized to include these same user validation features while maintaining template variable substitutions.

**Key changes needed:**
1. Import the three user-related functions from `adw_modules.github`
2. Add user assignment check in the issue processing loop
3. Add issue assignment call in the workflow trigger function
4. Display current user information on startup

## Relevant Files

### Source (Read-only)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_cron.py` - The authoritative source file with user validation logic already implemented (lines 44-50 for imports, lines 296-297 for user check, lines 219-222 for assignment, lines 352-356 for startup messages)

### Template to Update
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_cron.py.j2` - The Jinja2 template that currently lacks the user validation logic

## Step by Step Tasks

### Task 1: Add user-related imports to template
- Update the imports section (lines 42-49) in the template to include:
  - `get_current_gh_user`
  - `is_issue_assigned_to_me`
  - `assign_issue_to_me`
- Match the exact import structure from the source file (lines 42-52)

### Task 2: Add user validation in check_and_process_issues()
- Locate the issue processing loop in `check_and_process_issues()` function (around line 286)
- Add the user validation check before processing workflow triggers:
  ```python
  # Check if issue is assigned to current user
  if not is_issue_assigned_to_me(str(issue_number), REPO_PATH):
      continue
  ```
- This should be placed after extracting `issue_number` and before checking for workflow info (matching lines 296-297 in source)

### Task 3: Add issue assignment in trigger_workflow()
- Locate the `trigger_workflow()` function (around line 171)
- Add the assignment call after setting up the logger and before posting the comment:
  ```python
  # Assign issue to current user
  try:
      assign_issue_to_me(str(issue_number))
  except Exception as e:
      logger.warning(f"Failed to assign issue: {e}")
  ```
- This should be placed around line 218 (matching lines 218-222 in source)

### Task 4: Add current user display in main()
- Update the `main()` function startup messages (around line 339)
- Add current user information display:
  ```python
  current_user = get_current_gh_user()
  print(f"INFO: Starting ADW cron trigger for {{ config.project.name }}")
  print(f"INFO: Repository: {REPO_PATH}")
  print(f"INFO: Current user: {current_user or 'unknown'}")
  print(f"INFO: Only processing issues assigned to current user")
  print(f"INFO: Polling interval: {interval} seconds")
  print(f"INFO: Supported workflows: {len(AVAILABLE_ADW_WORKFLOWS)}")
  ```
- Match lines 352-358 from source while preserving Jinja2 template variables

### Task 5: Validate changes
- Execute all validation commands to ensure no regressions
- Verify template renders correctly with sample config
- Ensure all Jinja2 variables are preserved

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The template must maintain all existing Jinja2 variable substitutions (e.g., `{{ config.project.name }}`, `{{ config.agentic.cron_interval | default(20) }}`)
- The source file serves as the authoritative reference - the template should match its logic exactly
- User validation prevents the cron trigger from processing issues assigned to other users
- The assignment call ensures that triggered workflows automatically assign the issue to the executing user
