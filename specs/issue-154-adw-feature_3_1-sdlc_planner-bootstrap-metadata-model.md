# Feature: BootstrapMetadata Model for Generation Traceability

## Metadata
issue_number: `154`
adw_id: `feature_3_1`
issue_json: `{"number":154,"title":"Tarea 3.1: Modelo BootstrapMetadata","body":"/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_3_1\n\n***Tipo**: feature\n**Ganancia**: Modelo tipado para la metadata de generacion. Previene datos inconsistentes en config.yml.\n\n**Instrucciones para el agente**:\n\n1. Modificar `tac_bootstrap_cli/tac_bootstrap/domain/models.py`\n2. Agregar modelo:\n   ```python\n   class BootstrapMetadata(BaseModel):\n       generated_at: str  # ISO8601 timestamp\n       generated_by: str  # \"tac-bootstrap v{version}\"\n       last_upgrade: str | None = None  # ISO8601 timestamp\n       schema_version: int = 2\n       template_checksums: dict[str, str] = {}  # {template_name: md5}\n   ```\n3. Agregar campo `bootstrap: BootstrapMetadata | None = None` al modelo `TACConfig`\n\n**Criterios de aceptacion**:\n- TACConfig acepta seccion bootstrap opcional\n- Timestamps son ISO8601 validos\n- Modelo es serializable a YAML\n\n# FASE 3: Audit Trail y Metadata\n\n**Objetivo**: Registrar metadata de generacion en config.yml para trazabilidad.\n\n**Ganancia de la fase**: Saber exactamente cuando se genero el proyecto, con que version del CLI, y cuando fue la ultima actualizacion. Util para upgrades y debugging.\n\n"}`

## Feature Description

This feature introduces a typed `BootstrapMetadata` model that captures generation and upgrade metadata for TAC Bootstrap projects. The metadata tracks when a project was generated, what version of the CLI created it, when it was last upgraded, and checksums of the templates used. This provides an audit trail for generated projects, making it easier to track changes, perform upgrades, and debug issues.

The metadata is stored as an optional section in `config.yml` and is fully serializable using Pydantic's YAML serialization.

## User Story

As a developer using TAC Bootstrap CLI
I want to track when my project was generated and with which version of the CLI
So that I can make informed decisions about upgrades, understand what templates were used, and have a clear audit trail of generation history

## Problem Statement

Currently, generated projects have no built-in mechanism to track:
- When they were initially generated
- What version of TAC Bootstrap created them
- When they were last upgraded
- What templates were used during generation

This lack of metadata makes it difficult to:
- Know which CLI version generated a project
- Determine if a project needs upgrading
- Track template changes over time
- Debug issues related to generation or upgrades

## Solution Statement

We introduce a `BootstrapMetadata` Pydantic model that captures:
1. **Generation timestamp** - ISO8601 formatted string indicating when the project was created
2. **Generator version** - The TAC Bootstrap version that created the project (format: "tac-bootstrap v{version}")
3. **Last upgrade timestamp** - Optional ISO8601 timestamp for the last upgrade operation (None if never upgraded)
4. **Schema version** - Integer indicating the config schema version (hardcoded default: 2)
5. **Template checksums** - Dictionary mapping template names to their MD5 checksums for change detection

