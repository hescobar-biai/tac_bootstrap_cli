---
doc_type: feature
adw_id: feature_Tac_12_task_21
date: 2026-01-30
idk:
  - session-management
  - hook
  - configuration
  - error-handling
  - metadata-capture
  - jinja2-template
tags:
  - feature
  - hooks
  - observability
related_code:
  - .claude/hooks/session_start.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - .claude/session_context.json
---

# Session Start Hook

**ADW ID:** feature_Tac_12_task_21
**Date:** 2026-01-30
**Specification:** specs/issue-473-adw-feature_Tac_12_task_21-sdlc_planner-create-session-start-hook.md

## Overview

The session_start hook captures session initialization context when Claude Code sessions begin. It records git branch, model name, project metadata, timestamp, and working directory to a JSON file, enabling session tracking, debugging, and observability.

## What Was Built

- **Base Hook Implementation**: `.claude/hooks/session_start.py` - Standalone executable hook that captures session metadata
- **Jinja2 Template**: `session_start.py.j2` - Template for CLI-generated projects
- **Scaffold Service Integration**: Updated to include session_start hook in generated projects
- **Session Context File**: `.claude/session_context.json` - JSON output containing session metadata

## Technical Implementation

### Files Modified

- `.claude/hooks/session_start.py`: New executable hook with uv shebang pattern, graceful error handling, and metadata capture
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2`: Jinja2 template mirroring base implementation with `{{ config.project.name }}` variable
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added session_start.py to hooks list at line 356
- `.claude/session_context.json`: New file containing session metadata as flat JSON dictionary

### Key Changes

- Uses `#!/usr/bin/env -S uv run --script` pattern with PyYAML dependency
- Captures git branch via subprocess with 5-second timeout and graceful fallback to "unknown"
- Reads project name from config.yml using PyYAML safe_load
- Retrieves model name from CLAUDE_MODEL environment variable
- Generates ISO 8601 timestamp using datetime.now(timezone.utc)
- Writes all metadata to `.claude/session_context.json` as flat dictionary
- All operations wrapped in try-except blocks with "unknown" fallbacks
- Always exits with status 0 to ensure session-safe, non-blocking behavior

### Session Context Structure

The hook creates a JSON file with the following structure:

```json
{
  "git_branch": "feature-branch-name",
  "model": "claude-sonnet-4-5-20250929",
  "project_name": "tac-bootstrap",
  "timestamp": "2026-01-30T12:34:56.789012+00:00",
  "cwd": "/Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_12_task_21"
}
```

## How to Use

### Automatic Execution

The hook executes automatically when Claude Code sessions start (configured in `.claude/settings.json`):

```json
{
  "hooks": {
    "session_start": ".claude/hooks/session_start.py"
  }
}
```

### Manual Execution

You can manually test the hook:

```bash
uv run .claude/hooks/session_start.py
```

### Reading Session Context

After execution, read the session context file:

```bash
cat .claude/session_context.json
```

### Integration in New Projects

When generating new projects with TAC Bootstrap CLI, the session_start hook is automatically included:

```bash
tac-bootstrap generate my-project
```

The hook will be present in `.claude/hooks/session_start.py` and configured in `.claude/settings.json`.

## Configuration

### Dependencies

The hook requires PyYAML for config.yml parsing:

```toml
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml",
# ]
# ///
```

### Environment Variables

- **CLAUDE_MODEL**: Model identifier (e.g., "claude-sonnet-4-5-20250929")
  - Fallback: "unknown" if not set

### Required Files

- `config.yml`: Project configuration file with project.name field
  - Fallback: "unknown" if missing or malformed

### Git Repository

- Git repository with valid branch name
  - Fallback: "unknown" if not a git repo or git command fails

## Testing

### Test Base Hook Execution

```bash
uv run .claude/hooks/session_start.py
```

### Verify Session Context File Creation

```bash
test -f .claude/session_context.json && echo "Session context file created"
```

### Verify JSON Structure

```bash
cat .claude/session_context.json
```

Expected output should contain all required fields: git_branch, model, project_name, timestamp, cwd.

### Test Error Handling in Non-Git Directory

```bash
cd /tmp && uv run /path/to/.claude/hooks/session_start.py
```

Should create session_context.json with git_branch="unknown".

### Run Scaffold Service Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Run Linting and Type Checking

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### CLI Smoke Test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is task 21 of 49 in the TAC Bootstrap Wave 3 implementation plan
- Hook follows the same pattern as send_event.py for consistency
- The hook is non-blocking and session-safe, always exiting with status 0
- JSON file is overwritten on each session start (not merged or appended)
- Future enhancement: Could integrate with send_event.py for remote observability
- Future enhancement: Could capture additional metadata (Python version, OS, CPU/memory stats)
- Reference implementation exists in TAC-12 project but was not required for this task
- Template uses minimal Jinja2 logic, only `{{ config.project.name }}` variable in docstring
- All error handling uses graceful fallbacks to "unknown" values rather than failing
