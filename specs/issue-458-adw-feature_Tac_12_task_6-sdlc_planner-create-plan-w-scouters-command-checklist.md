# Validation Checklist: Create plan_w_scouters.md Command File

**Spec:** `specs/issue-458-adw-feature_Tac_12_task_6-sdlc_planner-create-plan-w-scouters-command.md`
**Branch:** `feature-issue-458-adw-feature_Tac_12_task_6-create-plan-w-scouters-command`
**Review ID:** `feature_Tac_12_task_6`
**Date:** `2026-01-29`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (690 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [x] Base command file `.claude/commands/plan_w_scouters.md` created with complete implementation
- [ ] Jinja2 template `plan_w_scouters.md.j2` created with minimal templating
- [ ] Template uses only `config.project.name` and `config.project.description` variables
- [x] Command integrated into `scaffold_service.py` commands list
- [ ] Template renders correctly with sample TACConfig
- [x] Rendered file has valid markdown syntax
- [x] File is generated in `.claude/commands/` during scaffolding
- [ ] Command structure follows existing patterns from `/quick-plan` and `/scout`
- [ ] Command includes:
   - [x] Variables section (USER_PROMPT, scout counts, output directory)
   - [ ] Instructions section (when to use, scout strategy explanation) - Missing distinction from /quick-plan
   - [x] Workflow section (scout launching, aggregation, plan generation)
   - [x] Report section (output format)
   - [x] Plan Format template
- [x] All validation commands pass with zero regressions

## Validation Commands Executed

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The implementation successfully creates the plan_w_scouters command file and integrates it into the scaffold service. All technical validations pass (690 tests, linting, type checking). However, there are several blocking issues: (1) the Jinja2 template is identical to the base file without any template variables, (2) the command title is "Quick Plan" instead of a unique identifier, and (3) the Instructions section doesn't explain when to use this command over /quick-plan or the scout strategy advantages.

## Review Issues

### Issue 1: Missing Jinja2 Templating Variables
**Severity:** blocker
**Description:** The template file `plan_w_scouters.md.j2` is identical to the base `.md` file and contains no Jinja2 variables. Acceptance criteria #3 requires template uses `config.project.name` and `config.project.description` variables.
**Resolution:** Add Jinja2 templating to at least reference project context in the command. For example, in the description or instructions section, add references like "for the {{ config.project.name }} project" or similar contextual uses.

### Issue 2: Command Title Not Distinctive
**Severity:** blocker
**Description:** The command file has title "# Quick Plan" which is identical to the `/quick-plan` command. This creates confusion about which command is being used.
**Resolution:** Change the title to "# Plan w/ Scouters" or "# Plan with Scout Exploration" to clearly distinguish this command from `/quick-plan`.

### Issue 3: Missing Scout Strategy Explanation
**Severity:** blocker
**Description:** The Instructions section doesn't explain when to use `/plan_w_scouters` over `/quick-plan` or describe the scout strategy advantages. The spec requires "Instructions section (when to use, scout strategy explanation)" in acceptance criteria #9.
**Resolution:** Add clear guidance in Instructions section explaining: (1) when to prefer this command over /quick-plan (complex tasks, unfamiliar codebases, need comprehensive context), (2) how the two-phase scout strategy works (fast scouts for surface, thorough scouts for depth), and (3) expected outcomes from using parallel exploration.

### Issue 4: Hardcoded Scout Agent Names
**Severity:** tech_debt
**Description:** The workflow references `@agent-scout-report-suggest` and `@agent-scout-report-suggest-fast` which are specific agent names that may not exist in all generated projects. This reduces portability.
**Resolution:** Either (1) use generic Task tool calls with subagent_type='Explore' and thoroughness parameter, or (2) document these as required agent definitions that must exist in the generated project's agent configuration.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
