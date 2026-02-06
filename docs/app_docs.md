---
folder: app_docs
idk:
  - documentation
  - feature-tracking
  - orchestrator
  - agentic-workflows
  - test-coverage
---

# app_docs

Application documentation and feature specifications for TAC Bootstrap.

## Overview

The `app_docs/` directory contains feature documentation, test specifications, and implementation notes for TAC Bootstrap components. These markdown files track feature completeness, technical implementation details, and integration points.

## Contents

- **feature-\*.md** - Feature documentation files tracking specific implementations with metadata, overview, technical details, and usage instructions

## Key Files

### feature-4848fdf1-orchestrator-tests-docs.md
Comprehensive documentation for the ADW-to-SQLite bridge tests and orchestrator integration, including:
- 355-line test suite for database bridge
- 4 test fixtures using in-memory SQLite
- 13 test functions spanning 4 test classes
- Orchestrator integration section in `adws/README.md`
- Agent module improvements for quota exhaustion handling

## Structure Pattern

Feature documentation files follow a consistent frontmatter and markdown structure:
- **Frontmatter**: doc_type, adw_id, date, idk tags, related_code references
- **Overview**: High-level summary of what was built
- **What Was Built**: Key artifacts and implementations
- **Technical Implementation**: Files modified and key changes
- **How to Use**: Running tests and integration examples
- **Configuration**: Settings and environment variables
- **Testing**: Test command examples
- **Notes**: Important implementation details

## Related Directories

- `adws/` - AI Developer Workflows with test suite and database bridge
- `.claude/` - Claude Code configuration and commands
- `docs/` - Generated fractal documentation
