"""
Tests for ValidationService

Comprehensive unit tests for multi-layer validation service including:
- Framework-language compatibility
- Framework-architecture compatibility
- Template validation
- Filesystem validation
- Git validation
- Multiple error accumulation
"""

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from tac_bootstrap.application.validation_service import (
    ValidationIssue,
    ValidationLevel,
    ValidationResult,
    ValidationService,
)
from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType
from tac_bootstrap.domain.models import (
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    PackageManager,
    ProjectSpec,
    TACConfig,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_template_repo():
    """Create a mock TemplateRepository."""
    mock_repo = Mock()
    # By default, templates exist
    mock_repo.template_exists.return_value = True
    mock_repo.templates_dir = Path("/mock/templates")
    return mock_repo


@pytest.fixture
def validation_service(mock_template_repo):
    """Create ValidationService with mock template repository."""
    return ValidationService(mock_template_repo)


@pytest.fixture
def sample_valid_config():
    """Create a valid TACConfig (FastAPI + Python + Layered)."""
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


# ============================================================================
# TEST FRAMEWORK-LANGUAGE COMPATIBILITY
# ============================================================================


class TestFrameworkLanguageCompatibility:
    """Test framework-language compatibility validation."""

    def test_compatible_framework_language_passes(self, validation_service, sample_valid_config):
        """Test that compatible framework + language passes validation."""
        result = validation_service.validate_config(sample_valid_config)

        # Filter domain issues only
        domain_errors = [
            i
            for i in result.errors()
            if i.level == ValidationLevel.DOMAIN and "not compatible" in i.message.lower()
        ]
        assert len(domain_errors) == 0

    def test_incompatible_framework_language_fails(self, validation_service):
        """Test that incompatible framework + language fails validation."""
        # FastAPI only works with Python, not JavaScript
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.JAVASCRIPT,
                framework=Framework.FASTAPI,
                architecture=Architecture.SIMPLE,
                package_manager=PackageManager.NPM,
            ),
            commands=CommandsSpec(start="npm start", test="npm test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        result = validation_service.validate_config(config)

        assert result.valid is False
        errors = result.errors()
        assert len(errors) >= 1

        # Find the framework-language error
        lang_errors = [e for e in errors if "not compatible" in e.message]
        assert len(lang_errors) >= 1

        error = lang_errors[0]
        assert error.level == ValidationLevel.DOMAIN
        assert "fastapi" in error.message.lower()
        assert "javascript" in error.message.lower()
        assert error.suggestion is not None
        assert "python" in error.suggestion.lower()

    def test_multiple_valid_combinations(self, validation_service):
        """Test multiple valid framework-language combinations."""
        valid_combinations = [
            (Framework.FASTAPI, Language.PYTHON),
            (Framework.DJANGO, Language.PYTHON),
            (Framework.EXPRESS, Language.TYPESCRIPT),
            (Framework.EXPRESS, Language.JAVASCRIPT),
            (Framework.NESTJS, Language.TYPESCRIPT),
            (Framework.GIN, Language.GO),
            (Framework.AXUM, Language.RUST),
            (Framework.SPRING, Language.JAVA),
        ]

        for framework, language in valid_combinations:
            config = TACConfig(
                project=ProjectSpec(
                    name="test-app",
                    language=language,
                    framework=framework,
                    architecture=Architecture.SIMPLE,
                    # Will be invalid but we're testing framework-language only
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="test", test="test"),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            )

            result = validation_service.validate_config(config)

            # Check no framework-language compatibility errors
            lang_errors = [
                e
                for e in result.errors()
                if e.level == ValidationLevel.DOMAIN
                and "not compatible" in e.message.lower()
                and "language" in e.message.lower()
            ]
            assert len(lang_errors) == 0, f"Failed for {framework.value} + {language.value}"

    def test_multiple_invalid_combinations(self, validation_service):
        """Test multiple invalid framework-language combinations."""
        invalid_combinations = [
            (Framework.FASTAPI, Language.JAVASCRIPT),
            (Framework.DJANGO, Language.GO),
            (Framework.NESTJS, Language.PYTHON),
            (Framework.GIN, Language.PYTHON),
            (Framework.AXUM, Language.JAVA),
        ]

        for framework, language in invalid_combinations:
            config = TACConfig(
                project=ProjectSpec(
                    name="test-app",
                    language=language,
                    framework=framework,
                    architecture=Architecture.SIMPLE,
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="test", test="test"),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            )

            result = validation_service.validate_config(config)

            # Should have framework-language compatibility error
            lang_errors = [
                e
                for e in result.errors()
                if e.level == ValidationLevel.DOMAIN and "not compatible" in e.message.lower()
            ]
            assert len(lang_errors) >= 1, f"Should fail for {framework.value} + {language.value}"

    def test_framework_none_accepts_all_languages(self, validation_service):
        """Test that Framework.NONE accepts all languages."""
        languages = [
            Language.PYTHON,
            Language.TYPESCRIPT,
            Language.JAVASCRIPT,
            Language.GO,
            Language.RUST,
            Language.JAVA,
        ]

        for language in languages:
            config = TACConfig(
                project=ProjectSpec(
                    name="test-app",
                    language=language,
                    framework=Framework.NONE,
                    architecture=Architecture.SIMPLE,
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="test", test="test"),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            )

            result = validation_service.validate_config(config)

            # Check no framework-language compatibility errors
            lang_errors = [
                e
                for e in result.errors()
                if e.level == ValidationLevel.DOMAIN
                and "not compatible" in e.message.lower()
                and "language" in e.message.lower()
            ]
            assert len(lang_errors) == 0, f"Framework.NONE should accept {language.value}"


# ============================================================================
# TEST FRAMEWORK-ARCHITECTURE COMPATIBILITY
# ============================================================================


class TestFrameworkArchitectureCompatibility:
    """Test framework-architecture compatibility validation."""

    def test_compatible_framework_architecture_passes(
        self, validation_service, sample_valid_config
    ):
        """Test that compatible framework + architecture passes validation."""
        # FastAPI + Layered is valid
        result = validation_service.validate_config(sample_valid_config)

        arch_errors = [
            e
            for e in result.errors()
            if e.level == ValidationLevel.DOMAIN and "does not support" in e.message.lower()
        ]
        assert len(arch_errors) == 0

    def test_incompatible_framework_architecture_fails(self, validation_service):
        """Test that incompatible framework + architecture fails validation."""
        # Django does NOT support DDD architecture
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.PYTHON,
                framework=Framework.DJANGO,
                architecture=Architecture.DDD,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        result = validation_service.validate_config(config)

        assert result.valid is False
        errors = result.errors()

        arch_errors = [e for e in errors if "does not support" in e.message]
        assert len(arch_errors) >= 1

        error = arch_errors[0]
        assert error.level == ValidationLevel.DOMAIN
        assert "django" in error.message.lower()
        assert "ddd" in error.message.lower()
        assert error.suggestion is not None
        # Should suggest valid architectures
        assert "simple" in error.suggestion.lower() or "layered" in error.suggestion.lower()

    def test_multiple_valid_architecture_combinations(self, validation_service):
        """Test multiple valid framework-architecture combinations."""
        valid_combinations = [
            (Framework.FASTAPI, Architecture.SIMPLE),
            (Framework.FASTAPI, Architecture.LAYERED),
            (Framework.FASTAPI, Architecture.DDD),
            (Framework.DJANGO, Architecture.SIMPLE),
            (Framework.DJANGO, Architecture.LAYERED),
            (Framework.NESTJS, Architecture.DDD),
        ]

        for framework, architecture in valid_combinations:
            config = TACConfig(
                project=ProjectSpec(
                    name="test-app",
                    language=Language.PYTHON
                    if framework in [Framework.FASTAPI, Framework.DJANGO]
                    else Language.TYPESCRIPT,
                    framework=framework,
                    architecture=architecture,
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="test", test="test"),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            )

            result = validation_service.validate_config(config)

            arch_errors = [
                e
                for e in result.errors()
                if e.level == ValidationLevel.DOMAIN and "does not support" in e.message.lower()
            ]
            assert len(arch_errors) == 0, f"Failed for {framework.value} + {architecture.value}"

    def test_multiple_invalid_architecture_combinations(self, validation_service):
        """Test multiple invalid framework-architecture combinations."""
        invalid_combinations = [
            (Framework.DJANGO, Architecture.DDD),
            (Framework.DJANGO, Architecture.CLEAN),
            (Framework.DJANGO, Architecture.HEXAGONAL),
            (Framework.NONE, Architecture.LAYERED),
            (Framework.NONE, Architecture.DDD),
        ]

        for framework, architecture in invalid_combinations:
            config = TACConfig(
                project=ProjectSpec(
                    name="test-app",
                    language=Language.PYTHON,
                    framework=framework,
                    architecture=architecture,
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="test", test="test"),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
            )

            result = validation_service.validate_config(config)

            arch_errors = [
                e
                for e in result.errors()
                if e.level == ValidationLevel.DOMAIN and "does not support" in e.message.lower()
            ]
            assert len(arch_errors) >= 1, (
                f"Should fail for {framework.value} + {architecture.value}"
            )

    def test_framework_none_only_accepts_simple(self, validation_service):
        """Test that Framework.NONE only accepts Architecture.SIMPLE."""
        # Valid: NONE + SIMPLE
        config_valid = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.PYTHON,
                framework=Framework.NONE,
                architecture=Architecture.SIMPLE,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        result = validation_service.validate_config(config_valid)
        arch_errors = [
            e
            for e in result.errors()
            if e.level == ValidationLevel.DOMAIN and "does not support" in e.message.lower()
        ]
        assert len(arch_errors) == 0

        # Invalid: NONE + LAYERED
        config_invalid = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.PYTHON,
                framework=Framework.NONE,
                architecture=Architecture.LAYERED,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        result = validation_service.validate_config(config_invalid)
        arch_errors = [
            e
            for e in result.errors()
            if e.level == ValidationLevel.DOMAIN and "does not support" in e.message.lower()
        ]
        assert len(arch_errors) >= 1


# ============================================================================
# TEST TEMPLATE VALIDATION
# ============================================================================


class TestTemplateValidation:
    """Test template existence validation."""

    def test_critical_templates_exist_passes(self, mock_template_repo, sample_valid_config):
        """Test validation passes when critical templates exist."""
        # Mock all templates exist
        mock_template_repo.template_exists.return_value = True

        validator = ValidationService(mock_template_repo)
        result = validator.validate_config(sample_valid_config)

        template_errors = [e for e in result.errors() if e.level == ValidationLevel.TEMPLATE]
        assert len(template_errors) == 0

    def test_missing_critical_template_fails(self, mock_template_repo, sample_valid_config):
        """Test validation fails when critical template is missing."""

        # Mock missing settings.json.j2
        def template_exists(name):
            return name != "claude/settings.json.j2"

        mock_template_repo.template_exists.side_effect = template_exists

        validator = ValidationService(mock_template_repo)
        result = validator.validate_config(sample_valid_config)

        assert result.valid is False
        template_errors = [e for e in result.errors() if e.level == ValidationLevel.TEMPLATE]
        assert len(template_errors) >= 1

        error = template_errors[0]
        assert "claude/settings.json.j2" in error.message
        assert error.suggestion is not None

    def test_multiple_missing_templates_generates_multiple_issues(
        self, mock_template_repo, sample_valid_config
    ):
        """Test that both missing templates generate separate issues."""
        # Mock both critical templates missing
        mock_template_repo.template_exists.return_value = False

        validator = ValidationService(mock_template_repo)
        result = validator.validate_config(sample_valid_config)

        assert result.valid is False
        template_errors = [e for e in result.errors() if e.level == ValidationLevel.TEMPLATE]
        assert len(template_errors) == 2

        # Verify both templates are mentioned
        messages = [e.message for e in template_errors]
        assert any("claude/settings.json.j2" in msg for msg in messages)
        assert any("claude/hooks/user_prompt_submit.py.j2" in msg for msg in messages)


# ============================================================================
# TEST FILESYSTEM VALIDATION
# ============================================================================


class TestFilesystemValidation:
    """Test filesystem permissions and conflicts validation."""

    def test_nonexistent_directory_with_writable_parent_passes(
        self, validation_service, sample_valid_config, tmp_path
    ):
        """Test validation passes when directory doesn't exist but parent is writable."""
        output_dir = tmp_path / "new_project"
        assert not output_dir.exists()
        assert os.access(tmp_path, os.W_OK)

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        fs_errors = [e for e in result.errors() if e.level == ValidationLevel.FILESYSTEM]
        assert len(fs_errors) == 0

    def test_non_writable_directory_fails(self, validation_service, sample_valid_config, tmp_path):
        """Test validation fails when directory is not writable."""
        # Create directory and remove write permissions
        output_dir = tmp_path / "readonly_dir"
        output_dir.mkdir()

        try:
            os.chmod(output_dir, 0o555)

            result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

            assert result.valid is False
            fs_errors = [e for e in result.errors() if e.level == ValidationLevel.FILESYSTEM]
            assert len(fs_errors) >= 1

            error = fs_errors[0]
            assert "not writable" in error.message.lower()
            assert str(output_dir) in error.message
        finally:
            # Restore permissions for cleanup
            os.chmod(output_dir, 0o755)

    def test_existing_tac_config_yaml_fails(
        self, validation_service, sample_valid_config, tmp_path
    ):
        """Test validation fails when .tac_config.yaml already exists."""
        output_dir = tmp_path / "existing_project"
        output_dir.mkdir()

        # Create .tac_config.yaml
        tac_config = output_dir / ".tac_config.yaml"
        tac_config.write_text("version: 1.1.0")

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        assert result.valid is False
        fs_errors = [e for e in result.errors() if e.level == ValidationLevel.FILESYSTEM]
        assert len(fs_errors) >= 1

        error = fs_errors[0]
        assert ".tac_config.yaml" in error.message
        assert "already contains" in error.message.lower()
        assert error.suggestion is not None

    def test_parent_directory_not_exist_fails(
        self, validation_service, sample_valid_config, tmp_path
    ):
        """Test validation fails when parent directory doesn't exist."""
        output_dir = tmp_path / "nonexistent_parent" / "project"

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        assert result.valid is False
        fs_errors = [e for e in result.errors() if e.level == ValidationLevel.FILESYSTEM]
        assert len(fs_errors) >= 1

        error = fs_errors[0]
        assert "parent directory does not exist" in error.message.lower()
        assert error.suggestion is not None

    def test_parent_directory_not_writable_fails(
        self, validation_service, sample_valid_config, tmp_path
    ):
        """Test validation fails when parent directory is not writable."""
        parent_dir = tmp_path / "readonly_parent"
        parent_dir.mkdir()
        output_dir = parent_dir / "project"

        try:
            os.chmod(parent_dir, 0o555)

            result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

            assert result.valid is False
            fs_errors = [e for e in result.errors() if e.level == ValidationLevel.FILESYSTEM]
            assert len(fs_errors) >= 1

            error = fs_errors[0]
            assert "parent directory is not writable" in error.message.lower()
        finally:
            # Restore permissions for cleanup
            os.chmod(parent_dir, 0o755)


# ============================================================================
# TEST GIT VALIDATION
# ============================================================================


class TestGitValidation:
    """Test git availability and status validation (warnings only)."""

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_git_not_installed_generates_warning(
        self, mock_which, validation_service, sample_valid_config, tmp_path
    ):
        """Test that git not installed generates warning, not error."""
        mock_which.return_value = None
        output_dir = tmp_path / "project"

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        # Warnings don't block
        assert result.valid is True

        warnings = result.warnings()
        git_warnings = [w for w in warnings if w.level == ValidationLevel.GIT]
        assert len(git_warnings) >= 1

        warning = git_warnings[0]
        assert warning.severity == "warning"
        assert (
            "git is not installed" in warning.message.lower()
            or "not available" in warning.message.lower()
        )

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    @patch("tac_bootstrap.application.validation_service.GitAdapter")
    def test_uncommitted_changes_generates_warning(
        self, mock_git_adapter_class, mock_which, validation_service, sample_valid_config, tmp_path
    ):
        """Test that uncommitted changes generate warning, not error."""
        mock_which.return_value = "/usr/bin/git"

        output_dir = tmp_path / "project"
        output_dir.mkdir()

        # Mock GitAdapter to simulate uncommitted changes
        mock_adapter = Mock()
        mock_adapter.is_repo.return_value = True
        mock_adapter.has_changes.return_value = True
        mock_git_adapter_class.return_value = mock_adapter

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        # Warnings don't block
        assert result.valid is True

        warnings = result.warnings()
        git_warnings = [w for w in warnings if w.level == ValidationLevel.GIT]
        assert len(git_warnings) >= 1

        warning = git_warnings[0]
        assert warning.severity == "warning"
        assert "uncommitted changes" in warning.message.lower()

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    @patch("tac_bootstrap.application.validation_service.GitAdapter")
    def test_git_installed_repo_clean_no_warnings(
        self, mock_git_adapter_class, mock_which, validation_service, sample_valid_config, tmp_path
    ):
        """Test no warnings when git is installed and repo is clean."""
        mock_which.return_value = "/usr/bin/git"

        output_dir = tmp_path / "project"
        output_dir.mkdir()

        # Mock GitAdapter to simulate clean repo
        mock_adapter = Mock()
        mock_adapter.is_repo.return_value = True
        mock_adapter.has_changes.return_value = False
        mock_git_adapter_class.return_value = mock_adapter

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        assert result.valid is True

        git_warnings = [w for w in result.warnings() if w.level == ValidationLevel.GIT]
        assert len(git_warnings) == 0


# ============================================================================
# TEST MULTIPLE ERRORS
# ============================================================================


class TestMultipleErrors:
    """Test accumulation of multiple validation errors."""

    def test_multiple_errors_accumulate(self, mock_template_repo, tmp_path):
        """Test that multiple errors from different layers accumulate."""
        # Setup config with multiple errors:
        # 1. Framework-language incompatible (FastAPI + JavaScript)
        # 2. Framework-architecture incompatible (Django + DDD)
        # Note: Can't have both FastAPI and Django, so we'll use Django + JS + DDD
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.JAVASCRIPT,  # Incompatible with Django
                framework=Framework.DJANGO,
                architecture=Architecture.DDD,  # Incompatible with Django
                package_manager=PackageManager.NPM,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        # Mock missing template
        mock_template_repo.template_exists.return_value = False

        validator = ValidationService(mock_template_repo)

        # Use tmp_path that doesn't exist to avoid filesystem errors
        output_dir = tmp_path / "nonexistent_parent" / "project"

        result = validator.validate_pre_scaffold(config, output_dir)

        assert result.valid is False

        errors = result.errors()
        assert len(errors) >= 3

        # Verify we have errors from multiple levels
        levels = {e.level for e in errors}
        assert ValidationLevel.DOMAIN in levels
        assert ValidationLevel.TEMPLATE in levels
        assert ValidationLevel.FILESYSTEM in levels

    def test_error_count_methods(self, mock_template_repo, tmp_path):
        """Test that errors() and warnings() filter correctly."""
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.JAVASCRIPT,
                framework=Framework.DJANGO,
                architecture=Architecture.DDD,
                package_manager=PackageManager.NPM,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        mock_template_repo.template_exists.return_value = False
        validator = ValidationService(mock_template_repo)

        output_dir = tmp_path / "nonexistent_parent" / "project"

        with patch("tac_bootstrap.application.validation_service.shutil.which") as mock_which:
            mock_which.return_value = None  # Git not installed (warning)

            result = validator.validate_pre_scaffold(config, output_dir)

        # Should have both errors and warnings
        assert len(result.errors()) >= 3
        assert len(result.warnings()) >= 1

        # Verify all errors have severity='error'
        for error in result.errors():
            assert error.severity == "error"

        # Verify all warnings have severity='warning'
        for warning in result.warnings():
            assert warning.severity == "warning"


# ============================================================================
# TEST PRE-SCAFFOLD VALIDATION
# ============================================================================


class TestPreScaffoldValidation:
    """Test complete pre-scaffold validation integration."""

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_complete_valid_configuration_passes(
        self, mock_which, validation_service, sample_valid_config, tmp_path
    ):
        """Test that completely valid configuration passes all validations."""
        mock_which.return_value = "/usr/bin/git"
        output_dir = tmp_path / "new_project"

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        assert result.valid is True
        assert len(result.errors()) == 0

    def test_multiple_layer_failures(self, mock_template_repo, tmp_path):
        """Test integration with failures in config and filesystem layers."""
        # Invalid config
        config = TACConfig(
            project=ProjectSpec(
                name="test-app",
                language=Language.GO,
                framework=Framework.FASTAPI,  # Incompatible with Go
                architecture=Architecture.SIMPLE,
                package_manager=PackageManager.GO_MOD,
            ),
            commands=CommandsSpec(start="test", test="test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-app")),
        )

        mock_template_repo.template_exists.return_value = True
        validator = ValidationService(mock_template_repo)

        # Filesystem problem: parent doesn't exist
        output_dir = tmp_path / "nonexistent" / "project"

        result = validator.validate_pre_scaffold(config, output_dir)

        assert result.valid is False
        errors = result.errors()

        # Should have both domain and filesystem errors
        assert any(e.level == ValidationLevel.DOMAIN for e in errors)
        assert any(e.level == ValidationLevel.FILESYSTEM for e in errors)

    @patch("tac_bootstrap.application.validation_service.shutil.which")
    def test_warnings_do_not_affect_validity(
        self, mock_which, validation_service, sample_valid_config, tmp_path
    ):
        """Test that git warnings are included but don't affect result.valid."""
        mock_which.return_value = None  # Git not installed
        output_dir = tmp_path / "project"

        result = validation_service.validate_pre_scaffold(sample_valid_config, output_dir)

        # Should be valid despite warning
        assert result.valid is True
        assert len(result.errors()) == 0
        assert len(result.warnings()) >= 1

        git_warnings = [w for w in result.warnings() if w.level == ValidationLevel.GIT]
        assert len(git_warnings) >= 1


