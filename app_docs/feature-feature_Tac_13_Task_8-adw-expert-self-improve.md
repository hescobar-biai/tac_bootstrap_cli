---
doc_type: feature
adw_id: feature_Tac_13_Task_8
date: 2026-02-03
idk:
  - adw-expert
  - self-improve-workflow
  - expertise-validation
  - mental-model
  - yaml-validation
  - line-limit-enforcement
  - codebase-validation
tags:
  - feature
  - adw
  - expert-system
related_code:
  - .claude/commands/experts/adw/self-improve.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# ADW Expert Self-Improve Workflow

**ADW ID:** feature_Tac_13_Task_8
**Date:** 2026-02-03
**Specification:** specs/issue-570-adw-feature_Tac_13_Task_8-sdlc_planner-adw-self-improve-prompt.md

## Overview

This feature implements a self-improvement workflow for the ADW (AI Developer Workflow) expert agent, enabling it to validate and update its mental model (expertise.yaml) by comparing it against the actual codebase. This is the "Learn" step in the Act → Learn → Reuse cycle, implementing a 7-phase validation workflow following the TAC-13 expert system pattern.

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2` - Reusable template for CLI generation
- **Implementation File**: `.claude/commands/experts/adw/self-improve.md` - Working ADW expert self-improve prompt
- **Scaffold Registration**: Updated `scaffold_service.py` to include the template in automatic project scaffolding
- **7-Phase Workflow**: Complete workflow covering git diff analysis, expertise reading, codebase validation, discrepancy identification, expertise updates, line limit enforcement, and YAML validation

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2`: New Jinja2 template (511 lines) - Template for generating self-improve prompts in generated projects
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added registration for ADW expert self-improve template (2 lines changed)
- `.claude/commands/experts/adw/self-improve.md`: New implementation (511 lines) - Working self-improve prompt for this repository

### Key Changes

1. **7-Phase Workflow Structure**: Implemented TAC-13 standard self-improve workflow with phases for git diff checking, expertise reading, codebase validation, discrepancy identification, expertise updating, line limit enforcement, and YAML validation

2. **ADW-Specific Focus Areas**: Tailored validation to ADW domain including:
   - State management patterns (adw_modules/state.py)
   - GitHub integration (adw_modules/github.py, git_ops.py)
   - Workflow orchestration (adw_modules/workflow_ops.py, tool_sequencer.py)
   - Worktree operations (adw_modules/worktree_ops.py)
   - Isolation patterns (adw_*_iso.py workflows)

3. **Compression Strategies**: Built-in line limit enforcement (1000 lines max) with intelligent compression strategies:
   - Remove old recent_changes entries
   - Consolidate similar patterns
   - Use line ranges instead of detailed method listings
   - Remove self-evident information

4. **YAML Validation**: Automated YAML syntax validation with Python-based checks

## How to Use

### Basic Usage

Run the self-improve command from the project root:

```bash
/experts:adw:self-improve
```

### With Git Diff Analysis

To focus on recently changed ADW files:

```bash
/experts:adw:self-improve true
```

### With Focus Area

To concentrate on specific domain area:

```bash
/experts:adw:self-improve false state_management
```

Or with git diff and focus area:

```bash
/experts:adw:self-improve true github_integration
```

### Focus Areas

Available focus areas for targeted validation:
- `state_management`: State persistence patterns in state.py
- `github_integration`: GitHub API and git operations
- `workflow_orchestration`: Workflow coordination and tool sequencing
- `worktree_operations`: Git worktree management patterns

## Configuration

### Variables

The self-improve workflow uses these variables:

- **CHECK_GIT_DIFF**: `$1` (default: `false`) - Analyze recent changes
- **FOCUS_AREA**: `$2` (default: empty) - Target specific domain
- **EXPERTISE_FILE**: `.claude/commands/experts/adw/expertise.yaml` (static)
- **ADW_ROOT**: `adws/` (static)
- **ADW_MODULES**: `adws/adw_modules/` (static)
- **MAX_LINES**: `1000` (static)

