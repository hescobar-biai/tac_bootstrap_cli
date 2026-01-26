---
doc_type: feature
adw_id: feature_Tac_9_task_18_v2
date: 2026-01-26
idk:
  - hook-logger
  - post-tool-use
  - jsonl-logging
  - tool-sanitization
  - audit-trail
  - credential-detection
tags:
  - feature
  - hooks
  - logging
  - security
related_code:
  - .claude/hooks/universal_hook_logger.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2
---

# Universal Hook Logger Template

**ADW ID:** feature_Tac_9_task_18_v2
**Date:** 2026-01-26
**Specification:** specs/issue-259-adw-feature_Tac_9_task_18_v2-sdlc_planner-universal-hook-logger.md

## Overview

The Universal Hook Logger provides comprehensive audit trail logging for ALL Claude Code tool executions via a post_tool_use hook. This Jinja2 template generates a Python script that logs every tool invocation (Read, Write, Edit, Bash, Grep, Glob, WebFetch, Task, etc.) to session-specific JSONL files with built-in sanitization to protect sensitive data.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2`
- **Rendered Example**: `.claude/hooks/universal_hook_logger.py` (582 lines)
- **Core Features**:
  - Universal tool coverage (logs ALL tools, not selective filtering)
  - Security-first sanitization (strips credentials, truncates large payloads)
  - Fail-silent philosophy (always exits 0, never blocks workflows)
  - Session isolation (one JSONL file per session for parallel safety)
  - Comprehensive credential detection using regex patterns
  - Metadata-only logging (excludes full file contents, environment variables)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2`: Jinja2 template with configurable paths via `{{ config.paths.logs_dir }}` and `{{ config.project.name }}`
- `.claude/hooks/universal_hook_logger.py`: Rendered hook script for tac-bootstrap project (testing/reference)

### Key Changes

1. **Universal Tool Sanitization**: Implements tool-specific sanitization functions for Bash, Read, Write, Edit, NotebookEdit, Grep, Glob, WebFetch, Task, and all other tools
2. **JSONL Schema**: Each log entry contains `timestamp`, `session_id`, `tool_name`, sanitized `tool_input`, sanitized `tool_response`, and `status` (success/error)
3. **Credential Detection**: Uses regex patterns to detect and exclude API keys, tokens, passwords, secrets, bearer tokens, and base64-encoded strings
4. **Fail-Silent Error Handling**: All exceptions caught and logged to stderr with exit 0 to never block workflows
5. **Path Sanitization**: Converts absolute paths to relative paths to avoid leaking system structure

### Sanitization Rules

| Tool | Logged Metadata | Excluded Data |
|------|----------------|---------------|
| **Bash** | Command (truncated 500 chars), timeout | Environment variables, output |
| **Read** | file_path, offset, limit, line count | File contents |
| **Write** | file_path, content_length | File contents |
| **Edit** | file_path, old_string_length, new_string_length, replace_all | old_string, new_string |
| **NotebookEdit** | notebook_path, cell_id, cell_type, edit_mode | Cell source code |
| **Grep** | pattern, path, output_mode, glob | Search results |
| **Glob** | pattern, path, result_count | File paths |
| **WebFetch** | url (sanitized) | prompt, response body |
| **Task** | subagent_type, description, prompt (truncated 200 chars) | Full context |
| **All Tools** | Tool name, timestamp, status | Credentials, sensitive env vars |

## How to Use

### 1. Generate Hook in Target Project

When running the TAC Bootstrap CLI to generate an agentic layer, the universal hook logger template will be rendered to `.claude/hooks/universal_hook_logger.py` in the target project with appropriate paths configured.

### 2. Enable Hook (if not auto-enabled)

Add to `.claude/settings.json` in target project:

```json
{
  "hooks": {
    "post_tool_use": ".claude/hooks/universal_hook_logger.py"
  }
}
```

### 3. View Logs

Logs are written to session-specific JSONL files:

