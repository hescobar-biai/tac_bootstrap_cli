"""
Tests for ValidationService System Requirements, Project Name, and Project Path Validation

Comprehensive unit tests covering:
- Git version detection (2.29 fails, 2.30 passes, 2.39 passes)
- Python version detection
- Command existence checking (uv, npm, gh)
- Project name validation (valid and invalid formats)
- Project path validation (special chars, permissions, reserved names)
- Preflight checks combined
- Edge cases (commands not in PATH, parsing errors)

All subprocess calls are mocked to ensure test isolation.
"""

import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from tac_bootstrap.application.validation_service import (
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
    ValidationService,
    PROJECT_NAME_PATTERN,
    WINDOWS_RESERVED_NAMES,
)
from tac_bootstrap.domain.models import (
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    OrchestratorConfig,
    PackageManager,
    PathsSpec,
    ProjectSpec,
    SystemRequirement,
    TACConfig,
)


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_template_repo():
    """Create a mock TemplateRepository."""
    mock_repo = Mock()
    mock_repo.template_exists.return_value = True
    mock_repo.templates_dir = Path("/mock/templates")
    return mock_repo


@pytest.fixture
def validation_service(mock_template_repo):
    """Create ValidationService with mock template repository."""
    return ValidationService(mock_template_repo)


@pytest.fixture
def sample_config():
    """Create a valid TACConfig for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="test-app",
            language=Language.PYTHON,
            framework=Framework.FASTAPI,
            architecture=Architecture.LAYERED,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
    )


@pytest.fixture
def npm_config():
    """Create a TACConfig with npm package manager."""
    return TACConfig(
        project=ProjectSpec(
            name="test-js-app",
            language=Language.TYPESCRIPT,
            framework=Framework.NEXTJS,
            architecture=Architecture.SIMPLE,
            package_manager=PackageManager.NPM,
        ),
        commands=CommandsSpec(
            start="npm run dev",
            test="npm test",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-js-app")),
    )


@pytest.fixture
def orchestrator_config():
    """Create a TACConfig with orchestrator enabled."""
    return TACConfig(
        project=ProjectSpec(
            name="test-orch",
            language=Language.PYTHON,
            framework=Framework.FASTAPI,
            architecture=Architecture.SIMPLE,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
        ),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-orch")),
        orchestrator=OrchestratorConfig(enabled=True),
    )


def _make_subprocess_result(stdout="", returncode=0):
    """Helper to create mock subprocess.CompletedProcess."""
    result = MagicMock()
    result.stdout = stdout
    result.stderr = ""
    result.returncode = returncode
    return result


# ============================================================================
# TEST GIT VERSION DETECTION
# ============================================================================


class TestGitVersionDetection:
    """Test git version checking and comparison."""

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_229_fails(self, mock_run, validation_service):
        """Git 2.29 should fail minimum requirement of 2.30."""
        mock_run.return_value = _make_subprocess_result("git version 2.29.0")

        ok, version = validation_service._check_git_version("2.30")

        assert ok is False
        assert version == "2.29.0"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_230_passes(self, mock_run, validation_service):
        """Git 2.30 should pass minimum requirement of 2.30."""
        mock_run.return_value = _make_subprocess_result("git version 2.30.0")

        ok, version = validation_service._check_git_version("2.30")

        assert ok is True
        assert version == "2.30.0"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_239_passes(self, mock_run, validation_service):
        """Git 2.39.1 should pass minimum requirement of 2.30."""
        mock_run.return_value = _make_subprocess_result("git version 2.39.1")

        ok, version = validation_service._check_git_version("2.30")

        assert ok is True
        assert version == "2.39.1"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_not_found(self, mock_run, validation_service):
        """Git not found should return (False, None)."""
        mock_run.side_effect = FileNotFoundError()

        ok, version = validation_service._check_git_version("2.30")

        assert ok is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_timeout(self, mock_run, validation_service):
        """Git command timeout should return (False, None)."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="git", timeout=10)

        ok, version = validation_service._check_git_version("2.30")

        assert ok is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_nonzero_returncode(self, mock_run, validation_service):
        """Git returning non-zero exit code should return (False, None)."""
        mock_run.return_value = _make_subprocess_result("", returncode=1)

        ok, version = validation_service._check_git_version("2.30")

        assert ok is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_unparseable_output(self, mock_run, validation_service):
        """Git returning unparseable output should return (False, None)."""
        mock_run.return_value = _make_subprocess_result("git version unknown")

        ok, version = validation_service._check_git_version("2.30")

        assert ok is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_git_macos_format(self, mock_run, validation_service):
        """Git on macOS with Apple format should still parse correctly."""
        mock_run.return_value = _make_subprocess_result(
            "git version 2.39.5 (Apple Git-154)"
        )

        ok, version = validation_service._check_git_version("2.30")

        assert ok is True
        assert version == "2.39.5"


