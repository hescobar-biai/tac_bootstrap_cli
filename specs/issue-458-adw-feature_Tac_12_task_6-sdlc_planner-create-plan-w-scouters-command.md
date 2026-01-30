# Feature: Create plan_w_scouters.md Command File

## Metadata
issue_number: `458`
adw_id: `feature_Tac_12_task_6`
issue_json: `{"number":458,"title":"[Task 6/49] [FEATURE] Create plan_w_scouters.md command file","body":"## Description\n\nCreate a planning command that uses scout subagents for codebase exploration.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_scouters.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`\n\n## Key Features\n- Multiple parallel scout agents\n- Both base and fast scouts\n- Comprehensive codebase analysis\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md`\n\n## Wave 1 - New Commands (Task 6 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_6"}`

## Feature Description
Create a new slash command `/plan_w_scouters` that launches multiple parallel scout agents to comprehensively explore the codebase before creating implementation plans. This command combines the planning capabilities of `/quick-plan` with the parallel exploration power of `/scout`, launching both fast and thorough scout agents to gather maximum context before generating detailed implementation specifications.

The command will be available in both the base TAC Bootstrap repository and as a Jinja2 template for CLI-generated projects.

## User Story
As a developer using TAC Bootstrap
I want to create implementation plans with comprehensive codebase exploration
So that my plans are based on complete understanding of existing code, patterns, and dependencies

## Problem Statement
Current planning commands (`/feature`, `/quick-plan`) rely on manual exploration or limited search strategies before generating implementation plans. This can lead to:
- Incomplete understanding of existing patterns
- Missed dependencies and related files
- Plans that don't account for all affected areas
- Need for plan revisions after discovering additional context

The existing `/scout` command provides excellent parallel exploration but is separate from plan generation, requiring two-step manual workflow.

## Solution Statement
Create a unified `/plan_w_scouters` command that:
1. Launches 2-3 fast scouts for rapid surface exploration
2. Launches 2-3 thorough scouts for deep architectural analysis
3. Aggregates scout findings into a comprehensive file list
4. Generates an implementation plan based on complete codebase understanding

The command will be implemented as:
- Base command file: `.claude/commands/plan_w_scouters.md`
- Jinja2 template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`
- Integration into `scaffold_service.py` command list

## Relevant Files
Files needed for implementing this feature:

- `.claude/commands/plan_w_scouters.md` (NEW) - Base command file for TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` (NEW) - Template for CLI generation
- `tac_bootstrap_cli/tac_bootstrap/application/services/scaffold_service.py` - Add command to rendering list
- `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` - Reference implementation (if accessible)
- `.claude/commands/quick-plan.md` - Reference for planning workflow structure
- `.claude/commands/scout.md` - Reference for scout agent patterns

### New Files
- `.claude/commands/plan_w_scouters.md` - Base command implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2` - Template with Jinja2 variables

## Implementation Plan

### Phase 1: Foundation
Read reference files and understand command patterns:
- Attempt to read reference file from TAC-12 if accessible
- Read existing `/quick-plan` command for plan generation patterns
- Read existing `/scout` command for parallel exploration patterns
- Understand command structure: Variables, Instructions, Workflow, Report sections

### Phase 2: Core Implementation
Create base command file and template:
- Create `.claude/commands/plan_w_scouters.md` with command implementation
- Convert to Jinja2 template with minimal templating (project.name, project.description)
- Implement scout launching strategy (2-3 fast + 2-3 thorough agents)
- Implement plan generation workflow based on scout results

### Phase 3: Integration
Integrate into CLI scaffolding:
- Add "plan_w_scouters" to commands list in `scaffold_service.py`
- Verify template rendering with sample config
- Test file generation in both base repo and CLI output

## Step by Step Tasks

### 1. Gather Context and Read Reference Files
- Attempt to read `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` if accessible
- Read `.claude/commands/quick-plan.md` to understand planning workflow
- Read `.claude/commands/scout.md` to understand scout patterns
- Identify key sections: Variables, Instructions, Workflow, Report

### 2. Design Command Structure
- Define Variables section:
  - `USER_PROMPT: $1` - Required task description
  - `TOTAL_BASE_SCOUT_SUBAGENTS: 3` - Thorough scouts
  - `TOTAL_FAST_SCOUT_SUBAGENTS: 5` - Fast scouts
  - `PLAN_OUTPUT_DIRECTORY: specs/` - Output location
- Define Instructions section with usage guidance
- Design Workflow section:
  - Step 1: Validate USER_PROMPT
  - Step 2: Launch fast scouts in parallel (3-5 agents with thoroughness='quick')
  - Step 3: Launch thorough scouts in parallel (2-3 agents with thoroughness='very thorough')
  - Step 4: Aggregate scout results
  - Step 5: Generate implementation plan based on findings
  - Step 6: Save plan to `specs/` directory
- Define Report section with output format

### 3. Create Base Command File
- Create `.claude/commands/plan_w_scouters.md`
- Add frontmatter with description and metadata
- Implement Variables section
- Implement Instructions section:
  - When to use this command
  - Scout strategy explanation (fast vs thorough)
  - Expected outcomes
- Implement Workflow section:
  - Scout launching logic (parallel Task tool calls)
  - Result aggregation approach
  - Plan generation based on Plan Format
- Implement Report section
- Include Plan Format template matching `/quick-plan` structure

### 4. Convert to Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`
- Add Jinja2 variables:
  - `{{ config.project.name }}` for project-specific references
  - `{{ config.project.description }}` if needed for context
