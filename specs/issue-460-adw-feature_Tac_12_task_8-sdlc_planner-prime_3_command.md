# Feature: prime_3.md - Deep Context Loading Command

## Metadata
issue_number: `460`
adw_id: `feature_Tac_12_task_8`
issue_json: `{"number":460,"title":"[Task 8/49] [FEATURE] Create prime_3.md command file","body":"## Description\n\nCreate a deep priming command with 3 levels of exploration.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_3.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`\n\n## Key Features\n- 3-level deep context loading\n- Comprehensive codebase understanding\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md`\n\n## Wave 1 - New Commands (Task 8 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_8"}`

## Feature Description
Create a comprehensive 3-level deep context loading command (`prime_3.md`) that performs sequential exploration passes to build thorough understanding of a codebase. This command extends the existing `/prime` and `/prime_cc` commands by adding a third tier with three distinct exploration levels:

1. **Level 1**: High-level architecture and directory structure
2. **Level 2**: Key modules, components, and their interactions
3. **Level 3**: Detailed implementation patterns, code conventions, and technical specifics

This command provides the deepest possible context loading for complex tasks requiring comprehensive codebase understanding.

## User Story
As a developer using TAC Bootstrap CLI,
I want a `/prime_3` command that performs deep 3-level codebase exploration,
So that I can prepare agents with comprehensive context before tackling complex implementation tasks or major architectural changes.

## Problem Statement
Current context loading commands (`/prime` and `/prime_cc`) provide basic and Claude Code-specific context respectively, but lack a comprehensive deep-dive option for:
- Major architectural refactoring tasks
- Complex feature implementation requiring deep understanding
- Onboarding to large or complex codebases
- Tasks spanning multiple architectural layers or modules

Without a structured 3-level exploration command, developers must manually navigate and read numerous files, increasing cognitive load and risk of missing critical context.

## Solution Statement
Create a `prime_3.md` slash command and corresponding Jinja2 template that:
- Executes `/prime` and `/prime_cc` as foundation (levels 0)
- Performs Level 1 exploration: architecture, directory structure, key entry points
- Performs Level 2 exploration: module interactions, dependency patterns, data flow
- Performs Level 3 exploration: implementation details, code conventions, testing patterns
- Provides a comprehensive summary with architectural insights and key patterns discovered
- Uses minimal Jinja2 templating for project-specific variables (project name, paths)
- Follows the established command file format (frontmatter + instructions)

## Relevant Files
Files needed for implementation:

### Existing Reference Files
- `.claude/commands/prime.md` - Level 0 basic context loading (reference for structure)
- `.claude/commands/prime_cc.md` - Level 0 Claude Code context (reference for extended commands)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Template pattern reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Extended template pattern reference
- `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md` - Original reference (may not be accessible)

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:279-324` - Commands list to add 'prime_3'

### New Files
- `.claude/commands/prime_3.md` - Base command file for TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Analysis and Reference Review
Review existing command patterns and determine prime_3 structure:
1. Read reference file if accessible (best effort)
2. Analyze prime.md and prime_cc.md for structural patterns
3. Determine 3-level exploration strategy
4. Design command workflow structure

### Phase 2: Create Base Command File
Create `.claude/commands/prime_3.md` in base repository:
1. Add frontmatter with description and metadata
2. Define 3-level exploration workflow
3. Structure Read, Run, and Understand sections
4. Add comprehensive Report section

### Phase 3: Create Jinja2 Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`:
1. Convert base command to template
2. Add Jinja2 variables for project name, paths
3. Keep exploration logic static (methodology is universal)
4. Test template renders correctly with config variables

### Phase 4: Register Command
Update scaffold_service.py to include prime_3 in commands list:
1. Add 'prime_3' to commands array
2. Ensure correct alphabetical or logical ordering
3. Verify template path mapping works

## Step by Step Tasks
IMPORTANTE: Execute each step in order.

