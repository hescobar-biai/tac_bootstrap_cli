#!/usr/bin/env python3
"""
Universal Hook Logger - Claude Code Hook for tac-bootstrap

Provides comprehensive logging of ALL Claude Code tool executions to session-specific
JSONL files. Tracks every tool invocation (Read, Write, Edit, Bash, Grep, Glob,
WebFetch, Task, etc.) for debugging, auditing, and workflow analysis.

This hook enables:
- Complete audit trail of all agent actions
- Debugging complex workflows by reviewing tool execution history
- Compliance tracking for regulated environments
- Workflow analysis and optimization insights

JSONL files are stored at: logs/universal_hook_logs/session_{session_id}.jsonl

JSONL Entry Schema:
{
    "timestamp": "2024-01-26T14:30:45.123456",  # ISO8601 timestamp
    "session_id": "uuid-string",                 # Session identifier
    "tool_name": "Bash|Read|Write|...",          # Tool name
    "tool_input": {...},                         # Sanitized input metadata
    "tool_response": {...},                      # Sanitized response metadata
    "status": "success|error"                    # Operation status
}

Security & Privacy:
- Sanitizes credentials (API keys, tokens, passwords)
- Excludes full file contents (tracks metadata only)
- Truncates large payloads (commands > 500 chars, prompts > 200 chars)
- Converts paths to relative format
- Never logs environment variables or sensitive data

Error Handling Philosophy:
All errors are handled silently (logged to stderr, exit 0) to ensure the hook
never blocks user workflows. Logging is best-effort only.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# Credential detection patterns
CREDENTIAL_PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']?[\w-]+',
    r'token["\']?\s*[:=]\s*["\']?[\w-]+',
    r'password["\']?\s*[:=]\s*["\']?[\w-]+',
    r'secret["\']?\s*[:=]\s*["\']?[\w-]+',
    r'bearer\s+[\w-]+',
    r'authorization["\']?\s*[:=]\s*["\']?[\w-]+',
    r'[A-Za-z0-9+/]{40,}={0,2}',  # Base64-like strings
]

CREDENTIAL_REGEX = re.compile('|'.join(CREDENTIAL_PATTERNS), re.IGNORECASE)


def detect_credentials(value: str) -> bool:
    """
    Detect potential credentials in string values.

    Args:
        value: String to check for credentials

    Returns:
        True if credentials detected, False otherwise
    """
    if not isinstance(value, str):
        return False
    return bool(CREDENTIAL_REGEX.search(value))


def truncate_string(value: str, max_length: int) -> str:
    """
    Truncate string to max length with ellipsis.

    Args:
        value: String to truncate
        max_length: Maximum length

    Returns:
        Truncated string
    """
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."


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


def sanitize_bash_input(tool_input: dict) -> dict:
    """
    Sanitize Bash tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include command but truncate if too long
    if "command" in tool_input:
        command = tool_input["command"]
        if detect_credentials(command):
            sanitized["command"] = "[REDACTED - contains credentials]"
        else:
            sanitized["command"] = truncate_string(command, 500)

    # Include timeout if present
    if "timeout" in tool_input:
        sanitized["timeout"] = tool_input["timeout"]

    # Include description if present
    if "description" in tool_input:
        sanitized["description"] = truncate_string(tool_input["description"], 200)

    # Never log environment variables or run_in_background flag
    return sanitized


def sanitize_read_input(tool_input: dict) -> dict:
    """
    Sanitize Read tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include file path as relative
    if "file_path" in tool_input:
        sanitized["file_path"] = make_path_relative(tool_input["file_path"])

    # Include pagination parameters
    if "offset" in tool_input:
        sanitized["offset"] = tool_input["offset"]
    if "limit" in tool_input:
        sanitized["limit"] = tool_input["limit"]

    # Never log file content
    return sanitized


def sanitize_write_input(tool_input: dict) -> dict:
    """
    Sanitize Write tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include file path as relative
    if "file_path" in tool_input:
        sanitized["file_path"] = make_path_relative(tool_input["file_path"])

    # Track content length but not content itself
    if "content" in tool_input:
        content = tool_input["content"]
        sanitized["content_length"] = len(content)
        # Flag if content might contain credentials
        if detect_credentials(content):
            sanitized["contains_credentials"] = True

    return sanitized


