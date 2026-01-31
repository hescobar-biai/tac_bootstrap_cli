---
doc_type: feature
adw_id: feature_Tac_12_task_27
date: 2026-01-31
idk:
  - hook-system
  - context-compaction
  - logging
  - jinja2-templating
  - session-management
tags:
  - feature
  - hooks
  - observability
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_compact.py.j2
  - .claude/hooks/pre_compact.py
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Pre-Compact Hook Template Implementation

**ADW ID:** feature_Tac_12_task_27
**Date:** 2026-01-31
**Specification:** specs/issue-479-adw-feature_Tac_12_task_27-sdlc_planner-pre-compact-hook.md

## Overview

Created a Jinja2 template for the `pre_compact.py` hook that captures context state before Claude Code performs context compaction. The hook provides observability into context management by logging pre-compaction metrics and session metadata, enabling debugging and analysis of the compaction process without requiring external utility dependencies.

## What Was Built

- **Jinja2 Template Conversion**: Converted the base `pre_compact.py` implementation to a `pre_compact.py.j2` template with configuration variable support
- **Configuration Integration**: Replaced hardcoded path logic with `{{ config.paths.logs_dir }}` for dynamic configuration during project generation
- **Hook Self-Sufficiency**: Removed dependency on external `utils.constants` module by implementing inline directory creation logic
- **Enhanced Documentation**: Added docstring describing hook purpose, behavior, and log output location
- **Python 3 Shebang**: Updated from uv script format to standard Python 3 executable format for better portability

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_compact.py.j2`: Updated template with configuration variables and removed external dependencies

### Key Changes

1. **Removed uv Script Shebang**: Changed from `#!/usr/bin/env -S uv run --script` with requires-python metadata to standard `#!/usr/bin/env python3` for generated hooks
2. **Configuration Variable**: Replaced `ensure_session_log_dir(session_id)` utility call with inline logic using `{{ config.paths.logs_dir }}` template variable for path configuration
3. **Inline Directory Creation**: Implemented `log_dir.mkdir(parents=True, exist_ok=True)` directly in hook code instead of delegating to utility module
4. **Enhanced Docstring**: Added module-level documentation describing hook purpose, input expectations, and log file output location
5. **Maintained Error Handling**: Preserved graceful error handling pattern that exits with code 0 on any exception to avoid disrupting Claude Code workflow

## How to Use

The `pre_compact.py` hook is automatically included when generating new projects via the TAC Bootstrap CLI:

1. **Generate Project**: Use the CLI to scaffold a new project
   ```bash
   uv run tac-bootstrap scaffold --name my-project --output /path/to/project
   ```

2. **Hook Activation**: The hook is automatically placed in `.claude/hooks/pre_compact.py` with executable permissions

3. **Automatic Execution**: The hook runs automatically when Claude Code begins context compaction, receiving JSON input via stdin containing session and context information

4. **Log Output**: Pre-compaction data is appended to `.claude/logs/{session_id}/pre_compact.json` as a JSON array

### Example Hook Input

```json
{
  "session_id": "abc123",
  "context_size": 45000,
  "timestamp": "2026-01-31T10:30:45Z",
  "compaction_reason": "token_limit"
}
```

### Example Log Output

`.claude/logs/{session_id}/pre_compact.json`:
```json
[
  {
    "session_id": "abc123",
    "context_size": 45000,
    "timestamp": "2026-01-31T10:30:45Z",
    "compaction_reason": "token_limit"
  }
]
```

## Configuration

The hook uses the following configuration variable:

- `{{ config.paths.logs_dir }}`: Base directory path for session logs. Configured during project generation based on user preferences

## Testing

### Verify Template Rendering

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v -k "pre_compact" --tb=short
```

### Smoke Test: Generate Project

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap scaffold --name test-project --output /tmp/test-project
test -f /tmp/test-project/.claude/hooks/pre_compact.py && echo "Hook file exists"
grep "config.paths.logs_dir" /tmp/test-project/.claude/hooks/pre_compact.py && echo "Configuration variable present"
```

### Verify Hook Logic

```bash
# Test hook with sample JSON input
echo '{"session_id": "test-123", "context_size": 50000}' | \
  python3 /tmp/test-project/.claude/hooks/pre_compact.py
test -f /tmp/test-project/.claude/logs/test-123/pre_compact.json && echo "Log file created"
```

### Run All Validation

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
uv run ruff check .
uv run mypy tac_bootstrap/
```

## Notes

- **Hook Registration**: The hook is already registered in `scaffold_service.py` at line 349, no additional integration changes required
- **Error Handling**: All errors result in graceful exit (exit code 0) to prevent disruption of Claude Code workflow
- **JSON Format**: Uses append-only JSON array format for audit trail of all pre-compaction events
- **No External Dependencies**: Template only uses Python standard library (json, sys, pathlib)
- **Session Isolation**: Each session maintains its own log directory under `.claude/logs/{session_id}/`
- **Malformed Input**: Hook handles missing or invalid JSON gracefully by exiting cleanly without logging
