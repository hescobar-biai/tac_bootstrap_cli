#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

"""
Pre-Tool Use Hook - Observability Logging
Captures tool invocation metadata before each tool execution.
Provides lightweight telemetry without blocking execution.

This hook runs before every tool call and logs:
- Tool name
- Timestamp (ISO 8601 format)
- Current working directory
- Session ID

Exit code: Always 0 (non-blocking)
"""

import json
import os
import sys
from datetime import datetime, timezone


def main():
    try:
        # Read JSON input from stdin (provided by Claude Code)
        input_data = json.load(sys.stdin)

        # Extract tool metadata
        tool_name = input_data.get('tool_name', 'unknown')
        session_id = input_data.get('session_id', 'unknown')

        # Capture timestamp in ISO 8601 format
        timestamp = datetime.now(timezone.utc).isoformat()

        # Capture current working directory
        cwd = os.getcwd()

        # Output structured text to stdout (human-readable format)
        print(f"[{timestamp}] tool={tool_name} cwd={cwd} session={session_id}")

        # Always exit successfully (non-blocking)
        sys.exit(0)

    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors - don't block execution
        sys.exit(0)
    except Exception as e:
        # Handle any errors gracefully - log to stderr but don't block
        print(f"pre_tool_use hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