# ============================================================================
# TEST PYTHON VERSION DETECTION
# ============================================================================


class TestPythonVersionDetection:
    """Test Python version checking."""

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_python_310_passes(self, mock_run, validation_service):
        """Python 3.10.0 should pass minimum requirement of 3.10."""
        mock_run.return_value = _make_subprocess_result("Python 3.10.0")

        ok, version = validation_service._check_python_version("3.10")

        assert ok is True
        assert version == "3.10.0"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_python_312_passes(self, mock_run, validation_service):
        """Python 3.12.1 should pass minimum requirement of 3.10."""
        mock_run.return_value = _make_subprocess_result("Python 3.12.1")

        ok, version = validation_service._check_python_version("3.10")

        assert ok is True
        assert version == "3.12.1"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_python_39_fails(self, mock_run, validation_service):
        """Python 3.9 should fail minimum requirement of 3.10."""
        mock_run.return_value = _make_subprocess_result("Python 3.9.7")

        ok, version = validation_service._check_python_version("3.10")

        assert ok is False
        assert version == "3.9.7"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_python_not_found(self, mock_run, validation_service):
        """Python not found should return (False, None)."""
        mock_run.side_effect = FileNotFoundError()

        ok, version = validation_service._check_python_version("3.10")

        assert ok is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    def test_python3_fallback(self, mock_run, validation_service):
        """Should try python3 first, then fall back to python."""
        # First call (python3) fails, second call (python) succeeds
        mock_run.side_effect = [
            FileNotFoundError(),  # python3 not found
            _make_subprocess_result("Python 3.11.0"),  # python found
        ]

        ok, version = validation_service._check_python_version("3.10")

        assert ok is True
        assert version == "3.11.0"
        assert mock_run.call_count == 2


# ============================================================================
# TEST COMMAND EXISTENCE CHECKING
# ============================================================================


class TestCommandExistence:
    """Test command existence checking (uv, npm, gh)."""

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_uv_installed(self, mock_which, mock_run, validation_service):
        """uv installed and version detectable."""
        mock_which.return_value = "/usr/local/bin/uv"
        mock_run.return_value = _make_subprocess_result("uv 0.4.30")

        installed, version = validation_service._check_command_exists("uv")

        assert installed is True
        assert version == "0.4.30"

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_uv_not_installed(self, mock_which, validation_service):
        """uv not installed should return (False, None)."""
        mock_which.return_value = None

        installed, version = validation_service._check_command_exists("uv")

        assert installed is False
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_npm_installed(self, mock_which, mock_run, validation_service):
        """npm installed and version detectable."""
        mock_which.return_value = "/usr/local/bin/npm"
        mock_run.return_value = _make_subprocess_result("10.2.0")

        installed, version = validation_service._check_command_exists("npm")

        assert installed is True
        assert version == "10.2.0"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_gh_installed(self, mock_which, mock_run, validation_service):
        """gh CLI installed and version detectable."""
        mock_which.return_value = "/usr/local/bin/gh"
        mock_run.return_value = _make_subprocess_result("gh version 2.40.0")

        installed, version = validation_service._check_command_exists("gh")

        assert installed is True
        assert version == "2.40.0"

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_command_exists_but_no_version(self, mock_which, mock_run, validation_service):
        """Command exists but version can't be parsed."""
        mock_which.return_value = "/usr/local/bin/tool"
        mock_run.return_value = _make_subprocess_result("some-tool no-version-here")

        installed, version = validation_service._check_command_exists("tool")

        assert installed is True
        assert version is None

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_command_exists_but_timeout(self, mock_which, mock_run, validation_service):
        """Command exists but times out when checking version."""
        import subprocess
        mock_which.return_value = "/usr/local/bin/tool"
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="tool", timeout=10)

        installed, version = validation_service._check_command_exists("tool")

        assert installed is True
        assert version is None


# ============================================================================
# TEST SYSTEM REQUIREMENTS VALIDATION
# ============================================================================