# ============================================================================
# TEST VALIDATION RESULT HELPERS
# ============================================================================


class TestValidationResult:
    """Test ValidationResult helper methods."""

    def test_errors_filters_only_errors(self):
        """Test that errors() returns only error-severity issues."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Error 1",
            ),
            ValidationIssue(
                level=ValidationLevel.TEMPLATE,
                severity="warning",
                message="Warning 1",
            ),
            ValidationIssue(
                level=ValidationLevel.FILESYSTEM,
                severity="error",
                message="Error 2",
            ),
        ]

        result = ValidationResult(valid=False, issues=issues)

        errors = result.errors()
        assert len(errors) == 2
        assert all(e.severity == "error" for e in errors)

    def test_warnings_filters_only_warnings(self):
        """Test that warnings() returns only warning-severity issues."""
        issues = [
            ValidationIssue(
                level=ValidationLevel.DOMAIN,
                severity="error",
                message="Error 1",
            ),
            ValidationIssue(
                level=ValidationLevel.GIT,
                severity="warning",
                message="Warning 1",
            ),
            ValidationIssue(
                level=ValidationLevel.GIT,
                severity="warning",
                message="Warning 2",
            ),
        ]

        result = ValidationResult(valid=False, issues=issues)

        warnings = result.warnings()
        assert len(warnings) == 2
        assert all(w.severity == "warning" for w in warnings)

    def test_mixed_errors_and_warnings(self):
        """Test filtering mixed list of errors and warnings."""
        issues = [
            ValidationIssue(level=ValidationLevel.DOMAIN, severity="error", message="Error 1"),
            ValidationIssue(level=ValidationLevel.DOMAIN, severity="error", message="Error 2"),
            ValidationIssue(level=ValidationLevel.DOMAIN, severity="error", message="Error 3"),
            ValidationIssue(level=ValidationLevel.GIT, severity="warning", message="Warning 1"),
            ValidationIssue(level=ValidationLevel.GIT, severity="warning", message="Warning 2"),
        ]

        result = ValidationResult(valid=False, issues=issues)

        assert len(result.errors()) == 3
        assert len(result.warnings()) == 2
        assert len(result.issues) == 5


# ============================================================================
# TEST ENTITY VALIDATION
# ============================================================================


class TestEntityValidation:
    """Test entity specification validation."""

    def test_valid_entity_passes(self, validation_service, tmp_path):
        """Test that valid entity passes validation."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(name="title", field_type=FieldType.STRING),
                FieldSpec(name="price", field_type=FieldType.DECIMAL),
            ],
        )

        result = validation_service.validate_entity(entity, tmp_path)
        assert result.valid is True
        assert len(result.errors()) == 0

    def test_duplicate_field_names_fails(self, validation_service, tmp_path):
        """Test that duplicate field names fail validation."""
        entity = EntitySpec(
            name="Product",
            capability="catalog",
            fields=[
                FieldSpec(name="title", field_type=FieldType.STRING),
                FieldSpec(name="price", field_type=FieldType.DECIMAL),
                FieldSpec(name="title", field_type=FieldType.TEXT),  # Duplicate!
            ],
        )

        result = validation_service.validate_entity(entity, tmp_path)
        assert result.valid is False

        errors = result.errors()
        assert len(errors) >= 1
        assert any("duplicate" in e.message.lower() for e in errors)
        assert any("title" in e.message for e in errors)
