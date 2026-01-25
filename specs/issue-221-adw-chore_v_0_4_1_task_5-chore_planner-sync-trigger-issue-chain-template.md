# Chore: Synchronize trigger_issue_chain.py.j2 template with root (user validation)

## Metadata
issue_number: `221`
adw_id: `chore_v_0_4_1_task_5`
issue_json: `{"number":221,"title":"Synchronize trigger_issue_chain.py.j2 template with root (user validation)","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_0_4_1_task_5\n\n**Description:**\nThe root `trigger_issue_chain.py` already has user assignment validation. Update the template to match the root file exactly.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_issue_chain.py` (SOURCE - read only)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2` (UPDATE)\n\n**Changes required in template:**\n- Add imports: `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me`\n- Modify `get_current_issue()` to check assignment before returning issue\n- Add `assign_issue_to_me()` call in `trigger_workflow()`\n- Add current user display in `main()` startup messages\n"}`

## Chore Description
The root file `trigger_issue_chain.py` has been enhanced with user assignment validation to ensure only issues assigned to the current GitHub user are processed. The Jinja2 template needs to be synchronized with these improvements to ensure generated projects have the same functionality.

Key differences between root and template:
1. Root imports `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me` from `adw_modules.github`
2. Root's `get_current_issue()` checks if issue is assigned to current user before returning
3. Root's `trigger_workflow()` assigns issue to current user
4. Root's `main()` displays current user and filtering message

## Relevant Files
Files needed to complete this chore:

- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_triggers/trigger_issue_chain.py` - SOURCE file with user validation logic (read-only reference)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_chain.py.j2` - TARGET template to update

### New Files
None required.

## Step by Step Tasks

### Task 1: Add missing imports to template
- Add `get_current_gh_user`, `is_issue_assigned_to_me`, `assign_issue_to_me` to the imports from `adw_modules.github` (line 40-47)
- Match the exact import structure from the root file

### Task 2: Update get_current_issue() function
- Modify `get_current_issue()` function (lines 118-125) to check assignment
- Add `is_issue_assigned_to_me()` check after verifying issue is open
- Add informative message when issue is open but not assigned to current user
- Match lines 118-129 from root file exactly

### Task 3: Add assign_issue_to_me() call in trigger_workflow()
- Add the assignment call in `trigger_workflow()` function after logger setup (after line 248)
- Include try-except block to handle assignment failures gracefully
- Match lines 254-258 from root file

### Task 4: Update main() startup messages
- Add `get_current_gh_user()` call at start of `main()` (after line 367)
- Add current user display message (line 382 in root)
- Add filtering message about only processing assigned issues (line 383 in root)
- Match lines 379-383 from root file

### Task 5: Validate changes and run tests
- Run pytest to ensure no regressions: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run ruff linting: `cd tac_bootstrap_cli && uv run ruff check .`
- Run smoke test: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify template matches root file logic exactly

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a template synchronization task - the root file already has the correct implementation
- The template uses Jinja2 variables (e.g., `{{ config.project.name }}`), which should be preserved
- Focus on adding the user validation logic while maintaining all existing Jinja2 template variables
- The changes ensure generated projects filter issues by current user assignment, preventing accidental processing of other users' issues
