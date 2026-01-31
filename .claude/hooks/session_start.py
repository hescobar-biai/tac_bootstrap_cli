#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///

"""
Session Start Hook
Captures session initialization context and writes to session_context.json
Executes when Claude Code session starts
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    try:
        # Initialize session context dictionary
        session_context = {}

        # Capture git branch with error handling
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5,
                check=True
            )
            session_context['git_branch'] = result.stdout.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            session_context['git_branch'] = 'unknown'

        # Capture model from environment variable
        session_context['model'] = os.environ.get('CLAUDE_MODEL', 'unknown')

        # Capture project name from config.yml
        try:
            import yaml
            config_path = Path('config.yml')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                    session_context['project_name'] = config_data.get('project', {}).get('name', 'unknown')
            else:
                session_context['project_name'] = 'unknown'
        except Exception:
            session_context['project_name'] = 'unknown'

        # Capture timestamp in ISO format
        session_context['timestamp'] = datetime.now(timezone.utc).isoformat()

        # Capture current working directory
        session_context['cwd'] = os.getcwd()

        # Write session context to JSON file
        output_path = Path('.claude/session_context.json')
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(session_context, f, indent=2)

        # Always exit successfully (non-blocking)
        sys.exit(0)

    except Exception as e:
        # Handle any errors gracefully - don't break the session
        print(f'Error in session_start hook: {e}', file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
