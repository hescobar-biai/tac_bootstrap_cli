"""
IDK: upgrade-service, migration, config-update, backward-compatibility, version-management
Responsibility: Upgrades TAC Bootstrap projects to newer versions preserving user code
Invariants: Only updates framework files, never touches user code, preserves config values
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

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

    def __init__(self, project_path: Path):
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

            # Actualizar version al target
            config_data["version"] = self.get_target_version()

            return TACConfig(**config_data)
        except Exception as e:
            console.print(f"[red]Error loading config: {e}[/red]")
            return None

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

        return backup_dir

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
        # Load existing config
        config = self.load_existing_config()
        if config is None:
            return False, "Could not load existing configuration"

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
