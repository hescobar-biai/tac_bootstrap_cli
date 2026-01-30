---
doc_type: feature
adw_id: feature_Tac_12_task_15
date: 2026-01-30
idk:
  - playwright
  - e2e-testing
  - browser-automation
  - test-validation
  - agent-definition
  - jinja2-template
  - scaffold-service
tags:
  - feature
  - agents
  - testing
related_code:
  - .claude/agents/playwright-validator.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Playwright Validator Agent

**ADW ID:** feature_Tac_12_task_15
**Date:** 2026-01-30
**Specification:** specs/issue-467-adw-feature_Tac_12_task_15-sdlc_planner-playwright-validator-agent.md

## Overview

Created a specialized Claude Code agent for browser automation and end-to-end (E2E) validation using Playwright. This agent enables users to run E2E tests, validate UI functionality, capture screenshots/videos on failures, and automate browser-based workflows with structured guidance and evidence collection. The implementation follows the established agent pattern in TAC Bootstrap with both a base file and Jinja2 template for CLI generation.

## What Was Built

- **Base Agent Definition**: `.claude/agents/playwright-validator.md` with complete frontmatter, workflow instructions, and structured reporting format
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2` for CLI generation with project-specific templating
- **Scaffold Integration**: Updated `scaffold_service.py` to include playwright-validator in the agents list for automatic generation

## Technical Implementation

### Files Modified

- `.claude/agents/playwright-validator.md`: New base agent definition with Purpose, Workflow (7 steps), and Report/Response sections. Configured with tools (Bash, Read, Write, Edit, Grep, Glob, TodoWrite), model (sonnet), and color (green).

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/playwright-validator.md.j2`: Jinja2 template mirroring base agent with minimal templating using `{{ config.project.name }}` in description and Purpose sections.

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:416`: Added `("playwright-validator.md", "Playwright E2E validation agent")` to the agents list in `_add_claude_files` method.

### Key Changes

- **Agent Frontmatter**: Defined name, description (action-oriented delegation), tools array, model, and color following existing agent patterns from build-agent.md and meta-agent.md

- **Comprehensive Workflow**: 7-step validation process covering test discovery, environment preparation, test execution, failure handling with evidence capture, result analysis, evidence organization, and structured reporting

- **Multi-Browser Support**: Instructions support all three Playwright browsers (chromium, firefox, webkit) with headless (default) and headed (debugging) modes

- **Evidence Collection**: Automatic screenshot and video capture on test failures using Playwright's built-in capabilities in `test-results/` directory

- **Structured Output Format**: Detailed reporting template including test execution summary, failed test details with evidence paths, failure analysis, recommendations, and next steps

## How to Use

### For TAC Bootstrap Repository

The playwright-validator agent is now available in `.claude/agents/` and can be invoked manually for E2E testing tasks:

1. Configure Playwright in your project with `playwright.config.ts` or `playwright.config.js`
2. Create E2E test files in your configured test directory (e.g., `tests/`, `e2e/`)
3. Invoke the agent manually when you need to run tests, validate UI, or debug browser automation
4. The agent will discover tests, execute them, capture evidence on failures, and provide structured reports

### For Generated Projects (via TAC Bootstrap CLI)

When developers run `tac-bootstrap init <project>`, the CLI will now automatically generate the playwright-validator agent:

1. The agent will be created at `<project>/.claude/agents/playwright-validator.md`
2. The agent description will reference the project name from the configuration
3. Developers can invoke the agent for E2E testing workflows in their generated project

### Agent Capabilities

- Test discovery from Playwright configuration
- Multi-browser execution (chromium, firefox, webkit)
- Headless and headed modes
- Automatic screenshot/video capture on failures
- Test result parsing and analysis
- Failure categorization (functional bugs, flaky tests, configuration issues)
- Evidence organization with file paths
- Structured reporting with recommendations

## Configuration

The agent respects existing Playwright configuration rather than overriding settings. Key configuration considerations:

- **Playwright Config**: Expects `playwright.config.ts` or `playwright.config.js` in the project root
- **Test Directories**: Typically `tests/`, `e2e/`, or patterns defined in Playwright config
- **Browser Settings**: Uses project's browser configuration (chromium/firefox/webkit)
- **Screenshot/Video**: Automatic capture enabled by default in Playwright for failed tests
- **Environment Variables**: Validates test environment variables if required by tests

### Template Variables

The Jinja2 template uses minimal templating:
- `{{ config.project.name }}` - Injected into description and Purpose section for project-specific context

## Testing

### Validation Commands

Run all validation commands to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Unit tests for scaffold service and template rendering.

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Linting validation.

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Type checking.

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

CLI smoke test to verify the agent is included in scaffold plan generation.

### Integration Testing

To verify the agent is properly integrated:

1. Generate a new project with TAC Bootstrap CLI
2. Check that `.claude/agents/playwright-validator.md` is created in the generated project
3. Verify the agent file has correct frontmatter and project-specific references
4. Confirm the agent follows the 3-section structure (Purpose, Workflow, Report/Response)

## Notes

- The agent follows a **manual invocation model** - it is not triggered automatically but invoked when E2E testing is needed
- Focus is strictly on **functional E2E validation** - visual regression, accessibility testing, and performance testing are explicitly out of scope
- **Browser-agnostic design** respects existing Playwright configuration rather than hardcoding browser preferences
- **Evidence capture** (screenshots/videos) is handled automatically by Playwright's built-in capabilities
- Default mode is **headless** for CI-compatibility; headed mode available for debugging
- Agent includes best practices like test file references with line numbers (e.g., `tests/login.spec.ts:42`)
- Future iterations may include example Playwright test workflows or expanded debugging capabilities
- Playwright installation and setup instructions are referenced but not duplicated (assumes project has Playwright configured)
