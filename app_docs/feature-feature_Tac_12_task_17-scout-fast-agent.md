---
doc_type: feature
adw_id: feature_Tac_12_task_17
date: 2026-01-30
idk:
  - agent-definition
  - haiku-model
  - scout-agent
  - codebase-analysis
  - read-only-workflow
  - jinja2-template
  - scaffold-service
tags:
  - feature
  - agent
  - performance
related_code:
  - .claude/agents/scout-report-suggest-fast.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Scout-Fast Agent Definition

**ADW ID:** feature_Tac_12_task_17
**Date:** 2026-01-30
**Specification:** specs/issue-469-adw-feature_Tac_12_task_17-sdlc_planner-scout-fast-agent.md

## Overview

Added a speed-optimized variant of the scout-report-suggest agent that uses the haiku model for faster codebase analysis and issue identification. This fast agent maintains identical functionality and reporting capabilities while prioritizing quick responses for time-sensitive code exploration tasks.

## What Was Built

- **Base Agent Definition**: Created `.claude/agents/scout-report-suggest-fast.md` with haiku model configuration
- **Jinja2 Template**: Created `scout-report-suggest-fast.md.j2` template for CLI generation
- **Scaffold Integration**: Updated `scaffold_service.py` to include the new agent in generated projects

## Technical Implementation

### Files Modified

- `.claude/agents/scout-report-suggest-fast.md`: New agent definition file using `model: haiku` for speed optimization
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest-fast.md.j2`: Jinja2 template version for CLI scaffold generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added scout-fast agent to the agents list at line 418

### Key Changes

1. **Model Configuration**: Changed from `model: sonnet` to `model: haiku` for faster execution
2. **Updated Description**: Added "Fast variant optimized for speed using haiku model" to agent description
3. **Maintained Feature Parity**: All tools (Read, Glob, Grep), workflow steps, and report format remain identical to the standard scout agent
4. **Scaffold Service Integration**: Added tuple entry `("scout-report-suggest-fast.md", "Fast codebase scouting agent (haiku)")` to agents list
5. **Template Synchronization**: Ensured both base file and Jinja2 template have identical structure

## How to Use

The scout-fast agent is automatically included when generating new projects with TAC Bootstrap:

1. **Generate a New Project**:
```bash
uv run tac-bootstrap new myproject
```

2. **Agent is Available in Generated Project**:
The agent definition will be created at `.claude/agents/scout-report-suggest-fast.md` in the generated project.

3. **Using the Agent** (in generated projects):
Invoke the agent for quick codebase analysis when speed is more important than exhaustive analysis. The agent maintains all the same capabilities as the standard scout agent including:
- Codebase scouting and file discovery
- Issue identification and root cause analysis
- Detailed reporting with file paths and line numbers
- Resolution suggestions and best practices

## Configuration

No additional configuration required. The agent uses:
- **Model**: haiku (fast)
- **Tools**: Read, Glob, Grep (read-only)
- **Color**: blue
- **Mode**: Read-only analysis

## Testing

Run the full test suite to verify integration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to ensure code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- The fast agent provides the same comprehensive workflow and reporting as the standard scout agent
- Speed optimization comes from using the haiku model, not from reducing features or capabilities
- Users can choose between thorough analysis (sonnet model) and quick analysis (haiku model) based on their specific needs
- Both agents support the same thoroughness levels (quick/medium/very thorough) in their invocation
- This follows a minimal-diff approach: only model selection and description differ from the standard scout agent
- The agent operates in read-only mode and cannot modify files, ensuring safe code exploration