def sanitize_edit_input(tool_input: dict) -> dict:
    """
    Sanitize Edit tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include file path as relative
    if "file_path" in tool_input:
        sanitized["file_path"] = make_path_relative(tool_input["file_path"])

    # Track string lengths but not strings themselves
    if "old_string" in tool_input:
        sanitized["old_string_length"] = len(tool_input["old_string"])
    if "new_string" in tool_input:
        sanitized["new_string_length"] = len(tool_input["new_string"])

    # Include replace_all flag
    if "replace_all" in tool_input:
        sanitized["replace_all"] = tool_input["replace_all"]

    return sanitized


def sanitize_notebookedit_input(tool_input: dict) -> dict:
    """
    Sanitize NotebookEdit tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include notebook path as relative
    if "notebook_path" in tool_input:
        sanitized["notebook_path"] = make_path_relative(tool_input["notebook_path"])

    # Include cell metadata
    if "cell_id" in tool_input:
        sanitized["cell_id"] = tool_input["cell_id"]
    if "cell_type" in tool_input:
        sanitized["cell_type"] = tool_input["cell_type"]
    if "edit_mode" in tool_input:
        sanitized["edit_mode"] = tool_input["edit_mode"]

    # Track source length but not source itself
    if "new_source" in tool_input:
        sanitized["new_source_length"] = len(tool_input["new_source"])

    return sanitized


def sanitize_grep_input(tool_input: dict) -> dict:
    """
    Sanitize Grep tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include pattern (truncate if too long)
    if "pattern" in tool_input:
        sanitized["pattern"] = truncate_string(tool_input["pattern"], 200)

    # Include path as relative
    if "path" in tool_input:
        sanitized["path"] = make_path_relative(tool_input["path"])

    # Include search options
    if "output_mode" in tool_input:
        sanitized["output_mode"] = tool_input["output_mode"]
    if "glob" in tool_input:
        sanitized["glob"] = tool_input["glob"]
    if "type" in tool_input:
        sanitized["type"] = tool_input["type"]
    if "-i" in tool_input:
        sanitized["case_insensitive"] = tool_input["-i"]
    if "multiline" in tool_input:
        sanitized["multiline"] = tool_input["multiline"]

    # Never log results
    return sanitized


def sanitize_glob_input(tool_input: dict) -> dict:
    """
    Sanitize Glob tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include pattern
    if "pattern" in tool_input:
        sanitized["pattern"] = tool_input["pattern"]

    # Include path as relative
    if "path" in tool_input:
        sanitized["path"] = make_path_relative(tool_input["path"])

    # Never log results
    return sanitized


