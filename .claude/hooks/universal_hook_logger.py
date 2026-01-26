#!/usr/bin/env python3
"""
Universal hook logger for tac-bootstrap.

This hook provides comprehensive logging across ALL Claude Code hook events.
It accepts generic JSON input from any hook type and logs to a unified file.

WARNING: This logger captures ALL hook events and may contain sensitive data
including API keys, file paths, and user prompts. Review logs carefully before
sharing. Consider using .gitignore to exclude log directories.

Logs are written to: logs/{session_id}/universal_hook.json

MANUAL ACTIVATION REQUIRED:
This hook is NOT enabled by default. To activate it, add entries to your
.claude/settings.json for the hook types you want to monitor:

Example for all 7 hook types:
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/universal_hook_logger.py || true"
      }]
    }],
    "PostToolUse": [{ ... }],
    "UserPromptSubmit": [{ ... }],
    "Notification": [{ ... }],
    "Stop": [{ ... }],
    "SubagentStop": [{ ... }],
    "PreCompact": [{ ... }]
  }
}

LOG ROTATION:
This logger does NOT implement automatic log rotation. Large logs can consume
significant disk space. Users should implement their own log rotation strategy
using logrotate, cron jobs, or similar tools.

PERFORMANCE IMPACT:
Logging all events may impact performance, especially in high-frequency workflows.
Enable only the hook types you need for debugging or auditing.
"""

import json
import sys
from pathlib import Path


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract session_id and event_type
        session_id = input_data.get('session_id', 'unknown')

        # Infer event_type from input data structure or use explicit field
        # Different hooks provide different fields, try to infer intelligently
        event_type = input_data.get('event_type', 'unknown')
        if event_type == 'unknown':
            if 'tool_name' in input_data and 'tool_output' in input_data:
                event_type = 'PostToolUse'
            elif 'tool_name' in input_data and 'tool_input' in input_data:
                event_type = 'PreToolUse'
            elif 'prompt' in input_data:
                event_type = 'UserPromptSubmit'
            elif 'notification' in input_data:
                event_type = 'Notification'
            elif 'reason' in input_data:
                event_type = 'Stop'
            elif 'subagent_id' in input_data:
                event_type = 'SubagentStop'
            elif 'compact' in input_data:
                event_type = 'PreCompact'

        # Ensure log directory exists
        log_base_dir = Path("logs")
        log_dir = log_base_dir / session_id
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'universal_hook.json'

        # Create a copy of input_data without tool_output to prevent excessive log sizes
        # tool_output can be very large (multi-MB) and would bloat logs
        log_input_data = input_data.copy()
        if 'tool_output' in log_input_data:
            # Remove tool_output entirely - users can enable PostToolUse hook if they need output
            del log_input_data['tool_output']

        # Prepare log entry
        log_entry = {
            'timestamp': input_data.get('timestamp', ''),
            'event_type': event_type,
            'session_id': session_id,
            'input_data': log_input_data,
        }

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    # Corrupted log file - reinitialize as empty list
                    log_data = []
        else:
            log_data = []

        # Append new entry
        log_data.append(log_entry)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully - invalid input from stdin
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error (logging is best-effort)
        # Never disrupt the workflow due to logging failures
        sys.exit(0)


if __name__ == '__main__':
    main()