### Task 1: Review Reference Files and Determine Structure
- Read `.claude/commands/prime.md` and analyze structure
- Read `.claude/commands/prime_cc.md` to understand extended command pattern
- Read templates `prime.md.j2` and `prime_cc.md.j2` to understand Jinja2 usage
- Attempt to read reference file `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md` (best effort)
- Design 3-level exploration strategy based on patterns observed

### Task 2: Create Base Command File
- Create `.claude/commands/prime_3.md` with frontmatter (description metadata)
- Define Variables section (minimal or none)
- Define Instructions section explaining 3-level approach
- Create Run section with 3 sequential exploration phases:
  - **Phase 1**: Execute /prime and /prime_cc for foundation
  - **Level 1**: High-level architecture exploration (git ls-files, README, architecture docs, entry points)
  - **Level 2**: Module interaction exploration (key services, components, data models, API contracts)
  - **Level 3**: Implementation details exploration (code patterns, testing strategies, configuration, conventions)
- Create Understand section documenting what was discovered at each level
- Create Report section with comprehensive summary format

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`
- Copy content from `.claude/commands/prime_3.md`
- Replace hardcoded project references with `{{ config.project.name }}`
- Replace paths with `{{ config.paths.* }}` where applicable
- Keep exploration methodology static (no conditional logic needed)
- Verify all Jinja2 variables match those used in other command templates

### Task 4: Register Command in Scaffold Service
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate the commands list (around line 279-324)
- Add `"prime_3"` to the list following existing pattern
- Maintain logical ordering (likely near other prime commands)
- Verify the file-to-template mapping follows convention (`.claude/commands/prime_3.md` → `claude/commands/prime_3.md.j2`)

### Task 5: Validation and Testing
- Run validation commands to ensure zero regressions
- Verify template renders correctly
- Check that command file has proper markdown structure
- Ensure scaffold_service.py has no syntax errors

## Testing Strategy

### Unit Tests
- No dedicated unit tests required for command files (they are markdown content)
- Template rendering is tested indirectly through scaffold_service integration tests
- If `test_scaffold_service.py` exists, verify it still passes

### Manual Testing
- Generate a test project using tac-bootstrap CLI with prime_3 command included
- Verify `.claude/commands/prime_3.md` is created
- Verify command content matches expected structure
- Test that command executes in Claude Code environment (if possible)

### Edge Cases
- Missing reference file should not block implementation
- Template should render with minimal config (only required variables)
- Command should work with different project architectures (DDD, Clean, Hexagonal)
- Large codebases should still execute without token overflow (recommend file sampling strategy)

## Acceptance Criteria
1. **Base Command File Created**: `.claude/commands/prime_3.md` exists with proper frontmatter and 3-level exploration workflow
2. **Template Created**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2` exists and uses minimal Jinja2 templating
3. **Registered in Scaffold Service**: `scaffold_service.py` includes 'prime_3' in commands list
4. **3-Level Structure Clear**: Command clearly defines and executes 3 distinct exploration levels
5. **Comprehensive Report**: Report section provides structured summary of all 3 levels
6. **Consistent with Patterns**: Follows same structure as prime.md and prime_cc.md
7. **Template Variables Correct**: Uses same Jinja2 variables as other command templates (config.project.name, config.paths.*)
8. **All Validation Passes**: Validation commands run successfully with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Decisions
- **3-Level Approach**: Mirrors natural code understanding progression (structure → components → details)
- **Minimal Templating**: Exploration methodology is universal, only project-specific values need Jinja2
- **Sequential Execution**: Each level builds on previous, ensuring comprehensive context
- **Token Management**: Level 3 should recommend file sampling or focus areas to avoid token overflow

### Future Considerations
- May want to add optional parameters for focusing Level 3 on specific modules
- Could add time estimates or token usage warnings for large codebases
- Might benefit from integration with `/scout` command for targeted deep dives

### Dependencies
- No blocking dependencies on other Wave 1 tasks
- Independent implementation that can be executed in any order
- Should maintain consistency with existing prime commands if they are updated

### Reference Notes
- Original reference at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_3.md` provides canonical example
- If reference is accessible, use it as primary guide
- If reference is not accessible, follow patterns from prime.md and prime_cc.md and apply 3-level exploration logic
