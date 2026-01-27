---
doc_type: feature
adw_id: chore_Tac_11_task_7
date: 2026-01-27
idk:
  - hooks
  - PreToolUse
  - dangerous-command-blocker
  - configuration
  - security
  - settings.json
tags:
  - feature
  - security
  - configuration
related_code:
  - .claude/settings.json
  - .claude/hooks/dangerous_command_blocker.py
---

# Dangerous Command Blocker Hook Configuration

**ADW ID:** chore_Tac_11_task_7
**Date:** 2026-01-27
**Specification:** specs/issue-354-adw-chore_Tac_11_task_7-sdlc_planner-add-dangerous-command-blocker-hook.md

## Overview

Updated `.claude/settings.json` to add a dedicated PreToolUse hook entry for Bash commands that runs the dangerous command blocker before other hooks, ensuring destructive commands are blocked before reaching logging hooks.

## What Was Built

- Dedicated PreToolUse hook entry with "Bash" matcher for dangerous command blocking
- Separated dangerous_command_blocker from universal hook chain
- Proper hook execution order ensuring security checks run first

## Technical Implementation

### Files Modified

- `.claude/settings.json`: Added dedicated PreToolUse entry for Bash commands with dangerous_command_blocker hook, removed dangerous_command_blocker from universal hook chain

### Key Changes

- Created new PreToolUse array entry at index 0 with "Bash" matcher targeting only Bash tool calls
- Configured hook command: `uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py` with 5-second timeout
- Removed `&& uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py` from universal PreToolUse hook chain
- Ensured dangerous_command_blocker runs first for all Bash commands before other hooks
- Maintained universal logger hook functionality for non-Bash tools

## How to Use

The dangerous command blocker is now automatically active for all Bash commands. No user action required - it runs transparently before any Bash command execution.

1. The hook automatically blocks dangerous commands like `rm -rf /`, `dd` to devices, `mkfs`, `chmod -R 777`
2. When a dangerous command is detected, the hook exits with code 2 and prevents execution
3. The blocked attempt is still logged by the universal logger hook
4. Safe commands proceed normally through the hook chain

## Configuration

The hook is configured in `.claude/settings.json` under `hooks.PreToolUse`:

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py",
      "timeout": 5000
    }
  ]
}
```

Key configuration parameters:
- `matcher: "Bash"`: Targets only Bash tool calls
- `timeout: 5000`: 5-second timeout for hook execution
- Placement at index 0 ensures it runs before other hooks

## Testing

Validate JSON syntax:

```bash
python3 -m json.tool .claude/settings.json > /dev/null
```

Run unit tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

The dangerous_command_blocker.py hook exits with code 2 when it blocks a command, which prevents subsequent hooks from executing. By placing it in a dedicated PreToolUse entry with "Bash" matcher before the universal logger hook, we ensure:

1. It runs first for all Bash commands
2. Dangerous commands are blocked before reaching other hooks
3. The universal logger still logs the blocked attempt
4. Other non-Bash tools are not affected by this hook

This is a configuration-only change - the dangerous_command_blocker.py hook script already existed and is functional. The chore restructured settings.json for better hook execution order and separation of concerns.
