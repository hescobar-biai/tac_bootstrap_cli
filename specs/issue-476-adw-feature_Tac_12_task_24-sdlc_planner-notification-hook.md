# Feature: Create notification.py Hook File

## Metadata
issue_number: `476`
adw_id: `feature_Tac_12_task_24`
issue_json: `{"number": 476, "title": "[Task 24/49] [FEATURE] Create notification.py hook file", "body": "## Description\ncron-enabled\nCreate a hook for system notifications.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/notification.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2`\n\n## Key Features\n- System notification handling\n- Event logging\n\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/notification.py`\n\n## Wave 3 - New Hooks (Task 24 of 9)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_24"}`

## Feature Description
This task is part of Wave 3 - New Hooks in the TAC Bootstrap project. The notification.py hook provides a cross-platform system notification and event logging mechanism for Claude Code sessions. The hook captures notification events, logs them to session-specific JSON files, and maintains an audit trail of all notifications during a coding session.

**Current Status**: The feature is already implemented. Both the base file (`.claude/hooks/notification.py`) and the Jinja2 template (`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2`) already exist and are functionally complete. The hook is already registered in `scaffold_service.py` line 348 and configured in `.claude/settings.json` lines 56-66.

## User Story
As a TAC Bootstrap CLI user
I want notification events to be automatically captured and logged during my Claude Code sessions
So that I have an audit trail of all system notifications and can debug or review notification-related issues

## Problem Statement
Claude Code generates various notification events during agent sessions (task completions, errors, warnings, etc.). Without proper logging infrastructure, these events are ephemeral and cannot be reviewed later. Users need a lightweight, cross-platform mechanism to capture and persist notification events for debugging, auditing, and session recovery purposes.

## Solution Statement
The notification.py hook implements a JSON-based event logging system that:
1. Receives notification events via stdin as JSON
2. Logs events to session-specific files at `logs/session_{session_id}/notification.json`
3. Uses stdlib-only dependencies (json, sys, os, pathlib, argparse) plus optional python-dotenv
4. Fails gracefully with sys.exit(0) to never block user workflows
5. Integrates with universal_hook_logger.py for cross-hook event tracking
6. Is configured in settings.json as a Notification hook

## Relevant Files
Files necessary for implementing the feature:

**Existing Implementation (Already Complete)**:
- `.claude/hooks/notification.py` - Base hook implementation (73 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2` - Jinja2 template (74 lines, identical to base)
- `.claude/settings.json` - Hook configuration with Notification hook entry (lines 56-66)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Hook registration in _add_claude_files (line 348)

**Related Files**:
- `.claude/hooks/utils/constants.py` - Provides ensure_session_log_dir() function used by hook
- `.claude/hooks/universal_hook_logger.py` - Universal event logger called alongside notification.py
- `.claude/hooks/stop.py` - Similar hook pattern for reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Settings template with hook configuration

### New Files
None - all required files already exist

## Implementation Plan

### Phase 1: Verification
Verify that the existing implementation meets all requirements specified in the issue

### Phase 2: Documentation
Add inline documentation comments if needed to clarify hook behavior

### Phase 3: Testing
Validate the hook works correctly in both base repository and generated projects

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Existing Implementation
- Read `.claude/hooks/notification.py` and confirm it implements required features
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2` and verify template is correct
- Check `.claude/settings.json` confirms hook is configured under Notification event (lines 56-66)
- Check `scaffold_service.py` confirms notification.py is in hooks list (line 348)
- Verify hook follows established patterns (fail silently, exit 0, JSON logging)

### Task 2: Verify Cross-Platform Compatibility
- Confirm hook uses only stdlib dependencies: json, sys, os, pathlib, argparse
- Confirm python-dotenv is optional and gracefully skipped if missing
- Verify no OS-specific notification calls are made
- Check that ensure_session_log_dir() import is correct

### Task 3: Verify Settings Integration
- Read `.claude/settings.json` and confirm Notification hook configuration
- Verify hook is called with `--notify` flag
- Confirm universal_hook_logger.py is also called for Notification events
- Check that `|| true` ensures hook never blocks workflow

### Task 4: Verify Template Consistency
- Compare base file with template file to ensure they are functionally identical
- Verify template imports from utils.constants (not hardcoded paths)
- Check that no Jinja2 variables are needed (hook is project-agnostic)

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions

## Testing Strategy

### Unit Tests
Since the hook is already implemented and uses stdlib-only dependencies:
- Test hook with valid JSON input via stdin
- Test hook with invalid JSON (should exit 0 gracefully)
- Test hook with missing session_id (should use 'unknown')
- Test that log files are created in correct location
- Test that multiple events append to same log file
- Test that --notify flag is parsed correctly

### Edge Cases
- Empty JSON input
- Missing session_id in JSON
- Non-existent log directory (should be created)
- Corrupted existing log file (should reinitialize)
- Permission errors writing to log file (should exit 0)
- Very large JSON input

## Acceptance Criteria
- Base hook file exists at `.claude/hooks/notification.py` with executable permissions
- Template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2`
- Hook is registered in scaffold_service.py hooks list (line 348: `("notification.py", "Notification logging")`)
- Hook is configured in settings.json under Notification event (lines 56-66)
- Hook uses only stdlib dependencies (json, sys, os, pathlib, argparse) plus optional python-dotenv
- Hook logs to session-specific files: `logs/session_{session_id}/notification.json`
- Hook fails silently with sys.exit(0) on all errors
- Hook parses `--notify` flag correctly
- Hook appends to existing log files or creates new ones
- Template imports from utils.constants for ensure_session_log_dir()
- All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `uv run .claude/hooks/notification.py --notify < test_notification.json` - Manual hook test (optional)

## Notes

**Implementation Already Complete**: This task appears to be already fully implemented. All three required changes are done:
1. Base hook file exists: `.claude/hooks/notification.py`
2. Jinja2 template exists: `notification.py.j2`
3. scaffold_service.py includes hook in list: line 348

**Auto-Resolved Clarifications Summary**: The clarifications confirm that:
- The hook uses JSON logging (no OS-level notifications)
- It's a generic notification framework (not tied to specific events)
- Session-specific JSON files are used for logging
- Cross-platform stdlib-only implementation
- No template variables needed (imports from utils.constants)
- Integrates via settings.json Notification hook
- Fails silently to avoid blocking workflows
- Already user-configurable via settings.json
- Uses stdlib + optional python-dotenv only
- Reference file not needed (implementation already exists)

**Next Steps**: Since the implementation is complete, the primary task is verification and validation. If any issues are found during verification, they should be documented and fixed. Otherwise, this task can be marked as complete after running validation commands.

**Hook Pattern**: This hook follows the established pattern used by other hooks:
- Receives JSON via stdin
- Logs to session-specific directory
- Uses ensure_session_log_dir() from utils.constants
- Fails silently with exit 0
- Called by universal_hook_logger.py
- Configured in settings.json with `|| true` to prevent blocking

**Cron-Enabled**: The issue description mentions "cron-enabled" which likely refers to the automated workflow triggers in the ADW system, not traditional cron jobs. The hook itself is event-driven via Claude Code's hook system.
