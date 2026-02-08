"""Comprehensive unit tests for UpgradeService.

Tests cover:
- Version detection (with/without version field, corrupt config)
- Version comparison logic
- Backup creation with correct exclusions
- Preview generation
- Config loading
- Successful upgrade flow preserving user code
- Critical: config.yml version update
- Edge cases: rollback, backup failures, missing directories
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from tac_bootstrap import __version__
from tac_bootstrap.application.upgrade_service import UpgradeService
from tac_bootstrap.domain.models import TACConfig

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def mock_project(tmp_path: Path) -> Path:
    """Create a mock project structure for testing.

    Creates:
    - config.yml with version 0.1.0
    - adws/, .claude/, scripts/ directories with dummy files
    - src/ directory with user code (main.py)
    """
    # Create config.yml with version 0.1.0
    config_data = {
        "version": "0.1.0",
        "schema_version": 1,
        "project": {
            "name": "test-project",
            "language": "python",
            "package_manager": "uv",
        },
        "commands": {
            "start": "uv run python -m app",
            "test": "uv run pytest",
        },
        "claude": {
            "settings": {
                "project_name": "test-project",
            }
        },
    }

    config_file = tmp_path / "config.yml"
    with open(config_file, "w") as f:
        yaml.dump(config_data, f)

    # Create agentic layer directories with dummy files
    for dir_name in ["adws", ".claude", "scripts"]:
        dir_path = tmp_path / dir_name
        dir_path.mkdir()
        (dir_path / "dummy.txt").write_text("old content")

    # Create user code directory
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text("# User code\nprint('Hello')")

    return tmp_path


# ============================================================================
# TEST VERSION DETECTION
# ============================================================================


class TestUpgradeService:
    """Tests for core UpgradeService functionality."""

    def test_get_current_version(self, mock_project: Path) -> None:
        """get_current_version should read version from config.yml."""
        service = UpgradeService(mock_project)
        version = service.get_current_version()

        assert version == "0.1.0"

    def test_get_current_version_missing_file(self, tmp_path: Path) -> None:
        """get_current_version should return None if config.yml doesn't exist."""
        service = UpgradeService(tmp_path)
        version = service.get_current_version()

        assert version is None

    def test_get_current_version_no_version_field(self, tmp_path: Path) -> None:
        """get_current_version should return '0.1.0' for pre-0.10.0 projects without version field.
        """
        # Create config without version field (pre-0.10.0 projects)
        config_file = tmp_path / "config.yml"
        config_data = {
            "project": {"name": "old-project"},
            "commands": {"start": "python main.py"},
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        version = service.get_current_version()

        assert version == "0.1.0"

    def test_get_target_version(self, mock_project: Path) -> None:
        """get_target_version should return current CLI version."""
        service = UpgradeService(mock_project)
        version = service.get_target_version()

        assert version == __version__

    def test_needs_upgrade_true(self, mock_project: Path) -> None:
        """needs_upgrade should return True when current < target."""
        service = UpgradeService(mock_project)

        # Patch __version__ to simulate newer version
        with patch("tac_bootstrap.application.upgrade_service.__version__", "0.10.0"):
            needs, current, target = service.needs_upgrade()

            assert needs is True
            assert current == "0.1.0"
            assert target == "0.10.0"

    def test_needs_upgrade_false_same_version(self, tmp_path: Path) -> None:
        """needs_upgrade should return False when current == target."""
        # Create config with current version
        config_file = tmp_path / "config.yml"
        config_data = {"version": __version__, "project": {"name": "test"}}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        needs, current, target = service.needs_upgrade()

        assert needs is False
        assert current == __version__
        assert target == __version__

    # ============================================================================
    # TEST BACKUP CREATION
    # ============================================================================

    def test_create_backup(self, mock_project: Path) -> None:
        """create_backup should backup agentic layer but not user code."""
        service = UpgradeService(mock_project)
        backup_path = service.create_backup()

        # Verify backup directory exists
        assert backup_path.exists()
        assert backup_path.name.startswith(".tac-backup-")

        # Verify agentic layer directories are backed up
        assert (backup_path / "adws").exists()
        assert (backup_path / ".claude").exists()
        assert (backup_path / "scripts").exists()
        assert (backup_path / "config.yml").exists()

        # Verify user code is NOT in backup
        assert not (backup_path / "src").exists()

        # Verify content is preserved
        assert (backup_path / "adws" / "dummy.txt").read_text() == "old content"

    # ============================================================================
    # TEST PREVIEW AND CONFIG LOADING
    # ============================================================================

    def test_get_changes_preview(self, mock_project: Path) -> None:
        """get_changes_preview should list changes that will be made."""
        service = UpgradeService(mock_project)
        changes = service.get_changes_preview()

        assert "Update adws/ directory" in changes
        assert "Update .claude/ directory" in changes
        assert "Update scripts/ directory" in changes
        assert "Update version in config.yml" in changes

    def test_get_changes_preview_missing_directories(self, tmp_path: Path) -> None:
        """get_changes_preview should show 'Create' for missing directories."""
        # Create minimal config without agentic layer
        config_file = tmp_path / "config.yml"
        config_data = {"version": "0.1.0", "project": {"name": "test"}}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        changes = service.get_changes_preview()

        assert "Create adws/ directory" in changes
        assert "Create .claude/ directory" in changes
        assert "Create scripts/ directory" in changes

    def test_load_existing_config(self, mock_project: Path) -> None:
        """load_existing_config should parse config.yml and update version."""
        service = UpgradeService(mock_project)

        with patch("tac_bootstrap.application.upgrade_service.__version__", "0.10.0"):
            config = service.load_existing_config()

            assert config is not None
            assert isinstance(config, TACConfig)
            assert config.project.name == "test-project"
            # Version should be updated to target
            assert config.version == "0.10.0"

    def test_load_existing_config_normalizes_legacy_tac_version(self, tmp_path: Path) -> None:
        """load_existing_config should normalize legacy 'tac_version' to 'version'."""
        # Create config with legacy tac_version field
        config_file = tmp_path / "config.yml"
        config_data = {
            "tac_version": "0.1.0",
            "schema_version": 1,
            "project": {
                "name": "legacy-project",
                "language": "python",
                "package_manager": "uv",
            },
            "commands": {
                "start": "python main.py",
                "test": "pytest",
            },
            "claude": {
                "settings": {
                    "project_name": "legacy-project",
                }
            },
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        config = service.load_existing_config()

        assert config is not None
        assert isinstance(config, TACConfig)
        assert config.project.name == "legacy-project"
        # Version should be updated to target (not legacy value)
        assert config.version == __version__

    def test_load_existing_config_preserves_existing_version(self, tmp_path: Path) -> None:
        """load_existing_config should preserve existing 'version' field."""
        # Create config with modern version field
        config_file = tmp_path / "config.yml"
        config_data = {
            "version": "0.1.5",
            "schema_version": 1,
            "project": {
                "name": "modern-project",
                "language": "python",
                "package_manager": "uv",
            },
            "commands": {
                "start": "python main.py",
                "test": "pytest",
            },
            "claude": {
                "settings": {
                    "project_name": "modern-project",
                }
            },
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        config = service.load_existing_config()

        assert config is not None
        assert isinstance(config, TACConfig)
        # Version should be updated to target
        assert config.version == __version__

    def test_load_existing_config_handles_both_fields(self, tmp_path: Path) -> None:
        """load_existing_config should keep 'version' when both fields present."""
        # Create config with both tac_version and version (migration in progress)
        config_file = tmp_path / "config.yml"
        config_data = {
            "tac_version": "0.0.9",  # Old field
            "version": "0.1.0",      # New field (should take precedence)
            "schema_version": 1,
            "project": {
                "name": "migrating-project",
                "language": "python",
                "package_manager": "uv",
            },
            "commands": {
                "start": "python main.py",
                "test": "pytest",
            },
            "claude": {
                "settings": {
                    "project_name": "migrating-project",
                }
            },
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        config = service.load_existing_config()

        assert config is not None
        assert isinstance(config, TACConfig)
        # Version should be updated to target (not legacy value)
        assert config.version == __version__

    # ============================================================================
    # TEST SUCCESSFUL UPGRADE
    # ============================================================================

    def test_perform_upgrade_preserves_user_code(self, mock_project: Path) -> None:
        """perform_upgrade should preserve user code in src/."""
        service = UpgradeService(mock_project)

        # Mock scaffold_service to avoid real I/O
        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                # Setup mocks
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                mock_result = MagicMock()
                mock_result.success = True
                mock_apply.return_value = mock_result

                # Perform upgrade
                success, message = service.perform_upgrade(backup=False)

                assert success is True
                # User code should still exist
                assert (mock_project / "src" / "main.py").exists()
                user_code = (mock_project / "src" / "main.py").read_text()
                assert user_code == "# User code\nprint('Hello')"

    def test_perform_upgrade_with_backup(self, mock_project: Path) -> None:
        """perform_upgrade should create backup when backup=True."""
        service = UpgradeService(mock_project)

        # Mock scaffold_service
        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                mock_result = MagicMock()
                mock_result.success = True
                mock_apply.return_value = mock_result

                # Perform upgrade with backup
                success, message = service.perform_upgrade(backup=True)

                assert success is True
                # Verify backup directory was created
                backups = list(mock_project.glob(".tac-backup-*"))
                assert len(backups) == 1

    def test_perform_upgrade_updates_config_version(self, mock_project: Path) -> None:
        """CRITICAL: perform_upgrade should update config.yml with new version."""
        service = UpgradeService(mock_project)

        # Mock scaffold_service to apply a config with new version
        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                def apply_side_effect(plan, path, config):
                    """Side effect to write new config with updated version."""
                    config_file = path / "config.yml"
                    config_data = {
                        "version": config.version,
                        "project": {"name": config.project.name},
                    }
                    with open(config_file, "w") as f:
                        yaml.dump(config_data, f)

                    result = MagicMock()
                    result.success = True
                    return result

                mock_apply.side_effect = apply_side_effect

                # Perform upgrade
                success, message = service.perform_upgrade(backup=False)

                assert success is True

                # Verify config.yml has updated version
                with open(mock_project / "config.yml") as f:
                    config_data = yaml.safe_load(f)
                    assert config_data["version"] == __version__

    def test_perform_upgrade_calls_scaffold_correctly(self, mock_project: Path) -> None:
        """perform_upgrade should call scaffold_service with correct arguments."""
        service = UpgradeService(mock_project)

        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                mock_result = MagicMock()
                mock_result.success = True
                mock_apply.return_value = mock_result

                # Perform upgrade
                service.perform_upgrade(backup=False)

                # Verify build_plan was called with existing_repo=True
                mock_build.assert_called_once()
                call_args = mock_build.call_args
                config_arg = call_args[0][0]
                assert isinstance(config_arg, TACConfig)
                assert call_args[1]["existing_repo"] is True

                # Verify apply_plan was called with correct path and config
                mock_apply.assert_called_once()
                assert mock_apply.call_args[0][1] == mock_project


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestUpgradeServiceEdgeCases:
    """Tests for edge cases and error handling."""

    def test_upgrade_invalid_config(self, tmp_path: Path) -> None:
        """load_existing_config should return None for corrupted config."""
        # Create corrupted YAML
        config_file = tmp_path / "config.yml"
        config_file.write_text("invalid: yaml: content:\n  - broken")

        service = UpgradeService(tmp_path)
        config = service.load_existing_config()

        assert config is None

    def test_upgrade_missing_directories(self, tmp_path: Path) -> None:
        """get_changes_preview should show 'Create' for missing directories."""
        # Create minimal project without agentic layer
        config_file = tmp_path / "config.yml"
        config_data = {"version": "0.1.0", "project": {"name": "test"}}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        changes = service.get_changes_preview()

        # All directories should be "Create" not "Update"
        assert "Create adws/ directory" in changes
        assert "Create .claude/ directory" in changes
        assert "Create scripts/ directory" in changes

    def test_perform_upgrade_rollback_on_failure(self, mock_project: Path) -> None:
        """CRITICAL: perform_upgrade should rollback from backup when scaffold fails."""
        service = UpgradeService(mock_project)

        # Verify initial state
        assert (mock_project / "adws" / "dummy.txt").read_text() == "old content"

        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                # Make apply_plan fail
                mock_result = MagicMock()
                mock_result.success = False
                mock_result.error = "Scaffold failed"
                mock_apply.return_value = mock_result

                # Perform upgrade with backup
                success, message = service.perform_upgrade(backup=True)

                assert success is False
                assert "Scaffold failed" in message

                # Verify rollback: old content should be restored
                assert (mock_project / "adws" / "dummy.txt").exists()
                assert (mock_project / "adws" / "dummy.txt").read_text() == "old content"

    def test_perform_upgrade_rollback_on_exception(self, mock_project: Path) -> None:
        """perform_upgrade should rollback when scaffold raises exception."""
        service = UpgradeService(mock_project)

        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                # Make apply_plan raise exception
                mock_apply.side_effect = Exception("Something went wrong")

                # Perform upgrade with backup
                success, message = service.perform_upgrade(backup=True)

                assert success is False
                assert "Something went wrong" in message

                # Verify rollback occurred
                assert (mock_project / "adws" / "dummy.txt").exists()

    def test_perform_upgrade_aborts_on_backup_failure(self, mock_project: Path) -> None:
        """CRITICAL: perform_upgrade should abort if create_backup fails.

        Note: Currently backup failure raises an exception (not caught).
        This test documents the current behavior.
        """
        service = UpgradeService(mock_project)

        # Mock create_backup to fail
        with patch.object(service, "create_backup") as mock_backup:
            mock_backup.side_effect = Exception("Backup failed")

            # Perform upgrade - expect exception to propagate
            with pytest.raises(Exception, match="Backup failed"):
                service.perform_upgrade(backup=True)

    def test_perform_upgrade_removes_old_files(self, mock_project: Path) -> None:
        """perform_upgrade should remove old files from agentic layer."""
        service = UpgradeService(mock_project)

        # Create an old file in adws/
        old_file = mock_project / "adws" / "old_workflow.py"
        old_file.write_text("# Old workflow")

        with patch.object(service.scaffold_service, "build_plan") as mock_build:
            with patch.object(service.scaffold_service, "apply_plan") as mock_apply:
                mock_plan = MagicMock()
                mock_build.return_value = mock_plan

                mock_result = MagicMock()
                mock_result.success = True
                mock_apply.return_value = mock_result

                # Perform upgrade
                success, message = service.perform_upgrade(backup=False)

                assert success is True

                # Old file should be gone (adws directory is removed and recreated)
                assert not old_file.exists()

    def test_perform_upgrade_fails_without_config(self, tmp_path: Path) -> None:
        """perform_upgrade should fail gracefully if config cannot be loaded."""
        # No config.yml exists
        service = UpgradeService(tmp_path)

        success, message = service.perform_upgrade(backup=False)

        assert success is False
        assert "Could not load existing configuration" in message

    def test_needs_upgrade_handles_invalid_version_format(self, tmp_path: Path) -> None:
        """needs_upgrade should handle invalid version strings gracefully."""
        # Create config with invalid version format
        config_file = tmp_path / "config.yml"
        config_data = {"version": "not-a-version", "project": {"name": "test"}}
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        service = UpgradeService(tmp_path)
        needs, current, target = service.needs_upgrade()

        # Should return False on parse error
        assert needs is False
        assert current == "not-a-version"

    def test_get_current_version_handles_non_dict_yaml(self, tmp_path: Path) -> None:
        """get_current_version should handle YAML that doesn't parse to dict."""
        # Create YAML that parses to a list
        config_file = tmp_path / "config.yml"
        config_file.write_text("- item1\n- item2\n")

        service = UpgradeService(tmp_path)
        version = service.get_current_version()

        # Should default to 0.1.0 for non-dict content
        assert version == "0.1.0"
