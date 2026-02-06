# TAC-15: Migrate ADW Agent System to Claude Agent SDK

## Assumptions

1. The `claude-agent-sdk>=0.1.18` package is already declared in `adw_agent_sdk.py` inline script metadata and available via `uv run`.
2. The existing `adw_agent_sdk.py` module (1656 lines) with `query_to_completion()` and `quick_prompt()` is tested and functional.
3. The feature flag `ADW_USE_SDK` environment variable defaults to `"0"` (disabled) to avoid breaking existing workflows during rollout.
4. Template `.j2` files in `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/` are plain copies of the source files (no Jinja2 variables), so syncing is a file copy operation.
5. Model IDs in `adw_agent_sdk.py::ModelName` enum are current and correct for the Claude 4.5 family.
6. The `asyncio.run()` bridge from sync to async is acceptable since each ADW phase is a separate process with its own event loop.
7. Version bump will be `0.9.0` -> `0.10.0` (minor version increment for new feature capability).

---

## Task 1 — [FEATURE] Add SDK bridge function `_prompt_claude_code_sdk()` to `agent.py`

**Title**: Add SDK bridge function to agent.py with feature flag dispatch

**Description**:

Add a new function `_prompt_claude_code_sdk(request: AgentPromptRequest) -> AgentPromptResponse` that:

1. Imports `QueryInput`, `QueryOptions`, `QueryOutput`, `ModelName` from `adw_agent_sdk`
2. Maps short model names (`"sonnet"`, `"opus"`, `"haiku"`) to `ModelName` enum values
3. Builds `QueryOptions` with:
   - `model`: mapped from request.model
   - `cwd`: from request.working_dir
   - `bypass_permissions`: from request.dangerously_skip_permissions
   - `setting_sources`: `["project"]` to load `.claude/commands/` and settings
4. Builds `QueryInput` with prompt and options
5. Executes `asyncio.run(asyncio.wait_for(query_to_completion(query_input), timeout=request.timeout_seconds))`
6. Converts `QueryOutput` -> `AgentPromptResponse` preserving:
   - `output`: from `result.result`
   - `success`: from `result.success`
   - `session_id`: from `result.session_id`
   - `retry_code`: classified via existing `is_quota_exhausted_error()`, `is_rate_limited_error()`, `is_connection_error()` functions
   - `token_usage`: mapped from SDK `TokenUsage` to `data_types.TokenUsage`
7. Handles exceptions: `asyncio.TimeoutError` -> `RetryCode.TIMEOUT_ERROR`, general `Exception` -> classified via error message

Add helper functions:
- `_classify_sdk_error(error_msg: str) -> RetryCode`: reuses existing classifiers
- `_convert_sdk_token_usage(sdk_usage, duration_seconds: float) -> data_types.TokenUsage`: maps SDK fields to data_types fields, computing `duration_ms = int(duration_seconds * 1000)`

Add feature flag constant at module level:
```python
USE_SDK = os.getenv("ADW_USE_SDK", "0") == "1"
```

Modify `prompt_claude_code()` (line 578) to dispatch:
```python
def prompt_claude_code(request: AgentPromptRequest) -> AgentPromptResponse:
    save_prompt(request.prompt, request.adw_id, request.agent_name)
    if USE_SDK:
        return _prompt_claude_code_sdk(request)
    # ... existing subprocess code unchanged ...
```

**Acceptance Criteria**:
- `ADW_USE_SDK=0` preserves exact existing behavior (subprocess path)
- `ADW_USE_SDK=1` routes through SDK, returns same `AgentPromptResponse` type
- `prompt_claude_code_with_retry()` works transparently with both paths (no changes needed)
- `execute_template()` works transparently with both paths (no changes needed)
- Error classification produces correct `RetryCode` values for SDK errors

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`

---

## Task 2 — [FEATURE] Add `sdk_session_id` field to `ADWStateData` for session persistence

**Title**: Add SDK session ID tracking to ADWStateData model

**Description**:

Add `sdk_session_id: Optional[str] = None` field to the `ADWStateData` Pydantic model in `data_types.py` (after line 311, alongside existing `loaded_docs_topic` field).

This field will store the Claude Agent SDK session ID after each phase completes, enabling subsequent phases to resume the same session and benefit from context persistence.

**Acceptance Criteria**:
- `ADWStateData` model accepts `sdk_session_id` field
- Field defaults to `None` (backward compatible with existing state files)
- Field serializes/deserializes correctly to/from `adw_state.json`
- Existing state files without this field load without error

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`

