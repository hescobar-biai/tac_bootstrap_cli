# Upgrade Service for TAC Bootstrap Projects

**ADW ID:** c928f831
**Date:** 2026-01-21
**Specification:** specs/issue-82-adw-c928f831-sdlc_planner-upgrade-service.md

## Overview

The UpgradeService enables automated upgrading of TAC Bootstrap projects to newer CLI versions. It safely updates the Agentic Layer (`.claude/`, `adws/`, `scripts/`) while preserving user configuration, with automatic backup and rollback capabilities.

## What Was Built

The implementation includes:

- **UpgradeService class** - Core service managing project upgrade lifecycle
- **Version detection** - Compares current project version with CLI version
- **Automatic backup** - Creates timestamped backups before modifications
- **Selective regeneration** - Updates only Agentic Layer directories
- **Configuration preservation** - Maintains user settings during upgrade
- **Automatic rollback** - Restores from backup if upgrade fails
- **Change preview** - Dry-run capability to preview modifications

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py`: New service implementing complete upgrade logic (190 lines)
- `specs/issue-82-adw-c928f831-sdlc_planner-upgrade-service.md`: Complete specification document (244 lines)
- `specs/issue-82-adw-c928f831-sdlc_planner-upgrade-service-checklist.md`: Implementation checklist (54 lines)

### Key Changes

1. **Version Management**
   - `get_current_version()`: Reads version from `config.yml` (defaults to "0.1.0" for legacy projects)
   - `get_target_version()`: Returns current CLI version from `tac_bootstrap.__version__`
   - `needs_upgrade()`: Semantic version comparison using `packaging.version.parse()`

2. **Backup System**
   - `create_backup()`: Creates `.tac-backup-{timestamp}/` directory
   - Copies all UPGRADEABLE_DIRS (`adws/`, `.claude/`, `scripts/`)
   - Preserves `config.yml` for rollback scenarios

3. **Upgrade Execution**
   - `perform_upgrade()`: Main upgrade orchestration method
   - Removes old Agentic Layer directories
   - Regenerates using `ScaffoldService.build_plan()` and `apply_plan()`
   - Automatic restoration from backup on failure

4. **Preview Capability**
   - `get_changes_preview()`: Returns list of planned changes
   - Enables CLI dry-run functionality
   - Shows which directories will be updated or created

## How to Use

The UpgradeService is designed to be consumed by the CLI upgrade command (to be implemented in TAREA 5). Programmatic usage:

```python
from pathlib import Path
from tac_bootstrap.application.upgrade_service import UpgradeService

# Initialize service
project_path = Path("/path/to/project")
upgrade_service = UpgradeService(project_path)

# Check if upgrade needed
needs_upgrade, current, target = upgrade_service.needs_upgrade()
if needs_upgrade:
    print(f"Upgrade available: {current} → {target}")

    # Preview changes
    changes = upgrade_service.get_changes_preview()
    for change in changes:
        print(f"  - {change}")

    # Perform upgrade (with automatic backup)
    success, message = upgrade_service.perform_upgrade(backup=True)
    print(message)
```

## Configuration

### Upgradeable Components

The service defines which directories are regenerated during upgrade:

```python
UPGRADEABLE_DIRS = ["adws", ".claude", "scripts"]
UPGRADEABLE_FILES = ["config.yml"]
```

**Important**: User customizations in these directories are **overwritten**. The backup preserves them for manual restoration if needed.

### Version Detection

Projects without a `version` field in `config.yml` default to `"0.1.0"`. The service updates this field to the target version during upgrade.

## Testing

Unit tests will be created in TAREA 4. The implementation follows the testing strategy defined in the specification:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "upgrade_service"
```

### Validation Commands

All validation commands pass:

```bash
# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Design Decisions

### 1. Complete Agentic Layer Replacement
The upgrade **completely overwrites** `.claude/`, `adws/`, and `scripts/`. User customizations are lost but preserved in backup for manual restoration. This ensures templates are always in sync with the CLI version.

### 2. Mandatory Backup
When `backup=True` (default), upgrade aborts if backup creation fails. This provides a safety net for all operations.

### 3. No Automatic Rollback Command
There is no `tac-bootstrap rollback` command. Users must manually restore from `.tac-backup-{timestamp}/` if needed after confirming the upgrade.

### 4. Semantic Version Comparison
Uses `packaging.version.parse()` for proper semantic versioning (handles pre-releases, build metadata, etc.). Falls back to string comparison if parsing fails.

### 5. Reuses ScaffoldService
Upgrade leverages the existing `ScaffoldService` with `existing_repo=True` flag, ensuring consistency with initial project generation.

### 6. Manual Backup Cleanup
Backups are **not** automatically deleted. Users must remove `.tac-backup-*` directories manually after verifying the upgrade succeeded.

## Notes

### Dependencies

All required dependencies are already installed:
- `packaging` (25.0) - Semantic version comparison
- `PyYAML` - Configuration file parsing
- `rich` - Formatted console output
- `shutil`, `datetime` - Python stdlib

### Edge Cases Handled

- **Missing config.yml**: Returns `None` from `get_current_version()`
- **Missing version field**: Defaults to `"0.1.0"`
- **Malformed versions**: Falls back to no-upgrade decision
- **Downgrade prevention**: `needs_upgrade()` returns `False` if current > target
- **Upgrade failure**: Automatic restoration from backup
- **Backup failure**: Aborts upgrade when `backup=True`

### Future Tasks

- **TAREA 4**: Unit tests for UpgradeService
- **TAREA 5**: CLI command `tac-bootstrap upgrade` implementation
- **TAREA 6**: User-facing documentation for upgrade command

### Architecture Notes

The UpgradeService follows TAC Bootstrap's Domain-Driven Design architecture:

- **Application Layer** (`application/upgrade_service.py`) - Business logic for upgrades
- **Domain Layer** (uses `TACConfig` model) - Configuration validation
- **Infrastructure Layer** (uses `ScaffoldService`) - Template regeneration
- **Interface Layer** (future TAREA 5) - CLI command interface

This separation ensures testability, maintainability, and adherence to the project's architectural patterns.
