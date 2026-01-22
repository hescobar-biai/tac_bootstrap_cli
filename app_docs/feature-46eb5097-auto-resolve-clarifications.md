# Auto-Resolve Clarifications in Planning Workflow

**ADW ID:** 46eb5097
**Date:** 2026-01-22
**Specification:** `/Volumes/MAc1/Celes/tac_bootstrap/trees/46eb5097/specs/issue-100-adw-46eb5097-chore_planner-auto-resolve-clarifications.md`

## Overview

Modified the planning workflow (`adw_plan_iso.py`) to automatically resolve clarification questions when ambiguities are detected in GitHub issues, replacing the previous behavior of pausing execution and waiting for manual user responses. The workflow now uses AI-powered auto-resolution via the `resolve_clarifications` function, ensuring continuous execution even when issues contain ambiguities.

## What Was Built

- **Auto-resolution Integration**: Replaced manual pause workflow with automatic clarification resolution
- **Fallback Mechanism**: Added graceful degradation to documented assumptions when auto-resolution fails
- **Template Synchronization**: Applied identical changes to both base file and Jinja2 template
- **Workflow Continuity**: Eliminated workflow interruptions caused by clarification needs

## Technical Implementation

### Files Modified

- `adws/adw_plan_iso.py`: Base planning workflow implementation
  - Removed `--clarify-continue` CLI argument (line 72)
  - Removed `clarify_continue` variable assignment (line 79)
  - Replaced pause-on-clarify logic with auto-resolution (lines 180-202)

- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`: Template version
  - Applied identical changes to ensure template generates updated code

- `.mcp.json`: Updated MCP configuration path (playwright config reference)
- `playwright-mcp-config.json`: Path update for consistency

### Key Changes

1. **Removed Pause Behavior**: Eliminated `sys.exit(2)` call that paused workflow execution when clarifications were needed

2. **Added Auto-Resolution**: Integrated `resolve_clarifications()` function from `adw_modules.workflow_ops`:
   ```python
   from adw_modules.workflow_ops import resolve_clarifications

   resolved_text, resolve_error = resolve_clarifications(
       issue, clarification_response, adw_id, logger, working_dir=None
   )
   ```

3. **Implemented Error Handling**: Added fallback logic when auto-resolution fails:
   - Logs warning message
   - Posts issue comment with failure notification
   - Uses documented assumptions from `clarification_response.assumptions`

4. **Success Path**: When auto-resolution succeeds:
   - Uses resolved text as clarification documentation
   - Posts issue comment with auto-resolved decisions
   - Continues workflow without interruption

5. **Removed CLI Argument**: Eliminated `--clarify-continue` flag since auto-resolution is now always active

## How to Use

The auto-resolve feature works transparently when running the planning workflow:

1. **Standard Workflow Execution**:
   ```bash
   uv run adws/adw_plan_iso.py <issue_number> [adw_id]
   ```

2. **When Ambiguities Detected**:
   - Workflow automatically invokes `resolve_clarifications()`
   - AI analyzes the issue and clarification questions
   - Provides concrete answers or uses documented assumptions
   - Posts results to GitHub issue as a comment
   - Continues to planning phase without pausing

3. **Manual Skip** (if needed):
   ```bash
   uv run adws/adw_plan_iso.py <issue_number> --skip-clarify
   ```

4. **Monitoring Results**:
   - Check GitHub issue comments for auto-resolution status
   - Success: "🤖 Auto-resolved clarifications: ..."
   - Failure: "⚠️ Auto-resolution failed, using assumptions: ..."

## Configuration

No configuration changes required. The feature works out-of-the-box.

**Key Behaviors**:
- `working_dir=None`: Uses current working directory (default behavior)
- `awaiting_clarification` state: Always set to `False` (no longer pauses)
- Error handling: Non-blocking - failures log warnings but don't stop workflow

## Testing

Run the test suite to verify the changes:

```bash
# Full project tests
cd /Volumes/MAc1/Celes/tac_bootstrap/trees/46eb5097
uv run pytest

# CLI-specific tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting validation
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

**Test an Issue with Ambiguities**:
1. Create a GitHub issue with vague requirements
2. Run: `uv run adws/adw_plan_iso.py <issue_number>`
3. Verify workflow completes without pausing
4. Check issue comments for auto-resolution results
5. Confirm planning phase executes with resolved clarifications

## Notes

### Design Decisions

- **Always Auto-Resolve**: No manual intervention option. The workflow always attempts automatic resolution to maximize automation and reduce friction.

- **Non-Blocking Failures**: If auto-resolution fails, the system falls back to documented assumptions and continues. This ensures workflows never get stuck.

- **Preserved sys.exit**: The `sys` module import remains because `sys.exit()` is used elsewhere in the file (error handling, validation failures). Only the pause-specific `sys.exit(2)` was removed.

- **Idempotent Templates**: Changes applied to both base file and Jinja2 template ensure newly generated projects include the auto-resolve behavior.

### Dependencies

Requires the `resolve_clarifications` function from Issue #98:
- Located in `adws/adw_modules/workflow_ops.py` (lines 269-340)
- Uses AI to analyze issues and provide concrete answers to clarification questions
- Returns `(resolved_text: str, error: str | None)`

### Future Considerations

- **Feedback Loop**: Consider adding metrics to track auto-resolution success rate
- **User Override**: Could add advanced flag to force manual clarification if needed
- **Resolution Quality**: Monitor quality of auto-resolved answers to improve prompts
- **Assumption Validation**: Post-implementation validation of whether assumptions were correct
