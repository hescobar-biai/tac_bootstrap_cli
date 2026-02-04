# Chore: Verify expert-orchestrate template

## Metadata
issue_number: `583`
adw_id: `chore_Tac_13_Task_21`
issue_json: `{"number": 583, "title": "[TAC-13] Task 21: Verify expert-orchestrate template", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_21\n```\n\n**Description:**\n**✅ ALREADY COMPLETED**: Expert-orchestrate template was created in Task 16 with dual strategy.\n\n**Technical Steps:**\n\n**Verification only**:\n```bash\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2 && echo \"✓ Template\"\ngrep \"expert-orchestrate.md.j2\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"✓ Registered\"\n```\n\n**Acceptance Criteria:**\n- ✅ Created by Task 16\n- ✅ Template registered\n\n**Impacted Paths:**\n- ✅ Created by Task 16: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`"}`

## Chore Description
This is a verification task to confirm that the `expert-orchestrate` template was properly created in Task 16 using the dual strategy pattern. The template implements a meta-command that orchestrates a complete expert workflow cycle: planning, building, and self-improvement for domain experts.

**Status**: Already completed in Task 16. This task only verifies that:
1. Template file exists at the correct location
2. Template is registered in `scaffold_service.py`
3. Template uses correct Jinja2 syntax with `{{ config }}` variables

## Relevant Files

### Verification Targets
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2` - The Jinja2 template (ALREADY EXISTS)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:345` - Registration in command list (ALREADY EXISTS)

### Documentation References
- `PLAN_TAC_BOOTSTRAP.md` - Contains TAC-13 tasks overview
- `ai_docs/doc/TAC-13_dual_strategy_summary.md` - Dual strategy pattern documentation
- `ai_docs/doc/TAC-13_implementation_status.md` - Implementation progress tracking

## Step by Step Tasks

### Task 1: Verify Template File Exists
- Run verification command to confirm template file exists
- Expected output: `✓ Template`
- File path: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2`

### Task 2: Verify Template Registration
- Check that `expert-orchestrate` is in the commands list in `scaffold_service.py`
- Line 345 should contain `"expert-orchestrate",`
- Template should be registered with action (skip_if_exists or create) at line ~359

### Task 3: Verify Template Content Structure
- Read template file to ensure it follows correct format:
  - Has YAML frontmatter with allowed-tools, description, argument-hint, model
  - Uses `{{ config.project.name }}` syntax (not hardcoded values)
  - Contains proper orchestration workflow instructions (Plan → Build → Improve)
  - Has 7 main steps: validation, todo init, plan, build, self-improve, report, final status

### Task 4: Verify Seed File (Optional)
- Check if seed file exists in repository: `.claude/commands/expert-orchestrate.md`
- This is the actual implementation used by agents (not a template)
- If missing, this is acceptable as it may be scaffolded on-demand

### Task 5: Run Validation Commands
- Execute all validation commands to ensure zero regressions
- Confirm all tests pass, linting succeeds, and smoke test works

## Validation Commands
Execute all commands to validate with zero regressions:

- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2 && echo "✓ Template exists"` - Template file existence
- `grep -n "expert-orchestrate" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Registration verification
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Findings from Initial Verification
✅ **Template exists**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-orchestrate.md.j2` (301 lines)
✅ **Registered in scaffold_service.py**: Line 345 contains `"expert-orchestrate",`
✅ **Template uses correct syntax**: Contains `{{ config.project.name }}` on line 84
✅ **Complete workflow structure**: Has all 7 required steps with proper error handling

### Verification Result
**STATUS: VERIFIED**

The expert-orchestrate template was properly created in Task 16 with:
- ✅ Jinja2 template at correct location
- ✅ Registration in scaffold_service.py commands list
- ✅ Proper use of `{{ config }}` variable
- ✅ Complete orchestration workflow (Plan → Build → Improve)
- ✅ Input validation, error handling, todo tracking, synthesis report

**Dual Strategy Pattern Confirmed:**
1. **Template**: `templates/claude/commands/expert-orchestrate.md.j2` ✅
2. **Registration**: `scaffold_service.py:345` ✅
3. **Implementation**: Seed file in repo root (optional, scaffolded on-demand)

This task is effectively complete and requires no additional implementation work.
