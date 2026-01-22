# Auto-Resolve Clarifications Function

**ADW ID:** 81ea2c63
**Date:** 2026-01-22
**Specification:** specs/issue-98-adw-81ea2c63-sdlc_planner-resolve-clarifications-function.md

## Overview

This feature adds a new `resolve_clarifications()` function to the `workflow_ops.py` module that enables automatic resolution of clarification questions during ADW workflow execution. The function uses an LLM agent (Claude Sonnet) to make implementation decisions based on issue context, eliminating the need for manual intervention in automated workflows while documenting all design decisions for traceability.

## What Was Built

- **`resolve_clarifications()` function** in `adws/adw_modules/workflow_ops.py` (lines 269-353)
  - Auto-resolves clarification questions using AI agent
  - Returns formatted markdown with decisions and rationales
  - Gracefully handles errors with fallback mechanism

## Technical Implementation

### Files Modified

- `adws/adw_modules/workflow_ops.py`: Added new `resolve_clarifications()` function after `clarify_issue()` function

### Key Changes

- **Function Signature**: `resolve_clarifications(issue, clarification, adw_id, logger, working_dir=None) -> Tuple[Optional[str], Optional[str]]`
  - Takes GitHubIssue and ClarificationResponse as input
  - Returns tuple of (resolved_text, error_message)

- **AI Agent Integration**: Constructs specialized prompt for LLM agent acting as senior software architect
  - Formats questions with category and severity
  - Includes current assumptions for context
  - Requests structured JSON response with decisions and rationales

- **Response Processing**:
  - Strips markdown code fences from agent output
  - Parses JSON response using `parse_json()` helper
  - Formats decisions as readable markdown

- **Error Handling**: Try-except block catches all failures
  - Agent execution failures return error message
  - JSON parsing errors are caught and returned
  - Caller can use assumptions as fallback when function returns None

## How to Use

The function is designed to be called from ADW workflows (like `adw_plan_iso.py`) after clarification analysis:

```python
from adws.adw_modules.workflow_ops import resolve_clarifications

# After running clarify_issue() and getting a ClarificationResponse
resolved_text, error_msg = resolve_clarifications(
    issue=github_issue,
    clarification=clarification_response,
    adw_id="some-adw-id",
    logger=logger,
    working_dir="/path/to/working/dir"
)

if resolved_text:
    # Use resolved decisions in spec file
    spec_content += resolved_text
else:
    # Fallback to assumptions if auto-resolution failed
    logger.warning(f"Auto-resolve failed: {error_msg}")
    # Use clarification.assumptions instead
```

## Configuration

- **Agent Model**: Uses Claude Sonnet model (configurable via `AgentPromptRequest.model`)
- **Output Location**: Saves agent decisions to `agents/{adw_id}/resolver/decisions.txt` for traceability
- **Permissions**: Agent runs with `dangerously_skip_permissions=False` for safety

## Expected Output Format

When successful, the function returns markdown formatted as:

```markdown
## Auto-Resolved Clarifications

**Summary:** brief overall approach

**Q:** original question text
**A:** decision made by AI
*rationale for the decision*

**Q:** next question...
**A:** next decision...
*rationale...*
```

## Error Cases Handled

- **Agent Execution Failure**: Returns `(None, response.output)` if agent fails to execute
- **Malformed JSON**: Try-except catches parsing errors and returns error message
- **Missing Fields**: Uses `.get()` with 'N/A' defaults for missing JSON fields
- **Markdown Code Fences**: Automatically strips ```json and ``` markers from agent responses

## Testing

The function can be imported and verified:

```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && python -c "from adws.adw_modules.workflow_ops import resolve_clarifications; print('Import successful')"
```

Linting and type checking:

```bash
cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && uv run ruff check adws/adw_modules/workflow_ops.py
cd /Volumes/MAc1/Celes/tac_bootstrap/trees/81ea2c63 && uv run mypy adws/adw_modules/
```

## Integration Notes

- **Designed for ZTE Workflows**: Enables Zero Touch Execution by removing manual clarification bottleneck
- **Fallback Strategy**: Caller should use original `clarification.assumptions` when function returns None
- **No Retries**: Function implements simple error handling without retry logic - simplicidad sobre robustez
- **Traceability**: All decisions saved to file for audit trail

## Notes

- This is Task 1 of a multi-task feature series for auto-resolving clarifications in ADW workflows
- Future tasks will integrate this function into `adw_plan_iso.py` workflow
- The function trusts the LLM agent to make reasonable decisions - validation happens at workflow level
- All required imports and helper functions (`execute_prompt`, `parse_json`) already exist in codebase
- No new dependencies required
