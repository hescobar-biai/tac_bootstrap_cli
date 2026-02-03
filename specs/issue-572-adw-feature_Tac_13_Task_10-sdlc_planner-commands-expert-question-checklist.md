# Validation Checklist: Commands Expert - Question Prompt

**Spec:** `specs/issue-572-adw-feature_Tac_13_Task_10-sdlc_planner-commands-expert-question.md`
**Branch:** `feature-issue-572-adw-feature_Tac_13_Task_10-commands-expert-question-prompt`
**Review ID:** `feature_Tac_13_Task_10`
**Date:** `2026-02-03`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [x] **Template Created**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2` exists with valid structure
- [x] **Implementation Created**: `.claude/commands/experts/commands/question.md` exists and mirrors template
- [x] **Registration Complete**: scaffold_service.py includes Commands expert question registration
- [x] **TAC-13 Pattern Followed**: 3-phase workflow (Reuse → Validate → Answer)
- [x] **Read-Only Tools**: Only Bash, Read, Grep, Glob, TodoWrite allowed
- [x] **Variables Defined**: USER_QUESTION ($1), EXPERTISE_PATH, COMMANDS_ROOT
- [x] **Answers Command Topics**: Structure, variables, workflows, tool restrictions, integration patterns
- [x] **Evidence-Based**: Report format includes file:line citations
- [x] **Mirrors ADW Expert**: Consistent structure with ADW expert from Task 9
- [x] **No Jinja2 in Implementation**: Concrete file has no template syntax

## Validation Commands Executed

```bash
# Test 1: File existence
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2 && echo "✅ Template exists" || echo "❌ Template missing"

test -f .claude/commands/experts/commands/question.md && echo "✅ Implementation exists" || echo "❌ Implementation missing"

# Test 2: YAML frontmatter validation
head -6 .claude/commands/experts/commands/question.md | grep -q "allowed-tools: Bash, Read, Grep, Glob, TodoWrite" && echo "✅ Read-only tools verified" || echo "❌ Wrong tools"

# Test 3: Registration verification
grep -q "experts/commands/question.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✅ Registration found" || echo "❌ Not registered"

# Test 4: Unit tests (if applicable)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Test 5: Linting
cd tac_bootstrap_cli && uv run ruff check .

# Test 6: Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Test 7: Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

Successfully implemented Commands expert question prompt following TAC-13 Agent Expert pattern. The implementation includes both a Jinja2 template for CLI generation and a concrete implementation in the repository root. The prompt follows the 3-phase workflow (Read Expertise → Validate Against Code → Report Findings) and is configured as read-only with appropriate tool restrictions. All 718 unit tests pass, linting is clean, type checking passes, and CLI smoke test succeeds.

## Review Issues

No blocking issues found. The implementation fully meets all acceptance criteria.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
