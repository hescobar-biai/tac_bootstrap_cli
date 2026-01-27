---
doc_type: folder
domain: tac_bootstrap_cli.templates.claude.commands.e2e
owner: UNKNOWN
level: L5
tags:
  - expert:backend
  - level:L5
  - topic:api
idk:
  - e2e-test-commands
  - playwright-test-templates
  - end-to-end-validation
  - integration-test-scenarios
  - ui-automation
  - api-e2e-testing
  - test-command-generators
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/e2e
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

Template directory for end-to-end (E2E) test command definitions in Claude Code slash commands. Contains command templates that will be instantiated when generating project-specific E2E test workflows.

# Responsibilities

- Provide reusable E2E test command templates
- Define slash command structure for E2E test execution
- Template integration test scenarios (UI, API, database)
- Support Playwright/browser-based E2E workflows
- Enable test command customization via Jinja2 variables

# Key APIs / Components

- Slash command templates for E2E test runners
- Test scenario command definitions
- E2E workflow command templates (basic-query, complex-query, export, SQL-injection, etc.)
- Integration with project test infrastructure

# Invariants & Contracts

- Templates use `{{ config }}` Jinja2 variable structure
- Commands must be valid slash command format
- Generated commands integrate with project's test runner
- Template outputs are valid markdown/command definitions

# Side Effects & IO

- No direct IO (template directory only)
- Generated commands may execute browser automation
- Generated commands may trigger API calls, database queries
- Test execution side effects depend on instantiated templates

# Operational Notes

- Templates instantiated during `tac-bootstrap init` or generation phase
- E2E commands typically require test environment setup
- Browser/Playwright dependencies needed for UI E2E tests
- Performance depends on generated test complexity

# TODO / Gaps

- No source files currently present in directory
- Missing README or template examples
- Command template inventory unknown
- Integration with parent command structure unclear