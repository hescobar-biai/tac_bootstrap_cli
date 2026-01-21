"""Test CLI interface."""

import json
from pathlib import Path

import yaml
from typer.testing import CliRunner

from tac_bootstrap import __version__
from tac_bootstrap.interfaces.cli import app

runner = CliRunner()


def test_cli_app_exists():
    """Test that the CLI app is properly configured."""
    assert app is not None
    assert app.info.name == "tac-bootstrap"


def test_help_command():
    """Test the help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Show version" in result.stdout


# ============================================================================
# COMPREHENSIVE CLI COMMAND TESTS
# ============================================================================


def test_version_command():
    """Test version command displays correct version information.

    Validates:
    - Exit code is 0 (success)
    - Output contains version number
    - Output contains "TAC Bootstrap" text
    """
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.stdout
    assert "TAC Bootstrap" in result.stdout


def test_init_dry_run(tmp_path: Path):
    """Test init command with --dry-run flag doesn't create files.

    Validates:
    - Exit code is 0 (success)
    - Output contains "Dry Run" or "Preview"
    - Output lists directories and files that would be created
    - No actual files/directories were created in tmp_path
    """
    # Use tmp_path as working directory but don't create project inside it
    result = runner.invoke(
        app,
        [
            "init",
            "test-project",
            "--output",
            str(tmp_path / "test-project"),
            "--dry-run",
            "--no-interactive",
        ],
    )

    assert result.exit_code == 0
    # Check for dry run indicators
    assert "Dry Run" in result.stdout or "Preview" in result.stdout
    # Should show what would be created
    assert "Would create" in result.stdout or "would create" in result.stdout.lower()
    # Should list directories
    assert "📁" in result.stdout or "Directories" in result.stdout
    # Should list files
    assert "📄" in result.stdout or "Files" in result.stdout
    # Verify no files were actually created
    project_dir = tmp_path / "test-project"
    assert not project_dir.exists(), "Dry run should not create project directory"


def test_init_with_options(tmp_path: Path):
    """Test init command with explicit language, framework, and package manager options.

    Validates:
    - Exit code is 0 (success)
    - Output contains specified language, framework, and package manager
    - Options are properly parsed and displayed in preview
    """
    result = runner.invoke(
        app,
        [
            "init",
            "test-fastapi-app",
            "--output",
            str(tmp_path / "test-fastapi-app"),
            "--language",
            "python",
            "--framework",
            "fastapi",
            "--package-manager",
            "uv",
            "--architecture",
            "ddd",
            "--no-interactive",
            "--dry-run",
        ],
    )

    assert result.exit_code == 0
    # Verify options appear in output
    assert "python" in result.stdout.lower()
    assert "fastapi" in result.stdout.lower()
    assert "uv" in result.stdout.lower()
    # Verify it's a preview
    assert "Preview" in result.stdout or "Dry Run" in result.stdout


def test_add_agentic_dry_run(tmp_path: Path):
    """Test add-agentic command with --dry-run flag.

    Validates:
    - Exit code is 0 (success) when project is detected
    - Output contains "Dry Run" or "Preview"
    - Output shows auto-detection results
    - No files were modified
    """
    # Create a minimal Python project structure for detection
    (tmp_path / "pyproject.toml").write_text(
        """[project]
