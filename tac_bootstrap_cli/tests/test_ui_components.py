"""Tests for UIComponents module.

Comprehensive tests for Rich UI components used in the interactive
setup wizard. All tests use mocked Console to prevent terminal output
during testing while verifying correct method invocations and arguments.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tac_bootstrap.domain.models import (
    AgenticSpec,
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
    TACConfig,
    WorktreeConfig,
)
from tac_bootstrap.infrastructure.ui_components import UIComponents

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_config() -> TACConfig:
    """Create a sample TACConfig for testing UI components.

    Returns a fully-configured TACConfig with Python/FastAPI/DDD settings
    suitable for testing all UI component rendering paths.
    """
    return TACConfig(
        project=ProjectSpec(
            name="test-project",
            language=Language.PYTHON,
            framework=Framework.FASTAPI,
            architecture=Architecture.DDD,
            package_manager=PackageManager.UV,
        ),
        paths=PathsSpec(app_root="src"),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
            lint="uv run ruff check .",
        ),
        agentic=AgenticSpec(
            target_branch="main",
            worktrees=WorktreeConfig(enabled=True, max_parallel=5),
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="test-project"),
        ),
        orchestrator=OrchestratorConfig(enabled=False),
    )


@pytest.fixture
def sample_config_simple() -> TACConfig:
    """Create a simple architecture TACConfig for testing."""
    return TACConfig(
        project=ProjectSpec(
            name="simple-app",
            language=Language.PYTHON,
            framework=Framework.NONE,
            architecture=Architecture.SIMPLE,
            package_manager=PackageManager.UV,
        ),
        paths=PathsSpec(app_root="."),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest",
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="simple-app"),
        ),
        orchestrator=OrchestratorConfig(enabled=False),
    )


@pytest.fixture
def sample_config_with_orchestrator() -> TACConfig:
    """Create a TACConfig with orchestrator enabled."""
    return TACConfig(
        project=ProjectSpec(
            name="orch-project",
            language=Language.TYPESCRIPT,
            framework=Framework.NEXTJS,
            architecture=Architecture.LAYERED,
            package_manager=PackageManager.PNPM,
        ),
        paths=PathsSpec(app_root="src"),
        commands=CommandsSpec(
            start="pnpm dev",
            test="pnpm test",
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="orch-project"),
        ),
        orchestrator=OrchestratorConfig(enabled=True),
    )


# ============================================================================
# TEST SHOW BANNER
# ============================================================================


class TestShowBanner:
    """Tests for UIComponents.show_banner method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_banner_with_title_only(self, mock_console_cls):
        """Test banner renders with title only."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_banner("TAC Bootstrap")

        # Should print multiple times (newlines, panel)
        assert mock_console.print.call_count >= 2

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_banner_with_title_and_subtitle(self, mock_console_cls):
        """Test banner renders with title and subtitle."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_banner("TAC Bootstrap", "Interactive Setup Wizard")

        assert mock_console.print.call_count >= 2


# ============================================================================
# TEST SHOW STEP HEADER
# ============================================================================


class TestShowStepHeader:
    """Tests for UIComponents.show_step_header method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_step_header_renders(self, mock_console_cls):
        """Test step header renders with progress indicator."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_step_header(3, 7, "Framework Selection")

        mock_console.print.assert_called_once()
        # Verify a Panel was passed
        call_args = mock_console.print.call_args
        assert call_args is not None

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_step_header_first_step(self, mock_console_cls):
        """Test step header for first step."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_step_header(1, 7, "Project Name")

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_step_header_last_step(self, mock_console_cls):
        """Test step header for last step."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_step_header(7, 7, "Preview")

        mock_console.print.assert_called_once()


# ============================================================================
# TEST SHOW PROJECT TREE PREVIEW
# ============================================================================


