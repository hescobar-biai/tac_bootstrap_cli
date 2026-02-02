# Feature: Add TAC-12 Helper Functions to workflow_ops.py

## Metadata
issue_number: `501`
adw_id: `feature_Tac_12_task_49`
issue_json: `{"number": 501, "title": "[Task 49/49] [OPTIONAL] Add TAC-12 helper functions to workflow_ops.py", "body": "## Description (OPTIONAL)\n\nAdd optional helper functions for using new TAC-12 commands from ADW workflows.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`\n\n## Changes Required\nAdd functions:\n- scout_codebase() - Wrapper for /scout\n- plan_with_scouts() - Wrapper for /plan_w_scouters\n- build_in_parallel() - Wrapper for /build_in_parallel\n- find_and_summarize() - Wrapper for /find_and_summarize\n\n## Wave 9 - Optional Enhancements (Task 49 of 1) - **OPTIONAL**"}`

## Feature Description

Add optional helper functions to `workflow_ops.py` that serve as wrappers for new TAC-12 skill commands. These functions will provide convenient interfaces for ADW workflows to use advanced agentic features like parallel scouting, planning with documentation exploration, parallel builds, and code search/summarization.

The feature adds four wrapper functions corresponding to TAC-12 command enhancements:
1. `scout_codebase()` - Executes the /scout skill for exploring codebases
2. `plan_with_scouts()` - Executes the /plan_w_scouters skill for enhanced planning with parallel exploration
3. `build_in_parallel()` - Executes the /build_in_parallel skill for delegated parallel file creation
4. `find_and_summarize()` - Executes the /find_and_summarize skill for searching and summarizing code

## User Story

As an ADW workflow developer
I want to use TAC-12 command helpers from workflow_ops
So that I can leverage advanced agentic features like parallel exploration and builds without writing command execution code

## Problem Statement

ADW workflows need to invoke advanced TAC-12 features (/scout, /plan_w_scouters, /build_in_parallel, /find_and_summarize) but there are no wrapper functions in workflow_ops.py to simplify these calls. Each workflow must write its own agent execution code.

## Solution Statement

Add four helper functions to `workflow_ops.py` that wrap TAC-12 command execution. These functions will:
- Follow the existing pattern of wrapper functions in workflow_ops.py (like `load_ai_docs()`)
- Use `AgentTemplateRequest` and `execute_template()` to invoke the corresponding slash commands
- Accept appropriate parameters for each command
- Return `AgentPromptResponse` for consistent error handling
- Be documented with clear docstrings

## Relevant Files

### Files to Modify
- `adws/adw_modules/workflow_ops.py` - Add four new helper functions
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` - Update template with new functions

### Referenced Files
- `adws/adw_modules/data_types.py` - AgentTemplateRequest, AgentPromptResponse types (no changes)
- `adws/adw_modules/agent.py` - execute_template() function (no changes)

## Implementation Plan

### Phase 1: Understand Current Patterns
Review existing wrapper functions in workflow_ops.py (like `load_ai_docs()`) to understand:
- How AgentTemplateRequest is constructed
- How slash commands are invoked
- How responses are handled
- Parameter handling and logging patterns

### Phase 2: Implement Helper Functions
Add four new functions following the established patterns:
1. `scout_codebase()` - For /scout command
2. `plan_with_scouts()` - For /plan_w_scouters command
3. `build_in_parallel()` - For /build_in_parallel command
4. `find_and_summarize()` - For /find_and_summarize command

### Phase 3: Update Jinja2 Template
Update the template file to include the new functions so generated projects include these helpers.

## Step by Step Tasks

### Task 1: Research TAC-12 Commands
- Review available TAC-12 slash commands documentation
- Understand required and optional parameters for each command
- Identify return value expectations

### Task 2: Implement scout_codebase() Function
- Add function that wraps `/scout` command
- Accept parameters: query string, optional scale parameter, adw_id, logger, working_dir
- Return AgentPromptResponse with exploration results

### Task 3: Implement plan_with_scouts() Function
- Add function that wraps `/plan_w_scouters` command
- Accept parameters: description, adw_id, logger, working_dir
- Return AgentPromptResponse with enhanced plan

### Task 4: Implement build_in_parallel() Function
- Add function that wraps `/build_in_parallel` command
- Accept parameters: plan_file, adw_id, logger, working_dir
- Return AgentPromptResponse with build results

### Task 5: Implement find_and_summarize() Function
- Add function that wraps `/find_and_summarize` command
- Accept parameters: search_term, adw_id, logger, working_dir
- Return AgentPromptResponse with search and summary results

### Task 6: Update Jinja2 Template
- Add corresponding functions to `workflow_ops.py.j2` template
- Ensure template preserves variable placeholders (config.project, etc.)

### Task 7: Validation and Testing
- Verify functions follow existing code style and patterns
- Ensure proper type hints and docstrings
- Run linting and type checking
- Execute: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`

## Testing Strategy

### Unit Tests
- Test each function can be called with valid parameters
- Test error handling when execution fails
- Test logging output

### Integration Tests
- Verify functions work with ADW workflows
- Test with actual workflow_ops imports

### Edge Cases
- Missing required parameters
- Invalid adw_id
- None logger passed
- working_dir that doesn't exist

## Acceptance Criteria

1. All four helper functions are added to `workflow_ops.py`
2. Functions follow existing code patterns (style, naming, docstrings)
3. Proper type hints on all functions
4. Proper logging with debug statements
5. Functions match signatures of commands they wrap
6. Template is updated with all new functions
7. No breaking changes to existing functions
8. Code passes linting (ruff check)
9. Code passes type checking (mypy)
10. All existing tests continue to pass

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- This is an optional enhancement (Wave 9, Task 49)
- Functions are convenience wrappers following DDD pattern
- No new dependencies required
- All four functions follow the same pattern as `load_ai_docs()` in terms of:
  - Using AgentTemplateRequest for consistency
  - Returning AgentPromptResponse
  - Debug logging of requests and responses
  - Optional working_dir parameter
- Template synchronization is critical to ensure generated projects include these new helpers