name = "test-project"
version = "0.1.0"
"""
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "__init__.py").write_text("")

    result = runner.invoke(
        app,
        [
            "add-agentic",
            str(tmp_path),
            "--dry-run",
            "--no-interactive",
        ],
    )

    assert result.exit_code == 0
    # Check for dry run indicators
    assert "Dry Run" in result.stdout or "Preview" in result.stdout
    # Should show auto-detection results
    assert "Detection" in result.stdout or "Auto-Detection" in result.stdout
    # Should indicate what would be created/modified
    assert "Would create" in result.stdout or "would create" in result.stdout.lower()
    # Verify no .claude directory was created
    assert not (tmp_path / ".claude").exists(), "Dry run should not create .claude directory"


def test_doctor_healthy(tmp_path: Path):
    """Test doctor command on a valid/healthy agentic layer setup.

    Validates:
    - Exit code is 0 (success) for healthy setup
    - Output contains "healthy" or "All checks passed"
    """
    # Create a valid agentic layer structure
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "commands").mkdir()
    (tmp_path / ".claude" / "hooks").mkdir()

    # Create proper settings.json with permissions (must be JSON, not YAML)
    settings_content = {
        "project_name": "test",
        "permissions": {
            "bash": {"allow_any": True},
        },
    }
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps(settings_content, indent=2))

    # Create at least one command file to satisfy doctor checks
    (tmp_path / ".claude" / "commands" / "prime.md").write_text(
        "# Prime Command\n\nPrepare context."
    )
    (tmp_path / ".claude" / "commands" / "test.md").write_text(
        "# Test Command\n\nRun tests."
    )
    (tmp_path / ".claude" / "commands" / "commit.md").write_text(
        "# Commit Command\n\nCreate commit."
    )

    (tmp_path / "adws").mkdir()
    (tmp_path / "adws" / "adw_modules").mkdir()
    (tmp_path / "specs").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "prompts").mkdir()
    (tmp_path / "logs").mkdir()

    # Create config.yml
    config_content = {
        "project": {
            "name": "test-project",
            "language": "python",
            "package_manager": "uv",
        },
        "commands": {
            "start": "uv run python -m app",
            "test": "uv run pytest",
        },
    }
    (tmp_path / "config.yml").write_text(yaml.dump(config_content))

    result = runner.invoke(app, ["doctor", str(tmp_path)])

    assert result.exit_code == 0
    # Should indicate healthy status
    assert "healthy" in result.stdout.lower() or "all checks passed" in result.stdout.lower()


def test_doctor_with_fix(tmp_path: Path):
    """Test doctor command with --fix flag on incomplete setup.

    Validates:
    - Exit code indicates issues were found (1) or fixed (could be 0 or 1)
    - Output indicates fixes were applied or attempted
    """
    # Create an incomplete structure (missing some directories)
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "settings.json").write_text('{"project_name": "test"}')
    # Missing: commands, hooks, adws, specs, etc.

    # Create minimal config.yml so doctor can run
    config_content = {
        "project": {
            "name": "test-project",
            "language": "python",
            "package_manager": "uv",
        },
        "commands": {
            "start": "uv run python -m app",
            "test": "uv run pytest",
        },
    }
    (tmp_path / "config.yml").write_text(yaml.dump(config_content))

    result = runner.invoke(app, ["doctor", str(tmp_path), "--fix"])

    # Exit code could be 0 (fixed) or 1 (issues found/partially fixed)
    # The important thing is that it doesn't crash
    assert result.exit_code in [0, 1]
    # Should indicate fixing was attempted
    assert "fix" in result.stdout.lower() or "fixed" in result.stdout.lower()


def test_render_dry_run(tmp_path: Path):
    """Test render command with --dry-run flag.

    Validates:
    - Exit code is 0 (success)
    - Output contains "Dry Run" or "Preview"
    - Output shows what would be created/modified
    """
    # Create a valid config.yml file
    config_content = {
        "project": {
            "name": "test-render-project",
            "language": "python",
            "framework": "fastapi",
            "package_manager": "uv",
            "architecture": "ddd",
        },
        "paths": {
            "app_root": "src",
            "adws_dir": "adws",
            "specs_dir": "specs",
        },
        "commands": {
            "start": "uv run uvicorn app.main:app --reload",
            "test": "uv run pytest",
            "lint": "uv run ruff check .",
            "typecheck": "uv run mypy src/",
            "format": "uv run ruff format .",
            "build": "uv build",
        },
        "claude": {
            "settings": {
                "project_name": "test-render-project",
            },
        },
    }

    config_file = tmp_path / "config.yml"
    config_file.write_text(yaml.dump(config_content))

    result = runner.invoke(app, ["render", str(config_file), "--dry-run"])

    assert result.exit_code == 0
    # Check for dry run indicators
    assert "Dry Run" in result.stdout or "Preview" in result.stdout
    # Should show what would be created/modified
    assert "Would create" in result.stdout or "would create" in result.stdout.lower()
    # Should reference the config file
    assert "config.yml" in result.stdout or str(config_file.name) in result.stdout