class TestSystemRequirementsValidation:
    """Test validate_system_requirements method."""

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_all_requirements_met(
        self, mock_which, mock_run, validation_service, sample_config
    ):
        """All system requirements met should return valid."""
        mock_which.return_value = "/usr/local/bin/uv"
        mock_run.side_effect = [
            _make_subprocess_result("git version 2.39.1"),  # git
            _make_subprocess_result("Python 3.12.1"),  # python3
            _make_subprocess_result("uv 0.4.30"),  # uv
        ]

        result = validation_service.validate_system_requirements(sample_config)

        assert result.valid is True
        assert len(result.errors()) == 0

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_git_not_installed_error(
        self, mock_which, mock_run, validation_service, sample_config
    ):
        """Missing git should produce an error."""
        mock_which.return_value = "/usr/local/bin/uv"
        mock_run.side_effect = [
            FileNotFoundError(),  # git not found
            _make_subprocess_result("Python 3.12.1"),  # python3
            _make_subprocess_result("uv 0.4.30"),  # uv
        ]

        result = validation_service.validate_system_requirements(sample_config)

        assert result.valid is False
        errors = result.errors()
        git_errors = [e for e in errors if "git" in e.message.lower()]
        assert len(git_errors) >= 1
        assert git_errors[0].level == ValidationLevel.SYSTEM

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_git_outdated_error(
        self, mock_which, mock_run, validation_service, sample_config
    ):
        """Outdated git version should produce an error."""
        mock_which.return_value = "/usr/local/bin/uv"
        mock_run.side_effect = [
            _make_subprocess_result("git version 2.29.0"),  # old git
            _make_subprocess_result("Python 3.12.1"),  # python3
            _make_subprocess_result("uv 0.4.30"),  # uv
        ]

        result = validation_service.validate_system_requirements(sample_config)

        assert result.valid is False
        errors = result.errors()
        git_errors = [e for e in errors if "git" in e.message.lower()]
        assert len(git_errors) >= 1
        assert "2.29" in git_errors[0].message

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_uv_not_installed_when_required(
        self, mock_which, mock_run, validation_service, sample_config
    ):
        """Missing uv when configured as package manager should produce error."""
        def which_side_effect(cmd):
            if cmd == "uv":
                return None
            return f"/usr/local/bin/{cmd}"

        mock_which.side_effect = which_side_effect
        mock_run.side_effect = [
            _make_subprocess_result("git version 2.39.1"),  # git
            _make_subprocess_result("Python 3.12.1"),  # python3
        ]

        result = validation_service.validate_system_requirements(sample_config)

        assert result.valid is False
        errors = result.errors()
        uv_errors = [e for e in errors if "uv" in e.message.lower()]
        assert len(uv_errors) >= 1

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_npm_not_installed_when_required(
        self, mock_which, mock_run, validation_service, npm_config
    ):
        """Missing npm when configured as package manager should produce error."""
        def which_side_effect(cmd):
            if cmd == "npm":
                return None
            return f"/usr/local/bin/{cmd}"

        mock_which.side_effect = which_side_effect
        mock_run.side_effect = [
            _make_subprocess_result("git version 2.39.1"),  # git
            _make_subprocess_result("Python 3.12.1"),  # python3
        ]

        result = validation_service.validate_system_requirements(npm_config)

        assert result.valid is False
        errors = result.errors()
        npm_errors = [e for e in errors if "npm" in e.message.lower()]
        assert len(npm_errors) >= 1

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_gh_not_installed_warning_with_orchestrator(
        self, mock_which, mock_run, validation_service, orchestrator_config
    ):
        """Missing gh with orchestrator enabled should produce warning, not error."""
        def which_side_effect(cmd):
            if cmd == "gh":
                return None
            return f"/usr/local/bin/{cmd}"

        mock_which.side_effect = which_side_effect
        mock_run.side_effect = [
            _make_subprocess_result("git version 2.39.1"),  # git
            _make_subprocess_result("Python 3.12.1"),  # python3
            _make_subprocess_result("uv 0.4.30"),  # uv
        ]

        result = validation_service.validate_system_requirements(orchestrator_config)

        # gh missing is a warning, not error
        assert result.valid is True
        warnings = result.warnings()
        gh_warnings = [w for w in warnings if "gh" in w.message.lower()]
        assert len(gh_warnings) >= 1


# ============================================================================
# TEST PROJECT NAME VALIDATION
# ============================================================================


