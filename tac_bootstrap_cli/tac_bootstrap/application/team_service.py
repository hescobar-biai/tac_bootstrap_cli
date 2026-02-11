"""
IDK: team-service, collaboration, sharing, notifications, workspace-management
Responsibility: Manages team project sharing, change notifications, and collaborative scaffolding
Invariants: Team state is stored in ~/.tac-bootstrap/teams/, all sharing operations are local-first,
            no remote server required for basic functionality

Example usage:
    from tac_bootstrap.application.team_service import TeamService

    service = TeamService()
    service.share_project(Path("/my/project"), "alice@company.com")
    members = service.list_shared(Path("/my/project"))
    service.sync_changes(Path("/my/project"))
    service.notify_team(Path("/my/project"), "Updated API schema")
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TeamMember(BaseModel):
    """A team member with access to a project."""

    email: str = Field(..., description="Member email address")
    role: str = Field(default="contributor", description="Role: owner, admin, contributor, viewer")
    added_at: str = Field(default="", description="ISO 8601 timestamp when added")
    last_sync: Optional[str] = Field(default=None, description="Last sync timestamp")


class TeamNotification(BaseModel):
    """A team notification/message."""

    id: str = Field(..., description="Notification ID")
    sender: str = Field(default="system", description="Sender identifier")
    message: str = Field(..., description="Notification message")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    read: bool = Field(default=False, description="Whether notification has been read")
    notification_type: str = Field(default="info", description="info, warning, change, mention")


class TeamWorkspace(BaseModel):
    """A team workspace for a project."""

    project_path: str = Field(..., description="Project path")
    project_name: str = Field(default="", description="Project name")
    owner: str = Field(default="local", description="Workspace owner")
    members: List[TeamMember] = Field(default_factory=list, description="Team members")
    notifications: List[TeamNotification] = Field(
        default_factory=list, description="Recent notifications"
    )
    created_at: str = Field(default="", description="Workspace creation timestamp")
    last_activity: str = Field(default="", description="Last activity timestamp")
    sync_enabled: bool = Field(default=True, description="Whether auto-sync is enabled")


class SyncResult(BaseModel):
    """Result of a sync operation."""

    success: bool = Field(default=True, description="Whether sync succeeded")
    files_synced: int = Field(default=0, description="Number of files synced")
    conflicts: List[str] = Field(default_factory=list, description="Files with conflicts")
    message: str = Field(default="", description="Status message")
    timestamp: str = Field(default="", description="Sync timestamp")


class TeamService:
    """
    IDK: team-core, collaboration-engine, workspace-manager, notification-service
    Responsibility: Manages team workspaces, member access, notifications, and sync
    Invariants: All data stored locally in ~/.tac-bootstrap/teams/, operations are idempotent,
                supports offline-first workflow
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize team service.

        Args:
            base_dir: Base directory for team data. Defaults to ~/.tac-bootstrap/teams/
        """
        self._base_dir = base_dir or (Path.home() / ".tac-bootstrap" / "teams")

    def _workspace_file(self, project_path: Path) -> Path:
        """Get the workspace file path for a project.

        Args:
            project_path: Project path

        Returns:
            Path to workspace JSON file
        """
        import hashlib

        path_hash = hashlib.sha256(str(project_path.resolve()).encode()).hexdigest()[:12]
        return self._base_dir / f"{path_hash}.json"

    def _load_workspace(self, project_path: Path) -> Optional[TeamWorkspace]:
        """Load workspace data for a project.

        Args:
            project_path: Project path

        Returns:
            TeamWorkspace if exists, None otherwise
        """
        ws_file = self._workspace_file(project_path)
        if not ws_file.exists():
            return None
        try:
            data = json.loads(ws_file.read_text())
            return TeamWorkspace(**data)
        except (json.JSONDecodeError, Exception):
            return None

    def _save_workspace(self, workspace: TeamWorkspace) -> None:
        """Save workspace data.

        Args:
            workspace: TeamWorkspace to save
        """
        ws_file = self._workspace_file(Path(workspace.project_path))
        ws_file.parent.mkdir(parents=True, exist_ok=True)
        ws_file.write_text(workspace.model_dump_json(indent=2))

    def _get_or_create_workspace(self, project_path: Path) -> TeamWorkspace:
        """Get existing workspace or create a new one.

        Args:
            project_path: Project path

        Returns:
            TeamWorkspace instance
        """
        workspace = self._load_workspace(project_path)
        if workspace is None:
            workspace = TeamWorkspace(
                project_path=str(project_path.resolve()),
                project_name=project_path.name,
                created_at=datetime.now(timezone.utc).isoformat(),
                last_activity=datetime.now(timezone.utc).isoformat(),
            )
            self._save_workspace(workspace)
        return workspace

    def share_project(
        self,
        project_path: Path,
        email: str,
        role: str = "contributor",
    ) -> TeamMember:
        """Share a project with a team member.

        Args:
            project_path: Path to the project
            email: Member's email address
            role: Role to assign (owner, admin, contributor, viewer)

        Returns:
            TeamMember that was added

        Raises:
            ValueError: If email is invalid or member already exists
        """
        if not email or "@" not in email:
            raise ValueError(f"Invalid email address: {email}")

        valid_roles = {"owner", "admin", "contributor", "viewer"}
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}. Must be one of: {', '.join(valid_roles)}")

        workspace = self._get_or_create_workspace(project_path)

        # Check if already shared
        for member in workspace.members:
            if member.email == email:
                raise ValueError(f"Project already shared with {email}")

        member = TeamMember(
            email=email,
            role=role,
            added_at=datetime.now(timezone.utc).isoformat(),
        )
        workspace.members.append(member)
        workspace.last_activity = datetime.now(timezone.utc).isoformat()

        # Add notification
        notif = TeamNotification(
            id=f"share-{len(workspace.notifications) + 1}",
            message=f"Project shared with {email} as {role}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            notification_type="info",
        )
        workspace.notifications.append(notif)

        self._save_workspace(workspace)
        return member

    def remove_member(self, project_path: Path, email: str) -> bool:
        """Remove a team member from a project.

        Args:
            project_path: Path to the project
            email: Member's email address

        Returns:
            True if member was removed, False if not found
        """
        workspace = self._load_workspace(project_path)
        if workspace is None:
            return False

        original_count = len(workspace.members)
        workspace.members = [m for m in workspace.members if m.email != email]

        if len(workspace.members) == original_count:
            return False

        workspace.last_activity = datetime.now(timezone.utc).isoformat()
        self._save_workspace(workspace)
        return True

    def list_shared(self, project_path: Path) -> List[TeamMember]:
        """List all team members for a project.

        Args:
            project_path: Path to the project

        Returns:
            List of TeamMember objects
        """
        workspace = self._load_workspace(project_path)
        if workspace is None:
            return []
        return workspace.members

    def sync_changes(self, project_path: Path) -> SyncResult:
        """Sync changes with team (local-only operation that records sync event).

        In this implementation, sync tracks the sync event and updates timestamps.
        A full remote sync would require a server component.

        Args:
            project_path: Path to the project

        Returns:
            SyncResult with operation details
        """
        workspace = self._get_or_create_workspace(project_path)
        now = datetime.now(timezone.utc).isoformat()

        # Update last sync for all members
        for member in workspace.members:
            member.last_sync = now

        workspace.last_activity = now

        # Add notification
        notif = TeamNotification(
            id=f"sync-{len(workspace.notifications) + 1}",
            message="Project synced with team",
            timestamp=now,
            notification_type="change",
        )
        workspace.notifications.append(notif)

        self._save_workspace(workspace)

        return SyncResult(
            success=True,
            files_synced=0,
            message="Sync event recorded. Remote sync requires server configuration.",
            timestamp=now,
        )

    def notify_team(
        self,
        project_path: Path,
        message: str,
        notification_type: str = "info",
    ) -> TeamNotification:
        """Send a notification to the team.

        Args:
            project_path: Path to the project
            message: Notification message
            notification_type: Type of notification (info, warning, change, mention)

        Returns:
            The created TeamNotification
        """
        workspace = self._get_or_create_workspace(project_path)
        now = datetime.now(timezone.utc).isoformat()

        notif = TeamNotification(
            id=f"notif-{len(workspace.notifications) + 1}",
            message=message,
            timestamp=now,
            notification_type=notification_type,
        )
        workspace.notifications.append(notif)
        workspace.last_activity = now

        self._save_workspace(workspace)
        return notif

    def get_notifications(
        self, project_path: Path, unread_only: bool = False
    ) -> List[TeamNotification]:
        """Get notifications for a project.

        Args:
            project_path: Path to the project
            unread_only: Only return unread notifications

        Returns:
            List of TeamNotification objects
        """
        workspace = self._load_workspace(project_path)
        if workspace is None:
            return []

        if unread_only:
            return [n for n in workspace.notifications if not n.read]
        return workspace.notifications

    def get_workspace_info(self, project_path: Path) -> Optional[TeamWorkspace]:
        """Get full workspace information for a project.

        Args:
            project_path: Path to the project

        Returns:
            TeamWorkspace if exists, None otherwise
        """
        return self._load_workspace(project_path)
