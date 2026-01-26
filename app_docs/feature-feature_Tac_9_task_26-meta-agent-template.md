---
doc_type: feature
adw_id: feature_Tac_9_task_26
date: 2026-01-26
idk:
  - jinja2-template
  - claude-code-agents
  - sub-agent
  - agent-architecture
  - meta-programming
  - delegation
tags:
  - feature
  - agent-template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2
---

# Meta-Agent Template for TAC Bootstrap

**ADW ID:** feature_Tac_9_task_26
**Date:** 2026-01-26
**Specification:** specs/issue-267-adw-feature_Tac_9_task_26-sdlc_planner-add-meta-agent-template.md

## Overview

Added a Jinja2 template for the meta-agent configuration to TAC Bootstrap CLI. The meta-agent is a specialized Claude Code sub-agent that acts as an agent architect, enabling dynamic creation of new sub-agent configuration files based on natural language descriptions. This expands TAC Bootstrap's capability to generate comprehensive agentic development environments with meta-programming features.

## What Was Built

- **Jinja2 Template File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`
  - Complete meta-agent configuration with YAML frontmatter
  - 10-step workflow for creating new agents
  - Integration with Claude Code documentation and Firecrawl API
  - Output format specification for generated agents

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`: Created new Jinja2 template for meta-agent configuration
  - Defines agent metadata in YAML frontmatter (name, description, tools, color, model)
  - Implements comprehensive workflow for agent creation
  - Specifies required tools: Write, WebFetch, Firecrawl scrape/search, MultiEdit
  - Uses opus model for advanced reasoning capabilities

### Key Changes

1. **Agent Frontmatter Configuration**
   - Name: `meta-agent`
   - Description: Action-oriented delegation prompt for automatic invocation
   - Tools: Write (file creation), WebFetch (documentation), Firecrawl (scraping), MultiEdit (batch edits)
   - Color: cyan (visual identification in Claude Code)
   - Model: opus (highest reasoning capability for architecting agents)

2. **10-Step Agent Creation Workflow**
   - Step 0: Fetch latest Claude Code documentation
   - Steps 1-9: Analyze requirements, generate name, select color, write delegation description, infer tools, construct system prompt, provide action list, incorporate best practices, define output structure
   - Step 10: Assemble complete agent file and write to `.claude/agents/` directory

3. **Output Format Specification**
   - Defines structured markdown template for generated agents
   - Includes frontmatter schema, Purpose section, Instructions section, Best Practices, and Report/Response format
   - Ensures consistency across all meta-generated agents

4. **Template Structure**
   - Pure template without Jinja2 variables (minimal config dependency)
   - Ready for CLI rendering and generation in target projects
   - Follows pattern established by docs-scraper.md.j2 template

## How to Use

Once TAC Bootstrap CLI supports agent template rendering, users can generate a meta-agent in their project:

1. Run TAC Bootstrap CLI to scaffold a new project or add components to existing project
2. CLI will render meta-agent.md.j2 template to `.claude/agents/meta-agent.md`
3. In Claude Code, invoke the meta-agent by describing a new agent need
4. Meta-agent will generate the new sub-agent configuration file automatically

### Example Usage Scenario

```bash
# Future CLI command (when implemented)
tac-bootstrap init my-project --with-agents

# This would generate:
# my-project/.claude/agents/meta-agent.md
# my-project/.claude/agents/docs-scraper.md
# ...other templates
```

Then in Claude Code:
```
User: "Create a database migration agent that handles schema changes"
Claude: [Automatically delegates to meta-agent]
Meta-agent: [Generates .claude/agents/database-migration.md with appropriate configuration]
```

## Configuration

This template uses minimal configuration:
- No Jinja2 variables required (unlike docs-scraper template which uses `config.project.name`)
- Standalone template that works across all project types
- Fixed tool set: Write, WebFetch, Firecrawl scrape/search, MultiEdit
- Fixed model: opus (for best agent architecture reasoning)

## Testing

### Template Validation

Verify template syntax and integration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Code Quality Checks

Ensure code quality standards:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Type Checking

Verify type safety:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test

Confirm CLI still functions:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Template Review

Inspect the generated template file:

```bash
cat tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2
```

Verify:
- Valid YAML frontmatter
- Complete workflow steps (0-10)
- Proper markdown formatting
- Correct tool specifications
- Output format example included

## Notes

- This template enables **meta-programming** in Claude Code: an agent that creates other agents
- The meta-agent uses **opus model** specifically for its superior reasoning needed when architecting new agents
- The template is part of TAC Bootstrap's expanding agent template library (alongside docs-scraper)
- **No rendered output** (`.claude/agents/meta-agent.md`) should be created in the bootstrap repository itself - rendering happens only when CLI generates target projects
- Future enhancements could include:
  - Template rendering validation in CI/CD pipeline
  - Additional agent templates (code-reviewer, debugger, test-writer, etc.)
  - Config-driven tool selection based on project stack
  - Agent template versioning and migration system
- The meta-agent's delegation description is crafted for **proactive invocation** by Claude Code when users describe agent creation needs
- Tools selected (Firecrawl, WebFetch) enable the meta-agent to stay current with Claude Code documentation
