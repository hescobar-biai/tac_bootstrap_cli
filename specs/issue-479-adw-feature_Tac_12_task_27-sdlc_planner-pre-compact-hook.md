# Feature: Create pre_compact.py Hook File

## Metadata
- **issue_number:** `479`
- **adw_id:** `feature_Tac_12_task_27`
- **task:** Task 27/49 - Wave 3: New Hooks

## Feature Description

Create a hook that captures context state before Claude Code performs context compaction. This hook logs pre-compaction metrics and context size information to enable observability and debugging of the compaction process.

The hook will run as part of Claude Code's lifecycle, reading JSON input from stdin, extracting session metadata, and appending structured log entries to a session-specific `pre_compact.json` file.

## User Story

As a Claude Code user
I want to track context state before compaction occurs
So that I can debug and analyze how context is being managed across sessions

## Problem Statement

When Claude Code compacts context to manage token usage, there's no observability into what state existed before compaction. This makes it difficult to:
- Debug context loss issues
- Understand compaction timing and frequency
- Track context size changes over session lifetime
- Correlate compaction events with other session activities

## Solution Statement

Create a `pre_compact.py` hook that:
1. Receives JSON input from Claude Code via stdin containing session and context information
2. Extracts session_id to identify the session
3. Creates/maintains a session-specific log directory
4. Appends pre-compaction data to a `pre_compact.json` array file
5. Logs gracefully even if input is malformed

The implementation follows established hook patterns in the codebase (similar to `stop.py` and `pre_tool_use.py`), using JSON array logging with proper error handling.

## Relevant Files

### Base Repository Files
- `.claude/hooks/pre_compact.py` - Base implementation (already exists and is complete)

### Template Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_compact.py.j2` - Jinja2 template for CLI generation

### Service Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Already registers `pre_compact.py` at line 349

### Reference Files
- `.claude/hooks/stop.py` - Similar logging hook pattern
- `.claude/hooks/pre_tool_use.py` - Similar JSON array logging pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2` - Reference template using `{{ config.paths.logs_dir }}`

## Implementation Plan

### Phase 1: Template Creation
Convert the base `pre_compact.py` into a Jinja2 template using `{{ config.paths.logs_dir }}` for path configuration, consistent with how `stop.py.j2` is structured.

### Phase 2: Integration Verification
Verify that:
- The hook is properly registered in `scaffold_service.py`
- The template file exists and has correct content
- No additional changes needed to scaffold service

### Phase 3: Testing
- Verify template syntax and Jinja2 rendering works correctly
- Ensure hook logic handles missing/malformed input gracefully
- Confirm JSON logging format matches established patterns

## Step by Step Tasks

### Task 1: Review and Understand Current State
- Read base implementation in `.claude/hooks/pre_compact.py`
- Review template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_compact.py.j2`
- Compare with `stop.py.j2` template pattern for consistency
- Verify hook is registered in `scaffold_service.py`

**Status:** Review in progress

### Task 2: Create/Update Jinja2 Template
- Convert base implementation to template format
- Replace hardcoded path logic with `{{ config.paths.logs_dir }}` variable
- Keep uv script shebang and JSON logging pattern
- Ensure consistent formatting with other hook templates

**Status:** Pending

### Task 3: Verify Integration
- Confirm `pre_compact.py` entry in `scaffold_service.py` hooks list
- Verify template path matches the registered hook name
- Check that template file is in correct location

**Status:** Pending

### Task 4: Run Validation Tests
- Execute all validation commands to ensure no regressions
- Verify scaffold still generates correctly
- Confirm no breaking changes to existing functionality

**Status:** Pending

## Testing Strategy

### Unit Tests
- Hook template renders without errors
- JSON logging array format is maintained
- Session log directory creation works correctly
- Error handling gracefully exits on all error conditions

### Edge Cases
- Malformed JSON input (should exit with code 0)
- Missing session_id in input (defaults to 'unknown')
- Pre-existing log files are appended to (not overwritten)
- Permission errors are handled gracefully

### Integration Tests
- New projects generated via CLI include the hook
- Hook appears in `.claude/hooks/` directory
- Hook has correct executable permissions

## Acceptance Criteria

✅ `pre_compact.py.j2` template file exists and is properly formatted
✅ Template uses `{{ config.paths.logs_dir }}` for path configuration
✅ Template maintains uv script format and JSON logging pattern
✅ Hook is registered in `scaffold_service.py` at line 349
✅ No changes needed to existing functionality
✅ All validation commands pass without errors
✅ Template generates correctly when scaffolding new projects
✅ Hook follows same error handling pattern as other hooks

## Validation Commands

Execute all commands in the `tac_bootstrap_cli/` directory to validate:

```bash
# Run all unit tests
uv run pytest tests/ -v --tb=short

# Check code quality
uv run ruff check .

# Type checking
uv run mypy tac_bootstrap/

# Test CLI generation (smoke test)
uv run tac-bootstrap --help

# Verify scaffold generates correctly
uv run tac-bootstrap scaffold --name test-project --output /tmp/test-project
```

All commands must pass with zero failures.

## Notes

- **Status:** Base implementation already exists and is complete - no changes needed
- **Template Pattern:** The base file uses `ensure_session_log_dir()` utility which is available to base hooks. The template will use `{{ config.paths.logs_dir }}` configuration variable for the same functionality, following the established pattern in `stop.py.j2`
- **Hook Behavior:** Pure logging hook - no threshold checking or warnings. Captures what's provided in input, lets Claude Code decide what matters
- **Error Handling:** All errors result in `sys.exit(0)` - hook fails silently to avoid breaking Claude Code workflow
- **JSON Format:** Uses JSON array format (append-only), consistent with `stop.py` and `pre_tool_use.py`
- **Dependencies:** No new dependencies required - uses only stdlib (json, sys, pathlib)
- **Wave Context:** Part of Wave 3 - New Hooks (Tasks 25-28)
