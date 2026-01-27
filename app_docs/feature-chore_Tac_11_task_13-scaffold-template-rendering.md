---
doc_type: feature
adw_id: chore_Tac_11_task_13
date: 2026-01-27
idk:
  - scaffold-service
  - template-rendering
  - jinja2
  - agentic-layer
  - hooks
  - slash-commands
  - gitkeep
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2
---

# Scaffold Template Rendering Update

**ADW ID:** chore_Tac_11_task_13
**Date:** 2026-01-27
**Specification:** specs/issue-362-adw-chore_Tac_11_task_13-update-scaffold-render-templates.md

## Overview

Extended the scaffold service to render newly created templates for the agentic layer, including two new utility slash commands (`/scout` and `/question`), a security validation hook (`dangerous_command_blocker.py`), and directory structures for agent state management (`security_logs` and `scout_files`).

## What Was Built

- Added `/scout` command template to scaffold rendering
- Added `/question` command template to scaffold rendering
- Added `dangerous_command_blocker.py` security hook to scaffold rendering
- Added `agents/security_logs/` directory with `.gitkeep` for security hook logs
- Added `agents/scout_files/` directory with `.gitkeep` for scout command state

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Updated scaffold service to include new templates in rendering process

### Key Changes

- Extended `_add_claude_files` method (lines 289-324) to include two new utility commands: `scout` and `question` in the commands list
- Added `dangerous_command_blocker.py` to the hooks list in `_add_claude_files` method with description "Security validation hook"
- Extended `_add_directories` method (lines 119-155) to create two new agent directories: `agents/security_logs` and `agents/scout_files`
- Added `.gitkeep` files for both new directories to preserve them in Git with empty content
- Maintained existing patterns for file rendering, using Jinja2 templates with `config` context variable

## How to Use

### Generate New Project with Updated Templates

1. Create a project configuration file or use default settings
2. Run the TAC Bootstrap CLI to scaffold a new project:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap scaffold --name my-project
```

3. Verify the new templates are rendered in the generated project:
   - Check `.claude/commands/scout.md` exists
   - Check `.claude/commands/question.md` exists
   - Check `.claude/hooks/dangerous_command_blocker.py` exists
   - Check `agents/security_logs/.gitkeep` exists
   - Check `agents/scout_files/.gitkeep` exists

### Verify Template Rendering

Use the following commands to verify the scaffold service works correctly:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

## Configuration

No new configuration variables are required. The new templates use the existing `config` context variable available in all Jinja2 templates. The scaffold service automatically includes these templates when rendering the agentic layer structure.

## Testing

### Run Unit Tests

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli
uv run ruff check .
```

### CLI Smoke Test

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

## Notes

- The `/scout` command enables parallel codebase exploration for agent workflows
- The `/question` command supports interactive user queries during agent execution
- The `dangerous_command_blocker.py` hook provides security validation before executing potentially dangerous commands
- The `.gitkeep` files use `content=""` and `FileAction.CREATE` pattern, not Jinja2 template rendering
- The `dangerous_command_blocker.py` hook is marked as `executable=True` like other hook files
- Directory structure follows the existing pattern with descriptive reasons for each directory
- All changes maintain backward compatibility with existing scaffold functionality