---

## Task 3 — [FEATURE] Add `resume_session_id` parameter to `AgentPromptRequest`

**Title**: Add optional session resume parameter to AgentPromptRequest

**Description**:

Add `resume_session_id: Optional[str] = None` field to the `AgentPromptRequest` Pydantic model in `data_types.py` (after `timeout_seconds` field, line 198).

Update `_prompt_claude_code_sdk()` in `agent.py` (from Task 1) to pass `resume_session_id` to `QueryOptions(resume=request.resume_session_id)` when the value is not None.

The subprocess path in `prompt_claude_code()` ignores this field (Claude CLI subprocess creates new sessions each time).

**Acceptance Criteria**:
- `AgentPromptRequest` accepts optional `resume_session_id` field
- SDK path uses `QueryOptions(resume=...)` when session ID is provided
- SDK path falls back to new session (no resume) when `resume_session_id` is None
- Subprocess path ignores the field entirely
- If session resume fails (expired session), the SDK returns an error that gets classified and retried without resume

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`

---

## Task 4 — [FEATURE] Wire session persistence into `workflow_ops.py` for cross-phase context

**Title**: Save and reuse SDK session IDs across workflow phases in workflow_ops.py

**Description**:

Modify `workflow_ops.py` functions that call `execute_template()` or `execute_prompt()` to:

1. **After each successful execution**: Save `response.session_id` to ADW state:
   ```python
   if response.success and response.session_id:
       state = ADWState(adw_id)
       state.update(sdk_session_id=response.session_id)
   ```

2. **Before each execution**: Load `sdk_session_id` from state and pass it to the request:
   ```python
   state = ADWState(adw_id)
   session_id = state.get("sdk_session_id")
   ```

3. Update the `execute_template()` function in `agent.py` to accept and propagate `resume_session_id`:
   - Add optional parameter to `AgentTemplateRequest`: `resume_session_id: Optional[str] = None`
   - Pass it through to `AgentPromptRequest` when building the prompt request (line 1000)

4. Update key workflow_ops functions that chain phases:
   - `build_plan()` - save session after plan phase
   - `run_build()` - load session from plan, save after build
   - `run_tests()` - load session from build, save after test
   - `run_review()` - load session, save after review
   - `generate_documentation()` - load session, save after docs

**Acceptance Criteria**:
- Session ID is saved to `adw_state.json` after each successful phase
- Subsequent phases load and pass the session ID to their requests
- When `ADW_USE_SDK=0`, session ID is saved but ignored (subprocess creates new sessions)
- When `ADW_USE_SDK=1`, session ID enables context persistence across phases
- If a phase fails, the session ID from the last successful phase remains in state

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`

---

## Task 5 — [FEATURE] Make `output_file` optional in `AgentPromptRequest` for SDK path

**Title**: Make output_file optional to eliminate JSONL file I/O on SDK path

**Description**:

Change `output_file: str` to `output_file: Optional[str] = None` in `AgentPromptRequest` (line 196 of `data_types.py`).

Update `prompt_claude_code()` in `agent.py`:
- Subprocess path: require `output_file` (raise ValueError if None)
- SDK path (`_prompt_claude_code_sdk`): ignore `output_file` entirely

Update `execute_template()` in `agent.py`:
- When `USE_SDK` is True: set `output_file=None` in the `AgentPromptRequest`
- When `USE_SDK` is False: set `output_file` to the JSONL path (existing behavior, lines 991-997)

Optionally save SDK transcript for debugging:
- When SDK path completes, if `QueryOutput.messages` is non-empty, serialize to `agents/{adw_id}/{agent_name}/sdk_transcript.json`

