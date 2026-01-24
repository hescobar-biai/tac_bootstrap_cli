# Bootstrap Metadata Registration in Scaffold

**ADW ID:** feature_3_2
**Date:** 2026-01-23
**Specification:** specs/issue-156-adw-feature_3_2-sdlc_planner-register-metadata-scaffold.md

## Overview

This feature adds automatic bootstrap metadata registration to the scaffold generation process. When TAC Bootstrap generates or updates a project, it now records timestamp, CLI version, and schema version information in config.yml for audit trail, traceability, and future upgrade support.

## What Was Built

- Bootstrap metadata domain model (`BootstrapMetadata`) with generation audit trail
- Automatic metadata population in `ScaffoldService.apply_plan()` before template rendering
- Template updates to render metadata section in generated config.yml files
- UTC ISO8601 timestamp tracking with timezone awareness
- Version fallback mechanism for graceful handling of missing version info

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py:405-434` - Added `BootstrapMetadata` Pydantic model with fields:
  - `generated_at`: ISO8601 UTC timestamp of when project was generated
  - `generated_by`: TAC Bootstrap CLI version string (e.g., "tac-bootstrap v0.2.2")
  - `schema_version`: Config schema version for future migrations (hardcoded to 2)
  - `last_upgrade`: Optional ISO8601 UTC timestamp of last upgrade (None on initial generation)

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py:496-499` - Added `metadata` field to `TACConfig`:
  - Type: `BootstrapMetadata | None`
  - Default: `None` for backward compatibility
  - Description: "Bootstrap metadata for generation audit trail"

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:575-596` - Modified `apply_plan()` to register metadata:
  - Import `datetime` and `timezone` for UTC timestamp generation
  - Import `__version__` from `tac_bootstrap` with fallback to "unknown"
  - Create `BootstrapMetadata` instance before template rendering
  - Assign metadata to `config.metadata` for template context

- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2:110-119` - Added metadata section to config template:
  - Conditional rendering with `{% if config.metadata %}`
  - Renders `generated_at`, `generated_by`, `schema_version`
  - Conditionally renders `last_upgrade` only if present
  - Uses YAML string quoting for timestamp values

### Key Changes

- **Automatic Metadata Population**: Metadata is created and registered automatically before any template rendering, ensuring all generated config.yml files include audit trail information
- **Backward Compatibility**: Template uses conditional rendering (`{% if config.metadata %}`) to avoid breaking older projects without metadata
- **UTC Timestamps**: Uses `datetime.now(timezone.utc).isoformat()` for consistent, timezone-aware ISO8601 timestamps
- **Graceful Fallback**: If `__version__` import fails, uses "unknown" as version string instead of crashing
- **Future-Proof Schema Versioning**: Includes `schema_version` field (currently hardcoded to 2) for future config migration support

## How to Use

Metadata registration happens automatically during project generation. No user action required.

### During Project Initialization

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap init /path/to/project --project-name myproject --language python --package-manager uv --interactive=false
```

The generated `config.yml` will contain:

```yaml
# TAC Bootstrap Metadata (auto-generated)
metadata:
  generated_at: "2026-01-23T10:30:00.123456+00:00"
  generated_by: "tac-bootstrap v0.2.2"
  schema_version: 2
```

### During Add-Agentic Operation

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic /path/to/existing-repo
```

Same metadata section is added to `config.yml` in existing repositories.

## Configuration

No configuration options. Metadata is automatically generated with:
- Current UTC timestamp
- CLI version from `tac_bootstrap.__version__`
- Schema version 2 (hardcoded)
- `last_upgrade` set to `None` (populated only by future upgrade command)

## Testing

### Manual Verification

```bash
# Generate test project
cd tac_bootstrap_cli && uv run tac-bootstrap init /tmp/test-metadata --project-name test --language python --package-manager uv --interactive=false

# Verify metadata in config.yml
cat /tmp/test-metadata/config.yml | grep -A 5 "metadata:"

# Cleanup
rm -rf /tmp/test-metadata
```

### Unit Tests

Existing tests in `test_scaffold_service.py` validate metadata presence after `apply_plan()` execution.

```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v -k "apply_plan"
```

### Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Notes

- This feature is foundational for the future `tac-bootstrap upgrade` command (FASE 4), which will use metadata to detect project version and perform selective upgrades
- `schema_version=2` is hardcoded; versioning strategy will be defined in future work
- `last_upgrade` field is a placeholder for the upgrade command and remains `None` on initial generation
- Metadata is named "metadata" in YAML (not "bootstrap") to avoid confusion with the existing "bootstrap" section for project options
- The implementation ensures zero regressions - all existing tests pass without modification

## Related Files

- Specification: `/Volumes/MAc1/Celes/tac_bootstrap/trees/feature_3_2/specs/issue-156-adw-feature_3_2-sdlc_planner-register-metadata-scaffold.md`
- Domain Models: `tac_bootstrap_cli/tac_bootstrap/domain/models.py:405-434,496-499`
- Scaffold Service: `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:575-596`
- Config Template: `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2:110-119`
