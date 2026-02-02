# Chore: Add statusLine and ALL hooks to .claude/settings.json

## Metadata
issue_number: `492`
adw_id: `chore_Tac_12_task_40`
issue_json: `{"number": 492, "title": "[Task 40/49] [CHORE] Add statusLine and ALL hooks to .claude/settings.json", "body": "## Description\n\nAdd statusLine configuration and ALL 7 hook types to settings.json.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/settings.json`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`\n\n## Key Changes\n- Add statusLine configuration\n- Add PreToolUse hooks (pre_tool_use.py + send_event.py)\n- Add PostToolUse hooks (post_tool_use.py + send_event.py)\n- Add Notification hooks (notification.py + send_event.py)\n- Add Stop hooks (stop.py + send_event.py with --add-chat)\n- Add SubagentStop hooks (subagent_stop.py + send_event.py)\n- Add PreCompact hooks (send_event.py only)\n- Add UserPromptSubmit hooks (user_prompt_submit.py with flags + send_event.py)\n\n## Changes Required\n- Update base file with all hook configurations\n- Update template file\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/settings.json`"}`

## Chore Description

This chore adds statusLine configuration and enhances 7 existing hook types with send_event.py chaining for observability in the TAC Bootstrap CLI.

**Key Updates:**
1. Add statusLine top-level configuration (command type, pointing to status_line_main.py)
2. Enhance PreToolUse hooks with send_event.py chaining
3. Enhance PostToolUse hooks with send_event.py chaining
4. Enhance Notification hooks with send_event.py chaining
5. Enhance Stop hooks with send_event.py chaining (using --add-chat flag)
6. Enhance SubagentStop hooks with send_event.py chaining
7. Enhance PreCompact hooks with send_event.py chaining
8. Enhance UserPromptSubmit hooks with send_event.py chaining (using --summarize flag)

## Relevant Files

### Base Files (tac_bootstrap project)
- `./.claude/settings.json` - Main hooks configuration file that needs statusLine + enhanced hooks
  - Currently has 8 hook types (PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit, SessionStart, SessionEnd)
  - Missing statusLine configuration
  - Hooks need send_event.py chaining for observability

### Template Files (for generated projects)
- `./tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Jinja2 template
  - Must mirror base file changes
  - Uses `{{ config.project.package_manager.value }}` for templating

### Reference
- `ai_docs/doc/plan_tasks_Tac_12.md` - Contains statusLine and send_event.py specifications

## Step by Step Tasks

### Task 1: Add statusLine configuration to base settings.json
- Open `./.claude/settings.json`
- Add statusLine as a root-level key (after "permissions" and before "hooks")
- Structure:
  ```json
  "statusLine": {
    "type": "command",
    "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py",
    "padding": 0
  }
  ```
- Note: Do NOT place inside hooks object - it's a sibling to permissions and hooks

### Task 2: Enhance PreToolUse hooks with send_event.py
- In the universal hook logger command (matcher: ""), append send_event.py:
  - From: `"uv run ... universal_hook_logger.py --event PreToolUse && uv run ... pre_tool_use.py || true"`
  - To: `"uv run ... universal_hook_logger.py --event PreToolUse && uv run ... pre_tool_use.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py || true"`

### Task 3: Enhance PostToolUse hooks with send_event.py
- In the context_bundle_builder command, append send_event.py:
  - From: `"uv run ... context_bundle_builder.py ... && uv run ... post_tool_use.py || true"`
  - To: `"uv run ... context_bundle_builder.py ... && uv run ... post_tool_use.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py || true"`

### Task 4: Enhance Notification hooks with send_event.py
- Append send_event.py to command:
  - From: `"uv run ... universal_hook_logger.py --event Notification && uv run ... notification.py --notify || true"`
  - To: `"uv run ... universal_hook_logger.py --event Notification && uv run ... notification.py --notify && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py || true"`

### Task 5: Enhance Stop hooks with send_event.py and --add-chat flag
- Append send_event.py with --add-chat flag:
  - From: `"uv run ... universal_hook_logger.py --event Stop && uv run ... stop.py --chat || true"`
  - To: `"uv run ... universal_hook_logger.py --event Stop && uv run ... stop.py --chat && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py --add-chat || true"`

### Task 6: Enhance SubagentStop hooks with send_event.py
- Append send_event.py to command:
  - From: `"uv run ... universal_hook_logger.py --event SubagentStop && uv run ... subagent_stop.py || true"`
  - To: `"uv run ... universal_hook_logger.py --event SubagentStop && uv run ... subagent_stop.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py || true"`

### Task 7: Enhance PreCompact hooks with send_event.py
- Append send_event.py to command:
  - From: `"uv run ... universal_hook_logger.py --event PreCompact && uv run ... pre_compact.py || true"`
  - To: `"uv run ... universal_hook_logger.py --event PreCompact && uv run ... pre_compact.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py || true"`

### Task 8: Enhance UserPromptSubmit hooks with send_event.py and --summarize flag
- Modify the context_bundle_builder command to append send_event.py with --summarize:
  - From: `"uv run ... context_bundle_builder.py --type user_prompt || true"`
  - To: `"uv run ... context_bundle_builder.py --type user_prompt && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/send_event.py --summarize || true"`

### Task 9: Update template file with same changes
- Open `./tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`
- Add statusLine configuration (same structure, but keep at same location as base file)
- Enhance all 7 hook types with send_event.py chaining (use `{{ config.project.package_manager.value }}` for package manager templating)
- Ensure template matches base file structure exactly (except for templating variables)

### Task 10: Validation
- Verify `./.claude/settings.json` is valid JSON
- Verify `./tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` is valid JSON with Jinja2 syntax
- Run: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run: `cd tac_bootstrap_cli && uv run ruff check .`
- Run linting on updated files to ensure no syntax errors

## Validation Commands

Ensure all changes are complete and valid:

```bash
# Check JSON syntax
python3 -m json.tool ./.claude/settings.json > /dev/null && echo "✓ Base settings.json is valid JSON"

# Verify all required hooks are enhanced
grep -c "send_event.py" ./.claude/settings.json && echo "✓ send_event.py chaining found"

# Run tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test template generation
cd tac_bootstrap_cli && uv run python3 -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap/templates/claude')); t = env.get_template('settings.json.j2'); print('✓ Template loads successfully')"
```

## Notes

- **Hook Chaining Pattern:** All hooks use `&&` to chain commands and `|| true` at the end to prevent failures from stopping execution
- **statusLine Configuration:** Must be at root level, NOT inside hooks object
- **Template Variables:** Use `{{ config.project.package_manager.value }}` in template file for package manager (e.g., uv, pip, npm)
- **Base File:** Use hardcoded `uv` since tac_bootstrap itself uses uv
- **SessionStart/SessionEnd:** Do NOT modify these hooks (not part of this task)
- **Flag Mappings:**
  - Stop hook: Pass `--add-chat` to send_event.py for richer event data
  - UserPromptSubmit: Pass `--summarize` to send_event.py for event summarization
  - Other hooks: No special flags, just add send_event.py

## Auto-Resolved Clarifications Summary

From issue clarifications:
- statusLine is a command-type configuration for dynamic status display
- send_event.py is an observability sink that chains after primary hook logic
- All 7 hooks already exist (not creating new ones)
- Stop hook uses `--add-chat` flag with send_event.py
- UserPromptSubmit uses `--summarize` flag with send_event.py
- SessionStart/SessionEnd are unchanged
- Template uses package_manager variable; base uses 'uv'