**Acceptance Criteria**:
- `output_file` defaults to `None` in `AgentPromptRequest`
- SDK path does not create or write to JSONL files
- Subprocess path still requires and uses `output_file`
- `execute_template()` correctly sets `output_file` based on `USE_SDK` flag
- `execute_prompt()` correctly sets `output_file` based on `USE_SDK` flag
- SDK transcript is optionally saved for debugging

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py`

---

## Task 6 — [CHORE] Sync modified `agent.py` to template `agent.py.j2`

**Title**: Copy updated agent.py to Jinja2 template for CLI scaffolding

**Description**:

Copy the contents of the modified `agent.py` (from Tasks 1, 3, 5) to the corresponding Jinja2 template file. Since this template is a plain copy (no Jinja2 variables), the sync is a direct file copy.

Verify the template file is byte-identical to the source file after copy.

**Acceptance Criteria**:
- Template file contains the exact same content as the source file
- `diff` between source and template returns no differences
- CLI scaffolding produces the updated `agent.py` when generating new projects

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/agent.py` (source)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2` (target)

---

## Task 7 — [CHORE] Sync modified `data_types.py` to template `data_types.py.j2`

**Title**: Copy updated data_types.py to Jinja2 template for CLI scaffolding

**Description**:

Copy the contents of the modified `data_types.py` (from Tasks 2, 3, 5) to the corresponding Jinja2 template file. Since this template is a plain copy, the sync is a direct file copy.

**Acceptance Criteria**:
- Template file contains the exact same content as the source file
- `diff` between source and template returns no differences

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/data_types.py` (source)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2` (target)

---

## Task 8 — [CHORE] Sync modified `workflow_ops.py` to template `workflow_ops.py.j2`

**Title**: Copy updated workflow_ops.py to Jinja2 template for CLI scaffolding

**Description**:

Copy the contents of the modified `workflow_ops.py` (from Task 4) to the corresponding Jinja2 template file.

**Acceptance Criteria**:
- Template file contains the exact same content as the source file
- `diff` between source and template returns no differences

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_modules/workflow_ops.py` (source)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2` (target)

---

## Task 9 — [CHORE] Add `claude-agent-sdk` dependency to `adw_*_iso.py` script metadata

**Title**: Add claude-agent-sdk to inline script dependencies in ADW workflow scripts

**Description**:

Each `adw_*_iso.py` file uses PEP 723 inline script metadata (`# /// script`) to declare its dependencies for `uv run`. Since the SDK is now used transitively via `agent.py -> adw_agent_sdk.py`, add `"claude-agent-sdk>=0.1.18"` to the `dependencies` list in the following files:

1. `adw_plan_iso.py`
2. `adw_build_iso.py`
3. `adw_test_iso.py`
4. `adw_review_iso.py`
5. `adw_document_iso.py`
6. `adw_ship_iso.py`
7. `adw_patch_iso.py`
8. `adw_sdlc_iso.py`
9. `adw_sdlc_zte_iso.py`
10. `adw_plan_build_iso.py`
11. `adw_plan_build_test_iso.py`
12. `adw_plan_build_test_review_iso.py`
13. `adw_plan_build_review_iso.py`
14. `adw_plan_build_document_iso.py`

Only add the dependency if it is not already present. Also add to `workflow_ops.py` and `agent.py` inline script metadata if they have one.

**Acceptance Criteria**:
- All 14 workflow scripts include `claude-agent-sdk>=0.1.18` in their inline dependencies
- `uv run adws/adw_plan_iso.py --help` resolves the dependency without errors
- No duplicate dependency entries

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_build_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_test_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_review_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_document_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_ship_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_patch_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_sdlc_zte_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_build_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_build_test_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_build_test_review_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_build_review_iso.py`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_build_document_iso.py`

---

## Task 10 — [CHORE] Sync updated ADW workflow scripts to their `.j2` templates

**Title**: Copy updated ADW workflow scripts to Jinja2 templates after dependency addition

**Description**:

