# Chore: Verify expert-parallel template

## Metadata
issue_number: `584`
adw_id: `chore_Tac_13_Task_22`
issue_json: `{"number": 584, "title": "[TAC-13] Task 22: Verify expert-parallel template", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_22\n```\n\n**Description:**\n**✅ ALREADY COMPLETED**: Expert-parallel template was created in Task 17 with dual strategy.\n\n**Technical Steps:**\n\n**Verification only**:\n```bash\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo \"✓ Template\"\ngrep \"expert-parallel.md.j2\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"✓ Registered\"\n```\n\n**Acceptance Criteria:**\n- ✅ Created by Task 17\n- ✅ Template registered\n\n**Impacted Paths:**\n- ✅ Created by Task 17: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`\n"}`

## Chore Description
This is a verification task for TAC-13 Task 22. According to the issue, expert-parallel was already created in Task 17 with the dual strategy pattern (template + registration + implementation).

**Current Status:**
- ✅ Template exists: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
- ✅ Implementation exists: `.claude/commands/expert-parallel.md`
- ❌ Registration missing: Template is NOT registered in `scaffold_service.py`
- ❌ Skills registration missing: Command not listed in `.claude/settings.json`

**Issue Found:**
The template and implementation exist, but the registration in `scaffold_service.py` was not completed. The dual strategy requires all 3 components:
1. Template (.j2) - ✅ EXISTS
2. Registration (scaffold_service.py) - ❌ MISSING
3. Implementation (repo root) - ✅ EXISTS

This task will complete the missing registration step to fully implement the dual strategy pattern.

## Relevant Files

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add registration for expert-parallel.md.j2 template (around line 488-550 in expert commands section)

### Files to Verify (Existing)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2` - Jinja2 template (already exists)
- `.claude/commands/expert-parallel.md` - Implementation in repo root (already exists)
- `.claude/settings.json` - Skills registration (verify expert-parallel is listed)

### Reference Files
- `ai_docs/doc/plan_tasks_tac_13.md` - TAC-13 Task 17 original specification
- `ai_docs/doc/TAC-13_dual_strategy_summary.md` - Dual strategy pattern documentation

## Step by Step Tasks

### Task 1: Verify template and implementation files exist
- Verify `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2` exists
- Verify `.claude/commands/expert-parallel.md` exists
- Confirm both files have matching structure and frontmatter

### Task 2: Add registration to scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate the expert commands section (around line 488-550)
- Add registration entry for expert-parallel.md template:
  ```python
  # TAC-13 Task 17: Expert Parallel Scaling
  ("expert-parallel.md", "Parallel expert consensus - 3-10 agents for validation"),
  ```
- Place after expert-orchestrate (if it exists) or with other TAC-13 commands
- Follow the existing pattern used for expert-orchestrate and meta-agent

### Task 3: Verify skills registration in settings.json
- Check if `.claude/settings.json` has expert-parallel in skills list
- If missing, add entry following the pattern from other skills
- Ensure description matches: "Parallel expert consensus - spawn 3-10 agents for validation"

### Task 4: Verify dual strategy completeness
- Confirm all 3 components exist:
  1. Template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2`
  2. Registration: Entry in `scaffold_service.py`
  3. Implementation: `.claude/commands/expert-parallel.md`
- Run verification commands from issue description

### Task 5: Run validation commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo "✓ Template"` - Verify template exists
- `grep "expert-parallel.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"` - Verify registration

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/expert-parallel.md.j2 && echo "✓ Template"` - Template exists
- `grep "expert-parallel.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"` - Registration exists

## Notes

**About Dual Strategy Pattern:**
TAC-13 uses a "dual strategy" pattern where each command/skill requires 3 components:
1. **Template** (.j2 file in `tac_bootstrap_cli/tac_bootstrap/templates/`) - For CLI generation
2. **Registration** (entry in `scaffold_service.py`) - To include template in scaffolding
3. **Implementation** (file in repo root `.claude/commands/`) - Working version for this repo

**Task 17 Context:**
According to Task 17 in `ai_docs/doc/plan_tasks_tac_13.md`, the expert-parallel command was created with:
- 4-phase workflow (validate, spawn, monitor, synthesize)
- Variables: EXPERT_DOMAIN ($1), TASK ($2), NUM_AGENTS ($3, default 3)
- Range validation: 3-10 agents
- Opus model for synthesis

**Why Registration Missing:**
The template and implementation were created correctly, but the registration step in `scaffold_service.py` was likely overlooked during Task 17 implementation. This task completes that missing step.

**Similar Commands:**
Reference patterns from:
- `expert-orchestrate.md` (Task 16) - Similar meta-agentics command
- `meta-agent.md` (Task 14) - Another TAC-13 meta-agentics feature
- `meta-prompt.md` (Task 13) - First meta-agentics implementation
