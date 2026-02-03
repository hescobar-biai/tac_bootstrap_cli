---
doc_type: feature
adw_id: feature_Tac_13_Task_4
date: 2026-02-02
idk:
  - agent-experts
  - mental-model
  - expertise-file
  - read-only-query
  - dual-strategy
  - jinja2-template
  - slash-command
  - evidence-based-reporting
tags:
  - feature
  - agent-experts
  - cli
related_code:
  - .claude/commands/experts/cli/question.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# CLI Expert: Question Prompt

**ADW ID:** feature_Tac_13_Task_4
**Date:** 2026-02-02
**Specification:** specs/issue-566-adw-feature_Tac_13_Task_4-sdlc_planner-cli-expert-question-prompt.md

## Overview

Implemented the "question prompt" for the CLI Expert following the TAC-13 dual strategy pattern. This slash command enables read-only interrogation of the CLI expert's expertise (mental model) to answer questions about the CLI without making code modifications. It's the first of three files in the CLI expert system (question.md, self-improve.md, expertise.yaml).

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2` - Template for CLI generation with Jinja2 variable substitution
- **Implementation File**: `.claude/commands/experts/cli/question.md` - Ready-to-use command in repo root with hardcoded values for tac_bootstrap
- **Template Registration**: Added to `scaffold_service.py` for automatic inclusion in scaffolded projects

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2` (new): Jinja2 template with `{{ config.project.name }}` variable for project-agnostic generation
- `.claude/commands/experts/cli/question.md` (new): Implementation file with hardcoded "tac-bootstrap" values for immediate local use
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:488-489`: Added template registration to `_add_claude_code_commands()` method

### Key Changes

1. **Dual Strategy Implementation**: Created both template (for generation) and implementation (for local use) versions following TAC-13 pattern
2. **Read-Only Design**: Command restricts to `Bash, Read, Grep, Glob, TodoWrite` tools - no code modifications allowed
3. **Three-Phase Workflow**:
   - Phase 1: Read expertise file (mental model)
   - Phase 2: Validate expertise against actual codebase (source of truth)
   - Phase 3: Report findings with evidence (file paths + line numbers)
4. **Evidence-Based Reporting**: Structured output format with direct answers, code references, expertise validation, and discrepancy flagging
5. **Template Registration**: Added to expert commands list in scaffold service with reason "CLI expert question prompt for read-only queries"

### Architecture Details

The question prompt implements the "Reuse" step of the Act→Learn→Reuse cycle:
- **Reuse**: Start with expertise (mental model) - this command
- **Act**: Execute work with expertise guidance (future build commands)
- **Learn**: Update expertise based on changes (self-improve command)

Key design decisions:
- Expertise file is a mental model, NOT source of truth
- Always cross-reference expertise claims with actual code
- Flag discrepancies for future self-improvement
- Provide file paths with line numbers for all evidence

## How to Use

1. **Ask a question about the CLI**:
   ```bash
   /experts/cli/question "How does template registration work in scaffold_service?"
   ```

2. **The command will**:
   - Read `.claude/commands/experts/cli/expertise.yaml` for mental model
   - Validate claims against actual code in `tac_bootstrap_cli/tac_bootstrap/`
   - Report findings with file references and line numbers
   - Flag any discrepancies between expertise and code

3. **Receive structured answer**:
   - Direct answer to your question
   - Evidence from code (file paths + line numbers)
   - Expertise validation notes
   - Discrepancies or gaps identified

## Configuration

### YAML Frontmatter
```yaml
allowed-tools: Bash, Read, Grep, Glob, TodoWrite
description: Answer questions about {{ config.project.name }} CLI without coding
argument-hint: [question]
model: sonnet
```

### Variables
- **USER_QUESTION**: `$1` (required) - The question to answer
- **EXPERTISE_PATH**: `.claude/commands/experts/cli/expertise.yaml` (static)
- **CLI_ROOT**: `{{ config.project.name }}/` (template) or `tac_bootstrap_cli/tac_bootstrap/` (implementation)

### Jinja2 Template Variables
- `{{ config.project.name }}`: Project name used throughout prompt

## Testing

Verify template file exists and has valid Jinja2 syntax:
```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2 && echo "✓ Template exists"
```

Verify implementation file exists:
```bash
test -f .claude/commands/experts/cli/question.md && echo "✓ Implementation exists"
```

Check YAML frontmatter is valid:
```bash
head -20 .claude/commands/experts/cli/question.md | grep -A 10 "^---$" | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)" && echo "✓ YAML valid"
```

Verify template registration in scaffold_service.py:
```bash
grep -q "experts/cli/question.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"
```

Run unit tests:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting:
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Run type checking:
```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

Smoke test CLI:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Workflow Philosophy
Generic agents forget everything between executions and must re-explore codebases every time, wasting context and time. The CLI expert solves this by:
- Accumulating expertise (mental model) from previous work
- Validating expertise against actual code (source of truth)
- Providing fast, accurate answers with file references
- Flagging when mental model diverges from code (for self-improvement)

### Future Integration
This question prompt will be used by:
- Developers exploring the CLI structure
- Other expert commands (self-improve, build workflows)
- Meta-agentic commands (expert orchestrator)

### Related Tasks
- Task 3: Directory structure (prerequisite - completed)
- Task 5: CLI self-improve prompt (next task)
- Task 6: CLI expertise seed file (final CLI expert task)
- Tasks 7-9: ADW expert (parallel pattern)
- Tasks 10-12: Commands expert (parallel pattern)

### Design Principles
1. **Start with expertise (mental model)** - Leverage accumulated knowledge first
2. **Validate against actual code (source of truth)** - Never trust mental model blindly
3. **Report with evidence (file references + line numbers)** - All claims must be backed by code
4. **Never guess - if unsure, read the code** - Accuracy over speed
