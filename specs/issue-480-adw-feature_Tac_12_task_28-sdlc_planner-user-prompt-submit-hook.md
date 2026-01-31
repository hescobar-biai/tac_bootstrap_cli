# Feature: Create user_prompt_submit.py Hook File

## Metadata
- **issue_number**: `480`
- **adw_id**: `feature_Tac_12_task_28`
- **issue_json**: Task 28 - Create user_prompt_submit.py hook file
- **status**: COMPLETE

## Feature Description

This hook runs when users submit prompts to Claude Code. It provides:
- **Prompt logging**: Appends all submitted prompts to a session-specific JSON log file
- **Optional validation**: Validates prompts against configurable patterns
- **User interaction tracking**: Captures session ID, prompt text, and metadata
- **Graceful error handling**: Ensures logging failures don't block user workflows

## User Story

As a Claude Code agent developer,
I want to log all user prompts submitted during a session,
So that I can audit user interactions, debug workflows, and track agent behavior.

## Problem Statement

Agents need visibility into user interactions within a session. Without prompt logging, there's no audit trail of what users submitted, making debugging and analysis difficult.

## Solution Statement

Create a hook that:
1. Reads JSON input from stdin containing session_id and prompt
2. Appends each prompt to a session-specific append-only JSON log
3. Optionally validates prompts against blocked patterns
4. Exits with code 0 to allow prompt processing regardless of logging status
5. Fails gracefully without blocking user workflows

## Relevant Files

### Existing Implementation Files
- `.claude/hooks/user_prompt_submit.py` - Base hook implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2` - Jinja2 template
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Scaffold service (line 351)

### Related Files
- `.claude/hooks/utils/constants.py` - Session log directory utilities
- `.claude/settings.json` - Hook configuration
- `PLAN_TAC_BOOTSTRAP.md` - Main implementation plan

## Implementation Status

### ✅ COMPLETE

#### Deliverables Completed:
1. **Base Hook File** (`.claude/hooks/user_prompt_submit.py`)
   - Reads JSON input from stdin
   - Extracts session_id and prompt
   - Logs to session-specific directory using `ensure_session_log_dir()`
   - Implements `validate_prompt()` with extensible blocked_patterns
   - Supports `--validate` and `--log-only` flags
   - Graceful error handling with exit code 0

2. **Jinja2 Template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2`)
   - Functionally identical to base file
   - Ready for CLI generation with template variables

3. **Scaffold Integration** (`scaffold_service.py` line 351)
   - Hook registered in scaffolding service
   - Description: "User prompt validation and logging"
   - Will be included in generated projects

## Key Features (Implemented)

- **Append-only logging**: Maintains historical record in JSON format
- **Session isolation**: Each session has its own log directory
- **Optional validation**: `--validate` flag enables blocked pattern checking
- **Log-only mode**: `--log-only` flag skips blocking even if validation fails
- **Error tolerance**: Exit code 0 allows prompt submission even if logging fails
- **Flexible input schema**: Accepts `session_id` (required), `prompt` (required), and arbitrary metadata

## Features (Not Yet Implemented)

These can be added in future iterations if needed:
- **`--store-last-prompt`**: Persist only the most recent prompt to separate file
- **`--name-agent`**: Add `agent_name` field to logged JSON entries

## Architecture

### Input Schema
```json
{
  "session_id": "string (required)",
  "prompt": "string (required)",
  "metadata": "object (optional)"
}
```

### Log File Format
```
.claude/hooks/logs/{session_id}/user_prompt_submit.json
```

Array of prompt entries:
```json
[
  {"session_id": "...", "prompt": "...", ...metadata},
  {"session_id": "...", "prompt": "...", ...metadata}
]
```

## Validation Framework

The hook includes extensible validation:
```python
blocked_patterns = [
    # Add patterns to block, e.g.:
    # ('rm -rf /', 'Dangerous command detected'),
]
```

Empty by default (opt-in behavior).

## Testing Strategy

### Unit Tests
- Test JSON parsing from stdin
- Test log file creation and appending
- Test validation with empty blocked_patterns
- Test validation with sample blocked patterns
- Test error handling for invalid JSON
- Test filesystem error handling

### Integration Tests
- Test hook invocation via settings.json
- Test log directory creation
- Test session isolation
- Test flag combinations (--validate + --log-only)

### Edge Cases
- Missing session_id field (defaults to 'unknown')
- Missing prompt field (defaults to empty string)
- Corrupted log file (reinitialize as empty array)
- Filesystem write failures (exit 0, fail silently)
- Invalid JSON input (exit 0, fail silently)

## Acceptance Criteria

- [x] Base hook file exists and is executable
- [x] Template file exists and matches base file
- [x] Hook is registered in scaffold_service.py
- [x] Prompt logging works with append-only JSON
- [x] `--validate` flag functions correctly
- [x] `--log-only` flag disables blocking
- [x] Error handling prevents blocking user workflows
- [x] Session-based log isolation works
- [x] Hook integrates with settings.json

## Notes

### Design Decisions
1. **Append-only logging**: Ensures complete audit trail without data loss
2. **Exit code 0 always**: Hooks should not interrupt user sessions even if logging fails
3. **Graceful degradation**: Invalid JSON or filesystem errors don't throw exceptions
4. **Flexible validation**: Empty blocked_patterns allows users to customize via environment variables or editing
5. **Session isolation**: Logs are stored per-session for better organization and analysis

### Future Enhancements
- Add `--store-last-prompt` for tracking most recent prompt only
- Add `--name-agent` to identify which agent submitted the prompt
- Add configuration file for blocked_patterns instead of in-code list
- Implement log rotation to prevent unbounded growth
- Add filtering for sensitive data (tokens, credentials)

### Dependencies
- `python-dotenv` (optional, for .env file support)
- `pathlib.Path` (stdlib)
- `json` (stdlib)
- `.claude/hooks/utils/constants.py` (internal utility)

## Validation Commands

All validation passed:

```bash
# Verify hook exists
ls -la .claude/hooks/user_prompt_submit.py

# Verify template exists
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2

# Verify scaffold integration
grep -n "user_prompt_submit" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

# Run tests (if test suite exists)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Type check
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Linting
cd tac_bootstrap_cli && uv run ruff check .
```

## Summary

**Status**: Task 28 is COMPLETE. Both the base hook file and Jinja2 template exist and are functionally correct. The hook is properly integrated into the scaffold service and ready for use. The implementation covers all core requirements: prompt logging, optional validation, user interaction tracking, and graceful error handling.

No breaking changes or refactoring needed. Optional enhancements (--store-last-prompt, --name-agent flags) can be added in future iterations without affecting existing functionality.
