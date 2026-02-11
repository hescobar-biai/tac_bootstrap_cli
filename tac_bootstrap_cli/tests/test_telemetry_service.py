"""Tests for TelemetryService.

Comprehensive unit tests for opt-in telemetry tracking including
event tracking, error tracking, performance tracking, statistics
aggregation, opt-in/opt-out, daily log rotation, data clearing,
and configuration persistence.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tac_bootstrap.infrastructure.telemetry import TelemetryService

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def telemetry_home(tmp_path: Path) -> Path:
    """Create a temporary home directory for telemetry testing."""
    tac_dir = tmp_path / ".tac-bootstrap"
    tac_dir.mkdir(parents=True)
    return tmp_path


@pytest.fixture
def enabled_service(telemetry_home: Path) -> TelemetryService:
    """Create a TelemetryService with telemetry explicitly enabled."""
    with patch.object(Path, "home", return_value=telemetry_home):
        service = TelemetryService(enabled=True)
    return service


@pytest.fixture
def disabled_service(telemetry_home: Path) -> TelemetryService:
    """Create a TelemetryService with telemetry explicitly disabled."""
    with patch.object(Path, "home", return_value=telemetry_home):
        service = TelemetryService(enabled=False)
    return service


# ============================================================================
# TEST INITIALIZATION
# ============================================================================


class TestTelemetryServiceInit:
    """Tests for TelemetryService initialization."""

    def test_default_is_disabled(self, telemetry_home: Path):
        """Default state should be disabled when no config file exists."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService()
        assert service.enabled is False

    def test_explicit_enable_overrides_config(self, telemetry_home: Path):
        """Explicit enabled=True should override config file."""
        # Write disabled to config
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("disabled")

        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=True)
        assert service.enabled is True

    def test_explicit_disable_overrides_config(self, telemetry_home: Path):
        """Explicit enabled=False should override config file."""
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("enabled")

        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=False)
        assert service.enabled is False

    def test_reads_config_file_enabled(self, telemetry_home: Path):
        """Should read 'enabled' from config file when no explicit value."""
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("enabled")

        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService()
        assert service.enabled is True

    def test_reads_config_file_disabled(self, telemetry_home: Path):
        """Should read 'disabled' from config file."""
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("disabled")

        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService()
        assert service.enabled is False

    def test_creates_storage_dir_when_enabled(self, telemetry_home: Path):
        """Storage directory should be created when telemetry is enabled."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=True)
        assert service.storage_dir.exists()
        assert service.storage_dir.is_dir()

    def test_storage_dir_not_created_when_disabled(self, telemetry_home: Path):
        """Storage directory should NOT be created when telemetry is disabled."""
        with patch.object(Path, "home", return_value=telemetry_home):
            TelemetryService(enabled=False)
        # The .tac-bootstrap dir exists (from fixture) but telemetry/ should not
        assert not (telemetry_home / ".tac-bootstrap" / "telemetry").exists()


# ============================================================================
# TEST EVENT TRACKING
# ============================================================================


class TestTelemetryEventTracking:
    """Tests for track_event method."""

    def test_track_event_when_enabled(self, enabled_service: TelemetryService):
        """track_event should write event to daily log when enabled."""
        enabled_service.track_event("command_executed", {"command": "init"})

        # Find the log file
        log_files = list(enabled_service.storage_dir.glob("*.jsonl"))
        # Filter out errors.jsonl
        daily_logs = [f for f in log_files if f.name != "errors.jsonl"]
        assert len(daily_logs) == 1

        # Parse the event
        content = daily_logs[0].read_text().strip()
        event = json.loads(content)
        assert event["event"] == "command_executed"
        assert event["command"] == "init"
        assert "timestamp" in event

    def test_track_event_when_disabled(self, disabled_service: TelemetryService):
        """track_event should be a no-op when disabled."""
        disabled_service.track_event("command_executed", {"command": "init"})

        # No files should be created
        if disabled_service.storage_dir.exists():
            log_files = list(disabled_service.storage_dir.glob("*.jsonl"))
            assert len(log_files) == 0

    def test_track_event_without_properties(self, enabled_service: TelemetryService):
        """track_event should work with just an event name."""
        enabled_service.track_event("startup")

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) == 1

        content = daily_logs[0].read_text().strip()
        event = json.loads(content)
        assert event["event"] == "startup"
        assert "timestamp" in event

    def test_track_multiple_events(self, enabled_service: TelemetryService):
        """Multiple events should be appended to the same daily log."""
        enabled_service.track_event("event_1")
        enabled_service.track_event("event_2")
        enabled_service.track_event("event_3")

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) == 1

        lines = daily_logs[0].read_text().strip().splitlines()
        assert len(lines) == 3

        events = [json.loads(line) for line in lines]
        assert events[0]["event"] == "event_1"
        assert events[1]["event"] == "event_2"
        assert events[2]["event"] == "event_3"

    def test_track_event_timestamp_format(self, enabled_service: TelemetryService):
        """Event timestamps should be valid ISO 8601 format."""
        from datetime import datetime

        enabled_service.track_event("test_event")

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        content = daily_logs[0].read_text().strip()
        event = json.loads(content)

        # Should parse without error
        timestamp = datetime.fromisoformat(event["timestamp"])
        assert timestamp is not None


# ============================================================================
# TEST ERROR TRACKING
# ============================================================================


class TestTelemetryErrorTracking:
    """Tests for track_error method."""

    def test_track_error_when_enabled(self, enabled_service: TelemetryService):
        """track_error should write to errors.jsonl when enabled."""
        try:
            raise ValueError("test error message")
        except ValueError as e:
            enabled_service.track_error(e, {"operation": "test_op"})

        error_file = enabled_service.storage_dir / "errors.jsonl"
        assert error_file.exists()

        content = error_file.read_text().strip()
        event = json.loads(content)
        assert event["event"] == "error"
        assert event["error_type"] == "ValueError"
        assert event["operation"] == "test_op"
        assert "timestamp" in event

    def test_track_error_does_not_log_message(self, enabled_service: TelemetryService):
        """track_error should NOT log the error message (privacy)."""
        try:
            raise RuntimeError("sensitive path: /home/user/secret_project")
        except RuntimeError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        content = error_file.read_text()

        # Error message should NOT appear anywhere
        assert "sensitive" not in content
        assert "secret_project" not in content
        assert "/home/user" not in content

    def test_track_error_logs_error_type_only(self, enabled_service: TelemetryService):
        """track_error should log error type name and module only."""
        try:
            raise FileNotFoundError("some/path.txt")
        except FileNotFoundError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        content = error_file.read_text().strip()
        event = json.loads(content)

        assert event["error_type"] == "FileNotFoundError"
        assert event["error_module"] == "builtins"
        # The actual error message should not be in the event
        assert "some/path.txt" not in json.dumps(event)

    def test_track_error_when_disabled(self, disabled_service: TelemetryService):
        """track_error should be a no-op when disabled."""
        try:
            raise ValueError("test")
        except ValueError as e:
            disabled_service.track_error(e)

        if disabled_service.storage_dir.exists():
            error_file = disabled_service.storage_dir / "errors.jsonl"
            assert not error_file.exists()

    def test_track_error_without_context(self, enabled_service: TelemetryService):
        """track_error should work without context parameter."""
        try:
            raise TypeError("test")
        except TypeError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        content = error_file.read_text().strip()
        event = json.loads(content)
        assert event["error_type"] == "TypeError"


# ============================================================================
# TEST PERFORMANCE TRACKING
# ============================================================================


class TestTelemetryPerformanceTracking:
    """Tests for track_performance method."""

    def test_track_performance_when_enabled(self, enabled_service: TelemetryService):
        """track_performance should write to daily log when enabled."""
        enabled_service.track_performance("template_rendering", 567.89)

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) == 1

        content = daily_logs[0].read_text().strip()
        event = json.loads(content)
        assert event["event"] == "performance"
        assert event["operation"] == "template_rendering"
        assert event["duration_ms"] == 567.89

    def test_track_performance_when_disabled(self, disabled_service: TelemetryService):
        """track_performance should be a no-op when disabled."""
        disabled_service.track_performance("template_rendering", 567.89)

        if disabled_service.storage_dir.exists():
            log_files = list(disabled_service.storage_dir.glob("*.jsonl"))
            assert len(log_files) == 0

    def test_track_performance_rounds_duration(self, enabled_service: TelemetryService):
        """track_performance should round duration to 2 decimal places."""
        enabled_service.track_performance("scaffold_creation", 2345.6789)

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        content = daily_logs[0].read_text().strip()
        event = json.loads(content)
        assert event["duration_ms"] == 2345.68


# ============================================================================
# TEST STATISTICS AGGREGATION
# ============================================================================


class TestTelemetryStatistics:
    """Tests for get_statistics method."""

    def test_statistics_when_disabled(self, disabled_service: TelemetryService):
        """get_statistics should return disabled message when disabled."""
        stats = disabled_service.get_statistics()
        assert stats["enabled"] is False
        assert "message" in stats

    def test_statistics_empty(self, enabled_service: TelemetryService):
        """get_statistics should return zeros when no data exists."""
        stats = enabled_service.get_statistics()
        assert stats["enabled"] is True
        assert stats["total_events"] == 0
        assert stats["events_today"] == 0
        assert stats["commands"] == {}
        assert stats["errors"] == {}
        assert stats["avg_duration_ms"] == 0.0

    def test_statistics_counts_events(self, enabled_service: TelemetryService):
        """get_statistics should count total events correctly."""
        enabled_service.track_event("event_1")
        enabled_service.track_event("event_2")
        enabled_service.track_event("event_3")

        stats = enabled_service.get_statistics()
        assert stats["total_events"] == 3
        assert stats["events_today"] == 3

    def test_statistics_counts_commands(self, enabled_service: TelemetryService):
        """get_statistics should aggregate command usage."""
        enabled_service.track_event("command_executed", {"command": "init"})
        enabled_service.track_event("command_executed", {"command": "init"})
        enabled_service.track_event("command_executed", {"command": "upgrade"})

        stats = enabled_service.get_statistics()
        assert stats["commands"]["init"] == 2
        assert stats["commands"]["upgrade"] == 1

    def test_statistics_counts_errors(self, enabled_service: TelemetryService):
        """get_statistics should aggregate error types from errors.jsonl."""
        try:
            raise ValueError("err1")
        except ValueError as e:
            enabled_service.track_error(e)

        try:
            raise TypeError("err2")
        except TypeError as e:
            enabled_service.track_error(e)

        try:
            raise ValueError("err3")
        except ValueError as e:
            enabled_service.track_error(e)

        stats = enabled_service.get_statistics()
        assert stats["errors"]["ValueError"] == 2
        assert stats["errors"]["TypeError"] == 1

    def test_statistics_calculates_avg_duration(self, enabled_service: TelemetryService):
        """get_statistics should calculate average duration."""
        enabled_service.track_performance("op1", 100.0)
        enabled_service.track_performance("op2", 200.0)
        enabled_service.track_performance("op3", 300.0)

        stats = enabled_service.get_statistics()
        # Average of [100, 200, 300] = 200
        assert stats["avg_duration_ms"] == 200.0

    def test_statistics_reports_log_file_count(self, enabled_service: TelemetryService):
        """get_statistics should count log files."""
        enabled_service.track_event("test_event")

        stats = enabled_service.get_statistics()
        assert stats["log_files"] >= 1


# ============================================================================
# TEST OPT-IN / OPT-OUT
# ============================================================================


class TestTelemetryOptInOut:
    """Tests for opt_in and opt_out methods."""

    def test_opt_in_enables_telemetry(self, telemetry_home: Path):
        """opt_in should enable telemetry and write config file."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=False)
            assert service.enabled is False

            service.opt_in()
            assert service.enabled is True

        # Verify config file
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        assert config_file.exists()
        assert config_file.read_text().strip() == "enabled"

    def test_opt_out_disables_telemetry(self, telemetry_home: Path):
        """opt_out should disable telemetry and write config file."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=True)
            assert service.enabled is True

            service.opt_out()
            assert service.enabled is False

        # Verify config file
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        assert config_file.exists()
        assert config_file.read_text().strip() == "disabled"

    def test_opt_in_creates_storage_dir(self, telemetry_home: Path):
        """opt_in should create the storage directory."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=False)
            service.opt_in()

        assert service.storage_dir.exists()

    def test_opt_out_preserves_data(self, telemetry_home: Path):
        """opt_out should NOT delete existing data."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=True)
            service.track_event("before_opt_out")
            service.opt_out()

        # Data should still exist
        log_files = list(service.storage_dir.glob("*.jsonl"))
        assert len(log_files) > 0

    def test_config_persists_across_instances(self, telemetry_home: Path):
        """Config should persist across TelemetryService instances."""
        with patch.object(Path, "home", return_value=telemetry_home):
            # First instance enables
            service1 = TelemetryService()
            service1.opt_in()

            # Second instance should read enabled state
            service2 = TelemetryService()
            assert service2.enabled is True

            # Disable
            service2.opt_out()

            # Third instance should read disabled state
            service3 = TelemetryService()
            assert service3.enabled is False


# ============================================================================
# TEST FILE STORAGE AND DAILY ROTATION
# ============================================================================


class TestTelemetryFileStorage:
    """Tests for file-based storage and daily log rotation."""

    def test_daily_log_file_naming(self, enabled_service: TelemetryService):
        """Log files should be named with YYYY-MM-DD format."""
        from datetime import datetime, timezone

        enabled_service.track_event("test")

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        expected_file = enabled_service.storage_dir / f"{today}.jsonl"
        assert expected_file.exists()

    def test_events_are_jsonl_format(self, enabled_service: TelemetryService):
        """Each line in log file should be valid JSON."""
        enabled_service.track_event("event_1", {"key": "value1"})
        enabled_service.track_event("event_2", {"key": "value2"})

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) == 1

        for line in daily_logs[0].read_text().strip().splitlines():
            # Each line should be valid JSON
            parsed = json.loads(line)
            assert isinstance(parsed, dict)

    def test_errors_go_to_separate_file(self, enabled_service: TelemetryService):
        """Errors should be written to errors.jsonl, not daily logs."""
        try:
            raise ValueError("test")
        except ValueError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        assert error_file.exists()

        # Daily log should NOT contain the error
        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        for log in daily_logs:
            content = log.read_text()
            assert '"event": "error"' not in content

    def test_events_and_errors_coexist(self, enabled_service: TelemetryService):
        """Regular events and errors should coexist without interference."""
        enabled_service.track_event("normal_event")

        try:
            raise RuntimeError("test")
        except RuntimeError as e:
            enabled_service.track_error(e)

        enabled_service.track_performance("test_op", 100.0)

        # Verify daily log has 2 entries (event + performance)
        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) == 1
        lines = daily_logs[0].read_text().strip().splitlines()
        assert len(lines) == 2

        # Verify error log has 1 entry
        error_file = enabled_service.storage_dir / "errors.jsonl"
        error_lines = error_file.read_text().strip().splitlines()
        assert len(error_lines) == 1


# ============================================================================
# TEST DATA CLEARING
# ============================================================================


class TestTelemetryDataClearing:
    """Tests for clear_data method."""

    def test_clear_data_removes_all_logs(self, enabled_service: TelemetryService):
        """clear_data should remove all log files."""
        enabled_service.track_event("event_1")
        enabled_service.track_event("event_2")

        try:
            raise ValueError("test")
        except ValueError as e:
            enabled_service.track_error(e)

        # Verify files exist
        log_files = list(enabled_service.storage_dir.glob("*.jsonl"))
        assert len(log_files) > 0

        # Clear data
        files_deleted = enabled_service.clear_data()
        assert files_deleted > 0

        # Verify files are gone
        log_files = list(enabled_service.storage_dir.glob("*.jsonl"))
        assert len(log_files) == 0

    def test_clear_data_preserves_storage_dir(self, enabled_service: TelemetryService):
        """clear_data should recreate the storage directory."""
        enabled_service.track_event("event_1")
        enabled_service.clear_data()

        # Storage directory should still exist (recreated)
        assert enabled_service.storage_dir.exists()

    def test_clear_data_returns_count(self, enabled_service: TelemetryService):
        """clear_data should return the number of files deleted."""
        enabled_service.track_event("event_1")
        try:
            raise ValueError("test")
        except ValueError as e:
            enabled_service.track_error(e)

        count = enabled_service.clear_data()
        # At least 2 files: daily log + errors.jsonl
        assert count >= 2

    def test_clear_data_on_empty_dir(self, enabled_service: TelemetryService):
        """clear_data should work when no data exists."""
        count = enabled_service.clear_data()
        assert count == 0

    def test_clear_data_preserves_config(self, telemetry_home: Path):
        """clear_data should NOT affect the telemetry config file."""
        with patch.object(Path, "home", return_value=telemetry_home):
            service = TelemetryService(enabled=True)
            service.opt_in()  # Write config
            service.track_event("some_event")
            service.clear_data()

        # Config file should still exist
        config_file = telemetry_home / ".tac-bootstrap" / ".telemetry_config"
        assert config_file.exists()
        assert config_file.read_text().strip() == "enabled"


# ============================================================================
# TEST CLI INTEGRATION
# ============================================================================


class TestTelemetryCLIIntegration:
    """Tests for telemetry CLI command."""

    def test_telemetry_enable_command(self, telemetry_home: Path):
        """CLI telemetry enable command should work."""
        from typer.testing import CliRunner

        from tac_bootstrap.interfaces.cli import app

        runner = CliRunner()

        with patch.object(Path, "home", return_value=telemetry_home):
            result = runner.invoke(app, ["telemetry", "enable"])

        assert result.exit_code == 0
        assert "enabled" in result.stdout.lower()

    def test_telemetry_disable_command(self, telemetry_home: Path):
        """CLI telemetry disable command should work."""
        from typer.testing import CliRunner

        from tac_bootstrap.interfaces.cli import app

        runner = CliRunner()

        with patch.object(Path, "home", return_value=telemetry_home):
            result = runner.invoke(app, ["telemetry", "disable"])

        assert result.exit_code == 0
        assert "disabled" in result.stdout.lower()

    def test_telemetry_status_command(self, telemetry_home: Path):
        """CLI telemetry status command should work."""
        from typer.testing import CliRunner

        from tac_bootstrap.interfaces.cli import app

        runner = CliRunner()

        with patch.object(Path, "home", return_value=telemetry_home):
            result = runner.invoke(app, ["telemetry", "status"])

        assert result.exit_code == 0
        assert "status" in result.stdout.lower() or "disabled" in result.stdout.lower()

    def test_telemetry_clear_command(self, telemetry_home: Path):
        """CLI telemetry clear command should work."""
        from typer.testing import CliRunner

        from tac_bootstrap.interfaces.cli import app

        runner = CliRunner()

        with patch.object(Path, "home", return_value=telemetry_home):
            result = runner.invoke(app, ["telemetry", "clear"])

        assert result.exit_code == 0
        assert "cleared" in result.stdout.lower()

    def test_telemetry_invalid_action(self, telemetry_home: Path):
        """CLI telemetry with invalid action should fail."""
        from typer.testing import CliRunner

        from tac_bootstrap.interfaces.cli import app

        runner = CliRunner()

        with patch.object(Path, "home", return_value=telemetry_home):
            result = runner.invoke(app, ["telemetry", "invalid"])

        assert result.exit_code == 1


# ============================================================================
# TEST SCAFFOLD SERVICE INTEGRATION
# ============================================================================


class TestTelemetryScaffoldIntegration:
    """Tests for telemetry integration with ScaffoldService."""

    def test_scaffold_service_accepts_telemetry(self, enabled_service: TelemetryService):
        """ScaffoldService should accept telemetry parameter."""
        from tac_bootstrap.application.scaffold_service import ScaffoldService

        service = ScaffoldService(telemetry=enabled_service)
        assert service.telemetry is enabled_service

    def test_scaffold_service_works_without_telemetry(self):
        """ScaffoldService should work without telemetry (backward compatible)."""
        from tac_bootstrap.application.scaffold_service import ScaffoldService

        service = ScaffoldService()
        assert service.telemetry is None

    def test_build_plan_tracks_performance(self, telemetry_home: Path):
        """build_plan should track performance when telemetry is provided."""
        with patch.object(Path, "home", return_value=telemetry_home):
            telemetry = TelemetryService(enabled=True)

        from tac_bootstrap.application.scaffold_service import ScaffoldService
        from tac_bootstrap.domain.models import (
            ClaudeConfig,
            ClaudeSettings,
            CommandsSpec,
            Language,
            PackageManager,
            ProjectSpec,
            TACConfig,
        )

        config = TACConfig(
            project=ProjectSpec(
                name="test-project",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="uv run python -m app", test="uv run pytest"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-project")),
        )

        service = ScaffoldService(telemetry=telemetry)
        service.build_plan(config)

        # Check that performance event was logged
        daily_logs = [
            f for f in telemetry.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        assert len(daily_logs) >= 1

        all_events = []
        for log_file in daily_logs:
            for line in log_file.read_text().strip().splitlines():
                all_events.append(json.loads(line))

        perf_events = [
            e for e in all_events
            if e.get("event") == "performance"
            and e.get("operation") == "scaffold_plan_build"
        ]
        assert len(perf_events) == 1
        assert "duration_ms" in perf_events[0]
        assert perf_events[0]["duration_ms"] > 0

    def test_apply_plan_tracks_scaffold_event(self, telemetry_home: Path, tmp_path: Path):
        """apply_plan should track scaffold_applied event with telemetry."""
        with patch.object(Path, "home", return_value=telemetry_home):
            telemetry = TelemetryService(enabled=True)

        from tac_bootstrap.application.scaffold_service import ScaffoldService
        from tac_bootstrap.domain.models import (
            ClaudeConfig,
            ClaudeSettings,
            CommandsSpec,
            Language,
            PackageManager,
            ProjectSpec,
            TACConfig,
        )

        config = TACConfig(
            project=ProjectSpec(
                name="test-project",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="uv run python -m app", test="uv run pytest"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-project")),
        )

        service = ScaffoldService(telemetry=telemetry)
        plan = service.build_plan(config)
        output_dir = tmp_path / "test_telemetry_project"
        result = service.apply_plan(plan, output_dir, config)

        assert result.success

        # Check that scaffold_applied event was logged
        daily_logs = [
            f for f in telemetry.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]

        all_events = []
        for log_file in daily_logs:
            for line in log_file.read_text().strip().splitlines():
                all_events.append(json.loads(line))

        scaffold_events = [
            e for e in all_events
            if e.get("event") == "scaffold_applied"
        ]
        assert len(scaffold_events) == 1
        assert scaffold_events[0]["success"] is True
        assert scaffold_events[0]["files_created"] > 0
        assert scaffold_events[0]["directories_created"] > 0
        assert "duration_ms" in scaffold_events[0]


# ============================================================================
# TEST PRIVACY GUARANTEES
# ============================================================================


class TestTelemetryPrivacy:
    """Tests verifying that no sensitive data is ever logged."""

    def test_no_file_paths_in_events(self, enabled_service: TelemetryService):
        """Events should not contain file paths."""
        enabled_service.track_event("command_executed", {
            "command": "init",
            "duration_ms": 1234,
        })

        daily_logs = [
            f for f in enabled_service.storage_dir.glob("*.jsonl")
            if f.name != "errors.jsonl"
        ]
        content = daily_logs[0].read_text()
        # Should not contain path-like patterns
        assert "/home/" not in content
        assert "/Users/" not in content
        assert "C:\\" not in content

    def test_no_error_messages_in_error_tracking(self, enabled_service: TelemetryService):
        """Error tracking should not include exception messages."""
        sensitive_message = "Failed to read /home/user/secret/credentials.json"
        try:
            raise IOError(sensitive_message)
        except IOError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        content = error_file.read_text()

        assert sensitive_message not in content
        assert "credentials" not in content
        assert "/home/user" not in content
        assert "secret" not in content

    def test_error_tracking_only_stores_type(self, enabled_service: TelemetryService):
        """Error tracking should only store error type name."""
        try:
            raise PermissionError("access denied to /etc/shadow")
        except PermissionError as e:
            enabled_service.track_error(e)

        error_file = enabled_service.storage_dir / "errors.jsonl"
        event = json.loads(error_file.read_text().strip())

        # Should only have safe fields
        safe_keys = {"timestamp", "event", "error_type", "error_module"}
        assert set(event.keys()) == safe_keys
        assert event["error_type"] == "PermissionError"
        assert "/etc/shadow" not in json.dumps(event)
