"""
DoctorService - Validation and health checking for Agentic Layer setups.

This module provides comprehensive diagnostics for TAC Bootstrap generated
Agentic Layers, detecting and auto-fixing common issues:
- Missing required/optional directories (.claude, adws, specs, scripts)
- Invalid configuration files (malformed JSON/YAML)
- Non-executable hooks
- Missing essential commands
- Incomplete ADW setups

Used by the doctor command to validate project health and suggest/apply fixes.
"""

import json
import os
import stat
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, List, Optional

import yaml


class Severity(str, Enum):
    """
    Severity levels for diagnostic issues.

    Used to classify issues by their impact on functionality.
    """

    ERROR = "error"  # Must fix for functionality
    WARNING = "warning"  # Should fix for best results
    INFO = "info"  # Optional improvement


@dataclass
class Issue:
    """
    Represents a single diagnostic issue.

    Attributes:
        severity: Issue severity level
        message: Human-readable description of the issue
        suggestion: Optional suggestion for fixing the issue
        fix_fn: Optional function to auto-fix the issue
    """

    severity: Severity
    message: str
    suggestion: Optional[str] = None
    fix_fn: Optional[Callable[[Path], bool]] = None


@dataclass
class DiagnosticReport:
    """
    Result of a diagnostic check.

    Attributes:
        healthy: Flag indicating overall health (False if any ERROR exists)
        issues: List of detected issues
    """

    healthy: bool = True
    issues: List[Issue] = field(default_factory=list)

    def add_issue(self, issue: Issue) -> None:
        """
        Add an issue to the report.

        Args:
            issue: Issue to add
        """
        self.issues.append(issue)
        if issue.severity == Severity.ERROR:
            self.healthy = False


@dataclass
class FixResult:
    """
    Result of auto-fix attempts.

    Attributes:
        fixed_count: Number of successfully fixed issues
        failed_count: Number of failed fix attempts
        messages: List of result messages
    """

    fixed_count: int = 0
    failed_count: int = 0
    messages: List[str] = field(default_factory=list)


