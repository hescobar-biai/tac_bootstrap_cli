#!/usr/bin/env python3
"""
Stop hook for tac-bootstrap.

This hook runs when a Claude Code session ends.
It generates a session summary including tool usage statistics.

Summary is written to: logs/{session_id}/summary.json
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def count_tool_uses(session_log_dir):
    """
    Count tool uses from the post_tool_use.json log.

    Args:
        session_log_dir: Path to session log directory

    Returns:
        Number of tool uses, or 0 if file doesn't exist
    """
    try:
        post_tool_log = session_log_dir / 'post_tool_use.json'
        if post_tool_log.exists():
            with open(post_tool_log, 'r') as f:
                log_data = json.load(f)
                return len(log_data) if isinstance(log_data, list) else 0
        return 0
    except Exception:
        return 0


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--chat', action='store_true', help='Copy transcript to chat.json')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract required fields
        session_id = input_data.get("session_id", "unknown")
        stop_hook_active = input_data.get("stop_hook_active", False)

        # Ensure log directory exists
        log_base_dir = Path("logs")
        log_dir = log_base_dir / session_id
        log_dir.mkdir(parents=True, exist_ok=True)

        # Log stop event
        stop_log_path = log_dir / "stop.json"

        # Read existing log data or initialize empty list
        if stop_log_path.exists():
            with open(stop_log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(stop_log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Generate session summary
        tool_uses = count_tool_uses(log_dir)
        summary = {
            'session_id': session_id,
            'ended_at': datetime.now().isoformat(),
            'tool_uses': tool_uses,
            'stop_hook_active': stop_hook_active,
        }

        summary_path = log_dir / 'summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        # Handle --chat switch to copy transcript
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            try:
                # Read .jsonl file and convert to JSON array
                chat_data = []
                with open(transcript_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass  # Skip invalid lines

                # Write to session-specific chat.json
                chat_file = log_dir / 'chat.json'
                with open(chat_file, 'w') as f:
                    json.dump(chat_data, f, indent=2)
            except Exception:
                pass  # Fail silently

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == "__main__":
    main()
