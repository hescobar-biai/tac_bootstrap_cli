---
doc_type: feature
adw_id: feature_Tac_12_task_34_2_3
date: 2026-02-02
idk:
  - status-line-script
  - environment-variables
  - git-integration
  - graceful-degradation
  - subprocess-handling
  - executable-python-script
  - jinja2-templating
tags:
  - feature
  - cli-integration
  - developer-experience
related_code:
  - .claude/status_lines/status_line_main.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Status Lines Script - Dynamic Agent/Model/Branch Display

**ADW ID:** feature_Tac_12_task_34_2_3
**Date:** 2026-02-02
**Specification:** specs/issue-486-adw-feature_Tac_12_task_34_2_3-status-lines.md

## Overview

Created a lightweight Python script that generates dynamic status line information for Claude Code's status bar configuration. The script displays agent name, model identifier, and current git branch in a single-line format, enabling quick context awareness during agentic workflows without blocking execution.

## What Was Built

- **Status line main script** (`.claude/status_lines/status_line_main.py`) - Executable Python script that queries agent, model, and git branch information
- **Jinja2 template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2`) - Template for CLI generation with project context
- **Scaffold service integration** - Updated `scaffold_service.py` to create status_lines directory and file during project generation

### Key Features

- Reads `CLAUDE_AGENT_NAME` environment variable with graceful fallback to 'unknown'
- Reads `CLAUDE_MODEL` environment variable with graceful fallback to 'unknown'
- Queries current git branch via `git rev-parse --abbrev-ref HEAD` with comprehensive error handling
- Outputs formatted single-line status: `Agent: <name> | Model: <model> | Branch: <branch>`
- Always exits with code 0 (non-blocking; status line is informational only)
- Handles all exceptions gracefully without failing execution

## Technical Implementation

### Files Modified

- `.claude/status_lines/status_line_main.py` - New executable status line script (104 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2` - New Jinja2 template (106 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Updated to register status line file creation (9 lines added)

### Key Changes

1. **Environment Variable Handling**: Implements robust reading of `CLAUDE_AGENT_NAME` and `CLAUDE_MODEL` with `.strip()` to handle whitespace and empty string fallbacks to 'unknown'

2. **Subprocess Git Integration**: Uses `git rev-parse --abbrev-ref HEAD` with timeout (2 seconds), capture output, and comprehensive exception handling covering FileNotFoundError (git not installed), CalledProcessError (not a git repo), TimeoutExpired, and generic Exception

3. **Graceful Degradation**: All function components return 'unknown' on any error, ensuring status line always produces output

4. **Executable Script Pattern**: Follows existing hook patterns (pre_tool_use.py, post_tool_use.py) with shebang directive `#!/usr/bin/env python3` and proper module-level documentation

5. **Template Consistency**: Jinja2 template mirrors base script structure, includes project name via `{{ config.project.name }}` in docstring for context during generation

6. **Scaffold Integration**: Registers status line file creation in scaffold_service with `executable=True` flag to preserve shebang permissions

## How to Use

### Direct Execution

Test the status line script directly:

```bash
uv run .claude/status_lines/status_line_main.py
```

With environment variables set:

```bash
CLAUDE_AGENT_NAME="MyAgent" CLAUDE_MODEL="claude-opus" uv run .claude/status_lines/status_line_main.py
```

### Claude Code Integration

The script is configured as executable via Claude Code's status line configuration in `.claude/settings.json`. When Claude Code invokes the status line command, it:

1. Sets `CLAUDE_AGENT_NAME` and `CLAUDE_MODEL` environment variables at runtime
2. Executes the status line script
3. Captures and displays the single-line output in the status bar

### CLI Project Generation

When generating a new project with TAC Bootstrap CLI, the status_lines directory and script are automatically created as part of the `.claude/` scaffold:

```bash
uv run tac_bootstrap_cli/main.py generate --project my-project
```

## Configuration

### Environment Variables

- `CLAUDE_AGENT_NAME`: Agent name displayed in status line (set by Claude Code at runtime)
- `CLAUDE_MODEL`: Model identifier displayed in status line (set by Claude Code at runtime)

### Scaffold Configuration

In `scaffold_service.py`, the status line file is registered with:
- `template`: Points to Jinja2 template for CLI generation
- `executable=True`: Preserves executable permissions and shebang directive
- `reason`: Documents purpose in scaffold plan

## Testing

### Smoke Test

Test the script with no environment variables (all fallback to 'unknown'):

```bash
uv run .claude/status_lines/status_line_main.py
```

Expected output:
```
Agent: unknown | Model: unknown | Branch: unknown
```

### With Environment Variables

Test with environment variables set:

```bash
CLAUDE_AGENT_NAME="TestAgent" CLAUDE_MODEL="claude-haiku" uv run .claude/status_lines/status_line_main.py
```

Expected output (branch depends on current git state):
```
Agent: TestAgent | Model: claude-haiku | Branch: <current-branch>
```

### Edge Cases

Test graceful handling of edge cases:

```bash
# Non-git directory (temporary directory)
mkdir -p /tmp/not-git && cd /tmp/not-git && uv run /path/to/status_line_main.py

# Empty environment variables
CLAUDE_AGENT_NAME="" CLAUDE_MODEL="" uv run .claude/status_lines/status_line_main.py

# Whitespace-only environment variables
CLAUDE_AGENT_NAME="   " CLAUDE_MODEL="   " uv run .claude/status_lines/status_line_main.py
```

All should output fallback format with 'unknown' for missing/invalid values.

### Integration Testing

Run full test suite to verify no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
uv run ruff check .
uv run mypy tac_bootstrap/
```

## Notes

- Script follows existing hook patterns (pre_tool_use.py, post_tool_use.py) for consistency with project conventions
- Status line is intentionally lightweight and non-blocking to avoid performance impact on Claude Code's status bar rendering
- Timeout of 2 seconds on git subprocess prevents hanging if git is slow or network-dependent
- Exit code is always 0 to ensure status line failures never interrupt agentic workflows
- Template uses project name in docstring for context; runtime values (agent, model, branch) are environment/subprocess-based only
- Shebang directive enables direct execution via `uv run` when configured in Claude Code settings
- This implementation is Wave 5, Task 34 of the TAC Bootstrap development plan

