"""
IDK: upgrade-service, migration, config-update, backward-compatibility, version-management
Responsibility: Upgrades TAC Bootstrap projects to newer versions preserving user code
Invariants: Only updates framework files, never touches user code, preserves config values
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Tuple

import yaml
from packaging import version as pkg_version
from rich.console import Console

from tac_bootstrap import __version__
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import OrchestratorConfig, TACConfig

console = Console()


class UpgradeService:
    """
    IDK: project-upgrade, version-migration, safe-update, config-preservation
    Responsibility: Orchestrates project upgrades to newer TAC Bootstrap versions
    Invariants: Preserves user code, updates framework dirs, maintains compatibility
    """

    # Directorios que se actualizan (no código del usuario)
    UPGRADEABLE_DIRS = ["adws", ".claude", "scripts"]

    # Archivos que se actualizan en root
    UPGRADEABLE_FILES = ["config.yml"]

    def __init__(self, project_path: Path) -> Any:
        """Initialize upgrade service.

        Args:
            project_path: Path to the project to upgrade
        """
        self.project_path = project_path
        self.config_path = project_path / "config.yml"
        self.scaffold_service = ScaffoldService()

    def get_current_version(self) -> Optional[str]:
        """Get current project version from config.yml.

        Returns:
            Version string or None if not found/invalid
        """
        if not self.config_path.exists():
            return None

        try:
            with open(self.config_path) as f:
                config_data = yaml.safe_load(f)
                if isinstance(config_data, dict):
                    version: str = config_data.get("version", "0.1.0")
                    return version
                return "0.1.0"  # Default for old projects
        except Exception:
            return None

    def get_target_version(self) -> str:
        """Get target version (current CLI version)."""
        return __version__

    def needs_upgrade(self) -> Tuple[bool, str, str]:
        """Check if project needs upgrade.

        Returns:
            Tuple of (needs_upgrade, current_version, target_version)
        """
        current = self.get_current_version()
        target = self.get_target_version()

        if current is None:
            return False, "unknown", target

        try:
            needs = pkg_version.parse(current) < pkg_version.parse(target)
            return needs, current, target
        except Exception:
            return False, current, target

    def load_existing_config(self) -> Optional[TACConfig]:
        """Load existing project configuration.

        Returns:
            TACConfig or None if invalid
        """
        if not self.config_path.exists():
            return None

        try:
            with open(self.config_path) as f:
                config_data = yaml.safe_load(f)

            # Normalize legacy field names for compatibility
            if "tac_version" in config_data:
                if "version" not in config_data:
                    config_data["version"] = config_data["tac_version"]
                config_data.pop("tac_version")

            # Migrate schema if needed
            config_data = self._migrate_schema(config_data)

            # Actualizar version al target
            config_data["version"] = self.get_target_version()

            config = TACConfig(**config_data)
            return config
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            import traceback
            traceback.print_exc()
            return None

    def _ensure_all_config_fields(self) -> None:
        """Ensure all required fields are present in config.yml after upgrade.

        This is a post-migration step that ensures the config.yml file has all
        required fields (model IDs, backup retention, schema version) by directly
        modifying the YAML file without relying on template rendering.
        """
        log_file = self.project_path / "upgrade.log"

        with open(log_file, "a") as f:
            f.write(f"[ENSURE] _ensure_all_config_fields started\n")
            f.write(f"[ENSURE] config_path: {self.config_path}\n")
            f.write(f"[ENSURE] exists: {self.config_path.exists()}\n")

        if not self.config_path.exists():
            with open(log_file, "a") as f:
                f.write(f"[ENSURE] Config doesn't exist, returning\n")
            return

        try:
            # Read current config
            with open(self.config_path) as f:
                content = f.read()
                config_data = yaml.safe_load(content)

            with open(log_file, "a") as f:
                f.write(f"[ENSURE] config_data loaded: {config_data is not None}\n")

            if config_data is None:
                config_data = {}

            needs_update = False

            # Ensure model fields in agentic.model_policy
            if "agentic" not in config_data:
                config_data["agentic"] = {}
            if "model_policy" not in config_data["agentic"]:
                config_data["agentic"]["model_policy"] = {}

            model_policy = config_data["agentic"]["model_policy"]
            for field, default_value in [
                ("opus_model", "claude-opus-4-5-20251101"),
                ("sonnet_model", "claude-sonnet-4-5-20250929"),
                ("haiku_model", "claude-haiku-4-5-20251001"),
            ]:
                if field not in model_policy or model_policy[field] is None:
                    model_policy[field] = default_value
                    needs_update = True
                    with open(log_file, "a") as f:
                        f.write(f"[ENSURE] Added {field}\n")

            # Ensure bootstrap_retention field
            if "bootstrap" not in config_data:
                config_data["bootstrap"] = {}

            with open(log_file, "a") as f:
                f.write(f"[ENSURE] bootstrap exists: {'bootstrap' in config_data}\n")
                f.write(f"[ENSURE] backup_retention in bootstrap: {'backup_retention' in config_data.get('bootstrap', {})}\n")

            if "backup_retention" not in config_data["bootstrap"]:
                config_data["bootstrap"]["backup_retention"] = 3
                needs_update = True
                with open(log_file, "a") as f:
                    f.write(f"[ENSURE] Added backup_retention = 3\n")

            # Update schema_version to 2
            if config_data.get("schema_version") != 2:
                config_data["schema_version"] = 2
                needs_update = True
                with open(log_file, "a") as f:
                    f.write(f"[ENSURE] Updated schema_version to 2\n")

            with open(log_file, "a") as f:
                f.write(f"[ENSURE] needs_update: {needs_update}\n")

            # Write back if any updates needed
            if needs_update:
                with open(self.config_path, "w") as f:
                    yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
                with open(log_file, "a") as f:
                    f.write(f"[ENSURE] File written successfully\n")
                console.print("[green]✓ config.yml updated with model IDs and backup settings[/green]")

        except Exception as e:
            # Log errors
            with open(log_file, "a") as f:
                f.write(f"[ENSURE] Exception: {e}\n")
                import traceback
                f.write(traceback.format_exc())

    def _migrate_schema(self, config_data: dict) -> dict:
        """Migrate configuration schema to latest version.

        Args:
            config_data: Raw configuration dictionary

        Returns:
            Migrated configuration dictionary
        """
        current_schema = config_data.get("schema_version", 1)

        # Migrate from schema v1 to v2 (add model IDs)
        if current_schema == 1:
            if "agentic" not in config_data:
                config_data["agentic"] = {}
            if "model_policy" not in config_data["agentic"]:
                config_data["agentic"]["model_policy"] = {}

            # Add new model ID fields if not present
            model_policy = config_data["agentic"]["model_policy"]
            if "opus_model" not in model_policy:
                model_policy["opus_model"] = "claude-opus-4-5-20251101"
            if "sonnet_model" not in model_policy:
                model_policy["sonnet_model"] = "claude-sonnet-4-5-20250929"
            if "haiku_model" not in model_policy:
                model_policy["haiku_model"] = "claude-haiku-4-5-20251001"

            # Update schema version
            config_data["schema_version"] = 2

        return config_data

    def create_backup(self) -> Path:
        """Create backup of upgradeable directories.

        Returns:
            Path to backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.project_path / f".tac-backup-{timestamp}"
        backup_dir.mkdir(exist_ok=True)

        for dir_name in self.UPGRADEABLE_DIRS:
            source = self.project_path / dir_name
            if source.exists():
                shutil.copytree(source, backup_dir / dir_name)

        # Backup config.yml
        if self.config_path.exists():
            shutil.copy2(self.config_path, backup_dir / "config.yml")

        # Clean up old backups (keep based on config setting)
        keep_count = 3  # Default value
        config = self.load_existing_config()
        if config and config.bootstrap and hasattr(config.bootstrap, 'backup_retention'):
            keep_count = config.bootstrap.backup_retention
        self._cleanup_old_backups(keep_count=keep_count)

        return backup_dir

    def _cleanup_old_backups(self, keep_count: int = 3) -> None:
        """Remove old backup directories, keeping only the most recent ones.

        Args:
            keep_count: Number of recent backups to keep (default: 3)
        """
        try:
            # Find all backup directories
            backup_dirs = sorted(
                [d for d in self.project_path.glob(".tac-backup-*") if d.is_dir()],
                key=lambda p: p.name,  # Sorts by timestamp in name
                reverse=True  # Newest first
            )

            # Remove old backups
            for old_backup in backup_dirs[keep_count:]:
                shutil.rmtree(old_backup)
                console.print(f"[dim]Removed old backup: {old_backup.name}[/dim]")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not clean up old backups: {e}[/yellow]")

    def get_changes_preview(self, with_orchestrator: bool = False) -> List[str]:
        """Get list of changes that will be made.

        Args:
            with_orchestrator: Whether orchestrator will be added/updated

        Returns:
            List of change descriptions
        """
        changes = []

        for dir_name in self.UPGRADEABLE_DIRS:
            dir_path = self.project_path / dir_name
            if dir_path.exists():
                changes.append(f"Update {dir_name}/ directory")
            else:
                changes.append(f"Create {dir_name}/ directory")

        if with_orchestrator:
            orch_path = self.project_path / "apps" / "orchestrator_3_stream"
            if orch_path.exists():
                changes.append("Update apps/orchestrator_3_stream/ (orchestrator)")
            else:
                changes.append("Add apps/orchestrator_3_stream/ (orchestrator)")

            db_path = self.project_path / "apps" / "orchestrator_db"
            if db_path.exists():
                changes.append("Update apps/orchestrator_db/ (PostgreSQL migrations)")
            else:
                changes.append("Add apps/orchestrator_db/ (PostgreSQL migrations)")

        changes.append("Update version in config.yml")

        return changes

    def perform_upgrade(
        self, backup: bool = True, with_orchestrator: bool = False
    ) -> Tuple[bool, str]:
        """Perform the upgrade.

        Args:
            backup: Whether to create backup before upgrading
            with_orchestrator: Whether to enable orchestrator in config

        Returns:
            Tuple of (success, message)
        """
        # Debug log
        log_file = self.project_path / "upgrade.log"
        with open(log_file, "w") as f:
            f.write(f"[START] perform_upgrade called\n")

        # Load existing config
        config = self.load_existing_config()
        with open(log_file, "a") as f:
            f.write(f"[LOAD] config loaded: {config is not None}\n")
            if config and config.bootstrap:
                f.write(f"[LOAD] backup_retention before ensure: {config.bootstrap.backup_retention}\n")
        if config is None:
            return False, "Could not load existing configuration"

        # Ensure bootstrap config has backup_retention field
        if not config.bootstrap:
            from tac_bootstrap.domain.models import BootstrapConfig
            config.bootstrap = BootstrapConfig()
        elif not hasattr(config.bootstrap, 'backup_retention') or config.bootstrap.backup_retention is None:
            config.bootstrap.backup_retention = 3

        # Enable orchestrator if requested
        if with_orchestrator:
            config.orchestrator = OrchestratorConfig(enabled=True)

        # Create backup if requested
        backup_path = None
        if backup:
            backup_path = self.create_backup()
            console.print(f"[green]Created backup at: {backup_path}[/green]")

        try:
            # Remove old directories
            for dir_name in self.UPGRADEABLE_DIRS:
                dir_path = self.project_path / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path)

            # Regenerate using scaffold service with updated config
            plan = self.scaffold_service.build_plan(config, existing_repo=True)
            result = self.scaffold_service.apply_plan(plan, self.project_path, config)

            if not result.success:
                for err in result.errors:
                    console.print(f"  [red]• {err}[/red]")
                raise Exception(result.error or "Scaffold apply failed")

            return True, f"Successfully upgraded to v{self.get_target_version()}"

        except Exception as e:

            # Restore from backup if available
            if backup_path and backup_path.exists():
                console.print("[yellow]Restoring from backup...[/yellow]")
                for dir_name in self.UPGRADEABLE_DIRS:
                    backup_source = backup_path / dir_name
                    if backup_source.exists():
                        target = self.project_path / dir_name
                        if target.exists():
                            shutil.rmtree(target)
                        shutil.copytree(backup_source, target)

            return False, f"Upgrade failed: {e}"

        finally:
            # Post-migration: ALWAYS ensure all required fields are present
            # This runs whether upgrade succeeded or failed
            log_file = self.project_path / "upgrade.log"
            with open(log_file, "a") as f:
                f.write(f"[FINALLY] Post-migration starting\n")
                f.write(f"[FINALLY] config_path exists: {self.config_path.exists()}\n")

            self._ensure_all_config_fields()

            with open(log_file, "a") as f:
                f.write(f"[FINALLY] Post-migration complete\n")
                if self.config_path.exists():
                    with open(self.config_path) as cf:
                        content = cf.read()
                        if "backup_retention" in content:
                            f.write(f"[FINALLY] backup_retention FOUND in config.yml\n")
                        else:
                            f.write(f"[FINALLY] backup_retention NOT FOUND in config.yml\n")
