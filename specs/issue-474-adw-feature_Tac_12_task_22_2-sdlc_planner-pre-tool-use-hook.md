# Feature: Pre-Tool Use Hook Implementation

## Metadata
issue_number: `474`
adw_id: `feature_Tac_12_task_22_2`
issue_json: `{"number": 474, "title": "[Task 22/49] [FEATURE] Create pre_tool_use.py hook file", "body": "## Description\n\nCreate a hook that runs BEFORE every tool use.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/pre_tool_use.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`\n\n## Key Features\n- Pre-tool use logging\n- Integration point for observability\n- Called before every tool invocation\n\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/pre_tool_use.py`\n\n## Wave 3 - New Hooks (Task 22 of 9)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_22_2"}`

## Feature Description
This task implements a lightweight pre-tool-use hook that runs before every tool invocation in Claude Code. The hook provides observability and telemetry by logging basic metadata about each tool call without blocking execution. Unlike the existing pre_tool_use.py which implements dangerous command blocking and forbidden path access checks, this new version should focus purely on non-blocking observability logging that captures tool name, timestamp, and working directory to stdout.

The implementation follows the session_start hook pattern - simple, robust, always exits successfully (even on errors), and provides structured text output for easy parsing and human readability.

## User Story
As a **developer using Claude Code in TAC Bootstrap projects**
I want to **automatically log metadata about every tool invocation**
So that **I can observe agent behavior, debug workflows, and understand tool usage patterns without disrupting execution**

## Problem Statement
Currently, TAC Bootstrap projects lack a standardized, non-blocking pre-tool-use hook that provides observability into tool invocations. While the existing pre_tool_use.py file implements security checks (dangerous commands, forbidden paths), there's a need for a simpler, pure observability hook that:
- Logs tool invocation metadata without blocking execution
- Provides structured, human-readable output to stdout
- Always exits successfully to prevent workflow disruption
- Follows Claude Code hook conventions and patterns

This hook serves as a lightweight telemetry layer that helps developers understand what tools agents are using, when, and in what context - essential for debugging, monitoring, and optimizing agentic workflows.

## Solution Statement
Implement a pre-tool-use hook that:
1. Receives tool invocation data via stdin (JSON format from Claude Code)
2. Extracts tool name, timestamp, and working directory
3. Outputs structured text (not JSON) to stdout with ISO timestamps and key-value format
4. Wraps all logic in try-except to handle errors gracefully
5. Always exits with code 0, even on failures
6. Requires no configuration or dependencies beyond Python stdlib

The hook will be:
- Created in `.claude/hooks/pre_tool_use.py` (base repository)
- Templated in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`
- Registered in `scaffold_service.py` hooks list (already present, verify presence)

This approach balances observability needs with robustness - providing valuable telemetry without introducing fragility into the tool execution pipeline.

## Relevant Files
Files necessary to implement the feature:

### Existing Hook Implementation (for reference)
- `.claude/hooks/pre_tool_use.py` - Current hook with security checks and logging to JSON files
  - Shows the existing implementation which focuses on dangerous command blocking and forbidden path access
  - Writes to session-specific JSON log files in agents/hook_logs/
  - Provides pattern for error handling and graceful degradation

### Template Files (for reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2` - Existing template
  - Already exists and implements security validation (rm -rf blocking, forbidden path checks)
  - Uses Jinja2 variables: `{{ config.project.name }}`, `{{ config.agentic.safety.forbidden_paths }}`, `{{ config.paths.logs_dir }}`
  - Follows similar pattern to session_start.py.j2

### Reference Hook (for pattern matching)
- `.claude/hooks/session_start.py` - Session initialization hook
  - Best pattern to follow for simple, non-blocking logging hook
  - Shows proper error handling, graceful degradation, structured text output
  - Uses ISO timestamps, key-value format, stdout logging

### Template Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2` - Session start template
  - Shows minimal template approach with project name substitution
  - Good pattern for static implementation without complex Jinja2 logic

### Service Configuration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Scaffold service
  - Line 344-357: Hook registration in `_add_claude_files` method
  - Hook already registered as: `("pre_tool_use.py", "Pre-execution validation")`
  - No changes needed - just verify it's present

### New Files
None - all files already exist and will be modified/replaced.

## Implementation Plan

### Phase 1: Analysis and Design
Analyze the existing pre_tool_use.py hook implementation to understand:
- Current security validation logic (rm -rf blocking, forbidden paths)
- Data structure of stdin input from Claude Code
- Error handling patterns
- Logging approach

Review session_start.py hook to extract the best-practice pattern for:
- Structured text output format (not JSON)
- Error handling (try-except wrapping)
- Always-successful exit (sys.exit(0) in all paths)
- Minimal dependencies approach

Confirm that pre_tool_use.py is already registered in scaffold_service.py hooks list.

### Phase 2: Core Implementation
Implement the new lightweight pre-tool-use hook:
- Replace/modify `.claude/hooks/pre_tool_use.py` to focus on observability
- Simplify to remove security validation logic (moved to separate hook if needed)
- Add structured text output to stdout (ISO timestamp + tool_name + cwd)
- Ensure robust error handling with try-except
- Always exit with code 0

