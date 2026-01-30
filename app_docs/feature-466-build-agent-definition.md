---
doc_type: feature
adw_id: feature_Tac_12_task_14
date: 2026-01-30
idk:
  - agent-definition
  - parallel-build
  - file-implementation
  - workflow-delegation
  - claude-agent
  - scaffold-service
  - jinja2-template
tags:
  - feature
  - agent
  - build
  - parallel
related_code:
  - .claude/agents/build-agent.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Build Agent Definition

**ADW ID:** feature_Tac_12_task_14
**Date:** 2026-01-30
**Specification:** specs/issue-466-adw-feature_Tac_12_task_14-sdlc_planner-build-agent-definition.md

## Overview

Created a specialized build-agent definition that enables parallel file implementation in TAC Bootstrap workflows. This agent is designed to implement one specific file at a time based on detailed instructions, following a rigorous 6-step workflow that ensures production-quality code with proper verification and structured reporting.

## What Was Built

- **Agent Definition File**: `.claude/agents/build-agent.md` - Complete agent specification with metadata, workflow, and reporting format
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2` - Template for generating the agent in new projects
- **Scaffold Service Integration**: Updated `scaffold_service.py` to include build-agent in the agents list alongside docs-scraper, meta-agent, and research-docs-fetcher

## Technical Implementation

### Files Modified

- `.claude/agents/build-agent.md`: Created new agent definition file with complete 6-step workflow and structured report format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2`: Created Jinja2 template matching the agent definition for CLI generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added build-agent to the agents list at line 415

### Key Changes

- **Agent Configuration**: Defined build-agent with tools (Write, Read, Edit, Grep, Glob, Bash, TodoWrite), model (sonnet), and color (blue)
- **6-Step Workflow**: Implemented systematic approach: (1) Read spec, (2) Gather context, (3) Understand conventions, (4) Implement file, (5) Verify implementation, (6) Report completion
- **Structured Reporting**: Created comprehensive report format with Implementation Summary, Specification Compliance, Quality Checks, Issues & Concerns, and Code Snippet sections
- **Scaffold Integration**: Registered agent using the same pattern as existing agents, ensuring automatic inclusion in generated projects

## How to Use

### In TAC Bootstrap Base Repository

The build-agent is now available at `.claude/agents/build-agent.md` and can be invoked via the Task tool:

```bash
# Example: Delegate file implementation to build-agent
# From Claude Code, use Task tool with subagent_type="build-agent"
```

### In Generated Projects

When you generate a new project using tac-bootstrap CLI, the build-agent will be automatically included:

```bash
# Generate a new project (build-agent is automatically included)
uv run tac-bootstrap init my-project

# The generated project will have .claude/agents/build-agent.md
# Ready to use for parallel build workflows
```

### Typical Usage Pattern

The build-agent is designed to be used as part of parallel build workflows:

1. A parent agent (like build-swarm coordinator) creates detailed specifications for each file
2. Multiple build-agent instances are spawned in parallel using the Task tool
3. Each build-agent receives a specification and implements one file
4. Each agent follows the 6-step workflow and returns a structured report
5. The parent agent collects results and validates the overall build

## Configuration

### Agent Metadata

```yaml
name: build-agent
description: Use proactively when you need to delegate writing a single file as part of a parallel build workflow
tools: Write, Read, Edit, Grep, Glob, Bash, TodoWrite
model: sonnet
color: blue
```

### Workflow Steps

1. **Read and analyze the specification thoroughly**: Extract file path, requirements, constraints, dependencies
2. **Gather context by reading referenced files**: Examine examples, find related files, study codebase structure
3. **Understand codebase conventions**: Analyze import styles, naming conventions, error handling, documentation standards
4. **Implement the file according to specification**: Write production-quality code with proper error handling, type annotations, and documentation
5. **Verify the implementation**: Run type checks, linters, formatters, tests
6. **Report completion status**: Confirm file creation, note deviations, flag issues

## Testing

### Verify Agent Files Exist

```bash
# Check base repository agent
ls -la .claude/agents/build-agent.md

# Check template exists
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/build-agent.md.j2
```

### Validate Scaffold Service Integration

```bash
# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Test in Generated Project

```bash
# Generate a test project
cd tac_bootstrap_cli
uv run tac-bootstrap init test-project --force

# Verify build-agent was created
ls -la test-project/.claude/agents/build-agent.md
```

## Notes

- The build-agent is copied from the proven TAC-12 reference implementation at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/build-agent.md`
- No templating variables are used in the agent definition since agent behavior is project-agnostic
- The agent emphasizes meticulous attention to detail and requires verbose, detailed specifications to function properly
- The 6-step workflow ensures rigorous implementation with proper context gathering and verification
- The structured report format provides clear visibility into implementation quality and potential issues
- Directory creation for `.claude/agents/` is already handled in scaffold_service.py at line 112 in the `_add_directories` method
- This is Task 14 of 49 in Wave 2 - New Agents for TAC-12 integration, enhancing parallel build capabilities