### Allowed Tools

The workflow has access to: Read, Grep, Glob, Bash, Edit, Write, TodoWrite

### Model

Uses Claude Sonnet model for expertise updates

## Testing

### Validate Template and Registration

Check that template file exists and is registered:

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo "✓ Template exists"
```

```bash
grep "experts/adw/self-improve.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered in scaffold service"
```

### Validate Implementation File

Check implementation file structure:

```bash
test -f .claude/commands/experts/adw/self-improve.md && echo "✓ Implementation exists"
```

Verify frontmatter and required keys:

```bash
grep -E "^(allowed-tools|description|argument-hint|model):" .claude/commands/experts/adw/self-improve.md
```

Count phases (should be 7):

```bash
grep -c "^### Phase" .claude/commands/experts/adw/self-improve.md
```

### Validate Variables and Focus Areas

Check that key variables are defined:

```bash
grep -E "CHECK_GIT_DIFF.*\$1" .claude/commands/experts/adw/self-improve.md && echo "✓ CHECK_GIT_DIFF variable"
grep -E "FOCUS_AREA.*\$2" .claude/commands/experts/adw/self-improve.md && echo "✓ FOCUS_AREA variable"
grep -E "MAX_LINES.*1000" .claude/commands/experts/adw/self-improve.md && echo "✓ MAX_LINES constraint"
```

Verify ADW-specific focus areas are documented:

```bash
grep -i "state management" .claude/commands/experts/adw/self-improve.md && echo "✓ State management focus area"
grep -i "github integration" .claude/commands/experts/adw/self-improve.md && echo "✓ GitHub integration focus area"
grep -i "workflow orchestration" .claude/commands/experts/adw/self-improve.md && echo "✓ Workflow orchestration focus area"
```

### CLI Smoke Test

Verify CLI still works after changes:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### ADW Domain Expertise

The self-improve workflow is specifically designed for ADW domain knowledge, focusing on:

1. **State Management**: How ADW persists workflow state across executions (adw_modules/state.py)
2. **GitHub Integration**: API patterns, authentication, and GitHub operations (adw_modules/github.py, git_ops.py)
3. **Workflow Orchestration**: How isolated workflows coordinate and sequence tools (adw_modules/workflow_ops.py, tool_sequencer.py)
4. **Worktree Operations**: Complex git worktree patterns for isolation (adw_modules/worktree_ops.py)
5. **Isolation Patterns**: How ADW workflows maintain process isolation (adw_*_iso.py files)

### Workflow Design Principles

- **Expertise as Mental Model**: The expertise file is NOT source of truth, but a curated mental model for the agent
- **Focus on High-Value Knowledge**: Document patterns, relationships, and non-obvious knowledge
- **Line Limit Discipline**: Keep under 1000 lines through intelligent compression
- **YAML Validation**: Always validate syntax before completing updates
- **Systematic Validation**: Check every claim in expertise against actual codebase

### Compression Strategies

When expertise exceeds 1000 lines, the workflow applies:
1. Remove old recent_changes entries (keep latest 3-5)
2. Consolidate similar workflow patterns
3. Use line ranges instead of detailed method listings
4. Remove self-evident information, focus on non-obvious patterns

### Integration with TAC-13

This feature completes the TAC-13 expert system pattern by providing:
- **Act**: `/experts:adw:question` - Answer questions using expertise
- **Learn**: `/experts:adw:self-improve` - Update expertise from codebase (THIS FEATURE)
- **Reuse**: Expertise.yaml serves as persistent mental model across sessions

### Future Considerations

- Consider seeding expertise.yaml with initial ADW domain knowledge (potential Task 9)
- Explore automated self-improve triggers (e.g., after significant ADW changes)
- Document ADW expert usage patterns in fractal documentation
- Track expertise evolution over time with metrics