class TestShowProjectTreePreview:
    """Tests for UIComponents.show_project_tree_preview method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_ddd_architecture(self, mock_console_cls, sample_config):
        """Test tree preview shows DDD-specific directories."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(sample_config)

        mock_console.print.assert_called_once()
        # Verify a Panel was rendered
        call_args = mock_console.print.call_args
        assert call_args is not None

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_simple_architecture(self, mock_console_cls, sample_config_simple):
        """Test tree preview for simple architecture."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(sample_config_simple)

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_with_orchestrator(
        self, mock_console_cls, sample_config_with_orchestrator
    ):
        """Test tree preview includes apps/ when orchestrator is enabled."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(sample_config_with_orchestrator)

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_clean_architecture(self, mock_console_cls):
        """Test tree preview shows Clean architecture directories."""
        config = TACConfig(
            project=ProjectSpec(
                name="clean-app",
                language=Language.PYTHON,
                framework=Framework.FASTAPI,
                architecture=Architecture.CLEAN,
                package_manager=PackageManager.UV,
            ),
            paths=PathsSpec(app_root="src"),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="clean-app")),
        )
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(config)

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_layered_architecture(self, mock_console_cls):
        """Test tree preview shows Layered architecture directories."""
        config = TACConfig(
            project=ProjectSpec(
                name="layered-app",
                language=Language.TYPESCRIPT,
                framework=Framework.EXPRESS,
                architecture=Architecture.LAYERED,
                package_manager=PackageManager.NPM,
            ),
            paths=PathsSpec(app_root="src"),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="layered-app")),
        )
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(config)

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_tree_preview_hexagonal_architecture(self, mock_console_cls):
        """Test tree preview shows Hexagonal architecture directories."""
        config = TACConfig(
            project=ProjectSpec(
                name="hex-app",
                language=Language.GO,
                framework=Framework.GIN,
                architecture=Architecture.HEXAGONAL,
                package_manager=PackageManager.GO_MOD,
            ),
            paths=PathsSpec(app_root="src"),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="hex-app")),
        )
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_project_tree_preview(config)

        mock_console.print.assert_called_once()


# ============================================================================
# TEST PROMPT WITH SUGGESTIONS
# ============================================================================


class TestPromptWithSuggestions:
    """Tests for UIComponents.prompt_with_suggestions method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_returns_user_input(self, mock_console_cls):
        """Test prompt returns user input when provided."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = "my-custom-app"

        result = UIComponents.prompt_with_suggestions(
            "Project name",
            ["my-app", "api-service"],
            default="my-app",
        )

        assert result == "my-custom-app"

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_returns_default_on_empty_input(self, mock_console_cls):
        """Test prompt returns default when user enters empty string."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = ""

        result = UIComponents.prompt_with_suggestions(
            "Project name",
            ["my-app"],
            default="my-app",
        )

        assert result == "my-app"

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_returns_empty_on_no_default(self, mock_console_cls):
        """Test prompt returns empty string when no default and empty input."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = ""

        result = UIComponents.prompt_with_suggestions(
            "Project name",
            ["my-app"],
        )

        assert result == ""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_handles_eof(self, mock_console_cls):
        """Test prompt handles EOFError gracefully."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.side_effect = EOFError()

        result = UIComponents.prompt_with_suggestions(
            "Project name",
            ["my-app"],
            default="fallback",
        )

        assert result == "fallback"

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_shows_suggestions(self, mock_console_cls):
        """Test prompt displays suggestions."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = "input"

        UIComponents.prompt_with_suggestions(
            "Project name",
            ["my-app", "api-service", "data-pipeline"],
            default="my-app",
        )

        # Should print suggestions line
        mock_console.print.assert_called()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_truncates_many_suggestions(self, mock_console_cls):
        """Test prompt truncates when more than 5 suggestions."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = "input"

        UIComponents.prompt_with_suggestions(
            "Name",
            ["a", "b", "c", "d", "e", "f", "g"],
            default="a",
        )

        mock_console.print.assert_called()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_prompt_strips_whitespace(self, mock_console_cls):
        """Test prompt strips leading/trailing whitespace from input."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console
        mock_console.input.return_value = "  my-app  "

        result = UIComponents.prompt_with_suggestions(
            "Name",
            [],
            default="default",
        )

        assert result == "my-app"


