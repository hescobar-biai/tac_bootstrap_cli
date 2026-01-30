---
doc_type: feature
adw_id: chore_Tac_12_task_1
date: 2026-01-30
idk:
  - slash-command
  - claude-code
  - mcp-tools
  - tool-discovery
  - agent-capabilities
  - jinja2-template
  - scaffold-service
tags:
  - feature
  - command
  - documentation
related_code:
  - .claude/commands/all_tools.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# /all_tools Slash Command

**ADW ID:** chore_Tac_12_task_1
**Date:** 2026-01-30
**Specification:** specs/issue-453-adw-chore_Tac_12_task_1-chore_planner-create-all-tools-command.md

## Overview

Created a comprehensive `/all_tools` slash command that provides a single reference point for Claude Code agents to view all available tools. This includes built-in development tools, MCP integrations (GitHub, Playwright, Firecrawl), task management tools, and specialized utilities. The command serves as complete tool documentation for agent workflows.

## What Was Built

- **Base Command File**: `.claude/commands/all_tools.md` with comprehensive tool listings organized by category
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2` for CLI generation
- **Scaffold Integration**: Updated `scaffold_service.py` to include `all_tools` in the commands list

## Technical Implementation

### Files Modified

- `.claude/commands/all_tools.md`: New slash command file listing 93 lines of tool documentation organized into 7 major categories:
  - Built-in Development Tools (7 tools)
  - Task & Planning Tools (6 tools)
  - MCP GitHub Integration (19 tools)
  - MCP Browser Automation (9 tools)
  - MCP Web Scraping (5 tools)
  - MCP Context7 Library Documentation (2 tools)
  - MCP Git Operations (9 tools)
  - Specialized Tools (4 tools)
  - MCP Server Management (5 tools)
  - MCP Resources (2 tools)

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`: Jinja2 template with static content matching the base file (no dynamic variables, following the `tools.md.j2` pattern)

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:310`: Added `'all_tools'` to the commands list in the utility commands section, placed after `'tools'` for logical grouping

### Key Changes

- Created comprehensive tool reference listing all Claude Code capabilities in bullet format with signatures
- Organized tools into logical categories for easy navigation
- Followed existing command pattern from `tools.md` - simple header, clear instruction, concise documentation
- Used static Jinja2 template with no variables for maximum portability
- Integrated into scaffold service for automatic inclusion in generated projects

## How to Use

1. **As a User**: Invoke the command in Claude Code to view all available tools:
   ```
   /all_tools
   ```

2. **In Generated Projects**: The command is automatically included when scaffolding new projects:
   ```bash
   uv run tac-bootstrap scaffold my-project
   ```
   The `.claude/commands/all_tools.md` file will be created in the new project.

3. **For Agent Reference**: Agents can use this command to discover capabilities before selecting appropriate tools for tasks.

## Configuration

No configuration required. The command is a static documentation file that works out of the box.

### Template Structure

The Jinja2 template uses static content with no variables:
```jinja2
# List All Available Tools

List all available tools including both built-in development tools and MCP integrations...
```

This follows the pattern established by other documentation commands in the TAC Bootstrap system.

## Testing

Verify the base file exists and has correct content:
```bash
ls -la .claude/commands/all_tools.md
```

Verify the template exists and matches the base file:
```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2
```

Verify command is registered in scaffold service:
```bash
grep -n "all_tools" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

Run unit tests to ensure no regressions:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check code quality:
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test the CLI:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is Wave 1, Task 1 of 13 new commands being added to TAC Bootstrap
- The command provides 68+ tools across 10 categories for complete agent capability discovery
- Following the established pattern from `tools.md` ensures consistency across all slash commands
- Static template approach (no Jinja2 variables) maximizes portability and simplifies maintenance
- Tool signatures include optional parameters marked with `?` for clarity (e.g., `page?`, `perPage?`)
- The command complements the existing `/tools` command by providing more comprehensive MCP tool documentation
