# Chore: Update documentation for /scout and /question commands

## Metadata
issue_number: `356`
adw_id: `chore_Tac_11_task_16`
issue_json: `{"number":356,"title":"Update documentation in tac_bootstrap_cli/docs/commands.md","body":"chore\n/adw_sdlc_iso\n/adw_id: chore_Tac_11_task_16\n\n\nDocument the new /scout and /question commands.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`\n\n**Implementation details:**\n- Add /scout command documentation under \"Agent Orchestration Commands\"\n- Add /question command documentation under \"Research Commands\" or new section\n- Include usage examples and options\n"}`

## Chore Description
Add documentation for two new slash commands (`/scout` and `/question`) to the TAC Bootstrap CLI documentation file. The `/scout` command enables parallel codebase exploration with configurable search strategies, while `/question` provides read-only Q&A about project structure and architecture.

## Relevant Files
Files needed to complete this chore:

- `tac_bootstrap_cli/docs/commands.md` - Main documentation file where new command documentation will be added. Currently has sections for various command categories, needs additions for /scout and /question.
- `.claude/commands/scout.md` - Complete specification for the /scout command including variables, workflow, and examples. Source of truth for /scout documentation.
- `.claude/commands/question.md` - Complete specification for the /question command including variables, workflow, and report format. Source of truth for /question documentation.

### New Files
No new files required.

## Step by Step Tasks

### Task 1: Add /scout command to Agent Delegation Commands section
- Locate the "Agent Delegation Commands" section (around line 133) in `tac_bootstrap_cli/docs/commands.md`
- Add `/scout <task> [scale]` entry to the command table with description "Find relevant files using parallel exploration strategies"
- Create a detailed subsection (###) for `/scout` after the `/parallel_subagents` subsection
- Document the SCALE parameter (optional, range 2-10, default 4) and its effect on number of parallel strategies
- Include usage examples relevant to TAC Bootstrap:
  - `/scout "add authentication to API endpoints"` - basic usage
  - `/scout "implement caching layer" 6` - with custom scale
  - `/scout "fix database connection pooling" 2` - quick exploration
- Document the 4 core search strategies (file patterns, content search, architecture, dependencies)
- Mention the output location: `agents/scout_files/relevant_files_{timestamp}.md`
- Note when to use vs. not use the command (unfamiliar codebase vs. known specific files)

### Task 2: Add /question command to Context Management Commands section
- Locate the "Context Management Commands" section (around line 100) in `tac_bootstrap_cli/docs/commands.md`
- Add a simple table entry for `/question <query>` with description "Answer questions about project structure using read-only exploration"
- Include a brief usage example in the table or as a note: `/question What is the project structure?`
- No detailed subsection needed (command is straightforward, no complex parameters)

### Task 3: Validate documentation consistency
- Review the updated commands.md file to ensure formatting matches existing patterns
- Verify table formatting is correct (pipes aligned, descriptions concise)
- Ensure subsection headers use correct markdown level (### for command details)
- Check that examples use TAC Bootstrap-relevant scenarios
- Confirm no absolute paths used in documentation
- Validate that auto-resolved clarifications are correctly applied:
  - /scout under "Agent Delegation Commands" (not "Agent Orchestration")
  - /question under "Context Management Commands" (not "Research Commands")
  - SCALE parameter documented as numeric 2-10, default 4
  - No model parameter mentioned for /question
  - Tables for simple commands, subsections for complex ones

### Task 4: Run validation commands
- Execute all validation commands to ensure zero regressions
- Fix any issues that arise

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Run linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI

## Notes
- The /scout command is complex with a SCALE parameter and multiple strategies - requires detailed subsection with examples
- The /question command is simple - only needs table entry with brief description
- Auto-resolved clarifications specify exact sections and formatting patterns to follow
- Documentation should focus on user-visible functionality, not internal implementation details
- Use TAC Bootstrap-specific examples to maintain consistency with CLAUDE.md
- Both commands are read-only (no code modification) - this is a key characteristic to note
