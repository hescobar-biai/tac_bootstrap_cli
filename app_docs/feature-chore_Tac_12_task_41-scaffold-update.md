---
doc_type: feature
adw_id: chore_Tac_12_task_41
date: 2026-02-01
idk:
  - scaffold-generation
  - configuration-updates
  - settings-json
  - slash-commands
  - hook-orchestration
  - jinja2-templates
  - file-scaffolding
tags:
  - chore
  - configuration
  - scaffold
  - hooks
  - cli
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2
  - adws/adw_modules/data_types.py
  - .claude/settings.json
---

# Scaffold Service Update with TAC-12 Configuration Files

**ADW ID:** chore_Tac_12_task_41
**Date:** 2026-02-01
**Specification:** specs/issue-493-adw-chore_Tac_12_task_41-scaffold-update.md

## Overview

Updated scaffold service infrastructure and templates to include TAC-12 configuration enhancements. This includes new status line configuration, enhanced hook orchestration patterns, and expanded slash command definitions for multi-agent orchestration workflows.

## What Was Built

- **Status Line Integration**: Added status line configuration to settings.json template
- **Hook Orchestration Enhancement**: Updated hook commands to integrate send_event.py for event tracking
- **Expanded Slash Commands**: Added 17 new multi-agent orchestration commands to data_types.py
- **Template Synchronization**: Ensured Jinja2 templates match generated output files

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/settings.json.j2`: Added statusLine configuration block and updated hook commands to include send_event.py calls
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/data_types.py.j2`: Added 17 new TAC-12 slash commands to SlashCommand type definition
- `.claude/settings.json`: Mirrored template changes for status line and hook orchestration
- `adws/adw_modules/data_types.py`: Mirrored template changes for slash command definitions

### Key Changes

1. **Status Line Configuration**: Added new `statusLine` object in settings.json that references `.claude/status_lines/status_line_main.py` script with `padding: 0` configuration

2. **Hook Event Integration**: All existing hooks (PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit) now include `send_event.py` calls for event tracking and telemetry

3. **Multi-Agent Command Definitions**: Added 17 new slash commands including:
   - Orchestration commands: `/all_tools`, `/build`, `/build_in_parallel`, `/plan`, `/plan_w_docs`, `/plan_w_scouters`, `/scout_plan_build`
   - Advanced planning: `/prime_3`, `/prime_cc`, `/quick-plan`
   - Data utilities: `/find_and_summarize`, `/load_ai_docs`, `/load_bundle`
   - Background execution: `/background`, `/parallel_subagents`

4. **Template Variable Usage**: Maintained Jinja2 template variable `{{ config.project.package_manager.value }}` for flexible package manager selection in generated projects

## How to Use

### For Project Generation

When the scaffold service generates a new project, it will now include:

1. Status line integration in `.claude/settings.json`
2. Enhanced hook chains with event tracking
3. Full range of multi-agent orchestration commands available in slash command definitions

### Manual Verification

Verify the configuration was applied correctly:

```bash
# Check status line configuration
grep -A 5 "statusLine" .claude/settings.json
```

Check hook integration:

```bash
# Verify send_event.py is included in hook chains
grep "send_event.py" .claude/settings.json
```

Verify slash commands:

```bash
# Confirm new commands appear in data_types
grep "/scout_plan_build\|/plan_w_docs\|/prime_cc" adws/adw_modules/data_types.py
```

## Configuration

### Status Line Setup

The status line configuration points to a Python script that customizes Claude Code's output. Projects can modify the script at:

```
.claude/status_lines/status_line_main.py
```

### Hook Event Tracking

The `send_event.py` hook utility requires proper setup in the hook utilities directory. Ensure the file exists at:

```
.claude/hooks/send_event.py
```

### Package Manager Flexibility

The Jinja2 template uses `config.project.package_manager.value` to support different package managers (uv, pip, npm, etc.) in generated projects.

## Testing

Run unit tests for scaffold service:

```bash
cd tac_bootstrap_cli && uv run pytest tests/application/test_scaffold_service.py -v
```

Run full test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify template rendering:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -k "template" -v
```

Lint check for syntax validation:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

- This is part of Wave 7 (Configuration Updates), Task 41 of 49 in the TAC-12 initiative
- The scaffold service uses a builder pattern (ScaffoldPlan) to track all file operations idempotently
- Status line is a new TAC-12 feature enabling custom CLI output customization
- Hook orchestration patterns now support event-driven architecture with send_event.py
- All templates maintain backward compatibility through Jinja2 variable substitution
- The slash command definitions follow the SlashCommand Literal type constraint in data_types.py
