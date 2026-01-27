# Chore: Update scaffold_service.py to render new templates

## Metadata
issue_number: `362`
adw_id: `chore_Tac_11_task_13`
issue_json: `{"number":362,"title":"Update scaffold_service.py to render new templates","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_13\n\n\nUpdate the scaffold service to include the new templates in the rendering process.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n\n**Implementation details:**\n- Add `dangerous_command_blocker.py.j2` to hooks rendering\n- Add `scout.md.j2` to commands rendering\n- Add `question.md.j2` to commands rendering\n- Add `security_logs/.gitkeep.j2` to structure rendering\n- Add `scout_files/.gitkeep.j2` to structure rendering\n- Verify template paths are correct"}`

## Chore Description
Update the scaffold service to include newly created templates in the rendering process. This includes adding two new slash commands (`scout` and `question`), one new hook (`dangerous_command_blocker.py`), and two new agent directories (`security_logs` and `scout_files`) with `.gitkeep` files to preserve them in Git.

## Relevant Files
Files to complete this chore:

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Main file to update. Contains the `_add_claude_files` method for commands/hooks and `_add_directories` method for directory structure.
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2` - New scout command template (verify exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2` - New question command template (verify exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2` - New security hook template (verify exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/security_logs/.gitkeep.j2` - New directory marker (verify exists)
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/agents/scout_files/.gitkeep.j2` - New directory marker (verify exists)

### New Files
No new files required - only modifications to existing `scaffold_service.py`

## Step by Step Tasks

### Task 1: Add new command templates to _add_claude_files method
- Add `"scout"` to the commands list in `_add_claude_files` method (around line 291-292)
- Add `"question"` to the commands list in `_add_claude_files` method (around line 291-292)
- Maintain alphabetical/logical ordering within the "Utility commands" section

### Task 2: Add new hook template to _add_claude_files method
- Add `("dangerous_command_blocker.py", "Security validation hook")` to the hooks list in `_add_claude_files` method (around line 303-311)
- Maintain logical ordering (security hooks should be grouped together)

### Task 3: Add new agent directories to _add_directories method
- Add `("agents/security_logs", "Security hook execution logs")` to the directories list in `_add_directories` method (around line 119-125)
- Add `("agents/scout_files", "Scout command state and cache")` to the directories list in `_add_directories` method (around line 119-125)
- Add corresponding `.gitkeep` files using the existing pattern (around line 131-142):
  - `agents/security_logs/.gitkeep` with empty content
  - `agents/scout_files/.gitkeep` with empty content

### Task 4: Verify template files exist
- Use Glob to verify all referenced template files exist in the templates directory
- Ensure paths match the expected structure

### Task 5: Run validation commands
- Execute all validation commands below to ensure zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests must pass
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting must pass with no errors
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - CLI smoke test must succeed

## Notes
- Follow the existing patterns in `scaffold_service.py` for adding commands, hooks, and directories
- The `.gitkeep` files should use `content=""` and `FileAction.CREATE`, not templates (despite the .j2 extension on the template files themselves)
- The `dangerous_command_blocker.py` hook should be marked as `executable=True` like other hook files
- Templates use the `config` context variable for rendering - no new config variables are needed for these templates
- Scout and question commands are utility commands that support agent exploration and user interaction
- The dangerous command blocker hook provides security validation before command execution
