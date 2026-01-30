# Feature: Plan with Documentation Exploration Command

## Metadata
issue_number: `457`
adw_id: `feature_Tac_12_task_5`
issue_json: `{"number":457,"title":"[Task 5/49] [FEATURE] Create plan_w_docs.md command file","body":"## Description\n\nCreate a planning command that explores documentation before creating plans.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/plan_w_docs.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2`\n\n## Key Features\n- allowed-tools: Task, Read, Glob, Grep, WebFetch\n- Documentation exploration with subagents\n- Enhanced planning with doc context\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_docs.md`\n\n## Wave 1 - New Commands (Task 5 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_5"}`

## Feature Description
Create a new slash command `/plan_w_docs` that enhances the planning process by exploring relevant documentation before generating implementation plans. This command combines the structured planning approach from `feature.md` with an intelligent documentation discovery phase that uses the Task/Explore agent to find and summarize relevant documentation from both local sources (ai_docs/, app_docs/, specs/) and web-based library documentation via WebFetch.

The command provides better-informed planning by:
1. Understanding existing project documentation and patterns
2. Discovering relevant library/framework documentation
3. Identifying documentation gaps that might affect planning
4. Generating plans enriched with contextual information

## User Story
As a developer using TAC Bootstrap
I want to create implementation plans informed by relevant documentation
So that my plans are based on actual project context, architectural patterns, and framework best practices rather than assumptions

## Problem Statement
Current planning commands (feature.md, bug.md, etc.) rely on the agent's general knowledge and ad-hoc codebase exploration. This can lead to:
- Plans that don't align with existing documentation or architectural decisions
- Missing important context from project-specific guidelines in ai_docs/ or app_docs/
- Overlooking relevant framework documentation that could inform better approaches
- Inconsistency between documented patterns and planned implementations

## Solution Statement
Create a `plan_w_docs.md` command that adds a pre-planning documentation exploration phase:
1. Use Task tool with Explore agent (medium thoroughness) to search local documentation directories
2. Optionally fetch relevant web-based library/framework documentation via WebFetch
3. Summarize the top 5-10 most relevant documentation sources
4. Note any documentation gaps or missing context
5. Proceed with standard feature.md planning format, enriched with documentation insights
6. Gracefully handle missing or incomplete documentation by logging warnings in the plan's Notes section

The output follows the same format as feature.md, ensuring compatibility with existing workflows.

## Relevant Files
Files to understand and modify:

- `.claude/commands/feature.md` - Base planning command structure to extend (lines 40-116 show plan format)
- `.claude/commands/quick-plan.md` - Alternative planning pattern for reference
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that registers commands (lines 279-324 show commands list)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` - Directory for command templates
- `.claude/commands/conditional_docs.md` - Reference for documentation routing patterns (if exists)
- `config.yml` - Project configuration with paths (config.paths.ai_docs, etc.)

### New Files
Files to create:

- `.claude/commands/plan_w_docs.md` - New command file in base repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Foundation - Understand Patterns
1. Read existing planning commands (feature.md, quick-plan.md) to understand structure
2. Analyze how config.paths is used in templates
3. Review scaffold_service.py commands list registration pattern
4. Identify documentation directories to search (ai_docs/, app_docs/, specs/)

### Phase 2: Core Implementation - Create Command Files
1. Create `.claude/commands/plan_w_docs.md` with:
   - YAML frontmatter with allowed-tools: Task, Read, Glob, Grep, WebFetch
   - Variables section (issue_number, adw_id, issue_json)
   - Instructions section with documentation exploration workflow
   - Documentation exploration instructions for Task/Explore agent
   - Plan format section (reuse from feature.md)
   - Report section with relative path output rules

2. Create template `plan_w_docs.md.j2` with:
   - Jinja2 template using {{ config }} object
   - Support for {{ config.paths.ai_docs }}, {{ config.paths.specs_dir }}, etc.
   - Same structure as command file but templated paths

### Phase 3: Integration - Register Command
1. Update `scaffold_service.py`:
   - Add "plan_w_docs" to commands list (line ~324)
   - Ensure template is registered for generation
2. Test template rendering with sample config
3. Verify command file is created in generated projects

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create base command file `.claude/commands/plan_w_docs.md`
- Add YAML frontmatter with allowed-tools: Task, Read, Glob, Grep, WebFetch
- Add description: "Enhanced planning with documentation exploration"
- Define variables: issue_number ($1), adw_id ($2), issue_json ($3)
- Create Instructions section with:
  - Documentation exploration workflow (3 steps: search → summarize → identify gaps)
  - Task/Explore agent usage with 'medium' thoroughness
  - Graceful handling of missing docs
  - Relative path requirements (CRITICAL sections from feature.md)
- Add Documentation Exploration section with specific prompts:
  - Search ai_docs/ for architectural patterns and guidelines
  - Search app_docs/ for project-specific documentation
  - Search specs/ for recent implementation patterns
  - Optional: WebFetch for framework/library docs if needed
  - Return summaries of top 5 relevant docs
  - Note any documentation gaps
- Include Plan Format section (copy from feature.md lines 40-116)
- Add Report section with machine-parseable output rules
- Add validation that plan file path is relative only

### Task 2: Create Jinja2 template `plan_w_docs.md.j2`
- Create file in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
- Copy structure from plan_w_docs.md
- Replace hardcoded paths with Jinja2 variables:
  - `ai_docs/` → `{{ config.paths.ai_docs }}/`
  - `specs/` → `{{ config.paths.specs_dir }}/`
  - Add `app_docs` to config paths if not present
- Preserve all CRITICAL and IMPORTANT instructions exactly
- Ensure template renders valid markdown

### Task 3: Update scaffold_service.py to register command
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list (around line 279-324)
- Add "plan_w_docs" to the commands list in alphabetical order
- Verify template file pattern matches: `claude/commands/{cmd}.md.j2`
- Ensure file action is CREATE (only creates if doesn't exist)

### Task 4: Verify template rendering
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_docs.md.j2`
- Check that all {{ config.* }} variables are valid
- Verify no syntax errors in Jinja2 template
- Confirm frontmatter YAML is valid

