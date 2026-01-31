# Feature: Create post_tool_use.py Hook File

## Metadata
issue_number: `475`
adw_id: `feature_Tac_12_task_23`
issue_json: `{"number": 475, "title": "[Task 23/49] [FEATURE] Create post_tool_use.py hook file", "body": "## Description\n\nCreate a hook that runs AFTER every tool use.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/post_tool_use.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2`\n\n## Key Features\n- Post-tool use logging\n- Result capture\n- Performance tracking\n\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/post_tool_use.py`\n\n## Wave 3 - New Hooks (Task 23 of 9)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_23"}`

## Feature Description
Create a post-tool-use hook that runs AFTER every tool execution in Claude Code sessions. This hook captures essential observability data including tool name, input parameters, output results (truncated), and timestamps. The hook is best-effort logging - it must never block or interrupt the tool execution workflow. All errors are silently suppressed (exit 0).

This hook is part of Wave 3 of the hook system implementation, complementing the existing pre_tool_use.py hook for comprehensive tool execution observability.

## User Story
As a TAC Bootstrap user
I want my generated projects to log post-tool execution data automatically
So that I can observe, debug, and analyze tool usage patterns without blocking workflows

## Problem Statement
Currently, the TAC Bootstrap project has:
1. An existing base implementation at `.claude/hooks/post_tool_use.py`
2. An existing template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2`
3. Registration in `scaffold_service.py` at line 346

However, the issue requires verification that:
- The base implementation follows the correct pattern (uses utils.constants.ensure_session_log_dir)
- The template correctly uses Jinja2 variables ({{ config.paths.logs_dir }})
- Both implementations are aligned and follow best practices
- The hook is properly registered in scaffold_service.py

There's a mismatch between the base implementation and template:
- Base uses `utils.constants.ensure_session_log_dir` utility
- Template manually creates the log directory structure
- Template includes truncate_output helper (500 char limit)
- Base doesn't explicitly truncate (but doesn't need to since it logs raw input_data)

## Solution Statement
Align the base implementation and template to follow consistent patterns:

1. **Base Implementation Alignment**: Update `.claude/hooks/post_tool_use.py` to match the template's approach:
   - Add truncate_output helper function
   - Extract specific fields (tool_name, tool_input, tool_output, timestamp, session_id)
   - Apply truncation to tool_output
   - Use ensure_session_log_dir from utils.constants

2. **Template Verification**: Ensure the template correctly uses {{ config.paths.logs_dir }} and follows the same logging pattern

3. **Registration Verification**: Confirm scaffold_service.py includes the hook in the hooks list (already verified at line 346)

4. **Documentation**: Ensure both files have clear docstrings explaining:
   - What the hook does
   - Where logs are stored
   - That errors are silently suppressed
   - Truncation behavior

## Relevant Files
Files necessary for implementing the feature:

- `.claude/hooks/post_tool_use.py` - Base implementation that serves as template source
  - Currently uses ensure_session_log_dir utility
  - Needs to add truncation and field extraction to match template

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2` - Jinja2 template for CLI generation
  - Already includes truncate_output helper
  - Already extracts specific fields with truncation
  - Uses {{ config.paths.logs_dir }} correctly

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Hook registration
  - Already includes post_tool_use.py at line 346
  - No changes needed

- `.claude/hooks/utils/constants.py` - Utility for ensure_session_log_dir
  - Referenced by base implementation
  - Template should also use this pattern for consistency

### New Files
None - all files already exist and are registered

## Implementation Plan

### Phase 1: Alignment Analysis
Analyze differences between base implementation and template to determine the canonical approach:
- Base implementation uses ensure_session_log_dir utility (good)
- Template manually creates directories (less maintainable)
- Template includes truncation (good for preventing log bloat)
- Template extracts specific fields (good for structured logging)

**Decision**: Update base implementation to include truncation and field extraction while keeping ensure_session_log_dir utility. Update template to use ensure_session_log_dir pattern.

### Phase 2: Base Implementation Update
Update `.claude/hooks/post_tool_use.py` to:
- Add truncate_output helper function
- Extract and structure log entry with specific fields
- Apply truncation to tool_output
- Maintain ensure_session_log_dir usage
- Add comprehensive docstring

