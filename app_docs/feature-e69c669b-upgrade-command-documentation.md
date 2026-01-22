# Upgrade Command Documentation

**ADW ID:** e69c669b
**Date:** 2026-01-22
**Specification:** specs/issue-89-adw-e69c669b-chore_planner-document-upgrade-command.md

## Overview

Comprehensive documentation for the `upgrade` command has been added to both the main repository README and the CLI README. The documentation provides users with clear guidance on how to safely upgrade existing TAC Bootstrap projects to the latest templates while preserving their custom code and configuration.

## What Was Built

- Upgrade command usage section in main README (`README.md`)
- Upgrade command usage section in CLI README (`tac_bootstrap_cli/README.md`)
- Detailed explanations of what gets upgraded vs. what gets preserved
- Examples covering all upgrade scenarios (dry-run, backup options, force mode)
- Safety information about backup behavior

## Technical Implementation

### Files Modified

- `README.md`: Added "Actualizar Proyectos Existentes" section with Spanish documentation
- `tac_bootstrap_cli/README.md`: Added "Upgrading Projects" section with English documentation

### Key Changes

- Added comprehensive upgrade documentation section before "Flujo de Usuario" in main README
- Added "Upgrading Projects" section before "Commands" section in CLI README
- Added `upgrade` command entry to the Commands reference section with full options table
- Included practical examples covering all command flags (--dry-run, --no-backup, --force)
- Documented directory preservation strategy (src/, config.yml) and upgrade targets (adws/, .claude/, scripts/)

## How to Use

The documentation describes the upgrade command usage:

1. **Preview changes** (recommended first step):
   ```bash
   tac-bootstrap upgrade --dry-run
   ```

2. **Upgrade with backup** (default, safest option):
   ```bash
   tac-bootstrap upgrade
   ```

3. **Upgrade specific project**:
   ```bash
   tac-bootstrap upgrade ./path/to/project
   ```

4. **Advanced options**:
   ```bash
   # Skip backup (use with caution)
   tac-bootstrap upgrade --no-backup

   # Force upgrade even if versions match
   tac-bootstrap upgrade --force
   ```

## Configuration

No configuration changes required. The documentation covers the existing upgrade command options:

- `--dry-run`: Preview changes without applying them
- `--no-backup`: Skip creating backup before upgrade
- `--force`: Force upgrade even if versions match

## Testing

Documentation was validated as part of the chore workflow. To verify the command works as documented:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "upgrade"
```

To verify the CLI help matches the documentation:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap upgrade --help
```

## Notes

- Main README uses Spanish ("Actualizar Proyectos Existentes") while CLI README uses English ("Upgrading Projects"), maintaining consistency with each file's existing language
- Documentation emphasizes safety features (backup by default, dry-run option)
- Backup cleanup is manual by design - this is explicitly documented to prevent users from expecting automatic cleanup
- The upgrade command was implemented in issues 81-87 and is now fully documented for user accessibility
- Both READMEs have consistent information but differ in presentation style to match their respective audiences
