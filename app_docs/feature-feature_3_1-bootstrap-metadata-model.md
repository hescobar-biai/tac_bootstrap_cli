# BootstrapMetadata Model for Generation Traceability

**ADW ID:** feature_3_1
**Date:** 2026-01-23
**Specification:** specs/issue-154-adw-feature_3_1-sdlc_planner-bootstrap-metadata-model.md

## Overview

This feature introduces a typed `BootstrapMetadata` Pydantic model that captures generation and upgrade metadata for TAC Bootstrap projects. The metadata provides an audit trail for tracking when projects were generated, what CLI version created them, when they were last upgraded, and which templates were used.

## What Was Built

- **BootstrapMetadata Model**: Comprehensive Pydantic model with 5 fields tracking generation metadata
- **TACConfig Integration**: New optional `metadata` field in the root `TACConfig` model
- **Audit Trail Foundation**: Infrastructure for tracking project lifecycle from generation through upgrades

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Added `BootstrapMetadata` model (71 new lines) and integrated into `TACConfig` as optional field

### Key Changes

1. **BootstrapMetadata Model** (line 406-471):
   - `generated_at: str` - ISO8601 timestamp of initial generation
   - `generated_by: str` - TAC Bootstrap version identifier (format: "tac-bootstrap v{version}")
   - `last_upgrade: str | None` - Optional timestamp of last upgrade (None if never upgraded)
   - `schema_version: int` - Config schema version (default: 2)
   - `template_checksums: dict[str, str]` - MD5 checksums of templates for change detection

2. **TACConfig Integration** (line 535-537):
   - Added `metadata: BootstrapMetadata | None = None` field to root config model
   - Field is optional to maintain backward compatibility with existing configs
   - Placed after existing `bootstrap: BootstrapConfig` field (note: different models for different purposes)

3. **Comprehensive Documentation**:
   - Detailed docstring explaining each field's purpose and format
   - Usage examples showing model instantiation
   - Implementation notes about timestamp format, checksum calculation, and upgrade semantics

## How to Use

### Creating Metadata During Generation

When generating a project, populate the metadata:

```python
from datetime import datetime
from tac_bootstrap.domain.models import BootstrapMetadata, TACConfig

metadata = BootstrapMetadata(
    generated_at=datetime.now().isoformat(),
    generated_by="tac-bootstrap v0.2.0",
    last_upgrade=None,  # Initial generation
    schema_version=2,
    template_checksums={
        "adw_sdlc_iso.py": "a1b2c3d4e5f6g7h8",
        "start.md": "1a2b3c4d5e6f7g8h"
    }
)

config = TACConfig(
    project=...,
    metadata=metadata
)
```

### Reading Metadata from Existing Config

```python
from tac_bootstrap.domain.models import TACConfig

config = TACConfig.model_validate(yaml_data)

if config.metadata:
    print(f"Generated: {config.metadata.generated_at}")
    print(f"Version: {config.metadata.generated_by}")
    print(f"Last upgrade: {config.metadata.last_upgrade or 'Never'}")
```

### Updating Metadata During Upgrade

```python
from datetime import datetime

if config.metadata:
    config.metadata.last_upgrade = datetime.now().isoformat()
    # Update checksums after regenerating templates
    config.metadata.template_checksums["adw_sdlc_iso.py"] = new_checksum
```

## Configuration

The `metadata` field in `config.yml` is optional and will appear like:

```yaml
metadata:
  generated_at: "2024-01-15T10:30:00.123456"
  generated_by: "tac-bootstrap v0.2.0"
  last_upgrade: "2024-02-20T14:45:00.789012"
  schema_version: 2
  template_checksums:
    adw_sdlc_iso.py: "a1b2c3d4e5f6g7h8"
    start.md: "1a2b3c4d5e6f7g8h"
```

### Template Checksums Scope

Tracks primary user-facing templates:
- `.claude/commands/*.md` - Claude slash commands
- `adws/adw_*_iso.py` - AI Developer Workflows
- `scripts/*.sh` - Utility scripts

### Version String Format

Use `importlib.metadata.version('tac-bootstrap')` with fallback to '0.1.0-dev':

```python
try:
    from importlib.metadata import version
    ver = version('tac-bootstrap')
except Exception:
    ver = '0.1.0-dev'

generated_by = f"tac-bootstrap v{ver}"
```

## Testing

Run validation commands to verify implementation:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

1. **String-based Timestamps**: Timestamps are stored as plain strings without validation. The generator is responsible for creating valid ISO8601 timestamps using `datetime.now().isoformat()`.

2. **Optional Field**: The `metadata` field is optional to maintain backward compatibility. Existing `config.yml` files without this field will continue to work.

3. **Naming Collision**: Two distinct models exist:
   - `BootstrapConfig` - Generation options (what to generate)
   - `BootstrapMetadata` - Audit trail (when/how it was generated)

4. **Checksum Implementation**: Use `hashlib.md5(file_content.encode()).hexdigest()` on full file content for template checksums.

5. **Upgrade Semantics**:
   - `last_upgrade = None` means never upgraded
   - Regeneration counts as an upgrade
   - Updates timestamp and affected template checksums

### Future Enhancements

- Add field validators for timestamp format validation
- Implement automatic checksum calculation during generation
- Create migration utilities for upgrading older configs
- Add comparison methods to detect template drift
