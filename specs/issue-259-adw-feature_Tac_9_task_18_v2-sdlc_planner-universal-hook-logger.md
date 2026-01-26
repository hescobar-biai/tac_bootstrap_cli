# Feature: Universal Hook Logger Template

## Metadata
issue_number: `259`
adw_id: `feature_Tac_9_task_18_v2`
issue_json: `{"number":259,"title":"Add universal_hook_logger.py.j2 hook template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_18_v2\n\n**Description:**\nCreate Jinja2 template for universal hook logger. Provides comprehensive logging across all Claude Code hook events.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/universal_hook_logger.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/universal_hook_logger.py` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for a universal hook logger that provides comprehensive audit trail of all Claude Code tool executions. This hook will log all post_tool_use events across ALL tools (Read, Write, Edit, NotebookEdit, Bash, Grep, Glob, WebFetch, etc.) to session-specific JSONL files, enabling debugging, compliance tracking, and workflow analysis.

The logger follows the established context_bundle_builder pattern with key differences:
- **Scope**: Logs ALL tools (not just file operations)
- **Data captured**: Tool name, sanitized inputs/outputs, timestamp, session_id, status
- **Security**: Sanitizes sensitive data (credentials, full file contents, environment variables)
- **Reliability**: Always fails silently (stderr + exit 0) to never block workflows

## User Story
As a TAC Bootstrap user
I want to generate a universal hook logger in target projects
So that I can track all Claude Code tool executions for debugging, auditing, and workflow analysis without blocking agent operations

## Problem Statement
While context_bundle_builder tracks file operations, there is no comprehensive logging mechanism for ALL Claude Code tool executions. Users need visibility into:
- Which tools agents are using and when
- What parameters were passed to tools
- Success/failure status of operations
- Complete audit trail for compliance and debugging

Current limitations:
- context_bundle_builder only logs file operations (Read, Write, Edit, NotebookEdit)
- No logging for Bash, Grep, Glob, WebFetch, Task, and other tools
- No centralized audit trail across all agent actions
- Difficult to debug complex workflows or understand agent behavior

## Solution Statement
Create a Jinja2 template `universal_hook_logger.py.j2` that generates a post_tool_use hook logging ALL tool executions to session-specific JSONL files at `{{ config.paths.logs_dir }}/universal_hook_logs/session_{session_id}.jsonl`.

Key design decisions:
1. **Universal coverage**: Log ALL tools, not selective filtering
2. **Security-first sanitization**: Strip credentials, truncate large payloads, track metadata only
3. **Fail-silent philosophy**: Always exit 0, log errors to stderr, never block workflows
4. **Session isolation**: One JSONL file per session for parallel safety
5. **Simple implementation**: No log rotation, no dynamic levels, no buffering - YAGNI principle

JSONL schema per entry:
```json
{
  "timestamp": "2024-01-26T14:30:45.123456",
  "session_id": "uuid-string",
  "tool_name": "Bash|Read|Write|...",
  "tool_input": {...},  // sanitized metadata only
  "tool_response": {...},  // sanitized metadata only
  "status": "success|error"
}
```

## Relevant Files
Files necessary for implementing this feature:

### Existing Templates (Reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2` - Reference pattern for sanitization, error handling, JSONL writing
- `.claude/hooks/context_bundle_builder.py` - Rendered example of similar hook

### Source Reference (External)
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/universal_hook_logger.py` - Original implementation to adapt

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2` (CREATE) - Main Jinja2 template
- `.claude/hooks/universal_hook_logger.py` (CREATE - rendered for testing)

## Implementation Plan

### Phase 1: Foundation
1. Study context_bundle_builder.py.j2 template structure
2. Identify reusable patterns: error handling, JSONL writing, path sanitization
3. Define sanitization rules for each tool type
4. Design JSONL schema for universal logging

### Phase 2: Core Implementation
1. Create universal_hook_logger.py.j2 template with:
   - Jinja2 variable substitution: `{{ config.paths.logs_dir }}`
   - Universal tool handling (no filtering by tool_name)
   - Comprehensive sanitization functions per tool type
   - Session-specific JSONL file writing
   - Fail-silent error handling (always exit 0)