### Phase 3: Template Alignment
Update `post_tool_use.py.j2` template to:
- Use ensure_session_log_dir pattern (import from utils.constants)
- Maintain truncate_output helper
- Keep structured log entry extraction
- Use {{ config.paths.logs_dir }} in ensure_session_log_dir call
- Ensure docstring matches base implementation style

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and Compare Implementations
- Read `.claude/hooks/post_tool_use.py` (already done)
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2` (already done)
- Read `.claude/hooks/utils/constants.py` to understand ensure_session_log_dir
- Document differences and alignment strategy

### Task 2: Update Base Implementation
- Add truncate_output function (500 char limit with "... [truncated]" suffix)
- Update main() to extract specific fields: tool_name, tool_input, tool_output (truncated), timestamp, session_id
- Maintain ensure_session_log_dir usage
- Add comprehensive docstring explaining hook behavior
- Preserve all error handling (sys.exit(0) on all exceptions)

### Task 3: Update Template Implementation
- Add import for ensure_session_log_dir from utils.constants
- Replace manual directory creation with ensure_session_log_dir call
- Adjust template to use: `log_dir = ensure_session_log_dir(session_id)` where logs_dir comes from config
- Maintain truncate_output helper function
- Maintain structured log entry extraction
- Update docstring to use Jinja2 variable: {{ config.paths.logs_dir }}/{session_id}/post_tool_use.json

### Task 4: Verify Registration
- Confirm scaffold_service.py includes post_tool_use.py in hooks list at line 346 (already verified)
- Check doctor_service.py also references post_tool_use.py correctly (already verified)
- No code changes needed

### Task 5: Validation
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
No new unit tests required - existing scaffold_service tests cover hook registration. The hook is designed to fail silently (exit 0) on all errors, making it difficult to unit test meaningfully.

Manual testing approach:
1. Generate a new project with tac-bootstrap
2. Verify `.claude/hooks/post_tool_use.py` is created
3. Trigger tool execution in Claude Code session
4. Verify log file created at `.claude/logs/{session_id}/post_tool_use.json`
5. Verify log entries contain: tool_name, tool_input, tool_output (truncated), timestamp, session_id
6. Verify long outputs are truncated to 500 chars

### Edge Cases
- **Empty tool_output**: Should log as empty string or null, not crash
- **Very large tool_output**: Should truncate to 500 chars with "... [truncated]"
- **Missing session_id**: Should default to "unknown" and still log
- **Corrupted existing log file**: Should initialize empty array and continue
- **Permission errors**: Should exit 0 silently
- **JSON decode errors**: Should exit 0 silently

## Acceptance Criteria
1. ✅ Base implementation (`.claude/hooks/post_tool_use.py`) includes truncate_output helper
2. ✅ Base implementation extracts specific fields: tool_name, tool_input, tool_output (truncated), timestamp, session_id
3. ✅ Base implementation uses ensure_session_log_dir from utils.constants
4. ✅ Template (`post_tool_use.py.j2`) uses ensure_session_log_dir pattern
5. ✅ Template uses {{ config.paths.logs_dir }} correctly
6. ✅ Both implementations have consistent error handling (sys.exit(0) on all exceptions)
7. ✅ Both implementations have clear docstrings
8. ✅ Hook is registered in scaffold_service.py (line 346)
9. ✅ All validation commands pass with zero regressions
10. ✅ Generated projects create functional post_tool_use.py hooks

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Key Design Decisions
1. **Truncation**: 500 character limit prevents log bloat while preserving enough context for debugging
2. **Silent Failures**: sys.exit(0) on all errors ensures hooks never block user workflows
3. **Structured Logging**: Extracting specific fields makes logs easier to parse and analyze
4. **JSON Format**: indent=2 balances machine-parseability with human readability
5. **No Filtering**: Log all tool executions unconditionally for complete observability

### Implementation Pattern Clarification
After analysis, there are two viable approaches:

**Approach A (Template's current approach)**: Manually create log directories using Path operations
- Simple, no external dependencies
- Template uses: `log_dir = Path("{{ config.paths.logs_dir }}") / session_id`

**Approach B (Base's current approach)**: Use ensure_session_log_dir utility
- Requires utils module to be available in generated projects
- More maintainable if utility is already scaffolded

**Decision**: Use Approach A for template (manual directory creation) since:
1. Templates should be self-contained where possible
2. Avoids dependency on utils module being scaffolded first
3. Simple operation that doesn't require utility abstraction

Base implementation should align with template approach for consistency.

### Template Variable Usage
The template correctly uses {{ config.paths.logs_dir }} for the base log directory path. No additional configuration variables are needed.

### Auto-Resolved Clarifications Applied
- ✅ Log: tool_name, tool_input, tool_output (truncated), timestamp, session_id
- ✅ No performance metrics (use timestamp diff between pre/post for duration if needed)
- ✅ Store in {logs_dir}/{session_id}/post_tool_use.json as JSON array
- ✅ No filtering - log all tool executions
- ✅ Fail silently (exit 0) on all errors
- ✅ Store per-invocation, no aggregation
- ✅ JSON format with indent=2
- ✅ Truncate tool_output to 500 chars max
- ✅ Use {{ config.paths.logs_dir }} only, no other config needed