```bash
# View logs for specific session
cat logs/universal_hook_logs/session_{session_id}.jsonl | jq .

# Count tool invocations by type
cat logs/universal_hook_logs/session_*.jsonl | jq -r '.tool_name' | sort | uniq -c

# Find all Bash commands executed
cat logs/universal_hook_logs/session_*.jsonl | jq 'select(.tool_name == "Bash") | .tool_input.command'

# Check for errors
cat logs/universal_hook_logs/session_*.jsonl | jq 'select(.status == "error")'
```

## Configuration

The template uses Jinja2 variables from `config` object:

- `{{ config.paths.logs_dir }}`: Base directory for logs (default: `logs`)
- `{{ config.project.name }}`: Project name used in docstring

Example config for rendering:

```python
config = {
    "paths": {"logs_dir": "logs"},
    "project": {"name": "my-project"}
}
```

## Testing

### Syntax Validation

```bash
# Validate Python syntax
python -m py_compile .claude/hooks/universal_hook_logger.py
```

### Functional Testing (Manual)

```bash
# Create test input for Bash tool
echo '{
  "session_id": "test-session-123",
  "tool_name": "Bash",
  "tool_input": {"command": "echo hello", "timeout": 120000},
  "tool_response": {"output": "hello\n", "status": 0}
}' | .claude/hooks/universal_hook_logger.py

# Check log output
cat logs/universal_hook_logs/session_test-session-123.jsonl | jq .
```

### Verify Sanitization

```bash
# Test credential detection (should be sanitized)
echo '{
  "session_id": "test-creds",
  "tool_name": "Bash",
  "tool_input": {"command": "export API_KEY=secret123", "timeout": 120000},
  "tool_response": {"output": "", "status": 0}
}' | .claude/hooks/universal_hook_logger.py

# Verify credential was sanitized in log
cat logs/universal_hook_logs/session_test-creds.jsonl | jq '.tool_input'
```

### Verify Fail-Silent Behavior

```bash
# Test with malformed JSON (should exit 0)
echo 'invalid json' | .claude/hooks/universal_hook_logger.py
echo "Exit code: $?"  # Should be 0

# Test with unwritable directory (should exit 0)
chmod 000 logs/universal_hook_logs 2>/dev/null || true
echo '{"session_id": "test", "tool_name": "Read"}' | .claude/hooks/universal_hook_logger.py
echo "Exit code: $?"  # Should be 0
chmod 755 logs/universal_hook_logs 2>/dev/null || true
```

## Notes

### Security Considerations

- **Credential Detection**: Uses 7 regex patterns to detect API keys, tokens, passwords, secrets, bearer tokens, authorization headers, and base64-encoded strings
- **Truncation Limits**: Commands limited to 500 characters, prompts to 200 characters, other strings to 1000 characters to prevent log bloat
- **Exclusion List**: Never logs environment variables, full file contents, raw WebFetch responses, or detected credentials
- **Path Sanitization**: Always converts to relative paths to avoid leaking system structure

### Performance

- Post-tool-use hooks run after tool completion (not in critical path)
- Synchronous JSONL appends are fast (<1ms per write)
- No buffering to avoid data loss on crashes
- Session-specific files prevent lock contention in parallel execution

### Use Cases

1. **Debugging**: Review complete tool execution history to understand agent behavior
2. **Auditing**: Compliance tracking for regulated environments (healthcare, finance)
3. **Workflow Analysis**: Identify tool usage patterns and optimization opportunities
4. **Incident Response**: Reconstruct agent actions during unexpected behavior
5. **Cost Tracking**: Count tool invocations per session for billing analysis

### Limitations

- No log rotation (files grow indefinitely per session)
- No dynamic log levels (INFO/DEBUG/etc.)
- No structured query interface (raw JSONL files)
- No integration with observability platforms (Datadog, Grafana)

These are intentional design decisions following YAGNI principle. Features can be added in future iterations if needed.

### Future Enhancements (Out of Scope)

- Configurable log rotation policies
- Dynamic log levels via environment variables
- SQLite backend for structured queries
- Integration with observability platforms
- Log compression for long-running sessions
- Real-time log streaming to external systems
