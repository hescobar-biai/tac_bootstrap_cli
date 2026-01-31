---
doc_type: feature
adw_id: feature_Tac_12_task_22_2
date: 2026-01-31
idk:
  - hook
  - observability
  - telemetry
  - pre-tool-use
  - logging
  - non-blocking
  - Claude Code
tags:
  - feature
  - hooks
  - observability
related_code:
  - .claude/hooks/pre_tool_use.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Pre-Tool Use Observability Hook

**ADW ID:** feature_Tac_12_task_22_2
**Date:** 2026-01-31
**Specification:** specs/issue-474-adw-feature_Tac_12_task_22_2-sdlc_planner-pre-tool-use-hook.md

## Overview

This feature implements a lightweight pre-tool-use hook that runs before every tool invocation in Claude Code. The hook provides observability and telemetry by logging basic metadata about each tool call without blocking execution. This replaces the previous implementation which focused on security validation (dangerous command blocking, forbidden path checks) with a simpler, non-blocking observability-focused approach.

## What Was Built

- **Refactored pre_tool_use.py hook** - Simplified from 144 lines to 57 lines, removing security validation logic and focusing purely on observability logging
- **Updated Jinja2 template** - Replaced complex security template with minimal observability-focused template that uses only project name variable substitution
- **Structured text output** - Outputs human-readable key-value format to stdout instead of writing to JSON log files
- **Robust error handling** - Always exits successfully (code 0) even on errors to prevent workflow disruption

## Technical Implementation

### Files Modified

- `.claude/hooks/pre_tool_use.py`: Refactored from security validation hook to pure observability hook
  - Changed from complex rm command blocking and forbidden path validation to simple metadata logging
  - Removed file-based JSON logging, now outputs to stdout
  - Changed from Python 3.8+ to 3.11+ requirement
  - Added ISO 8601 timestamp formatting
  - Simplified error handling to always exit with code 0

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`: Updated template to match new implementation
  - Removed Jinja2 variables for forbidden paths and log directories
  - Simplified to use only `{{ config.project.name }}` in docstring
  - Removed security validation logic entirely
  - Matches the pattern of session_start.py.j2 for simplicity

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Updated hook description
  - Changed from "Pre-execution validation" to "Pre-tool observability logging" (line 349)

### Key Changes

- **Removed security features**: No more dangerous command blocking or forbidden path validation (moved responsibility elsewhere if needed)
- **Structured text output**: Changed from JSON file logging to stdout with format `[TIMESTAMP] tool=TOOL_NAME cwd=CWD session=SESSION_ID`
- **Non-blocking design**: Always exits with code 0, even on JSON decode errors or other exceptions
- **Simplified dependencies**: Removed pathlib, re modules; only uses json, os, sys, datetime
- **Improved observability**: Captures tool name, ISO 8601 timestamp, current working directory, and session ID

## How to Use

The hook runs automatically before every tool call in Claude Code. No configuration or user action required.

To observe hook output when running Claude Code:
1. Hook output appears in stdout before each tool execution
2. Look for lines with format: `[2026-01-31T12:34:56.789012+00:00] tool=Read cwd=/path/to/project session=abc123`

The hook provides telemetry for:
- Debugging agent workflows
- Understanding tool usage patterns
- Monitoring session behavior
- Tracking working directory changes

## Configuration

No configuration required in version 1. The hook is statically implemented with no options.

Future enhancements could include:
- Configurable log format
- Filtering specific tools
- Log level controls
- Output destination options

## Testing

Test the hook manually with valid JSON input:

```bash
echo '{"tool_name": "Read", "tool_input": {"file_path": "test.txt"}, "session_id": "test-123"}' | .claude/hooks/pre_tool_use.py
```

Expected output (timestamp will vary):
```
[2026-01-31T12:34:56.789012+00:00] tool=Read cwd=/current/working/directory session=test-123
```

Verify exit code is 0:

```bash
echo '{"tool_name": "Read", "tool_input": {}, "session_id": "test"}' | .claude/hooks/pre_tool_use.py && echo "Exit code: $?"
```

Test error handling with invalid JSON:

```bash
echo 'invalid json' | .claude/hooks/pre_tool_use.py && echo "Exit code: $?"
```

Test with missing fields (should use defaults):

```bash
echo '{}' | .claude/hooks/pre_tool_use.py
```

Run full validation suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This hook replaced a more complex security validation implementation with a simpler observability-focused approach
- The previous implementation blocked dangerous `rm -rf` commands and forbidden path access - this functionality should be moved to a dedicated security hook if needed
- Hook is called frequently (before every tool use), so it's designed to be lightweight and fast
- Uses structured text output instead of JSON for better human readability
- Always exits successfully to prevent disrupting the tool execution pipeline
- Follows the same pattern as session_start.py hook for consistency
- Template uses minimal Jinja2 variables to keep generated hooks simple and maintainable
