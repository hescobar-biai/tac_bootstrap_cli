# Feature: Create scout-report-suggest.md agent definition

## Metadata
issue_number: `468`
adw_id: `feature_Tac_12_task_16`
issue_json: `{"number": 468, "title": "[Task 16/49] [FEATURE] Create scout-report-suggest.md agent definition", "body": "## Description\n\nCreate a full scout agent for codebase exploration with detailed reports.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2`\n\n## Key Features\n- name: scout-report-suggest\n- tools: Read, Glob, Grep\n- model: sonnet\n- color: blue\n- READ-ONLY analysis\n- Structured SCOUT REPORT format\n- Root cause analysis\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest.md`\n\n## Wave 2 - New Agents (Task 16 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_16"}`

## Feature Description
This feature adds a specialized scout agent for codebase exploration with detailed reporting capabilities. The scout-report-suggest agent is a READ-ONLY analysis specialist that investigates problems, identifies exact file locations, performs root cause analysis, and provides structured reports with resolution suggestions. This agent is critical for the TAC Bootstrap workflow, enabling developers to quickly understand codebase issues without making modifications.

## User Story
As a developer using TAC Bootstrap CLI
I want to generate projects with a scout-report-suggest agent
So that I can efficiently explore codebases, identify issues, and receive detailed analysis reports without risking accidental modifications

## Problem Statement
The TAC Bootstrap CLI currently generates projects with several agents (build-agent, docs-scraper, meta-agent, playwright-validator, research-docs-fetcher), but lacks a specialized agent for codebase scouting and analysis. Developers need a READ-ONLY tool that can:
- Navigate unfamiliar codebases systematically
- Identify exact locations of issues with line numbers
- Perform root cause analysis
- Provide structured, actionable reports
- Suggest resolutions without implementing them

Without this agent, developers must manually search codebases or risk using editing agents that might modify files during exploration.

## Solution Statement
Implement the scout-report-suggest agent by:
1. Creating the base agent definition at `.claude/agents/scout-report-suggest.md` with exact content from the reference file
2. Creating a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` with minimal variable substitution (agent behavior is generic)
3. Updating `scaffold_service.py` to include scout-report-suggest in the agents list, following the existing pattern

The agent will use only READ-ONLY tools (Read, Glob, Grep), operate with the sonnet model, and produce structured SCOUT REPORT format outputs with sections for findings, detailed analysis, suggested resolutions, and additional context.

## Relevant Files
Files necessary for implementing the feature:

1. **Reference file** (source of truth):
   - `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest.md` - Contains exact agent definition to copy

2. **Base repository agent file** (to create):
   - `.claude/agents/scout-report-suggest.md` - Agent definition for this repo

3. **Template file** (to create):
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` - Jinja2 template for CLI generation

4. **Service file** (to modify):
   - `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add agent to agents list in `_add_claude_files` method

5. **Existing agents** (for pattern reference):
   - `.claude/agents/build-agent.md` - Example agent structure
   - `.claude/agents/playwright-validator.md` - Another agent example
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2` - Example template structure

### New Files
- `.claude/agents/scout-report-suggest.md` - Base agent definition (125 lines based on reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` - Jinja2 template (mostly static content)

## Implementation Plan

### Phase 1: Foundation
Read and understand the reference file structure, examine existing agent patterns in the codebase, and verify the scaffold_service.py registration mechanism.

### Phase 2: Core Implementation
Create the base agent file and template file with exact content from the reference, ensuring proper frontmatter (name, description, tools, model, color) and complete workflow documentation.

### Phase 3: Integration
Update scaffold_service.py to register the new agent, following the exact pattern used for existing agents (build-agent, playwright-validator, etc.).

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify reference file accessibility and read content
- Confirm reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest.md` is accessible
- Read complete reference file to extract exact content
- Note the structure: frontmatter (YAML), purpose section, workflow steps, report format

### Task 2: Create base agent file at `.claude/agents/scout-report-suggest.md`
- Copy exact content from reference file
- Verify frontmatter contains:
  - name: scout-report-suggest
  - description: Use proactively to scout codebase issues...
  - tools: Read, Glob, Grep
  - model: sonnet
  - color: blue
- Ensure all workflow steps (6 steps) are present
- Verify SCOUT REPORT format section is complete with all subsections

### Task 3: Create Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2`
- Copy content from base agent file
- Keep content mostly static (agent behavior is generic)
- Only add `{{ config.project.name }}` if explicitly referenced in examples/documentation
- Examine existing templates (build-agent.md.j2) to confirm pattern
- Ensure template renders valid markdown

### Task 4: Update scaffold_service.py to register the agent
- Locate the `_add_claude_files` method around line 266
- Find the `agents` list around line 410-424
- Add new tuple entry: `("scout-report-suggest.md", "Codebase scouting and analysis agent")`
- Follow alphabetical or logical ordering if present
- Maintain consistent formatting with existing entries

### Task 5: Validate implementation
- Read created files to verify content accuracy
- Check that scaffold_service.py syntax is correct
- Verify agent registration follows existing pattern
- Compare created template with existing templates for consistency
- Run validation commands (final step)

### Task 6: Run validation commands
- Execute all validation commands listed below to ensure zero regressions
- Verify type checking passes
- Confirm linting passes
- Run smoke test to ensure CLI still functions

## Testing Strategy

### Unit Tests
No specific unit tests required for this feature. The agent definition is a configuration file consumed by Claude Code at runtime. Validation occurs through:
- Template rendering validation (implicit in scaffold_service)
- Runtime validation by Claude Code when agent is invoked
- Manual inspection of generated files

### Edge Cases
- **Reference file unavailable**: If reference file cannot be read, fallback to creating agent based on spec requirements (tools, model, format sections)
- **Template variable confusion**: Ensure template uses minimal variables - agent behavior should be generic
- **Agent registration duplicates**: Check that scout-report-suggest is not already in the agents list
- **File permissions**: Ensure created files have appropriate permissions (agent files are markdown, should be readable)

## Acceptance Criteria
1. Base agent file `.claude/agents/scout-report-suggest.md` exists with exact content from reference file
2. Template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` exists and renders valid markdown
3. `scaffold_service.py` includes scout-report-suggest in agents list with appropriate description
4. Agent definition has correct frontmatter (name, description, tools: Read/Glob/Grep, model: sonnet, color: blue)
5. Agent definition includes complete workflow (6 steps) and SCOUT REPORT format documentation
6. All validation commands pass (pytest, ruff, mypy, smoke test)
7. Generated template follows same pattern as existing agent templates (build-agent, playwright-validator)

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is task 16/49 in Wave 2 (New Agents)
- Agent definitions are mostly static - they describe agent behavior, not project-specific logic
- The reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest.md` is the source of truth
- Follow existing agent patterns in `.claude/agents/` directory for consistency
- The agent uses READ-ONLY tools (Read, Glob, Grep) to prevent accidental modifications during exploration
- Root cause analysis is explicitly listed as a key feature and should be documented in the agent prompt
- The structured SCOUT REPORT format is critical - it provides consistency and actionability
- This agent will be generated for all new TAC Bootstrap projects going forward
