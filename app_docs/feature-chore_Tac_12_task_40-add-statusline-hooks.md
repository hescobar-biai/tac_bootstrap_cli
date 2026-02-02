---
doc_type: feature
adw_id: chore_Tac_12_task_40
date: 2026-02-01
idk:
  - statusLine configuration
  - hook chaining
  - send_event.py observability
  - Claude Code hooks
  - event observability sink
tags:
  - feature
  - configuration
  - hooks
  - observability
related_code:
  - .claude/settings.json
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2
---

# Add StatusLine and Hook Observability to Settings Configuration

**ADW ID:** chore_Tac_12_task_40
**Date:** 2026-02-01
**Specification:** `specs/issue-492-adw-chore_Tac_12_task_40-add-statusline-hooks.md`

## Overview

This feature adds comprehensive observability and status display capabilities to the TAC Bootstrap CLI by introducing statusLine configuration and enhancing all seven hook types with send_event.py chaining. The changes enable real-time status monitoring and event tracking throughout the Claude Code development workflow.

## What Was Built

- **StatusLine Configuration**: Root-level configuration for dynamic status display via `status_line_main.py`
- **Hook Observability Enhancement**: send_event.py chaining on all 7 hook types for event observability:
  - PreToolUse hooks with event logging
  - PostToolUse hooks with context bundle tracking
  - Notification hooks with event notification
  - Stop hooks with chat context (`--add-chat` flag)
  - SubagentStop hooks with subagent stop tracking
  - PreCompact hooks with compaction events
  - UserPromptSubmit hooks with event summarization (`--summarize` flag)

## Technical Implementation

### Files Modified

- `./.claude/settings.json`: Main hooks configuration file
  - Added statusLine as root-level configuration (sibling to permissions and hooks)
  - Enhanced all 7 hook types with send_event.py command chaining
  - Maintained backward compatibility with existing hooks

- `./tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`: Jinja2 template for generated projects
  - Mirrors base file structure with templating variables
  - Uses `{{ config.project.package_manager.value }}` for package manager templating (uv, pip, npm)
  - Matches base file configuration exactly (except for template variables)

### Key Changes

- **StatusLine Structure**: Added root-level configuration block:
  ```json
  "statusLine": {
    "type": "command",
    "command": "uv run $CLAUDE_PROJECT_DIR/.claude/status_lines/status_line_main.py",
    "padding": 0
  }
  ```

- **Hook Chaining Pattern**: All hooks now chain send_event.py using `&&` operator:
  - Primary hook → send_event.py for observability
  - Uses `|| true` at end to prevent execution failures from halting workflows

- **Special Flags**:
  - Stop hook: `send_event.py --add-chat` for richer event data with chat context
  - UserPromptSubmit: `send_event.py --summarize` for event summarization

## How to Use

### Adding StatusLine to a Generated Project

The statusLine configuration is automatically included in generated projects via the template file. Generated projects will have dynamic status display capability once the `status_line_main.py` hook script is in place.

### Understanding Hook Observability

All seven hook types now emit observability events through send_event.py:

1. **PreToolUse** - Logs before any tool execution
2. **PostToolUse** - Tracks after tool completion
3. **Notification** - Sends notifications with event data
4. **Stop** - Captures session stop events with chat context
5. **SubagentStop** - Tracks subagent completion
6. **PreCompact** - Handles pre-compaction events
7. **UserPromptSubmit** - Submits user prompt events with summary

Each hook follows this pattern:
```bash
primary_hook && send_event.py [optional_flags] || true
```

### Testing Hook Configuration

Verify the configuration is valid:

```bash
# Check JSON syntax
python3 -m json.tool ./.claude/settings.json > /dev/null && echo "✓ settings.json is valid"

# Count send_event.py occurrences
grep -c "send_event.py" ./.claude/settings.json
```

### Verifying Template Generation

Test that the Jinja2 template renders correctly:

```bash
cd tac_bootstrap_cli && python3 -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap/templates/claude')); t = env.get_template('settings.json.j2'); print('✓ Template loads successfully')"
```

## Configuration

### StatusLine Configuration Options

The statusLine configuration at root level accepts:

- **type**: `"command"` - Specifies this is a command-based status display
- **command**: Path to status line script with environment variable substitution
- **padding**: Number of lines to pad (typically 0)

### Hook Event Flags

- **--add-chat** (Stop hook only): Includes chat context in event data
- **--summarize** (UserPromptSubmit only): Summarizes event for transmission

### Template Variables

In generated projects, the template substitutes:

```jinja2
{{ config.project.package_manager.value }}  # Resolves to: uv, pip, npm, etc.
```

## Testing

Verify the implementation with these commands:

```bash
# Validate JSON structure
python3 -m json.tool ./.claude/settings.json > /dev/null && echo "✓ Valid JSON"
```

Run tests for the TAC Bootstrap CLI:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to ensure no syntax errors:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

- **Hook Chaining**: All hooks use `&&` to chain commands sequentially and `|| true` at the end to ensure execution continues even if a hook fails
- **StatusLine Placement**: Must be at root level of settings.json, NOT inside the hooks object
- **Base vs Template**: Base file uses hardcoded `uv` (tac_bootstrap's package manager); templates use `{{ config.project.package_manager.value }}`
- **Session Hooks**: SessionStart and SessionEnd hooks are not modified by this change
- **Observability Pattern**: send_event.py acts as an observability sink, capturing events from all major hook execution points for monitoring and debugging

## Related Documentation

- [ai_docs/doc/plan_tasks_Tac_12.md](ai_docs/doc/plan_tasks_Tac_12.md) - Contains statusLine and send_event.py specifications
- [.claude/hooks/](`.claude/hooks/`) - Hook implementation directory
- [tac_bootstrap_cli/tac_bootstrap/templates/](tac_bootstrap_cli/tac_bootstrap/templates/) - Template directory structure
