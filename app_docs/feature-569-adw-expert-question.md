---
doc_type: feature
adw_id: feature_Tac_13_Task_7
date: 2026-02-03
idk:
  - adw
  - workflow
  - expertise
  - validation
  - sdlc-orchestration
  - worktree-isolation
  - module-composition
  - trigger-automation
tags:
  - feature
  - expert-system
  - adw
related_code:
  - .claude/commands/experts/adw/question.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# ADW Expert Question Prompt

**ADW ID:** feature_Tac_13_Task_7
**Date:** 2026-02-03
**Specification:** specs/issue-569-adw-feature_Tac_13_Task_7-sdlc_planner-adw-expert-question.md

## Overview

This feature implements the question prompt for the ADW (AI Developer Workflow) Expert, following the TAC-13 dual strategy pattern. It enables agents to query the ADW expert's mental model about workflow patterns, isolation strategies, module composition, trigger automation, and SDLC orchestration before making changes to ADW code. This implements the **Reuse** step in the Act → Learn → Reuse loop.

## What Was Built

- **ADW Expert Question Command** - Read-only prompt that queries ADW expertise and validates against codebase
- **Jinja2 Template** - Template for generating the question command in new projects
- **Scaffold Registration** - Integration with scaffold_service.py for CLI generation
- **3-Phase Validation Workflow** - Read expertise → validate against code → report findings

## Technical Implementation

### Files Modified

- `.claude/commands/experts/adw/question.md` - Implementation file in repo root for immediate use
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2` - Jinja2 template for CLI generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registration in `_add_claude_code_commands()` method

### Key Changes

1. **Question Prompt Structure** - Follows TAC-13 3-phase pattern:
   - Phase 1: Read `.claude/commands/experts/adw/expertise.yaml` for mental model
   - Phase 2: Validate expertise claims against ADW codebase (`adws/`, `adw_modules/`, `adw_triggers/`)
   - Phase 3: Report findings with evidence (file paths + line numbers) and architectural context

2. **ADW-Specific Validation** - Checks for:
   - Isolation patterns in `adw_*_iso.py` files
   - Module composition patterns in `adw_modules/`
   - Trigger integration in `adw_triggers/`
   - SDLC orchestration chains
   - State management via `adw_state.json`
   - Metadata conventions (`/adw_id`, `/adw_sdlc_zte_iso`)

3. **Read-Only Operation** - Uses allowed-tools: Bash, Read, Grep, Glob, TodoWrite (no Edit/Write)

4. **Dual Strategy Implementation** - Creates both template (.j2) and implementation file for immediate testing

5. **Evidence-Based Reporting** - Responses include:
   - Direct answer using ADW terminology
   - Code evidence with file paths and line numbers
   - Context and relationships within ADW ecosystem
   - ADW-specific pattern analysis
   - Discrepancy reporting if expertise differs from code

## How to Use

### Invoking the Question Command

From the project root, ask the ADW expert a question:

```bash
# Ask about SDLC orchestration
experts/adw/question "How does SDLC orchestration work across isolated phases?"

# Ask about isolation patterns
experts/adw/question "What is the worktree isolation pattern?"

# Ask about module composition
experts/adw/question "How should I compose modules from adw_modules?"

# Ask about trigger automation
experts/adw/question "What trigger strategies are available?"
```

### Expected Workflow

1. Agent reads the ADW expertise file (mental model)
2. Agent identifies relevant sections for the question
3. Agent validates expertise claims against actual code in `adws/`, `adw_modules/`, `adw_triggers/`
4. Agent reports findings with:
   - Direct answer
   - Code evidence (file:line references)
   - Context and relationships
   - ADW pattern analysis
   - Discrepancies if any

### Example Questions

- "How does worktree isolation work in ADW workflows?"
- "What modules are available in adw_modules and how should they be composed?"
- "How are workflows chained together in SDLC orchestration?"
- "What trigger automation options exist?"
- "How is state managed across workflow phases?"
- "What metadata conventions should I follow for new workflows?"

## Configuration

No configuration required. The command uses static paths:

- **Expertise File**: `.claude/commands/experts/adw/expertise.yaml`
- **ADW Root**: `adws/`
- **ADW Modules**: `adws/adw_modules/`
- **ADW Triggers**: `adws/adw_triggers/`

## Testing

### Verify Template and Registration

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2 && echo "✓ Template exists"

# Verify registration in scaffold_service.py
grep -A 3 "experts/adw/question.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"

# Verify implementation file exists
test -f .claude/commands/experts/adw/question.md && echo "✓ Implementation file exists"
```

### Verify Structure

```bash
# Verify frontmatter structure
head -n 5 .claude/commands/experts/adw/question.md | grep -q "allowed-tools" && echo "✓ Frontmatter valid"

# Verify 3-phase structure
grep -q "Phase 1: Read Expertise File" .claude/commands/experts/adw/question.md && \
grep -q "Phase 2: Validate Expertise Against Codebase" .claude/commands/experts/adw/question.md && \
grep -q "Phase 3: Report Findings" .claude/commands/experts/adw/question.md && \
echo "✓ 3-phase structure present"

# Verify ADW-specific paths
grep -q "adws/" .claude/commands/experts/adw/question.md && \
grep -q "adw_modules/" .claude/commands/experts/adw/question.md && \
grep -q "adw_triggers/" .claude/commands/experts/adw/question.md && \
echo "✓ ADW paths referenced"
```

### Run Validation Suite

```bash
# Run standard validation suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### ADW Patterns Documented

The question prompt validates and reports on these key ADW patterns:

1. **Isolation Pattern** - `adw_*_iso.py` naming convention for standalone workflows
2. **Worktree Coordination** - Git worktrees under `trees/<adw_id>/` for parallel execution
3. **Module Composition** - Shared functionality via `adw_modules/` (state, git_ops, workflow_ops, etc.)
4. **Trigger Integration** - Automation scripts in `adw_triggers/` (cron, webhook, issue_chain, etc.)
5. **SDLC Orchestration** - Sequential workflow chaining (plan → build → test → review → document → ship)
6. **State Management** - Persistent coordination via `adw_state.json`
7. **Metadata Conventions** - `/adw_id`, `/adw_sdlc_zte_iso` format for workflow identification

### Design Decisions

- **Read-Only by Design** - Question prompt cannot modify code, only analyze and report
- **Code as Source of Truth** - Expertise file is mental model; always validate against actual code
- **Evidence-Based Reporting** - All answers include file paths and line numbers
- **Progressive Disclosure** - Start with expertise, validate against code, report with context
- **Dual Query Support** - Handles both general pattern questions and specific workflow queries

### Edge Cases Handled

1. **Missing ADW directories** - Informs user if `adws/`, `adw_modules/`, or `adw_triggers/` don't exist
2. **Empty expertise file** - Falls back to code-only analysis
3. **Malformed YAML** - Reports parsing errors and continues with code validation
4. **Non-existent workflows** - Guides user to available workflows
5. **General vs specific queries** - Supports both pattern and implementation questions

### Integration with Expert System

This question prompt complements the ADW expert system:

- **expertise.yaml** - Mental model (Act → Learn phase)
- **question.md** - Query mental model (Reuse phase)
- **self-improve.md** - Update mental model (Learn phase)

Together, these implement the complete Act → Learn → Reuse loop for ADW expertise accumulation and application.
