# Validation Checklist: Update SLASH_COMMAND_MODEL_MAP in agent.py with TAC-11 commands

**Spec:** `specs/issue-332-adw-chore_Tac_11_task_14-chore_planner-update-slash-command-model-map.md`
**Branch:** `chore-issue-332-adw-chore_Tac_11_task_14-update-slash-command-model-map`
**Review ID:** `chore_Tac_11_task_14`
**Date:** `2026-01-27`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (690 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

No explicit acceptance criteria section was found in the spec file. Based on the implementation:

- [x] `/scout` command added to SLASH_COMMAND_MODEL_MAP with sonnet for both base and heavy model sets
- [x] `/question` command added to SLASH_COMMAND_MODEL_MAP with sonnet for both base and heavy model sets
- [x] Both commands include descriptive comments following the existing pattern (TAC-11)
- [x] Dictionary syntax is correct (proper commas, quotes, braces)
- [x] New entries are positioned logically at the end with other TAC-series commands
- [x] All validation commands pass without regressions

## Validation Commands Executed

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The implementation successfully adds the two new TAC-11 slash commands (`/scout` and `/question`) to the `SLASH_COMMAND_MODEL_MAP` dictionary in `adws/adw_modules/agent.py`. Both commands are correctly configured to use the "sonnet" model for both base and heavy model sets, as specified. The implementation follows the existing code style with appropriate inline comments. All validation tests pass with no regressions.

## Review Issues

No issues found. The implementation is complete and correct.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
