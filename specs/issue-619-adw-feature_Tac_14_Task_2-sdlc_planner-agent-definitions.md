# Feature: Agent Definitions Implementation (BASE + TEMPLATES)

## Metadata
issue_number: `619`
adw_id: `feature_Tac_14_Task_2`
issue_json: `{"number": 619, "title": "Implementar Agent Definitions completas (BASE + TEMPLATES)", "body": "..."}`

## Feature Description
Implement the complete agent definitions system for TAC Bootstrap following the TAC-14 "dual location" pattern. This involves copying 7 specialized agent definition files from the tac-14 reference repository into BASE (.claude/agents/) and creating corresponding Jinja2 templates for project generation. The implementation ensures that tac_bootstrap itself has functional agent definitions while also generating these definitions for new projects created by the CLI.

The 7 agent types are:
1. **build-agent**: Parallel file implementation specialist
2. **scout-report-suggest**: Codebase exploration and analysis
3. **scout-report-suggest-fast**: Fast codebase scouting (haiku model)
4. **planner**: Implementation planning specialist
5. **playwright-validator**: E2E validation specialist
6. **meta-agent**: Agent definition generator
7. **docs-scraper**: Documentation scraping specialist

## User Story
As a TAC Bootstrap developer
I want complete agent definitions in both BASE and templates
So that tac_bootstrap itself can use agents AND generated projects get these agents automatically

