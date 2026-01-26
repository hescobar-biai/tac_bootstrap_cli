---
doc_type: feature
adw_id: feature_Tac_9_task_25_v2
date: 2026-01-26
idk:
  - jinja2-template
  - agent-definition
  - documentation-scraping
  - webfetch
  - ai-docs
  - template-generation
tags:
  - feature
  - general
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2
---

# Docs-Scraper Agent Template

**ADW ID:** feature_Tac_9_task_25_v2
**Date:** 2026-01-26
**Specification:** specs/issue-266-adw-feature_Tac_9_task_25_v2-sdlc_planner-docs-scraper-template.md

## Overview

This feature adds a reusable Jinja2 template for a docs-scraper agent that enables generated projects to integrate external documentation (API references, framework guides, library docs) into their AI-assisted development workflows. The template provides clear instructions for fetching, processing, and contextualizing documentation using Claude Code's built-in WebFetch tool.

## What Was Built

- **Jinja2 Template**: Created `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` with minimal templating using only `{{ config.project.name }}`
- **Instructional Content**: Comprehensive agent definition with step-by-step guidance on documentation scraping workflows
- **Example Workflows**: Included examples for scraping API docs, library references, and framework guides
- **Multi-format Support**: Instructions for handling HTML, Markdown, API specifications, and PDF documentation

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`: Created new Jinja2 template file (173 lines)

### Key Changes

- Added self-contained agent definition template following TAC Bootstrap conventions
- Implemented minimal Jinja2 templating pattern (only `{{ config.project.name }}`) consistent with other templates like `build.md.j2`
- Structured content in 6 main sections: identifying sources, fetching, processing, integrating, handling formats, and maintenance
- Included 3 practical example workflows demonstrating common use cases
- Defined recommended directory structure (`ai_docs/frameworks/`, `ai_docs/libraries/`, `ai_docs/apis/`, `ai_docs/internal/`)
- Added error handling guidance for common scenarios (inaccessible URLs, rate limiting, large content)

## How to Use

### For TAC Bootstrap Users

1. Generate a new project with TAC Bootstrap CLI:
```bash
uv run tac-bootstrap generate --config config.yml
```

2. The docs-scraper agent will be automatically included in `.claude/agents/docs-scraper.md` in the generated project

3. Use the agent by requesting documentation scraping:
```
"Use the docs-scraper agent to fetch FastAPI routing documentation"
```

### For Template Developers

1. The template is located at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`

2. When TAC Bootstrap renders this template, it substitutes `{{ config.project.name }}` with the actual project name from `config.yml`

3. To customize the template, edit the `.j2` file and follow the existing pattern

## Configuration

The template uses minimal configuration:

- **Required Variable**: `config.project.name` - The project name from the TAC Bootstrap configuration file
- **No Additional Config Needed**: The agent is self-contained and instructional, requiring no additional schema changes or configuration files

## Testing

Verify the template exists and contains correct content:

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2
```

Inspect the template content:

```bash
cat tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2
```

Verify Jinja2 variable usage (should return 1):

```bash
grep -c "{{ config.project.name }}" tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2
```

Test template rendering (if you have a rendered version):

```bash
cat .claude/agents/docs-scraper.md | grep -c "tac-bootstrap"
```

## Notes

- This template follows the YAGNI (You Ain't Gonna Need It) principle - keeping it simple without adding unnecessary configuration
- The template emphasizes using Claude Code's built-in WebFetch tool rather than external scraping libraries, maintaining consistency with the platform
- Common use cases include scraping API references (REST, GraphQL), framework documentation (React, FastAPI), library documentation (Python packages, npm modules), and internal company documentation
- The agent definition is instructional rather than pre-configured with hardcoded URLs, allowing maximum reusability across different projects and documentation sources
- Future enhancements could include automated update scripts or version-aware documentation management, but the initial implementation focuses on clear, actionable instructions
- The recommended `ai_docs/` directory structure helps organize documentation by type (frameworks, libraries, apis, internal) for better discoverability
