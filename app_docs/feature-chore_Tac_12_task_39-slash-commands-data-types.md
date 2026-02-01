---
doc_type: feature
adw_id: chore_Tac_12_task_39
date: 2026-02-01
idk:
  - slash-commands
  - type-definitions
  - literal-types
  - multi-agent-orchestration
  - data-types
  - python-typing
  - template-synchronization
tags:
  - chore
  - type-system
  - data-types
  - adw
related_code:
  - adws/adw_modules/data_types.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2
---

# Add TAC-12 Commands to SlashCommand Literal

**ADW ID:** chore_Tac_12_task_39
**Date:** 2026-02-01
**Specification:** specs/issue-491-adw-chore_Tac_12_task_39-slash-commands-datatypes.md

## Overview

Updated the SlashCommand Literal type definition to include 15 new TAC-12 multi-agent orchestration commands. This was a type definition update only—no runtime registration or SLASH_COMMAND_MODEL_MAP changes were required. Both the base file and Jinja2 template were synchronized to maintain consistency across the codebase.

## What Was Built

- Added 15 new TAC-12 slash commands to the SlashCommand Literal type definition
- Updated both base implementation and Jinja2 template to maintain synchronization
- Organized commands with a descriptive comment block for maintainability
- All commands properly formatted with trailing commas and correct string quotes

### TAC-12 Commands Added

1. `/all_tools` - List all available tools
2. `/build` - Build implementation from plan
3. `/build_in_parallel` - Parallel build implementation
4. `/find_and_summarize` - Find and summarize codebase
5. `/load_ai_docs` - Load AI documentation
6. `/load_bundle` - Load context bundle
7. `/parallel_subagents` - Launch parallel subagents
8. `/plan` - Create implementation plan
9. `/plan_w_docs` - Plan with documentation exploration
10. `/plan_w_scouters` - Plan with parallel scout exploration
11. `/prime_3` - Deep context loading
12. `/prime_cc` - Prime Claude Code context
13. `/scout_plan_build` - Scout, plan, and build orchestration
14. `/quick-plan` - Quick planning workflow
15. `/background` - Background command execution

## Technical Implementation

### Files Modified

- `adws/adw_modules/data_types.py` (lines 75-90): Added TAC-12 comment block and 15 new commands to SlashCommand Literal
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2` (lines 75-90): Applied identical changes to Jinja2 template for project generation

### Key Changes

- Extended SlashCommand Literal with new multi-agent orchestration commands
- Added `# TAC-12: Multi-agent orchestration commands` comment for logical grouping
- Maintained proper Python syntax with trailing commas after each entry
- Ensured synchronization between base file and template file
- No changes to SLASH_COMMAND_MODEL_MAP—this was a type-only update

## How to Use

The SlashCommand Literal acts as a type contract/whitelist for available commands in the ADW system. These new commands are now recognized by the type system and can be referenced in code that expects SlashCommand types.

1. Import the updated SlashCommand type from data_types.py:
   ```python
   from tac_bootstrap.adws.adw_modules.data_types import SlashCommand
   ```

2. Use in type annotations:
   ```python
   def execute_command(command: SlashCommand) -> None:
       # Command is now type-safe and can be any of the 25+ defined slash commands
       pass
   ```

3. The commands are available for slash command implementations without requiring runtime registration changes

## Configuration

No additional configuration is required. The SlashCommand Literal is automatically updated in both the base implementation and Jinja2 templates used for new project generation.

## Testing

All validation tests passed with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
# Result: 716 passed, 2 skipped in 4.85s
```

```bash
# Code style check
cd tac_bootstrap_cli && uv run ruff check .
# Result: All checks passed!
```

```bash
# Smoke test to verify CLI functionality
cd tac_bootstrap_cli && uv run tac-bootstrap --help
# Result: CLI displays help correctly with all commands available
```

## Notes

- This is a pure type definition update with no logic changes or runtime registration required
- The order of entries in a Python Literal is unordered at runtime, but logical grouping improves code readability and maintainability
- Both the base file and template must remain synchronized to ensure consistent behavior across new project generations
- The SlashCommand Literal serves as a contract defining all available commands in the ADW ecosystem
- Commands are grouped by category (issue classification, ADW workflows, documentation, installation/setup, and multi-agent orchestration)
