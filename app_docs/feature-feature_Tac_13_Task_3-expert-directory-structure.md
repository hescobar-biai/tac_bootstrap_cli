---
doc_type: feature
adw_id: feature_Tac_13_Task_3
date: 2026-02-02
idk:
  - agent-experts
  - directory-structure
  - dual-strategy
  - cli-templates
  - gitkeep
  - tac-13
tags:
  - feature
  - infrastructure
related_code:
  - .claude/commands/experts/cli/.gitkeep
  - .claude/commands/experts/adw/.gitkeep
  - .claude/commands/experts/commands/.gitkeep
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/.gitkeep
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/.gitkeep
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/.gitkeep
---

# Agent Experts Directory Structure

**ADW ID:** feature_Tac_13_Task_3
**Date:** 2026-02-02
**Specification:** specs/issue-565-adw-feature_Tac_13_Task_3-sdlc_planner-expert-directory-structure.md

## Overview

This feature implements the foundational directory structure for TAC-13 Agent Experts, creating a three-tier organizational framework for domain-specific agent experts (CLI, ADW, and Commands) in both the CLI template system and repository root. This dual-location strategy enables local testing of expert patterns before they're templated into generated projects.

## What Was Built

- **CLI Template Expert Directories**: Three empty directories with .gitkeep files in the CLI template structure for scaffolding into generated projects
- **Repo Root Expert Directories**: Mirror directories in repository root for local testing and validation
- **Three Domain-Specific Experts**: Organizational structure for cli, adw, and commands expert domains
- **Git Tracking Infrastructure**: .gitkeep files ensuring Git recognizes empty directory structures

## Technical Implementation

### Files Modified

- `.claude/commands/experts/cli/.gitkeep`: Created - placeholder for CLI expert files (question.md, self-improve.md, expertise.yaml)
- `.claude/commands/experts/adw/.gitkeep`: Created - placeholder for ADW expert files
- `.claude/commands/experts/commands/.gitkeep`: Created - placeholder for Commands expert files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/.gitkeep`: Created - CLI template version for generated projects
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/.gitkeep`: Created - CLI template version for generated projects
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/.gitkeep`: Created - CLI template version for generated projects

### Key Changes

- **Three-Tier Expert Structure**: Established directories for cli (tac_bootstrap generator patterns), adw (workflow patterns), and commands (slash command patterns)
- **Dual Strategy Pattern**: Synchronized directory structures in both CLI templates and repo root for testing before templating
- **Git Tracking with .gitkeep**: Used empty .gitkeep files to ensure Git tracks the directory structure despite having no content files yet
- **Pattern Consistency**: Mirrored existing cc_hook_expert/ structure demonstrating proven expert organization pattern
- **TAC-13 Foundation**: Prepared infrastructure for Tasks 4-12 which will implement the actual expert files (question prompts, self-improve workflows, expertise YAML files)

## How to Use

This is infrastructure - end users won't directly interact with these directories. They provide the organizational framework for:

1. **Future Expert Implementations** (Tasks 4-12 in TAC-13):
   - CLI Expert files will go in `experts/cli/`
   - ADW Expert files will go in `experts/adw/`
   - Commands Expert files will go in `experts/commands/`

2. **Local Testing** (developers):
   - Add expert files to `.claude/commands/experts/{domain}/` for testing
   - Validate expert patterns work correctly before templating

3. **Generated Projects** (CLI users):
   - Running `tac-bootstrap generate` will scaffold these directories with expert files
   - Expert directories will be auto-populated from CLI templates

## Configuration

No configuration required. The directories are part of the project structure and automatically included in:
- Git version control (via .gitkeep files)
- CLI template scaffolding system (scaffold_service.py will auto-include when expert files are added in Tasks 4-12)

## Testing

Verify the directory structure was created correctly:

```bash
# Verify CLI template structure
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/
```

Expected output: Each directory should show a .gitkeep file.

```bash
# Verify repo root structure
ls -la .claude/commands/experts/cli/
ls -la .claude/commands/experts/adw/
ls -la .claude/commands/experts/commands/
```

Expected output: Each directory should show a .gitkeep file.

```bash
# Verify Git tracking
git status
```

Expected output: Should show 6 new .gitkeep files (3 in CLI templates, 3 in repo root).

## Notes

**Design Decisions:**
- Used .gitkeep convention instead of README.md to minimize context window usage in generated projects
- Named directories `cli`, `adw`, `commands` to match TAC-13 specification domain boundaries
- Directory-only task deliberately kept simple - expert implementations are separate tasks (Tasks 4-12)

**Future Tasks Enabled:**
- Task 4-6: CLI Expert implementation (question.md, self-improve.md, expertise.yaml)
- Task 7-9: ADW Expert implementation
- Task 10-12: Commands Expert implementation

**No Code Changes Required:**
No scaffold_service.py or other code changes in this task - directories will be auto-included when template files are added in subsequent tasks.

**Pattern Consistency:**
Matches existing `cc_hook_expert/` structure demonstrating the proven three-file expert pattern.
