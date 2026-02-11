"""
TAC Bootstrap Migration Service

Provides safe schema migration for config.yml files, including:
- Version detection and comparison
- Forward and backward migration application
- Dry-run previews
- Automatic backup creation before destructive operations
- Multi-step migration path resolution

Example usage:
    from pathlib import Path
    from tac_bootstrap.application.migration_service import MigrationService

    service = MigrationService(Path("/path/to/project"))
    current = service.detect_current_version()
    target = service.get_target_version()

    if service.can_migrate(current, target):
        # Preview changes
        changes = service.dry_run(target)
        for change in changes:
            print(change)

        # Apply migration with backup
        success, message = service.apply_migration(target, backup=True)
"""

from __future__ import annotations

import copy
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import yaml

from tac_bootstrap.domain.migrations import (
    Migration,
    get_latest_version,
    get_migration_path,
)

# ============================================================================
# VERSION COMPARISON HELPER
# ============================================================================


def _compare_versions(v1: str, v2: str) -> int:
    """
    Compare two schema version strings numerically.

    Args:
        v1: First version string (e.g., "1").
        v2: Second version string (e.g., "2").

    Returns:
        -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2.

    Raises:
        ValueError: If either version string is not a valid integer.
    """
    try:
        int_v1 = int(v1)
        int_v2 = int(v2)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid version format: '{v1}' or '{v2}' (must be integers)") from e

    if int_v1 < int_v2:
        return -1
    elif int_v1 > int_v2:
        return 1
    else:
        return 0


# ============================================================================
# MIGRATION SERVICE
# ============================================================================