## Problem Statement
TAC-14 introduces a multi-agent system with 7 specialized agent types. Currently, tac_bootstrap lacks these agent definitions in both:
1. BASE implementation (.claude/agents/) - needed for tac_bootstrap's own development
2. Template system (templates/.claude/agents/*.j2) - needed for generating projects

Without these definitions, neither tac_bootstrap nor generated projects can leverage the full TAC-14 agent orchestration capabilities.

## Solution Statement
Copy the 7 agent definition files from the validated tac-14 reference implementation at `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/` into two locations:

1. **BASE** (.claude/agents/): Functional copies with paths adapted for tac_bootstrap context
2. **TEMPLATES** (tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/): Jinja2 templates with minimal variable injection for project-specific paths

This follows the established pattern in scaffold_service.py where agent definitions are already partially registered (lines 459-475) but the actual template files don't exist yet.

## Relevant Files

### Source Files (Reference Implementation)
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/build-agent.md` - Build agent definition
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/scout-report-suggest.md` - Scout agent (full)
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/scout-report-suggest-fast.md` - Scout agent (fast)
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/planner.md` - Planning agent
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/playwright-validator.md` - E2E testing agent
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/meta-agent.md` - Meta agent
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/docs-scraper.md` - Documentation agent

### Target Files - BASE
- `.claude/agents/build-agent.md` [CREATE]
- `.claude/agents/scout-report-suggest.md` [CREATE]
- `.claude/agents/scout-report-suggest-fast.md` [CREATE]
- `.claude/agents/planner.md` [CREATE]
- `.claude/agents/playwright-validator.md` [CREATE]
- `.claude/agents/meta-agent.md` [CREATE]
- `.claude/agents/docs-scraper.md` [CREATE]

### Target Files - TEMPLATES
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/build-agent.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/scout-report-suggest.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/scout-report-suggest-fast.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/planner.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/playwright-validator.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/meta-agent.md.j2` [CREATE]
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/docs-scraper.md.j2` [CREATE]

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Agent registration already exists (lines 459-475), verify template paths match

### New Files
All 14 files listed in Target Files sections above (7 BASE + 7 TEMPLATES)

## Implementation Plan

### Phase 1: Validation and Preparation
- Verify source files exist and are accessible
- Verify .claude/agents/ directory exists in BASE (should already exist per scaffold_service.py:118)
- Verify tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/ directory exists
- Create a Python script to validate YAML frontmatter syntax

### Phase 2: BASE Implementation
- Copy all 7 agent definition files from source to .claude/agents/
- Validate YAML frontmatter in each file (name, description, tools, model, color)
- Adapt any absolute paths to relative paths for tac_bootstrap context
- Preserve all agent logic, tools, and behavior exactly

### Phase 3: Template Generation
- Create .j2 templates for each agent definition
- Preserve YAML frontmatter structure
- Inject minimal Jinja2 variables only where project-specific context needed
- Follow existing template patterns from scaffold_service.py

### Phase 4: Registration Verification
- Verify scaffold_service.py agent registration (lines 459-475) matches template filenames
- Confirm template rendering will occur during project generation
- Validate the "agents" tuple in scaffold_service.py includes all 7 agents

## Step by Step Tasks

### Task 1: Pre-flight Validation
- Run bash command to verify source files exist: `ls -la /Volumes/MAc1/Celes/TAC/tac-14/.claude/agents/`
- Verify all 7 expected files are present
- If any file is missing, FAIL EARLY with clear error message
- Verify .claude/agents/ directory exists in BASE: `ls -la .claude/agents/`
- Verify templates directory structure: `ls -la tac_bootstrap_cli/tac_bootstrap/templates/.claude/`

### Task 2: Create YAML Validation Script
- Create a temporary Python script in scratchpad to validate YAML frontmatter
- Script should parse YAML between --- delimiters
- Validate required fields: name, description, tools (list), model, color
- Script should return exit code 0 if valid, 1 if invalid with error message

### Task 3: Copy Agent Definitions to BASE
- Copy build-agent.md from source to .claude/agents/build-agent.md
- Copy scout-report-suggest.md from source to .claude/agents/scout-report-suggest.md
- Copy scout-report-suggest-fast.md from source to .claude/agents/scout-report-suggest-fast.md
- Copy planner.md from source to .claude/agents/planner.md
- Copy playwright-validator.md from source to .claude/agents/playwright-validator.md
- Copy meta-agent.md from source to .claude/agents/meta-agent.md
- Copy docs-scraper.md from source to .claude/agents/docs-scraper.md
- Run YAML validation script on each copied file
- If any validation fails, fix the YAML in place

### Task 4: Adapt Paths in BASE Files
- Read each agent definition file
- Identify any absolute paths or tac-14-specific references
- Replace with relative paths or tac_bootstrap-appropriate paths
- Preserve all agent logic, tools, model selection, and behavior
- Write back modified files

### Task 5: Create Template Directory
- Ensure tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/ exists
- Run: `mkdir -p tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/`

### Task 6: Generate Jinja2 Templates
- For each of the 7 agent definitions in BASE:
  - Read the BASE file
  - Create corresponding .j2 template in templates/.claude/agents/
  - Preserve YAML frontmatter exactly
  - Keep agent content mostly static
  - Only inject Jinja2 variables where project-specific context needed (paths, project names)
  - Follow pattern from existing scaffold_service.py templates (e.g., claude/commands/*.md.j2)
- Files to create:
  - build-agent.md.j2
  - scout-report-suggest.md.j2
  - scout-report-suggest-fast.md.j2
  - planner.md.j2
  - playwright-validator.md.j2
  - meta-agent.md.j2
  - docs-scraper.md.j2

### Task 7: Verify Scaffold Service Registration
- Read scaffold_service.py lines 459-475 (agent registration section)
- Verify each of the 7 agents is listed in the agents tuple
- Verify template path format matches: f".claude/agents/{agent}.j2"
- Verify FileAction is correct (should be FileAction.CREATE)
- If any discrepancies, note them for manual review

### Task 8: Integration Testing
- Run a quick test of template rendering (if test infrastructure exists)
- Verify templates can be loaded by TemplateRepository
- Check that no Jinja2 syntax errors exist

### Task 9: Final Validation
- Run YAML validation script on all 7 BASE files
- Run YAML validation script on all 7 template files (after rendering with test config)
- Verify tools list in each agent is valid
- Confirm all files are readable and properly formatted
- Execute all Validation Commands

## Testing Strategy

### Unit Tests
No new unit tests required for this task - focus is on file copying and template creation. Existing scaffold_service tests should cover template rendering.

### Manual Validation
1. YAML frontmatter syntax validation using Python script
2. Visual inspection of YAML fields (name, description, tools, model, color)
3. Verification that tools list matches agent capabilities described in content
4. Path adaptation verification (no absolute paths remain)
5. Template variable injection verification (minimal, only where needed)

### Integration Tests
1. Verify scaffold_service.py can load all 7 agent templates
2. Verify templates render without Jinja2 errors
3. Verify rendered output has valid YAML frontmatter

### Edge Cases
- Missing source files: Handled by Task 1 fail-early check
- Invalid YAML in source: Fixed during Task 3 validation
- Template rendering errors: Caught during Task 8
- Path adaptation errors: Verified during Task 4 manual review

## Acceptance Criteria
- [ ] All 7 agent definition files exist in .claude/agents/ (BASE)
- [ ] All 7 agent definition files have valid YAML frontmatter
- [ ] YAML frontmatter contains required fields: name, description, tools (as list), model, color
- [ ] Tools list in each agent matches described capabilities
- [ ] No absolute paths remain in BASE files
- [ ] All 7 Jinja2 templates exist in tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/
- [ ] Templates preserve YAML frontmatter structure
- [ ] Templates inject minimal Jinja2 variables (only where project-specific)
- [ ] scaffold_service.py agent registration matches template filenames
- [ ] All validation commands pass with zero errors

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Verify BASE agent files exist
ls -la .claude/agents/

# Verify template files exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/.claude/agents/

# Validate YAML syntax in BASE files (run script from scratchpad)
uv run python /private/tmp/claude/-Users-hernandoescobar-Documents-Celes-tac-bootstrap-trees-feature-Tac-14-Task-2/*/scratchpad/validate_yaml.py .claude/agents/*.md

# Validate scaffold service registration
grep -A 20 "Agent definitions" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

# Run standard validation commands
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Path Adaptation Strategy
- Replace absolute paths like `/Users/...` or `/Volumes/...` with relative paths
- For BASE: Use paths relative to repository root (e.g., `specs/`, `agents/`)
- For TEMPLATES: Use Jinja2 variables like `{{ config.paths.specs_dir }}` where paths vary per project

### Template Variable Usage
Based on scaffold_service.py patterns, available config variables include:
- `{{ config.project.name }}`
- `{{ config.project.description }}`
- `{{ config.paths.specs_dir }}`
- `{{ config.paths.adws_dir }}`
- `{{ config.paths.logs_dir }}`
- `{{ config.paths.scripts_dir }}`
- `{{ config.paths.worktrees_dir }}`

### YAML Frontmatter Structure
```yaml
---
name: agent-name
description: Brief description of agent purpose
tools: Tool1, Tool2, Tool3  # Or as YAML list
model: opus|sonnet|haiku
color: blue|green|red|etc
---
```

### Scaffold Service Registration Pattern
The agents are registered in scaffold_service.py:459-475 following this pattern:
```python
agents = [
    ("docs-scraper.md", "Documentation scraping agent"),
    ("meta-agent.md", "Agent generation from specifications"),
    # ... etc
]
for agent, reason in agents:
    plan.add_file(
        f".claude/agents/{agent}",
        action=action,
        template=f"claude/agents/{agent}.j2",
        reason=reason,
    )
```

This means templates MUST be named exactly: `{agent-name}.md.j2`

### Fail-Fast Strategy
Per clarifications, if source files are unavailable or invalid:
1. Fail early in Task 1 with clear error message
2. Do not proceed to create files with guessed/incorrect content
3. Report to user that source files are inaccessible

### Backwards Compatibility
This change is additive - it adds missing agent definition files that are already referenced in scaffold_service.py but don't exist yet in the templates directory. No breaking changes to existing functionality.
