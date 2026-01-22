# CLI Upgrade Command

**ADW ID:** d181e409
**Date:** 2026-01-21
**Specification:** specs/issue-85-adw-d181e409-sdlc_planner-cli-upgrade-command.md

## Overview

Added the `tac-bootstrap upgrade` command to the CLI, enabling users to upgrade existing TAC Bootstrap projects to the latest version. The command safely updates the Agentic Layer (`.claude/`, `adws/`, `scripts/`) while preserving user code and project configuration, with automatic backup and rollback capabilities.

## What Was Built

- CLI `upgrade` command with comprehensive argument and option handling
- Integration with existing `UpgradeService` for upgrade logic
- Interactive confirmation workflow with version comparison display
- Dry-run mode for previewing changes without modifications
- Configurable backup control (enabled by default)
- Force upgrade mode for re-applying templates
- Comprehensive error handling and user feedback
- Complete test suite with 8 test cases covering all scenarios

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Added `upgrade()` command function with full CLI interface (88 lines)
- `tac_bootstrap_cli/tests/test_upgrade_cli.py`: Created comprehensive test suite (164 lines)

### Key Changes

**CLI Command Implementation (cli.py:624-707)**:
- Added `@app.command()` decorated `upgrade()` function
- Configured 4 parameters:
  - `path`: Directory to upgrade (default: current directory)
  - `--dry-run/-n`: Preview changes without applying
  - `--backup/--no-backup`: Control backup creation (default: enabled)
  - `--force/-f`: Force upgrade even when versions match
- Implemented full upgrade workflow:
  1. Validate `config.yml` exists (exit with error if missing)
  2. Instantiate `UpgradeService` with project path
  3. Check versions and display current vs target
  4. Exit early if already up-to-date (unless `--force`)
  5. Display changes preview
  6. Exit if dry-run mode
  7. Request user confirmation
  8. Execute upgrade with automatic backup/rollback
  9. Display success/failure with appropriate messaging

**Welcome Panel Update (cli.py:76)**:
- Added `upgrade` command to welcome message displayed on `tac-bootstrap` invocation

**Test Suite (test_upgrade_cli.py)**:
- `test_upgrade_command_no_config()`: Validates error when config.yml missing
- `test_upgrade_command_already_up_to_date()`: Validates exit 0 when current
- `test_upgrade_command_dry_run()`: Validates preview mode doesn't modify files
- `test_upgrade_command_user_cancels()`: Validates cancellation handling
- `test_upgrade_command_success()`: Validates successful upgrade with backup
- `test_upgrade_command_no_backup()`: Validates upgrade without backup
- `test_upgrade_command_force()`: Validates force mode with matching versions
- `test_upgrade_command_failure()`: Validates error handling

## How to Use

### Basic Usage

Upgrade the current directory to the latest TAC Bootstrap version:

```bash
cd /path/to/your/project
tac-bootstrap upgrade
```

### Upgrade Specific Project

Upgrade a project at a specific path:

```bash
tac-bootstrap upgrade ./my-project
```

### Preview Changes (Dry Run)

See what would change without applying modifications:

```bash
tac-bootstrap upgrade --dry-run
```

### Upgrade Without Backup

For advanced users who don't need backup (not recommended):

```bash
tac-bootstrap upgrade --no-backup
```

### Force Upgrade

Re-apply templates even when versions match (useful for fixing corrupted files):

```bash
tac-bootstrap upgrade --force
```

### Combined Options

```bash
tac-bootstrap upgrade ./my-project --dry-run  # Preview specific project
tac-bootstrap upgrade --force --no-backup     # Force upgrade without backup
```

## Configuration

No additional configuration required. The command uses:

- `config.yml` in project root (must exist)
- `version` field in `config.yml` to determine current version
- TAC Bootstrap CLI version (`__version__`) as target version
- Default backup location: `.tac-backup-{timestamp}/` in project root

## Testing

Run the upgrade command tests:

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_upgrade_cli.py -v
```

Run all tests to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Verify command appears in help:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
cd tac_bootstrap_cli && uv run tac-bootstrap upgrade --help
```

## Notes

### Upgrade Behavior

**Directories Updated (complete overwrite)**:
- `adws/` - AI Developer Workflows
- `.claude/` - Claude Code commands and settings
- `scripts/` - Utility scripts

**Directories Preserved**:
- `src/`, `tac_bootstrap_cli/`, or any user code directories
- All custom user files outside template directories

**Partial Updates**:
- `config.yml` - Only `version` field updated, all other configuration preserved

### Safety Features

1. **Automatic Backup**: Creates `.tac-backup-{timestamp}/` before modifications (enabled by default)
2. **Automatic Rollback**: If upgrade fails mid-process, backup is automatically restored
3. **Manual Cleanup**: User must manually delete backup after confirming upgrade success
4. **Dry Run**: Preview all changes before committing
5. **Confirmation**: Requires explicit user confirmation before proceeding

### Version Handling

- Projects without `version` field default to "0.1.0"
- Uses semantic version comparison via `packaging` library
- Shows both current and target versions before upgrade
- Exit code 0 when already up-to-date (no error)

### Edge Cases

- **Missing directories**: Created during upgrade (not an error)
- **Only config.yml validation**: Full structure validation not required
- **Git status**: Not validated (backup provides protection)
- **Force mode**: Allows re-application of templates for repair scenarios

### Related Components

- **UpgradeService** (issue #82): Core upgrade logic and rollback mechanism
- **ScaffoldService**: Used to regenerate template directories
- **TACConfig Schema** (issue #79): Includes `version` field
- **__version__** (issue #81): Centralized version constant
- **packaging dependency** (issue #86): Semantic version comparison

### Future Enhancements (Not Implemented)

- Pre/post upgrade hooks for custom scripts
- Target specific version with `--target-version`
- Git validation for uncommitted changes
- Detailed file-level diff in dry-run mode
