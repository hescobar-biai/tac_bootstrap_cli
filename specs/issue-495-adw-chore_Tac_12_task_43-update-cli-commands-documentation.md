# Chore: Update CLI Commands Documentation

## Metadata
issue_number: `495`
adw_id: `chore_Tac_12_task_43`
issue_json: `{"number": 495, "title": "[Task 43/49] [CHORE] Update CLI commands documentation", "body": "Update CLI commands documentation with all new TAC-12 commands.\n\nFiles:\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/docs/commands.md`\n\nChanges Required:\n- Add documentation for 13 new commands\n- Include usage examples\n- Document allowed-tools and models"}`

## Chore Description

Update the CLI commands documentation (`tac_bootstrap_cli/docs/commands.md`) to include documentation for 13 new TAC-12 commands. These commands represent enhancements to the planning, implementation, agent delegation, and context management workflows.

The 13 new commands to document are:
1. `/plan` - Basic planning without exploration (legacy variant)
2. `/plan_w_docs` - Planning with documentation exploration
3. `/plan_w_scouters` - Planning with parallel scout-based exploration
4. `/build_in_parallel` - Parallel file creation delegation to build-agents
5. `/scout_plan_build` - End-to-end scout-plan-build orchestration
6. `/find_and_summarize` - Lightweight file discovery with AI summarization
7. `/all_tools` - List all available tools
8. `/prime_3` - Deep context loading (prime variant)
9. `/quick-plan` - Rapid planning with architect pattern
10. `/resolve_failed_test` - Analyze and fix failing tests
11. `/resolve_failed_e2e_test` - Analyze and fix failing E2E tests
12. `/track_agentic_kpis` - Track agentic development KPIs
13. `/build_w_report` - Implement with detailed YAML change report

### Integration Strategy

Based on clarifications, new commands should be:
- **Integrated into existing sections** by functional category (not new sections)
- **Organized by feature relationship and complexity** within sections (simpler before complex)
- **Documented with 1-2 concise examples** extracted from command files
- **Tools listed inline** in tables as a simple 4th column (e.g., `Tools: Read, Write`)
- **Documented as stable and production-ready** (no development status caveats)

### Section Mapping

- **Planning Commands**: `/plan`, `/plan_w_docs`, `/plan_w_scouters`, `/quick-plan`
- **Implementation Commands**: `/build_in_parallel`, `/build_w_report` (alongside existing `/implement`, `/commit`, `/pull_request`)
- **Agent Delegation Commands**: `/scout_plan_build` (alongside existing `/scout`, `/background`, `/parallel_subagents`)
- **Context Management Commands**: `/all_tools` (alongside existing `/prime_cc`, `/load_bundle`, `/tools`, `/question`)
- **Test Commands**: `/resolve_failed_test`, `/resolve_failed_e2e_test`, `/track_agentic_kpis` (with `/test` commands)
- **Documentation Commands**: `/find_and_summarize`, `/prime_3` (alongside existing commands)

## Relevant Files

### Main File to Update
- `tac_bootstrap_cli/docs/commands.md` - Primary documentation file containing all slash command references

### Command Definition Files (for extracting examples and metadata)
- `.claude/commands/plan.md` - Basic planning command
- `.claude/commands/plan_w_docs.md` - Planning with documentation exploration
- `.claude/commands/plan_w_scouters.md` - Planning with scout exploration
- `.claude/commands/quick-plan.md` - Rapid planning with architect pattern
- `.claude/commands/build_in_parallel.md` - Parallel build-agent delegation
- `.claude/commands/build_w_report.md` - Implementation with YAML report
- `.claude/commands/scout_plan_build.md` - End-to-end scout-plan-build
- `.claude/commands/find_and_summarize.md` - File discovery with summarization
- `.claude/commands/all_tools.md` - Tool listing reference
- `.claude/commands/prime_3.md` - Deep context loading
- `.claude/commands/resolve_failed_test.md` - Test failure analysis
- `.claude/commands/resolve_failed_e2e_test.md` - E2E test failure analysis
- `.claude/commands/track_agentic_kpis.md` - KPI tracking command

### Reference Files
- `CLAUDE.md` - Project guidelines for agents
- `PLAN_TAC_BOOTSTRAP.md` - Master implementation plan
- `.claude/commands/` - All command definitions for pattern reference

## Step by Step Tasks

### Task 1: Analyze Current Documentation Structure
- Read the current `commands.md` file completely
- Identify existing section organization (Core Development, Planning, Implementation, Review & Quality, Documentation, Context Management, Agent Delegation, Meta & Generation, Expert, Workflow, Test Commands)
- Understand current table format and inline documentation style
- Identify where new commands fit best by category

