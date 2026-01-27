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
  - e2e-test-commands
  - playwright-test-automation
  - end-to-end-validation
  - sql-injection-tests
  - query-execution-tests
  - export-functionality
  - input-debounce-tests
  - random-query-generator
  - complex-query-filtering
  - test-suite-templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/e2e
children: []
source_readmes: []
last_reviewed: UNKNOWN
---

# Overview

E2E test command templates for Claude Code slash commands. Contains skill definitions for end-to-end testing workflows using Playwright automation framework. Templates generate test execution commands for SQL injection protection, export functionality, input handling, query operations, and random test generation.

# Responsibilities

- Define E2E test skill templates for generated projects
- Provide Playwright-based browser automation test patterns
- Template SQL injection security validation tests
- Template query execution and filtering test scenarios
- Template export functionality validation workflows
- Template input debouncing and state management tests
- Generate random query test automation
- Provide README documentation template for E2E test suite

# Key APIs / Components

- `e2e:README` - E2E test suite overview and examples documentation
- `e2e:test_sql_injection` - SQL injection protection validation
- `e2e:test_export_functionality` - Export feature validation
- `e2e:test_disable_input_debounce` - Input state and debouncing tests
- `e2e:test_complex_query` - Complex query with filtering validation
- `e2e:test_basic_query` - Basic query execution validation
- `e2e:test_random_query_generator` - Random query generation tests

# Invariants & Contracts

- All E2E test templates assume Playwright framework availability
- Test commands expect browser automation capabilities
- SQL injection tests validate security boundaries
- Query tests validate data integrity and filtering logic
- Export tests validate output format correctness
- Input tests validate debouncing and state management
- Templates generate executable skill definitions for Claude Code

# Side Effects & IO

- Generated test commands execute browser automation
- Test execution may create screenshots, network logs
- Database queries executed during test scenarios
- File exports generated and validated
- Console output captured for debugging
- Test results written to test framework output

# Operational Notes

- E2E tests require Playwright browser binaries installed
- Test execution time varies by complexity (SQL injection, exports longer)
- Random query generator creates non-deterministic test scenarios
- Browser automation may require headless mode for CI/CD
- Test templates assume project-specific query structures exist
- Complex query tests validate filtering, pagination, performance

# TODO / Gaps

- Template versioning strategy UNKNOWN
- Playwright configuration templating unclear
- Test data seeding approach not documented
- CI/CD integration patterns not specified
- Test reporting format not defined
- Browser compatibility matrix UNKNOWN