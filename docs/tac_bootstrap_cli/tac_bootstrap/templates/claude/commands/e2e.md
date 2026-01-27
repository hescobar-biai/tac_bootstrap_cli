---
doc_type: folder
domain: tac_bootstrap_cli.templates.claude.commands.e2e
owner: UNKNOWN
level: L5
tags:
  - expert:infra
  - level:L5
  - topic:api
idk:
  - e2e-test-commands
  - playwright-automation
  - end-to-end-validation
  - browser-testing
  - integration-test-suite
  - test-scenario-execution
  - automated-qa
  - functional-testing
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/e2e
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

## Overview

E2E command templates for Claude Code slash commands. Provides end-to-end testing automation command definitions. Part of TAC Bootstrap CLI template generation system.

## Responsibilities

- Define e2e test execution commands for generated projects
- Template slash command configurations for browser-based testing
- Enable automated functional validation workflows
- Provide test runner command scaffolding

## Key APIs / Components

- E2E command templates (slash command definitions)
- Test execution configuration templates
- Browser automation integration points
- Test scenario command structures

## Invariants & Contracts

- Templates use Jinja2 variable substitution (`{{ config.* }}`)
- Commands integrate with Claude Code slash command system
- Test runners expect Playwright or similar browser automation
- Generated commands preserve project-specific test paths

## Side Effects & IO

- Templates generate `.claude/commands/e2e/*.md` files in target projects
- Executed commands trigger browser automation processes
- Test execution may create screenshot/trace artifacts
- Console output streamed during test runs

## Operational Notes

- Template rendering occurs during `tac-bootstrap init`
- Commands assume test infrastructure already installed
- Browser binaries must be available in target environment
- Parallel test execution support depends on test framework

## TODO / Gaps

- No docstrings or README available for detailed behavior
- Specific command definitions not visible without file content
- Test framework choice (Playwright/Cypress/etc) unclear
- Integration with CI/CD pipelines not documented