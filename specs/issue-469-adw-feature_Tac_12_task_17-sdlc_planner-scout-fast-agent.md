# Feature: Create scout-report-suggest-fast.md agent definition

## Metadata
issue_number: `469`
adw_id: `feature_Tac_12_task_17`
issue_json: `{"number": 469, "title": "[Task 17/49] [FEATURE] Create scout-report-suggest-fast.md agent definition", "body": "## Description\n\nCreate a fast scout agent optimized for quick exploration.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/scout-report-suggest-fast.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2`\n\n## Key Features\n- Optimized for speed\n- model: haiku (faster)\n- Similar structure to scout-report-suggest\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/scout-report-suggest-fast.md`\n\n## Wave 2 - New Agents (Task 17 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_17"}`

## Feature Description
Create a fast variant of the scout-report-suggest agent that uses the haiku model for faster execution while maintaining all the same capabilities. This agent will provide quicker responses for codebase analysis and reporting tasks where speed is prioritized over the most detailed analysis.

## User Story
As a developer using TAC Bootstrap
I want a fast scout agent for quick codebase analysis
So that I can get rapid feedback on code issues and research requests when I don't need the most thorough analysis

## Problem Statement
The current scout-report-suggest agent uses the sonnet model, which provides comprehensive analysis but can be slower for simple or time-sensitive inquiries. Users need a faster alternative for quick code exploration, rapid issue identification, and situations where speed is more valuable than exhaustive analysis.

## Solution Statement
Create a scout-report-suggest-fast agent that is identical to scout-report-suggest in structure and capabilities, but uses the haiku model instead of sonnet. This provides users with a speed-optimized option while maintaining the same workflow, tools, and reporting format. The agent will be available in both the base repository and as a Jinja2 template for CLI generation.

## Relevant Files
Files necessary for implementing the feature:

1. `.claude/agents/scout-report-suggest.md` - Source agent to base the fast variant on
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` - Template to create fast variant from
3. `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that needs to include new agent in generation list

### New Files
1. `.claude/agents/scout-report-suggest-fast.md` - Fast variant agent definition (base repository)
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2` - Fast variant Jinja2 template

## Implementation Plan

### Phase 1: Foundation
Read existing scout-report-suggest agent files to understand the complete structure and verify the pattern for agent definitions.

### Phase 2: Core Implementation
Create both the base agent file and the Jinja2 template for the fast variant, changing only the model to haiku and adding a brief note about speed optimization in the description.

### Phase 3: Integration
Update scaffold_service.py to include the new agent in the agents list so it gets generated for new projects.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create base agent file
- Create `.claude/agents/scout-report-suggest-fast.md`
- Copy structure from scout-report-suggest.md
- Change `model: sonnet` to `model: haiku`
- Update description to: "Use proactively to scout codebase issues, identify problem locations, and suggest resolutions. Fast variant optimized for speed using haiku model. Specialist for read-only analysis and reporting without making changes."
- Keep all other content identical (tools, workflow, report format)

### Task 2: Create Jinja2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2`
- Copy structure from scout-report-suggest.md.j2
- Apply same changes as in Task 1 (model and description)
- Ensure template variables remain identical to the regular scout-report-suggest template

### Task 3: Update scaffold_service.py
- Add entry to agents list in `_add_claude_files()` method around line 411-418
- Add tuple: `("scout-report-suggest-fast.md", "Fast codebase scouting and analysis agent (haiku model)")`
- Place it after the regular scout-report-suggest entry
- Ensure consistent formatting with existing entries

### Task 4: Validation
- Run validation commands to ensure no regressions
- Verify new agent file syntax is correct
- Verify template renders correctly
- Verify scaffold_service.py has no syntax errors

## Testing Strategy

### Unit Tests
- Verify that scaffold_service.py correctly includes the new agent in the plan
- Verify template renders correctly with sample config
- Verify both files (base and template) have identical structure except for expected differences

### Edge Cases
- Verify agent metadata is properly formatted with correct YAML frontmatter
- Verify description accurately reflects the speed optimization
- Verify all tools are correctly specified (Read, Glob, Grep)
- Verify color and other metadata fields are present

## Acceptance Criteria
1. `.claude/agents/scout-report-suggest-fast.md` exists in base repository
2. Template `scout-report-suggest-fast.md.j2` exists in templates directory
3. Agent uses `model: haiku` instead of sonnet
4. Agent description mentions speed optimization
5. All other agent capabilities, tools, workflow, and report format are identical to scout-report-suggest
6. `scaffold_service.py` includes new agent in agents list
7. All validation commands pass with zero regressions
8. Agent file has valid YAML frontmatter and markdown structure

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The fast agent provides the same functionality as the regular scout agent but with faster response times using the haiku model
- Users can choose between thorough analysis (sonnet) and quick analysis (haiku) based on their needs
- Both agents maintain identical thoroughness level options (quick/medium/very thorough) - speed comes from the model, not from limiting features
- The reference file path may not be accessible, so we use the existing scout-report-suggest.md in this repo as the authoritative source
- This is a minimal-diff approach - only model and description change, maintaining feature parity
