# Chore: Create all_tools.md command file

## Metadata
issue_number: `453`
adw_id: `chore_Ta`
issue_json: `{"number":453,"title":"[Task 1/49] [CHORE] Create all_tools.md command file","body":"## Description\n\nCreate a new slash command that lists all available tools for Claude Code agents.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/all_tools.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/all_tools.md`\n\n## Wave 1 - New Commands (Task 1 of 13)\n\n## Workflow Metadata\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_12_task_1"}`

## Chore Description
Create a new slash command `/all_tools` that lists ALL available tools for Claude Code agents - both built-in Claude Code tools AND MCP tools. This extends the existing `/tools` command which only shows core built-in non-MCP tools.

The command should:
- Dynamically query and list available tools at runtime
- Display results in categorized bullet format with TypeScript-style function signatures
- Split output into two sections: "Built-in Tools" and "MCP Tools"
- Serve as a comprehensive inventory of all agent capabilities

This is a meta-command that instructs the agent's behavior and doesn't require project-specific configuration variables.

## Relevant Files

### Base Repository Files
- `.claude/commands/all_tools.md` - New command file to create in base repo
- `.claude/commands/tools.md` - Reference pattern for command structure (lists only built-in non-MCP tools)

### CLI Template Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2` - New Jinja2 template to create
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/tools.md.j2` - Reference template (3 lines, simple static text)

### Service Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:309` - Add 'all_tools' to commands list in Utility commands section (after 'tools')

## Step by Step Tasks

### Task 1: Create base command file `.claude/commands/all_tools.md`
- Create new file in base repository at `.claude/commands/all_tools.md`
- Write command prompt that instructs agent to:
  - List ALL available tools (both built-in and MCP)
  - Query tools dynamically at runtime
  - Display in categorized bullet format with two sections: "Built-in Tools" and "MCP Tools"
  - Use TypeScript function syntax with parameters for each tool
- Pattern after `/tools` command but extend scope to include MCP tools

### Task 2: Create Jinja2 template `all_tools.md.j2`
- Create template file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`
- Since this is a generic meta-command with no project-specific variables, template can be static text (like tools.md.j2)
- Content should match the base command file created in Task 1
- No Jinja2 variables needed (no `{{ config.* }}` references)

### Task 3: Update `scaffold_service.py` to include command
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Add `"all_tools"` to the commands list at line 309 (in the Utility commands section, right after `"tools"`)
- Maintains logical grouping with related `/tools` command

### Task 4: Validation
- Run validation commands to ensure no regressions
- Verify command files are properly formatted
- Confirm scaffold_service.py syntax is valid

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `cat .claude/commands/all_tools.md` - Verify base command content
- `cat tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2` - Verify template content

## Notes

### Design Decisions (from Auto-Resolved Clarifications)
- **Scope:** ALL tools (built-in + MCP), not just built-in like `/tools`
- **Format:** Categorized bullet list with TypeScript signatures, split into "Built-in Tools" and "MCP Tools" sections
- **Dynamic vs Static:** Dynamic runtime querying (MCP tools vary by project configuration)
- **Config Variables:** None needed - pure instructional prompt like `/tools`
- **Permissions:** None needed - read-only introspection command
- **Relationship to /tools:** Separate complementary command (/tools = focused view, /all_tools = complete inventory)

### Implementation Notes
- No special permissions or hooks required in settings.json
- Template can be minimal/static text (no Jinja2 variables)
- Reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/all_tools.md` cannot be accessed (outside working directory)
- Follow existing `/tools` command pattern and naming conventions
