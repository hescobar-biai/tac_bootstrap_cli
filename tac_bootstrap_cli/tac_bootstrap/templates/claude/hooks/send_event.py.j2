#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from utils.constants import ensure_session_log_dir

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(description='Send observability events to remote server')
        parser.add_argument('--source-app', required=True, help='Source application name')
        parser.add_argument('--event-type', required=True, help='Type of event being sent')
        parser.add_argument('--server-url', help='Override server URL (defaults to OBSERVABILITY_URL env var)')
        parser.add_argument('--add-chat', action='store_true', help='Include conversation data in event (placeholder)')
        parser.add_argument('--summarize', action='store_true', help='Summarize event data (placeholder)')
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.loads(sys.stdin.read())

        # Extract session_id for logging
        session_id = input_data.get('session_id', 'unknown')

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'send_event.json'

        # Log the event locally for debugging
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Create enriched payload
        enriched_payload = {
            'source_app': args.source_app,
            'event_type': args.event_type,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'data': input_data
        }

        # Placeholder logic for future features
        if args.add_chat:
            # Future: integrate with conversation data
            enriched_payload['include_chat'] = True

        if args.summarize:
            # Future: integrate with summarizer.py
            enriched_payload['summarized'] = True

        # Append to local log
        log_data.append(enriched_payload)
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Determine server URL (argument takes precedence over env var)
        server_url = args.server_url or os.environ.get('OBSERVABILITY_URL')

        if not server_url:
            print('Warning: No server URL provided (use --server-url or OBSERVABILITY_URL env var)', file=sys.stderr)
            sys.exit(0)

        # Prepare HTTP request
        headers = {
            'Content-Type': 'application/json'
        }

        # Add authentication if token is available
        auth_token = os.environ.get('OBSERVABILITY_TOKEN')
        if auth_token:
            headers['Authorization'] = f'Bearer {auth_token}'

        # Convert payload to JSON bytes
        payload_bytes = json.dumps(enriched_payload).encode('utf-8')

        # Create request
        req = urllib.request.Request(
            server_url,
            data=payload_bytes,
            headers=headers,
            method='POST'
        )

        # Send HTTP POST with 30s timeout
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = response.read()
                # Successfully sent
                pass
        except urllib.error.HTTPError as e:
            # Log HTTP errors but don't fail
            print(f'HTTP error sending event: {e.code} {e.reason}', file=sys.stderr)
        except urllib.error.URLError as e:
            # Log network errors but don't fail
            print(f'Network error sending event: {e.reason}', file=sys.stderr)
        except Exception as e:
            # Log any other errors but don't fail
            print(f'Error sending event: {e}', file=sys.stderr)

        # Always exit successfully (non-blocking)
        sys.exit(0)

    except json.JSONDecodeError as e:
        # Handle JSON decode errors gracefully
        print(f'JSON decode error: {e}', file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Handle any other errors gracefully
        print(f'Unexpected error: {e}', file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
