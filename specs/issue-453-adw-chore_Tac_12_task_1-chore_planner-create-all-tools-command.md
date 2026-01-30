# Chore: Create all_tools.md command file

## Metadata
issue_number: `453`
adw_id: `chore_Tac_12_task_1`
issue_json: `{"number":453,"title":"[Task 1/49] [CHORE] Create all_tools.md command file","body":"## Description\n\nCreate a new slash command that lists all available tools for Claude Code agents.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/all_tools.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/all_tools.md`\n\n## Wave 1 - New Commands (Task 1 of 13)\n\n## Workflow Metadata\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_12_task_1"}`

## Chore Description
Create a comprehensive `/all_tools` slash command that lists all available tools for Claude Code agents. This includes both MCP (Model Context Protocol) tools and built-in Claude Code development tools. The command should provide a single reference point for agents to understand all available capabilities.

Following the pattern of the existing `/tools` command, this will be a static documentation command that displays tool listings in bullet format with descriptions and usage examples.

## Relevant Files

### Files to Read
- `.claude/commands/tools.md` - Existing tools command showing the pattern to follow (simple header, instruction, bullet format)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/tools.md.j2` - Existing Jinja2 template showing static content pattern (no dynamic variables)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (line 279-324) - Commands list where we need to add 'all_tools'

### New Files to Create
- `.claude/commands/all_tools.md` - Base command file for the TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2` - Jinja2 template for CLI generation

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create base all_tools.md command file
- Create `.claude/commands/all_tools.md` with comprehensive tool listings
- Follow the pattern from `tools.md`: brief header (# List All Available Tools), clear instruction
- Include sections for:
  - Built-in development tools (Read, Write, Edit, Bash, Glob, Grep, etc.)
  - MCP tools (GitHub, Playwright, Firecrawl, etc.)
  - Task management tools (Task, TodoWrite, EnterPlanMode, etc.)
- Use bullet format for tool listings
- Include brief descriptions and key parameters for each tool
- Keep it concise and actionable, matching the style of existing commands

### Task 2: Create Jinja2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2`
- Copy the exact content from `.claude/commands/all_tools.md`
- Use static content with NO Jinja2 variables (following the tools.md.j2 pattern)
- Ensure the template is simple and consistent with existing command templates

### Task 3: Update scaffold_service.py
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Add 'all_tools' to the commands list in the `_add_claude_files` method (around line 309)
- Place it in the "# Utility commands" section, after 'tools' for logical grouping
- Ensure the placement maintains alphabetical/logical ordering

### Task 4: Validate changes
- Run all validation commands to ensure zero regressions
- Verify that the new command file exists and has correct content
- Verify that the template exists and matches the base file
- Verify that scaffold_service.py includes 'all_tools' in the commands list

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `ls -la .claude/commands/all_tools.md` - Verify base file exists
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/all_tools.md.j2` - Verify template exists
- `grep -n "all_tools" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Verify command is in list

## Notes

### Content Guidelines
The all_tools.md command should be comprehensive but concise. It should list:

1. **Built-in Development Tools**: Core file operation tools that agents use for coding tasks
   - Read, Write, Edit, Glob, Grep, Bash, NotebookEdit
   - Include key parameters and common use cases

2. **MCP Tools**: External integrations available via Model Context Protocol
   - GitHub tools (search_code, create_pull_request, list_issues, etc.)
   - Playwright browser automation tools
   - Firecrawl web scraping tools
   - Include brief descriptions of what each category provides

3. **Task & Planning Tools**: Agent workflow and coordination tools
   - Task, TodoWrite, EnterPlanMode, ExitPlanMode, AskUserQuestion
   - Skill tool for executing slash commands

4. **Specialized Tools**: Domain-specific capabilities
   - WebFetch, WebSearch
   - KillShell, TaskOutput

### Pattern to Follow
Based on tools.md:
```markdown
# List All Available Tools

List all available tools including both built-in development tools and MCP integrations. Display in bullet format with brief descriptions and key parameters.

## Built-in Development Tools
- Read(file_path) - Read file contents with line numbers
- Write(file_path, content) - Write or overwrite files
[...]

## MCP Tools
### GitHub Integration
- search_code(query) - Search code across repositories
[...]

### Browser Automation (Playwright)
[...]
```

### Reference Unavailable
The reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/all_tools.md` is on an external volume and may not be accessible. We'll create comprehensive content based on:
- Claude Code system capabilities
- Existing command patterns (tools.md)
- MCP tool documentation

This approach ensures we create authoritative, complete documentation without depending on the external reference.
