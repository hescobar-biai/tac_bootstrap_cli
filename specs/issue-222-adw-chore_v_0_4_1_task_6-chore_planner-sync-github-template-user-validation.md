# Chore: Synchronize github.py.j2 template with root (user validation functions)

## Metadata
issue_number: `222`
adw_id: `chore_v_0_4_1_task_6`
issue_json: `{"number":222,"title":"Synchronize github.py.j2 template with root (user validation functions)","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_v_0_4_1_task_6\n\n\n**Description:**\nThe root `github.py` already has user validation functions. Update the template to include these three new functions.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/github.py` (SOURCE - read only)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2` (UPDATE)\n\n**Functions to add to template:**\n1. `get_current_gh_user() -> Optional[str]` - Returns the authenticated GitHub user login\n2. `is_issue_assigned_to_me(issue_number: str, repo_path: Optional[str] = None) -> bool` - Checks if issue is assigned to current user\n3. `assign_issue_to_me(issue_id: str) -> bool` - Assigns issue to current user using `@me`"}`

## Chore Description

The root `github.py` module has been updated with three new functions for user validation and assignment:
- `get_current_gh_user()`: Fetches the authenticated GitHub user login via `gh api user`
- `is_issue_assigned_to_me()`: Checks if an issue is assigned to the current user
- `assign_issue_to_me()`: Assigns an issue to the current user using the `@me` shorthand

These functions need to be synchronized to the Jinja2 template (`github.py.j2`) so that generated projects include this functionality.

## Relevant Files

### Source File (Read-Only)
- `adws/adw_modules/github.py` - Contains the three new functions (lines 290-388):
  - `get_current_gh_user()` (lines 290-308)
  - `is_issue_assigned_to_me()` (lines 311-351)
  - `assign_issue_to_me()` (lines 354-387)

### Target File (Update Required)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2` - Template that needs the three functions added

### New Files
None - this is a synchronization task only.

## Step by Step Tasks

### Task 1: Read the target template file
- Read `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/github.py.j2`
- Identify where the three new functions should be inserted (after `fetch_issue_comments()` function, before `find_keyword_from_comment()`)

### Task 2: Add the three user validation functions to the template
- Copy the three functions from `adws/adw_modules/github.py` (lines 290-388)
- Insert them into the template in the correct location
- Ensure proper formatting and indentation matches the template style
- Verify no Jinja2 template variables are needed in these functions (they should be plain Python)

### Task 3: Verify the synchronization
- Visually compare the source functions with the template functions
- Ensure all three functions are present and complete:
  - `get_current_gh_user()` with correct implementation
  - `is_issue_assigned_to_me()` with correct implementation
  - `assign_issue_to_me()` with correct implementation

### Task 4: Run validation commands
- Execute all validation commands to ensure no regressions

## Validation Commands

Executar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- The three functions are complete implementations and should be copied verbatim from the source
- No Jinja2 templating is required within these functions - they are pure Python
- The functions use subprocess calls to `gh` CLI, which is consistent with other functions in the module
- The insertion point should be after `fetch_issue_comments()` and before `find_keyword_from_comment()` to maintain logical grouping
