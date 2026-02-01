---
doc_type: feature
adw_id: feature_Tac_12_task_38
date: 2026-02-01
idk:
  - scout-based-planning
  - parallel-agent-coordination
  - codebase-exploration
  - task-type-determination
  - conditional-planning
  - TAC-12-implementation
  - plan-generation
tags:
  - feature
  - commands
  - planning
  - scouts
related_code:
  - .claude/commands/quick-plan.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2
  - ai_docs/doc/plan_tasks_Tac_12_v2_UPDATED.md
  - ai_docs/doc/plan_tasks_Tac_12_v3_FINAL.md
---

# Quick-Plan: Scout-Based Planning Command

**ADW ID:** feature_Tac_12_task_38
**Date:** 2026-02-01
**Specification:** specs/issue-490-adw-feature_Tac_12_task_38-sdlc_planner-quick-plan-tac12.md

## Overview

Updated the `/quick-plan` command to implement complete TAC-12 improvements featuring parallel scout-based codebase exploration. The enhanced command deploys 3 base scout agents and 5 fast scout agents in parallel to discover relevant files and architectural patterns before generating implementation plans. It also implements intelligent task type and complexity determination with conditional plan formatting, expanding the command from 48 lines to approximately 250+ lines of sophisticated planning logic.

## What Was Built

- **Scout-Based Codebase Exploration**: Parallel execution of 8 agents (3 base scouts + 5 fast scouts) for divide-and-conquer codebase exploration
- **Task Type Determination**: Automatic classification of tasks as chore, feature, refactor, fix, or enhancement
- **Complexity Estimation**: Classification of work complexity as simple, medium, or complex based on file scope
- **Conditional Plan Sections**: Dynamic inclusion of plan sections (Problem Statement, Solution Approach, Implementation Phases, Testing Strategy) based on task characteristics
- **File Discovery & Scoring**: High-confidence file identification through scout consensus (2+ scout mentions)
- **Architectural Pattern Extraction**: Discovery and recommendation of existing patterns and design decisions
- **Scout Exploration Workflow**: Comprehensive multi-step process for parallel exploration and result aggregation

## Technical Implementation

### Files Modified

