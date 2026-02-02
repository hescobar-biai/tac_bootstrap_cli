---
doc_type: feature
adw_id: chore_Tac_12_task_43
date: 2026-02-02
idk:
  - cli-commands
  - documentation
  - planning-workflows
  - implementation-strategies
  - agent-delegation
  - test-automation
  - context-management
tags:
  - feature
  - cli
  - documentation
  - workflow
related_code:
  - tac_bootstrap_cli/docs/commands.md
  - .claude/commands/plan.md
  - .claude/commands/plan_w_docs.md
  - .claude/commands/plan_w_scouters.md
  - .claude/commands/quick-plan.md
  - .claude/commands/build_in_parallel.md
  - .claude/commands/build_w_report.md
  - .claude/commands/scout_plan_build.md
  - .claude/commands/find_and_summarize.md
  - .claude/commands/all_tools.md
  - .claude/commands/prime_3.md
  - .claude/commands/resolve_failed_test.md
  - .claude/commands/resolve_failed_e2e_test.md
  - .claude/commands/track_agentic_kpis.md
---

# CLI Commands Documentation Update

**ADW ID:** chore_Tac_12_task_43
**Date:** 2026-02-02
**Specification:** issue-495-adw-chore_Tac_12_task_43-update-cli-commands-documentation.md

## Overview

Updated comprehensive CLI commands documentation in `tac_bootstrap_cli/docs/commands.md` to include 13 new TAC-12 commands. These commands represent enhancements to planning, implementation, agent delegation, and test automation workflows, organized into existing functional categories with tool references and practical examples.

## What Was Built

Integrated 13 new slash commands into existing documentation structure:

**Planning Commands**
- `/plan` - Basic planning without exploration (legacy variant)
- `/plan_w_docs` - Planning with documentation exploration
- `/plan_w_scouters` - Planning with parallel scout-based exploration
- `/quick-plan` - Rapid planning with architect pattern (enhanced existing)

**Implementation Commands**
- `/build_in_parallel` - Parallel file creation delegation to build-agents
- `/build_w_report` - Implement with detailed YAML change report (enhanced existing)

**Agent Delegation Commands**
- `/scout_plan_build` - End-to-end scout-plan-build orchestration

**Context Management Commands**
- `/all_tools` - Comprehensive tool reference
- `/prime_3` - Deep context loading (3-level exploration)

**Documentation Commands**
- `/find_and_summarize` - Lightweight file discovery with AI summarization

**Test Commands**
- `/resolve_failed_test` - Analyze and fix failing unit tests
- `/resolve_failed_e2e_test` - Analyze and fix failing E2E tests
- `/track_agentic_kpis` - Track agentic development KPIs

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/docs/commands.md` - Added 13 new commands with examples, tools, and detailed sections
  - Added Tools column to all command tables for transparency on available capabilities
  - Integrated commands by functional category (Planning, Implementation, Delegation, Context, Documentation, Tests)
  - Added detailed subsections with usage examples and workflows for each new command
  - Maintained consistent markdown formatting and visual hierarchy

### Key Changes

- **Planning Section**: Added `/plan`, `/plan_w_docs`, `/plan_w_scouters` variants showing planning evolution from basic to comprehensive exploration patterns
- **Implementation Section**: Added `/build_in_parallel` for parallel delegation and enhanced `/build_w_report` with complete YAML structure examples
- **Agent Delegation**: Added `/scout_plan_build` as capstone orchestration command showing 3-phase workflow
- **Context Management**: Added `/prime_3` for deep context loading and `/all_tools` for comprehensive tool reference
- **Documentation**: Added `/find_and_summarize` for lightweight pattern-based file discovery
- **Test Commands**: Added three test automation commands with JSON parameter examples and detailed workflows
- **Tools Column**: All command tables now include Tools column showing which built-in tools each command uses

## How to Use

### Viewing Commands

The documentation is organized by functional category in `tac_bootstrap_cli/docs/commands.md`:

1. Planning Commands - Choose plan variant based on exploration needs
2. Implementation Commands - Select implementation strategy (sequential, parallel, with reporting)
3. Documentation Commands - Find and explore codebase efficiently
4. Context Management - Prepare environment with appropriate context depth
5. Agent Delegation - Orchestrate multi-phase workflows
6. Test Commands - Analyze and resolve test failures

### Finding Specific Commands

Quick reference for command categories:
- Want to **plan implementation**? See Planning Commands: `/plan`, `/plan_w_docs`, `/plan_w_scouters`, `/quick-plan`
- Want to **implement code**? See Implementation Commands: `/implement`, `/build_in_parallel`, `/build_w_report`
- Want to **manage context**? See Context Management: `/prime_cc`, `/prime_3`, `/all_tools`
- Want to **fix tests**? See Test Commands: `/resolve_failed_test`, `/resolve_failed_e2e_test`, `/track_agentic_kpis`

### Using Tools Column

Each command table includes Tools column showing:
- Core tools available to the command
- Tool categories like (core tools), (git tools), (documentation agent)
- Specific tools like Read, Write, Edit, Bash, Task

## Configuration

Commands are documented as stable and production-ready with:
- Consistent argument notation (required vs optional parameters in square brackets)
- Tool requirements listed in tables
- Usage examples showing typical invocations
- Output format descriptions for commands with structured results

## Testing

Validate command documentation consistency:

```bash
# Count documented commands (should show all command tables)
grep -c "^| \`/" tac_bootstrap_cli/docs/commands.md

# Verify all 13 new commands appear in documentation
grep -E "^\`/(plan|plan_w_docs|plan_w_scouters|quick-plan|build_in_parallel|build_w_report|scout_plan_build|find_and_summarize|all_tools|prime_3|resolve_failed_test|resolve_failed_e2e_test|track_agentic_kpis)\`" tac_bootstrap_cli/docs/commands.md | wc -l

# Check markdown table integrity (verify no broken formatting)
grep "^|" tac_bootstrap_cli/docs/commands.md | wc -l
```

## Notes

### Documentation Approach

- Commands organized by functional category, not by recency
- Tool requirements documented transparently in tables
- Examples are concise (1-2 lines) showing typical usage
- Detailed command specifications linked in command definition files (`.claude/commands/`)
- Consistent formatting for easy navigation and reference

### Organizational Benefits

- **Planning variants** show evolution from basic to comprehensive exploration
- **Build strategies** display different implementation approaches (sequential, parallel, with reporting)
- **Agent delegation** demonstrates orchestration patterns from single scout to multi-phase workflows
- **Context tools** provide progressive context loading options (prime_cc → prime_3)
- **Test utilities** organize by analysis depth and scope

### Integration Pattern

All new commands integrated into existing sections:
- No new section types created
- Maintained backward compatibility with existing documentation
- Consistent table format with added Tools column
- Examples extracted from command definition files
- No raw frontmatter exposed in user-facing documentation

