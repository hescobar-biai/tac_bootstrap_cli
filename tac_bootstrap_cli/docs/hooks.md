# Hook System

TAC Bootstrap includes a comprehensive hook system for automating actions during Claude Code sessions.

## Overview

Hooks are scripts that execute automatically in response to Claude Code events. They enable:
- Session tracking and logging
- Context preservation
- Security validation
- Custom automations

## Hook Types

| Hook | Trigger | Use Case |
|------|---------|----------|
| `PreToolUse` | Before any tool executes | Validation, blocking dangerous commands |
| `PostToolUse` | After tool execution | Logging, context tracking |
| `UserPromptSubmit` | When user submits prompt | Prompt logging, preprocessing |
| `Stop` | When session ends | Cleanup, final reporting |
| `SubagentStop` | When subagent completes | Result aggregation |
| `Notification` | On system notifications | External integrations |
| `PreCompact` | Before context compaction | Save important context |
| `SessionStart` | When session begins | Initialization |
| `SessionEnd` | When session ends | Cleanup |

## Core Hooks

### Universal Hook Logger

Comprehensive logging across all hook events.

**Location:** `.claude/hooks/universal_hook_logger.py`

**Features:**
- Logs all hook events with timestamps
- Session-aware logging
- Structured JSON output
- Configurable verbosity

**Usage in settings.json:**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse || true"
      }]
    }]
  }
}
```

**Log location:** `agents/hook_logs/`

### Context Bundle Builder

Tracks Read/Write operations for context recovery.

**Location:** `.claude/hooks/context_bundle_builder.py`

**Features:**
- Tracks file operations during sessions
- Saves context to JSONL bundles
- Enables session recovery via `/load_bundle`
- Supports multiple event types

**Usage:**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type post_tool_use --matcher \"Read|Write\" || true"
      }]
    }],
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type user_prompt || true"
      }]
    }]
  }
}
```

**Bundle location:** `agents/context_bundles/`

### Pre-Tool Use Hook

Validates and controls tool execution.

**Location:** `.claude/hooks/pre_tool_use.py`

**Features:**
- Block dangerous commands (rm -rf, etc.)
- Validate file access patterns
- Security checks
- Custom validation rules

**Exit codes:**
- `0` - Allow operation
- `1` - Warning (show but allow)
- `2` - Block operation

### Post-Tool Use Hook

Processes tool results after execution.

**Location:** `.claude/hooks/post_tool_use.py`

**Features:**
- Log tool usage statistics
- Track file modifications
- Trigger follow-up actions

### Stop Hook

Executes when session ends.

**Location:** `.claude/hooks/stop.py`

**Features:**
- Generate session summary
- Save session state
- Cleanup temporary files
- Send notifications

### Notification Hook

Handles system notifications.

**Location:** `.claude/hooks/notification.py`

**Features:**
- Desktop notifications
- External service integration
- Alert routing

## Hook Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type post_tool_use --matcher \"Read|Write\" && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event Stop && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/stop.py --chat || true"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_builder.py --type user_prompt || true"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SubagentStop && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/subagent_stop.py || true"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event Notification && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/notification.py --notify || true"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreCompact && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_compact.py || true"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SessionStart || true"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event SessionEnd || true"
          }
        ]
      }
    ]
  }
}
```

## Matcher Patterns

The `matcher` field accepts regex patterns to filter which tools trigger the hook:

```json
{
  "matcher": "",           // All tools
  "matcher": "Bash",       // Only Bash tool
  "matcher": "Read|Write", // Read or Write tools
  "matcher": "Edit.*"      // Edit and related tools
}
```

## Hook Input

Hooks receive JSON on stdin:

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "ls -la",
    "description": "List files"
  },
  "session_id": "abc-123-def",
  "timestamp": "2026-01-27T10:30:00Z"
}
```

## Creating Custom Hooks

### Basic Structure

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        session_id = input_data.get('session_id', 'unknown')

        # Your logic here
        if should_block(tool_input):
            print("BLOCKED: Reason", file=sys.stderr)
            sys.exit(2)

        if should_warn(tool_input):
            print("WARNING: Reason", file=sys.stderr)
            sys.exit(1)

        sys.exit(0)  # Allow

    except json.JSONDecodeError:
        sys.exit(0)  # Graceful failure
    except Exception:
        sys.exit(0)  # Graceful failure

if __name__ == '__main__':
    main()
```

### Exit Code Strategy

| Code | Meaning | Behavior |
|------|---------|----------|
| `0` | Allow | Operation proceeds normally |
| `1` | Warning | Shows warning, operation proceeds |
| `2` | Block | Operation is blocked, error shown |

### Best Practices

1. **Always use `|| true`** in settings.json to prevent hook failures from blocking the agent
2. **Handle errors gracefully** with exit code 0 for unexpected errors
3. **Use session-aware logging** for debugging
4. **Keep hooks fast** - they run on every tool invocation
5. **Test hooks manually** before deploying:
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | .claude/hooks/your_hook.py
   echo $?  # Check exit code
   ```

## Hook Directories

```
project/
├── .claude/
│   └── hooks/
│       ├── pre_tool_use.py
│       ├── post_tool_use.py
│       ├── stop.py
│       ├── notification.py
│       ├── subagent_stop.py
│       ├── pre_compact.py
│       ├── user_prompt_submit.py
│       ├── context_bundle_builder.py
│       ├── universal_hook_logger.py
│       └── utils/
│           ├── constants.py
│           ├── llm/        # LLM utilities
│           └── tts/        # TTS utilities
└── agents/
    ├── hook_logs/          # Universal logger output
    └── context_bundles/    # Context bundle storage
```

## Expert Hook Development

For complex hook development, use the expert pattern:

```
/experts:cc_hook_expert:cc_hook_expert_plan "Create a hook for X"
/experts:cc_hook_expert:cc_hook_expert_build
/experts:cc_hook_expert:cc_hook_expert_improve
```

See [Agents Documentation](agents.md#expert-pattern) for details.
