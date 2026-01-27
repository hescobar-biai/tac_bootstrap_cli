---
doc_type: feature
adw_id: chore_Tac_11_task_14
date: 2026-01-27
idk:
  - slash-command
  - model-map
  - configuration
  - agent
  - tac-11
  - sonnet
tags:
  - feature
  - configuration
  - agent
related_code:
  - adws/adw_modules/agent.py
---

# TAC-11 Slash Command Model Map Update

**ADW ID:** chore_Tac_11_task_14
**Date:** 2026-01-27
**Specification:** specs/issue-332-adw-chore_Tac_11_task_14-chore_planner-update-slash-command-model-map.md

## Overview

This feature adds two new TAC-11 slash commands (`/scout` and `/question`) to the `SLASH_COMMAND_MODEL_MAP` configuration in the agent module. These lightweight exploration and clarification commands use the "sonnet" model for optimal performance without requiring the heavyweight "opus" model.

## What Was Built

- Added `/scout` command mapping to SLASH_COMMAND_MODEL_MAP
- Added `/question` command mapping to SLASH_COMMAND_MODEL_MAP
- Both commands configured to use "sonnet" model for base and heavy model sets
- Added descriptive inline comments following existing TAC-9 and TAC-10 patterns

## Technical Implementation

### Files Modified

- `adws/adw_modules/agent.py`: Added two new entries to the `SLASH_COMMAND_MODEL_MAP` dictionary (lines 69-71)

### Key Changes

- Extended the `SLASH_COMMAND_MODEL_MAP` dictionary with TAC-11 commands section
- `/scout`: Maps to `{"base": "sonnet", "heavy": "sonnet"}` for codebase exploration tasks
- `/question`: Maps to `{"base": "sonnet", "heavy": "sonnet"}` for clarification and question-answering tasks
- Added category comment: `# TAC-11: Exploration and clarification (lightweight)`
- Positioned entries logically after TAC-10 commands to maintain chronological organization

## How to Use

The updated model map is used automatically by the `get_model_for_slash_command()` function in `agent.py`. When agents execute `/scout` or `/question` commands, the system will now correctly select the "sonnet" model regardless of whether the "base" or "heavy" model set is active.

1. Commands are invoked in slash command files (e.g., `.claude/commands/scout.md`)
2. The agent module reads the `SLASH_COMMAND_MODEL_MAP` to determine which model to use
3. For both `/scout` and `/question`, the system uses "sonnet" for optimal balance of speed and capability

## Configuration

The `SLASH_COMMAND_MODEL_MAP` is a constant dictionary defined at module level in `agent.py`:

```python
SLASH_COMMAND_MODEL_MAP: Final[Dict[SlashCommand, Dict[ModelSet, str]]] = {
    # ... existing commands ...
    # TAC-11: Exploration and clarification (lightweight)
    "/scout": {"base": "sonnet", "heavy": "sonnet"},
    "/question": {"base": "sonnet", "heavy": "sonnet"},
}
```

Model options:
- `"opus"`: Most capable, slowest, most expensive
- `"sonnet"`: Balanced performance (recommended for lightweight commands)
- `"haiku"`: Fastest, least expensive, suitable for simple tasks

## Testing

Verify the configuration syntax is valid:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check for linting issues:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test the CLI still functions:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verify the agent module loads without errors:

```bash
python -c "from adws.adw_modules.agent import SLASH_COMMAND_MODEL_MAP; print('/scout' in SLASH_COMMAND_MODEL_MAP)"
```

## Notes

- This is a low-risk configuration change that only adds new entries without modifying existing ones
- The choice of "sonnet" for both commands reflects their lightweight nature compared to heavyweight implementation commands that require "opus"
- The TAC-11 commands focus on exploration (`/scout`) and clarification (`/question`), which don't need the full reasoning power of opus
- The model map follows the established pattern of TAC-9 and TAC-10 integrations with clear category comments
- Future TAC integrations should follow this pattern of chronologically organized sections with descriptive comments