def sanitize_webfetch_input(tool_input: dict) -> dict:
    """
    Sanitize WebFetch tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include URL (check for credentials in query params)
    if "url" in tool_input:
        url = tool_input["url"]
        if detect_credentials(url):
            sanitized["url"] = "[REDACTED - contains credentials]"
        else:
            sanitized["url"] = url

    # Never log prompt or response
    return sanitized


def sanitize_task_input(tool_input: dict) -> dict:
    """
    Sanitize Task tool input.

    Args:
        tool_input: Raw tool input

    Returns:
        Sanitized metadata
    """
    sanitized = {}

    # Include subagent type
    if "subagent_type" in tool_input:
        sanitized["subagent_type"] = tool_input["subagent_type"]

    # Include description
    if "description" in tool_input:
        sanitized["description"] = tool_input["description"]

    # Include prompt but truncate
    if "prompt" in tool_input:
        prompt = tool_input["prompt"]
        sanitized["prompt"] = truncate_string(prompt, 200)

    # Include mode if present
    if "mode" in tool_input:
        sanitized["mode"] = tool_input["mode"]

    # Include model if present
    if "model" in tool_input:
        sanitized["model"] = tool_input["model"]

    # Never log full context
    return sanitized


def sanitize_tool_input(tool_name: str, tool_input: dict) -> dict:
    """
    Sanitize tool input based on tool type.

    Args:
        tool_name: Name of the tool
        tool_input: Raw tool input

    Returns:
        Sanitized metadata dictionary
    """
    if not isinstance(tool_input, dict):
        return {}

    # Route to specific sanitizer
    if tool_name == "Bash":
        return sanitize_bash_input(tool_input)
    elif tool_name == "Read":
        return sanitize_read_input(tool_input)
    elif tool_name == "Write":
        return sanitize_write_input(tool_input)
    elif tool_name == "Edit":
        return sanitize_edit_input(tool_input)
    elif tool_name == "NotebookEdit":
        return sanitize_notebookedit_input(tool_input)
    elif tool_name == "Grep":
        return sanitize_grep_input(tool_input)
    elif tool_name == "Glob":
        return sanitize_glob_input(tool_input)
    elif tool_name == "WebFetch":
        return sanitize_webfetch_input(tool_input)
    elif tool_name == "Task":
        return sanitize_task_input(tool_input)
    else:
        # Unknown tool - log minimal safe metadata
        return {"tool_name": tool_name}


def sanitize_tool_response(tool_name: str, tool_response: dict) -> dict:
    """
    Sanitize tool response based on tool type.

    Args:
        tool_name: Name of the tool
        tool_response: Raw tool response

    Returns:
        Sanitized metadata dictionary
    """
    if not isinstance(tool_response, dict):
        return {}

    sanitized = {}

    # Always include success status if present
    if "success" in tool_response:
        sanitized["success"] = tool_response["success"]

    # Include error messages if present (truncate to avoid leaking sensitive data)
    if "error" in tool_response:
        error = tool_response["error"]
        if isinstance(error, str):
            sanitized["error"] = truncate_string(error, 500)

    # For Bash, include exit code but not output
    if tool_name == "Bash":
        if "exit_code" in tool_response:
            sanitized["exit_code"] = tool_response["exit_code"]
        # Never log stdout/stderr

    # For file operations, minimal metadata
    if tool_name in ["Read", "Write", "Edit", "NotebookEdit"]:
        # Just success status, no content
        pass

    # For search operations, track result counts but not results
    if tool_name in ["Grep", "Glob"]:
        if "result_count" in tool_response:
            sanitized["result_count"] = tool_response["result_count"]
        # Never log actual results

    # For Task, track completion but not output
    if tool_name == "Task":
        if "agent_id" in tool_response:
            sanitized["agent_id"] = tool_response["agent_id"]
        # Never log full output

    return sanitized


def get_operation_status(tool_response: dict) -> str:
    """
    Determine if operation was successful based on tool response.

    Args:
        tool_response: Tool response data

    Returns:
        "success" or "error"
    """
    if not tool_response:
        # No response usually means success
        return "success"

    # Check explicit success field
    success = tool_response.get("success", True)

    # Also check for error field
    if "error" in tool_response:
        return "error"

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
        log_dir = Path("logs") / "universal_hook_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Use session-specific JSONL file
        log_file = log_dir / f"session_{session_id}.jsonl"

        # Append to JSONL file (atomic operation for small writes)
        with open(log_file, 'a') as f:
            # Write as a single line of JSON
            f.write(json.dumps(log_entry) + '\n')

    except IOError as e:
        print(f"Error writing to universal hook log: {e}", file=sys.stderr)
        # Exit cleanly - never block user workflows
        sys.exit(0)


def handle_tool_execution(input_data: dict) -> None:
    """
    Handle logging of all tool executions.

    Args:
        input_data: Hook input data from stdin
    """
    # Extract relevant data
    session_id = input_data.get("session_id", "unknown")
    tool_name = input_data.get("tool_name", "Unknown")
    tool_input = input_data.get("tool_input", {})
    tool_response = input_data.get("tool_response", {})

    # Sanitize input and response
    sanitized_input = sanitize_tool_input(tool_name, tool_input)
    sanitized_response = sanitize_tool_response(tool_name, tool_response)

    # Determine operation status
    status = get_operation_status(tool_response)

    # Create the log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "tool_name": tool_name,
        "tool_input": sanitized_input,
        "tool_response": sanitized_response,
        "status": status
    }

    # Write to JSONL file
    write_log_entry(session_id, log_entry)


def main():
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)

        # Handle tool execution logging
        handle_tool_execution(input_data)

        # Success - exit silently
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        # Catch-all for unexpected errors - never block user workflows
        print(f"Unexpected error in universal hook logger: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()