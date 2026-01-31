---
doc_type: feature
adw_id: feature_Tac_12_task_19
date: 2026-01-30
idk:
  - agent-generation
  - meta-agent
  - jinja2-template
  - claude-code-agent
  - yaml-frontmatter
  - natural-language-specification
  - agent-workflow
  - validation
tags:
  - feature
  - agent
  - code-generation
related_code:
  - .claude/agents/meta-agent.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Meta-Agent Definition Generator

**ADW ID:** feature_Tac_12_task_19
**Date:** 2026-01-30
**Specification:** specs/issue-471-adw-feature_Tac_12_task_19-sdlc_planner-meta-agent-definition.md

## Overview

Implemented a specialized meta-agent that automatically generates new Claude Code agent definitions from natural language specifications. The meta-agent creates both the base markdown file (.md) and its corresponding Jinja2 template (.j2), enforcing consistency and following established patterns across the codebase.

## What Was Built

- **Meta-agent definition file** (`.claude/agents/meta-agent.md`) with comprehensive 8-step workflow
- **Jinja2 template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`) for CLI generation
- **Integration** with scaffold_service.py to include meta-agent in the agents list
- **Validation framework** for agent specifications with known tool checking
- **Error handling** for edge cases (existing agents, missing specifications, invalid tools)
- **Example workflows** covering creation from scratch, template-based generation, and minimal specifications

## Technical Implementation

### Files Modified

- `.claude/agents/meta-agent.md`: Created comprehensive agent definition with 386 lines including detailed workflows, validation rules, and examples
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`: Created template version with {{ config.project.name }} variables
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added meta-agent to agents list (line ~413)

### Key Changes

- **YAML frontmatter** with tools (Read, Write, Edit, Glob, Grep), model (sonnet), and color (purple)
- **8-step workflow**: specification parsing → reference agent checking → validation → file generation → writing → success reporting
- **Comprehensive validation**: agent name format, tool availability, structure completeness, content quality
- **Three practical examples**: from-scratch creation, template-based creation, minimal specification handling
- **Tool-specific guidelines**: detailed instructions for Read, Write, Edit, Glob, Grep usage in agent generation context
- **Error handling sections**: unclear specifications, missing reference agents, invalid tools, file conflicts

## How to Use

### Basic Agent Creation

1. Invoke the meta-agent with a natural language specification:

```
@meta-agent Create a test-runner agent that runs pytest tests and reports failures. Needs Bash and Read tools.
```

2. The meta-agent will:
   - Parse your specification
   - Validate requirements
   - Check for existing agents
   - Generate both .md and .j2 files
   - Report success with next steps

### Template-Based Agent Creation

To create an agent based on an existing one:

```
@meta-agent Create a security-scanner agent like scout-report-suggest but focused on finding security vulnerabilities.
```

The meta-agent will read the reference agent and adapt its structure for the new purpose.

### Register the New Agent

After generation, manually add the agent to `scaffold_service.py`:

```python
("new-agent-name.md", "Brief description of the agent"),
```

## Configuration

The meta-agent accepts these specification elements:

- **Agent name**: Kebab-case identifier (e.g., "code-reviewer")
- **Description**: One-line purpose summary
- **Tools**: List from Claude Code toolkit (Read, Write, Edit, Glob, Grep, Bash, WebFetch, Task, TodoWrite, AskUserQuestion)
- **Capabilities**: What the agent should accomplish
- **Style**: YAML frontmatter (default) or markdown-only
- **Reference agent** (optional): Existing agent to use as template

## Testing

### Verify Agent Files

Check that the meta-agent files were created correctly:

```bash
ls -la .claude/agents/meta-agent.md
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2
```

### Test Agent Generation

Generate a simple test agent:

```bash
# In Claude Code session:
@meta-agent Create a simple echo-agent that reads input and writes it back. Tools: Read, Write.
```

### Run Validation Commands

Ensure all tests and checks pass:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Test Template Rendering

Verify the Jinja2 template renders correctly:

```bash
# Template should contain {{ config.project.name }} references
grep "config.project.name" tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2
```

## Notes

### Design Decisions

- **Tool selection**: Limited to Read, Write, Edit, Glob, Grep to avoid complex external dependencies
- **YAML frontmatter**: Chosen as default format for consistency with recent agents (scout-report-suggest, docs-scraper)
- **Manual scaffold update**: Updating `scaffold_service.py` remains manual to avoid accidental modifications to service layer
- **Validation approach**: Basic pattern checking rather than strict schema to allow flexibility in agent designs
- **Model choice**: Uses Sonnet for balanced performance and cost

### Limitations

- Does not automatically update `scaffold_service.py` (manual step required)
- Cannot execute or test generated agents automatically
- Validation is pattern-based, not comprehensive schema validation
- Reference agents from external volumes may not be accessible

### Future Enhancements

- Automated scaffold_service.py updates
- Agent testing framework integration
- Schema-based validation
- Agent versioning support
- Bulk agent generation from specification files
