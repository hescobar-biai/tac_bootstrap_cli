# Validation Checklist: Update background.md with TAC-12 improvements

**Spec:** `specs/issue-489-adw-feature_Tac_12_task_37-sdlc_planner-update-background-command.md`
**Branch:** `feature-issue-489-adw-feature_Tac_12_task_37-update-background-command`
**Review ID:** `feature_Tac_12_task_37`
**Date:** `2026-01-31`

## Automated Technical Validations

- [ ] Syntax and type checking - FAILED
- [ ] Linting - PASSED
- [ ] Unit tests - PASSED
- [ ] Application smoke test - FAILED

## Acceptance Criteria

- [ ] Base file updated: `.claude/commands/background.md` completely replaced with bash-based claude CLI implementation
- [ ] Template file updated: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` with Jinja2 parameterization
- [ ] All Key Changes present:
  - [ ] Variables: USER_PROMPT ($1), MODEL ($2, defaults 'sonnet'), REPORT_FILE ($3)
  - [ ] Uses `claude` CLI directly with --dangerously-skip-permissions
  - [ ] Structured report format with append-system-prompt
  - [ ] Auto-rename to .complete.md or .failed.md based on exit code
  - [ ] Timestamp: TIMESTAMP=$(date +%a_%H_%M_%S)
  - [ ] Directory: agents/background/ documented
- [ ] Files are identical in structure: Base and template have same documentation approach, differ only in variable syntax
- [ ] Security warnings included: Clear documentation of --dangerously-skip-permissions implications
- [ ] Error handling documented: Fallback behavior when rename fails, directory doesn't exist, etc.
- [ ] Examples provided: 2-3 realistic use cases showing command execution
- [ ] Valid markdown and bash syntax: Files pass validation checks

## Validation Commands Executed

```bash
grep -q "USER_PROMPT" ./.claude/commands/background.md && echo "✓ USER_PROMPT variable documented" || echo "✗ USER_PROMPT variable NOT found"
grep -q "dangerously-skip-permissions" ./.claude/commands/background.md && echo "✓ Security flag documented" || echo "✗ Security flag NOT found"
grep -q ".complete.md" ./.claude/commands/background.md && echo "✓ Complete status renaming documented" || echo "✗ Complete status renaming NOT found"
grep -q ".failed.md" ./.claude/commands/background.md && echo "✓ Failed status renaming documented" || echo "✗ Failed status renaming NOT found"
grep -q "agents/background" ./.claude/commands/background.md && echo "✓ Directory structure documented" || echo "✗ Directory structure NOT found"
```

## Review Summary

**CRITICAL FINDINGS:** Implementation is incomplete. Neither the base file (`.claude/commands/background.md`) nor the template file (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`) have been updated with the TAC-12 bash-based claude CLI implementation. Both files still contain outdated Task Tool delegation documentation. All key requirements from the specification are missing:

- USER_PROMPT, MODEL, and REPORT_FILE variables are not defined
- Security flag `--dangerously-skip-permissions` is not documented
- File auto-renaming (.complete.md/.failed.md) is not implemented
- Claude CLI bash invocation is not present
- Directory structure requirements (agents/background/) are not documented
- Jinja2 parameterization in the template file is absent

This is a blocker for release - the implementation was not completed despite the specification being comprehensive and clear.

## Review Issues

### Issue #1: Base File Not Updated
- **Description:** `.claude/commands/background.md` still contains old Task Tool documentation instead of bash-based claude CLI implementation
- **Resolution:** Complete implementation of base file with all sections from spec: Variables ($1, $2, $3), Instructions, bash code block with claude CLI invocation, security warnings, examples, and report format
- **Severity:** blocker

### Issue #2: Template File Not Updated
- **Description:** `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` still contains old Task Tool documentation without Jinja2 parameterization
- **Resolution:** Update template file to match base file structure and add Jinja2 variables for directory paths and project-specific configuration
- **Severity:** blocker

### Issue #3: Missing Claude CLI Implementation
- **Description:** Neither file implements direct claude CLI invocation with `--dangerously-skip-permissions` flag as required by spec
- **Resolution:** Add bash code block showing: `claude run-on-files --dangerously-skip-permissions --append-system-prompt "..." $MODEL 2>&1 > "$REPORT_FILE"`
- **Severity:** blocker

### Issue #4: Missing Security Documentation
- **Description:** No security warnings about `--dangerously-skip-permissions` implications documented
- **Resolution:** Add clear warning section explaining permission bypass and when it's appropriate to use
- **Severity:** blocker

### Issue #5: Missing File Auto-Rename Logic
- **Description:** No documentation of automatic file renaming to .complete.md or .failed.md based on exit code
- **Resolution:** Add bash logic showing: `if [ $? -eq 0 ]; then mv "$REPORT_FILE" "${REPORT_FILE%.md}.complete.md"; else mv "$REPORT_FILE" "${REPORT_FILE%.md}.failed.md"; fi`
- **Severity:** blocker

### Issue #6: Missing Timestamp Handling
- **Description:** No TIMESTAMP=$(date +%a_%H_%M_%S) implementation documented
- **Resolution:** Document timestamp capture and inclusion in report format
- **Severity:** blocker

### Issue #7: Missing Directory Documentation
- **Description:** agents/background/ directory prerequisite not documented
- **Resolution:** Add notes about directory creation and when it should exist
- **Severity:** blocker

### Issue #8: No Examples Provided
- **Description:** Current examples don't show background command execution with proper parameters
- **Resolution:** Add 2-3 examples showing: $USER_PROMPT="...", $MODEL="sonnet", $REPORT_FILE="..."
- **Severity:** blocker

---
*Generado por el comando `/review` - TAC Bootstrap CLI*
