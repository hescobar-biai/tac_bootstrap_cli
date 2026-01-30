---
doc_type: feature
adw_id: feature_Tac_12_task_18
date: 2026-01-30
idk:
  - agent-definition
  - docs-scraper
  - web-scraping
  - jinja2-template
  - scaffold-service
  - documentation
tags:
  - feature
  - agent
  - scaffolding
related_code:
  - .claude/agents/docs-scraper.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# docs-scraper Agent Definition

**ADW ID:** feature_Tac_12_task_18
**Date:** 2026-01-30
**Specification:** specs/issue-470-adw-feature_Tac_12_task_18-sdlc_planner-create-docs-scraper-agent.md

## Overview

Added the `docs-scraper` agent definition to TAC Bootstrap CLI. This agent specializes in scraping and integrating external documentation into project contexts. The implementation includes both the base agent file for the TAC Bootstrap repository and a Jinja2 template for generating the agent in scaffolded projects.

## What Was Built

- Base agent definition file (`.claude/agents/docs-scraper.md`)
- Jinja2 template for CLI generation (`templates/claude/agents/docs-scraper.md.j2`)
- Registration in scaffold service for automatic inclusion in new projects

## Technical Implementation

### Files Modified

- `.claude/agents/docs-scraper.md`: Base agent definition with comprehensive instructions for web documentation scraping
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`: Jinja2 template using `{{ config.project.name }}` variable
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Agent registered in the agents list at line 412

### Key Changes

- Created specialized agent for fetching external documentation (API refs, framework guides, library docs) using WebFetch, WebSearch, Read, and Write tools
- Agent processes HTML/Markdown/PDF documentation and integrates it into `ai_docs/` directory structure
- Follows standard TAC Bootstrap agent pattern: base file + Jinja2 template + scaffold service registration
- Part of Wave 2 migration (Task 18/49) for TAC-12 agent definitions
- Implementation completed in commits 279ca76 and c5d29af; specification added in this branch

## How to Use

### For End Users (Generated Projects)

1. After scaffolding a project with TAC Bootstrap, the docs-scraper agent is available in `.claude/agents/docs-scraper.md`
2. Use the agent to fetch external documentation:
   ```
   User: "Scrape the FastAPI routing documentation"
   Agent: Fetches, processes, and saves to ai_docs/frameworks/fastapi-routing.md
   ```
3. The agent handles multiple documentation formats: HTML, Markdown, API specs, PDFs

### For TAC Bootstrap Developers

1. The base agent file serves as the reference implementation
2. The Jinja2 template enables project-specific customization during scaffolding
3. Modify `scaffold_service.py` if additional agents need to be registered

## Configuration

The agent template uses a single configuration variable:
- `{{ config.project.name }}`: Substituted during project scaffolding to personalize the agent description

No additional environment variables or configuration files are required.

## Testing

Test that the agent is properly scaffolded:

```bash
cd /tmp && uv run tac-bootstrap init --project-name test-proj --language python
```

Verify the generated project contains `.claude/agents/docs-scraper.md` with the project name substituted.

Run validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

All commands should pass with zero errors (718 tests passed, linting clean, type checking successful).

## Notes

- This is a user-invoked agent, not an automatic background agent
- Default behavior is single-page scraping; users must explicitly request multi-page scraping
- No authentication support in the initial version
- Minimal content processing relies on WebFetch's built-in HTML-to-markdown conversion
- Agent writes to user-specified locations with no hardcoded output directories
- Recommended documentation structure: `ai_docs/frameworks/`, `ai_docs/libraries/`, `ai_docs/apis/`, `ai_docs/internal/`
- Always attributes sources with URLs and fetch dates
- Part of Wave 2 of TAC-12 agent definitions migration (Task 18 of 49)
