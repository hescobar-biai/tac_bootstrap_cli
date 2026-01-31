# Feature: Create send_event.py Observability Hook

## Metadata
issue_number: `472`
adw_id: `feature_Tac_12_task_20`
issue_json: `{"number": 472, "title": "[Task 20/49] [FEATURE] Create send_event.py hook file", "body": "## Description\n\nCreate observability hook that sends events to server.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/send_event.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2`\n\n## Key Features\n- HTTP POST to observability endpoint\n- Arguments: --source-app, --event-type, --server-url, --add-chat, --summarize\n- Integrates with summarizer.py and model_extractor.py\n- Always exits with 0 (non-blocking)\n\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/send_event.py`\n\n## Wave 3 - New Hooks (Task 20 of 9)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_20"}`

## Feature Description
Create a new observability hook `send_event.py` that sends event data to a remote observability server via HTTP POST. This hook enables centralized event tracking and monitoring for Claude Code sessions by forwarding hook events to a configurable endpoint. The hook must be non-blocking (always exit 0) to never interrupt Claude Code execution, even on network failures or server errors.

This is part of Wave 3 (New Hooks) in the TAC Bootstrap CLI implementation plan, specifically Task 20 of 49.

## User Story
As a TAC Bootstrap CLI user
I want to send observability events to a remote server
So that I can centrally monitor and analyze Claude Code session activity across multiple projects

## Problem Statement
TAC Bootstrap currently lacks centralized observability for Claude Code hooks and session events. Each project logs events locally, but there's no way to aggregate, analyze, or monitor events across projects. Teams need a way to send event data to a central observability platform for:
- Session tracking and debugging
- Usage analytics
- Error monitoring
- Audit trails

## Solution Statement
Implement a `send_event.py` hook that:
1. Reads event data from stdin (JSON format)
2. Enriches the payload with metadata (source_app, event_type, timestamp)
3. Sends the data via HTTP POST to a configurable observability endpoint
4. Supports optional authentication via Bearer token
5. Handles --add-chat and --summarize flags for future integration with summarizer utilities
6. Always exits with 0 to ensure non-blocking behavior
7. Uses stdlib urllib (no external dependencies) for HTTP requests

The implementation follows existing hook patterns (uv script, dotenv, session logging) and creates both the base hook file and Jinja2 template for CLI generation.

## Relevant Files
Files necessary for implementing the feature:

- `.claude/hooks/notification.py` - Reference for hook pattern (stdin, logging, exit 0)
- `.claude/hooks/post_tool_use.py` - Reference for session logging pattern
- `.claude/hooks/utils/constants.py` - Session log utilities
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2` - Template reference
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (lines 344-355) - Hooks list to update

### New Files
- `.claude/hooks/send_event.py` - Base observability hook implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2` - Jinja2 template for CLI

## Implementation Plan

### Phase 1: Foundation
1. Review existing hook patterns and HTTP communication requirements
2. Understand environment variable configuration (OBSERVABILITY_URL, OBSERVABILITY_TOKEN)
3. Identify session logging patterns from utils/constants.py

### Phase 2: Core Implementation
1. Create base `.claude/hooks/send_event.py` with:
   - Argument parser for --source-app, --event-type, --server-url, --add-chat, --summarize
   - stdin JSON reading and parsing
   - Payload enrichment with metadata
   - HTTP POST using urllib with 30s timeout
   - Bearer token authentication support
   - Error handling with stderr logging but exit(0)
   - Session logging for debugging
2. Create Jinja2 template `.../templates/claude/hooks/send_event.py.j2`
   - Mirror base file structure (templates currently don't use Jinja2 variables for hooks)

### Phase 3: Integration
1. Update `scaffold_service.py` hooks list to include send_event.py
2. Verify template is included in hook generation process

## Step by Step Tasks

### Task 1: Create Base Hook File
- Create `.claude/hooks/send_event.py` with uv script header
- Add dependencies: `python-dotenv` (following notification.py pattern)
- Implement argument parser with required flags
- Add stdin JSON reading with error handling
- Implement payload enrichment (source_app, event_type, timestamp)
- Add session logging using ensure_session_log_dir pattern
- Implement HTTP POST using urllib.request with:
  - 30 second timeout
  - Bearer token from OBSERVABILITY_TOKEN env var (if present)
  - Content-Type: application/json
  - Error handling (log to stderr, exit 0)
- Add stub logic for --add-chat and --summarize flags
- Ensure script always exits with 0

### Task 2: Create Jinja2 Template
- Copy base hook to `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2`
- Verify template follows existing hook template patterns (no Jinja2 variables needed based on existing templates)

### Task 3: Update Scaffold Service
- Add `("send_event.py", "Event observability hook")` to hooks list in scaffold_service.py (line 355)
- Verify hook will be included in generation process

### Task 4: Validation
- Run validation commands to ensure zero regressions
- Test base hook manually with sample stdin input
- Verify template is properly formatted

## Testing Strategy

### Unit Tests
No unit tests required for this task - hooks are standalone scripts. Manual testing will verify:
- Argument parsing works correctly
- stdin JSON is read and enriched properly
- HTTP POST is sent with correct headers
- Environment variables are read correctly
- Error handling exits with 0
- Session logging works

### Edge Cases
- Invalid JSON from stdin - should exit 0
- Missing OBSERVABILITY_URL - should exit 0 with error logged
- Network timeout - should exit 0 after 30s
- HTTP error responses (4xx, 5xx) - should exit 0
- Missing optional OBSERVABILITY_TOKEN - should work without auth header
- --add-chat with no conversation data in stdin - should handle gracefully
- --summarize flag - should be placeholder for now

## Acceptance Criteria
1. Base hook file `.claude/hooks/send_event.py` exists and is executable
2. Hook accepts all required arguments: --source-app, --event-type, --server-url, --add-chat, --summarize
3. Hook reads JSON from stdin and enriches with metadata
4. Hook sends HTTP POST to configurable endpoint with 30s timeout
5. Hook supports optional Bearer token authentication via env var
6. Hook logs errors to stderr but always exits with 0
7. Hook writes session log for debugging
8. Jinja2 template created at correct path
9. scaffold_service.py includes send_event.py in hooks list
10. All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- Manual test: `echo '{"test":"data"}' | .claude/hooks/send_event.py --source-app test --event-type test_event --server-url http://localhost:8000/events`

## Notes
- Uses stdlib urllib (no additional dependencies beyond python-dotenv)
- HTTP timeout is hardcoded to 30s (reasonable for non-blocking hook)
- --add-chat and --summarize are implemented as placeholders for future integration
- Server URL priority: --server-url argument > OBSERVABILITY_URL env var
- Authentication is optional - works with or without token
- Hook is non-blocking by design - critical for not interrupting Claude Code execution
- Pattern follows existing hooks: notification.py and post_tool_use.py
- Templates in this codebase don't use Jinja2 variables for hooks - they're static copies