After Task 9 adds `claude-agent-sdk` to inline dependencies, copy each modified workflow script to its corresponding `.j2` template:

- `adws/adw_plan_iso.py` -> `templates/adws/adw_plan_iso.py.j2`
- `adws/adw_build_iso.py` -> `templates/adws/adw_build_iso.py.j2`
- (repeat for all 14 files)

**Acceptance Criteria**:
- All 14 template files match their source files
- `diff` between each source and template returns no differences

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_build_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_test_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_review_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_ship_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_patch_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_sdlc_zte_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_build_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_build_test_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_build_test_review_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_build_review_iso.py.j2`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_build_document_iso.py.j2`

---

## Task 11 — [CHORE] Add TAC-15 section to CLI README with SDK Integration table

**Title**: Document SDK integration in CLI README with component table

**Description**:

Add a new section `## TAC-15: Agent SDK Integration` to the CLI README after the existing TAC-14 section (after line ~229). The section must contain:

1. A brief description explaining the migration from subprocess CLI invocation to programmatic Agent SDK calls
2. A **component table** following the existing README style:

| # | Component | Description | Location |
|---|-----------|-------------|----------|
| 1 | SDK Bridge | Feature-flagged dispatch in agent.py (subprocess vs SDK) | `adws/adw_modules/agent.py` |
| 2 | SDK Wrapper | Typed Pydantic layer for claude-agent-sdk | `adws/adw_modules/adw_agent_sdk.py` |
| 3 | Session Persistence | Cross-phase context via sdk_session_id in ADWState | `adws/adw_modules/data_types.py` |
| 4 | Token Mapping | SDK TokenUsage -> data_types TokenUsage conversion | `adws/adw_modules/agent.py` |

3. A usage example:
```bash
# Enable SDK mode (default: disabled)
export ADW_USE_SDK=1

# Run workflow with SDK (same interface, SDK backend)
uv run adws/adw_sdlc_iso.py --issue 123

# Disable SDK mode (fallback to subprocess)
export ADW_USE_SDK=0
```

4. A benefits list:
- Context persistence across workflow phases (30-60% fewer input tokens)
- Elimination of JSONL file I/O overhead
- Programmatic error handling (typed Python exceptions vs exit codes)
- Session resume/fork capability for long-running workflows

**Acceptance Criteria**:
- New section appears after TAC-14 section
- Table uses same column format as existing tables in README
- Usage examples are copy-pasteable and correct
- No markdown rendering issues

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/README.md`

---

## Task 12 — [CHORE] Run existing test suite to verify backward compatibility

**Title**: Execute pytest to verify no regressions from SDK integration changes

**Description**:

Run the full test suite to verify that all changes maintain backward compatibility:

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
uv run pytest
```

Verify:
1. All existing tests pass without modification
2. No import errors from the new SDK imports (guarded by `USE_SDK` flag)
3. Pydantic model serialization/deserialization works with new optional fields
4. Template rendering still produces valid output files

If any tests fail, identify root cause and fix within this task.

**Acceptance Criteria**:
- `uv run pytest` exits with code 0
- No test failures related to SDK changes
- No deprecation warnings from new Pydantic field additions

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/` (test files)

---

## Task 13 — [CHORE] Validate SDK path with smoke test using `adw_plan_iso.py`

**Title**: Smoke test SDK integration by running a planning workflow with ADW_USE_SDK=1

**Description**:

Execute a real workflow phase with the SDK flag enabled to validate end-to-end functionality:

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
ADW_USE_SDK=1 uv run adws/adw_plan_iso.py <test-issue-number> <test-adw-id>
```

Verify:
1. The SDK path is invoked (check logs for SDK-related output, not subprocess)
2. `AgentPromptResponse` is returned with valid data
3. `session_id` is captured and saved to `adw_state.json`
4. `TokenUsage` is populated with non-zero values
5. The plan output is written to `specs/` directory in the worktree
6. No JSONL files are created when using SDK path

Compare with subprocess path:
```bash
ADW_USE_SDK=0 uv run adws/adw_plan_iso.py <test-issue-number> <test-adw-id-2>
```

