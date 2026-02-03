---
doc_type: feature
adw_id: feature_Tac_13_Task_14
date: 2026-02-03
idk:
  - meta-agent
  - agent-generator
  - code-generation
  - template
  - yaml-frontmatter
  - slash-command
  - agentic-layer
tags:
  - feature
  - meta-agentics
  - automation
related_code:
  - .claude/commands/meta-agent.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Meta-Agent Generator Command

**ADW ID:** feature_Tac_13_Task_14
**Date:** 2026-02-03
**Specification:** specs/issue-576-adw-feature_Tac_13_Task_14-sdlc_planner-meta-agent-generator.md

## Overview

The meta-agent generator is a specialized slash command (`/meta-agent`) that automates the creation of new agent definition files. It functions as an "agent that creates agents," enabling developers to generate complete, production-ready agent files from natural language descriptions without manually writing boilerplate structure.

## What Was Built

- `/meta-agent` slash command implementation in `.claude/commands/meta-agent.md`
- Jinja2 template for CLI generation at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`
- Registration of the command in `scaffold_service.py` commands list
- Automated agent schema generation with YAML frontmatter validation
- Intelligent tool inference based on agent purpose
- Kebab-case name generation from descriptions
- Error handling for edge cases (existing files, minimal descriptions, missing directories)

## Technical Implementation

### Files Modified

- `.claude/commands/meta-agent.md`: Meta-agent command implementation (224 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`: Jinja2 template version (224 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added "meta-agent" to commands list (line 344)

### Key Changes

- **YAML Frontmatter Structure**: Defined allowed tools (Write, Read, Glob, Grep, AskUserQuestion), model (sonnet), and argument hints
- **5-Phase Workflow**: Parse & validate description → Infer configuration → Design structure → Validate & write → Report generation
- **Tool Inference Logic**: Maps agent capabilities to Claude Code tools (e.g., "runs tests" → Bash, "searches code" → Grep/Glob)
- **Agent Schema Enforcement**: Validates YAML frontmatter, required sections (Purpose, Workflow, Report), and prevents placeholder text
- **Name Generation**: Auto-generates kebab-case names from natural language descriptions
- **Directory Auto-Creation**: Creates `.claude/agents/` directory if missing
- **Conflict Resolution**: Prompts user before overwriting existing agent files

## How to Use

### Basic Usage

Invoke the command with a description of the desired agent:

```bash
/meta-agent "create a test-runner agent that executes pytest tests, parses failures, and reports results"
```

### Minimal Description (triggers clarification questions)

```bash
/meta-agent "docs updater"
```

The agent will ask clarifying questions about:
- What tasks should the agent perform?
- What tools will it need?
- Should it be proactive or reactive?
- Any personality/behavior requirements?

### Complete Description Example

```bash
/meta-agent "create a security-validator agent that scans code for vulnerabilities, checks dependencies for known CVEs, validates input sanitization, and reports findings with severity levels. Should be thorough and cautious. Needs Read, Grep, Bash tools."
```

### Generated Output

The command creates a file at `.claude/agents/[kebab-case-name].md` with:
- YAML frontmatter (name, description, tools, model, color)
- Purpose section explaining the agent's role
- Workflow section with 4-7 numbered steps
- Report/Response section defining output format

## Configuration

### Variables

- `AGENT_DESCRIPTION`: $ARGUMENTS - Natural language description of the agent to generate

### Allowed Tools

The meta-agent command has access to:
- **Write**: Creates the agent definition file
- **Read**: Validates written files and reads reference agents
- **Glob**: Checks for existing agents and directory structure
- **Grep**: Searches for patterns in existing agent files
- **AskUserQuestion**: Clarifies vague descriptions or handles conflicts

### Model Selection

Uses **sonnet** for balanced performance in generating agent definitions.

## Testing

### Verify Installation

```bash
# Check template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo "✓ Template"

# Check registration
grep -A 3 "meta-agent" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep -E "(meta-agent|template|reason)" && echo "✓ Registration"

# Check implementation exists
test -f .claude/commands/meta-agent.md && echo "✓ Implementation"
```

### Manual Testing Scenarios

Test the command with various inputs:

```bash
# 1. Minimal description (should ask questions)
/meta-agent "docs updater"

# 2. Complete description
/meta-agent "create a test-runner agent that executes pytest tests, parses failures, and reports results. Needs Bash and Read tools."

# 3. Agent name collision (test conflict resolution)
# First, create an agent, then try creating it again with same description

# 4. Invalid description (should reject)
/meta-agent "test"  # Too short (< 10 chars)
```

### Structure Validation

```bash
# Verify command structure
grep -E "^(allowed-tools:|description:|argument-hint:|Variables|Instructions|Report)" .claude/commands/meta-agent.md && echo "✓ Structure"
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Code Quality Checks

```bash
# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Patterns

- **Meta-Agentic**: Implements "agents that create agents" pattern from TAC-13 meta-agentics phase
- **AI-Powered Inference**: Uses AI reasoning to map descriptions to tools, models, and personality traits
- **Validation First**: Validates structure before writing to prevent broken files
- **Graceful Degradation**: Asks clarifying questions instead of failing on vague input

### Agent vs Command Naming

The `.claude/agents/meta-agent.md` file is an agent definition (used with `@meta-agent`), while `.claude/commands/meta-agent.md` is a slash command (used with `/meta-agent`). Both coexist and serve different purposes.

### Tool Inference Examples

The command maps capabilities to tools:
- "runs tests" → Bash tool
- "updates files" → Edit, Read tools
- "searches code" → Grep, Glob tools
- "asks questions" → AskUserQuestion tool
- "creates files" → Write tool
- "launches sub-tasks" → Task tool

### Future Enhancements

- Integration with scaffold_service.py to auto-register generated agents
- Support for agent variants/versioning (e.g., "agent-v2")
- Agent templates library for common patterns (CRUD, API client, validator)
- Agent composition (combining multiple agent patterns)
- Interactive wizard mode for step-by-step agent generation
