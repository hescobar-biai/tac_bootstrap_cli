---
doc_type: feature
adw_id: feature_Tac_12_task_26
date: 2026-01-31
idk:
  - subagent-lifecycle-tracking
  - hook-pattern
  - session-logging
  - json-aggregation
  - silent-failure
  - event-tracking
tags:
  - feature
  - hooks
  - infrastructure
related_code:
  - .claude/hooks/subagent_stop.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Subagent Stop Hook Implementation

**ADW ID:** feature_Tac_12_task_26
**Date:** 2026-01-31
**Specification:** issue-478-adw-feature_Tac_12_task_26-sdlc_planner-subagent-stop-hook.md

## Overview

Implemented `subagent_stop.py` hook to enable automatic lifecycle tracking of subagent execution. This hook reads subagent metadata from stdin and appends it to session-specific JSON logs for post-hoc analysis and audit trail creation.

## What Was Built

- **Subagent Stop Hook** (`.claude/hooks/subagent_stop.py`): Production hook implementation that logs subagent lifecycle events
- **Hook Template** (`subagent_stop.py.j2`): Jinja2 template for CLI-based scaffold generation
- **Integration**: Registered hook in `scaffold_service.py` for automatic generation in new projects

## Technical Implementation

### Files Modified

- `.claude/hooks/subagent_stop.py`: Base hook implementation reading JSON from stdin and appending to session logs
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/subagent_stop.py.j2`: Jinja2 template for scaffold generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:350`: Hook registration in `_add_claude_files()` method

### Key Changes

- **JSON-based event logging**: Reads subagent lifecycle metadata from stdin as JSON and appends to chronological array
- **Per-session isolation**: Each session maintains separate `.claude/hooks/logs/subagent_stop.json` file via `ensure_session_log_dir()` utility
- **Silent failure pattern**: Hook gracefully handles JSON decode errors and file I/O exceptions without disrupting parent session
- **Transcript handling**: Optional `--chat` flag converts `.jsonl` transcript files to JSON array format in `chat.json`
- **Atomic writes**: In-memory list accumulation with single file write operation for data integrity

## How to Use

### Basic Operation

The hook automatically executes when subagent execution completes. Claude Code passes subagent metadata via stdin:

```bash
# Hook receives JSON payload like:
{
  "session_id": "abc123",
  "subagent_id": "task-123",
  "status": "completed",
  "execution_time": 45.2,
  "result": {...},
  "error": null
}
```

### With Transcript Export

Use the `--chat` flag to also export conversation transcript:

```bash
echo '{"session_id":"abc123","transcript_path":"/path/to/transcript.jsonl"}' | \
  .claude/hooks/subagent_stop.py --chat
```

### Accessing Logged Events

Session logs are stored in `.claude/hooks/logs/`:

```bash
# View all subagent events for a session
cat .claude/hooks/logs/subagent_stop.json | jq '.'

# Query specific subagent
cat .claude/hooks/logs/subagent_stop.json | jq '.[] | select(.subagent_id=="task-123")'

# Extract error events
cat .claude/hooks/logs/subagent_stop.json | jq '.[] | select(.error != null)'
```

## Configuration

### Environment Variables

- `SESSION_ID`: (Optional) Override session identifier for logging. If not set, extracted from hook input.

### Log Directory Structure

```
.claude/hooks/logs/
├── subagent_stop.json      # Chronological array of all subagent lifecycle events
└── chat.json               # Optional transcript export (if --chat flag used)
```

### Dependencies

- `python-dotenv`: For optional `.env` file loading
- `utils.constants.ensure_session_log_dir()`: Utility function for session directory management

## Testing

### Verify Hook Installation

```bash
# Check hook file exists and is executable
ls -la .claude/hooks/subagent_stop.py
```

### Test Hook Execution

```bash
# Simulate subagent completion event
echo '{
  "session_id": "test-session",
  "subagent_id": "test-subagent",
  "status": "completed",
  "execution_time": 5.2,
  "result": {"output": "success"}
}' | ./.claude/hooks/subagent_stop.py
```

### Verify Logged Data

```bash
# Check log file was created and contains data
cat .claude/hooks/logs/subagent_stop.json | jq 'length'
```

### Test Error Handling

```bash
# Invalid JSON should fail silently (exit 0)
echo 'invalid json' | ./.claude/hooks/subagent_stop.py
echo "Exit code: $?"  # Should be 0
```

## Notes

- Hook follows established `stop.py` pattern for consistency across Claude Code infrastructure
- No transformation or validation of input data—raw JSON is stored as-is for audit trail accuracy
- Silent failure design prevents hook errors from disrupting subagent execution or parent sessions
- Per-session logging enables independent analysis without cross-session data contamination
- Template-based generation ensures all new projects include subagent lifecycle tracking automatically
