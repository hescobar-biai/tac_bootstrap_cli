# Feature: Universal Hook Logger Template

## Metadata
issue_number: `259`
adw_id: `feature_Tac_9_task_18`
issue_json: `{"number":259,"title":"Add universal_hook_logger.py.j2 hook template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_18\n\n**Description:**\nCreate Jinja2 template for universal hook logger. Provides comprehensive logging across all Claude Code hook events.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/universal_hook_logger.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/universal_hook_logger.py` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for a universal hook logger that provides comprehensive logging across all Claude Code hook events. This logger will capture events from all 7 hook types (PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, PreCompact) in a unified format. The template follows existing patterns from post_tool_use.py.j2 and uses stdlib-only dependencies. Logs are written to `{{ config.paths.logs_dir }}/{session_id}/universal_hook.json` in JSON format for easy parsing and analysis.

## User Story
As a TAC Bootstrap user
I want to generate projects with a universal hook logger template
So that generated projects can comprehensively log all Claude Code hook events for debugging, auditing, and workflow analysis without needing to review multiple log files

## Problem Statement
Currently, hook logging in TAC Bootstrap templates is fragmented across individual hook files (post_tool_use.py.j2, pre_tool_use.py.j2, etc.). Users who want comprehensive visibility into all Claude Code hook events must:
1. Enable and configure multiple separate hooks
2. Review multiple log files to understand the full event sequence
3. Cannot easily correlate events across different hook types
4. Risk missing critical events if they forget to enable a specific hook

This fragmentation makes debugging complex workflows difficult and increases the cognitive load on users trying to understand their agentic development patterns.

## Solution Statement
Create a universal_hook_logger.py.j2 template that accepts generic JSON input from any hook event type and logs it to a single unified log file. The logger will:
- Support all 7 existing Claude Code hook types without modification
- Write to `{{ config.paths.logs_dir }}/{session_id}/universal_hook.json` following existing conventions
- Log timestamp, event_type, session_id, and full payload in JSON format (indent=2)
- Exclude tool_output by default to prevent excessive disk usage
- Fail silently (sys.exit(0)) on errors to never disrupt workflows
- Use only Python stdlib (json, sys, pathlib) - no external dependencies
- Follow exact patterns from post_tool_use.py.j2 for consistency
- Require manual activation in settings.json (not enabled by default)

The rendered file will be created in `.claude/hooks/` but users must explicitly add it to their settings.json to activate it, ensuring they understand the logging implications.

## Relevant Files
Files necessary to implement the feature:

### Templates to Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2` - Primary pattern reference for structure, error handling, and log format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2` - Additional reference for hook patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2` - Reference for stdin JSON parsing
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2` - Hook configuration reference (all 7 hook types)

### Configuration Files
- `.claude/settings.json` - Shows all 7 hook types currently in use: PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, PreCompact
- `config.yml` - Contains project configuration including paths.logs_dir variable used in templates

### Application Logic
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that renders hook templates during project generation
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py` - Service that renders templates to root directory

### Documentation
- `ai_docs/doc/plan_tasks_Tac_9.md` - Task 18 specification for this feature
- `ai_docs/claude-code-hooks.md` - Documentation about Claude Code hooks system
- `specs/issue-258-adw-feature_Tac_9_task_17-sdlc_planner-context-bundle-builder-hook.md` - Recent similar hook implementation for reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2` (CREATE)
- `.claude/hooks/universal_hook_logger.py` (CREATE - rendered via doctor command)

## Implementation Plan

### Phase 1: Foundation
**Goal:** Study existing hook patterns and understand requirements

1. Read and analyze existing hook templates:
   - Review post_tool_use.py.j2 (primary pattern reference)
   - Review pre_tool_use.py.j2 and user_prompt_submit.py.j2
   - Identify common patterns: error handling, log directory creation, JSON parsing/writing
   - Note truncation strategy in post_tool_use.py.j2 (max_length=500)

2. Verify settings.json structure:
   - Confirm all 7 hook types are present
   - Understand hook matcher patterns and command format
   - Note the `|| true` pattern for graceful failure

3. Understand template rendering:
   - Review how scaffold_service.py renders hook templates
   - Confirm {{ config.paths.logs_dir }} variable availability
   - Verify Jinja2 template syntax requirements

### Phase 2: Core Implementation
**Goal:** Create the universal_hook_logger.py.j2 template

1. Create template file structure:
   - Shebang: `#!/usr/bin/env python3`
   - Module docstring explaining purpose and log location
   - Stdlib imports only: json, sys, pathlib
   - WARNING comment about sensitive data in logs

2. Implement main() function:
   - Wrap entire logic in try/except for silent failure
   - Read JSON input from stdin using json.load(sys.stdin)
   - Extract session_id from input_data (default to 'unknown')
   - Extract event_type (could be inferred from hook type or passed explicitly)
   - Create log directory: `{{ config.paths.logs_dir }}/{session_id}/`
   - Set log file path: `universal_hook.json`

3. Implement log entry creation:
   - Structure: { "timestamp": str, "event_type": str, "session_id": str, "input_data": dict }
   - DO NOT include tool_output field to prevent excessive log sizes
   - Preserve full input_data payload for comprehensive debugging

4. Implement log file management:
   - Read existing log file if exists (handle JSONDecodeError gracefully)
   - Initialize empty list if file doesn't exist
   - Append new log entry to list
   - Write back with json.dump(log_data, f, indent=2)

5. Implement error handling:
   - Catch json.JSONDecodeError separately (silent exit)
   - Catch all other exceptions with bare except (silent exit)
   - Always sys.exit(0) - never disrupt workflow
   - Follow exact pattern from post_tool_use.py.j2 lines 78-83

