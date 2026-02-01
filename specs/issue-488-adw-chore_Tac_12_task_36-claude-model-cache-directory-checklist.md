# Validation Checklist: Create .claude/data/claude-model-cache directory with .gitkeep

**Spec:** `specs/issue-488-adw-chore_Tac_12_task_36-claude-model-cache-directory.md`
**Branch:** `chore-issue-488-adw-chore_Tac_12_task_36-create-model-cache-directory`
**Review ID:** `chore_Tac_12_task_36`
**Date:** `2026-01-31`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [ ] Base directory `.claude/data/claude-model-cache/` created
- [ ] `.gitkeep` file created in base directory
- [ ] Jinja2 template file created at `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`
- [ ] Directory entry added to `scaffold_service.py` `_add_directories()` method
- [ ] `.gitkeep` file creation added to `scaffold_service.py` after line 171

## Validation Commands Executed

```bash
cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/application/scaffold_service.py
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The technical validation checks pass (syntax, linting, tests, smoke test), but the implementation has a **critical logic error**: the changes show that the required files and code entries are being **deleted** rather than **created**. According to the spec, the chore should create the `.claude/data/claude-model-cache/` directory with a `.gitkeep` file in both the base repository and CLI templates, and update `scaffold_service.py` to include these in the directory creation logic. The current implementation does the opposite—it removes these files and entries.

## Review Issues

### Issue 1: Files Deleted Instead of Created - BLOCKER
- **Severity:** blocker
- **Description:** The `.claude/data/claude-model-cache/.gitkeep` file and the template file at `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2` are being deleted (as shown in git diff), not created as the spec requires.
- **Resolution:** Restore/create these files instead. The files should be empty, matching the pattern of the `sessions` directory created in Task 35.

### Issue 2: scaffold_service.py Entries Removed Instead of Added - BLOCKER
- **Severity:** blocker
- **Description:** The directory entry `(".claude/data/claude-model-cache", "Model cache storage")` and the `.gitkeep` file creation logic were removed from `scaffold_service.py` (lines 120 and 172-178 deleted), but the spec requires these to be added.
- **Resolution:** Add these entries back to `scaffold_service.py` following the exact pattern shown in the spec: the directory tuple should be in the directories list around line 120, and the file creation should be in the .gitkeep section around line 172.

### Issue 3: Base Directory Does Not Exist - BLOCKER
- **Severity:** blocker
- **Description:** Running `ls -la .claude/data/` shows only the `sessions` directory exists. The `claude-model-cache` directory is missing.
- **Resolution:** Create the directory with the `.gitkeep` file to match the reference implementation structure.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