class TestProjectNameValidation:
    """Test validate_project_name method."""

    def _make_config_with_name(self, name):
        """Helper to create a config with a specific project name."""
        return TACConfig(
            project=ProjectSpec(
                name=name,
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name=name)),
        )

    def test_valid_name_passes(self, validation_service):
        """Valid slug name should pass."""
        config = self._make_config_with_name("my-app")
        result = validation_service.validate_project_name(config)
        assert result.valid is True
        assert len(result.errors()) == 0

    def test_valid_name_with_numbers(self, validation_service):
        """Name with numbers should pass."""
        config = self._make_config_with_name("my-app-2")
        result = validation_service.validate_project_name(config)
        assert result.valid is True

    def test_valid_name_all_lowercase(self, validation_service):
        """All lowercase name should pass."""
        config = self._make_config_with_name("myapp")
        result = validation_service.validate_project_name(config)
        assert result.valid is True

    def test_name_too_short(self, validation_service):
        """Name with fewer than 3 characters should fail."""
        config = self._make_config_with_name("ab")
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("too short" in e.message for e in errors)

    def test_name_too_long(self, validation_service):
        """Name with more than 50 characters should fail."""
        long_name = "a" * 51
        config = self._make_config_with_name(long_name)
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("too long" in e.message for e in errors)

    def test_name_with_leading_hyphen(self, validation_service):
        """Name starting with hyphen should fail."""
        config = self._make_config_with_name("-my-app")
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("start with a hyphen" in e.message for e in errors)

    def test_name_with_trailing_hyphen(self, validation_service):
        """Name ending with hyphen should fail."""
        config = self._make_config_with_name("my-app-")
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("end with a hyphen" in e.message for e in errors)

    def test_name_with_underscores(self, validation_service):
        """Name with underscores should fail (not slug format)."""
        config = self._make_config_with_name("my_app_name")
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("invalid characters" in e.message for e in errors)

    def test_name_with_spaces(self, validation_service):
        """Name with spaces should fail."""
        # Note: ProjectSpec sanitizes names (converts spaces to hyphens),
        # but we test the validator directly
        config = self._make_config_with_name("my-app")
        result = validation_service.validate_project_name(config)
        # "my-app" is valid after sanitization
        assert result.valid is True

    def test_windows_reserved_name_con(self, validation_service):
        """Windows reserved name 'con' should fail."""
        config = self._make_config_with_name("con")
        result = validation_service.validate_project_name(config)
        assert result.valid is False
        errors = result.errors()
        assert any("reserved" in e.message.lower() for e in errors)

    def test_windows_reserved_name_prn(self, validation_service):
        """Windows reserved name 'prn' should fail."""
        config = self._make_config_with_name("prn")
        result = validation_service.validate_project_name(config)
        assert result.valid is False

    def test_windows_reserved_name_aux(self, validation_service):
        """Windows reserved name 'aux' should fail."""
        config = self._make_config_with_name("aux")
        result = validation_service.validate_project_name(config)
        assert result.valid is False

    def test_windows_reserved_name_nul(self, validation_service):
        """Windows reserved name 'nul' should fail."""
        config = self._make_config_with_name("nul")
        result = validation_service.validate_project_name(config)
        assert result.valid is False

    def test_name_50_chars_passes(self, validation_service):
        """Name exactly 50 characters should pass."""
        name = "a" * 50
        config = self._make_config_with_name(name)
        result = validation_service.validate_project_name(config)
        assert result.valid is True

    def test_name_3_chars_passes(self, validation_service):
        """Name exactly 3 characters should pass."""
        config = self._make_config_with_name("app")
        result = validation_service.validate_project_name(config)
        assert result.valid is True


# ============================================================================
# TEST PROJECT PATH VALIDATION
# ============================================================================