class DoctorService:
    """
    Service for diagnosing and fixing Agentic Layer setups.

    Performs comprehensive health checks on TAC Bootstrap generated projects,
    detecting missing directories, invalid configs, permission issues, etc.

    Example:
        doctor = DoctorService()
        report = doctor.diagnose(Path("/path/to/repo"))

        if not report.healthy:
            print(f"Found {len(report.issues)} issues")
            fix_result = doctor.fix(Path("/path/to/repo"), report)
            print(f"Fixed {fix_result.fixed_count} issues")
    """

    def diagnose(self, repo_path: Path) -> DiagnosticReport:
        """
        Run comprehensive diagnostics on repository.

        Args:
            repo_path: Path to repository root

        Returns:
            DiagnosticReport with all detected issues
        """
        report = DiagnosticReport()

        self._check_directory_structure(repo_path, report)
        self._check_claude_config(repo_path, report)
        self._check_commands(repo_path, report)
        self._check_hooks(repo_path, report)
        self._check_adws(repo_path, report)
        self._check_config_yml(repo_path, report)

        return report

    def fix(self, repo_path: Path, report: DiagnosticReport) -> FixResult:
        """
        Attempt to auto-fix issues in the diagnostic report.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport from diagnose()

        Returns:
            FixResult with counts and messages
        """
        result = FixResult()

        for issue in report.issues:
            if issue.fix_fn:
                try:
                    success = issue.fix_fn(repo_path)
                    if success:
                        result.fixed_count += 1
                        result.messages.append(f"✓ Fixed: {issue.message}")
                    else:
                        result.failed_count += 1
                        result.messages.append(f"✗ Failed to fix: {issue.message}")
                except Exception as e:
                    result.failed_count += 1
                    result.messages.append(f"✗ Error fixing {issue.message}: {e}")

        return result

    def _check_directory_structure(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check for required and optional directories.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        # Required directories
        required_dirs = [".claude", ".claude/commands", ".claude/hooks"]
        for dir_path in required_dirs:
            full_path = repo_path / dir_path
            if not full_path.is_dir():
                report.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        message=f"Missing required directory: {dir_path}",
                        suggestion=f"Run: mkdir -p {dir_path}",
                        fix_fn=lambda p, d=dir_path: self._fix_create_dir(p, d),
                    )
                )

        # Optional directories
        optional_dirs = {
            "adws": "ADW workflows for automated development tasks",
            "specs": "Specifications and feature documentation",
            "scripts": "Utility scripts for project automation",
        }
        for dir_path, benefit in optional_dirs.items():
            full_path = repo_path / dir_path
            if not full_path.is_dir():
                report.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        message=f"Missing optional directory: {dir_path}",
                        suggestion=f"Consider creating {dir_path}/ for {benefit}",
                        fix_fn=lambda p, d=dir_path: self._fix_create_dir(p, d),
                    )
                )

    def _check_claude_config(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check .claude/settings.json validity.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        config_path = repo_path / ".claude" / "settings.json"

        if not config_path.exists():
            report.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    message="Missing .claude/settings.json",
                    suggestion="Create settings.json with required Claude Code configuration",
                )
            )
            return

        try:
            with open(config_path, "r") as f:
                settings = json.load(f)

            if "permissions" not in settings:
                report.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        message="settings.json missing 'permissions' field",
                        suggestion="Add permissions configuration to control Claude Code access",
                    )
                )
        except json.JSONDecodeError as e:
            report.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    message=f"Invalid JSON in settings.json: {e}",
                    suggestion="Fix JSON syntax errors in .claude/settings.json",
                )
            )

    def _check_commands(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check for essential slash commands.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        commands_dir = repo_path / ".claude" / "commands"

        if not commands_dir.is_dir():
            # Already reported in directory check
            return

        # Essential commands
        essential_commands = ["prime.md", "test.md", "commit.md"]
        for cmd in essential_commands:
            cmd_path = commands_dir / cmd
            if not cmd_path.exists():
                report.add_issue(
                    Issue(
                        severity=Severity.WARNING,
                        message=f"Missing commonly used command: {cmd}",
                        suggestion=f"Consider adding .claude/commands/{cmd} for better workflow",
                    )
                )

        # Check if there's at least one command
        try:
            md_files = list(commands_dir.glob("*.md"))
            if not md_files:
                report.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        message="No command files found in .claude/commands/",
                        suggestion="Add at least one .md command file (e.g., prime.md, test.md)",
                    )
                )
        except (PermissionError, OSError):
            pass

    def _check_hooks(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check hook executability.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        hooks_dir = repo_path / ".claude" / "hooks"

        if not hooks_dir.is_dir():
            # Already reported in directory check
            return

        hook_files = ["pre_tool_use.py", "post_tool_use.py"]
        for hook in hook_files:
            hook_path = hooks_dir / hook
            if hook_path.exists():
                if not os.access(hook_path, os.X_OK):
                    report.add_issue(
                        Issue(
                            severity=Severity.WARNING,
                            message=f"Hook not executable: {hook}",
                            suggestion=f"Run: chmod +x .claude/hooks/{hook}",
                            fix_fn=lambda p, h=hook: self._fix_make_executable(p, h),
                        )
                    )

    def _check_adws(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check ADW (AI Developer Workflow) setup.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        adws_dir = repo_path / "adws"

        if not adws_dir.is_dir():
            # Optional directory, already reported if missing
            return

        # Check for adw_modules
        modules_dir = adws_dir / "adw_modules"
        if not modules_dir.is_dir():
            report.add_issue(
                Issue(
                    severity=Severity.WARNING,
                    message="Missing adws/adw_modules/ directory",
                    suggestion="Create adws/adw_modules/ for reusable ADW components",
                    fix_fn=lambda p: self._fix_create_dir(p, "adws/adw_modules"),
                )
            )

        # Check for at least one workflow
        try:
            workflows = list(adws_dir.glob("adw_*.py"))
            if not workflows:
                report.add_issue(
                    Issue(
                        severity=Severity.INFO,
                        message="No ADW workflows found",
                        suggestion=(
                            "Consider adding adws/adw_sdlc_iso.py "
                            "for automated development workflows"
                        ),
                    )
                )
        except (PermissionError, OSError):
            pass

    def _check_config_yml(self, repo_path: Path, report: DiagnosticReport) -> None:
        """
        Check config.yml validity.

        Args:
            repo_path: Path to repository root
            report: DiagnosticReport to append issues to
        """
        config_path = repo_path / "config.yml"

        if not config_path.exists():
            report.add_issue(
                Issue(
                    severity=Severity.WARNING,
                    message="Missing config.yml",
                    suggestion=(
                        "Create config.yml for idempotent regeneration and configuration management"
                    ),
                )
            )
            return

        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)

            if config is None or not config:
                report.add_issue(
                    Issue(
                        severity=Severity.ERROR,
                        message="config.yml is empty",
                        suggestion="Add project configuration to config.yml",
                    )
                )
                return

            # Check required fields
            required_fields = ["project", "commands"]
            for field in required_fields:
                if field not in config:
                    report.add_issue(
                        Issue(
                            severity=Severity.ERROR,
                            message=f"config.yml missing required field: {field}",
                            suggestion=f"Add '{field}' section to config.yml",
                        )
                    )
        except yaml.YAMLError as e:
            report.add_issue(
                Issue(
                    severity=Severity.ERROR,
                    message=f"Invalid YAML in config.yml: {e}",
                    suggestion="Fix YAML syntax errors in config.yml",
                )
            )

    def _fix_create_dir(self, repo_path: Path, dir_path: str) -> bool:
        """
        Create a missing directory.

        Args:
            repo_path: Path to repository root
            dir_path: Relative directory path to create

        Returns:
            True if successful, False otherwise
        """
        try:
            full_path = repo_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            return full_path.is_dir()
        except (PermissionError, OSError):
            return False

    def _fix_make_executable(self, repo_path: Path, hook: str) -> bool:
        """
        Make a hook file executable.

        Args:
            repo_path: Path to repository root
            hook: Hook filename (e.g., "pre_tool_use.py")

        Returns:
            True if successful, False otherwise
        """
        hook_path = repo_path / ".claude" / "hooks" / hook

        if not hook_path.exists():
            return False

        try:
            current_mode = hook_path.stat().st_mode
            new_mode = current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
            hook_path.chmod(new_mode)
            return os.access(hook_path, os.X_OK)
        except (PermissionError, OSError):
            return False
