---
doc_type: feature
adw_id: feature_Tac_12_task_28
date: 2026-01-31
idk:
  - prompt-logging
  - hook-execution
  - session-isolation
  - append-only-json
  - validation-framework
  - graceful-error-handling
tags:
  - feature
  - hooks
  - logging
  - validation
related_code:
  - .claude/hooks/user_prompt_submit.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# User Prompt Submit Hook

**ADW ID:** feature_Tac_12_task_28
**Date:** 2026-01-31
**Specification:** issue-480-adw-feature_Tac_12_task_28-sdlc_planner-user-prompt-submit-hook.md

## Overview

Created a Python hook that logs user prompts to JSON files in session-specific directories. This hook executes when users submit prompts to Claude Code, providing audit trails and enabling optional prompt validation. The implementation includes both a base hook file and a Jinja2 template for CLI-based project generation.

## What Was Built

- **Base hook implementation** (`.claude/hooks/user_prompt_submit.py`) - Reads JSON from stdin and appends prompts to session-specific log files
- **Jinja2 template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2`) - Ready for template-based code generation
- **Scaffold integration** - Hook registered in `scaffold_service.py` for inclusion in generated projects
- **Append-only JSON logging** - Maintains historical record of all prompts without data loss
- **Optional validation framework** - Extensible pattern-based validation with `--validate` flag
- **Graceful error handling** - Non-blocking logging that never interrupts user workflows

## Technical Implementation

### Files Modified

- `.claude/hooks/user_prompt_submit.py` - Core hook implementation with prompt logging, validation, and error handling
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2` - Jinja2 template version (functionally identical to base file)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Added hook registration at line 351

### Key Changes

- **JSON input parsing**: Reads structured data from stdin with required `session_id` and `prompt` fields
- **Session-based file organization**: Logs stored at `.claude/hooks/logs/{session_id}/user_prompt_submit.json`
- **Append-only pattern**: Each invocation reads existing JSON, appends new entry, and writes back with pretty formatting
- **Validation with extensible patterns**: Empty `blocked_patterns` list by default; can be customized with string tuples for matching and reason
- **Non-blocking exit strategy**: Always exits with code 0 (success) to allow prompt processing; validation failures exit with code 2 but only when `--validate` flag is used

## How to Use

### Basic Usage

The hook reads JSON input from stdin:

```json
{
  "session_id": "session-12345",
  "prompt": "Write a Python function",
  "metadata": {}
}
```

Invoke the hook with a command like:

```bash
echo '{"session_id": "my-session", "prompt": "Hello"}' | .claude/hooks/user_prompt_submit.py
```

### With Validation

Enable prompt validation with the `--validate` flag:

```bash
echo '{"session_id": "my-session", "prompt": "rm -rf /"}' | .claude/hooks/user_prompt_submit.py --validate
```

If a blocked pattern matches, the hook exits with code 2 and prints error to stderr.

### Log-Only Mode

Skip validation and only log prompts:

```bash
.claude/hooks/user_prompt_submit.py --log-only
```

## Configuration

### Validation Patterns

Edit the `blocked_patterns` list in the hook file to add custom validation rules:

```python
blocked_patterns = [
    ('rm -rf /', 'Dangerous command detected'),
    ('DROP TABLE', 'SQL injection detected'),
]
```

Patterns use case-insensitive substring matching.

### Session Logging

Logs are stored at:
```
.claude/hooks/logs/{session_id}/user_prompt_submit.json
```

Each entry in the JSON array contains:
```json
{
  "session_id": "string",
  "prompt": "string",
  "metadata": {}
}
```

## Testing

### Verify Hook Exists and is Executable

```bash
ls -la .claude/hooks/user_prompt_submit.py
```

### Test Basic Logging

```bash
mkdir -p .claude/hooks/logs/test-session
echo '{"session_id": "test-session", "prompt": "test prompt"}' | .claude/hooks/user_prompt_submit.py
cat .claude/hooks/logs/test-session/user_prompt_submit.json
```

### Test Validation

```bash
echo '{"session_id": "test-session", "prompt": "rm -rf /"}' | .claude/hooks/user_prompt_submit.py --validate
echo $?  # Should be 0 (success) since blocked_patterns is empty by default
```

### Test Template Rendering

```bash
grep -n "user_prompt_submit" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

The hook should appear as an available scaffold option in generated projects.

## Notes

### Design Decisions

1. **Append-only logging**: Ensures complete audit trail without overwriting previous entries
2. **Exit code 0 always**: Prevents logging failures from blocking user sessions; validation failures only exit 2 when explicitly enabled
3. **Graceful degradation**: Invalid JSON or filesystem errors are caught and don't crash the hook
4. **Empty blocked_patterns by default**: Validates are opt-in; users customize patterns as needed
5. **Session isolation**: Each session gets its own log directory for better organization and analysis

### Future Enhancements

- Add `--store-last-prompt` flag to persist only the most recent prompt
- Add `--name-agent` flag to identify which agent submitted the prompt
- Implement log rotation to prevent unbounded file growth
- Add sensitive data filtering (tokens, credentials, API keys)
- Support external configuration files instead of in-code patterns
