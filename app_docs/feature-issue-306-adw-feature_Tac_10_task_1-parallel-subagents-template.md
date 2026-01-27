---
doc_type: feature
adw_id: feature_Tac_10_task_1
date: 2026-01-26
idk:
  - delegation-prompt
  - parallel-agents
  - task-decomposition
  - compute-orchestration
  - tac-10
  - jinja2-template
  - command-template
tags:
  - feature
  - template
related_code:
  - .claude/commands/parallel_subagents.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2
---

# Parallel Subagents Template

**ADW ID:** feature_Tac_10_task_1
**Date:** 2026-01-26
**Specification:** specs/issue-306-adw-feature_Tac_10_task_1-sdlc_planner-parallel-subagents-template.md

## Overview

Created a new command template implementing TAC-10 Level 4 (Delegation Prompt) pattern that enables launching multiple agents in parallel for complex task decomposition and orchestration. The template exists in both Jinja2 format for CLI generation and as a rendered markdown file for direct usage.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2` - Template source for TAC Bootstrap CLI generation
- **Rendered Command**: `.claude/commands/parallel_subagents.md` - Functional command for immediate use in this repository (dogfooding)
- **Command Structure**: Full Input → Workflow → Output architecture with:
  - Variables: PROMPT_REQUEST ($1) and COUNT ($2, default: 3, range: 2-10)
  - Instructions: Guidance on when/how to use parallel decomposition
  - 4-step Workflow: Parse Input → Design Agent Prompts → Launch Parallel Agents → Collect & Summarize
  - Structured Report: Per-agent sections + overall summary with error handling

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/parallel_subagents.md.j2`: New Jinja2 template implementing TAC-10 Level 4 pattern
- `.claude/commands/parallel_subagents.md`: Rendered version for direct usage
- `tac_bootstrap_cli/tests/test_value_objects.py`: Minor test update (semantic version comparison)

### Key Changes

- **Template Architecture**: Follows established command template pattern with frontmatter, variables, instructions, workflow, and report sections
- **Decomposition Strategy**: Guides agents to split tasks by domain/concern with minimum overlap and clear deliverables
- **COUNT Validation**: Defaults to 3 agents, validates range [2-10], treats COUNT=1 as error case
- **Parallel Invocation**: Critical instruction to launch all agents in single message with multiple Task tool calls
- **Resilience Design**: Handles partial failures gracefully, continues with successful results, reports patterns when multiple agents fail
- **Structured Output**: Markdown-formatted report with per-agent sections and synthesized overall summary

## How to Use

The `/parallel_subagents` command accepts a task description and optional agent count:

1. **Basic Usage** (defaults to 3 agents):
```bash
/parallel_subagents "Implement user authentication system with backend API, frontend UI, and comprehensive tests"
```

2. **Specify Agent Count**:
```bash
/parallel_subagents "Refactor database layer across multiple modules" 5
```

3. **The Agent Will**:
   - Validate input and determine suitable agent count
   - Decompose the task into independent subtasks
   - Launch agents in parallel (single message, multiple Task tool calls)
   - Collect and synthesize results into structured report

## Configuration

### When to Use This Command

Use parallel subagents when:
- Task can be naturally decomposed into independent subtasks
- Subtasks can execute simultaneously without blocking each other
- Need to maximize throughput for complex multi-domain work
- Task involves multiple concerns (backend + frontend + tests + docs)

### When NOT to Use

Do NOT use parallel subagents when:
- Task is simple or straightforward
- Subtasks have strong sequential dependencies
- Task is inherently serial (step-by-step refactoring with shared state)
- COUNT=1 (use Task tool directly instead)

## Testing

Test the command directly in this repository:

```bash
/parallel_subagents "Analyze the TAC Bootstrap codebase structure and identify the three main architectural layers" 3
```

Test template rendering (requires TAC Bootstrap CLI implementation):

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

Verify template structure and syntax:

```bash
cd tac_bootstrap_cli
uv run ruff check .
uv run mypy tac_bootstrap/
```

## Notes

- This implements TAC-10 Level 4 (Delegation Prompt) pattern, representing S-tier usefulness with A-tier skill requirement
- The dual nature (.j2 template + rendered .md) reflects TAC Bootstrap's purpose as both generator and self-hosting example
- Default of 3 agents balances meaningful parallelization with resource efficiency
- Range [2-10] enforces true parallelization (minimum 2) while preventing resource exhaustion (maximum 10)
- Structured markdown report format is machine-parseable and human-readable
- Resilience design ensures partial failures don't block all progress
- This template will be used by other projects generated with TAC Bootstrap CLI
