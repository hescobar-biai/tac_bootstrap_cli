---
doc_type: feature
adw_id: feature_Tac_12_task_49
date: 2026-02-02
idk:
  - workflow-helpers
  - agenttemplate-request
  - parallel-exploration
  - slash-commands
  - adw-modules
tags:
  - feature
  - tac-12
  - helpers
related_code:
  - adws/adw_modules/workflow_ops.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2
  - adws/adw_modules/data_types.py
  - adws/adw_modules/agent.py
---

# TAC-12 Helper Functions in workflow_ops.py

**ADW ID:** feature_Tac_12_task_49
**Date:** 2026-02-02
**Specification:** specs/issue-501-adw-feature_Tac_12_task_49-sdlc_planner-add-tac12-helper-functions.md

## Overview

Added four convenient wrapper functions to `workflow_ops.py` that encapsulate TAC-12 command functionality. These helper functions enable ADW workflows to easily invoke advanced agentic features like parallel codebase exploration, enhanced planning with scouts, parallel builds, and code search/summarization without writing custom agent execution code.

## What Was Built

Four new helper functions following the established pattern of existing wrappers like `load_ai_docs()`:

- `scout_codebase()` - Wrapper for `/scout` command to explore codebases with configurable scale
- `plan_with_scouts()` - Wrapper for `/plan_w_scouters` command for enhanced planning with parallel exploration
- `build_in_parallel()` - Wrapper for `/build_in_parallel` command for delegated parallel file creation
- `find_and_summarize()` - Wrapper for `/find_and_summarize` command for code search and summarization

## Technical Implementation

### Files Modified

- `adws/adw_modules/workflow_ops.py` - Added four new helper functions (lines 528-672)
  - Functions follow existing wrapper pattern with consistent logging and error handling
  - All functions use `AgentTemplateRequest` for agent invocation
  - Return `AgentPromptResponse` for uniform error handling across workflows

### Key Changes

- **scout_codebase()** (lines 528-563): Accepts query and optional scale parameter ("quick", "medium", "very thorough")
- **plan_with_scouts()** (lines 566-600): Creates enhanced implementation plans with parallel codebase exploration
- **build_in_parallel()** (lines 603-636): Delegates build implementation to multiple parallel agents from a plan file
- **find_and_summarize()** (lines 639-672): Searches codebase and provides summarized findings

All functions follow the same pattern:
- Use `AgentTemplateRequest` to construct template execution requests
- Call `execute_template()` with the request
- Log debug information for request and response
- Return `AgentPromptResponse` for consistent handling in workflows
- Accept optional `working_dir` parameter for context-aware execution

## How to Use

### In ADW Workflows

Import and use the helper functions directly:

```python
from adw_modules.workflow_ops import scout_codebase, plan_with_scouts, build_in_parallel, find_and_summarize

# Scout the codebase
scout_result = scout_codebase(
    query="authentication middleware",
    adw_id=adw_id,
    logger=logger,
    scale="medium"
)

# Create enhanced plan with scouts
plan_result = plan_with_scouts(
    description="Add JWT token refresh mechanism",
    adw_id=adw_id,
    logger=logger
)

# Build in parallel from plan
build_result = build_in_parallel(
    plan_file="specs/plan.md",
    adw_id=adw_id,
    logger=logger
)

# Find and summarize code
search_result = find_and_summarize(
    search_term="error handling pattern",
    adw_id=adw_id,
    logger=logger
)
```

### Function Signatures

```python
def scout_codebase(
    query: str,
    adw_id: str,
    logger: logging.Logger,
    scale: str = "medium",
    working_dir: Optional[str] = None,
) -> AgentPromptResponse

def plan_with_scouts(
    description: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse

def build_in_parallel(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse

def find_and_summarize(
    search_term: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse
```

## Configuration

No additional configuration required. The functions work with existing ADW infrastructure:

- Uses existing `AgentTemplateRequest` data type
- Leverages `execute_template()` from `adw_modules.agent`
- Compatible with standard ADW logging
- Works with optional working directory specification for multi-workspace scenarios

## Testing

Verify the functions are properly integrated:

```bash
# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check linting and type safety:

```bash
# Linting check
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Test CLI functionality:

```bash
# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is an optional Wave 9 enhancement (Task 49 of 49)
- Functions are convenience wrappers following the Domain-Driven Design (DDD) pattern
- No new dependencies required
- Template file also updated to ensure generated projects include these helpers
- All functions follow consistent patterns with existing `load_ai_docs()` and other wrappers
- Debug logging provides visibility into agent execution for troubleshooting