2. Implement sanitization strategy:
   - **Bash**: Log command string (truncate if > 500 chars), exclude environment variables
   - **Read/Write/Edit**: Log file_path + metadata (lengths, offsets), exclude content
   - **Grep/Glob**: Log patterns, paths, exclude full results
   - **WebFetch**: Log URL, exclude response body
   - **Task**: Log prompt (truncated), subagent_type, exclude full context
   - **All tools**: Exclude any field matching credential patterns

3. Follow context_bundle_builder patterns:
   - `make_path_relative()` for file paths
   - `write_log_entry()` for atomic JSONL appends
   - `get_operation_status()` for success/error detection
   - Exception handling: catch-all with stderr logging + exit 0

### Phase 3: Integration
1. Render template to `.claude/hooks/universal_hook_logger.py` for testing
2. Validate JSONL output format
3. Test error handling (malformed input, disk full, permission denied)
4. Verify fail-silent behavior (always exit 0)

## Step by Step Tasks

### Task 1: Study Reference Patterns
- Read `context_bundle_builder.py.j2` template in detail
- Extract reusable patterns for:
  - Error handling philosophy (fail-silent)
  - JSONL writing (atomic appends)
  - Path sanitization (relative paths)
  - Template variable usage (`{{ config.* }}`)
- Document sanitization approach for file operations

### Task 2: Define Sanitization Rules
- Create sanitization specification for each tool:
  - Bash: command (truncate 500 chars), timeout, exclude env vars
  - Read: file_path, offset, limit (no content)
  - Write: file_path, content_length (no content)
  - Edit: file_path, old_string_length, new_string_length, replace_all (no strings)
  - NotebookEdit: notebook_path, cell_id, cell_type, edit_mode (no source)
  - Grep: pattern, path, output_mode, glob (no results)
  - Glob: pattern, path (no results)
  - WebFetch: url (no prompt, no response)
  - Task: subagent_type, description (prompt truncated to 200 chars)
  - All: detect and exclude credential patterns (API keys, tokens, passwords)

