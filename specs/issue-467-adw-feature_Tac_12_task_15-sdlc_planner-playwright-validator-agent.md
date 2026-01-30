# Feature: Create playwright-validator.md Agent Definition

## Metadata
issue_number: `467`
adw_id: `feature_Tac_12_task_15`
issue_json: `{"number":467,"title":"[Task 15/49] [FEATURE] Create playwright-validator.md agent definition","body":"## Description\n\nCreate an agent for browser automation and E2E validation.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/playwright-validator.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2`\n\n## Key Features\n- Browser automation with Playwright\n- E2E test execution\n- UI validation\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/playwright-validator.md`\n\n## Wave 2 - New Agents (Task 15 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_15"}`

## Feature Description
Create a specialized Claude Code agent for browser automation and end-to-end (E2E) validation using Playwright. This agent will enable users to run E2E tests, validate UI functionality, capture screenshots/videos on failures, and automate browser-based workflows. The agent follows the established pattern of other agents in the TAC Bootstrap ecosystem, providing both a base implementation file and a Jinja2 template for CLI generation.

## User Story
As a developer using TAC Bootstrap
I want to have a specialized Playwright validation agent
So that I can automate E2E testing, validate UI functionality, and debug browser-based workflows with structured guidance and error capture

## Problem Statement
Currently, the TAC Bootstrap CLI generates four agents (docs-scraper, meta-agent, research-docs-fetcher, build-agent) but lacks an agent for browser automation and E2E validation. Developers need structured guidance for running Playwright tests, handling test failures, capturing evidence (screenshots/videos), and validating UI functionality. Without this agent, users must manually craft Playwright testing workflows without the benefit of specialized agent instructions.

## Solution Statement
Create a `playwright-validator` agent that provides specialized workflows for E2E testing and browser automation. The agent will:
1. Guide users through Playwright test execution with proper configuration
2. Handle test failures gracefully with screenshot/video capture
3. Support all three Playwright browsers (chromium, firefox, webkit)
4. Follow manual invocation model for local test execution
5. Provide structured output reporting with test results and evidence
6. Include comprehensive instructions for functional E2E validation

The implementation includes both the base agent file (`.claude/agents/playwright-validator.md`) and a Jinja2 template (`.../templates/claude/agents/playwright-validator.md.j2`) for CLI generation, plus integration into `scaffold_service.py`.

## Relevant Files
Files necessary for implementing this feature:

### Base Agent File
- `.claude/agents/playwright-validator.md` - Base implementation of the playwright-validator agent in this repository

### Template Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2` - Jinja2 template for CLI generation

### Integration Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that manages agent generation, needs update to include playwright-validator in agents list (around line 410-424)

### Reference Agent Files (for pattern consistency)
- `.claude/agents/build-agent.md` - Example of frontmatter with tools, 3-section structure
- `.claude/agents/meta-agent.md` - Example of Purpose/Workflow/Report sections
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Example of minimal Jinja2 templating with {{ config.project.name }}

### New Files
- `.claude/agents/playwright-validator.md` (base agent definition)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2` (Jinja2 template)

## Implementation Plan

### Phase 1: Foundation
Study existing agent patterns to ensure consistency:
1. Read existing agents (build-agent.md, meta-agent.md) to understand frontmatter structure, tool definitions, and 3-section pattern
2. Read docs-scraper.md.j2 template to understand Jinja2 templating approach
3. Review scaffold_service.py to understand agent registration pattern

### Phase 2: Core Implementation
Create the playwright-validator agent files:
1. Create base agent file `.claude/agents/playwright-validator.md` with:
   - Frontmatter defining name, description, tools (Bash, Read, Write, Edit, Grep, Glob, TodoWrite), model, color
   - Purpose section explaining the agent's role
   - Workflow section with numbered instructions for E2E validation
   - Report/Response section defining structured output format
2. Create Jinja2 template `playwright-validator.md.j2` with minimal templating (only {{ config.project.name }})

### Phase 3: Integration
Integrate the agent into the CLI generation system:
1. Update `scaffold_service.py` to include `("playwright-validator.md", "Playwright E2E validation agent")` in the agents list
2. Verify the agent is included in scaffold plan generation

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Study Existing Agent Patterns
- Read `.claude/agents/build-agent.md` to understand frontmatter structure (name, description, tools, model, color)
- Read `.claude/agents/meta-agent.md` to understand Purpose/Workflow/Report sections
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` to understand Jinja2 templating approach
- Note the 3-section pattern: Purpose, Instructions/Workflow, Report/Response

