"""
IDK: community-service, plugin-registry, template-sharing, achievements, showcase
Responsibility: Manages community plugin/template sharing, user profiles, achievements,
                and community browsing
Invariants: Community data stored locally in ~/.tac-bootstrap/community/, supports offline
            browsing with built-in templates, achievement badges are earned automatically

Example usage:
    from tac_bootstrap.application.community_service import CommunityService

    service = CommunityService()
    service.share_plugin("my-plugin", Path("/my/plugin"), "Authentication plugin")
    templates = service.browse_templates(category="authentication")
    awards = service.get_awards()
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CommunityItem(BaseModel):
    """A community-shared item (plugin or template)."""

    name: str = Field(..., description="Item name")
    item_type: str = Field(..., description="plugin or template")
    description: str = Field(default="", description="Item description")
    author: str = Field(default="anonymous", description="Author identifier")
    category: str = Field(default="general", description="Category")
    tags: List[str] = Field(default_factory=list, description="Tags")
    version: str = Field(default="1.1.0", description="Item version")
    created_at: str = Field(default="", description="Creation timestamp")
    downloads: int = Field(default=0, description="Download count")
    rating: float = Field(default=0.0, description="Average rating (0-5)")
    source_path: Optional[str] = Field(default=None, description="Source file/directory path")


class Achievement(BaseModel):
    """A user achievement/badge."""

    id: str = Field(..., description="Achievement identifier")
    name: str = Field(..., description="Achievement name")
    description: str = Field(default="", description="How to earn this achievement")
    icon: str = Field(default="*", description="Display icon/emoji")
    earned: bool = Field(default=False, description="Whether achievement is earned")
    earned_at: Optional[str] = Field(default=None, description="When earned")
    category: str = Field(default="general", description="Achievement category")
    points: int = Field(default=10, description="Points value")


class UserProfile(BaseModel):
    """User community profile."""

    username: str = Field(default="anonymous", description="Username")
    email: Optional[str] = Field(default=None, description="Email")
    projects_created: int = Field(default=0, description="Number of projects created")
    plugins_shared: int = Field(default=0, description="Number of plugins shared")
    templates_published: int = Field(default=0, description="Templates published")
    total_points: int = Field(default=0, description="Total achievement points")
    achievements: List[Achievement] = Field(
        default_factory=list, description="Earned achievements"
    )
    member_since: str = Field(default="", description="Registration date")


class CommunityStats(BaseModel):
    """Community statistics."""

    total_plugins: int = Field(default=0, description="Total plugins shared")
    total_templates: int = Field(default=0, description="Total templates published")
    total_users: int = Field(default=0, description="Approximate user count")
    categories: Dict[str, int] = Field(default_factory=dict, description="Items by category")
    top_items: List[CommunityItem] = Field(
        default_factory=list, description="Top rated items"
    )


# Built-in achievement definitions
ACHIEVEMENTS: List[Dict[str, Any]] = [
    {
        "id": "first-project",
        "name": "First Steps",
        "description": "Create your first TAC Bootstrap project",
        "icon": "[star]",
        "category": "creation",
        "points": 10,
    },
    {
        "id": "five-projects",
        "name": "Project Builder",
        "description": "Create 5 projects with TAC Bootstrap",
        "icon": "[star][star]",
        "category": "creation",
        "points": 25,
    },
    {
        "id": "first-entity",
        "name": "Entity Creator",
        "description": "Generate your first CRUD entity",
        "icon": "[diamond]",
        "category": "generation",
        "points": 15,
    },
    {
        "id": "first-share",
        "name": "Community Contributor",
        "description": "Share your first plugin or template",
        "icon": "[heart]",
        "category": "community",
        "points": 20,
    },
    {
        "id": "ddd-architect",
        "name": "DDD Architect",
        "description": "Create a project with DDD architecture",
        "icon": "[building]",
        "category": "architecture",
        "points": 15,
    },
    {
        "id": "polyglot",
        "name": "Polyglot Developer",
        "description": "Create projects in 3 different languages",
        "icon": "[globe]",
        "category": "diversity",
        "points": 30,
    },
    {
        "id": "test-champion",
        "name": "Test Champion",
        "description": "Generate entities with full test coverage",
        "icon": "[check]",
        "category": "quality",
        "points": 20,
    },
    {
        "id": "full-stack",
        "name": "Full Stack",
        "description": "Create a project with orchestrator enabled",
        "icon": "[layers]",
        "category": "architecture",
        "points": 25,
    },
    {
        "id": "upgrader",
        "name": "Always Updated",
        "description": "Upgrade a project to latest version",
        "icon": "[arrow-up]",
        "category": "maintenance",
        "points": 10,
    },
    {
        "id": "health-check",
        "name": "Health Inspector",
        "description": "Run health-check and achieve all passing",
        "icon": "[heart-pulse]",
        "category": "quality",
        "points": 15,
    },
]

# Built-in community templates
BUILT_IN_TEMPLATES: List[CommunityItem] = [
    CommunityItem(
        name="fastapi-auth-starter",
        item_type="template",
        description="FastAPI starter with JWT authentication, user management, and role-based access",
        author="tac-team",
        category="authentication",
        tags=["fastapi", "auth", "jwt", "rbac", "python"],
        version="1.1.0",
        downloads=150,
        rating=4.5,
    ),
    CommunityItem(
        name="nextjs-dashboard",
        item_type="template",
        description="Next.js admin dashboard with charts, tables, and real-time data",
        author="tac-team",
        category="frontend",
        tags=["nextjs", "react", "dashboard", "typescript"],
        version="1.1.0",
        downloads=120,
        rating=4.3,
    ),
    CommunityItem(
        name="microservice-gateway",
        item_type="template",
        description="API Gateway template with rate limiting, auth, and service discovery",
        author="tac-team",
        category="infrastructure",
        tags=["gateway", "microservice", "api", "rate-limit"],
        version="1.1.0",
        downloads=85,
        rating=4.7,
    ),
    CommunityItem(
        name="event-driven-cqrs",
        item_type="template",
        description="CQRS/Event Sourcing template with command and query separation",
        author="tac-team",
        category="architecture",
        tags=["cqrs", "event-sourcing", "ddd", "architecture"],
        version="1.1.0",
        downloads=95,
        rating=4.6,
    ),
    CommunityItem(
        name="websocket-chat",
        item_type="plugin",
        description="Real-time WebSocket chat plugin with rooms and user presence",
        author="tac-team",
        category="communication",
        tags=["websocket", "chat", "real-time", "plugin"],
        version="1.1.0",
        downloads=60,
        rating=4.2,
    ),
    CommunityItem(
        name="s3-file-upload",
        item_type="plugin",
        description="File upload plugin with S3 integration and image processing",
        author="tac-team",
        category="storage",
        tags=["s3", "upload", "file", "storage", "plugin"],
        version="1.1.0",
        downloads=75,
        rating=4.4,
    ),
]


class CommunityService:
    """
    IDK: community-core, plugin-registry, template-browser, achievement-tracker
    Responsibility: Manages community content, user achievements, and content browsing
    Invariants: Local-first storage, built-in templates always available, achievements are
                tracked per-user in ~/.tac-bootstrap/community/
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        """Initialize community service.

        Args:
            base_dir: Base directory for community data.
                     Defaults to ~/.tac-bootstrap/community/
        """
        self._base_dir = base_dir or (Path.home() / ".tac-bootstrap" / "community")
        self._items_file = self._base_dir / "items.json"
        self._profile_file = self._base_dir / "profile.json"

    def _load_items(self) -> List[CommunityItem]:
        """Load community items from local storage + built-in templates."""
        items = list(BUILT_IN_TEMPLATES)

        if self._items_file.exists():
            try:
                data = json.loads(self._items_file.read_text())
                for item_data in data:
                    items.append(CommunityItem(**item_data))
            except (json.JSONDecodeError, Exception):
                pass

        return items

    def _save_items(self, custom_items: List[CommunityItem]) -> None:
        """Save custom community items to local storage."""
        self._items_file.parent.mkdir(parents=True, exist_ok=True)
        data = [item.model_dump() for item in custom_items]
        self._items_file.write_text(json.dumps(data, indent=2))

    def _load_profile(self) -> UserProfile:
        """Load user profile from local storage."""
        if self._profile_file.exists():
            try:
                data = json.loads(self._profile_file.read_text())
                return UserProfile(**data)
            except (json.JSONDecodeError, Exception):
                pass
        return UserProfile(
            member_since=datetime.now(timezone.utc).isoformat(),
        )

    def _save_profile(self, profile: UserProfile) -> None:
        """Save user profile to local storage."""
        self._profile_file.parent.mkdir(parents=True, exist_ok=True)
        self._profile_file.write_text(profile.model_dump_json(indent=2))

    def share_plugin(
        self,
        name: str,
        source_path: Optional[Path] = None,
        description: str = "",
        category: str = "general",
        tags: Optional[List[str]] = None,
    ) -> CommunityItem:
        """Share a plugin to the community registry.

        Args:
            name: Plugin name
            source_path: Path to plugin source
            description: Plugin description
            category: Plugin category
            tags: Plugin tags

        Returns:
            The created CommunityItem

        Raises:
            ValueError: If plugin name is empty
        """
        if not name:
            raise ValueError("Plugin name cannot be empty")

        item = CommunityItem(
            name=name,
            item_type="plugin",
            description=description,
            category=category,
            tags=tags or [],
            source_path=str(source_path) if source_path else None,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        # Load existing custom items
        existing = []
        if self._items_file.exists():
            try:
                data = json.loads(self._items_file.read_text())
                existing = [CommunityItem(**d) for d in data]
            except Exception:
                pass

        existing.append(item)
        self._save_items(existing)

        # Update profile
        profile = self._load_profile()
        profile.plugins_shared += 1
        self._save_profile(profile)

        return item

    def publish_template(
        self,
        name: str,
        source_path: Optional[Path] = None,
        description: str = "",
        category: str = "general",
        tags: Optional[List[str]] = None,
    ) -> CommunityItem:
        """Publish a template to the community.

        Args:
            name: Template name
            source_path: Path to template source
            description: Template description
            category: Template category
            tags: Template tags

        Returns:
            The created CommunityItem

        Raises:
            ValueError: If template name is empty
        """
        if not name:
            raise ValueError("Template name cannot be empty")

        item = CommunityItem(
            name=name,
            item_type="template",
            description=description,
            category=category,
            tags=tags or [],
            source_path=str(source_path) if source_path else None,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        existing = []
        if self._items_file.exists():
            try:
                data = json.loads(self._items_file.read_text())
                existing = [CommunityItem(**d) for d in data]
            except Exception:
                pass

        existing.append(item)
        self._save_items(existing)

        profile = self._load_profile()
        profile.templates_published += 1
        self._save_profile(profile)

        return item

    def browse_templates(
        self,
        category: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> List[CommunityItem]:
        """Browse community templates with optional filtering.

        Args:
            category: Filter by category
            query: Search query
            limit: Maximum results

        Returns:
            List of matching CommunityItem objects
        """
        items = self._load_items()
        results = [i for i in items if i.item_type == "template"]

        if category:
            category_lower = category.lower()
            results = [
                i
                for i in results
                if i.category.lower() == category_lower
                or any(category_lower in t.lower() for t in i.tags)
            ]

        if query:
            query_lower = query.lower()
            results = [
                i
                for i in results
                if query_lower in i.name.lower()
                or query_lower in i.description.lower()
                or any(query_lower in t.lower() for t in i.tags)
            ]

        # Sort by rating/downloads
        results.sort(key=lambda i: (i.rating, i.downloads), reverse=True)
        return results[:limit]

    def browse_plugins(
        self,
        category: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> List[CommunityItem]:
        """Browse community plugins.

        Args:
            category: Filter by category
            query: Search query
            limit: Maximum results

        Returns:
            List of matching plugin CommunityItem objects
        """
        items = self._load_items()
        results = [i for i in items if i.item_type == "plugin"]

        if category:
            results = [i for i in results if i.category.lower() == category.lower()]

        if query:
            query_lower = query.lower()
            results = [
                i
                for i in results
                if query_lower in i.name.lower() or query_lower in i.description.lower()
            ]

        results.sort(key=lambda i: (i.rating, i.downloads), reverse=True)
        return results[:limit]

    def get_awards(self) -> List[Achievement]:
        """Get all achievements with earned status.

        Returns:
            List of Achievement objects
        """
        profile = self._load_profile()
        earned_ids = {a.id for a in profile.achievements if a.earned}

        awards = []
        for ach_data in ACHIEVEMENTS:
            earned = ach_data["id"] in earned_ids
            earned_at = None
            for pa in profile.achievements:
                if pa.id == ach_data["id"] and pa.earned:
                    earned_at = pa.earned_at
                    break

            awards.append(
                Achievement(
                    id=ach_data["id"],
                    name=ach_data["name"],
                    description=ach_data["description"],
                    icon=ach_data["icon"],
                    category=ach_data["category"],
                    points=ach_data["points"],
                    earned=earned,
                    earned_at=earned_at,
                )
            )

        return awards

    def earn_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Mark an achievement as earned.

        Args:
            achievement_id: ID of the achievement to earn

        Returns:
            The earned Achievement, or None if not found or already earned
        """
        ach_data = None
        for a in ACHIEVEMENTS:
            if a["id"] == achievement_id:
                ach_data = a
                break

        if ach_data is None:
            return None

        profile = self._load_profile()
        for existing in profile.achievements:
            if existing.id == achievement_id and existing.earned:
                return None  # Already earned

        achievement = Achievement(
            id=ach_data["id"],
            name=ach_data["name"],
            description=ach_data["description"],
            icon=ach_data["icon"],
            category=ach_data["category"],
            points=ach_data["points"],
            earned=True,
            earned_at=datetime.now(timezone.utc).isoformat(),
        )

        profile.achievements.append(achievement)
        profile.total_points += ach_data["points"]
        self._save_profile(profile)

        return achievement

    def get_profile(self) -> UserProfile:
        """Get the current user profile.

        Returns:
            UserProfile with stats and achievements
        """
        return self._load_profile()

    def get_community_stats(self) -> CommunityStats:
        """Get community statistics.

        Returns:
            CommunityStats with aggregate data
        """
        items = self._load_items()

        categories: Dict[str, int] = {}
        for item in items:
            categories[item.category] = categories.get(item.category, 0) + 1

        plugins = [i for i in items if i.item_type == "plugin"]
        templates = [i for i in items if i.item_type == "template"]

        top_items = sorted(items, key=lambda i: i.rating, reverse=True)[:5]

        return CommunityStats(
            total_plugins=len(plugins),
            total_templates=len(templates),
            total_users=1,
            categories=categories,
            top_items=top_items,
        )
