# Chore: Document upgrade command in README files

## Metadata
issue_number: `89`
adw_id: `e69c669b`
issue_json: `{"number":89,"title":"TAREA 8: Documentar comando en README","body":"**Archivo**: `tac_bootstrap_cli/README.md` y `README.md` principal\n\n**Descripción**: Agregar documentación del comando upgrade.\n\n**Contenido a agregar**:\n\n```markdown\n## Upgrading Projects\n\nIf you have a project created with an older version of TAC Bootstrap,\nyou can upgrade it to the latest templates:\n\n```bash\n# Check what would be upgraded\ntac-bootstrap upgrade --dry-run\n\n# Upgrade with backup (default)\ntac-bootstrap upgrade\n\n# Upgrade without backup\ntac-bootstrap upgrade --no-backup\n\n# Force upgrade even if versions match\ntac-bootstrap upgrade --force\n\n# Upgrade specific project\ntac-bootstrap upgrade ./path/to/project\n```\n\n### What Gets Upgraded\n\nThe upgrade command updates:\n- `adws/` - AI Developer Workflows\n- `.claude/` - Claude Code configuration\n- `scripts/` - Utility scripts\n\nIt preserves:\n- `src/` - Your application code\n- `config.yml` - Your configuration (only version is updated)\n- Any custom files you've added\n\n### Backup\n\nBy default, a backup is created at `.tac-backup-{timestamp}/` before upgrading.\nDelete it manually after confirming the upgrade works correctly.\n```\n\n**Criterios de Aceptación**:\n- [ ] Documentación clara del comando\n- [ ] Ejemplos de uso\n- [ ] Explicación de qué se actualiza\n- [ ] Información sobre backups\n"}`

## Chore Description
Add comprehensive documentation for the `upgrade` command to both README files:
- Main repository README (`README.md`)
- CLI README (`tac_bootstrap_cli/README.md`)

The documentation should include:
1. Command usage examples (dry-run, backup options, force mode)
2. Explanation of what gets upgraded vs preserved
3. Backup behavior and cleanup instructions

## Relevant Files
Files that need to be modified:

- `tac_bootstrap_cli/README.md` - CLI-specific README that needs upgrade command documentation
- `README.md` - Main repository README that also needs upgrade command documentation

Both files already have comprehensive documentation for other commands (init, add-agentic, doctor, render), so the upgrade documentation should follow the same structure and style.

### New Files
No new files required.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Add upgrade documentation to CLI README
- Read `tac_bootstrap_cli/README.md` to understand current structure
- Identify the best location to add the upgrade documentation (after the "Utility Commands" section but before "Commands" section)
- Add the "## Upgrading Projects" section with all examples and subsections
- Ensure formatting matches existing documentation style

### Task 2: Add upgrade command to Commands section in CLI README
- Add `upgrade` command documentation in the Commands section
- Follow the same format as existing commands (init, add-agentic, doctor, render)
- Include options table with descriptions

### Task 3: Add upgrade documentation to main README
- Read `README.md` to understand current structure
- Add similar upgrade documentation to the main README
- Place it in the appropriate section (likely after "For Existing Projects" section)
- Ensure consistency with CLI README but adapt to main README context

### Task 4: Validate documentation
- Check that all code blocks use correct syntax highlighting
- Verify that examples are clear and complete
- Ensure backup information is prominent
- Execute validation commands

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The upgrade command was recently implemented (issues 81-87 in the plan)
- Documentation should emphasize the safety features (backup, dry-run)
- Make it clear that upgrade is safe and preserves user code
- Backup cleanup is manual by design - emphasize this
- Both READMEs should have consistent information but may differ in presentation style
