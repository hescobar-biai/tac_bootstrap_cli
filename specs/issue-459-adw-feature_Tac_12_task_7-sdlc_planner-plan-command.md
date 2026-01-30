# Feature: Create plan.md command file

## Metadata
issue_number: `459`
adw_id: `feature_Tac_12_task_7`
issue_json: `{"number":459,"title":"[Task 7/49] [FEATURE] Create plan.md command file","body":"## Description\n\nCreate a simple planning command without scout agents. SIMPLER than plan_w_scouters.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2`\n\n## Key Features\n- Model: claude-opus-4-1-20250805\n- allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit\n- Simple 5-step workflow (no scouts)\n- Saves to specs/ directory\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan.md`\n\n## Wave 1 - New Commands (Task 7 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_7"}`

## Feature Description
Create a simple planning command (`/plan`) that generates implementation plans without scout agents or codebase exploration. This command is simpler than `quick-plan.md` and focuses on direct planning workflow. It takes a user prompt, analyzes requirements, designs an approach, writes a plan document, and saves it to the specs/ directory with an auto-generated kebab-case filename.

The feature involves creating three files:
1. A base command file in `.claude/commands/plan.md`
2. A Jinja2 template for CLI generation
3. An update to scaffold_service.py to include the command in the generated command list

## User Story
As a **developer using TAC Bootstrap**
I want to **have a simple /plan command that creates implementation plans**
So that **I can quickly generate structured plans without needing scout agents or codebase exploration**

## Problem Statement
The current TAC Bootstrap system has `quick-plan.md` which creates implementation plans, but the issue specifically requests a simpler planning command called `plan.md` that:
- Does NOT use scout agents (unlike plan_w_scouters)
- Has a straightforward 5-step workflow
- Uses claude-opus-4-1-20250805 model
- Has limited allowed tools: Read, Write, Edit, Glob, Grep, MultiEdit
- Saves plans to specs/ directory with auto-generated filenames

This new command provides a lightweight alternative for planning tasks that don't require extensive codebase exploration.

## Solution Statement
Create a new `/plan` command that:
1. Takes user input via $ARGUMENTS
2. Analyzes requirements and designs an approach (5-step workflow: read prompt → analyze → design → write → save)
3. Auto-generates a descriptive kebab-case filename from the topic
4. Saves the plan to `{{ config.paths.specs_dir }}/filename.md` (creating directory if needed)
5. Reports completion to the user

The command will be:
- Model: claude-opus-4-1-20250805
- Allowed tools: Read, Write, Edit, Glob, Grep, MultiEdit
- Template variable: Only `{{ config.paths.specs_dir }}` for directory path

## Relevant Files

### Existing Files
- `.claude/commands/quick-plan.md` - Reference for structure and workflow (lines 1-48)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Commands list to update (lines 279-324)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config model showing PathsSpec with specs_dir (line 212)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2` - Template reference

### New Files
- `.claude/commands/plan.md` - Base command file in the TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` - Jinja2 template

## Implementation Plan

### Phase 1: Create Base Command File
Create `.claude/commands/plan.md` in the TAC Bootstrap repository. This file serves as the source template that will be templated into plan.md.j2.

### Phase 2: Create Jinja2 Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` that:
- Uses `{{ config.paths.specs_dir }}` for the specs directory path
- Maintains the same workflow structure as quick-plan.md but with the specified tool restrictions
- Uses claude-opus-4-1-20250805 model

### Phase 3: Update Scaffold Service
Add "plan" to the commands list in scaffold_service.py (line 321, alphabetically after "parallel_subagents" and before "patch").

## Step by Step Tasks

### Task 1: Create Base Command File
Create `.claude/commands/plan.md` with:
- Frontmatter specifying model: claude-opus-4-1-20250805
- Frontmatter specifying allowed-tools: Read, Write, Edit, Glob, Grep, MultiEdit
- Purpose section explaining the 5-step workflow
- Variables section with USER_PROMPT: $ARGUMENTS and PLAN_OUTPUT_DIRECTORY: specs/
- Instructions section with the 5-step workflow:
  1. Read and analyze user prompt
  2. Analyze requirements
  3. Design implementation approach
  4. Write comprehensive plan document
  5. Save to specs/<kebab-case-filename>.md
- Report section with completion confirmation format
- No scout agents or codebase exploration steps

### Task 2: Create Jinja2 Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` that:
- Mirrors the structure from Task 1
- Replaces hardcoded "specs/" with `{{ config.paths.specs_dir }}/`
- Keeps all other content static (no other template variables needed)
- Ensures directory creation is handled gracefully

### Task 3: Update Scaffold Service
Modify `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`:
- Add "plan" to the commands list (line 321)
- Position it alphabetically after "parallel_subagents" and before "patch"
- This ensures the command is included when scaffolding new projects

### Task 4: Verify Implementation
Run validation commands to ensure:
- No syntax errors in the command file
- Template renders correctly with config.paths.specs_dir
- Scaffold service includes the command in the list
- All tests pass with zero regressions

## Testing Strategy

### Unit Tests
No new unit tests required as this is a template/configuration change. The existing scaffold_service tests will cover the command list validation.

### Manual Testing
1. Run the TAC Bootstrap CLI to scaffold a new project
2. Verify `.claude/commands/plan.md` is created
3. Test the `/plan` command with a sample prompt
4. Verify plan file is created in specs/ directory with correct filename
5. Confirm the plan content follows the expected structure

### Edge Cases
- specs/ directory doesn't exist → command should create it
- Same plan topic run twice → overwrites silently (no prompt)
- Empty or invalid user prompt → handled by command instructions

## Acceptance Criteria
- [ ] `.claude/commands/plan.md` exists in the TAC Bootstrap repository
- [ ] `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan.md.j2` exists and uses `{{ config.paths.specs_dir }}`
- [ ] "plan" command is added to scaffold_service.py commands list in alphabetical order
- [ ] Command uses claude-opus-4-1-20250805 model
- [ ] Command allows only: Read, Write, Edit, Glob, Grep, MultiEdit tools
- [ ] Command has a simple 5-step workflow (no scout agents)
- [ ] Plans are saved to specs/ directory with auto-generated kebab-case filenames
- [ ] All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The command is intentionally simpler than quick-plan.md - no scout agents or codebase exploration
- The 5-step workflow is: read prompt → analyze requirements → design approach → write plan → save to specs/
- Using claude-opus-4-1-20250805 model as specified (different from quick-plan which uses claude-opus-4-1-20250805)
- The tool restriction (Read, Write, Edit, Glob, Grep, MultiEdit) is more limited than quick-plan (which only has Read, Write, Edit, Glob, Grep)
- This command will be part of Wave 1 - New Commands (Task 7 of 13) per the issue description
- Plans overwrite existing files silently without prompting for rapid iteration
