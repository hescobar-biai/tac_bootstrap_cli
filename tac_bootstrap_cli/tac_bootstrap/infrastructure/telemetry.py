"""
IDK: telemetry-service, usage-tracking, privacy-first, event-logging, performance-metrics
Responsibility: Provides opt-in anonymous usage tracking with local file-based storage
Invariants: Disabled by default, never logs sensitive data (paths, credentials, secrets),
            daily log rotation, all operations are no-ops when disabled
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


class TelemetryService:
    """
    IDK: telemetry-core, event-tracking, error-tracking, performance-tracking
    Responsibility: Opt-in usage tracking service with privacy-first design
    Invariants: All tracking methods are no-ops when disabled, no sensitive data is logged,
                storage uses daily-rotated JSONL files in ~/.tac-bootstrap/telemetry/
    """

    def __init__(self, enabled: Optional[bool] = None) -> None:
        """Initialize telemetry service.

        Args:
            enabled: Explicit override for telemetry state.
                     None = auto-detect from config file.
                     True/False = explicit override (ignores config).
        """
        self.storage_dir = Path.home() / ".tac-bootstrap" / "telemetry"
        self._config_file = Path.home() / ".tac-bootstrap" / ".telemetry_config"

        # Determine if enabled (create storage dir only if enabled)
        self.enabled = self._is_telemetry_enabled(enabled)

        if self.enabled:
            self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _is_telemetry_enabled(self, explicit: Optional[bool]) -> bool:
        """Check if telemetry is enabled.

        Priority:
        1. Explicit parameter (if not None)
        2. Config file (~/.tac-bootstrap/.telemetry_config)
        3. Default: disabled (False)

        Args:
            explicit: Explicit override, or None to auto-detect

        Returns:
            True if telemetry is enabled, False otherwise
        """
        if explicit is not None:
            return explicit

        if self._config_file.exists():
            try:
                return self._config_file.read_text().strip().lower() == "enabled"
            except OSError:
                return False

        # Default: disabled
        return False

    def track_event(self, event_name: str, properties: Optional[Dict[str, Any]] = None) -> None:
        """Track a CLI event (only if enabled).

        Events are appended to a daily JSONL log file. Each event includes
        a UTC timestamp and the event name.

        SAFE to log: event names, durations, counts, settings (architecture, framework)
        NEVER logs: file paths, project names, credentials, exception messages

        Args:
            event_name: Name of the event (e.g., "command_executed", "scaffold_generated")
            properties: Optional dict of safe-to-log properties

        Examples:
            track_event("command_executed", {"command": "init", "duration_ms": 1234})
            track_event("scaffold_generated", {"template_count": 150, "file_count": 234})
            track_event("validation_run", {"error_count": 0, "warning_count": 2})
        """
        if not self.enabled:
            return

        event: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event_name,
        }
        if properties:
            event.update(properties)

        self._append_to_log(event)

    def track_error(
        self, error: Exception, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Track an anonymized error (only if enabled).

        Logs ONLY the error type (class name) and module, never the error
        message, stack trace, file paths, or any sensitive information.

        Args:
            error: The exception to track (only type name is logged)
            context: Optional dict of safe-to-log context (e.g., {"operation": "build_plan"})
        """
        if not self.enabled:
            return

        event: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "error",
            "error_type": type(error).__name__,
            "error_module": type(error).__module__,
        }
        if context:
            event.update(context)

        # Write to separate errors.jsonl for analysis
        self._append_to_error_log(event)

    def track_performance(self, operation: str, duration_ms: float) -> None:
        """Track operation timing (only if enabled).

        Args:
            operation: Name of the operation (e.g., "template_rendering", "scaffold_creation")
            duration_ms: Duration in milliseconds

        Examples:
            track_performance("template_rendering", 567.0)
            track_performance("scaffold_creation", 2345.0)
        """
        if not self.enabled:
            return

        event: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "performance",
            "operation": operation,
            "duration_ms": round(duration_ms, 2),
        }
        self._append_to_log(event)

    def get_statistics(self) -> Dict[str, Any]:
        """Get aggregated statistics (safe to share).

        Scans all daily log files and the errors log to produce
        aggregate statistics about telemetry events.

        Returns:
            Dict with keys:
                enabled: bool
                total_events: int
                events_today: int
                commands: dict mapping command name to count
                errors: dict mapping error type to count
                avg_duration_ms: float (average of all performance events)
                log_files: int (number of daily log files)
        """
        if not self.enabled:
            return {"enabled": False, "message": "Telemetry disabled"}

        stats = self._load_statistics()
        return {
            "enabled": True,
            **stats,
        }

    def opt_in(self) -> None:
        """Enable telemetry tracking.

        Writes "enabled" to the config file and sets the internal state.
        Creates the storage directory if it does not exist.
        """
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text("enabled")
        self.enabled = True
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def opt_out(self) -> None:
        """Disable telemetry tracking.

        Writes "disabled" to the config file and sets the internal state.
        Does NOT delete existing data; use clear_data() for that.
        """
        self._config_file.parent.mkdir(parents=True, exist_ok=True)
        self._config_file.write_text("disabled")
        self.enabled = False

    def clear_data(self) -> int:
        """Delete all collected telemetry data.

        Removes and recreates the storage directory. The config file
        is preserved (telemetry stays enabled/disabled).

        Returns:
            Number of files deleted
        """
        files_deleted = 0

        if self.storage_dir.exists():
            # Count files before deletion
            for item in self.storage_dir.iterdir():
                if item.is_file():
                    files_deleted += 1
            shutil.rmtree(self.storage_dir)

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        return files_deleted

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    def _append_to_log(self, event: Dict[str, Any]) -> None:
        """Append event to daily log file (JSONL format).

        File naming convention: YYYY-MM-DD.jsonl (UTC date).

        Args:
            event: Event dict to serialize and append
        """
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_file = self.storage_dir / f"{today}.jsonl"

        try:
            with open(log_file, "a", encoding="utf-8") as f:
                json.dump(event, f, ensure_ascii=False)
                f.write("\n")
        except OSError:
            # Silently fail - telemetry should never break the CLI
            pass

    def _append_to_error_log(self, event: Dict[str, Any]) -> None:
        """Append error event to errors.jsonl (separate from daily logs).

        Args:
            event: Error event dict to serialize and append
        """
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        error_file = self.storage_dir / "errors.jsonl"

        try:
            with open(error_file, "a", encoding="utf-8") as f:
                json.dump(event, f, ensure_ascii=False)
                f.write("\n")
        except OSError:
            # Silently fail - telemetry should never break the CLI
            pass

    def _load_statistics(self) -> Dict[str, Any]:
        """Load and aggregate statistics from all log files.

        Scans all .jsonl files in the storage directory (except errors.jsonl)
        and aggregates event counts, command usage, error types, and durations.

        Returns:
            Dict with aggregated statistics
        """
        total_events = 0
        events_today = 0
        commands: Dict[str, int] = {}
        errors: Dict[str, int] = {}
        durations: list[float] = []
        log_file_count = 0

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        if not self.storage_dir.exists():
            return {
                "total_events": 0,
                "events_today": 0,
                "commands": {},
                "errors": {},
                "avg_duration_ms": 0.0,
                "log_files": 0,
            }

        for log_file in sorted(self.storage_dir.glob("*.jsonl")):
            if log_file.name == "errors.jsonl":
                # Process errors separately
                self._count_errors_from_file(log_file, errors)
                continue

            log_file_count += 1
            is_today = log_file.stem == today

            try:
                for line in log_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                        total_events += 1

                        if is_today:
                            events_today += 1

                        # Count commands
                        if event.get("event") == "command_executed":
                            cmd = event.get("command", "unknown")
                            commands[cmd] = commands.get(cmd, 0) + 1

                        # Track durations
                        if "duration_ms" in event:
                            try:
                                durations.append(float(event["duration_ms"]))
                            except (ValueError, TypeError):
                                pass

                    except json.JSONDecodeError:
                        # Skip malformed lines
                        pass
            except OSError:
                # Skip unreadable files
                pass

        avg_duration = sum(durations) / len(durations) if durations else 0.0

        return {
            "total_events": total_events,
            "events_today": events_today,
            "commands": commands,
            "errors": errors,
            "avg_duration_ms": round(avg_duration, 2),
            "log_files": log_file_count,
        }

    def _count_errors_from_file(
        self, error_file: Path, errors: Dict[str, int]
    ) -> None:
        """Count error types from the errors.jsonl file.

        Args:
            error_file: Path to errors.jsonl
            errors: Dict to accumulate error type counts into
        """
        try:
            for line in error_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                    err_type = event.get("error_type", "Unknown")
                    errors[err_type] = errors.get(err_type, 0) + 1
                except json.JSONDecodeError:
                    pass
        except OSError:
            pass