### Task 3: Create Template Structure
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2`
- Add docstring explaining:
  - Purpose: Universal logging of all tool executions
  - Log location: `{{ config.paths.logs_dir }}/universal_hook_logs/session_{session_id}.jsonl`
  - JSONL schema
  - Error handling philosophy (fail-silent)
- Add imports: json, os, sys, datetime, pathlib, re (for credential detection)

### Task 4: Implement Helper Functions
- `sanitize_tool_input(tool_name: str, tool_input: dict) -> dict` - Return sanitized metadata
- `sanitize_tool_response(tool_name: str, tool_response: dict) -> dict` - Return sanitized metadata
- `detect_credentials(value: str) -> bool` - Detect API keys, tokens, passwords using regex
- `make_path_relative(file_path: str) -> str` - Reuse from context_bundle_builder
- `get_operation_status(tool_response: dict) -> str` - Return "success" or "error"
- `write_log_entry(session_id: str, log_entry: dict) -> None` - Atomic JSONL append

### Task 5: Implement Main Handler
- `handle_tool_execution(input_data: dict) -> None`:
  - Extract session_id, tool_name, tool_input, tool_response from stdin JSON
  - Sanitize tool_input and tool_response
  - Determine operation status
  - Build log_entry dict with timestamp, session_id, tool_name, sanitized data, status
  - Call write_log_entry()
  - All exceptions caught and logged to stderr (never raise)

### Task 6: Implement Main Entry Point
- `main()` function:
  - Read JSON from stdin
  - Call handle_tool_execution()
  - Catch JSONDecodeError, IOError, all exceptions
  - Always exit 0 (never block workflows)
  - Log errors to stderr

### Task 7: Render and Test Template
- Use Jinja2 to render template with test config:
  - `config.paths.logs_dir = "logs"`
  - `config.project.name = "tac-bootstrap"`
- Write rendered output to `.claude/hooks/universal_hook_logger.py`
- Make hook executable: `chmod +x .claude/hooks/universal_hook_logger.py`
- Validate Python syntax: `python -m py_compile .claude/hooks/universal_hook_logger.py`

### Task 8: Validate Sanitization
- Review sanitization functions for each tool type
- Ensure no credentials, full file contents, or sensitive data logged
- Verify truncation of large payloads (commands > 500 chars, prompts > 200 chars)
- Test credential detection regex against sample patterns

### Task 9: Test Error Handling
- Test with malformed JSON input (should log to stderr, exit 0)
- Test with missing session_id (should use "unknown", exit 0)
- Test with unwritable log directory (should log to stderr, exit 0)
- Verify hook never exits with non-zero code

### Task 10: Run Validation Commands
- Execute all validation commands (see Validation Commands section)
- Fix any linting, type checking, or test failures
- Ensure zero regressions

## Testing Strategy

### Unit Tests
Create `tac_bootstrap_cli/tests/templates/test_universal_hook_logger.py`:

1. **Test sanitization functions**:
   - `test_sanitize_bash_input()` - Verify command truncation, env var exclusion
   - `test_sanitize_read_input()` - Verify file_path preserved, content excluded
   - `test_sanitize_write_input()` - Verify content_length tracked, content excluded
   - `test_sanitize_edit_input()` - Verify string lengths tracked, strings excluded
   - `test_sanitize_grep_input()` - Verify pattern preserved, results excluded
   - `test_detect_credentials()` - Verify API key, token, password detection

2. **Test JSONL writing**:
   - `test_write_log_entry_creates_directory()` - Verify directory creation
   - `test_write_log_entry_appends_jsonl()` - Verify atomic append
   - `test_write_log_entry_handles_io_error()` - Verify graceful failure

3. **Test error handling**:
   - `test_malformed_json_input()` - Should log to stderr, exit 0
   - `test_missing_session_id()` - Should use "unknown", exit 0
   - `test_unwritable_log_dir()` - Should log to stderr, exit 0

### Integration Tests
Manual validation:
1. Render template with sample config
2. Run hook with sample post_tool_use input for each tool type
3. Verify JSONL output correctness
4. Verify no sensitive data leaked
5. Verify hook always exits 0

### Edge Cases
- Empty tool_input or tool_response
- Tool_name not in known tools (should still log)
- Extremely long command strings (> 10KB)
- Unicode in file paths or commands
- Concurrent writes to same JSONL file (session isolation)
- Disk full during write (should fail silently)

## Acceptance Criteria
1. Template file created: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2`
2. Template renders valid Python 3.10+ code with Jinja2 variables substituted
3. Rendered hook logs ALL tool executions to session-specific JSONL files
4. JSONL schema includes: timestamp, session_id, tool_name, sanitized tool_input, sanitized tool_response, status
5. Sanitization rules implemented for all tool types (no credentials, no full content)
6. Hook always exits 0 (never blocks workflows)
7. Errors logged to stderr with descriptive messages
8. Log files written to `{{ config.paths.logs_dir }}/universal_hook_logs/session_{session_id}.jsonl`
9. All validation commands pass with zero errors
10. Unit tests achieve >90% code coverage for sanitization and error handling

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Security Considerations
- **Credential detection**: Use regex to detect patterns like `API_KEY=`, `token:`, `password=`, base64-encoded strings
- **Truncation limits**: Commands 500 chars, prompts 200 chars, other strings 1000 chars
- **Exclusion list**: Never log environment variables, full file contents, raw WebFetch responses
- **Path sanitization**: Always convert to relative paths to avoid leaking system structure

### Performance Considerations
- Post-tool-use hooks run after tool completion (not in critical path)
- Synchronous JSONL appends are fast enough (<1ms per write)
- No buffering to avoid data loss on crashes
- Session-specific files prevent lock contention

### Future Enhancements (Out of Scope)
- Log rotation policies (can be added later if needed)
- Dynamic log levels (INFO, DEBUG, etc.)
- Structured query interface for JSONL logs
- Integration with observability platforms (Datadog, Grafana)
- Log compression for long-running sessions

### Compatibility
- Python 3.10+ (uses `str | None` type hints)
- No external dependencies (stdlib only)
- Works with all Claude Code versions supporting post_tool_use hook
- Compatible with parallel session execution (session-specific files)
