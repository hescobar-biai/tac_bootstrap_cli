# Chore: Test ADW-to-SQLite Bridge & Document Orchestrator Integration

## Metadata
issue_number: `652`
adw_id: `4848fdf1`
issue_json: `{"number": 652, "title": "Test de orquestador", "body": "ve al readme y agrega la final orquestador ok"}`

## Chore Description

Add comprehensive pytest-based tests for the ADW-to-SQLite bridge (`adw_db_bridge.py`) and update `adws/README.md` with a new 'Orchestrator Integration' section. Tests must verify database connectivity, workflow state tracking (tracking functions), and error handling when database is unavailable.

## Relevant Files

### Existing Core Files
- `adws/adw_modules/adw_db_bridge.py` (282 lines) - Bridge implementation with graceful failure
- `adws/adw_modules/orch_database_models.py` - Pydantic models for orchestrator tables
- `adws/schema/schema_orchestrator.sql` - Database schema (ai_developer_workflows table)
- `adws/README.md` - Main README to update with Orchestrator Integration section
- `adws/adw_sdlc_iso.py` - Integrated bridge usage example
- `adws/adw_sdlc_zte_iso.py` - Another bridge integration example

### New Files Required
- `adws/tests/test_adw_db_bridge.py` - Integration tests for adw_db_bridge
- Update section in `adws/README.md` - Orchestrator Integration documentation

## Step by Step Tasks

### Task 1: Create test directory structure
- Create `adws/tests/` directory if it doesn't exist
- Create `adws/tests/__init__.py` for package detection
- Create `adws/tests/fixtures/` for test fixtures
- Create `adws/tests/fixtures/test_orchestrator.db` or use in-memory SQLite for tests

### Task 2: Write integration tests for adw_db_bridge.py
Create `adws/tests/test_adw_db_bridge.py` with pytest tests covering:
- **Initialization tests**:
  - `test_init_bridge_creates_default_path()` - Verify default path resolution
  - `test_init_bridge_with_custom_path()` - Custom database path handling
  - `test_init_bridge_with_env_variable()` - DATABASE_PATH env var
  - `test_init_bridge_creates_directory()` - mkdir behavior

- **Workflow lifecycle tests**:
  - `test_track_workflow_start()` - Record workflow in ai_developer_workflows table
  - `test_track_workflow_start_validates_fields()` - Verify all fields stored
  - `test_phase_update()` - Track phase transitions (plan→build→test→review→document)
  - `test_phase_update_increments_steps()` - Check completed_steps counter
  - `test_workflow_end()` - Set status to 'completed'

- **Error handling tests**:
  - `test_graceful_failure_when_db_unavailable()` - No crash when DB path invalid
  - `test_graceful_failure_on_permission_denied()` - No crash on permission errors
  - `test_graceful_failure_on_table_not_found()` - Missing table doesn't crash

- **Data integrity tests**:
  - `test_schema_validation()` - ai_developer_workflows table schema correct
  - `test_foreign_keys_enabled()` - PRAGMA foreign_keys=ON verified
  - `test_wal_mode_enabled()` - PRAGMA journal_mode=WAL verified

### Task 3: Update adws/README.md with Orchestrator Integration section
Add new section after "ADW Isolated Workflow Scripts" with:
- Overview of ADW-to-SQLite bridge
- How workflow state is tracked (workflow lifecycle)
- Database connection architecture (sync bridge, WAL mode)
- Graceful failure guarantees
- Monitoring workflow progress in orchestrator UI
- Example of accessing orchestrator data

### Task 4: Validation & Tests
Execute validation commands:
- `cd adws && python -m pytest tests/test_adw_db_bridge.py -v` - Run bridge tests
- `cd adws && python -m pytest tests/ --tb=short` - All tests pass
- Verify adws/README.md renders correctly in markdown
- Run smoke test: `uv run adws/adw_plan_iso.py --help` (verify nothing breaks)

## Validation Commands

```bash
# Run integration tests for adw_db_bridge
cd adws && python -m pytest tests/test_adw_db_bridge.py -v --tb=short

# Run all tests in adws/tests/
cd adws && python -m pytest tests/ -v --tb=short

# Verify README markdown syntax
cd adws && python -m markdown README.md > /dev/null && echo "✓ Markdown valid"

# Smoke test to ensure ADW still works
uv run adws/adw_plan_iso.py --help

# Check for any import errors
python -c "from adws.adw_modules.adw_db_bridge import init_bridge, close_bridge, track_workflow_start, phase_update, workflow_end" && echo "✓ Imports valid"
```

## Notes

- **Bridge Design**: `adw_db_bridge.py` uses plain `sqlite3` (sync) not `aiosqlite` (async) to avoid mismatch with subprocess-based ADWs. All functions have try/except to ensure graceful failure.
- **Database Path**: Default is `{project_root}/data/orchestrator.db`, can be overridden via `DATABASE_PATH` env var or parameter
- **WAL Mode**: Enables concurrent readers/writers - essential for dashboard live updates while workflows write
- **Table**: `ai_developer_workflows` tracks: id (adw_id), workflow_type, status, total_steps, completed_steps, timestamps, metadata
- **Integration**: Bridge already integrated into `adw_sdlc_iso.py`, `adw_sdlc_zte_iso.py`, `adw_ship_iso.py` via commit 5a83cad
- **Test Framework**: Use pytest with fixtures for in-memory SQLite to avoid database file conflicts
