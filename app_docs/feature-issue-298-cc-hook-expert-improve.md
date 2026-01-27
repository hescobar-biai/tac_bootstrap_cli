---
doc_type: feature
adw_id: feature_Tac_9_task_31
date: 2026-01-26
idk:
  - expert-command
  - jinja2-template
  - continuous-learning
  - git-analysis
  - hook-development
  - self-improvement
  - expertise-update
tags:
  - feature
  - expert-workflow
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2
  - .claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md
---

# CC Hook Expert Improve Template

**ADW ID:** feature_Tac_9_task_31
**Date:** 2026-01-26
**Specification:** specs/issue-298-adw-feature_Tac_9_task_31-sdlc_planner-cc-hook-expert-improve-template.md

## Overview

This feature adds the third and final step in the Plan-Build-Improve expert workflow cycle for Claude Code hook development. The `cc_hook_expert_improve` command template enables AI agents to perform continuous learning by analyzing recent hook-related changes, extracting patterns and best practices, and selectively updating expert knowledge in plan and build commands while maintaining workflow stability.

## What Was Built

- **Jinja2 Template**: Created `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` with 292 lines of expert guidance
- **Rendered Command**: Generated `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` in this repository as a working example
- **Complete Expert Cycle**: Closed the Plan → Build → Improve workflow loop for hook development
- **Self-Improvement Capability**: Agents can now analyze their own work and update expert knowledge automatically

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2` (CREATE): Jinja2 template with minimal variables (only `{{ config.project.name }}`)
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` (CREATE): Rendered version for TAC Bootstrap repository
- `specs/issue-298-adw-feature_Tac_9_task_31-sdlc_planner-cc-hook-expert-improve-template.md` (CREATE): Implementation specification
- `specs/issue-298-adw-feature_Tac_9_task_31-sdlc_planner-cc-hook-expert-improve-template-checklist.md` (CREATE): Acceptance criteria checklist

### Key Changes

1. **Five-Phase Workflow**: Structured expert guidance through Establish Expertise → Analyze Changes → Determine Relevance → Extract & Apply Learnings → Report phases
2. **Early Exit Logic**: Critical decision point in Phase 3 to stop processing if no relevant learnings are found, avoiding wasted effort
3. **Selective Updates**: Only modifies `## Expertise` sections of plan/build commands, never touching `## Workflow` or `## Instructions` to preserve stability
4. **Git-Based Analysis**: Uses `git diff`, `git diff --cached`, and `git log` commands to review uncommitted changes, staged changes, and recent commits
5. **Minimal Templating**: Uses only one Jinja2 variable (`{{ config.project.name }}`), keeping most expert content as static guidance
6. **Self-Contained Expertise**: Includes its own expertise section with guidance on when to improve, relevance criteria, update best practices, and git analysis techniques

## How to Use

### Basic Usage

```bash
/cc_hook_expert_improve
```

No arguments required - the command automatically analyzes recent git history.

### Workflow Context

This command completes the expert workflow cycle:

1. **Plan**: `/cc_hook_expert_plan` - Design hook implementation approach
2. **Build**: `/cc_hook_expert_build` - Execute the planned implementation
3. **Improve**: `/cc_hook_expert_improve` - Analyze work and update expert knowledge

### When to Use

- After completing hook implementation with `/cc_hook_expert_build`
- When you've made changes to hooks and want to capture learnings
- To update expert knowledge with discovered patterns and best practices
- As part of regular expert workflow maintenance

### What Happens

The agent will:
1. Read foundational hook documentation (uv-scripts, hooks architecture, slash commands)
2. Review git changes to identify hook-related modifications
3. Determine if changes contain new expertise worth capturing (early exit if not)
4. Extract learnings and categorize by planning vs building knowledge
5. Update ONLY the `## Expertise` sections of plan and build expert commands
6. Report what was analyzed and what updates were made

## Configuration

### YAML Frontmatter

```yaml
allowed-tools: Read, Edit, Bash, Grep, Glob
description: Review hook changes and update expert knowledge with improvements
model: sonnet
```

### Jinja2 Variables

Only one variable is used:
- `{{ config.project.name }}`: Project name for context (e.g., "tac_bootstrap")

### Hook-Related Files Analyzed

- `.claude/hooks/*.py` - Hook implementations
- `.claude/settings*.json` - Hook configurations
- `specs/experts/cc_hook_expert/*.md` - Hook specifications
- `specs/hook-*.md` - Hook implementation plans
- `ai_docs/*hooks*.md` - Hook documentation updates

## Testing

### Validate Template Rendering

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Run All Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Check Code Quality

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Manual Test: Review Rendered Command

```bash
cat .claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md
```

Verify:
- YAML frontmatter is valid
- Project name is correctly substituted
- All 5 phases are present
- Early exit logic is clear
- Expertise section is comprehensive

### Integration Test: Complete Expert Cycle

Test the full Plan → Build → Improve workflow:

```bash
# 1. Plan a new hook
/cc_hook_expert_plan

# 2. Build the hook
/cc_hook_expert_build

# 3. Improve expert knowledge
/cc_hook_expert_improve
```

Verify the improve command can:
- Read plan and build expert commands
- Analyze git changes
- Determine relevance correctly
- Update expertise sections without modifying workflows

## Notes

### Design Decisions

1. **Early Exit Logic**: The improve command must determine relevance early (Phase 3) and stop if no learnings are found to avoid wasted work and unnecessary file modifications.

2. **Selective Updates**: Only update `## Expertise` sections, never `## Workflow` sections, to maintain workflow stability. This ensures proven processes remain consistent while knowledge evolves.

3. **No Required Arguments**: Command analyzes recent work automatically via git, no user input needed. This enables frictionless continuous improvement.

4. **Git-Based Analysis**: Uses multiple git commands (`git diff`, `git diff --cached`, `git log`) to comprehensively review uncommitted changes, staged changes, and recent commits.

5. **Self-Referential**: This command updates other expert commands but includes its own expertise section about the improvement process itself.

6. **Minimal Templating**: Uses only one Jinja2 variable to keep the template simple and most expert guidance static.

### Workflow Closure

This feature completes the Plan-Build-Improve expert workflow cycle:
- **Plan** (cc_hook_expert_plan): Design the hook implementation approach
- **Build** (cc_hook_expert_build): Execute the planned implementation
- **Improve** (cc_hook_expert_improve): Analyze work and update expert knowledge

The improve phase creates a feedback loop that continuously enhances expert commands based on real-world usage patterns and discoveries, ensuring expertise remains current and valuable.

### Expertise Sections Included

The command includes comprehensive expertise guidance on:
- **When to Improve Expert Knowledge**: Trigger conditions and when NOT to improve
- **Criteria for Determining Relevance**: High relevance vs low relevance changes
- **Best Practices for Updating Expertise**: Selective updates, clear attribution, stability, quality
- **Git Analysis Techniques**: Effective commands and pattern identification methods

### Future Enhancements

- Could add metrics tracking (how many learnings captured over time)
- Could support analyzing specific commit ranges via arguments
- Could add ability to update other expert command sections beyond expertise
- Could integrate with CI/CD to auto-improve after successful hooks
