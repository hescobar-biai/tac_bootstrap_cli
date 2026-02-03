# Validation Checklist: ADW Expert - Question Prompt

**Spec:** `specs/issue-569-adw-feature_Tac_13_Task_7-sdlc_planner-adw-expert-question.md`
**Branch:** `feature-issue-569-adw-feature_Tac_13_Task_7-adw-expert-question-prompt`
**Review ID:** `feature_Tac_13_Task_7`
**Date:** `2026-02-03`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (716 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

**Template Creation:**
- [x] Template (.j2) created in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2`
- [x] Template follows TAC-13 3-phase pattern (read → validate → report)
- [x] Template includes frontmatter with allowed-tools and metadata
- [x] Template uses minimal Jinja2 variables

**Template Registration:**
- [x] Template registered in `scaffold_service.py` within `_add_claude_code_commands()` method
- [x] Registration uses correct action, template path, output path, and reason
- [x] Registration follows existing TAC-13 expert pattern

**Implementation File:**
- [x] Implementation file created in `.claude/commands/experts/adw/question.md`
- [x] Implementation file matches template content (static version)

**ADW-Specific Content:**
- [x] Phase 1 reads from `.claude/commands/experts/adw/expertise.yaml`
- [x] Phase 2 validates against `adws/`, `adw_modules/`, and `adw_triggers/` directories
- [x] Phase 3 reports on isolation patterns, module composition, triggers, and SDLC orchestration
- [x] Supports both general pattern queries and specific workflow queries
- [x] Includes examples of ADW-specific questions and expected reports

## Validation Commands Executed

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2 && echo "✓ Template exists"

# Verify registration in scaffold_service.py
grep -A 3 "experts/adw/question.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"

# Verify implementation file exists
test -f .claude/commands/experts/adw/question.md && echo "✓ Implementation file exists"

# Verify frontmatter structure
head -n 5 .claude/commands/experts/adw/question.md | grep -q "allowed-tools" && echo "✓ Frontmatter valid"

# Verify 3-phase structure
grep -q "Phase 1: Read Expertise File" .claude/commands/experts/adw/question.md && \
grep -q "Phase 2: Validate Expertise Against Codebase" .claude/commands/experts/adw/question.md && \
grep -q "Phase 3: Report Findings" .claude/commands/experts/adw/question.md && \
echo "✓ 3-phase structure present"

# Verify ADW-specific paths
grep -q "adws/" .claude/commands/experts/adw/question.md && \
grep -q "adw_modules/" .claude/commands/experts/adw/question.md && \
grep -q "adw_triggers/" .claude/commands/experts/adw/question.md && \
echo "✓ ADW paths referenced"

# Run standard validation suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The ADW Expert question prompt has been successfully implemented following the TAC-13 3-phase pattern. Both the Jinja2 template (.j2) and implementation file (.md) are in place, properly registered in scaffold_service.py, and include comprehensive ADW-specific validation logic for isolation patterns, module composition, trigger integration, and SDLC orchestration. All 716 automated tests pass with zero regressions.

## Review Issues

No blocking, tech debt, or skippable issues found.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
