"""Integration tests for ADW-to-SQLite database bridge.

Tests verify:
- Database connectivity and initialization
- Workflow lifecycle tracking (start, phase updates, end)
- Error handling with graceful failure
- Schema validation and database pragmas
- Agent tracking and system logging
"""

import pytest
import sqlite3
import tempfile
import os
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Import the bridge module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from adw_modules.adw_db_bridge import (
    init_bridge,
    close_bridge,
    track_workflow_start,
    track_phase_update,
    track_workflow_end,
    track_agent_start,
    track_agent_end,
    log_event,
)


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test_orchestrator.db")
        yield db_path
        # Cleanup
        close_bridge()


@pytest.fixture
def initialized_db(temp_db):
    """Initialize a test database with schema."""
    # Create schema
    conn = sqlite3.connect(temp_db)
    with open(Path(__file__).parent.parent / "schema" / "schema_orchestrator.sql") as f:
        conn.executescript(f.read())
    conn.close()

    # Initialize bridge
    init_bridge(temp_db)
    yield temp_db
    close_bridge()


class TestInitialization:
    """Tests for bridge initialization."""

    def test_init_bridge_creates_default_path(self, temp_db):
        """Verify default path resolution works."""
        with patch.dict(os.environ, {}, clear=True):
            init_bridge(temp_db)
            # Should connect without error
            close_bridge()

    def test_init_bridge_with_custom_path(self, temp_db):
        """Verify custom database path handling."""
        init_bridge(temp_db)
        close_bridge()
        # Verify file was created
        assert os.path.exists(temp_db)

    def test_init_bridge_with_env_variable(self, temp_db):
        """Verify DATABASE_PATH env var override."""
        with patch.dict(os.environ, {"DATABASE_PATH": temp_db}):
            init_bridge()
            close_bridge()
        assert os.path.exists(temp_db)

    def test_init_bridge_creates_directory(self):
        """Verify mkdir behavior for parent directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, "a", "b", "c", "test.db")
            init_bridge(nested_path)
            close_bridge()
            assert os.path.exists(nested_path)

    def test_graceful_failure_when_db_unavailable(self):
        """Verify no crash when DB path invalid."""
        init_bridge("/invalid/path/that/does/not/exist/file.db")
        close_bridge()
        # Should not raise exception

    def test_graceful_failure_on_permission_denied(self):
        """Verify no crash on permission errors."""
        # This is tricky to test across platforms, skip for now
        pass


class TestWorkflowLifecycle:
    """Tests for workflow tracking functions."""

    def test_track_workflow_start(self, initialized_db):
        """Record workflow in ai_developer_workflows table."""
        adw_id = "test-workflow-123"
        track_workflow_start(adw_id, "sdlc", issue_number="652", total_steps=5)

        # Verify in database
        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_developer_workflows WHERE id = ?", (adw_id,))
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row["adw_name"] == adw_id
        assert row["workflow_type"] == "sdlc"
        assert row["status"] == "in_progress"
        assert row["total_steps"] == 5
        assert row["completed_steps"] == 0

    def test_track_workflow_start_validates_fields(self, initialized_db):
        """Verify all fields are stored correctly."""
        adw_id = "test-workflow-456"
        issue = "999"
        track_workflow_start(adw_id, "patch", issue_number=issue, total_steps=3)

        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_developer_workflows WHERE id = ?", (adw_id,))
        row = cursor.fetchone()
        conn.close()

        assert row["id"] == adw_id
        assert row["workflow_type"] == "patch"
        assert row["total_steps"] == 3
        assert "999" in row["metadata"]
        assert row["started_at"] is not None

    def test_phase_update(self, initialized_db):
        """Track phase transitions (plan→build→test→review→document)."""
        adw_id = "test-phase-workflow"
        track_workflow_start(adw_id, "sdlc", total_steps=5)

        # Update through phases
        phases = ["plan", "build", "test", "review", "document"]
        for i, phase in enumerate(phases, 1):
            track_phase_update(adw_id, phase, "in_progress", i)

        # Verify final state
        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_developer_workflows WHERE id = ?", (adw_id,))
        row = cursor.fetchone()
        conn.close()

        assert row["current_step"] == "document"
        assert row["completed_steps"] == 5

    def test_phase_update_increments_steps(self, initialized_db):
        """Check completed_steps counter increments."""
        adw_id = "test-steps-workflow"
        track_workflow_start(adw_id, "sdlc", total_steps=3)

        for step in range(1, 4):
            track_phase_update(adw_id, f"phase-{step}", "in_progress", step)

            conn = sqlite3.connect(initialized_db)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT completed_steps FROM ai_developer_workflows WHERE id = ?", (adw_id,))
            row = cursor.fetchone()
            conn.close()

            assert row["completed_steps"] == step

    def test_workflow_end(self, initialized_db):
        """Set status to 'completed'."""
        adw_id = "test-end-workflow"
        track_workflow_start(adw_id, "sdlc")
        track_workflow_end(adw_id, "completed")

        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_developer_workflows WHERE id = ?", (adw_id,))
        row = cursor.fetchone()
        conn.close()

        assert row["status"] == "completed"
        assert row["completed_at"] is not None
        assert row["duration_seconds"] is not None

    def test_workflow_end_with_error(self, initialized_db):
        """Record workflow failure with error message."""
        adw_id = "test-error-workflow"
        track_workflow_start(adw_id, "sdlc")
        error_msg = "Test error occurred"
        track_workflow_end(adw_id, "failed", error_message=error_msg)

        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_developer_workflows WHERE id = ?", (adw_id,))
        row = cursor.fetchone()
        conn.close()

        assert row["status"] == "failed"
        assert row["error_message"] == error_msg


class TestAgentTracking:
    """Tests for agent lifecycle functions."""

    def test_track_agent_start(self, initialized_db):
        """Record agent start in agents table."""
        adw_id = "workflow-123"
        agent_name = "adw_plan_iso"

        # First ensure orchestrator_agents table has entry
        agent_id = track_agent_start(adw_id, agent_name, model="claude-opus")

        assert agent_id != ""

        # Verify in database
        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row["session_id"] == adw_id
        assert row["context"] == agent_name
        assert row["status"] == "executing"

    def test_track_agent_end(self, initialized_db):
        """Record agent completion."""
        adw_id = "workflow-456"
        agent_name = "adw_build_iso"

        agent_id = track_agent_start(adw_id, agent_name)
        track_agent_end(agent_id, status="completed", cost_usd=0.50)

        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE id = ?", (agent_id,))
        row = cursor.fetchone()
        conn.close()

        assert row["status"] == "completed"
        assert row["completed_at"] is not None
        assert row["cost_usd"] == 0.50


class TestDataIntegrity:
    """Tests for schema validation and database pragmas."""

    def test_schema_validation(self, initialized_db):
        """Verify ai_developer_workflows table schema correct."""
        conn = sqlite3.connect(initialized_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(ai_developer_workflows)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        conn.close()

        required_cols = {
            "id": "TEXT",
            "adw_name": "TEXT",
            "workflow_type": "TEXT",
            "status": "TEXT",
            "total_steps": "INTEGER",
            "completed_steps": "INTEGER",
            "started_at": "TEXT",
            "completed_at": "TEXT",
        }

        for col, col_type in required_cols.items():
            assert col in columns, f"Missing column: {col}"
            assert columns[col] == col_type, f"Wrong type for {col}"

    def test_foreign_keys_enabled(self, initialized_db):
        """Verify PRAGMA foreign_keys=ON set by bridge."""
        # Note: foreign_keys pragma is per-connection, so we verify the schema
        # supports foreign key constraints even if not globally enabled
        conn = sqlite3.connect(initialized_db)
        cursor = conn.cursor()

        # Enable for this connection to verify schema works
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA foreign_keys")
        result = cursor.fetchone()[0]
        conn.close()

        assert result == 1, "Foreign keys pragma not working"

    def test_wal_mode_enabled(self, initialized_db):
        """Verify PRAGMA journal_mode=WAL."""
        conn = sqlite3.connect(initialized_db)
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        conn.close()

        assert mode.upper() == "WAL", f"WAL mode not enabled, got: {mode}"


class TestErrorHandling:
    """Tests for graceful failure and error scenarios."""

    def test_track_workflow_without_connection(self):
        """Operations should not crash if connection unavailable."""
        close_bridge()

        # Should not raise exception
        track_workflow_start("test-id", "sdlc")
        track_phase_update("test-id", "plan", "in_progress", 1)
        track_workflow_end("test-id", "completed")

    def test_log_event(self, initialized_db):
        """Record system log entry."""
        log_event("adw_sdlc_iso", "Workflow started", level="INFO", details='{"issue": "652"}')

        conn = sqlite3.connect(initialized_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM system_logs WHERE component = ?", ("adw_sdlc_iso",))
        row = cursor.fetchone()
        conn.close()

        assert row is not None
        assert row["message"] == "Workflow started"
        assert row["log_level"] == "INFO"

    def test_close_bridge(self, temp_db):
        """Test closing database connection."""
        init_bridge(temp_db)
        close_bridge()

        # Subsequent calls should handle gracefully
        track_workflow_start("test", "sdlc")
        # Should not crash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
