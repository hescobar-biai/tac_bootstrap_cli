---
doc_type: feature
adw_id: chore_Tac_13_Task_23
date: 2026-02-03
idk:
  - expert-registration
  - scaffold-service
  - template-rendering
  - code-generation
  - file-operations
  - documentation
tags:
  - feature
  - chore
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2
---

# Template Registration Verification and Documentation

**ADW ID:** chore_Tac_13_Task_23
**Date:** 2026-02-03
**Specification:** specs/issue-585-adw-chore_Tac_13_Task_23-chore_planner-verify-template-registrations.md

## Overview

This chore verified that all TAC-13 agent expert templates (Tasks 4-17) are properly registered in `scaffold_service.py` and added comprehensive inline documentation to explain the expert system architecture. The verification confirmed completeness of all expert template registrations and improved code organization with clear section headers and consistent registration patterns.

## What Was Built

- Comprehensive code documentation for expert registration system in `scaffold_service.py`
- Clear section headers organizing expert commands by domain (CLI, ADW, Commands, Hook)
- Updated module docstring to include expert-registration in IDK and invariants
- Enhanced method docstring explaining dual-strategy pattern
- Refactored expert command registration for better readability and maintainability
- Added expert-specific directory creation with descriptive reasons
- Verified all 12 expert templates are registered correctly

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Complete reorganization and documentation of expert template registration
  - Lines 1-7: Updated module docstring with expert-registration IDK and invariants
  - Lines 110-117: Enhanced directory creation with expert-specific paths and descriptions
  - Lines 288-295: Enhanced `_add_claude_files()` method docstring explaining dual-strategy pattern
  - Lines 499-512: Added major section header explaining TAC-13 expert system architecture
  - Lines 514-543: Reorganized expert command registrations by domain with inline comments
  - Lines 546-560: Refactored expertise file registrations into cleaner loop pattern

### Key Changes

- **Module Documentation**: Added expert-registration to IDK list and documented the 3-component pattern invariant
- **Section Headers**: Created clear separation blocks with ASCII art dividers for TAC-13 expert commands section
- **Domain Grouping**: Organized expert registrations by domain (Hook, CLI, ADW, Commands) with descriptive comments
- **Registration Refactoring**: Consolidated expertise file registrations into a cleaner loop-based pattern
- **Directory Structure**: Updated directory creation to include all four expert domains with descriptive reasons
- **Code Comments**: Added comprehensive inline documentation explaining purpose and usage of each expert component

## How to Use

The improvements in this chore are transparent to end users. When generating a new project with TAC Bootstrap:

1. Run the scaffold command:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap wizard
```

2. The expert templates will be automatically registered and generated in `.claude/commands/experts/`

3. Each expert will have three components:
   - `question.md` - Read-only queries using expertise file
   - `self-improve.md` - 7-phase self-improvement workflow
   - `expertise.yaml` - Mental model working memory

## Configuration

No additional configuration is required. The expert registration system is fully integrated into the scaffold service. The registration follows these patterns:

- **Command files (.md)**: Use `FileAction.CREATE` (overwrite on regeneration)
- **Expertise files (.yaml)**: Use `FileAction.CREATE` (don't overwrite if exists)
- **Domains**: cli, adw, commands, cc_hook_expert

## Testing

Verify the improvements with these commands:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to ensure code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Test the CLI smoke test:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Verify expert templates appear in scaffold plan:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap wizard --dry-run
```

## Notes

This chore focused on verification and documentation rather than new functionality. All expert template registrations were already present in the codebase but lacked comprehensive documentation and consistent organization. The improvements include:

- **Documentation First**: Added extensive comments explaining the expert system architecture
- **Pattern Consistency**: Ensured all registrations follow the same structural pattern
- **Maintainability**: Refactored repetitive code into cleaner loop patterns
- **Discoverability**: Clear section headers make it easy to locate and understand expert registrations

The 3-component expert pattern consists of:
1. **question.md** - Read-only Q&A using expertise + codebase validation
2. **self-improve.md** - 7-phase improvement workflow
3. **expertise.yaml** - Mental model (working memory only, not source of truth)

All four expert domains (Hook, CLI, ADW, Commands) follow this pattern consistently, making the system predictable and maintainable.
