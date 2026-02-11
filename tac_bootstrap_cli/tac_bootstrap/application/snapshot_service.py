"""
IDK: snapshot-service, project-versioning, backup-restore, diff-snapshots, history-management
Responsibility: Manages named snapshots of TAC Bootstrap projects for version control and recovery
Invariants: Snapshots are stored in ~/.tac-bootstrap/snapshots/, each snapshot is a timestamped
            directory copy, metadata is stored in JSON, supports diff and restore operations

Example usage:
    from tac_bootstrap.application.snapshot_service import SnapshotService

    service = SnapshotService()
    service.create_snapshot(Path("/my/project"), "initial-setup")
    snapshots = service.list_snapshots(Path("/my/project"))
    diff = service.diff_snapshots("initial-setup", "after-changes", Path("/my/project"))
    service.restore_snapshot("initial-setup", Path("/my/project"))
"""

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SnapshotMetadata(BaseModel):
    """Metadata for a project snapshot."""

    name: str = Field(..., description="Snapshot name")
    project_path: str = Field(..., description="Original project path")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")
    file_count: int = Field(default=0, description="Number of files in snapshot")
    total_size_bytes: int = Field(default=0, description="Total size in bytes")
    description: str = Field(default="", description="Optional snapshot description")
    tac_version: str = Field(default="", description="TAC Bootstrap version at creation time")
    file_checksums: Dict[str, str] = Field(
        default_factory=dict, description="SHA256 checksums of all files"
    )


class SnapshotDiffEntry(BaseModel):
    """A single diff entry between two snapshots."""

    path: str = Field(..., description="Relative file path")
    status: str = Field(..., description="added, removed, or modified")
    old_checksum: Optional[str] = Field(default=None, description="Checksum in snapshot1")
    new_checksum: Optional[str] = Field(default=None, description="Checksum in snapshot2")


class SnapshotDiffResult(BaseModel):
    """Result of comparing two snapshots."""

    snapshot1: str = Field(..., description="First snapshot name")
    snapshot2: str = Field(..., description="Second snapshot name")
    added: List[str] = Field(default_factory=list, description="Files added in snapshot2")
    removed: List[str] = Field(default_factory=list, description="Files removed in snapshot2")
    modified: List[str] = Field(default_factory=list, description="Files modified between snapshots")
    unchanged: int = Field(default=0, description="Number of unchanged files")
    entries: List[SnapshotDiffEntry] = Field(default_factory=list, description="Detailed diff entries")


