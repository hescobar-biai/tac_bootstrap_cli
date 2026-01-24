# Audit Trail Tests for Bootstrap Metadata

**ADW ID:** chore_3_3
**Date:** 2026-01-24
**Specification:** specs/issue-158-adw-chore_3_3-chore_planner-audit-trail-tests.md

## Overview

This chore adds comprehensive tests to verify that bootstrap metadata is correctly generated and updated in all CLI flows (init and upgrade). The tests ensure the audit trail metadata in `config.yml` maintains data integrity across the project lifecycle.

## What Was Built

- Test class `TestScaffoldServiceBootstrapMetadata` with 4 test methods
- Validation of metadata field structure and presence
- ISO8601 timestamp format verification
- Version string format validation
- Upgrade flow metadata update verification
- Enhanced scaffold_service logic to preserve metadata during upgrades

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tests/test_scaffold_service.py`: Added 141 lines of new test class with 4 comprehensive test methods
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Enhanced apply_plan() to handle both initial generation and upgrade scenarios (lines 591-608)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Cleaned up duplicate BootstrapMetadata definition
- `tac_bootstrap_cli/tac_bootstrap/templates/config/config.yml.j2`: Updated template for metadata field
- `.mcp.json` and `playwright-mcp-config.json`: Minor configuration updates
- `specs/`: Added specification and review checklist files

### Key Changes

**Enhanced Metadata Handling in ScaffoldService**
- Modified `apply_plan()` method (scaffold_service.py:591-608) to distinguish between initial generation and upgrades
- On initial generation: Creates new metadata with `last_upgrade: None`
- On upgrade: Preserves original `generated_at`, updates `generated_by` version, and sets `last_upgrade` timestamp
- Ensures metadata continuity across project lifecycle

**Comprehensive Test Coverage**
- `test_init_generates_bootstrap_metadata`: Verifies config.yml contains all required metadata fields (generated_at, generated_by, schema_version, last_upgrade)
- `test_bootstrap_metadata_has_valid_timestamp`: Validates generated_at is a parseable ISO8601 timestamp using `datetime.fromisoformat()`
- `test_bootstrap_metadata_has_correct_version`: Confirms generated_by matches expected format `tac-bootstrap v{__version__}`
- `test_upgrade_updates_last_upgrade`: Verifies last_upgrade transitions from None to valid ISO8601 timestamp after UpgradeService.perform_upgrade()

**Test Design Principles**
- Each test uses `tempfile.TemporaryDirectory()` for isolation
- Tests verify structure and format without checking timestamp reasonableness (avoids flakiness)
- Single responsibility per test method
- Follows existing test patterns from the codebase

## How to Use

### Running the Tests

Run only the new metadata tests:
```bash
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceBootstrapMetadata -v --tb=short
```

Run the full test suite to ensure no regressions:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Metadata Structure in config.yml

The metadata field is automatically generated at the top level of `config.yml`:

```yaml
metadata:
  generated_at: "2026-01-24T10:30:00.123456+00:00"
  generated_by: "tac-bootstrap v0.2.0"
  schema_version: 2
  last_upgrade: null  # Set to timestamp after first upgrade
```

After running an upgrade:
```yaml
metadata:
  generated_at: "2026-01-24T10:30:00.123456+00:00"  # Preserved
  generated_by: "tac-bootstrap v0.2.1"              # Updated
  schema_version: 2
  last_upgrade: "2026-01-24T15:45:30.789012+00:00"  # Updated
```

## Configuration

No configuration required. Metadata generation is automatic in all CLI flows.

## Testing

### Test Validation Commands

Run all validation commands to ensure zero regressions:

```bash
# Run new metadata tests
cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py::TestScaffoldServiceBootstrapMetadata -v --tb=short

# Full test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Test Coverage

The test suite verifies:
- Metadata field presence and structure
- ISO8601 timestamp format validation
- Version string format matching
- Metadata preservation during upgrades
- last_upgrade field transition from None to timestamp

## Notes

### Important Clarifications
- The metadata field name in config.yml is `metadata`, not `bootstrap` (despite the issue description using "bootstrap metadata")
- BootstrapMetadata model is defined at models.py:406-497
- The implementation uses `datetime.fromisoformat()` for timestamp parsing, which handles ISO8601 format
- Tests intentionally avoid validating timestamp reasonableness (e.g., not in future) to prevent flakiness

### Design Decisions
- Scaffold service now handles both init and upgrade flows intelligently
- Original `generated_at` timestamp is preserved across upgrades for accurate audit trail
- `generated_by` version is updated on each upgrade to track CLI version evolution
- `last_upgrade` field provides upgrade detection and debugging capabilities

### Future Considerations
- The `schema_version` field is hardcoded to 2, with versioning strategy TBD for future migrations
- Template checksums tracking is part of BootstrapMetadata but not covered in this test suite
- Metadata can be used for upgrade eligibility checks and migration strategies in future features
