"""Tests for upgrade CLI command."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from tac_bootstrap.interfaces.cli import app

runner = CliRunner()


def test_upgrade_command_no_config(tmp_path: Path) -> None:
    """Test upgrade command when config.yml does not exist."""
    result = runner.invoke(app, ["upgrade", str(tmp_path)])

    assert result.exit_code == 1
    assert "No config.yml found" in result.stdout


def test_upgrade_command_already_up_to_date(tmp_path: Path) -> None:
    """Test upgrade command when project is already up to date."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.10.1\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (False, "0.10.1", "0.10.1")
        mock_service.return_value = mock_instance

        result = runner.invoke(app, ["upgrade", str(tmp_path)])

        assert result.exit_code == 0
        assert "already up to date" in result.stdout


def test_upgrade_command_dry_run(tmp_path: Path) -> None:
    """Test upgrade command in dry-run mode."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.1.0\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (True, "0.1.0", "0.10.1")
        mock_instance.get_changes_preview.return_value = [
            "Update adws/ directory",
            "Update .claude/ directory",
            "Update version in config.yml",
        ]
        mock_service.return_value = mock_instance

        result = runner.invoke(app, ["upgrade", str(tmp_path), "--dry-run"])

        assert result.exit_code == 0
        assert "Dry run - no changes made" in result.stdout
        assert "Update adws/ directory" in result.stdout
        mock_instance.perform_upgrade.assert_not_called()


def test_upgrade_command_user_cancels(tmp_path: Path) -> None:
    """Test upgrade command when user cancels confirmation."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.1.0\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (True, "0.1.0", "0.10.1")
        mock_instance.get_changes_preview.return_value = ["Update adws/ directory"]
        mock_service.return_value = mock_instance

        # Simulate user pressing 'n' for no
        result = runner.invoke(app, ["upgrade", str(tmp_path)], input="n\n")

        assert result.exit_code == 0
        assert "Upgrade cancelled" in result.stdout
        mock_instance.perform_upgrade.assert_not_called()


def test_upgrade_command_success(tmp_path: Path) -> None:
    """Test successful upgrade with backup."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.1.0\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (True, "0.1.0", "0.10.1")
        mock_instance.get_changes_preview.return_value = ["Update adws/ directory"]
        mock_instance.perform_upgrade.return_value = (True, "Successfully upgraded to v0.10.1")
        mock_service.return_value = mock_instance

        # Simulate user pressing 'y' for yes
        result = runner.invoke(app, ["upgrade", str(tmp_path)], input="y\n")

        assert result.exit_code == 0
        assert "Successfully upgraded to v0.10.1" in result.stdout
        assert "Backup preserved" in result.stdout
        mock_instance.perform_upgrade.assert_called_once_with(backup=True, with_orchestrator=False)


def test_upgrade_command_no_backup(tmp_path: Path) -> None:
    """Test upgrade without backup when --no-backup is used."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.1.0\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (True, "0.1.0", "0.10.1")
        mock_instance.get_changes_preview.return_value = ["Update adws/ directory"]
        mock_instance.perform_upgrade.return_value = (True, "Successfully upgraded to v0.10.1")
        mock_service.return_value = mock_instance

        # Simulate user pressing 'y' for yes
        result = runner.invoke(app, ["upgrade", str(tmp_path), "--no-backup"], input="y\n")

        assert result.exit_code == 0
        assert "Successfully upgraded to v0.10.1" in result.stdout
        assert "Backup preserved" not in result.stdout
        mock_instance.perform_upgrade.assert_called_once_with(backup=False, with_orchestrator=False)


def test_upgrade_command_force(tmp_path: Path) -> None:
    """Test upgrade with --force flag when versions match."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.10.1\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (False, "0.10.1", "0.10.1")
        mock_instance.get_changes_preview.return_value = ["Update adws/ directory"]
        mock_instance.perform_upgrade.return_value = (True, "Successfully upgraded to v0.10.1")
        mock_service.return_value = mock_instance

        # Simulate user pressing 'y' for yes
        result = runner.invoke(app, ["upgrade", str(tmp_path), "--force"], input="y\n")

        assert result.exit_code == 0
        assert "Successfully upgraded to v0.10.1" in result.stdout
        mock_instance.perform_upgrade.assert_called_once()


def test_upgrade_command_failure(tmp_path: Path) -> None:
    """Test upgrade command when perform_upgrade fails."""
    # Create a config.yml
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.1.0\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        mock_instance.needs_upgrade.return_value = (True, "0.1.0", "0.10.1")
        mock_instance.get_changes_preview.return_value = ["Update adws/ directory"]
        mock_instance.perform_upgrade.return_value = (False, "Upgrade failed: some error")
        mock_service.return_value = mock_instance

        # Simulate user pressing 'y' for yes
        result = runner.invoke(app, ["upgrade", str(tmp_path)], input="y\n")

        assert result.exit_code == 1
        assert "Upgrade failed: some error" in result.stdout


def test_upgrade_newer_project_version(tmp_path: Path) -> None:
    """Test upgrade when project version is newer than CLI version (downgrade not supported)."""
    # Create a config.yml with a version newer than CLI
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 0.10.1\nproject:\n  name: test\n")

    with patch("tac_bootstrap.interfaces.cli.UpgradeService") as mock_service:
        mock_instance = MagicMock()
        # Simulate project version (0.10.1) > CLI version (0.10.1)
        mock_instance.needs_upgrade.return_value = (False, "0.10.1", "0.10.1")
        mock_service.return_value = mock_instance

        result = runner.invoke(app, ["upgrade", str(tmp_path)])

        assert result.exit_code == 0
        assert "already up to date" in result.stdout
        mock_instance.perform_upgrade.assert_not_called()