class SnapshotService:
    """
    IDK: snapshot-core, project-backup, snapshot-management, diff-engine
    Responsibility: Creates, lists, diffs, restores, and deletes project snapshots
    Invariants: Snapshots are stored under ~/.tac-bootstrap/snapshots/<project-hash>/,
                each snapshot has metadata.json, supports cross-snapshot diffing
    """

    # Directories/files to exclude from snapshots
    EXCLUDE_PATTERNS = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".env",
        ".tox",
        "dist",
        "build",
        "*.pyc",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "trees",
    }

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize the snapshot service.

        Args:
            base_dir: Base directory for snapshot storage. Defaults to ~/.tac-bootstrap/snapshots/
        """
        self._base_dir = base_dir or (Path.home() / ".tac-bootstrap" / "snapshots")

    def _project_id(self, project_path: Path) -> str:
        """Generate a stable ID for a project based on its absolute path.

        Args:
            project_path: Absolute path to the project

        Returns:
            A short hash string identifying the project
        """
        path_str = str(project_path.resolve())
        return hashlib.sha256(path_str.encode()).hexdigest()[:12]

    def _snapshots_dir(self, project_path: Path) -> Path:
        """Get the snapshots directory for a project.

        Args:
            project_path: Path to the project

        Returns:
            Path to the project's snapshots directory
        """
        return self._base_dir / self._project_id(project_path)

    def _snapshot_dir(self, project_path: Path, name: str) -> Path:
        """Get the directory for a specific snapshot.

        Args:
            project_path: Path to the project
            name: Snapshot name

        Returns:
            Path to the snapshot directory
        """
        return self._snapshots_dir(project_path) / name

    def _should_exclude(self, path: Path) -> bool:
        """Check if a path should be excluded from snapshots.

        Args:
            path: Path to check

        Returns:
            True if the path should be excluded
        """
        for part in path.parts:
            if part in self.EXCLUDE_PATTERNS:
                return True
            for pattern in self.EXCLUDE_PATTERNS:
                if pattern.startswith("*") and part.endswith(pattern[1:]):
                    return True
        return False

    def _compute_checksum(self, file_path: Path) -> str:
        """Compute SHA256 checksum of a file.

        Args:
            file_path: Path to the file

        Returns:
            Hex digest of SHA256 hash
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (OSError, PermissionError):
            return ""

    def create_snapshot(
        self,
        project_path: Path,
        name: str,
        description: str = "",
    ) -> SnapshotMetadata:
        """Create a named snapshot of the project.

        Args:
            project_path: Path to the project to snapshot
            name: Name for the snapshot (must be unique per project)
            description: Optional description

        Returns:
            SnapshotMetadata for the created snapshot

        Raises:
            ValueError: If snapshot name already exists or project path is invalid
        """
        project_path = project_path.resolve()
        if not project_path.is_dir():
            raise ValueError(f"Project path does not exist: {project_path}")

        snapshot_dir = self._snapshot_dir(project_path, name)
        if snapshot_dir.exists():
            raise ValueError(f"Snapshot '{name}' already exists")

        # Create snapshot directory
        files_dir = snapshot_dir / "files"
        files_dir.mkdir(parents=True, exist_ok=True)

        # Copy files and compute checksums
        file_count = 0
        total_size = 0
        checksums: Dict[str, str] = {}

        for item in project_path.rglob("*"):
            if not item.is_file():
                continue
            relative = item.relative_to(project_path)
            if self._should_exclude(relative):
                continue

            dest = files_dir / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)

            checksum = self._compute_checksum(item)
            rel_str = str(relative)
            checksums[rel_str] = checksum
            file_count += 1
            try:
                total_size += item.stat().st_size
            except OSError:
                pass

        # Save metadata
        from tac_bootstrap import __version__

        metadata = SnapshotMetadata(
            name=name,
            project_path=str(project_path),
            created_at=datetime.now(timezone.utc).isoformat(),
            file_count=file_count,
            total_size_bytes=total_size,
            description=description,
            tac_version=__version__,
            file_checksums=checksums,
        )

        metadata_file = snapshot_dir / "metadata.json"
        metadata_file.write_text(metadata.model_dump_json(indent=2))

        return metadata

    def list_snapshots(self, project_path: Path) -> List[SnapshotMetadata]:
        """List all snapshots for a project.

        Args:
            project_path: Path to the project

        Returns:
            List of SnapshotMetadata, sorted by creation time (newest first)
        """
        snapshots_dir = self._snapshots_dir(project_path)
        if not snapshots_dir.exists():
            return []

        snapshots: List[SnapshotMetadata] = []
        for item in snapshots_dir.iterdir():
            if not item.is_dir():
                continue
            metadata_file = item / "metadata.json"
            if metadata_file.exists():
                try:
                    data = json.loads(metadata_file.read_text())
                    snapshots.append(SnapshotMetadata(**data))
                except (json.JSONDecodeError, Exception):
                    continue

        # Sort by creation time, newest first
        snapshots.sort(key=lambda s: s.created_at, reverse=True)
        return snapshots

    def get_snapshot(self, project_path: Path, name: str) -> Optional[SnapshotMetadata]:
        """Get metadata for a specific snapshot.

        Args:
            project_path: Path to the project
            name: Snapshot name

        Returns:
            SnapshotMetadata if found, None otherwise
        """
        snapshot_dir = self._snapshot_dir(project_path, name)
        metadata_file = snapshot_dir / "metadata.json"
        if not metadata_file.exists():
            return None
        try:
            data = json.loads(metadata_file.read_text())
            return SnapshotMetadata(**data)
        except (json.JSONDecodeError, Exception):
            return None

    def diff_snapshots(
        self, name1: str, name2: str, project_path: Path
    ) -> SnapshotDiffResult:
        """Compare two snapshots and return the differences.

        Args:
            name1: First snapshot name (baseline)
            name2: Second snapshot name (comparison)
            project_path: Path to the project

        Returns:
            SnapshotDiffResult with lists of added, removed, and modified files

        Raises:
            ValueError: If either snapshot does not exist
        """
        snap1 = self.get_snapshot(project_path, name1)
        snap2 = self.get_snapshot(project_path, name2)

        if snap1 is None:
            raise ValueError(f"Snapshot '{name1}' not found")
        if snap2 is None:
            raise ValueError(f"Snapshot '{name2}' not found")

        files1 = set(snap1.file_checksums.keys())
        files2 = set(snap2.file_checksums.keys())

        added = sorted(files2 - files1)
        removed = sorted(files1 - files2)
        common = files1 & files2

        modified = []
        unchanged = 0
        for f in sorted(common):
            if snap1.file_checksums[f] != snap2.file_checksums[f]:
                modified.append(f)
            else:
                unchanged += 1

        entries: List[SnapshotDiffEntry] = []
        for f in added:
            entries.append(
                SnapshotDiffEntry(
                    path=f, status="added", new_checksum=snap2.file_checksums.get(f)
                )
            )
        for f in removed:
            entries.append(
                SnapshotDiffEntry(
                    path=f, status="removed", old_checksum=snap1.file_checksums.get(f)
                )
            )
        for f in modified:
            entries.append(
                SnapshotDiffEntry(
                    path=f,
                    status="modified",
                    old_checksum=snap1.file_checksums.get(f),
                    new_checksum=snap2.file_checksums.get(f),
                )
            )

        return SnapshotDiffResult(
            snapshot1=name1,
            snapshot2=name2,
            added=added,
            removed=removed,
            modified=modified,
            unchanged=unchanged,
            entries=entries,
        )

    def restore_snapshot(self, name: str, project_path: Path) -> Dict[str, Any]:
        """Restore a project from a snapshot.

        Creates a backup of the current state before restoring.

        Args:
            name: Snapshot name to restore
            project_path: Path to the project

        Returns:
            Dict with restore results (files_restored, backup_name)

        Raises:
            ValueError: If snapshot does not exist
        """
        project_path = project_path.resolve()
        snapshot = self.get_snapshot(project_path, name)
        if snapshot is None:
            raise ValueError(f"Snapshot '{name}' not found")

        snapshot_dir = self._snapshot_dir(project_path, name)
        files_dir = snapshot_dir / "files"

        if not files_dir.exists():
            raise ValueError(f"Snapshot '{name}' has no files directory")

        # Create automatic backup before restore
        backup_name = f"pre-restore-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        try:
            self.create_snapshot(project_path, backup_name, description=f"Auto-backup before restoring '{name}'")
        except ValueError:
            pass  # If backup fails, proceed anyway

        # Restore files
        files_restored = 0
        for item in files_dir.rglob("*"):
            if not item.is_file():
                continue
            relative = item.relative_to(files_dir)
            dest = project_path / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            files_restored += 1

        return {
            "files_restored": files_restored,
            "backup_name": backup_name,
            "snapshot_name": name,
        }

    def delete_snapshot(self, name: str, project_path: Path) -> bool:
        """Delete a snapshot.

        Args:
            name: Snapshot name to delete
            project_path: Path to the project

        Returns:
            True if deleted, False if not found
        """
        snapshot_dir = self._snapshot_dir(project_path, name)
        if not snapshot_dir.exists():
            return False
        shutil.rmtree(snapshot_dir)
        return True

    def snapshot_exists(self, name: str, project_path: Path) -> bool:
        """Check if a snapshot exists.

        Args:
            name: Snapshot name
            project_path: Path to the project

        Returns:
            True if snapshot exists
        """
        return self._snapshot_dir(project_path, name).exists()