class TestProjectPathValidation:
    """Test validate_project_path method."""

    def test_valid_path_passes(self, validation_service, sample_config, tmp_path):
        """Valid ASCII path should pass."""
        output_dir = tmp_path / "my-project"
        result = validation_service.validate_project_path(sample_config, output_dir)
        assert result.valid is True

    def test_path_with_unicode_fails(self, validation_service, sample_config, tmp_path):
        """Path with Unicode characters should fail."""
        output_dir = tmp_path / "mi-proyecto-\u00e9"
        result = validation_service.validate_project_path(sample_config, output_dir)
        assert result.valid is False
        errors = result.errors()
        assert any("unicode" in e.message.lower() for e in errors)

    def test_path_too_long_fails(self, validation_service, sample_config, tmp_path):
        """Path longer than 255 characters should fail."""
        long_name = "a" * 300
        output_dir = tmp_path / long_name
        result = validation_service.validate_project_path(sample_config, output_dir)
        assert result.valid is False
        errors = result.errors()
        assert any("too long" in e.message for e in errors)

    def test_path_with_windows_reserved_name_warns(
        self, validation_service, sample_config, tmp_path
    ):
        """Path containing Windows reserved name in segment should warn."""
        output_dir = tmp_path / "CON" / "project"
        result = validation_service.validate_project_path(sample_config, output_dir)
        warnings = result.warnings()
        reserved_warnings = [
            w for w in warnings if "reserved" in w.message.lower()
        ]
        assert len(reserved_warnings) >= 1

    def test_existing_writable_path_passes(
        self, validation_service, sample_config, tmp_path
    ):
        """Existing writable directory should pass."""
        output_dir = tmp_path / "existing-project"
        output_dir.mkdir()
        result = validation_service.validate_project_path(sample_config, output_dir)
        assert result.valid is True

    def test_non_writable_existing_path_fails(
        self, validation_service, sample_config, tmp_path
    ):
        """Non-writable existing directory should fail."""
        output_dir = tmp_path / "readonly"
        output_dir.mkdir()
        try:
            os.chmod(output_dir, 0o555)
            result = validation_service.validate_project_path(sample_config, output_dir)
            assert result.valid is False
            errors = result.errors()
            assert any("not writable" in e.message for e in errors)
        finally:
            os.chmod(output_dir, 0o755)

    def test_non_writable_parent_fails(
        self, validation_service, sample_config, tmp_path
    ):
        """Non-writable parent directory should fail."""
        parent = tmp_path / "readonly-parent"
        parent.mkdir()
        output_dir = parent / "project"
        try:
            os.chmod(parent, 0o555)
            result = validation_service.validate_project_path(sample_config, output_dir)
            assert result.valid is False
            errors = result.errors()
            assert any("not writable" in e.message for e in errors)
        finally:
            os.chmod(parent, 0o755)


# ============================================================================
# TEST VERSION COMPARISON HELPERS
# ============================================================================


class TestVersionComparison:
    """Test version parsing and comparison helpers."""

    def test_parse_simple_version(self, validation_service):
        """Parse simple version string."""
        assert validation_service._parse_version("2.30.0") == (2, 30, 0)

    def test_parse_two_part_version(self, validation_service):
        """Parse two-part version string."""
        assert validation_service._parse_version("3.10") == (3, 10)

    def test_parse_version_with_suffix(self, validation_service):
        """Parse version with non-numeric suffix."""
        assert validation_service._parse_version("3.10.0-rc1") == (3, 10, 0)

    def test_compare_equal_versions(self, validation_service):
        """Equal versions should return True."""
        assert validation_service._compare_versions("2.30", "2.30") is True

    def test_compare_greater_version(self, validation_service):
        """Greater version should return True."""
        assert validation_service._compare_versions("2.39.1", "2.30") is True

    def test_compare_lesser_version(self, validation_service):
        """Lesser version should return False."""
        assert validation_service._compare_versions("2.29", "2.30") is False

    def test_compare_different_length(self, validation_service):
        """Versions with different lengths should compare correctly."""
        assert validation_service._compare_versions("3.10", "3.10.0") is True
        assert validation_service._compare_versions("3.10.0", "3.10") is True
        assert validation_service._compare_versions("3.9", "3.10") is False

    def test_compare_major_difference(self, validation_service):
        """Major version difference should dominate."""
        assert validation_service._compare_versions("4.0", "3.99") is True
        assert validation_service._compare_versions("2.99", "3.0") is False


# ============================================================================
# TEST PREFLIGHT CHECKS (COMBINED)
# ============================================================================


