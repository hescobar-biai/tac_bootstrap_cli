# Chore: Verify meta-agent template

## Metadata
issue_number: `582`
adw_id: `chore_Tac_13_Task_20`
issue_json: `{"number": 582, "title": "[TAC-13] Task 20: Verify meta-agent template", "body": "**Workflow Metadata:**\n```\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_13_Task_20\n```\n\n**Description:**\n**\u2705 ALREADY COMPLETED**: Meta-agent template was created in Task 14 with dual strategy.\n\n**Technical Steps:**\n\n**Verification only**:\n```bash\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo \"\u2713 Template\"\ngrep \"meta-agent.md.j2\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"\u2713 Registered\"\n```\n\n**Acceptance Criteria:**\n- \u2705 Created by Task 14\n- \u2705 Template registered\n\n**Impacted Paths:**\n- \u2705 Created by Task 14: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`"}`

## Chore Description

This is a verification chore for TAC-13 Task 20. The meta-agent template was previously created in Task 14 following the dual strategy pattern. This task verifies that:

1. The template file exists at the expected location
2. The template is properly registered in scaffold_service.py
3. The implementation file exists at the repo root

The meta-agent is a "generator of agents" - it takes natural language descriptions and generates complete agent definition files following TAC standards.

## Relevant Files

Files to verify for this chore:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2` - Jinja2 template for CLI generation (MUST EXIST)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that registers templates (lines 344, 447)
- `.claude/commands/meta-agent.md` - Implementation file at repo root (SHOULD EXIST)

### New Files

No new files required - this is verification only.

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify template file exists

Run the verification command to confirm the Jinja2 template exists:

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"
```

Expected: Template exists

### Task 2: Verify template registration

Check that the template is registered in scaffold_service.py:

```bash
grep -n "meta-agent" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

Expected: Should find references at:
- Line ~344: In commands list
- Line ~447: In agents tuple with description

### Task 3: Verify implementation file

Check that the implementation file exists at repo root:

```bash
test -f .claude/commands/meta-agent.md && echo "✓ Implementation exists" || echo "✗ Implementation missing"
```

Expected: Implementation exists

### Task 4: Verify dual strategy completion

Read both files to confirm they follow TAC standards:

- Template should use Jinja2 syntax with `{{ config }}` variables
- Implementation should be production-ready markdown
- Both should have the same structure (YAML frontmatter, workflow, report sections)

### Task 5: Run validation commands

Execute all validation commands to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

This is a verification-only task. The actual implementation was completed in Task 14 which created:

1. CLI template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`
2. Registration: Added to scaffold_service.py commands list (line 344) and agents list (line 447)
3. Implementation: `.claude/commands/meta-agent.md`

The dual strategy pattern ensures:
- CLI users get the meta-agent via `tac-bootstrap generate`
- Repo root has working example for immediate use
- Both follow TAC standards for agent design

Verification should confirm all three components exist and are properly integrated.
