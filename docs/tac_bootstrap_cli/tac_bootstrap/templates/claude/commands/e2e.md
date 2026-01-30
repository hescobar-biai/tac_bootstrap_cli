---
doc_type: folder
domain: tac_bootstrap_cli.templates.claude.commands.e2e
owner: UNKNOWN
level: L5
tags:
  - topic:api
  - level:L5
  - expert:backend
idk:
  - e2e-test-command-templates
  - playwright-browser-automation
  - slash-command-test-definitions
  - jinja2-test-templates
  - claude-code-integration
  - test-scenario-bootstrapping
  - command-template-generation
  - browser-snapshot-validation
  - sql-injection-test-pattern
  - query-execution-e2e
  - export-functionality-validation
  - input-debounce-testing
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/e2e
children: []
source_readmes: []
last_reviewed: 2026-01-30
---

## Overview

Template directory for E2E (end-to-end) test command definitions within the Claude Code slash command system. Contains templates for generating browser-based integration test commands that bootstrap projects can inherit.

## Responsibilities

- Store E2E test command template files (Jinja2 format)
- Define slash command structure for various test scenarios (SQL injection, export functionality, complex queries, basic queries, input debouncing)
- Provide reusable test patterns for generated projects
- Enable consistent E2E testing interface across bootstrapped codebases

## Key APIs / Components

- Template files for test commands (`.jinja2` or similar extension expected)
- E2E command definitions following Claude Code slash command schema
- Test scenario templates: SQL injection protection, export functionality, query execution, random query generation, input handling
- Integration with parent `commands/` template system

## Invariants & Contracts

- Templates MUST conform to Claude Code slash command schema
- Each E2E command template MUST be independently executable
- Templates reference `{{ config }}` variable for project-specific configuration
- Generated commands MUST integrate with Playwright MCP or equivalent browser automation
- Test commands SHOULD be idempotent and side-effect aware

## Side Effects & IO

- Templates are read during CLI generation phase
- Generated E2E commands will perform browser automation (navigate, click, type, snapshot)
- Tests may create/modify test databases or fixtures
- Browser console logs and network requests captured during execution
- Screenshots and test artifacts written to output directories

## Operational Notes

- E2E tests are resource-intensive (browser instances, network calls)
- Template rendering occurs once at project generation time
- Generated commands used repeatedly during development/CI cycles
- Performance depends on target application responsiveness
- Failure modes: browser timeout, network flakiness, selector changes
- Scaling: parallel test execution requires isolated browser contexts

## TODO / Gaps

- No README or docstrings available to document specific test templates
- Unclear which test scenarios are currently implemented vs planned
- Template file inventory and naming conventions not specified
- Integration points with test runners (pytest, Jest) not documented
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
