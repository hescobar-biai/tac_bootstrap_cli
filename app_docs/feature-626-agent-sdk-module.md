---
doc_type: feature
adw_id: feature_Tac_14_Task_5
date: 2026-02-04
idk:
  - agent-sdk
  - pydantic-models
  - type-safety
  - programmatic-agents
  - validation
  - enums
  - hook-events
  - class-2
tags:
  - feature
  - agent-sdk
  - infrastructure
  - templates
related_code:
  - adws/adw_modules/adw_agent_sdk.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Agent SDK Module (BASE + TEMPLATES)

**ADW ID:** feature_Tac_14_Task_5
**Date:** 2026-02-04
**Specification:** specs/issue-626-adw-feature_Tac_14_Task_5-sdlc_planner-agent-sdk-module.md

## Overview

The Agent SDK module provides a complete, type-safe Pydantic layer for programmatic control of the Claude Agent SDK. This foundational infrastructure enables database-backed ADW workflows and orchestration capabilities by providing validated abstractions for agent configuration, hooks, settings, and messages.

## What Was Built

- **BASE Module**: Complete `adw_agent_sdk.py` module (1655 lines) with Pydantic models, enums, validators, and docstrings
- **Template Copy**: Static `.j2` template copy for project generation (no Jinja2 variables)
- **Registration**: Template registered in `scaffold_service.py` for automatic inclusion in generated projects
- **PEP 723 Header**: Inline script metadata specifying Python 3.11+ and dependencies (pydantic>=2.0, claude-agent-sdk>=0.1.18, rich>=13.0)

## Technical Implementation

### Files Modified

**Created:**
- `adws/adw_modules/adw_agent_sdk.py`: BASE module with complete SDK abstractions (1655 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2`: Static template copy for project generation

**Modified:**
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added template registration in `_add_adw_files` method

### Key Changes

**Enums Defined:**
- `ModelName`: Claude model versions (Opus 4.5, Sonnet 4.5, Haiku 4.5) with convenience aliases
- `SettingSource`: Settings sources (USER, PROJECT) for filesystem-based skill loading
- `HookEventName`: Hook event types for Python SDK (PreToolUse, PostToolUse, etc.) and TypeScript SDK
- `PermissionDecision`: Permission outcomes for PreToolUse hooks (ALLOW, DENY, ASK)

**Pydantic Models:**
- Base configuration models for agent settings, tools, hooks
- Message models for user prompts, assistant responses, tool calls
- Hook configuration with event-based validation
- Complete type safety with field validators and ConfigDict settings

**Architecture:**
- Abstract base classes for extensibility
- Async generator support for streaming operations
- Type aliases for complex callback signatures
- PEP 723 inline metadata for dependency management

## How to Use

### In Generated Projects

The Agent SDK module is automatically included when generating a new project with TAC Bootstrap CLI:

```bash
uv run tac-bootstrap init my-project
```

The module will be available at `adws/adw_modules/adw_agent_sdk.py` in the generated project.

### Import and Use Types

```python
from adw_modules.adw_agent_sdk import (
    ModelName,
    HookEventName,
    PermissionDecision,
    # Import other models as needed
)

# Use enum values for type-safe configuration
model = ModelName.SONNET_4_5
hook_event = HookEventName.PRE_TOOL_USE
decision = PermissionDecision.ALLOW
```

### In ADW Workflows

Higher-level ADW workflows (Tasks 6-14) use this module for programmatic agent control:

```python
# Example: Configure agent with type safety
agent_config = {
    "model": ModelName.SONNET,
    "hooks": [
        {
            "event": HookEventName.PRE_TOOL_USE,
            "handler": my_permission_handler
        }
    ]
}
```

## Configuration

### PEP 723 Dependencies

The module uses inline script metadata (PEP 723) for dependency specification:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pydantic>=2.0",
#   "claude-agent-sdk>=0.1.18",
#   "rich>=13.0",
# ]
# ///
```

**Note:** Source requires Python 3.11+, while project baseline is 3.10+. Module was copied unchanged per specification. Verify Python version compatibility when using in 3.10 environments.

### Template Registration

Template is registered in `scaffold_service.py`:

```python
modules = [
    # ... other modules ...
    ("adw_agent_sdk.py", "Agent SDK type-safe layer"),
]
```

This ensures the module is automatically included in the `adws/adw_modules/` directory of generated projects.

## Testing

### Verify BASE Module Exists

```bash
ls -la adws/adw_modules/adw_agent_sdk.py
```

### Check Line Count (Should be 1655)

```bash
wc -l adws/adw_modules/adw_agent_sdk.py
```

### Validate PEP 723 Header

```bash
head -n 8 adws/adw_modules/adw_agent_sdk.py
```

### Syntax Check BASE File

```bash
python3 -m py_compile adws/adw_modules/adw_agent_sdk.py
```

### Verify Template Exists

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2
```

### Check Template Line Count

```bash
wc -l tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/adw_agent_sdk.py.j2
```

### Verify Template Registration

```bash
grep -n "adw_agent_sdk.py" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Type Check

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test CLI

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Module Purpose

The module provides an abstract typed layer for Claude Agent SDK control. It is intentionally generic and can be used for any Agent SDK use case. ADW-specific concerns belong in higher-level modules like `adw_agents.py`.

### Static Template Strategy

Per specification requirement "sin modificaciones" (without modifications), the `.j2` template is a byte-identical copy of the BASE module with no Jinja2 variable substitutions. The SDK module should be identical across all generated projects as it provides foundational type definitions rather than project-specific customization.

### Dependencies for Future Tasks

This module is foundational infrastructure that enables all subsequent TAC-14 Class 2 and Class 3 tasks:
- **Task 7**: Database models need SDK enums for agent configuration
- **Task 8**: Database operations need SDK types for CRUD
- **Task 9**: Logging needs SDK message types
- **Task 10**: Workflows need full SDK for agent orchestration
- **Task 11**: WebSockets need SDK types for event streaming

### Python Version Consideration

Source file requires Python 3.11+ in PEP 723 header, but project baseline is Python 3.10+. The module was copied unchanged per specification. Users running Python 3.10 should verify compatibility or adjust the `requires-python` field if needed.

### Component Breakdown

**Enums (4 total):**
- `ModelName` (lines 43-54): Claude model identifiers
- `SettingSource` (lines 57-62): Settings source types
- `HookEventName` (lines 69-87): Hook event identifiers
- `PermissionDecision` (lines 89-94): Permission outcomes

**Models:**
- Configuration models for agent settings
- Hook event models with validators
- Message models for prompts and responses
- Tool call and result models
- Async callback type aliases

All models use Pydantic v2 with field validators, ConfigDict settings, and comprehensive docstrings for IDE support.