# ============================================================================
# TEST SHOW VALIDATION ERRORS
# ============================================================================


class TestShowValidationErrors:
    """Tests for UIComponents.show_validation_errors method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_show_errors_renders_panel(self, mock_console_cls):
        """Test validation errors render in a panel."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_errors([
            "Project name is empty",
            "Invalid character in name",
        ])

        mock_console.print.assert_called_once()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_show_errors_does_nothing_for_empty_list(self, mock_console_cls):
        """Test no output when errors list is empty."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_errors([])

        mock_console.print.assert_not_called()

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_show_single_error(self, mock_console_cls):
        """Test rendering a single error."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_errors(["Something went wrong"])

        mock_console.print.assert_called_once()


# ============================================================================
# TEST SHOW VALIDATION FEEDBACK
# ============================================================================


class TestShowValidationFeedback:
    """Tests for UIComponents.show_validation_feedback method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_valid_feedback(self, mock_console_cls):
        """Test valid feedback shows checkmark."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_feedback("project_name", True, "Valid slug format")

        mock_console.print.assert_called_once()
        call_arg = mock_console.print.call_args[0][0]
        assert "project_name" in call_arg
        assert "Valid slug format" in call_arg

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_invalid_feedback(self, mock_console_cls):
        """Test invalid feedback shows cross mark."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_feedback("project_name", False, "Name cannot be empty")

        mock_console.print.assert_called_once()
        call_arg = mock_console.print.call_args[0][0]
        assert "project_name" in call_arg
        assert "Name cannot be empty" in call_arg

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_feedback_without_message(self, mock_console_cls):
        """Test feedback renders without optional message."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_validation_feedback("language", True)

        mock_console.print.assert_called_once()
        call_arg = mock_console.print.call_args[0][0]
        assert "language" in call_arg


# ============================================================================
# TEST SHOW CONFIGURATION SUMMARY
# ============================================================================


class TestShowConfigurationSummary:
    """Tests for UIComponents.show_configuration_summary method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_summary_renders_table(self, mock_console_cls, sample_config):
        """Test configuration summary renders a Rich table."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_configuration_summary(sample_config)

        # Should print empty line, table, empty line
        assert mock_console.print.call_count == 3

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_summary_with_orchestrator(self, mock_console_cls, sample_config_with_orchestrator):
        """Test configuration summary shows orchestrator as enabled."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_configuration_summary(sample_config_with_orchestrator)

        assert mock_console.print.call_count == 3

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_summary_with_empty_commands(self, mock_console_cls):
        """Test summary handles empty command strings."""
        config = TACConfig(
            project=ProjectSpec(
                name="empty-cmds",
                language=Language.PYTHON,
                framework=Framework.NONE,
                architecture=Architecture.SIMPLE,
                package_manager=PackageManager.UV,
            ),
            paths=PathsSpec(app_root="."),
            commands=CommandsSpec(start="", test=""),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="empty-cmds")),
        )
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_configuration_summary(config)

        # Should still render without errors
        assert mock_console.print.call_count == 3


# ============================================================================
# TEST SHOW SUCCESS MESSAGE
# ============================================================================


class TestShowSuccessMessage:
    """Tests for UIComponents.show_success_message method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_success_message_renders(self, mock_console_cls):
        """Test success message renders panel and next steps."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_success_message("my-app", Path("/home/user/my-app"))

        # Should print: newline, panel, newline, "Next steps:", 3 steps, newline
        assert mock_console.print.call_count >= 5

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_success_message_includes_project_name(self, mock_console_cls):
        """Test success message includes the project name."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_success_message("custom-project", Path("/tmp/custom-project"))

        # Verify project name appears in next steps
        all_calls = [str(c) for c in mock_console.print.call_args_list]
        joined = " ".join(all_calls)
        assert "custom-project" in joined


# ============================================================================
# TEST SHOW DRY RUN PREVIEW
# ============================================================================


