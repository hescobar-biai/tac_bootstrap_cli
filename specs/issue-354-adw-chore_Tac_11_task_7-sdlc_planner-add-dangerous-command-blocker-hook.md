# Chore: Add dangerous_command_blocker hook to PreToolUse for Bash commands

## Metadata
issue_number: `354`
adw_id: `chore_Tac_11_task_7`
issue_json: `{"number":354,"title":"Update settings.json to include dangerous_command_blocker hook in base repository","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_7\n\nAdd the dangerous_command_blocker hook to PreToolUse for Bash commands with a specific matcher.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`\n\n**Implementation details:**\n- Add new PreToolUse entry with matcher \"Bash\"\n- Hook command: `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py`\n- Set timeout: 5 seconds\n- Place before the universal logger hook\n- Ensure the hook blocks dangerous commands before they reach other hooks"}`

## Chore Description
Update `.claude/settings.json` to add a dedicated PreToolUse hook entry specifically for Bash commands that runs the `dangerous_command_blocker.py` hook before other hooks. Currently, the dangerous_command_blocker is chained with other hooks in the universal PreToolUse entry (line 30), but it should have its own dedicated entry with a "Bash" matcher to ensure it runs first and blocks dangerous commands before they reach the logging hooks.

The dangerous_command_blocker.py hook is already implemented and blocks dangerous commands like `rm -rf /`, `dd` to devices, `mkfs`, `chmod -R 777`, and other destructive operations. It needs to be separated from the universal hook chain to ensure proper execution order.

## Relevant Files
Files needed to complete this chore:

- `.claude/settings.json` - Main configuration file that needs to be updated. Currently has dangerous_command_blocker chained with other hooks in the universal PreToolUse entry. Need to add a new dedicated PreToolUse entry with "Bash" matcher.
- `.claude/hooks/dangerous_command_blocker.py` - The hook script that will be called (already exists and is working, no changes needed).

### New Files
No new files required. This is a configuration update only.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create new PreToolUse entry for Bash commands
- Add a new PreToolUse array entry before the universal matcher entry
- Set matcher to "Bash" to target only Bash tool calls
- Configure hook command: `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py`
- Set timeout to 5000 (5 seconds)
- This entry should be the FIRST PreToolUse entry (index 0) to ensure it runs before other hooks

### Task 2: Remove dangerous_command_blocker from universal PreToolUse hook chain
- Edit the universal PreToolUse entry (currently at line 30)
- Remove `&& uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py` from the chained command
- Keep `|| true` at the end of the remaining command chain
- This ensures dangerous_command_blocker runs only for Bash commands through its dedicated entry

### Task 3: Validate JSON structure
- Ensure the JSON file is properly formatted
- Verify all brackets, braces, and commas are correct
- Test that the file can be parsed as valid JSON
- Verify the PreToolUse array has the new Bash entry first, followed by the universal entry

### Task 4: Run validation commands
- Execute all validation commands below to ensure zero regressions
- Fix any issues that arise

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `python3 -m json.tool .claude/settings.json > /dev/null` - Validate JSON syntax

## Notes
The dangerous_command_blocker.py hook exits with code 2 when it blocks a command, which prevents subsequent hooks from executing. By placing it in a dedicated PreToolUse entry with "Bash" matcher before the universal logger hook, we ensure:

1. It runs first for all Bash commands
2. Dangerous commands are blocked before reaching other hooks
3. The universal logger still logs the blocked attempt
4. Other non-Bash tools are not affected by this hook

The hook already exists and is functional - this chore is purely about restructuring the settings.json configuration for better hook execution order and separation of concerns.