class MigrationService:
    """
    Orchestrates schema migrations for TAC Bootstrap config.yml files.

    Handles detection of current schema version, resolution of migration paths,
    application of forward/backward migrations, backup creation, and dry-run
    previews.

    Attributes:
        project_path: Root directory of the TAC Bootstrap project.
        config_path: Full path to the config.yml file.
    """

    def __init__(self, project_path: Path) -> None:
        """
        Initialize the migration service for a project.

        Args:
            project_path: Root directory of the TAC Bootstrap project.
        """
        self.project_path = project_path
        self.config_path = project_path / "config.yml"

    # ------------------------------------------------------------------ #
    # Version Detection
    # ------------------------------------------------------------------ #

    def detect_current_version(self) -> str:
        """
        Read and return the schema_version from config.yml.

        Falls back to "1" if the field is missing (pre-migration projects)
        or if the config file cannot be parsed.

        Returns:
            Current schema version as a string (e.g., "1" or "2").
        """
        if not self.config_path.exists():
            return "1"

        try:
            config = self.load_config()
            raw_version = config.get("schema_version", 1)
            return str(raw_version)
        except Exception:
            return "1"

    def get_target_version(self) -> str:
        """
        Return the latest available schema version from the migration registry.

        Returns:
            Latest schema version string (e.g., "2").
        """
        return get_latest_version()

    # ------------------------------------------------------------------ #
    # Migration Path Resolution
    # ------------------------------------------------------------------ #

    def get_migration_path(self, from_version: str, to_version: str) -> List[Migration]:
        """
        Find the ordered migration steps between two schema versions.

        Delegates to the domain-level path finder. Supports both forward
        (upgrade) and backward (rollback) paths.

        Args:
            from_version: Current schema version.
            to_version: Target schema version.

        Returns:
            Ordered list of Migration objects.

        Raises:
            ValueError: If no migration path exists.
        """
        return get_migration_path(from_version, to_version)

    def can_migrate(self, from_version: str, to_version: str) -> bool:
        """
        Check whether a migration path exists between two versions.

        Args:
            from_version: Current schema version.
            to_version: Target schema version.

        Returns:
            True if a valid migration path exists, False otherwise.
        """
        try:
            self.get_migration_path(from_version, to_version)
            return True
        except ValueError:
            return False

    # ------------------------------------------------------------------ #
    # Migration Application
    # ------------------------------------------------------------------ #

    def apply_migration(
        self, to_version: str, backup: bool = True
    ) -> Tuple[bool, str]:
        """
        Apply migrations from the current version up to the target version.

        Optionally creates a timestamped backup of config.yml before making
        changes. Applies each migration step in order, saving the config
        after all steps complete successfully.

        Args:
            to_version: Target schema version to migrate to.
            backup: If True, create a backup before applying (default: True).

        Returns:
            Tuple of (success: bool, message: str).
        """
        if not self.config_path.exists():
            return False, f"Config file not found: {self.config_path}"

        current_version = self.detect_current_version()

        if current_version == to_version:
            return True, f"Already at schema version {to_version}. No migration needed."

        # Resolve migration path
        try:
            migrations = self.get_migration_path(current_version, to_version)
        except ValueError as e:
            return False, str(e)

        if not migrations:
            return True, f"No migrations needed (already at version {to_version})."

        # Create backup if requested
        if backup:
            try:
                backup_path = self.create_backup()
            except Exception as e:
                return False, f"Failed to create backup: {e}"

        # Load current config
        try:
            config = self.load_config()
        except Exception as e:
            return False, f"Failed to load config: {e}"

        # Determine direction
        is_forward = _compare_versions(current_version, to_version) < 0

        # Apply each migration step
        try:
            for migration in migrations:
                if is_forward:
                    config = migration.forward(config)
                else:
                    config = migration.backward(config)

            # Save the migrated config
            self.save_config(config)

            direction = "Upgraded" if is_forward else "Rolled back"
            return True, (
                f"{direction} schema from version {current_version} to {to_version}. "
                f"Applied {len(migrations)} migration(s)."
            )

        except Exception as e:
            # Attempt to restore from backup on failure
            if backup:
                try:
                    self._restore_from_backup(backup_path)
                except Exception:
                    pass  # Best effort restoration
            return False, f"Migration failed: {e}"

    def rollback_migration(
        self, steps: int = 1, from_backup: bool = True
    ) -> Tuple[bool, str]:
        """
        Rollback the schema by the given number of migration steps.

        If from_backup is True and a backup exists, restores from the most
        recent backup instead of applying backward migrations.

        Args:
            steps: Number of schema versions to roll back (default: 1).
            from_backup: If True, try to restore from backup first (default: True).

        Returns:
            Tuple of (success: bool, message: str).
        """
        if not self.config_path.exists():
            return False, f"Config file not found: {self.config_path}"

        # Try backup restoration first if requested
        if from_backup:
            backup_path = self._find_latest_backup()
            if backup_path is not None:
                try:
                    self._restore_from_backup(backup_path)
                    return True, f"Restored config.yml from backup: {backup_path.name}"
                except Exception as e:
                    return False, f"Failed to restore from backup: {e}"

        # No backup available or not requested: apply backward migrations
        current_version = self.detect_current_version()
        current_int = int(current_version)
        target_int = max(1, current_int - steps)
        target_version = str(target_int)

        if current_version == target_version:
            return True, f"Already at schema version {target_version}. Nothing to rollback."

        return self.apply_migration(target_version, backup=False)

    # ------------------------------------------------------------------ #
    # Dry Run
    # ------------------------------------------------------------------ #

    def dry_run(self, to_version: str) -> List[str]:
        """
        Preview the changes that would be made by migrating to the target version.

        Applies the migrations to a deep copy of the config and reports
        differences without writing to disk.

        Args:
            to_version: Target schema version.

        Returns:
            List of human-readable change description strings.
        """
        changes: List[str] = []

        current_version = self.detect_current_version()

        if current_version == to_version:
            changes.append(f"Already at schema version {to_version}. No changes needed.")
            return changes

        # Resolve migration path
        try:
            migrations = self.get_migration_path(current_version, to_version)
        except ValueError as e:
            changes.append(f"Error: {e}")
            return changes

        is_forward = _compare_versions(current_version, to_version) < 0
        direction = "upgrade" if is_forward else "rollback"

        changes.append(
            f"Would {direction} schema from version {current_version} to {to_version}"
        )
        changes.append(f"Migration steps: {len(migrations)}")

        for i, migration in enumerate(migrations, start=1):
            if is_forward:
                changes.append(
                    f"  Step {i}: {migration.version_from} -> {migration.version_to} "
                    f"- {migration.description}"
                )
            else:
                changes.append(
                    f"  Step {i}: {migration.version_to} -> {migration.version_from} "
                    f"(rollback) - {migration.description}"
                )

        # Simulate the migration on a copy to show field-level changes
        if self.config_path.exists():
            try:
                original_config = self.load_config()
                preview_config = copy.deepcopy(original_config)

                for migration in migrations:
                    if is_forward:
                        preview_config = migration.forward(preview_config)
                    else:
                        preview_config = migration.backward(preview_config)

                # Detect added keys
                added = set(preview_config.keys()) - set(original_config.keys())
                removed = set(original_config.keys()) - set(preview_config.keys())

                for key in sorted(added):
                    changes.append(f"  + Add top-level key: '{key}'")
                for key in sorted(removed):
                    changes.append(f"  - Remove top-level key: '{key}'")

                # Detect changed values in existing keys
                for key in sorted(set(preview_config.keys()) & set(original_config.keys())):
                    if preview_config[key] != original_config[key]:
                        changes.append(f"  ~ Modify key: '{key}'")

            except Exception as e:
                changes.append(f"  (Could not preview field changes: {e})")

        return changes

    # ------------------------------------------------------------------ #
    # Backup Management
    # ------------------------------------------------------------------ #

    def create_backup(self) -> Path:
        """
        Create a timestamped backup of config.yml.

        The backup is stored as config.yml.bak.<timestamp> in the project
        root directory.

        Returns:
            Path to the created backup file.

        Raises:
            FileNotFoundError: If config.yml does not exist.
            OSError: If the backup file cannot be created.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.project_path / f"config.yml.bak.{timestamp}"
        shutil.copy2(self.config_path, backup_path)
        return backup_path

    def _find_latest_backup(self) -> Path | None:
        """
        Find the most recent config.yml backup file.

        Returns:
            Path to the latest backup, or None if no backups exist.
        """
        backups = sorted(
            self.project_path.glob("config.yml.bak.*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return backups[0] if backups else None

    def _restore_from_backup(self, backup_path: Path) -> None:
        """
        Restore config.yml from a backup file.

        Args:
            backup_path: Path to the backup file to restore from.

        Raises:
            FileNotFoundError: If the backup file does not exist.
            OSError: If the copy operation fails.
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_path}")

        shutil.copy2(backup_path, self.config_path)

    # ------------------------------------------------------------------ #
    # Config I/O
    # ------------------------------------------------------------------ #

    def load_config(self) -> dict:
        """
        Load and parse the YAML config file.

        Returns:
            Parsed config as a dictionary.

        Raises:
            FileNotFoundError: If config.yml does not exist.
            yaml.YAMLError: If the YAML content is invalid.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ValueError(f"Config file is not a valid YAML mapping: {self.config_path}")

        return config

    def save_config(self, config: dict) -> None:
        """
        Write the config dictionary back to the YAML file.

        Uses default YAML flow style (block style) for readability and
        preserves key ordering.

        Args:
            config: Config dictionary to write.
        """
        with open(self.config_path, "w") as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
            )
