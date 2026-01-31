---
doc_type: feature
adw_id: feature_Tac_12_task_23
date: 2026-01-31
idk:
  - hook
  - post-tool-use
  - logging
  - observability
  - truncation
  - json
tags:
  - feature
  - hooks
  - logging
related_code:
  - .claude/hooks/post_tool_use.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Post-Tool Use Hook

**ADW ID:** feature_Tac_12_task_23
**Date:** 2026-01-31
**Specification:** specs/issue-475-adw-feature_Tac_12_task_23-sdlc_planner-create-post-tool-use-hook.md

## Overview

Enhanced the post-tool-use hook to provide structured logging of tool execution details with output truncation. This hook captures tool name, input parameters, truncated output, timestamp, and session ID after every tool execution in Claude Code sessions. The implementation ensures best-effort logging that never blocks workflows.

## What Was Built

- Enhanced `.claude/hooks/post_tool_use.py` with output truncation and structured logging
- Added `truncate_output()` helper function to prevent log bloat (500 char limit)
- Implemented structured log entry extraction for better parseability
- Added comprehensive docstrings explaining hook behavior
- Aligned base implementation with template patterns for consistency

## Technical Implementation

### Files Modified

- `.claude/hooks/post_tool_use.py`: Enhanced with truncation logic and structured logging
  - Added `truncate_output(output, max_length=500)` function
  - Extracted specific fields: tool_name, tool_input, tool_output (truncated), timestamp, session_id
  - Replaced `ensure_session_log_dir` utility with direct Path operations for self-containment
  - Added comprehensive module and function docstrings

### Key Changes

1. **Output Truncation**: Implemented 500-character limit on tool_output to prevent excessive log sizes while preserving debugging context
2. **Structured Log Entries**: Changed from logging raw input_data to extracting specific fields into structured log_entry dict
3. **Directory Management**: Replaced utility dependency with direct `Path(".claude/logs") / session_id` pattern for template alignment
4. **Documentation**: Added module-level docstring explaining hook purpose, log location, and error handling behavior
5. **Error Handling**: Maintained silent failure pattern (sys.exit(0) on all exceptions) to ensure hooks never disrupt workflows

## How to Use

### Automatic Usage

The hook runs automatically after every tool execution in Claude Code sessions. No manual invocation required.

### Log Location

Logs are written to: `.claude/logs/{session_id}/post_tool_use.json`

Each log entry contains:
```json
{
  "tool_name": "Read",
  "tool_input": {"file_path": "/path/to/file.py"},
  "tool_output": "file contents... [truncated]",
  "timestamp": "2026-01-31T10:30:45.123456",
  "session_id": "abc123"
}
```

### Viewing Logs

```bash
# View latest session logs
cat .claude/logs/*/post_tool_use.json | jq '.'

# Count tool executions
cat .claude/logs/*/post_tool_use.json | jq 'length'

# Filter by tool name
cat .claude/logs/*/post_tool_use.json | jq '.[] | select(.tool_name == "Read")'
```

## Configuration

No configuration required. The hook is automatically registered and executed by Claude Code.

**Default Settings:**
- Output truncation limit: 500 characters
- Log format: JSON with indent=2
- Log location: `.claude/logs/{session_id}/post_tool_use.json`
- Error handling: Silent failures (exit 0)

## Testing

### Functional Test

Verify hook creates logs after tool execution:

```bash
# Trigger any tool execution in Claude Code, then check logs
ls -la .claude/logs/*/post_tool_use.json
```

### Validation Test

Verify hook is properly registered in scaffold service:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Code Quality

```bash
# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

1. **Truncation Limit**: 500 characters balances log size management with debugging utility
2. **Silent Failures**: Hook exits 0 on all errors to ensure observability never blocks user workflows
3. **No Filtering**: All tool executions are logged unconditionally for complete observability
4. **Self-Contained**: Removed utility dependencies to make hook work independently in generated projects
5. **JSON Format**: indent=2 provides human readability while maintaining machine parseability

### Edge Cases Handled

- **Long outputs**: Truncated with "... [truncated]" suffix
- **None/null outputs**: Handled gracefully without crashes
- **Missing session_id**: Defaults to "unknown"
- **Corrupted log files**: JSON decode errors are silently ignored, log is reinitialized
- **Permission errors**: Silent exit 0

### Future Considerations

- Consider adding configurable truncation limits via environment variable
- Potential log rotation for long-running sessions
- Optional integration with external observability platforms
