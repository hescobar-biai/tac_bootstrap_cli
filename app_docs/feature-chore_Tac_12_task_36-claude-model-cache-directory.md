---
doc_type: feature
adw_id: chore_Tac_12_task_36
date: 2026-01-31
idk:
  - model-cache
  - gitkeep
  - directory-structure
  - scaffold-service
  - jinja2-templates
  - project-initialization
tags:
  - chore
  - infrastructure
  - project-generation
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2
  - .claude/data/claude-model-cache/.gitkeep
---

# Claude Model Cache Directory Creation

**ADW ID:** chore_Tac_12_task_36
**Date:** 2026-01-31
**Specification:** specs/issue-488-adw-chore_Tac_12_task_36-claude-model-cache-directory.md

## Overview

Create a `.claude/data/claude-model-cache/` directory with `.gitkeep` file in both the base TAC Bootstrap repository and CLI templates. This directory is used by `model_extractor.py` to cache model information, following the same pattern as the `sessions` directory created in Task 35.

## What Was Built

- `.claude/data/claude-model-cache/.gitkeep` file in base repository
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2` Jinja2 template
- Updated `ScaffoldService._add_directories()` to include claude-model-cache directory entry
- Updated `ScaffoldService._add_files()` to create .gitkeep file for model cache directory

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added directory configuration and .gitkeep file creation for the model cache directory

### Files Created

- `.claude/data/claude-model-cache/.gitkeep`: Empty marker file for base repository
- `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`: Empty Jinja2 template

### Key Changes

- Added `(".claude/data/claude-model-cache", "Model cache storage")` tuple to the directories list in `_add_directories()` method (line 120)
- Added `.gitkeep` file creation using `plan.add_file()` in the file creation section around line 172
- Followed the exact same pattern as the `sessions` directory to maintain consistency
- Empty files with no content, matching Git's `.gitkeep` convention for preserving empty directories

## How to Use

The claude-model-cache directory is automatically created by the TAC Bootstrap CLI during project generation. No manual configuration is required.

### For Project Developers

When the TAC Bootstrap CLI generates a new project, it automatically creates this directory structure:

```
generated-project/
└── .claude/
    └── data/
        └── claude-model-cache/
            └── .gitkeep
```

The `.gitkeep` file ensures the directory is tracked by Git, allowing `model_extractor.py` to use it for caching model information.

## Configuration

The directory creation is configured in the `ScaffoldService` class within `_add_directories()` method. No additional configuration is needed beyond adding the directory tuple to the directories list.

## Testing

### Test that directory structure is created

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Test syntax validation

```bash
cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/application/scaffold_service.py
```

### Test linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Test CLI smoke test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This feature follows Wave 5 (Status Line & Data Directories) of the TAC Bootstrap implementation plan
- It implements the same pattern as Task 35 (sessions directory), ensuring consistency across data directories
- The `.gitkeep` file is empty and serves only to preserve the directory in Git version control
- Both base repository and CLI templates require matching changes to maintain proper project generation
- This directory is consumed by `model_extractor.py` for caching model information
