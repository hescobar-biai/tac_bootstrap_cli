---
doc_type: feature
adw_id: feature_Tac_12_task_16
date: 2026-01-30
idk:
  - agent-definition
  - codebase-analysis
  - read-only
  - root-cause-analysis
  - structured-reporting
  - scout-agent
  - jinja2-template
  - scaffold-service
tags:
  - feature
  - agent
  - wave2
related_code:
  - .claude/agents/scout-report-suggest.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Scout-Report-Suggest Agent

**ADW ID:** feature_Tac_12_task_16
**Date:** 2026-01-30
**Specification:** specs/issue-468-adw-feature_Tac_12_task_16-sdlc_planner-scout-report-suggest-agent.md

## Overview

This feature adds a specialized scout-report-suggest agent to TAC Bootstrap CLI. This agent is a READ-ONLY codebase analysis specialist that investigates problems, identifies exact file locations with line numbers, performs root cause analysis, and provides structured reports with resolution suggestions - without making any code modifications.

## What Was Built

- Agent definition file at `.claude/agents/scout-report-suggest.md` with frontmatter and complete workflow
- Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` for CLI generation
- Integration with `scaffold_service.py` to include agent in generated projects
- Structured SCOUT REPORT format with 6 sections: Problem Statement, Findings, Detailed Analysis, Suggested Resolution, Additional Context, Priority Level

## Technical Implementation

### Files Modified

- `.claude/agents/scout-report-suggest.md`: New agent definition (125 lines) with complete workflow and report format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2`: Jinja2 template (identical to base agent, minimal variables)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added scout-report-suggest to agents list at line 417

### Key Changes

- **Agent Frontmatter**: Configured with name `scout-report-suggest`, tools limited to `Read, Glob, Grep` (read-only), model `sonnet`, color `blue`
- **6-Step Workflow**: Accept and Parse Input → Scout the Codebase → Analyze Identified Files → Identify Root Causes → Document Findings → Formulate Resolution Strategy
- **Structured Report Format**: Standardized output with SCOUT REPORT sections ensuring consistency and actionability across all scouting tasks
- **Root Cause Analysis Focus**: Explicitly looks for logic errors, missing error handling, performance bottlenecks, security vulnerabilities, code quality issues, and architecture problems
- **Service Registration**: Added tuple `("scout-report-suggest.md", "Codebase scouting and analysis agent")` to agents list in `scaffold_service.py:417`

## How to Use

### In TAC Bootstrap CLI

1. Generate a new project using `tac-bootstrap` CLI
2. The scout-report-suggest agent will be automatically included in `.claude/agents/` directory
3. Invoke the agent using the Task tool in Claude Code:
   ```
   Task(
     subagent_type="scout-report-suggest",
     prompt="Investigate why authentication fails for expired tokens",
     description="Scout auth issue"
   )
   ```

### Agent Invocation Pattern

The agent expects a problem description or research request and will:
- Use Glob to find relevant files
- Use Grep to search for patterns/keywords
- Use Read to analyze code sections
- Generate a structured SCOUT REPORT with findings and suggestions

### Example Use Cases

- Investigating bug reports by identifying exact locations
- Researching unfamiliar code patterns
- Analyzing potential security vulnerabilities
- Finding performance bottlenecks
- Understanding dependency relationships

## Configuration

### Agent Configuration (Frontmatter)

```yaml
name: scout-report-suggest
description: Use proactively to scout codebase issues, identify problem locations, and suggest resolutions. Specialist for read-only analysis and reporting without making changes.
tools: Read, Glob, Grep
model: sonnet
color: blue
```

### Template Variables

The Jinja2 template uses minimal variables (agent behavior is generic across projects). The template is essentially static content.

## Testing

### Validate Agent Registration

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Expected: CLI help displays without errors, confirming scaffold_service.py changes are valid.

### Run Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Expected: No type errors in scaffold_service.py modifications.

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Expected: No linting issues in modified files.

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Expected: All tests pass, confirming no regressions in scaffold service.

### Manual Integration Test

```bash
# Generate a test project
cd tac_bootstrap_cli
uv run tac-bootstrap init my-test-project --template basic

# Verify agent file exists
ls -la my-test-project/.claude/agents/scout-report-suggest.md

# Verify content matches template
cat my-test-project/.claude/agents/scout-report-suggest.md
```

Expected: Agent file exists with correct frontmatter and complete workflow documentation.

## Notes

- This is task 16/49 in Wave 2 (New Agents) of the TAC Bootstrap roadmap
- The agent is READ-ONLY by design - it uses only Read, Glob, and Grep tools to prevent accidental modifications
- The structured SCOUT REPORT format ensures consistent outputs across all scouting tasks, making reports actionable and predictable
- The agent operates with the `sonnet` model for balanced performance and cost
- Root cause analysis is a core capability - the agent systematically looks for logic errors, missing error handling, performance bottlenecks, security vulnerabilities, code quality issues, and architecture problems
- The agent definition is mostly static content - it describes generic agent behavior rather than project-specific logic
- Future enhancements could include integration with issue tracking systems or automated report generation workflows