### Task 5: Run validation commands
- Execute all validation commands to ensure zero regressions
- Verify tests pass
- Check linting passes
- Ensure type checking passes
- Test CLI help output includes new command

## Testing Strategy

### Unit Tests
No new unit tests required - command files are templates, not executable code. Testing covered by:
- Template rendering validation (existing tests)
- Integration test for scaffold_service.build_plan including plan_w_docs
- Manual verification that generated command file is valid markdown

### Edge Cases
Test scenarios:
1. **Missing documentation directories**: Command should proceed with warning in Notes section
2. **Task/Explore agent timeout**: Command should continue with planning, log failure in Notes
3. **WebFetch unavailable**: Command should work with local docs only
4. **Empty documentation directories**: Command should note lack of docs and proceed
5. **Invalid config.paths**: Template should render with default paths
6. **Relative vs absolute path validation**: Command must reject absolute paths in output

### Manual Testing
After implementation:
1. Generate a new project with tac-bootstrap CLI
2. Verify `.claude/commands/plan_w_docs.md` exists
3. Check that file contains valid YAML frontmatter
4. Verify allowed-tools includes: Task, Read, Glob, Grep, WebFetch
5. Test command execution: `/plan_w_docs 999 test_feature '{"number":999,"title":"Test","body":"Test feature"}'`
6. Confirm output is relative path only: `specs/issue-999-adw-test_feature-sdlc_planner-*.md`
7. Verify created plan includes documentation exploration notes

## Acceptance Criteria
1. ✅ File `.claude/commands/plan_w_docs.md` exists in base repository
2. ✅ File has valid YAML frontmatter with allowed-tools: Task, Read, Glob, Grep, WebFetch
3. ✅ Template file `plan_w_docs.md.j2` exists in templates directory
4. ✅ Template uses {{ config.paths.* }} variables for documentation directories
5. ✅ Command registered in scaffold_service.py commands list
6. ✅ Generated command file includes documentation exploration instructions
7. ✅ Documentation exploration uses Task/Explore agent with 'medium' thoroughness
8. ✅ Command searches ai_docs/, app_docs/, specs/ directories
9. ✅ Command supports WebFetch for external documentation
10. ✅ Output follows feature.md plan format
11. ✅ Command gracefully handles missing/incomplete documentation
12. ✅ Documentation gaps logged in plan's Notes section
13. ✅ Output is RELATIVE path only (no absolute paths)
14. ✅ All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Reference file `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/plan_w_docs.md` is inaccessible (permission denied), so implementation based on feature.md and quick-plan.md patterns
- Documentation exploration is enhancement, not requirement - planning proceeds even if docs are missing
- Use Task tool with Explore agent (medium thoroughness) for token efficiency
- Limit documentation summaries to top 5-10 most relevant docs to avoid context overflow
- Command follows KISS principle: uses standard config object, no custom configuration variables beyond config.paths
- Advisory warnings for missing docs, not hard validation that blocks execution
- Subagent receives specific 3-step instructions: search → summarize → identify gaps
- This is Task 5 of 49 in TAC-12 integration, part of Wave 1 (New Commands)
- Command enables documentation-driven planning for better alignment with project context
- Compatible with existing ADW workflows (adw_sdlc_iso.py, adw_plan_iso.py, etc.)
