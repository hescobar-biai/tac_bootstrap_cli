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

## Security Hooks

Security hooks protect against destructive operations that could cause data loss or system damage. They run in the `PreToolUse` phase to validate and block dangerous commands before execution.

### Dangerous Command Blocker

Intercepts and blocks dangerous bash commands that could cause data loss, system damage, or security vulnerabilities.

**Location:** `.claude/hooks/dangerous_command_blocker.py`

**Features:**
- Validates bash commands before execution
- Blocks destructive operations (rm -rf /, dd to devices, mkfs, etc.)
- Prevents security vulnerabilities (chmod -R 777, etc.)
- Provides safer alternatives for blocked commands
- Logs all blocked operations to security audit trail
- Uses exit code 2 for blocking (see [Exit Code Strategy](#exit-code-strategy))

**Blocked Operations:**

The hook protects against the following dangerous command patterns:

| Category | Examples | Risk |
|----------|----------|------|
| **Recursive rm** | `rm -rf /`, `rm -rf /etc`, `rm -rf $VAR` | Data loss, system destruction |
| **Device writes** | `dd of=/dev/sda`, `dd of=/dev/nvme0n1` | Disk wipe, data loss |
| **Filesystem creation** | `mkfs.ext4 /dev/sda`, `mkfs.xfs /dev/nvme0n1` | Data destruction |
| **Insecure permissions** | `chmod -R 777 /`, `chmod -R 777 /var` | Security vulnerabilities |
| **Ownership changes** | `chown -R user:group /`, `chown -R user /etc` | System access issues |
| **Data destruction** | `shred /dev/sda`, `wipefs /dev/nvme0n1`, `format C:` | Permanent data loss |

**Critical Paths Protected:**

The hook provides extra protection for these system paths: `/`, `/etc`, `/usr`, `/bin`, `/sbin`, `/lib`, `/lib64`, `/boot`, `/home`, `/root`, `/var`, `/sys`, `/proc`, `/dev`

**Safer Alternatives:**

When a command is blocked, the hook suggests safer alternatives:

```bash
# Instead of: rm -rf /
# Use: rm -rf ./specific_folder

# Instead of: chmod -R 777 /var
# Use: chmod -R 755 ./project_directory

# Instead of: dd of=/dev/sda
# Use: dd if=source.img of=/path/to/file.img

# Instead of: chown -R user:group /
# Use: chown -R user:group ./project_dir
```

**Configuration:**

Add to `.claude/settings.json` in the `PreToolUse` hook chain:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py || true"
          }
        ]
      }
    ]
  }
}
```

For multiple PreToolUse hooks, chain them together:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py --event PreToolUse && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/dangerous_command_blocker.py && uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ]
  }
}
```

**Security Logs:**

All blocked commands are logged to a security audit trail for review:

- **Location:** `agents/security_logs/blocked_commands.jsonl`
- **Format:** JSON Lines (JSONL) - one JSON object per line for easy parsing
- **Contents:** Each entry includes:
  - `timestamp` - ISO 8601 timestamp with timezone
  - `command` - The full blocked command
  - `reason` - Why it was blocked
  - `suggested_alternative` - Safer alternative to use
  - `blocked` - Always `true`

Example log entry:
```json
{
  "timestamp": "2026-01-27T10:30:45.123456+00:00",
  "command": "rm -rf /etc",
  "reason": "Command matches dangerous pattern and targets critical path '/etc'",
  "suggested_alternative": "Use specific paths in /tmp or project directories: rm -rf /tmp/myapp_temp",
  "blocked": true
}
```

**Customization:**

To temporarily disable the hook:
- Remove `dangerous_command_blocker.py` from the PreToolUse hook chain in `.claude/settings.json`

To customize blocked patterns:
- Edit `DANGEROUS_PATTERNS` list in `.claude/hooks/dangerous_command_blocker.py`
- Add or remove critical paths in `CRITICAL_PATHS` list
- Modify safer alternatives in `SAFER_ALTERNATIVES` dictionary

**Warning:** Only modify the hook if you fully understand the security implications. The default patterns protect against common destructive operations.

**See Also:**
- [Pre-Tool Use Hook](#pre-tool-use-hook) - General pre-execution validation
- [Exit Code Strategy](#exit-code-strategy) - Understanding hook exit codes
- [Hook Configuration](#hook-configuration) - How to configure hooks in settings.json

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
│       ├── dangerous_command_blocker.py
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
    ├── context_bundles/    # Context bundle storage
    └── security_logs/      # Security audit trail
```

## Expert Hook Development

For complex hook development, use the expert pattern:

```
/experts:cc_hook_expert:cc_hook_expert_plan "Create a hook for X"
/experts:cc_hook_expert:cc_hook_expert_build
/experts:cc_hook_expert:cc_hook_expert_improve
```

See [Agents Documentation](agents.md#expert-pattern) for details.
