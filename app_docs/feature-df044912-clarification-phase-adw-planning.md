# Clarification Phase in ADW Planning

**ADW ID:** df044912
**Date:** 2026-01-21
**Specification:** specs/issue-67-adw-df044912-sdlc_planner-clarification-phase-adw-planning.md

## Overview

This feature adds an intelligent clarification phase to the ADW planning workflow (`adw_plan_iso.py`). Before generating an implementation plan, the system now analyzes GitHub issues using an LLM agent to detect ambiguities, missing information, or unclear technical decisions. This reduces the risk of implementing incorrect solutions and ensures all requirements are clearly defined.

## What Was Built

- **New Data Models**: Added `ClarificationQuestion` and `ClarificationResponse` Pydantic models for structured clarification analysis
- **LLM-Powered Analysis**: Implemented `clarify_issue()` function that uses an agent to detect ambiguities across four categories (requirements, technical decisions, edge cases, missing info)
- **CLI Arguments**: Added `--skip-clarify` and `--clarify-continue` flags to control clarification behavior
- **Workflow Integration**: Integrated clarification phase into `adw_plan_iso.py` between issue fetch and classification
- **Interactive Mode**: Workflow pauses and posts questions to GitHub issue when ambiguities are found
- **Continue Mode**: Alternative mode that documents assumptions and proceeds without pausing
- **State Persistence**: Clarifications saved to ADW state and passed to planning agent for inclusion in spec

## Technical Implementation

### Files Modified

- `adws/adw_modules/workflow_ops.py`: Added `clarify_issue()` function with LLM agent integration (119 lines added)
- `adws/adw_plan_iso.py`: Integrated clarification phase with argparse and workflow logic (100 lines added)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`: Added clarification data models (17 lines added)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_plan_iso.py.j2`: Template version of workflow changes (100 lines added)

### Key Changes

1. **Clarification Models** (data_types.py:269-285): Created `ClarificationQuestion` with question text, category (requirements/technical_decision/edge_case/missing_info), and severity (critical/important/nice_to_have). Created `ClarificationResponse` with has_ambiguities flag, questions list, assumptions list, and analysis text.

2. **LLM Analysis Function** (workflow_ops.py:160-265): Implemented `clarify_issue()` that constructs a detailed prompt for requirement analysis, executes it via `execute_prompt()` using sonnet model, parses JSON response with markdown code block stripping, and returns structured ClarificationResponse or error.

3. **Workflow Integration** (adw_plan_iso.py:149-226): Added argparse with three arguments (issue_number, adw_id, --skip-clarify, --clarify-continue), integrated clarification phase after fetch_issue and before classify_issue, implemented pause logic for interactive mode vs continue mode, and passed clarifications to build_plan() for spec inclusion.

4. **Build Plan Enhancement** (workflow_ops.py:280-292): Modified `build_plan()` to accept optional clarifications parameter and append clarification text to args passed to planning agent.

5. **GitHub Integration**: Added formatted markdown comments to issue with questions categorized by severity (emoji indicators: red/yellow/green), assumptions listed when in continue mode, and workflow pause notifications.

## How to Use

### Basic Usage (with clarification - default)

```bash
uv run adws/adw_plan_iso.py <issue-number>
```

This will analyze the issue for ambiguities. If found, it posts questions to the GitHub issue and pauses the workflow. You answer the questions in the issue comments, then re-run the workflow to continue.

### Skip Clarification Phase

```bash
uv run adws/adw_plan_iso.py <issue-number> --skip-clarify
```

Completely bypasses clarification analysis and proceeds directly to planning.

### Continue with Assumptions

```bash
uv run adws/adw_plan_iso.py <issue-number> --clarify-continue
```

If ambiguities are found, documents them in the spec as assumptions but continues without pausing. Useful when you want visibility into potential issues but don't want to block the workflow.

### Specify ADW ID

```bash
uv run adws/adw_plan_iso.py <issue-number> <adw-id>
```

Provide a specific ADW ID instead of auto-generating one.

## Configuration

No additional configuration required. The clarification phase uses:

- **Model**: sonnet (efficient for analysis tasks)
- **Agent Name**: clarifier
- **Output Location**: `agents/{adw_id}/clarifier/clarification.txt`

The LLM prompt is inline in workflow_ops.py:168-202 and can be modified to adjust analysis criteria.

## Clarification Categories

The agent analyzes issues across four categories:

1. **Requirements**: Unclear or incomplete functional requirements, missing success criteria
2. **Technical Decisions**: Unspecified technology choices, architectural patterns, or implementation approaches
3. **Edge Cases**: Unhandled error scenarios, boundary conditions, or special cases
4. **Missing Information**: Absent critical context, data, or specifications

Each question is rated by severity:
- **Critical**: Must be answered before implementation
- **Important**: Significant impact on design
- **Nice to have**: Optional clarification

## Testing

The feature was tested manually with issue #67. To test:

```bash
# Create a test issue with intentionally vague requirements
uv run adws/adw_plan_iso.py <test-issue-number>

# Verify that:
# - Clarification analysis runs and logs output
# - Questions are posted to GitHub issue if ambiguities found
# - Workflow pauses with exit code 0
# - Re-running after answering continues correctly
# - --clarify-continue mode documents assumptions
# - --skip-clarify bypasses the phase entirely
```

For general validation:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

- **Inline Prompt**: The LLM prompt is embedded in workflow_ops.py rather than in a separate template file for simplicity and immediate availability
- **Sonnet Model**: Uses sonnet for cost-efficiency and speed (analysis typically < 30s)
- **No Resume Logic**: Current implementation doesn't automatically resume when user answers. You manually re-run the workflow. Future enhancement could detect new comments and auto-resume.
- **State Persistence**: Clarifications are saved to state with key "clarification" and flag "awaiting_clarification" for tracking workflow phase

### Limitations

- **Single Round**: Only performs one round of clarification. Doesn't support iterative Q&A.
- **Manual Resume**: User must manually re-run workflow after answering questions (doesn't auto-detect responses)
- **No Response Extraction**: Current version doesn't parse user responses from issue comments (future enhancement)

### Future Extensions

- Multi-round clarification dialogs
- Auto-detection of user responses in issue comments
- Integration with issue templates to reduce ambiguities upfront
- Metrics on issue quality (% requiring clarification)
- Auto-suggestions for improving issue descriptions
- Integration with dedicated `/speckit` or `/clarify` commands
