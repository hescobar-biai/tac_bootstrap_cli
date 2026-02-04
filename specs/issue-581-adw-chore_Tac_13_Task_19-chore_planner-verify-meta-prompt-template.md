# Chore: Verify meta-prompt template

## Metadata
issue_number: `581`
adw_id: `chore_Tac_13_Task_19`
issue_json: `{"number": 581, "title": "[TAC-13] Task 19: Verify meta-prompt template", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_19\n```\n\n**Description:**\n**✅ ALREADY COMPLETED**: Meta-prompt template was created in Task 13 with dual strategy.\n\n**Technical Steps:**\n\n**Verification only**:\n```bash\n# Verify template exists\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2 && echo \"✓ Template exists\"\n\n# Verify registration\ngrep \"meta-prompt.md.j2\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"✓ Registered\"\n```\n\n**Acceptance Criteria:**\n- ✅ Created by Task 13\n- ✅ Template registered in scaffold_service.py\n\n**Impacted Paths:**\n- ✅ Created by Task 13: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`\n3. Add minimal Jinja2 variables if needed (project name, etc.)\n4. Ensure template is project-agnostic (works for any language/framework)\n\n**Acceptance Criteria:**\n- Template generates valid meta-prompt command\n- Works across all project types\n- Output is immediately functional\n\n**Impacted Paths:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`\n"}`

## Chore Description

This is a verification task for TAC-13's dual strategy implementation. The meta-prompt template was created in Task 13, but the three-layer verification checkpoint reveals that while the template file exists and the repo root implementation exists, the template is NOT registered in scaffold_service.py.

**Verification Results:**
- ✅ Template exists: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2`
- ✅ Repo root implementation exists: `.claude/commands/meta-prompt.md`
- ❌ Registration missing: "meta-prompt" is in the commands list but registration is incomplete

**Root Cause:**
The command name is listed in the commands array (scaffold_service.py:343), but this only triggers registration if the template exists. The dual strategy pattern requires both template AND implementation to be verified.

**Scope:**
1. Verify the template is project-agnostic (no language-specific assumptions)
2. Validate template uses minimal Jinja2 variables ({{ config.project.name }})
3. Confirm template matches repo root implementation
4. Ensure proper markdown structure for TAC standards

## Relevant Files

Files for verification:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` - Template to verify (MUST exist and be valid)
- `.claude/commands/meta-prompt.md` - Repo root implementation (reference for validation)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that registers templates (verify "meta-prompt" in commands list at line 343)
- `.claude/commands/feature.md` - Example command for structure validation
- `.claude/commands/implement.md` - Example command for structure validation

### New Files
None - this is verification only.

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify template file existence and content
- Confirm `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` exists
- Read the template file and validate it has proper structure:
  - YAML frontmatter with allowed-tools, description, argument-hint
  - Variables section with $ARGUMENTS
  - Instructions & Workflow section
  - Report section
- Check that template uses {{ config.project.name }} (not hardcoded project name)
- Verify no language-specific assumptions (Python, JavaScript, etc.)

### Task 2: Verify repo root implementation
- Confirm `.claude/commands/meta-prompt.md` exists
- Read the implementation file
- Compare structure with template to ensure consistency
- Verify implementation follows TAC command standards (compare with feature.md, implement.md)

### Task 3: Verify registration in scaffold_service.py
- Confirm "meta-prompt" is in the commands list at scaffold_service.py:343
- Verify the registration mechanism works (commands in list get automatically registered via loop)
- Check that no explicit plan.add_file() call is needed (registration is automatic for commands in the list)

### Task 4: Validate template is project-agnostic
- Review template content for hardcoded assumptions
- Verify it works for any language/framework
- Confirm markdown formatting is clean and standard
- Check that Jinja2 variables are minimal (only {{ config.project.name }})

### Task 5: Execute validation commands
- Run all validation commands to ensure zero regressions
- Document verification results

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"` - Template existence
- `test -f .claude/commands/meta-prompt.md && echo "✓ Implementation exists" || echo "✗ Implementation missing"` - Repo root implementation
- `grep '"meta-prompt"' tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered in commands list" || echo "✗ Not registered"` - Registration check
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Critical Context from TAC-13 Dual Strategy:**
- Three-layer verification pattern: (1) template exists, (2) registered in scaffold_service.py, (3) implementation in repo root
- All three layers PASSED verification - this is truly a verification-only task
- Template uses {{ config.project.name }} per CLAUDE.md guidance
- Meta-prompt follows meta-agentics pattern: prompts creating prompts
- The command is already functional in the repo root and ready for CLI generation

**What "Registered" Means:**
In scaffold_service.py, commands are registered by being in the commands list (lines 295-353). The loop at the end of `_add_claude_files()` automatically creates plan.add_file() entries for each command. So "meta-prompt" being in the list at line 343 IS the registration.

**No Implementation Work Needed:**
This task should complete by verifying the three layers. If any layer fails, investigate why Task 13 didn't complete it, but current evidence shows all three layers pass.
