# Update Unit Tests for add-agentic Existing Repo Scenario

**ADW ID:** 1a250086
**Date:** 2026-01-21
**Specification:** specs/issue-74-adw-1a250086-sdlc_planner-update-unit-tests.md

## Overview

This chore expanded and improved unit tests for the `ScaffoldService` to explicitly verify the behavior of the `add-agentic` scenario (when `existing_repo=True`). The tests now confirm that the scaffold service correctly uses `FileAction.CREATE` for existing repositories and properly respects this action by NOT overwriting existing files during `apply_plan()`.

## What Was Built

- Enhanced existing test `test_build_plan_existing_repo_creates_files` with specific verification for `.claude/` template files
- Added new test `test_apply_plan_create_does_not_overwrite_existing` to explicitly verify CREATE action behavior
- Comprehensive validation checklist documenting the test coverage

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Added 35 lines of test code to verify add-agentic scenario behavior
- `specs/issue-74-adw-1a250086-sdlc_planner-update-unit-tests-checklist.md`: Created validation checklist for implementation tracking
- `specs/issue-74-adw-1a250086-sdlc_planner-update-unit-tests.md`: Complete specification document for the chore

### Key Changes

1. **Enhanced `.claude/` Files Verification** (test_scaffold_service.py:145-151)
   - Added explicit check that all `.claude/` template files use `FileAction.CREATE`
   - Ensures existing repositories receive agentic layer files with safe CREATE action

2. **New Explicit Non-Overwrite Test** (test_scaffold_service.py:292-317)
   - Created `test_apply_plan_create_does_not_overwrite_existing()`
   - Manually creates file with "ORIGINAL CONTENT" before applying plan
   - Verifies that `apply_plan()` with `force=False` preserves existing content
   - Confirms `files_skipped` counter increments correctly

3. **Coverage for add-agentic Workflow**
   - Tests now comprehensively verify the three requirements:
     - `build_plan()` with `existing_repo=True` generates `FileAction.CREATE`
     - `apply_plan()` creates files when they don't exist
     - `apply_plan()` does NOT overwrite existing files (respects CREATE action)

## How to Use

### Running the Tests

Execute tests for the scaffold service:

```bash
cd tac_bootstrap_cli
uv run pytest tests/test_scaffold_service.py -v --tb=short
```

Run specific test:

```bash
cd tac_bootstrap_cli
uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceApplyPlan::test_apply_plan_create_does_not_overwrite_existing -v
```

Run all unit tests:

```bash
cd tac_bootstrap_cli
make test
```

### Understanding the Tests

The test suite verifies the complete add-agentic workflow:

1. **Test Build Plan** - `test_build_plan_existing_repo_creates_files` (line 134)
   - Verifies that existing repos get CREATE actions
   - Specifically checks `.claude/` files have CREATE action

2. **Test Apply Plan Safety** - `test_apply_plan_create_does_not_overwrite_existing` (line 292)
   - Creates pre-existing file with known content
   - Applies plan with CREATE action
   - Confirms original content preserved

3. **Test Skip Behavior** - `test_apply_plan_skips_existing_files` (line 261)
   - Verifies SKIP action doesn't modify files

## Configuration

No configuration changes required. Tests use the standard test fixtures and helpers:

- `create_test_config()` - Creates test TACConfig
- `tempfile.TemporaryDirectory()` - Provides isolated test environment
- `service.build_plan()` and `service.apply_plan()` - Core scaffold operations

## Testing

All tests pass with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short
```

Validation commands from specification:

```bash
# Scaffold service tests
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short

# All unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- The implementation in `scaffold_service.py` (lines 465-473) already had the correct logic for CREATE action non-overwrite behavior
- The tests make this behavior explicit and verifiable
- The `test_apply_plan_idempotent` test (line 297) also partially verified this by running `apply_plan()` twice, but the new test is more direct and clearer
- This test coverage is critical for the `add-agentic` use case where TAC Bootstrap adds agentic capabilities to existing repositories without destroying user files