### Task 2: Create Base Agent File
- Create `.claude/agents/playwright-validator.md` with:
  - Frontmatter: name=playwright-validator, description (action-oriented delegation description), tools=(Bash, Read, Write, Edit, Grep, Glob, TodoWrite), model=sonnet, color=green
  - Purpose section: Define role as E2E validation specialist
  - Workflow section: Numbered instructions covering:
    1. Test discovery and configuration validation
    2. Test execution with browser selection (chromium/firefox/webkit)
    3. Failure handling with screenshot/video capture
    4. Test result analysis and reporting
    5. Evidence collection and organization
  - Report/Response section: Define structured output format with test results, failures, evidence paths
- Focus on functional E2E validation only (no visual regression, accessibility, performance)
- Support both headless (default) and headed (debugging) modes
- Browser-agnostic design respecting Playwright config

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2`
- Copy content from base agent file
- Add minimal Jinja2 templating:
  - Use `{{ config.project.name }}` in description/purpose sections where contextually appropriate
  - Keep templating minimal following docs-scraper.md.j2 pattern
  - Do not add complex conditionals or loops

### Task 4: Update Scaffold Service
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- In `_add_claude_files` method, locate the agents list (around line 410-424)
- Add entry: `("playwright-validator.md", "Playwright E2E validation agent")`
- Maintain alphabetical or logical ordering with other agents

### Task 5: Validation
- Run all validation commands to ensure zero regressions
- Verify agent files are properly formatted
- Confirm Jinja2 template renders correctly
- Check that scaffold_service.py includes the new agent

## Testing Strategy

### Unit Tests
- No new unit tests required - this is a configuration/content change
- Existing scaffold_service tests should pass without modification
- If template rendering tests exist, they should automatically pick up the new agent template

### Integration Tests
- Verify scaffold plan includes playwright-validator.md in agent files
- Test template rendering with sample TACConfig
- Confirm generated agent file has correct frontmatter and structure

### Edge Cases
- Empty project name in config (Jinja2 template should handle gracefully)
- Missing Playwright configuration (agent should instruct user to create one)
- Test failures without screenshot capability (agent should handle gracefully)

## Acceptance Criteria
1. Base agent file `.claude/agents/playwright-validator.md` exists with:
   - Valid frontmatter (name, description, tools, model, color)
   - Purpose section defining agent role
   - Workflow section with comprehensive E2E validation instructions
   - Report/Response section defining structured output
2. Jinja2 template `playwright-validator.md.j2` exists with minimal templating ({{ config.project.name }})
3. `scaffold_service.py` includes playwright-validator in agents list
4. All validation commands pass (pytest, ruff, mypy, smoke test)
5. Agent follows established patterns from build-agent and meta-agent
6. Agent includes instructions for:
   - Browser automation with Playwright
   - E2E test execution
   - Screenshot/video capture on failures
   - Structured test result reporting
   - Support for chromium/firefox/webkit browsers
   - Headless and headed modes

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The agent follows manual invocation model (not triggered automatically)
- Focus on functional E2E validation only - visual regression, accessibility, and performance testing are out of scope
- Browser selection defaults to chromium but supports all three Playwright browsers via config
- Headless mode is default for CI-friendliness, headed mode for debugging
- The agent is browser-agnostic and respects existing Playwright configuration rather than hardcoding preferences
- Screenshot and video capture are core Playwright capabilities and essential for E2E validation
- Consider adding example Playwright test workflows in future iterations
- May need to document Playwright setup/installation in agent instructions or reference existing docs