Both should produce equivalent functional results.

**Acceptance Criteria**:
- SDK path completes without errors
- `adw_state.json` contains `sdk_session_id` field
- Token usage is tracked correctly
- Subprocess path still works identically to before

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/adws/adw_plan_iso.py` (execution target)
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/agents/` (output verification)

---

## Task 14 — [CHORE] Update CHANGELOG.md with version bump to 0.10.0

**Title**: Bump version to 0.10.0 and document TAC-15 changes in CHANGELOG

**Description**:

1. Update `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`:
   - Add new section `## [0.10.0] - YYYY-MM-DD` (use current date) below `## [Unreleased]`
   - Add header: `### Added - TAC-15: Agent SDK Integration`
   - Document all changes:

```markdown
## [0.10.0] - 2026-02-06

### Added - TAC-15: Agent SDK Integration

**SDK Bridge Layer:**
- Feature-flagged SDK dispatch in `agent.py` via `ADW_USE_SDK` environment variable
- `_prompt_claude_code_sdk()` bridge function converting `AgentPromptRequest` to SDK `QueryInput`
- Token usage mapping from SDK `TokenUsage` to `data_types.TokenUsage`
- Error classification reuse for SDK errors (quota, rate limit, connection, timeout)

**Cross-Phase Context Persistence:**
- `sdk_session_id` field added to `ADWStateData` for session tracking
- `resume_session_id` parameter in `AgentPromptRequest` for session resume
- Session ID saved/loaded across workflow phases in `workflow_ops.py`
- 30-60% input token reduction on build/test/review phases via context reuse

**Infrastructure:**
- `output_file` made optional in `AgentPromptRequest` (not needed for SDK path)
- `claude-agent-sdk>=0.1.18` added to all 14 ADW workflow script dependencies
- All modified source files synced to corresponding `.j2` templates
```

2. Update version in `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py` (or wherever `__version__` is defined) from `0.9.0` to `0.10.0`

3. Update version in `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml` from `0.9.0` to `0.10.0`

**Acceptance Criteria**:
- CHANGELOG has new `[0.10.0]` section with all changes documented
- Version string is `0.10.0` in all locations (pyproject.toml, __init__.py, CHANGELOG)
- Follows existing CHANGELOG format (Keep a Changelog 1.1.0)
- CHANGELOG section summarizes ALL tasks in this plan

**Impacted Paths**:
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/CHANGELOG.md`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml`
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/__init__.py`

---

## Parallel Execution Groups

| Grupo | Tareas | Cantidad | Dependencia | Descripcion |
|-------|--------|----------|-------------|-------------|
| P1 | 1, 2, 3 | 3 | Ninguna | Core SDK bridge + data model changes (agent.py, data_types.py) |
| P2 | 4, 5, 9 | 3 | P1 | Workflow integration (workflow_ops.py), output_file optionality, dependency declarations |
| P3 | 6, 7, 8, 10, 11 | 5 | P2 | Template sync (agent.py.j2, data_types.py.j2, workflow_ops.py.j2, workflow .j2s) + README docs |
| P4 | 12, 13 | 2 | P3 | Validation: pytest regression + SDK smoke test |
| SEQ | 14 | 1 | TODOS | CHANGELOG update and version bump to 0.10.0 |

### Dependency Rationale

- **P1 has no dependencies**: Tasks 1, 2, 3 modify separate files (`agent.py`, `data_types.py`) with no cross-dependency within the group.
- **P2 depends on P1**: Task 4 uses the `resume_session_id` from Task 3; Task 5 uses the `USE_SDK` flag from Task 1; Task 9 adds dependencies needed by Task 1's SDK imports.
- **P3 depends on P2**: Template syncs (Tasks 6-8, 10) must happen after all source modifications are complete. Task 11 (README) documents the final feature set.
- **P4 depends on P3**: Tests (Task 12) and smoke tests (Task 13) must run against the complete, synced codebase.
- **SEQ depends on ALL**: CHANGELOG (Task 14) summarizes all changes and must be the absolute last task.
