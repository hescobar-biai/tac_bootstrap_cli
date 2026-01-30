# Feature: Create docs-scraper.md Agent Definition

## Metadata
issue_number: `470`
adw_id: `feature_Tac_12_task_18`
issue_json: `{"number": 470, "title": "[Task 18/49] [FEATURE] Create docs-scraper.md agent definition", "body": "## Description\n\nCreate a specialized agent for scraping and extracting documentation from web sources.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/docs-scraper.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`\n\n## Key Features\n- Web documentation scraping\n- Content extraction\n- tools: WebFetch, WebSearch, Read, Write\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/docs-scraper.md`\n\n## Wave 2 - New Agents (Task 18 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_18"}`

## Feature Description
This feature adds a `docs-scraper` agent definition to the TAC Bootstrap CLI. The agent is a user-invoked specialist that scrapes web documentation and saves it to local markdown files. It uses WebFetch and WebSearch to retrieve content from web sources and Write to save the processed documentation. The agent focuses on single-page scraping with minimal post-processing, relying on WebFetch's built-in HTML-to-markdown conversion.

The agent is part of Wave 2 of the TAC-12 agent definitions migration, which involves creating both a base agent file in `.claude/agents/` and a Jinja2 template for CLI generation.

## User Story
As a developer using TAC Bootstrap
I want a docs-scraper agent definition included in generated projects
So that users can easily scrape external documentation into their project context for AI-assisted development

## Problem Statement
TAC Bootstrap CLI needs to include the docs-scraper agent definition as part of its scaffold generation. Currently, the agent file exists in the reference repository but is not yet fully integrated into the TAC Bootstrap CLI template system. This prevents generated projects from having access to this useful documentation scraping capability.

## Solution Statement
Create both the base agent file (`.claude/agents/docs-scraper.md`) and its corresponding Jinja2 template (`.claude/agents/docs-scraper.md.j2`) in the TAC Bootstrap repository. The agent will be registered in `scaffold_service.py` so it's included when scaffolding new projects. The implementation follows the established pattern from other agents like `scout-report-suggest.md` and `build-agent.md`.

## Relevant Files
Files necessary for implementing the feature:

- `.claude/agents/docs-scraper.md` - Base agent definition file (ALREADY EXISTS - verified)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Jinja2 template (ALREADY EXISTS - verified)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that registers agents (ALREADY UPDATED - verified at line 412)

### New Files
No new files need to be created. All required files already exist.

## Implementation Plan

### Phase 1: Verification
Verify that all required files already exist and are properly configured.

### Phase 2: Testing
Test that the agent is properly included in scaffold generation.

### Phase 3: Documentation
Document the agent in relevant README files if needed.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Base Agent File
- Confirm `.claude/agents/docs-scraper.md` exists in the base repository
- Verify the agent content follows the standard agent format
- Check that the agent has proper description, purpose, tools, and instructions sections

### Task 2: Verify Jinja2 Template
- Confirm `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` exists
- Verify the template uses `{{ config.project.name }}` variable correctly
- Check that the template content matches the base agent file structure

### Task 3: Verify Scaffold Service Registration
- Confirm the agent is listed in `scaffold_service.py` in the `agents` list (around line 410-426)
- Verify the registration follows the pattern: `("docs-scraper.md", "Documentation scraping agent")`
- Check that the template path mapping is correct in `_add_claude_files` method

### Task 4: Test Agent Scaffolding
- Create a test project using `uv run tac-bootstrap wizard` or direct CLI command
- Verify `.claude/agents/docs-scraper.md` is created in the generated project
- Confirm the file content is properly rendered with project-specific variables
- Check file permissions (should be readable, not executable)

### Task 5: Validation Commands
- Execute all validation commands to ensure no regressions
- Run unit tests
- Run linting checks
- Run type checking
- Run smoke test

## Testing Strategy

### Unit Tests
- Test that `scaffold_service.py` includes docs-scraper in the agents list
- Test that the Jinja2 template renders correctly with sample config
- Test that file operations create the agent file in the correct location

### Edge Cases
- Empty or minimal config - should still render properly
- Missing project name in config - should handle gracefully
- Existing docs-scraper.md file - should skip (CREATE action) or overwrite (based on force flag)

## Acceptance Criteria
- [ ] Base agent file `.claude/agents/docs-scraper.md` exists and contains proper agent definition
- [ ] Jinja2 template `.claude/agents/docs-scraper.md.j2` exists and uses `{{ config.project.name }}` variable
- [ ] Agent is registered in `scaffold_service.py` agents list with description "Documentation scraping agent"
- [ ] Running `tac-bootstrap wizard` creates `.claude/agents/docs-scraper.md` in the generated project
- [ ] Generated agent file has project name properly substituted from config
- [ ] All validation commands pass with zero errors
- [ ] No regressions in existing agent scaffolding

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The docs-scraper agent is a user-invoked agent (not automatic)
- It uses WebFetch, WebSearch, Read, and Write tools
- Default behavior is single-page scraping; user must explicitly request additional pages
- No authentication support in initial version
- Minimal content processing - relies on WebFetch's HTML-to-markdown conversion
- Agent writes to user-specified locations (no hardcoded output directories)
- Template uses only `config.project.name` variable, no other config customization
- This is part of Wave 2 of TAC-12 agent definitions migration (Task 18 of 49)