- `.claude/commands/quick-plan.md`: Base command file updated from 48 to 213+ lines
  - Added Task tool to allowed-tools (enables scout execution)
  - Expanded Variables section with scout configuration counts
  - Rewrote Instructions section with 6 major steps
  - Added Scout Exploration Workflow subsection with detailed steps
  - Added Task Type & Complexity Determination logic
  - Added Conditional Plan Format specification
  - Enhanced plan structure with scout-informed sections

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/quick-plan.md.j2`: Template synchronized with base file
  - Mirrored all changes from base file for template consistency
  - Maintains identical structure for generated projects

### Key Changes

- **Parallel Scout Architecture**: Replaced sequential exploration with 8 parallel scout agents (3 base, 5 fast) for efficient codebase discovery
- **Task Intelligence**: Added classification logic to determine task type and complexity before planning
- **Conditional Formatting**: Plan output now dynamically includes sections based on task characteristics:
  - Always: Feature Description, User Story, Relevant Files, Implementation Plan
  - If feature OR complex: Problem Statement, Solution Approach, Testing Strategy
  - If complex: Implementation Phases
- **Scout Configuration**: Added variables TOTAL_BASE_SCOUT_SUBAGENTS (3) and TOTAL_FAST_SCOUT_SUBAGENTS (5)
- **Graceful Degradation**: Plan continues even if individual scouts fail; failures logged in Notes section

## How to Use

### Basic Usage

```bash
/quick-plan Your task description here
```

The command will:

1. Parse your task description
2. Deploy 3 base scouts + 5 fast scouts in parallel to explore the codebase
3. Analyze task type (feature, chore, refactor, fix, enhancement) and complexity (simple, medium, complex)
4. Generate a plan with adaptive sections based on task characteristics
5. Reference discovered files and architectural patterns throughout the plan

### Scout Exploration

The command automatically executes:

**Base Scouts (3 agents, medium thoroughness):**
- Scout 1: Domain models, service layers, core abstractions, design patterns
- Scout 2: Infrastructure, integrations, CLI interfaces, templates, file operations
- Scout 3: Service orchestration, workflows, application patterns, extension mechanisms

**Fast Scouts (5 agents, quick thoroughness):**
- Scout 1: File naming patterns and test files
- Scout 2: Configuration and setup patterns
- Scout 3: Similar feature implementations
- Scout 4: Documentation and examples
- Scout 5: Integration points and extension mechanisms

### Task Type Classification

The command determines task type:
- **chore**: Simple housekeeping tasks (dependency updates, minor fixes)
- **feature**: New functionality requiring planning and testing
- **refactor**: Structural improvements with impact analysis
- **fix**: Bug fixes with investigation and testing
- **enhancement**: Improvements to existing features

### Complexity Determination

Work is classified by scope:
- **simple**: Changes to 1-2 files
- **medium**: Changes to 3-5 files
- **complex**: Changes to 5+ files with architectural impact

## Configuration

### Variables Available

```yaml
USER_PROMPT: $ARGUMENTS                    # Your task description
PLAN_OUTPUT_DIRECTORY: specs/              # Where plans are saved
TOTAL_BASE_SCOUT_SUBAGENTS: 3              # Base scout agent count
TOTAL_FAST_SCOUT_SUBAGENTS: 5              # Fast scout agent count
```

### Allowed Tools

The command has access to:
- Task (for launching parallel scouts)
- Read, Write, Edit (for file operations)
- Glob, Grep (for codebase searching)
- WebFetch (for external research)

## Testing

### Test Scout Coordination

```bash
/quick-plan Implement a new service layer for user authentication
```

Verify that:
- All 8 scouts launch in parallel (check logs for concurrent execution)
- Scout results are aggregated into the plan
- High-confidence files (found by 2+ scouts) are highlighted

### Test Task Type Detection

```bash
/quick-plan Update dependencies to latest versions
```

Should detect as **chore** and minimize plan sections.

```bash
/quick-plan Add OAuth2 support to the application
```

Should detect as **feature** and include Problem Statement, Solution Approach, Testing Strategy.

### Test Complexity Determination

```bash
/quick-plan Rename getUserId to getCurrentUserId across project
```

Should estimate **simple** complexity if affecting 1-2 files.

```bash
/quick-plan Refactor authentication layer to support multiple strategies
```

Should estimate **complex** and include Implementation Phases.

### Test Conditional Sections

Verify that plan output varies based on classification:
- **Simple task**: Minimal sections
- **Medium task**: Extended sections for features
- **Complex task**: Full planning sections including Implementation Phases

## Notes

### Positioning

Quick-plan serves as a "lean scout-based planning" command:
- Simpler than `plan_w_scouters` (477 lines, 3 base scouts only)
- More powerful than legacy `feature` command (basic planning without exploration)
- Balanced for most development tasks (250+ lines, 8 parallel scouts)

### Scout Consensus Algorithm

Files are scored by discovery frequency:
- **High confidence** (66%+): Found by 2+ scouts → Definitely relevant
- Unified file map built with frequency counts
- Architectural patterns extracted from multiple sources

### Graceful Failure Handling

If scouts fail:
- Plan continues with results from successful scouts
- Failures logged in plan Notes section
- General knowledge applied for missing exploration
- Plan is never blocked by individual scout failures

### Wave 6 Integration

This task (38/49) is part of Wave 6: Robustify Existing Commands. It upgrades the quick-plan command with TAC-12 improvements. Task 39 will register `/quick-plan` in the CLI's data_types.py SlashCommand Literal.

### Related Commands

- `/scout` - General codebase exploration (tool)
- `/plan_w_scouters` - Comprehensive planning (477 lines, 3 base scouts)
- `/quick-plan` - Lean planning (250+ lines, 8 parallel scouts) **NEW**
- `/feature` - Basic planning without scouts (legacy)
- `/plan_w_docs` - Planning with documentation exploration

### Dependencies

- **Prerequisite**: Scout agents (scout-report-suggest, scout-report-suggest-fast) created in earlier tasks
- **Next Task**: Task 39 registers command in data_types.py
- **Reference**: plan_w_scouters.md pattern (simpler version for quick-plan)
