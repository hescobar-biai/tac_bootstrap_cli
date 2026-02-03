---
doc_type: feature
adw_id: feature_Tac_13_Task_10
date: 2026-02-03
idk:
  - command-expert
  - question-prompt
  - expertise-validation
  - phase-based-workflow
  - read-only-agent
  - slash-commands
  - template-jinja2
tags:
  - feature
  - expert-system
  - tac-13
related_code:
  - .claude/commands/experts/commands/question.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Commands Expert: Question Prompt

**ADW ID:** feature_Tac_13_Task_10
**Date:** 2026-02-03
**Specification:** specs/issue-572-adw-feature_Tac_13_Task_10-sdlc_planner-commands-expert-question.md

## Overview

This feature implements a Commands expert question prompt following the TAC-13 Agent Expert pattern for self-improving agents. The prompt enables agents to answer questions about the `.claude/commands/*` ecosystem by leveraging a mental model (expertise file) while validating against actual command files as the source of truth. This is the "Reuse" phase of the Act → Learn → Reuse loop.

## What Was Built

- **Jinja2 Template**: Created template for CLI generation at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`
- **Concrete Implementation**: Created command file at `.claude/commands/experts/commands/question.md` for immediate use in the repo
- **Registration**: Registered the template in `scaffold_service.py` to include it in CLI-generated projects
- **3-Phase Workflow**: Implemented Reuse → Validate → Answer pattern
- **Read-Only Agent**: Restricted to Bash, Read, Grep, Glob, TodoWrite tools only

## Technical Implementation

### Files Modified

- `.claude/commands/experts/commands/question.md` (294 lines): New command prompt with complete 3-phase workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2` (294 lines): Jinja2 template version for CLI generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (+8 lines): Registration of Commands expert question prompt

### Key Changes

1. **Frontmatter Configuration**
   - `allowed-tools`: Bash, Read, Grep, Glob, TodoWrite (read-only)
   - `description`: Answer questions about command structure and workflows without coding
   - `argument-hint`: [question] for user guidance
   - `model`: sonnet for optimal performance

2. **Variable System**
   - `USER_QUESTION`: `$1` (shell expansion for runtime argument)
   - `EXPERTISE_PATH`: `.claude/expertise/commands.yaml` (static reference)
   - `COMMANDS_ROOT`: `.claude/commands/` (static reference)

3. **Phase-Based Workflow**
   - **Phase 1: Read Expertise File** - Load mental model from YAML
   - **Phase 2: Validate Expertise Against Codebase** - Cross-reference with actual command files
   - **Phase 3: Report Findings** - Provide evidence-based answer with file:line citations

4. **Commands Domain Knowledge**
   - Frontmatter patterns (YAML structure, allowed-tools)
   - Variable patterns (`$1`, `$2` shell expansion)
   - Phase-based workflow patterns
   - Tool restriction scoping
   - Expert architecture (question, plan, build, improve)
   - Integration patterns (command chaining)

5. **Registration Pattern**
   - Added to `expert_commands` list in scaffold_service.py
   - Follows existing pattern from ADW expert (Task 9)
   - Includes descriptive comment with TAC-13 task reference

## How to Use

### As a User

Invoke the command to ask questions about command structure and workflows:

```bash
/experts/commands/question "How do command variables like $1 and $2 work?"
```

The agent will:
1. Read the Commands expertise file (`.claude/expertise/commands.yaml`)
2. Validate information against actual command files
3. Provide an evidence-based answer with file:line citations
4. Report any discrepancies between expertise and code

### As a Developer

When generating a new project with tac-bootstrap CLI, the Commands expert question prompt will be automatically included:

```bash
tac-bootstrap scaffold my-project
# Creates: my-project/.claude/commands/experts/commands/question.md
```

The template uses Jinja2 variable substitution for project-specific configuration:

```jinja2
You are the Commands Expert for {{ config.project.name }}.
```

## Configuration

### Tool Restrictions

The command is intentionally read-only with limited tools:
- **Bash**: For file listing and basic commands
- **Read**: For reading expertise and command files
- **Grep**: For pattern searches across commands
- **Glob**: For finding relevant command files
- **TodoWrite**: For tracking workflow progress

**Not allowed**: Edit, Write, Task (prevents code modifications)

### Variables

The command defines three variables:
- `USER_QUESTION` (`$1`): Required runtime argument containing the user's question
- `EXPERTISE_PATH`: Static path to expertise file (`.claude/expertise/commands.yaml`)
- `COMMANDS_ROOT`: Static path to commands directory (`.claude/commands/`)

### Model Selection

Uses `model: sonnet` for optimal balance of speed and capability for analysis tasks.

## Testing

### Validation Commands

Execute these commands to verify the feature works correctly:

```bash
# Test 1: File existence
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2 && echo "✅ Template exists" || echo "❌ Template missing"
```

```bash
# Test 2: Concrete implementation exists
test -f .claude/commands/experts/commands/question.md && echo "✅ Implementation exists" || echo "❌ Implementation missing"
```

```bash
# Test 3: YAML frontmatter validation
head -6 .claude/commands/experts/commands/question.md | grep -q "allowed-tools: Bash, Read, Grep, Glob, TodoWrite" && echo "✅ Read-only tools verified" || echo "❌ Wrong tools"
```

```bash
# Test 4: Registration verification
grep -q "experts/commands/question.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✅ Registration found" || echo "❌ Not registered"
```

```bash
# Test 5: Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
# Test 6: Linting
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
# Test 7: Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

```bash
# Test 8: Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Expertise File Not Yet Created

The expertise file (`.claude/expertise/commands.yaml`) will be created in TAC-13 Task 12. This question prompt is designed to work with that file but can operate without it by falling back to code-only analysis.

### Consistent Pattern with ADW Expert

This implementation mirrors the ADW expert question prompt from Task 9, maintaining architectural consistency:
- Same 3-phase workflow structure
- Same read-only tool restrictions
- Same evidence-based report format
- Same edge case handling patterns

### Commands-Specific Knowledge

The prompt has deep understanding of:
- **Frontmatter**: YAML headers with `allowed-tools`, `description`, `argument-hint`, `model`
- **Variables**: Shell positional parameters (`$1`, `$2`) with semantic mapping
- **Phases**: Multi-step workflow execution patterns (Phase 1, 2, 3)
- **Tool Restrictions**: Permission scoping per command via `allowed-tools`
- **Integration**: Command chaining and expert workflow orchestration
- **Expert Architecture**: Specialized commands (question, plan, build, improve)

### Evidence-Based Responses

All answers include:
- File paths with line number ranges (e.g., `.claude/commands/feature.md:15-20`)
- Relevant code snippets
- Context about how the feature fits into the ecosystem
- Usage examples with actual command invocations
- Validation status (expertise accurate vs. needs update)

### Edge Cases Handled

1. Missing commands directory
2. Empty or missing expertise file
3. Malformed YAML in expertise
4. Non-existent commands
5. General vs. specific queries
6. Nested command structure (`experts/*/`, `e2e/*`)

### Future Integration

When the expertise file is created (Task 12), this question prompt will immediately leverage it without any modifications required. The prompt is designed to work with or without the expertise file present.