This metadata is added as an optional `bootstrap` field in the `TACConfig` root model. The implementation uses:
- Simple string types for timestamps (no validation initially)
- `importlib.metadata.version()` for version retrieval with fallback to '0.1.0-dev'
- MD5 checksums via `hashlib.md5()` for primary templates (.claude/commands/*.md, adws/adw_*_iso.py, scripts/*.sh)
- Pydantic's default serialization for YAML compatibility

## Relevant Files

Files that require modification:

- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Add `BootstrapMetadata` model and integrate into `TACConfig`

Files needed for reference:

- `tac_bootstrap_cli/tac_bootstrap/__init__.py` - Contains `__version__` constant used for versioning
- `tac_bootstrap_cli/pyproject.toml` - Package metadata for version information

### New Files

No new files are created. This is a pure model enhancement.

## Implementation Plan

### Phase 1: Foundation
1. Review existing `TACConfig` model structure in models.py:835
2. Understand how Pydantic models serialize to YAML
3. Verify `__version__` is available from `tac_bootstrap/__init__.py`

### Phase 2: Core Implementation
1. Define `BootstrapMetadata` Pydantic model with all required fields
2. Add comprehensive docstring explaining each field's purpose and format
3. Set appropriate default values and type annotations
4. Integrate `bootstrap` field into `TACConfig` as optional

### Phase 3: Integration
1. Ensure YAML serialization works correctly with the new model
2. Verify model can be deserialized from YAML back to Python objects
3. Validate that the optional field doesn't break existing configs

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Review Existing Code Structure
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` to understand current model patterns
- Read `tac_bootstrap_cli/tac_bootstrap/__init__.py` to confirm `__version__` availability
- Review how other models use type hints and defaults

### Task 2: Implement BootstrapMetadata Model
- Add `BootstrapMetadata` class after line 405 (after `BootstrapConfig` model)
- Define fields with proper type annotations:
  - `generated_at: str` - ISO8601 timestamp string
  - `generated_by: str` - Generator identifier (e.g., "tac-bootstrap v0.2.0")
  - `last_upgrade: str | None = None` - Optional upgrade timestamp
  - `schema_version: int = 2` - Config schema version
  - `template_checksums: dict[str, str] = {}` - Template name to MD5 hash mapping
- Add comprehensive docstring explaining:
  - Purpose of the model (audit trail and generation metadata)
  - Each field's purpose and expected format
  - Usage examples and notes about timestamp format, version string format, and checksums

### Task 3: Integrate into TACConfig
- Add `bootstrap: BootstrapMetadata | None = None` field to `TACConfig` class around line 466
- Place it after the existing `bootstrap: BootstrapConfig` field (note: there are two distinct models - `BootstrapConfig` for generation options and `BootstrapMetadata` for audit trail)
- Add field description: "Bootstrap generation metadata for audit trail"
- Ensure the field is optional to maintain backward compatibility

### Task 4: Validation and Testing
- Run unit tests: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run type checking: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run linting: `cd tac_bootstrap_cli && uv run ruff check .`
- Verify smoke test: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests

No new unit tests are required initially since this is a data model addition. However, future tests should verify:

1. **Model Instantiation**
   - Create `BootstrapMetadata` with all fields
   - Create with minimal fields (using defaults)
   - Verify default values are correctly set

2. **YAML Serialization**
   - Serialize model to dict/YAML
   - Deserialize from YAML back to model
   - Verify round-trip consistency

3. **Integration with TACConfig**
   - Create `TACConfig` with `bootstrap` field
   - Create `TACConfig` without `bootstrap` field (should be None)
   - Verify serialization includes/excludes bootstrap appropriately

### Edge Cases

1. **Empty template_checksums dict** - Should serialize as empty dict
2. **None for last_upgrade** - Should serialize as null/None in YAML
3. **Long version strings** - Should handle dev versions like "0.1.0-dev+git.abc123"
4. **Special characters in timestamps** - ISO8601 format with colons, hyphens, T separator

## Acceptance Criteria

1. ✅ `BootstrapMetadata` model exists with all specified fields
2. ✅ `generated_at` field is of type `str` for ISO8601 timestamps
3. ✅ `generated_by` field is of type `str` for version identifier
4. ✅ `last_upgrade` field is optional (`str | None`) with default None
5. ✅ `schema_version` field has default value of 2
6. ✅ `template_checksums` field has default value of empty dict
7. ✅ `TACConfig` has optional `bootstrap` field of type `BootstrapMetadata | None`
8. ✅ Model is serializable to YAML (uses Pydantic defaults)
9. ✅ Model is deserializable from YAML
10. ✅ All validation commands pass with zero regressions

## Validation Commands

Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Auto-Resolved Clarifications Summary

The following design decisions were pre-resolved:

1. **Version String Format**: Use `importlib.metadata.version('tac-bootstrap')` with fallback to '0.1.0-dev'. Format as "tac-bootstrap v{version}"

2. **Template Checksums Scope**: Track only primary user-facing templates:
   - `.claude/commands/*.md`
   - `adws/adw_*_iso.py`
   - `scripts/*.sh`

3. **Timestamp Validation**: Store as plain strings without validation. Generator controls these fields. Use `datetime.now().isoformat()` when generating.

4. **last_upgrade Semantics**:
   - `None` = never upgraded
   - ISO8601 string = last upgrade timestamp
   - Regeneration counts as an upgrade

5. **Checksum Implementation**: Use `hashlib.md5(file_content.encode()).hexdigest()` on full file content

6. **Schema Version**: Hardcoded default of 2, but accepts any integer from YAML for forward/backward compatibility

7. **YAML Serialization**: Use Pydantic's default string serialization, no custom serializers needed

8. **Field Placement**: Add `bootstrap` as top-level field in `TACConfig` after existing fields

### Implementation Notes

- The model is intentionally simple - no validation logic for timestamps or version strings
- This keeps the initial implementation focused on structure, not enforcement
- Future iterations can add validators if needed
- The optional nature of the field ensures backward compatibility with existing configs
- Naming collision: `BootstrapConfig` (generation options) vs `BootstrapMetadata` (audit trail) - both exist but serve different purposes
