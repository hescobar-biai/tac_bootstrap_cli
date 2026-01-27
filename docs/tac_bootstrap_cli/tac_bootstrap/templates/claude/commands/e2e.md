---
doc_type: folder
domain: tac_bootstrap_cli.templates.claude.commands.e2e
owner: UNKNOWN
level: L5
tags:
  - level:L5
  - topic:api
  - expert:backend
idk:
  - e2e-test-templates
  - playwright-commands
  - test-automation-slash-commands
  - sql-injection-validation
  - export-functionality
  - query-execution-testing
  - input-debounce-testing
  - jinja2-command-templates
  - claude-code-cli
  - mcp-playwright-integration
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/e2e
children: []
source_readmes: []
last_reviewed: 2026-01-27
---

## Overview

Template folder for end-to-end (e2e) test slash commands in Claude Code CLI. Contains command definitions for automated browser-based testing workflows targeting generated projects. Part of the TAC Bootstrap Agentic Layer template system.

## Responsibilities

- Define e2e test slash command templates for Jinja2 rendering
- Provide command structures for SQL injection, export, query execution, input validation tests
- Enable automated Playwright-based test execution via Claude Code CLI
- Template configuration for random query generation and complex filtering scenarios

## Key APIs / Components

- **e2e:README**: E2E test examples documentation for generated projects
- **e2e:test_sql_injection**: SQL injection protection test command
- **e2e:test_export_functionality**: Data export functionality test command
- **e2e:test_disable_input_debounce**: Input disabling and debouncing test command
- **e2e:test_complex_query**: Complex query with filtering test command
- **e2e:test_basic_query**: Basic query execution test command
- **e2e:test_random_query_generator**: Random query generator test command

## Invariants & Contracts

- All command templates must be valid Jinja2 syntax
- Commands reference `{{ config }}` variable for project-specific configuration
- Test commands assume Playwright MCP integration in target environment
- Each test command must be self-contained and executable independently

## Side Effects & IO

- Templates rendered during `tac-bootstrap` CLI execution to target project `.claude/commands/` directory
- Generated commands execute browser automation via Playwright MCP when invoked
- Test commands may create screenshots, network logs, console output files
- No side effects at template storage time; only during generation and command execution

## Operational Notes

- Templates are static until CLI generation phase
- Generated commands depend on Playwright MCP server availability in target environment
- Test execution performance varies by browser engine and network conditions
- Failure modes: missing Playwright installation, invalid selectors, network timeouts

## TODO / Gaps

- No Python docstrings available for verification of command behavior
- Actual command implementations not visible in this folder context
- README content not provided for validation of test coverage
- Integration with test-runner workflow unclear from folder alone