class TestShowDryRunPreview:
    """Tests for UIComponents.show_dry_run_preview method."""

    @patch("tac_bootstrap.infrastructure.ui_components.Console")
    def test_dry_run_preview_renders(self, mock_console_cls, sample_config):
        """Test dry run preview renders panel, tree, and summary."""
        mock_console = MagicMock()
        mock_console_cls.return_value = mock_console

        UIComponents.show_dry_run_preview(sample_config, Path("/tmp/test-project"))

        # Should render multiple elements (panel, tree, summary, dim text)
        assert mock_console.print.call_count >= 3


# ============================================================================
# TEST ENHANCED INIT WIZARD
# ============================================================================


class TestEnhancedInitWizard:
    """Tests for run_enhanced_init_wizard function."""

    @pytest.fixture
    def mock_console(self):
        """Mock the wizard module's console."""
        with patch("tac_bootstrap.interfaces.wizard.console") as mock:
            yield mock

    @pytest.fixture
    def mock_prompt(self):
        """Mock Prompt.ask for user input."""
        with patch("tac_bootstrap.interfaces.wizard.Prompt.ask") as mock:
            yield mock

    @pytest.fixture
    def mock_confirm(self):
        """Mock Confirm.ask for yes/no prompts."""
        with patch("tac_bootstrap.interfaces.wizard.Confirm.ask") as mock:
            yield mock

    @pytest.fixture
    def mock_ui_components(self):
        """Mock UIComponents to prevent console output."""
        with patch("tac_bootstrap.interfaces.wizard.UIComponents") as mock:
            yield mock

    def test_enhanced_wizard_returns_config(
        self, mock_console, mock_prompt, mock_confirm, mock_ui_components
    ):
        """Test enhanced wizard returns valid TACConfig."""
        from tac_bootstrap.domain.models import get_default_commands

        default_cmds = get_default_commands(Language.PYTHON, PackageManager.UV)

        mock_prompt.side_effect = [
            "1",  # Language: Python
            "1",  # Framework: first valid
            "1",  # Architecture: Simple
            "1",  # Package Manager: UV
            default_cmds.get("start", ""),  # Start command
            default_cmds.get("test", ""),  # Test command
            default_cmds.get("lint", ""),  # Lint command
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [
            False,  # Orchestrator: no
            True,   # Worktrees: yes
            True,   # Confirm: yes
        ]

        from tac_bootstrap.interfaces.wizard import run_enhanced_init_wizard

        config = run_enhanced_init_wizard("test-app")

        assert config is not None
        assert config.project.name == "test-app"
        assert config.project.language == Language.PYTHON

    def test_enhanced_wizard_returns_none_on_cancel(
        self, mock_console, mock_prompt, mock_confirm, mock_ui_components
    ):
        """Test enhanced wizard returns None when user cancels."""
        from tac_bootstrap.domain.models import get_default_commands

        default_cmds = get_default_commands(Language.PYTHON, PackageManager.UV)

        mock_prompt.side_effect = [
            "1",  # Language
            "1",  # Framework
            "1",  # Architecture
            "1",  # Package Manager
            default_cmds.get("start", ""),
            default_cmds.get("test", ""),
            default_cmds.get("lint", ""),
            "main",
        ]
        mock_confirm.side_effect = [
            False,  # Orchestrator: no
            True,   # Worktrees: yes
            False,  # Confirm: no (cancel)
        ]

        from tac_bootstrap.interfaces.wizard import run_enhanced_init_wizard

        config = run_enhanced_init_wizard("cancel-app")

        assert config is None

    def test_enhanced_wizard_with_presets(
        self, mock_console, mock_prompt, mock_confirm, mock_ui_components
    ):
        """Test enhanced wizard skips prompts for preset values."""
        mock_prompt.side_effect = [
            "",  # Start command
            "",  # Test command
            "",  # Lint command
            "main",  # Target branch
        ]
        mock_confirm.side_effect = [
            False,  # Orchestrator: no
            True,   # Worktrees: yes
            True,   # Confirm: yes
        ]

        from tac_bootstrap.interfaces.wizard import run_enhanced_init_wizard

        config = run_enhanced_init_wizard(
            "preset-app",
            language=Language.GO,
            framework=Framework.GIN,
            package_manager=PackageManager.GO_MOD,
            architecture=Architecture.DDD,
        )

        assert config is not None
        assert config.project.language == Language.GO
        assert config.project.framework == Framework.GIN
        assert config.project.architecture == Architecture.DDD

    def test_enhanced_wizard_invalid_name_exits(
        self, mock_console, mock_prompt, mock_confirm, mock_ui_components
    ):
        """Test enhanced wizard exits on invalid project name."""
        from tac_bootstrap.interfaces.wizard import run_enhanced_init_wizard

        with pytest.raises(SystemExit) as exc_info:
            run_enhanced_init_wizard("")  # Empty name

        assert exc_info.value.code == 1


# ============================================================================
# TEST PROJECT NAME VALIDATION
# ============================================================================


class TestValidateProjectName:
    """Tests for _validate_project_name helper function."""

    def test_valid_name(self):
        """Test valid project name."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("my-app")
        assert is_valid is True
        assert error == ""

    def test_valid_name_with_numbers(self):
        """Test valid project name with numbers."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("app-2024")
        assert is_valid is True

    def test_empty_name(self):
        """Test empty project name is invalid."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("")
        assert is_valid is False
        assert "empty" in error.lower()

    def test_whitespace_only_name(self):
        """Test whitespace-only project name is invalid."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("   ")
        assert is_valid is False

    def test_name_starting_with_number(self):
        """Test name starting with number is invalid."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("123-app")
        assert is_valid is False

    def test_name_with_special_characters(self):
        """Test name with special characters is invalid."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        is_valid, error = _validate_project_name("my@app!")
        assert is_valid is False

    def test_very_long_name(self):
        """Test name exceeding 100 characters is invalid."""
        from tac_bootstrap.interfaces.wizard import _validate_project_name

        long_name = "a" * 101
        is_valid, error = _validate_project_name(long_name)
        assert is_valid is False
        assert "100" in error


# ============================================================================
# TEST HELPER FUNCTIONS
# ============================================================================


class TestHelperFunctions:
    """Tests for wizard helper functions."""

    def test_get_frameworks_for_language_display_python(self):
        """Test Python framework display names."""
        from tac_bootstrap.interfaces.wizard import get_frameworks_for_language_display

        frameworks = get_frameworks_for_language_display("python")
        assert "FastAPI" in frameworks
        assert "Django" in frameworks
        assert "Flask" in frameworks

    def test_get_frameworks_for_language_display_typescript(self):
        """Test TypeScript framework display names."""
        from tac_bootstrap.interfaces.wizard import get_frameworks_for_language_display

        frameworks = get_frameworks_for_language_display("typescript")
        assert "Next.js" in frameworks
        assert "Express" in frameworks

    def test_get_frameworks_for_language_display_unknown(self):
        """Test unknown language returns None option."""
        from tac_bootstrap.interfaces.wizard import get_frameworks_for_language_display

        frameworks = get_frameworks_for_language_display("cobol")
        assert frameworks == ["None"]

    def test_get_managers_for_language_display_python(self):
        """Test Python package manager display names."""
        from tac_bootstrap.interfaces.wizard import get_managers_for_language_display

        managers = get_managers_for_language_display("python")
        assert "uv" in managers
        assert "poetry" in managers
        assert "pip" in managers

    def test_get_managers_for_language_display_go(self):
        """Test Go package manager display names."""
        from tac_bootstrap.interfaces.wizard import get_managers_for_language_display

        managers = get_managers_for_language_display("go")
        assert managers == ["go"]

    def test_get_managers_for_language_display_unknown(self):
        """Test unknown language returns empty list."""
        from tac_bootstrap.interfaces.wizard import get_managers_for_language_display

        managers = get_managers_for_language_display("cobol")
        assert managers == []
