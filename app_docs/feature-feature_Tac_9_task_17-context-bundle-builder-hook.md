---
doc_type: feature
adw_id: feature_Tac_9_task_17
date: 2026-01-26
idk:
  - jinja2-template
  - claude-code-hook
  - jsonl-logging
  - session-tracking
  - file-operations
  - context-recovery
  - audit-trail
  - template-rendering
tags:
  - feature
  - hooks
  - templates
  - logging
related_code:
  - .claude/hooks/context_bundle_builder.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2
---

# Context Bundle Builder Hook Template

**ADW ID:** feature_Tac_9_task_17
**Date:** 2026-01-26
**Specification:** specs/issue-258-adw-feature_Tac_9_task_17-sdlc_planner-context-bundle-builder-hook.md

## Overview

Created a Jinja2 template for a Claude Code tool-use hook that tracks file operations (Read, Write, Edit, NotebookEdit) during agent sessions and saves them to session-specific JSONL files. This enables context recovery, debugging, and audit trails for agent behavior across sessions.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2` - Template for generating context bundle builder hooks in projects
- **Rendered Example**: `.claude/hooks/context_bundle_builder.py` - Working implementation for tac-bootstrap project
- **Session Tracking**: Captures timestamp, operation type, file path, status, and session ID
- **JSONL Storage**: One JSONL file per session for atomic writes and streaming reads
- **Error Handling**: Silent failures that never block user workflows

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2`: Created Jinja2 template using configurable paths via `{{ config.paths.logs_dir }}` and `{{ config.project.name }}`
- `.claude/hooks/context_bundle_builder.py`: Rendered example hook for this project

### Key Changes

1. **Tool-Use Hook Implementation**: Intercepts Read, Write, Edit, and NotebookEdit operations via stdin JSON input
2. **Configurable Paths**: Uses `{{ config.paths.logs_dir }}/context_bundles/` for JSONL storage instead of hardcoded paths
3. **Metadata Extraction**: Tracks operation parameters (offset/limit for Read, content_length for Write, etc.) without storing full content
4. **Path Normalization**: Converts absolute paths to project-relative paths using `CLAUDE_PROJECT_DIR` environment variable
5. **Silent Error Handling**: All exceptions log to stderr and exit(0) to prevent blocking workflows

### JSONL Entry Schema

Each line in `logs/context_bundles/session_{session_id}.jsonl` contains:

```json
{
  "timestamp": "2026-01-26T14:30:45.123456",
  "operation": "read|write|edit|notebookedit",
  "file_path": "relative/path/to/file.py",
  "status": "success|error",
  "session_id": "uuid-string",
  "tool_input": {
    "limit": 100,
    "offset": 0
  }
}
```

## How to Use

### For TAC Bootstrap CLI Users

When generating a new project with `tac-bootstrap init`, the context bundle builder hook will be automatically included in `.claude/hooks/context_bundle_builder.py`.

### Manual Integration

1. Ensure your `config.yml` includes a `paths.logs_dir` configuration
2. The template will be rendered during project generation
3. Hook automatically activates when Claude Code runs (no manual registration needed)

### Reading Context Bundles

View session history using standard JSONL tools:

```bash
# View all operations from a session
cat logs/context_bundles/session_<uuid>.jsonl | jq .

# Filter by operation type
cat logs/context_bundles/session_*.jsonl | jq 'select(.operation == "write")'

# Find most-read files
cat logs/context_bundles/session_*.jsonl | jq -r '.file_path' | sort | uniq -c | sort -rn
```

## Configuration

The template uses these Jinja2 variables:

- `{{ config.project.name }}`: Project name used in docstring header
- `{{ config.paths.logs_dir }}`: Directory for storing JSONL files (default: `logs/`)

## Testing

### Verify Template Syntax

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Check Rendered Output

```bash
# Verify rendered file is valid Python
python3 -m py_compile .claude/hooks/context_bundle_builder.py
```

### Simulate Hook Execution

```bash
# Test with sample input
echo '{"session_id":"test-123","tool_name":"Read","tool_input":{"file_path":"test.py"},"tool_response":{"success":true}}' | python3 .claude/hooks/context_bundle_builder.py

# Check JSONL output
cat logs/context_bundles/session_test-123.jsonl
```

### Linting and Type Checking

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

- **JSONL Format**: Chosen for streaming reads, append-friendly writes, and line-atomic operations safe for concurrent access
- **Metadata Only**: Tracks parameters like `content_length` and `offset/limit` but not actual file content to prevent log bloat
- **Session Isolation**: One file per session prevents race conditions and enables easy session-based analysis
- **Best-Effort Logging**: Hook never blocks user workflows; all errors exit cleanly with stderr logging

### Future Enhancements (Out of Scope)

- Context recovery CLI command (`/recover-context <session_id>`)
- Integration with `/prime` to auto-inject previous session context
- JSONL rotation/compression for old sessions
- Aggregate statistics dashboard (most-modified files, operation frequency)
- Filtering by file pattern or date range