Key implementation requirements:
- Read JSON from stdin to get tool_name, tool_input, session_id
- Extract timestamp using `datetime.now(timezone.utc).isoformat()`
- Extract cwd using `os.getcwd()`
- Print structured text: `[TIMESTAMP] tool=TOOL_NAME cwd=CWD`
- Catch all exceptions, optionally log to stderr, exit 0 regardless

### Phase 3: Template Creation
Create/update the Jinja2 template:
- Modify `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`
- Replace complex security validation logic with simple observability logging
- Use minimal Jinja2 variables (only `{{ config.project.name }}` in docstring)
- Follow session_start.py.j2 pattern for simplicity

No configuration variables needed in v1 - static implementation.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze Existing Implementation
- Read `.claude/hooks/pre_tool_use.py` to understand current stdin data structure
- Read `.claude/hooks/session_start.py` to extract best-practice patterns
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2` to understand template structure
- Document the stdin JSON structure from Claude Code (tool_name, tool_input, session_id)
- Document the desired output format (structured text, not JSON)

### Task 2: Implement Base Hook File
- Create new implementation of `.claude/hooks/pre_tool_use.py`
- Add shebang: `#!/usr/bin/env -S uv run --script`
- Add script metadata block for uv (requires-python >= 3.11, no dependencies)
- Add docstring explaining the hook purpose
- Implement main() function with:
  - Read JSON from stdin: `json.load(sys.stdin)`
  - Extract tool_name, session_id, timestamp
  - Get current working directory: `os.getcwd()`
  - Print structured output: `[TIMESTAMP] tool=TOOL_NAME cwd=CWD session=SESSION_ID`
  - Wrap everything in try-except
  - Always exit with code 0
- Test manually by echoing JSON to the script: `echo '{"tool_name": "Read", "tool_input": {}, "session_id": "test"}' | .claude/hooks/pre_tool_use.py`

### Task 3: Create Jinja2 Template
- Create/update `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2`
- Copy structure from the base hook file
- Replace project-specific name with `{{ config.project.name }}` in docstring
- Keep implementation simple - no complex Jinja2 logic
- Ensure template matches base file structure exactly except for variable substitution

### Task 4: Verify Scaffold Service Registration
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Verify that pre_tool_use.py is in the hooks list (around line 345)
- Expected entry: `("pre_tool_use.py", "Pre-execution validation")`
- Update reason string if needed to: `("pre_tool_use.py", "Pre-tool observability logging")`

### Task 5: Execute Validation Commands
- Run all validation commands to ensure zero regressions
- Verify tests pass, linting passes, type checking passes
- Run smoke test to ensure CLI still works

## Testing Strategy

### Unit Tests
No dedicated unit tests needed for hooks - they're integration-tested via Claude Code runtime.

### Integration Testing
Test the hook manually:
1. Create test JSON input matching Claude Code format:
   ```bash
   echo '{"tool_name": "Read", "tool_input": {"file_path": "test.txt"}, "session_id": "test-123"}' | .claude/hooks/pre_tool_use.py
   ```
2. Verify structured text output appears on stdout
3. Verify exit code is 0: `echo $?`
4. Test error handling by providing invalid JSON:
   ```bash
   echo 'invalid json' | .claude/hooks/pre_tool_use.py
   ```
5. Verify still exits with code 0

### Edge Cases
- Empty stdin - should handle gracefully and exit 0
- Missing tool_name field - should handle gracefully with tool_name="unknown"
- Missing session_id field - should handle gracefully with session_id="unknown"
- Malformed JSON - should catch JSONDecodeError and exit 0
- General exceptions - should catch Exception and exit 0
- Very long tool names or paths - should not truncate or fail

## Acceptance Criteria
- [ ] Base hook file `.claude/hooks/pre_tool_use.py` exists and implements observability logging
- [ ] Hook reads JSON from stdin and extracts tool_name, session_id, cwd
- [ ] Hook outputs structured text (not JSON) to stdout with ISO timestamp, tool name, cwd
- [ ] Hook has robust error handling - wraps all logic in try-except
- [ ] Hook always exits with code 0, even on errors
- [ ] Jinja2 template `pre_tool_use.py.j2` exists and matches base file structure
- [ ] Template uses minimal Jinja2 variables (only project name in docstring)
- [ ] Hook is registered in scaffold_service.py hooks list (verify presence)
- [ ] Manual testing confirms hook works with valid JSON input
- [ ] Manual testing confirms hook handles errors gracefully (invalid JSON, missing fields)
- [ ] All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `echo '{"tool_name": "Read", "tool_input": {}, "session_id": "test"}' | .claude/hooks/pre_tool_use.py` - Hook manual test

## Notes
- The hook should be purely for observability - NO blocking or validation logic
- Follow the session_start.py pattern for simplicity and robustness
- Use structured text output (not JSON) for human readability
- Always exit successfully to prevent disrupting tool execution
- The existing pre_tool_use.py has complex security validation logic that should be removed in favor of pure observability
- Consider creating a separate hook for security validation if that functionality is needed
- No configuration options in v1 - keep it simple with static implementation
- Environment variables from Claude Code: Confirm what's available (likely TOOL_NAME, SESSION_ID via stdin JSON)
- The hook will be called frequently (before every tool use), so keep it lightweight and fast
- Future enhancements could include: configurable log formats, filtering specific tools, log levels
