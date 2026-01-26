#!/usr/bin/env python3
"""
Context Bundle Builder - Claude Code Hook for tac-bootstrap

Tracks file operations (Read, Write, Edit, NotebookEdit) during Claude Code sessions
and saves them to session-specific JSONL files for context recovery.

This hook enables agents to:
- Recover and understand files accessed during previous sessions
- Debug agent behavior by reviewing operation history
- Maintain an audit trail of file manipulations
- Build context bundles for session continuation

JSONL files are stored at: logs/context_bundles/session_{session_id}.jsonl

JSONL Entry Schema:
{
    "timestamp": "2024-01-26T14:30:45.123456",  # ISO8601 timestamp
    "operation": "read|write|edit|notebookedit",  # Operation type
    "file_path": "relative/path/to/file.py",      # Path relative to project root
    "status": "success|error",                     # Operation status
    "session_id": "uuid-string",                   # Session identifier
    "tool_input": {...}                            # Optional: filtered tool parameters
}

Error Handling Philosophy:
All errors are handled silently (logged to stderr, exit 0) to ensure the hook
never blocks user workflows. Logging is best-effort only.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_file_path_from_tool_input(tool_name: str, tool_input: dict) -> str | None:
    """
    Extract file path from tool input based on operation type.

    Args:
        tool_name: Name of the tool (Read, Write, Edit, NotebookEdit)
        tool_input: Tool input parameters

    Returns:
        File path string or None if not found
    """
    if tool_name in ["Read", "Write", "Edit"]:
        return tool_input.get("file_path")
    elif tool_name == "NotebookEdit":
        return tool_input.get("notebook_path")
    return None


def make_path_relative(file_path: str) -> str:
    """
    Convert absolute path to relative path (relative to project directory).

    Args:
        file_path: Absolute or relative file path

    Returns:
        Relative path if possible, otherwise original path
    """
    try:
        # Use CLAUDE_PROJECT_DIR if available, otherwise use cwd
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
        abs_path = Path(file_path).resolve()
        project_path = Path(project_dir).resolve()

        # Try to make path relative to project directory
        try:
            relative_path = abs_path.relative_to(project_path)
            return str(relative_path)
        except ValueError:
            # If file is outside project directory, keep absolute path
            return file_path
    except Exception:
        # If any error, keep original path
        return file_path


def get_tool_input_metadata(tool_name: str, tool_input: dict) -> dict:
    """
    Extract relevant metadata from tool input (excluding file_path).

    We track parameters but not content to avoid huge log files.

    Args:
        tool_name: Name of the tool
        tool_input: Tool input parameters

    Returns:
        Dictionary with filtered metadata
    """
    metadata = {}

    if tool_name == "Read":
        # Track pagination parameters
        if "limit" in tool_input:
            metadata["limit"] = tool_input["limit"]
        if "offset" in tool_input:
            metadata["offset"] = tool_input["offset"]

    elif tool_name == "Write":
        # Track content length but not content itself
        if "content" in tool_input:
            metadata["content_length"] = len(tool_input.get("content", ""))

    elif tool_name == "Edit":
        # Track that edit occurred but not the actual strings
        if "old_string" in tool_input:
            metadata["old_string_length"] = len(tool_input.get("old_string", ""))
        if "new_string" in tool_input:
            metadata["new_string_length"] = len(tool_input.get("new_string", ""))
        if "replace_all" in tool_input:
            metadata["replace_all"] = tool_input["replace_all"]

    elif tool_name == "NotebookEdit":
        # Track cell metadata
        if "cell_id" in tool_input:
            metadata["cell_id"] = tool_input["cell_id"]
        if "cell_type" in tool_input:
            metadata["cell_type"] = tool_input["cell_type"]
        if "edit_mode" in tool_input:
            metadata["edit_mode"] = tool_input["edit_mode"]

    return metadata


def get_operation_status(tool_name: str, tool_response: dict) -> str:
    """
    Determine if operation was successful based on tool response.

    Args:
        tool_name: Name of the tool
        tool_response: Tool response data

    Returns:
        "success" or "error"
    """
    if not tool_response:
        # No response usually means success for read operations
        return "success"

    # Check explicit success field
    success = tool_response.get("success", True)
    return "success" if success else "error"


def write_log_entry(session_id: str, log_entry: dict) -> None:
    """
    Write a log entry to the session-specific JSONL file.

    Args:
        session_id: Session identifier
        log_entry: Log entry dictionary to write
    """
    try:
        # Create directory structure
        bundle_dir = Path("logs") / "context_bundles"
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # Use session-specific JSONL file
        bundle_file = bundle_dir / f"session_{session_id}.jsonl"

        # Append to JSONL file (atomic operation for small writes)
        with open(bundle_file, 'a') as f:
            # Write as a single line of JSON
            f.write(json.dumps(log_entry) + '\n')

    except IOError as e:
        print(f"Error writing to context bundle: {e}", file=sys.stderr)
        # Exit cleanly - never block user workflows
        sys.exit(0)


def handle_file_operation(input_data: dict) -> None:
    """
    Handle file operation tracking (Read, Write, Edit, NotebookEdit).

    Args:
        input_data: Hook input data from stdin
    """
    # Extract relevant data
    session_id = input_data.get("session_id", "unknown")
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})

    # Only process tracked file operations
    if tool_name not in ["Read", "Write", "Edit", "NotebookEdit"]:
        sys.exit(0)

    # Extract file path
    file_path = get_file_path_from_tool_input(tool_name, tool_input)
    if not file_path:
        sys.exit(0)

    # Check operation status
    status = get_operation_status(tool_name, tool_response)

    # Skip failed Write operations (no file was actually written)
    if tool_name == "Write" and status == "error":
        sys.exit(0)

    # Convert to relative path
    file_path_relative = make_path_relative(file_path)

    # Create the log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": tool_name.lower(),
        "file_path": file_path_relative,
        "status": status,
        "session_id": session_id
    }

    # Add tool input metadata if present
    tool_metadata = get_tool_input_metadata(tool_name, tool_input)
    if tool_metadata:
        log_entry["tool_input"] = tool_metadata

    # Write to JSONL file
    write_log_entry(session_id, log_entry)


def main():
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)

        # Handle file operations
        handle_file_operation(input_data)

        # Success - exit silently
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch-all for unexpected errors - never block user workflows
        print(f"Unexpected error in context bundle builder: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
