---
doc_type: feature
adw_id: chore_Tac_12_task_42
date: 2026-02-02
idk:
  - slash-command-configuration
  - model-mapping
  - command-orchestration
  - type-safety
  - TAC-12
tags:
  - feature
  - configuration
  - command-system
related_code:
  - adws/adw_modules/agent.py
  - adws/adw_modules/data_types.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2
---

# TAC-12: Slash Commands Model Map Configuration

**ADW ID:** chore_Tac_12_task_42
**Date:** 2026-02-02
**Specification:** issue-494-adw-chore_Tac_12_task_42-sdlc_planner-add-commands-model-map.md

## Overview

Added model mappings for 13 new TAC-12 commands to the SLASH_COMMAND_MODEL_MAP dictionary in agent.py. This ensures each slash command uses the appropriate Claude model (haiku, sonnet, or opus) based on computational complexity and the execution model set (base or heavy).

## What Was Built

Model mappings for TAC-12 planning and orchestration commands:

- `/all_tools` - Lightweight utilities listing tool information
- `/build` - Sequential code building and implementation
- `/build_in_parallel` - Parallel build agent delegation
- `/find_and_summarize` - Code searching and summarization
- `/load_ai_docs` - AI documentation loading (duplicate entry updated)
- `/load_bundle` - Context bundle loading (updated with better model selection)
- `/parallel_subagents` - Parallel agent orchestration (duplicate entry updated)
- `/plan` - Complex opus-based planning
- `/plan_w_docs` - Planning with documentation exploration
- `/plan_w_scouters` - Planning with parallel codebase exploration
- `/prime_3` - Deep context loading and priming
- `/prime_cc` - Claude Code-specific priming (duplicate entry updated)
- `/scout_plan_build` - End-to-end workflow orchestration

## Technical Implementation

### Files Modified

- **`adws/adw_modules/agent.py:31-87`** - Production SLASH_COMMAND_MODEL_MAP dictionary with 13 new command entries and TAC-12 grouping comment
- **`adws/adw_modules/data_types.py:51-100`** - SlashCommand Literal type definition updated with 13 new command names for type safety
- **`tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/agent.py.j2`** - Template version kept in sync with production file

### Key Changes

1. **Added TAC-12 Section** - Grouped 13 new commands under "# TAC-12: Planning and orchestration" comment in SLASH_COMMAND_MODEL_MAP for organizational clarity

2. **Model Assignments**:
   - **Haiku (lightweight)**: `/all_tools` (haiku for base & heavy)
   - **Sonnet (standard)**: `/build`, `/find_and_summarize`, `/load_ai_docs`, `/prime_3`, `/prime_cc` (sonnet base, sonnet/opus heavy mix)
   - **Opus (complex)**: `/plan` (opus for both base & heavy), `/build_in_parallel`, `/plan_w_docs`, `/plan_w_scouters`, `/scout_plan_build` (sonnet base, opus heavy)

3. **Duplicate Entry Resolution** - Corrected existing entries for `/load_ai_docs`, `/load_bundle`, `/parallel_subagents`, and `/prime_cc` that appeared earlier with different model configurations

4. **Type Safety** - Updated SlashCommand Literal type with all 13 new commands to enable static type checking throughout the codebase

5. **Template Synchronization** - Ensured template file (agent.py.j2) maintains identical configuration for consistent code generation

## How to Use

The model mapping is automatically used when executing slash commands through the ADW system:

1. Execute a slash command via `execute_template()` function
2. The `get_model_for_slash_command()` function looks up the command in SLASH_COMMAND_MODEL_MAP
3. Loads ADW state to determine model_set (base or heavy)
4. Returns appropriate model for the command and model set
5. Claude Code executes with the selected model

```python
from adws.adw_modules.agent import get_model_for_slash_command
from adws.adw_modules.data_types import AgentTemplateRequest

# Create template request
request = AgentTemplateRequest(
    agent_name="planner",
    slash_command="/plan",  # Complex planning uses opus
    args=["requirements.md"],
    adw_id="tac12_demo"
)

# Get appropriate model (returns "opus" for /plan)
model = get_model_for_slash_command(request)
```

## Configuration

Model assignments follow these principles:

- **Haiku**: Information tools requiring minimal reasoning
- **Sonnet**: General-purpose commands with standard complexity
- **Opus**: Complex planning, orchestration, and multi-step workflows

The model_set in ADW state determines which tier is used:
- **base**: Uses first value in mapping (typically sonnet)
- **heavy**: Uses second value in mapping (typically opus for complex operations)

## Testing

Verify the command mappings are correctly configured:

```bash
# Run type validation tests to ensure all commands are recognized
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify specific command model selection:

```bash
# Check that /plan uses opus (heavy execution)
cd tac_bootstrap_cli && python -c "
from adws.adw_modules.agent import SLASH_COMMAND_MODEL_MAP
print(SLASH_COMMAND_MODEL_MAP['/plan'])
"
```

Smoke test the CLI to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verify linting compliance:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

- All 13 commands are TAC-12 additions representing significant expansion of the command infrastructure
- Model assignments were pre-designed based on computational complexity and are considered authoritative
- The Python type system enforces that only mapped commands can be executed
- Both production and template files must remain synchronized; there is no automatic sync mechanism
- Duplicate command entries for `/load_ai_docs`, `/load_bundle`, `/parallel_subagents`, and `/prime_cc` were consolidated to use the TAC-12 values
- The heavy model set enables more expensive operations (opus) for computation-intensive commands like planning and orchestration