6. Add __main__ guard and call main()

### Phase 3: Integration
**Goal:** Render template to root and document usage

1. Render template to .claude/hooks/:
   - Use doctor command to render universal_hook_logger.py to root
   - Verify file is created at `.claude/hooks/universal_hook_logger.py`
   - Verify Jinja2 variables are correctly substituted
   - Ensure file has executable permissions (doctor should handle this)

2. Document activation instructions:
   - Add comment block at top of template explaining manual activation
   - Document example settings.json entry for each hook type
   - Note that users must add this hook to their settings.json for desired events
   - Warn about potential log size and performance impact

3. Verify patterns match existing hooks:
   - Compare side-by-side with post_tool_use.py.j2
   - Ensure error handling is identical
   - Confirm log directory structure matches
   - Validate JSON format consistency

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze existing hook templates
- Read post_tool_use.py.j2 to understand primary pattern
- Read pre_tool_use.py.j2 and user_prompt_submit.py.j2 for additional patterns
- Read settings.json to confirm all 7 hook types
- Document key patterns: error handling, log creation, JSON format

### Task 2: Create universal_hook_logger.py.j2 template
- Create file at tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2
- Add shebang and module docstring with warning about sensitive data
- Import stdlib modules: json, sys, pathlib
- Implement main() function with comprehensive error handling
- Implement log entry creation (timestamp, event_type, session_id, input_data)
- Implement log file reading/writing with JSON format (indent=2)
- Add comment blocks explaining manual activation requirement
- Add __main__ guard

### Task 3: Render template to root directory
- Use doctor command or manual rendering to create .claude/hooks/universal_hook_logger.py
- Verify Jinja2 variables are correctly substituted
- Confirm file exists and has correct content
- Verify log directory path is correct

### Task 4: Validate implementation
- Compare universal_hook_logger.py with post_tool_use.py for consistency
- Verify error handling matches existing patterns exactly
- Confirm log format matches (JSON with indent=2)
- Check that no external dependencies are used
- Verify silent failure on all error conditions

### Task 5: Run validation commands
- Execute all validation commands listed below
- Fix any issues found by linting or type checking
- Ensure tests pass with zero regressions
- Verify CLI smoke test works

## Testing Strategy

### Unit Tests
No new unit tests required for templates - templates are validated through:
1. Rendering smoke test (doctor command succeeds)
2. Manual inspection of rendered output
3. Validation that Jinja2 syntax is correct
4. Comparison with existing hook templates

### Edge Cases
Document and handle these edge cases in code comments:
1. Log directory doesn't exist - create with parents=True, exist_ok=True
2. Log directory not writable - fail silently with sys.exit(0)
3. Disk full during write - fail silently with sys.exit(0)
4. Invalid JSON input - catch JSONDecodeError and exit silently
5. Missing session_id in input - default to 'unknown'
6. Missing timestamp in input - handle gracefully
7. Corrupted existing log file - reinitialize as empty list
8. Very large input_data payloads - no truncation, but warn in comments about disk usage

## Acceptance Criteria
- [ ] Template file created at tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/universal_hook_logger.py.j2
- [ ] Template uses ONLY Python stdlib (json, sys, pathlib) - no external dependencies
- [ ] Template logs to {{ config.paths.logs_dir }}/{session_id}/universal_hook.json
- [ ] Log format is JSON array with indent=2, appending new entries
- [ ] Log entry structure: { "timestamp": str, "event_type": str, "session_id": str, "input_data": dict }
- [ ] Template DOES NOT log tool_output field by default
- [ ] Error handling matches post_tool_use.py.j2 pattern exactly (silent sys.exit(0))
- [ ] Template includes warning comment about sensitive data in logs
- [ ] Template includes comment explaining manual activation requirement
- [ ] Template includes comment about log rotation (user responsibility)
- [ ] Rendered file created at .claude/hooks/universal_hook_logger.py with correct content
- [ ] All Jinja2 variables correctly substituted in rendered file
- [ ] No settings.json modifications (manual activation only)
- [ ] Comparison with post_tool_use.py.j2 shows consistent patterns
- [ ] All validation commands pass with zero errors

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions
1. **No automatic settings.json modification**: Users must manually add the universal logger to their settings.json. This is intentional because:
   - A universal logger capturing all events could create large logs
   - Performance impact should be a conscious user choice
   - Users should understand what they're enabling

2. **No tool_output logging**: Following the pattern from post_tool_use.py.j2 which truncates output, we exclude tool_output entirely to:
   - Prevent multi-GB log files
   - Focus on event metadata and input parameters
   - Maintain reasonable disk usage
   - Users can enable specific hooks if they need output details

3. **Generic JSON input acceptance**: The logger accepts any JSON structure from stdin, making it compatible with all hook types without code changes

4. **Single unified log file**: All events go to one file (universal_hook.json) rather than separate files per hook type, enabling easier correlation of events

### Future Enhancements (Out of Scope)
- Configurable log levels or event filtering
- Automatic log rotation (users should use logrotate or similar)
- Structured logging with separate files per event type
- Secret detection and redaction
- Log compression
- Integration with external logging services

### Related Tasks
- Task 17 (issue 258): Context bundle builder hook - similar hook implementation
- Task 16 (issue 257): TTS initialization - related utility template
- Task 14-15 (issues 255-256): TTS templates - similar template patterns

### Source Reference
Source file: `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/universal_hook_logger.py`
This source should be consulted during implementation but the template must follow TAC Bootstrap conventions and use Jinja2 variables.