- Keep most content static (scout behavior is universal)
- Ensure template renders valid markdown

### 5. Integrate into Scaffold Service
- Open `tac_bootstrap_cli/tac_bootstrap/application/services/scaffold_service.py`
- Locate the commands list in `_add_claude_files` method (around line 279-324)
- Add `"plan_w_scouters"` to the commands list in alphabetical/logical order
- Verify the command follows same pattern as others:
  ```python
  plan.add_file(
      f".claude/commands/plan_w_scouters.md",
      action=action,
      template=f"claude/commands/plan_w_scouters.md.j2",
      reason="/plan_w_scouters slash command",
  )
  ```

### 6. Test Template Rendering
- Use Python to render template with sample config:
  ```python
  from tac_bootstrap.infrastructure.template_repo import TemplateRepository
  from tac_bootstrap.domain.models import TACConfig

  # Create sample config
  config = TACConfig(...)

  # Render template
  repo = TemplateRepository()
  rendered = repo.render("claude/commands/plan_w_scouters.md.j2", config)

  # Verify output is valid markdown
  print(rendered[:500])
  ```

### 7. Verify File Generation
- Run CLI command to generate scaffold with new command
- Verify `.claude/commands/plan_w_scouters.md` is created
- Read generated file and verify content correctness
- Check file has valid markdown syntax

### 8. Manual Smoke Test
- In a test environment, try running `/plan_w_scouters "test task"`
- Verify it launches scout agents (don't wait for completion)
- Verify command syntax is correct (no errors)

### 9. Run Validation Commands
- Execute all validation commands to ensure no regressions
- Fix any issues discovered

## Testing Strategy

### Unit Tests
Not required for this task - command files are declarative markdown, not executable code. Testing focuses on:
1. Template rendering produces valid markdown
2. File is created in correct location during scaffolding
3. Content matches expected structure

### Manual Testing
1. Generate a new project using CLI and verify command file exists
2. Load command in Claude Code session (syntax check)
3. Optionally: Run command with test prompt to verify agent launching works

### Edge Cases
- Missing USER_PROMPT parameter - command should abort with error
- Template rendering with minimal config (only required fields)
- Template rendering with full config (all optional fields)

## Acceptance Criteria
1. Base command file `.claude/commands/plan_w_scouters.md` created with complete implementation
2. Jinja2 template `plan_w_scouters.md.j2` created with minimal templating
3. Template uses only `config.project.name` and `config.project.description` variables
4. Command integrated into `scaffold_service.py` commands list
5. Template renders correctly with sample TACConfig
6. Rendered file has valid markdown syntax
7. File is generated in `.claude/commands/` during scaffolding
8. Command structure follows existing patterns from `/quick-plan` and `/scout`
9. Command includes:
   - Variables section (USER_PROMPT, scout counts, output directory)
   - Instructions section (when to use, scout strategy explanation)
   - Workflow section (scout launching, aggregation, plan generation)
   - Report section (output format)
   - Plan Format template
10. All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI

## Notes

### Scout Strategy Design
The command uses a two-phase scout approach:
1. **Fast scouts (3-5 agents)**: Use `thoroughness='quick'` for rapid surface exploration
   - File pattern matching
   - Basic content search
   - Quick architectural overview

2. **Thorough scouts (2-3 agents)**: Use `thoroughness='very thorough'` for deep analysis
   - Dependency mapping
   - Architectural deep dive
   - Integration points analysis

This staged approach provides progressive understanding: fast scouts give quick context, thorough scouts dive deep into specific areas.

### Templating Philosophy
Keep templates generic and minimize Jinja2 variables. Only inject:
- `config.project.name` for project-specific references
- `config.project.description` for context if needed

Scout exploration patterns are universal and work across all project types. Scouts are intelligent enough to adapt to any codebase structure without hardcoded paths.

### Reference File
The reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_scouters.md` is the authoritative source if accessible. If not accessible, derive command structure from existing `/quick-plan` and `/scout` commands, following established patterns.

### Error Handling
No special error handling needed in the command file itself. Command files are instructions for Claude, not executable code. If scouts fail during execution, Claude will handle it in the normal conversation flow. Document expected behavior in comments.

### Future Enhancements
- Consider caching scout results to avoid re-exploring same areas
- Add support for custom scout focus areas via additional parameters
- Integrate with `/implement` to auto-feed discovered files
