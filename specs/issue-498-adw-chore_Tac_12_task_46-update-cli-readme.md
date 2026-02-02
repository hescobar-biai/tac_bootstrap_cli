# Chore: Update tac_bootstrap_cli README.md

## Metadata
issue_number: `498`
adw_id: `chore_Tac_12_task_46`
issue_json: `{"number": 498, "title": "[Task 46/49] [CHORE] Update tac_bootstrap_cli README.md", "body": "Update CLI README with TAC-12 features overview"}`

## Chore Description

Update the tac_bootstrap_cli README.md to document TAC-12 features and improvements. This involves:

1. Adding a new 'TAC-12 Multi-Agent Orchestration' section after 'ADW Workflows'
2. Expanding the existing 'Hooks' section to categorize TAC-12-specific hooks
3. Adding a new 'Observability' section covering hooks, status line integration, and logging
4. Updating command reference tables to highlight TAC-12 specific commands
5. Maintaining backward compatibility with existing documentation structure

The README should serve as a quick-reference guide with cross-references to detailed documentation files (hooks.md, utilities.md, commands.md) rather than duplicating content.

## Relevant Files

### Primary Files to Update
- `tac_bootstrap_cli/README.md` - Main CLI documentation file that needs updates

### Reference Files for Context
- `docs/hooks.md` - Detailed hooks documentation (9 TAC-12 hooks)
- `docs/utilities.md` - Observability utilities documentation
- `docs/commands.md` - Comprehensive command reference
- `adws/README.md` - ADW workflows documentation
- `CLAUDE.md` - Project guidelines

### New Files
No new files required; only README.md updates.

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review existing README structure and TAC-12 features
- Read current `tac_bootstrap_cli/README.md` to understand existing sections
- Identify where to insert new sections (after 'ADW Workflows')
- Note existing 'Hooks' section content for expansion
- Document current command reference table structure

### Task 2: Identify TAC-12 hooks to highlight
- Identify the 5 new TAC-12 hooks: `send_event`, `session_start`, `pre_compact`, `subagent_stop`, `user_prompt_submit`
- Categorize all 9 hooks into: Core hooks, Security hooks, TAC-12 Additional hooks
- Prepare summary descriptions for each TAC-12 hook
- Plan how to expand existing hooks table without duplicating detailed content

### Task 3: Document TAC-12 Multi-Agent Orchestration section
- Create new section with subsections for TAC-12-specific commands
- Include command syntax for `parallel_subagents` with and without arguments
- Add `scout_plan_build` and `implement` (with TAC-12 improvements) to command table
- Include practical examples focusing on: command syntax, workflow phases, trigger types
- Reference detailed docs for deep dives

### Task 4: Create Observability section
- Add new 'Observability' section after 'Hooks' section
- Summarize hooks system with category breakdown (Core, Security, TAC-12)
- Document status line integration overview
- Document logging infrastructure overview
- Add cross-references to hooks.md, utilities.md, and commands.md for detailed coverage

### Task 5: Update command reference tables
- Separate TAC-12-specific commands from 'Key Slash Commands' table to avoid breaking changes
- Create 'TAC-12 Specific Commands' subsection under 'TAC-12 Multi-Agent Orchestration'
- Include: parallel_subagents, scout_plan_build, implement (with TAC-12 improvements)
- Keep existing 'Key Slash Commands' table intact for backward compatibility

### Task 6: Validate and test updates
- Run validation commands to ensure no regressions
- Verify all cross-references point to existing documentation
- Check markdown formatting and consistency
- Confirm new sections appear in correct locations

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- Verify README.md renders correctly and all links/references are valid

## Notes

- All TAC-12 features documented are stable (released in current version)
- Focus on what's new/different from TAC-11 rather than duplicating existing content
- README should remain accessible without overwhelming users with detailed implementation
- Maintain section flow: commands → workflows → orchestration patterns → observability
- Cross-references keep README concise while pointing users to comprehensive docs for details
