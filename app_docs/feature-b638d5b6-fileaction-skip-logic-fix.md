# FileAction Skip Logic Fix

**ADW ID:** b638d5b6
**Date:** 2026-01-21
**Specification:** specs/issue-70-adw-b638d5b6-bug_planner-fix-fileaction-skip-logic.md

## Overview

Fixed a critical bug in scaffold_service.py where files were incorrectly marked as SKIP when scaffolding into existing repositories. This prevented TAC Bootstrap from creating any files in existing repos, even if those files didn't exist yet. The fix changes the file action logic to always use `FileAction.CREATE`, which is inherently idempotent and safe for existing repos.

## What Was Built

- Fixed file action logic in 5 scaffold methods in scaffold_service.py
- Updated test expectations to validate idempotent CREATE behavior
- Added clarifying comments explaining CREATE semantics

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Updated file action logic in 5 methods (lines 113, 204, 284, 305, 343)
- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Updated test to validate CREATE behavior instead of SKIP behavior

### Key Changes

**Before (Incorrect):**
```python
action = FileAction.CREATE if not existing_repo else FileAction.SKIP
```

**After (Correct):**
```python
action = FileAction.CREATE  # CREATE only creates if file doesn't exist
```

**Methods Updated:**
1. `_add_claude_files()` - scaffold_service.py:113
2. `_add_adw_files()` - scaffold_service.py:204
3. `_add_script_files()` - scaffold_service.py:284
4. `_add_config_files()` - scaffold_service.py:305
5. `_add_structure_files()` - scaffold_service.py:343

**Why This Fix Works:**
- `FileAction.CREATE` has built-in idempotency - it only creates files that don't exist
- The `apply_plan` method (scaffold_service.py:466-469) already checks if files exist before creating them
- `FileAction.SKIP` means "never create under any circumstances" - wrong for missing files
- `FileAction.CREATE` means "create if missing, skip if exists" - correct for all scenarios

## How to Use

This fix is transparent to end users. When running TAC Bootstrap on an existing repository:

```bash
cd existing-project
tac-bootstrap
```

**Before the fix:** Zero files created (all marked SKIP)
**After the fix:** Missing files are created, existing files are preserved

The CLI will now:
1. Create all template files that don't exist in the target directory
2. Skip all files that already exist (preserving user modifications)
3. Provide accurate reporting of files created vs skipped

## Configuration

No configuration changes required. The fix is automatic and backward compatible.

## Testing

Run the full test suite to validate the fix:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

**Key Test Updated:**
- `test_build_plan_existing_repo_creates_files` (formerly `test_build_plan_existing_repo_skips_files`)
- Now validates that files are marked CREATE (not SKIP) when `existing_repo=True`
- Validates that CREATE action is idempotent and safe for existing repositories

## Notes

- The `existing_repo` parameter remains in method signatures for potential future use (e.g., conditional logic, different templates)
- FileAction.CREATE already had correct semantics per domain/plan.py:16 - `CREATE = "create"  # Create new file (skip if exists)`
- The bug was in scaffold_service.py logic, not in the FileAction enum definition
- config.yml has special OVERWRITE logic and .gitignore has PATCH logic - these were not affected by this bug
- This fix enables safe scaffolding into existing repos without data loss
