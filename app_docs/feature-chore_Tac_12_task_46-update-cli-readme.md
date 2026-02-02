---
doc_type: feature
adw_id: chore_Tac_12_task_46
date: 2026-02-02
idk:
  - TAC-12 documentation
  - CLI README updates
  - Multi-agent orchestration
  - Hook system categorization
  - Observability infrastructure
  - Command reference tables
tags:
  - chore
  - documentation
  - cli
related_code:
  - tac_bootstrap_cli/README.md
  - docs/hooks.md
  - docs/utilities.md
  - docs/commands.md
---

# TAC Bootstrap CLI README Updates for TAC-12 Features

**ADW ID:** chore_Tac_12_task_46
**Date:** 2026-02-02
**Specification:** specs/issue-498-adw-chore_Tac_12_task_46-update-cli-readme.md

## Overview

Updated the TAC Bootstrap CLI README.md to document TAC-12 multi-agent orchestration features and improvements. This chore involved expanding documentation sections to highlight new capabilities for parallel subagent execution, observability infrastructure, and hook system enhancements introduced in TAC-12.

## What Was Built

- **TAC-12 Multi-Agent Orchestration Section**: New section documenting parallel subagent execution patterns and commands
- **Expanded Hooks Section**: Categorized hooks into Core, Security, and TAC-12-specific groups
- **Observability Section**: New comprehensive section covering hooks, status line integration, and logging infrastructure
- **Updated Command References**: Added TAC-12-specific commands (`parallel_subagents`, `scout_plan_build`, `implement` with enhancements)
- **Cross-Reference Documentation**: Maintained links to detailed documentation (hooks.md, utilities.md, commands.md)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/README.md`: Updated with new sections and command references

### Key Changes

- Added new section "TAC-12 Multi-Agent Orchestration" after "ADW Workflows" section
- Expanded "Hooks" section to categorize all 9 hooks into: Core hooks, Security hooks, TAC-12 Additional hooks
- Created new "Observability" section covering:
  - Hook system with category breakdown
  - Status line integration overview
  - Logging infrastructure summary
- Updated command reference tables to highlight TAC-12-specific commands:
  - `parallel_subagents` - Multi-agent parallel execution
  - `scout_plan_build` - Orchestrated scout-plan-build workflow
  - `implement` - Plan implementation with TAC-12 improvements
- Maintained backward compatibility with existing documentation structure

## How to Use

### Viewing the Documentation

1. Navigate to the TAC Bootstrap CLI directory:
   ```bash
   cd tac_bootstrap_cli
   ```

2. Open README.md to see the updated sections:
   ```bash
   cat README.md
   ```

3. Cross-reference with detailed documentation:
   - For complete command reference: `docs/commands.md`
   - For hook system details: `docs/hooks.md`
   - For observability utilities: `docs/utilities.md`

### TAC-12 Multi-Agent Orchestration Commands

Execute parallel subagent workflows:

```bash
# Execute parallel subagents without arguments (interactive mode)
/parallel_subagents

# Execute parallel subagents with specific agents
/parallel_subagents agent1,agent2,agent3
```

Use orchestrated workflow:

```bash
# Run scout-plan-build workflow
/scout_plan_build "<task description>"

# Implement a plan
/implement "<plan content>"
```

## Configuration

No additional configuration required. TAC-12 features are integrated into the standard CLI configuration via `config.yml`:

```yaml
agentic:
  provider: "claude_code"
  model_policy:
    default: "sonnet"
    heavy: "opus"
```

## Testing

Verify the README documentation is complete and properly formatted:

```bash
# Check markdown formatting
cd tac_bootstrap_cli && cat README.md | head -50

# Verify links to referenced documentation files
ls docs/hooks.md docs/utilities.md docs/commands.md
```

Test that command references are accurate:

```bash
# List available commands
tac-bootstrap --help

# View slash commands in settings
cat .claude/commands/
```

## Notes

- The TAC-12 features documented represent stable, released functionality
- README serves as a quick-reference guide with cross-references to detailed docs
- Maintains backward compatibility - existing sections remain unchanged
- Hook system now clearly distinguishes between core, security, and TAC-12 additional hooks
- Observability section provides entry point for users interested in system monitoring and logging
