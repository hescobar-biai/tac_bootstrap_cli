"""Tests for wizard module.

Comprehensive tests for interactive wizard functions using mocked
Rich components to avoid manual interaction during testing.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tac_bootstrap.domain.models import (
    Architecture,
    Framework,
    Language,
    PackageManager,
    ProjectMode,
)
from tac_bootstrap.interfaces.wizard import (
    run_add_agentic_wizard,
    run_init_wizard,
    select_from_enum,
)

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_console():
    """Mock Rich console to prevent output during tests."""
    with patch("tac_bootstrap.interfaces.wizard.console") as mock:
        yield mock


@pytest.fixture
def mock_prompt():
    """Mock Prompt.ask to simulate user input."""
    with patch("tac_bootstrap.interfaces.wizard.Prompt.ask") as mock:
        yield mock


@pytest.fixture
def mock_confirm():
    """Mock Confirm.ask to simulate yes/no confirmations."""
    with patch("tac_bootstrap.interfaces.wizard.Confirm.ask") as mock:
        yield mock


@pytest.fixture
def sample_detected_project():
    """Create a mock detected project with typical attributes."""
    detected = MagicMock()
    detected.language = Language.PYTHON
    detected.framework = Framework.FASTAPI
    detected.package_manager = PackageManager.UV
    detected.commands = {
        "start": "uv run fastapi dev",
        "test": "uv run pytest",
        "lint": "uv run ruff check .",
        "build": "uv build",
    }
    detected.app_root = "src"
    return detected


# ============================================================================
# TEST SELECT FROM ENUM
# ============================================================================


class TestSelectFromEnum:
    """Tests for select_from_enum function."""

    def test_select_with_default(self, mock_console, mock_prompt):
        """Test selection with default value."""
        # Simulate user pressing Enter (accepts default)
        mock_prompt.return_value = "1"  # First option (Python)

        result = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )

        assert result == Language.PYTHON
        mock_console.print.assert_called()  # Verify output was shown

    def test_select_different_option(self, mock_console, mock_prompt):
        """Test selecting non-default option."""
        # Simulate user selecting option 2 (TypeScript)
        mock_prompt.return_value = "2"

        result = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )

        # TypeScript should be second in the Language enum
        assert result == Language.TYPESCRIPT

    def test_select_with_filter(self, mock_console, mock_prompt):
        """Test selection with filter function."""
        # Only allow frameworks that work with Python
        from tac_bootstrap.domain.models import get_frameworks_for_language

        valid_frameworks = get_frameworks_for_language(Language.PYTHON)

        # Select first valid option
        mock_prompt.return_value = "1"

        result = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.NONE,
            filter_fn=lambda f: f in valid_frameworks,
        )

        # Should be a Python-compatible framework
        assert result in valid_frameworks

    def test_select_no_valid_options(self, mock_console, mock_prompt):
        """Test error when filter removes all options."""
        # Filter that rejects everything
        with pytest.raises(ValueError, match="No valid options available"):
            select_from_enum(
                "What framework?",
                Framework,
                filter_fn=lambda f: False,  # Reject all
            )

    def test_default_not_in_filtered_options(self, mock_console, mock_prompt):
        """Test when default is filtered out."""
        # Filter to only TypeScript frameworks
        from tac_bootstrap.domain.models import get_frameworks_for_language

        valid_frameworks = get_frameworks_for_language(Language.TYPESCRIPT)

        # Default is a Python framework, but we're filtering to TS
        mock_prompt.return_value = "1"  # Select first valid option

        result = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.FASTAPI,  # Python framework
            filter_fn=lambda f: f in valid_frameworks,
        )

        # Should select a TypeScript-compatible framework
        assert result in valid_frameworks


# ============================================================================
# TEST RUN INIT WIZARD
# ============================================================================


class TestRunInitWizard:
    """Tests for run_init_wizard function."""

    def test_wizard_with_all_defaults(self, mock_console, mock_prompt, mock_confirm):
        """Test wizard accepting all default values."""
        # Mock all prompts to accept defaults (option 1 for selects)
        # For commands, we need to return the actual default values since
        # empty string means "no input" not "use default"
        from tac_bootstrap.domain.models import get_default_commands
        default_cmds = get_default_commands(Language.PYTHON, PackageManager.UV)

        mock_prompt.side_effect = [
            "1",  # Language: Python (default)
            "1",  # Framework: FASTAPI (first option for Python)
            "1",  # Package Manager: UV (default for Python)
            "1",  # Architecture: Simple (default)
            default_cmds.get("start", ""),  # Start command (return default)
            default_cmds.get("test", ""),  # Test command (return default)
            default_cmds.get("lint", ""),  # Lint command (return default)
        ]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            True,  # Confirm configuration
        ]

        config = run_init_wizard("myproject")

        # Verify project configuration
        assert config.project.name == "myproject"
        assert config.project.mode == ProjectMode.NEW
        assert config.project.language == Language.PYTHON
        assert config.project.framework == Framework.FASTAPI  # First option for Python
        assert config.project.architecture == Architecture.SIMPLE

        # Verify default commands were set (should match what get_default_commands returns)
        assert config.commands.start == default_cmds.get("start", "")
        assert config.commands.test == default_cmds.get("test", "")

        # Verify worktrees enabled
        assert config.agentic.worktrees.enabled is True

    def test_wizard_with_custom_values(self, mock_console, mock_prompt, mock_confirm):
        """Test wizard with custom user selections."""
        # Mock prompts for TypeScript + React + npm + LAYERED
        mock_prompt.side_effect = [
            "2",  # Language: TypeScript
            "4",  # Framework: React (4th option for TS: NEXTJS, EXPRESS, NESTJS, REACT)
            "2",  # Package Manager: npm (2nd for TS: PNPM, NPM)
            "2",  # Architecture: LAYERED (2nd option)
            "npm run dev",  # Custom start command
            "npm test",  # Custom test command
            "npm run lint",  # Custom lint command
        ]
        mock_confirm.side_effect = [
            False,  # Disable worktrees
            True,  # Confirm configuration
        ]

        config = run_init_wizard("custom-app")

        # Verify custom selections
        assert config.project.name == "custom-app"
        assert config.project.language == Language.TYPESCRIPT
        assert config.project.architecture == Architecture.LAYERED
        assert config.commands.start == "npm run dev"
        assert config.commands.test == "npm test"
        assert config.commands.lint == "npm run lint"
        assert config.agentic.worktrees.enabled is False

    def test_wizard_with_preset_language(self, mock_console, mock_prompt, mock_confirm):
        """Test wizard when language is already provided."""
        # Language preset, so wizard skips that step
        mock_prompt.side_effect = [
            "1",  # Framework
            "1",  # Package Manager
            "1",  # Architecture
            "",  # Start command
            "",  # Test command
            "",  # Lint command
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard("preset-project", language=Language.GO)

        # Verify preset language was used
        assert config.project.language == Language.GO

    def test_wizard_cancellation(self, mock_console, mock_prompt, mock_confirm):
        """Test wizard when user cancels at confirmation."""
        mock_prompt.side_effect = ["1", "1", "1", "1", "", "", ""]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            False,  # Cancel at final confirmation
        ]

        # Should raise SystemExit when user cancels
        with pytest.raises(SystemExit) as exc_info:
            run_init_wizard("cancelled-project")

        assert exc_info.value.code == 0
        mock_console.print.assert_any_call("[yellow]Aborted.[/yellow]")


# ============================================================================
# TEST RUN ADD AGENTIC WIZARD
# ============================================================================


class TestRunAddAgenticWizard:
    """Tests for run_add_agentic_wizard function."""

    def test_wizard_with_detected_values(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """Test wizard using detected project values."""
        # Accept all detected values (option 1 for each select)
        # When Prompt.ask is called with a default, returning empty string means accept default
        mock_prompt.side_effect = [
            "1",  # Language: PYTHON (detected)
            "1",  # Framework: FASTAPI (detected)
            "1",  # Package Manager: UV (detected)
            "uv run fastapi dev",  # Start command (return detected value)
            "uv run pytest",  # Test command (return detected value)
            "uv run ruff check .",  # Lint command (return detected value)
            "uv build",  # Build command (return detected value)
        ]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            True,  # Confirm configuration
        ]

        repo_path = Path("/path/to/existing-repo")
        config = run_add_agentic_wizard(repo_path, sample_detected_project)

        # Verify detected values were used
        assert config.project.name == "existing-repo"
        assert config.project.mode == ProjectMode.EXISTING
        assert config.project.repo_root == str(repo_path)
        assert config.project.language == Language.PYTHON
        assert config.project.framework == Framework.FASTAPI
        assert config.project.package_manager == PackageManager.UV

        # Verify detected commands
        assert config.commands.start == "uv run fastapi dev"
        assert config.commands.test == "uv run pytest"
        assert config.commands.lint == "uv run ruff check ."
        assert config.commands.build == "uv build"

        # Verify detected app_root
        assert config.paths.app_root == "src"

    def test_wizard_overriding_detected_values(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """Test wizard when user overrides detected values."""
        # Change language to TypeScript
        mock_prompt.side_effect = [
            "2",  # Language: TypeScript (override detected)
            "1",  # Framework: First valid for TS
            "1",  # Package Manager: First valid for TS
            "pnpm dev",  # Custom start command
            "pnpm test",  # Custom test command
            "pnpm lint",  # Custom lint command
            "pnpm build",  # Custom build command
        ]
        mock_confirm.side_effect = [False, True]

        repo_path = Path("/path/to/existing-repo")
        config = run_add_agentic_wizard(repo_path, sample_detected_project)

        # Verify overrides
        assert config.project.language == Language.TYPESCRIPT
        assert config.commands.start == "pnpm dev"
        assert config.agentic.worktrees.enabled is False

    def test_add_agentic_cancellation(
        self, mock_console, mock_prompt, mock_confirm, sample_detected_project
    ):
        """Test add agentic wizard when user cancels."""
        mock_prompt.side_effect = ["1", "1", "1", "", "", "", ""]
        mock_confirm.side_effect = [
            True,  # Enable worktrees
            False,  # Cancel at final confirmation
        ]

        repo_path = Path("/path/to/repo")

        # Should raise SystemExit when user cancels
        with pytest.raises(SystemExit) as exc_info:
            run_add_agentic_wizard(repo_path, sample_detected_project)

        assert exc_info.value.code == 0
        mock_console.print.assert_any_call("[yellow]Aborted.[/yellow]")


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestWizardEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_empty_command_strings_allowed(
        self, mock_console, mock_prompt, mock_confirm
    ):
        """Test that empty strings are acceptable for optional commands."""
        mock_prompt.side_effect = [
            "1",  # Language
            "1",  # Framework
            "1",  # Package Manager
            "1",  # Architecture
            "",  # Start command (empty)
            "",  # Test command (empty)
            "",  # Lint command (empty)
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard("minimal-project")

        # Empty strings should be preserved (not None)
        assert isinstance(config.commands.start, str)
        assert isinstance(config.commands.test, str)
        assert isinstance(config.commands.lint, str)

    def test_preset_values_skip_prompts(
        self, mock_console, mock_prompt, mock_confirm
    ):
        """Test that preset values reduce number of prompts."""
        # When language, framework, and package_manager are preset
        mock_prompt.side_effect = [
            "1",  # Architecture (only remaining selection)
            "",  # Start command
            "",  # Test command
            "",  # Lint command
        ]
        mock_confirm.side_effect = [True, True]

        config = run_init_wizard(
            "preset-all",
            language=Language.RUST,
            framework=Framework.NONE,
            package_manager=PackageManager.CARGO,
        )

        # Verify presets were used
        assert config.project.language == Language.RUST
        assert config.project.framework == Framework.NONE
        assert config.project.package_manager == PackageManager.CARGO

        # Verify fewer prompts were called (no language/framework/pm selection)
        assert mock_prompt.call_count == 4  # Only arch + 3 commands
