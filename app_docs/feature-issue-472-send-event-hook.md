---
doc_type: feature
adw_id: feature_Tac_12_task_20
date: 2026-01-30
idk:
  - observability
  - hooks
  - event-tracking
  - http-post
  - session-management
  - urllib
  - non-blocking
  - monitoring
tags:
  - feature
  - hooks
  - observability
related_code:
  - .claude/hooks/send_event.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Send Event Observability Hook

**ADW ID:** feature_Tac_12_task_20
**Date:** 2026-01-30
**Specification:** specs/issue-472-adw-feature_Tac_12_task_20-sdlc_planner-send-event-hook.md

## Overview

Implemented a new `send_event.py` hook that enables centralized observability by sending Claude Code session events to a remote server via HTTP POST. The hook is designed to be non-blocking (always exits with code 0) to ensure it never interrupts Claude Code execution, even during network failures or server errors.

## What Was Built

- **Base Hook Implementation**: `.claude/hooks/send_event.py` - A standalone Python script using urllib for HTTP communication
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2` - Template for generating the hook in scaffolded projects
- **Scaffold Integration**: Updated `scaffold_service.py` to include send_event.py in the hooks list for automatic generation

## Technical Implementation

### Files Modified

- `.claude/hooks/send_event.py`: New executable hook script (138 lines) with:
  - Argument parser for `--source-app`, `--event-type`, `--server-url`, `--add-chat`, `--summarize`
  - stdin JSON reading and payload enrichment
  - HTTP POST using stdlib urllib with 30s timeout
  - Bearer token authentication support
  - Session logging for local debugging
  - Comprehensive error handling with guaranteed exit 0

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2`: Identical copy of base hook for template generation

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (line 355): Added `("send_event.py", "Event observability hook")` to hooks list

### Key Changes

- **Non-blocking Design**: All error paths exit with code 0 to prevent interrupting Claude Code workflows
- **Payload Enrichment**: Adds source_app, event_type, and UTC timestamp to incoming JSON data
- **Authentication**: Supports optional Bearer token via `OBSERVABILITY_TOKEN` environment variable
- **Session Logging**: Writes events to session-specific log files using `ensure_session_log_dir` pattern
- **URL Priority**: `--server-url` argument overrides `OBSERVABILITY_URL` environment variable
- **Graceful Degradation**: Missing server URL logs warning but doesn't fail; network errors are logged to stderr
- **Future Integration**: Placeholder flags `--add-chat` and `--summarize` for integration with conversation summarization utilities

## How to Use

### Basic Usage

1. Set the observability server URL (optional authentication token):
```bash
export OBSERVABILITY_URL="https://your-observability-server.com/events"
export OBSERVABILITY_TOKEN="your-bearer-token"  # Optional
```

2. Send an event via stdin:
```bash
echo '{"session_id": "abc123", "tool": "bash", "command": "ls"}' | \
  .claude/hooks/send_event.py \
  --source-app my-project \
  --event-type tool_use
```

3. Override server URL via argument:
```bash
echo '{"test": "data"}' | \
  .claude/hooks/send_event.py \
  --source-app test-app \
  --event-type test_event \
  --server-url http://localhost:8000/events
```

### Integration with Claude Code Hooks

The hook is designed to be called from other hooks via the hook system:

```json
{
  "hooks": {
    "after_tool_use": ".claude/hooks/send_event.py --source-app my-project --event-type tool_use"
  }
}
```

## Configuration

### Environment Variables

- `OBSERVABILITY_URL` (optional): Default server endpoint for event submissions
- `OBSERVABILITY_TOKEN` (optional): Bearer token for authentication

### Command Line Arguments

- `--source-app` (required): Name of the source application
- `--event-type` (required): Type of event being sent (e.g., "tool_use", "session_start")
- `--server-url` (optional): Override the server URL from environment
- `--add-chat` (flag): Placeholder for including conversation data in events
- `--summarize` (flag): Placeholder for summarizing event data before sending

### HTTP Request Details

- **Method**: POST
- **Timeout**: 30 seconds
- **Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <token>` (if OBSERVABILITY_TOKEN is set)
- **Payload**: Enriched JSON with source_app, event_type, timestamp, and original data

## Testing

### Manual Testing

Test with a local server:
```bash
echo '{"session_id": "test123", "message": "hello"}' | \
  .claude/hooks/send_event.py \
  --source-app test \
  --event-type manual_test \
  --server-url http://localhost:8000/events
```

Test error handling (missing server URL):
```bash
unset OBSERVABILITY_URL
echo '{"test": "data"}' | \
  .claude/hooks/send_event.py \
  --source-app test \
  --event-type test_event
```

### Validation Suite

Run the full validation suite:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check linting:
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Type checking:
```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

CLI smoke test:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Non-blocking Guarantee**: The hook is designed to NEVER fail Claude Code execution. All error paths exit with 0.
- **Stdlib Only**: Uses Python's built-in urllib (no external HTTP libraries) to minimize dependencies
- **Session Logging**: Events are logged locally to `.claude/session_logs/<session_id>/send_event.json` for debugging
- **Future Extensibility**: `--add-chat` and `--summarize` flags are placeholders for future integration with summarizer.py and conversation data
- **Security**: Bearer token authentication is optional but recommended for production use
- **Network Resilience**: 30s timeout prevents hung connections; URLError and HTTPError are caught and logged
- **Template Pattern**: Follows existing hook patterns (notification.py, post_tool_use.py) for consistency