### Task 2: Extract Examples and Metadata from New Commands
- Read each of the 13 command files
- Extract allowed-tools metadata from YAML frontmatter
- Extract 1-2 concise, realistic usage examples for each command
- Capture key descriptions and arguments from each command
- Document model selection if non-default (most use sonnet/haiku)

### Task 3: Update Planning Commands Section
- Integrate `/plan`, `/plan_w_docs`, `/plan_w_scouters`, `/quick-plan` into existing "Planning Commands" section
- Order by complexity: `/plan` (basic) before `/plan_w_docs` before `/plan_w_scouters`
- Add `/quick-plan` after `/patch` with examples
- Include Tools column showing allowed-tools for each
- Keep consistent table format with existing commands

### Task 4: Update Implementation Commands Section
- Add `/build_in_parallel` and `/build_w_report` to existing "Implementation Commands" section
- Place after existing `/implement` to show progression
- Add examples showing parallel delegation and report generation
- Document allowed-tools and model for each
- Maintain consistent table format

### Task 5: Update Agent Delegation Commands Section
- Add `/scout_plan_build` to existing "Agent Delegation Commands" section
- Place as capstone orchestration command (after `/scout`, `/background`, `/parallel_subagents`)
- Add examples showing complete workflow
- Document the 3-phase orchestration (Scout-Plan-Build)
- Include Tools and model information

### Task 6: Update Context Management Commands Section
- Add `/all_tools` and `/prime_3` to existing "Context Management Commands" section
- `/all_tools` alongside `/tools` as reference command
- `/prime_3` alongside other `/prime*` variants
- Add concise examples for each
- Document tools if unusual

### Task 7: Update Test Commands Section
- Add `/resolve_failed_test`, `/resolve_failed_e2e_test`, `/track_agentic_kpis` to Test Commands
- These provide advanced test analysis and tracking
- Add concise examples for each
- Document allowed-tools for analysis commands

### Task 8: Update Documentation Commands Section
- Add `/find_and_summarize` to Documentation Commands section
- Place as lightweight alternative to `/scout` for targeted file discovery
- Add example showing glob pattern usage
- Document tools and use cases

### Task 9: Validate Documentation Consistency
- Ensure all 13 commands are documented with consistent formatting
- Verify all examples are concise and realistic (1-2 lines)
- Check that Tools column is included for all new commands
- Verify inline text notes for arguments and special requirements
- Confirm no raw frontmatter is exposed in documentation

### Task 10: Final Review and Testing
- Read entire updated documentation file to ensure coherence
- Verify table formatting is consistent throughout
- Check for any missing commands or incomplete sections
- Validate links and references work properly
- Run markdown lint check if available
- Execute validation command to ensure no regressions

## Validation Commands

Execute these commands to validate with zero regressions:

- `cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/chore_Tac_12_task_43 && cat tac_bootstrap_cli/docs/commands.md | wc -l` - Verify file exists and has content
- `cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/chore_Tac_12_task_43 && grep -c "^| \`/" tac_bootstrap_cli/docs/commands.md` - Count command table entries
- Verify all 13 new commands appear in documentation
- Verify markdown formatting is valid (no broken tables)
- Verify examples are concise and accurate

## Notes

### Documentation Style Guidelines
- Examples should be 1-2 lines max, showing typical usage
- Tools should be listed inline in tables as simple text (not code blocks)
- Keep descriptions focused on what the command does, not exhaustive details
- Reference detailed command files for comprehensive instructions
- Maintain existing visual hierarchy and formatting

### Command Categorization Rationale
- **Plan variants** (`/plan`, `/plan_w_docs`, `/plan_w_scouters`) grouped together showing evolution
- **Build commands** (`/implement`, `/build_w_report`, `/build_in_parallel`) show different build strategies
- **Scout orchestration** (`/scout_plan_build`) represents capstone delegation pattern
- **Context tools** (`/all_tools`, `/prime_3`) provide access to system capabilities and deep context
- **Test utilities** organized by analysis depth and scope

### Implementation Notes
- Maintain backward compatibility with existing documentation sections
- Do not remove or modify existing command documentation
- Keep consistent markdown formatting and table styles
- No new section types needed; integrate by functionality
- Tools column format: `Tools: Read, Write, Bash` (inline text, comma-separated)

### Wave 8 Context
This is Task 43 of 49 in Wave 8 (Documentation). This chore completes documentation of all TAC-12 planning, implementation, and delegation commands introduced in earlier waves.
