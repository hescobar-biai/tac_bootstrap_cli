# Verify Add-Agentic Fix Specification

**ADW ID:** f24cb057
**Date:** 2026-01-21
**Specification:** specs/issue-72-adw-f24cb057-chore_planner-verify-add-agentic-fix.md

## Overview

This ADW created a comprehensive specification for manually verifying the fix to the `add-agentic` command (issue #70). The spec defines 10 verification tasks to ensure all templates are generated correctly, including commands, hooks, workflows, scripts, and configuration files. The actual verification work was not executed - only the specification and checklist files were created.

## What Was Built

- Verification specification with 10 detailed tasks
- Validation checklist with acceptance criteria
- MCP configuration updates for new worktree environment

## Technical Implementation

### Files Modified

- `specs/issue-72-adw-f24cb057-chore_planner-verify-add-agentic-fix.md`: Comprehensive verification spec with step-by-step tasks
- `specs/issue-72-adw-f24cb057-chore_planner-verify-add-agentic-fix-checklist.md`: Validation checklist with automated test results
- `.mcp.json`: Updated worktree path from b638d5b6 to f24cb057
- `playwright-mcp-config.json`: Updated video recording directory path

### Key Changes

- Created structured verification plan with 10 sequential tasks covering preparation, cleanup, execution, and validation
- Defined acceptance criteria for verifying 45+ files are generated (25+ commands, 6+ hooks, 14+ workflows, etc.)
- Included idempotency testing to ensure the command doesn't overwrite existing files
- Updated MCP configuration to point to current worktree directory
- Documented expected behavior before and after the fix (1 file vs 45+ files)

## How to Use

### Reviewing the Specification

1. Read the verification spec:
   ```bash
   cat specs/issue-72-adw-f24cb057-chore_planner-verify-add-agentic-fix.md
   ```

2. Review the validation checklist:
   ```bash
   cat specs/issue-72-adw-f24cb057-chore_planner-verify-add-agentic-fix-checklist.md
   ```

### Executing the Verification (Future Work)

The spec defines these verification steps (not yet executed):

1. **Prepare test directory**: Navigate to `~/Documents/Celes/dbt-models`
2. **Clean previous files**: Remove existing TAC artifacts
3. **Run add-agentic**: Execute `uv run tac-bootstrap add-agentic --target-dir ~/Documents/Celes/dbt-models`
4. **Verify Claude commands**: Check for 25+ .md files in `.claude/commands/`
5. **Verify Claude hooks**: Check for 6+ .py files in `.claude/hooks/`
6. **Verify ADW workflows**: Check for 14+ workflow files in `adws/`
7. **Verify config files**: Check for `config.yml`, `constitution.md`, `CLAUDE.md`
8. **Count total files**: Verify 45+ files were created
9. **Test idempotency**: Re-run and verify files are skipped, not overwritten
10. **Run validation tests**: Execute unit tests, linting, and smoke tests

## Configuration

No configuration changes required. The spec uses existing TAC Bootstrap CLI configuration.

## Testing

Automated tests passed:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
# ✓ 269 tests passed
```

Linting passed:
```bash
cd tac_bootstrap_cli && uv run ruff check .
# ✓ No issues found
```

Smoke test passed:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
# ✓ CLI responds correctly
```

## Notes

### Current Status

This ADW is **incomplete**. The spec and checklist were created, but the actual verification work defined in the 10 tasks was not executed. The review identified this as a blocker issue.

### Next Steps

To complete this verification:
1. Execute tasks 1-10 as defined in the spec
2. Document file counts and command outputs
3. Verify the 45+ files threshold is met
4. Test idempotency behavior
5. Capture results in a verification report

### Expected Results

- **Before fix (issue #70)**: `add-agentic` created only 1 file
- **After fix**: `add-agentic` should create 45+ files including:
  - 25+ Claude commands (.md files)
  - 6+ Claude hooks (.py files)
  - 14+ ADW workflows (.py files)
  - ADW modules directory with utilities
  - Scripts directory with helper scripts
  - Config files (config.yml, constitution.md, CLAUDE.md)

### Related Issues

- **Issue #70**: Original bug fix for FileAction skip logic
- **Issue #72**: This verification task to validate the fix works correctly