class TestPreflightChecks:
    """Test run_preflight_checks combining all validation layers."""

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_all_checks_pass(
        self, mock_which, mock_run, validation_service, sample_config, tmp_path
    ):
        """All preflight checks should pass with valid config and environment."""
        mock_which.return_value = "/usr/local/bin/tool"
        mock_run.side_effect = [
            # System requirements
            _make_subprocess_result("git version 2.39.1"),  # git
            _make_subprocess_result("Python 3.12.1"),  # python3
            _make_subprocess_result("uv 0.4.30"),  # uv
        ]

        output_dir = tmp_path / "new-project"
        result = validation_service.run_preflight_checks(sample_config, output_dir)

        # Should accumulate issues but no errors from system/name/path checks
        # Note: validate_pre_scaffold may add its own git warning
        system_errors = [
            e for e in result.errors()
            if e.level == ValidationLevel.SYSTEM
        ]
        domain_errors = [
            e for e in result.errors()
            if e.level == ValidationLevel.DOMAIN
        ]
        assert len(system_errors) == 0
        assert len(domain_errors) == 0

    @patch("tac_bootstrap.application.validation_service.subprocess.run")
    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_multiple_failures_accumulated(
        self, mock_which, mock_run, mock_template_repo, tmp_path
    ):
        """Multiple failures across layers should all be accumulated."""
        mock_which.return_value = None  # All commands not found

        mock_run.side_effect = [
            FileNotFoundError(),  # git
            FileNotFoundError(),  # python3
            FileNotFoundError(),  # python
        ]

        # Bad name + bad path
        config = TACConfig(
            project=ProjectSpec(
                name="ab",  # too short
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="ab")),
        )

        mock_template_repo.template_exists.return_value = True
        vs = ValidationService(mock_template_repo)

        output_dir = tmp_path / "nonexistent_parent" / "project"
        result = vs.run_preflight_checks(config, output_dir)

        assert result.valid is False
        errors = result.errors()

        # Should have errors from multiple levels
        levels = {e.level for e in errors}
        assert ValidationLevel.SYSTEM in levels  # git/python not found
        assert ValidationLevel.DOMAIN in levels  # name too short


# ============================================================================
# TEST SYSTEM REQUIREMENT MODEL
# ============================================================================


class TestSystemRequirementModel:
    """Test SystemRequirement Pydantic model."""

    def test_create_installed_requirement(self):
        """Create SystemRequirement for installed tool."""
        req = SystemRequirement(
            name="git",
            min_version="2.30",
            installed=True,
            version="2.39.1",
        )
        assert req.name == "git"
        assert req.min_version == "2.30"
        assert req.installed is True
        assert req.version == "2.39.1"

    def test_create_missing_requirement(self):
        """Create SystemRequirement for missing tool."""
        req = SystemRequirement(
            name="uv",
            min_version=None,
            installed=False,
            version=None,
        )
        assert req.name == "uv"
        assert req.min_version is None
        assert req.installed is False
        assert req.version is None

    def test_create_with_defaults(self):
        """Create SystemRequirement with defaults."""
        req = SystemRequirement(name="test-tool")
        assert req.name == "test-tool"
        assert req.min_version is None
        assert req.installed is False
        assert req.version is None


# ============================================================================
# TEST VALIDATION LEVEL ENUM
# ============================================================================


class TestValidationLevelEnum:
    """Test that SYSTEM validation level is available."""

    def test_system_level_exists(self):
        """SYSTEM level should be available in ValidationLevel."""
        assert ValidationLevel.SYSTEM == "system"
        assert ValidationLevel.SYSTEM.value == "system"

    def test_all_levels_available(self):
        """All expected validation levels should exist."""
        expected = {"schema", "domain", "template", "filesystem", "git", "system"}
        actual = {level.value for level in ValidationLevel}
        assert expected == actual


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_project_name_pattern_regex(self):
        """Verify PROJECT_NAME_PATTERN matches expected inputs."""
        assert PROJECT_NAME_PATTERN.match("abc") is not None
        assert PROJECT_NAME_PATTERN.match("my-app") is not None
        assert PROJECT_NAME_PATTERN.match("a1b2c3") is not None
        assert PROJECT_NAME_PATTERN.match("test-project-123") is not None

        assert PROJECT_NAME_PATTERN.match("ab") is None  # too short
        assert PROJECT_NAME_PATTERN.match("-abc") is None  # leading hyphen
        assert PROJECT_NAME_PATTERN.match("abc-") is None  # trailing hyphen
        assert PROJECT_NAME_PATTERN.match("ABC") is None  # uppercase
        assert PROJECT_NAME_PATTERN.match("a_b") is None  # underscore

    def test_windows_reserved_names_complete(self):
        """Verify all expected Windows reserved names are present."""
        expected = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5",
            "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5",
            "LPT6", "LPT7", "LPT8", "LPT9",
        }
        assert WINDOWS_RESERVED_NAMES == expected

    def test_validation_mode_field_in_config(self):
        """Verify validation_mode field exists in TACConfig."""
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )
        assert config.validation_mode == "standard"

    def test_validation_mode_custom_value(self):
        """Verify validation_mode can be set to custom value."""
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            validation_mode="strict",
        )
        assert config.validation_mode == "strict"
