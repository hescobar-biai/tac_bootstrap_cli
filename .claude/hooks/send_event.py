#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

"""
Multi-Agent Observability Hook Script
Sends Claude Code hook events to the observability server.
"""

import json
import sys
import os
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from utils.summarizer import generate_event_summary
from utils.model_extractor import get_model_from_transcript
from utils.constants import ensure_session_log_dir

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_event_to_server(event_data, server_url):
    """Send event data to the observability server."""
    try:
        # Add authentication if token is available
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Claude-Code-Hook/1.0",
        }

        auth_token = os.environ.get('OBSERVABILITY_TOKEN')
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'

        # Prepare the request
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event_data).encode("utf-8"),
            headers=headers,
        )

        # Send the request
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                return True
            else:
                print(f"Server returned status: {response.status}", file=sys.stderr)
                return False

    except urllib.error.URLError as e:
        print(f"Failed to send event: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return False


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Send Claude Code hook events to observability server"
    )
    parser.add_argument("--source-app", required=True, help="Source application name")
    parser.add_argument(
        "--event-type",
        required=True,
        help="Hook event type (PreToolUse, PostToolUse, etc.)",
    )
    parser.add_argument(
        "--server-url",
        help="Server URL (defaults to OBSERVABILITY_URL env var or http://localhost:4000/events)"
    )
    parser.add_argument(
        "--add-chat", action="store_true", help="Include chat transcript if available"
    )
    parser.add_argument(
        "--summarize", action="store_true", help="Generate AI summary of the event"
    )

    args = parser.parse_args()

    try:
        # Read hook data from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON input: {e}", file=sys.stderr)
        sys.exit(0)  # Exit gracefully

    # Extract session_id for logging
    session_id = input_data.get('session_id', 'unknown')

    # Extract model name from transcript (with caching)
    model_name = ''
    transcript_path = input_data.get('transcript_path', '')
    if transcript_path:
        model_name = get_model_from_transcript(session_id, transcript_path)

    # Prepare event data for server
    event_data = {
        "source_app": args.source_app,
        "session_id": session_id,
        "hook_event_type": args.event_type,
        "payload": input_data,
        "timestamp": int(datetime.now().timestamp() * 1000),
        "model_name": model_name,
    }

    # Handle --add-chat option
    if args.add_chat and "transcript_path" in input_data:
        transcript_path = input_data["transcript_path"]
        if os.path.exists(transcript_path):
            # Read .jsonl file and convert to JSON array
            chat_data = []
            try:
                with open(transcript_path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass  # Skip invalid lines

                # Add chat to event data
                event_data["chat"] = chat_data
            except Exception as e:
                print(f"Failed to read transcript: {e}", file=sys.stderr)

    # Generate summary if requested
    if args.summarize:
        summary = generate_event_summary(event_data)
        if summary:
            event_data["summary"] = summary
        # Continue even if summary generation fails

    # Local logging for debugging (tac_bootstrap enhancement)
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'send_event.jsonl'

        # Append to JSONL log file
        with open(log_file, 'a') as f:
            f.write(json.dumps(event_data) + '\n')
    except Exception as e:
        print(f"Warning: Failed to write local log: {e}", file=sys.stderr)

    # Determine server URL (argument takes precedence over env var)
    server_url = args.server_url or os.environ.get('OBSERVABILITY_URL') or 'http://localhost:4000/events'

    # Send to server
    success = send_event_to_server(event_data, server_url)

    # Always exit with 0 to not block Claude Code operations
    sys.exit(0)


if __name__ == "__main__":
    main()
