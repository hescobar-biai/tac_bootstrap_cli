"""
IDK: template-registry, template-search, template-metadata, local-store
Responsibility: Manages a local registry of reusable project templates with search,
                install, rating, and metadata capabilities
Invariants: Registry is stored as JSON, operations are idempotent, template IDs are unique,
            ratings are 1-5, all IO errors are handled gracefully
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

# ============================================================================
# TEMPLATE MODEL
# ============================================================================


class TemplateMetadata(BaseModel):
    """
    Metadata for a reusable project template.

    Attributes:
        id: Unique template identifier (author/name format)
        name: Human-readable template name
        description: Short description of what the template provides
        version: Semantic version string
        author: Template author name
        downloads: Number of times template has been installed
        rating: Average rating (1.0-5.0)
        rating_count: Number of ratings received
        tags: List of searchable tags
        dependencies: List of required dependencies
        created_at: ISO8601 timestamp of template creation
        updated_at: ISO8601 timestamp of last update
        source_url: Optional URL to template source repository
        installed: Whether this template is installed locally
        install_path: Local path where template is installed
    """

    id: str = Field(..., description="Unique template ID (author/name format)")
    name: str = Field(..., description="Human-readable template name")
    description: str = Field(default="", description="Template description")
    version: str = Field(default="1.1.0", description="Semantic version")
    author: str = Field(default="", description="Template author")
    downloads: int = Field(default=0, description="Download count", ge=0)
    rating: float = Field(default=0.0, description="Average rating (1-5)", ge=0.0, le=5.0)
    rating_count: int = Field(default=0, description="Number of ratings", ge=0)
    tags: List[str] = Field(default_factory=list, description="Searchable tags")
    dependencies: List[str] = Field(default_factory=list, description="Required dependencies")
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Creation timestamp",
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="Last update timestamp",
    )
    source_url: Optional[str] = Field(default=None, description="Source repository URL")
    installed: bool = Field(default=False, description="Whether installed locally")
    install_path: Optional[str] = Field(default=None, description="Local installation path")

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate template ID format (author/name or simple name)."""
        if not v or not v.strip():
            raise ValueError("Template ID cannot be empty")
        return v.strip()


# ============================================================================
# TEMPLATE STORE
# ============================================================================


class TemplateStore:
    """
    IDK: template-registry-manager, local-json-storage, search-engine
    Responsibility: Manages a local JSON-based template registry with CRUD operations,
                    search, filtering, rating, and installation tracking
    Invariants: Registry is persisted to disk after mutations, template IDs are unique,
                search is case-insensitive, ratings are bounded 1-5
    """

    DEFAULT_STORE_DIR = Path.home() / ".tac-bootstrap" / "template-store"

    def __init__(self, store_dir: Optional[Path] = None) -> None:
        """
        Initialize the template store.

        Args:
            store_dir: Directory for template storage (default: ~/.tac-bootstrap/template-store/)
        """
        self.store_dir = store_dir or self.DEFAULT_STORE_DIR
        self.registry_file = self.store_dir / "registry.json"
        self.templates_dir = self.store_dir / "templates"
        self._registry: Dict[str, TemplateMetadata] = {}

        # Ensure storage directories exist
        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)

        # Load existing registry
        self._load_registry()

    def _load_registry(self) -> None:
        """Load the template registry from disk."""
        if not self.registry_file.is_file():
            self._registry = {}
            return

        try:
            with open(self.registry_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

            self._registry = {}
            for template_id, template_data in raw_data.items():
                try:
                    self._registry[template_id] = TemplateMetadata(**template_data)
                except Exception:
                    # Skip invalid entries
                    continue
        except (json.JSONDecodeError, OSError):
            self._registry = {}

    def _save_registry(self) -> None:
        """Save the template registry to disk."""
        try:
            data = {
                tid: tmpl.model_dump()
                for tid, tmpl in self._registry.items()
            }
            with open(self.registry_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except OSError:
            pass  # Gracefully handle write failures

    # ========================================================================
    # SEARCH AND QUERY
    # ========================================================================

    def search(
        self,
        query: str = "",
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[TemplateMetadata]:
        """
        Search templates by query string and optional filters.

        Searches across template name, description, tags, and author.
        Search is case-insensitive.

        Args:
            query: Search query string (matched against name, description, tags, author)
            filters: Optional filters dict:
                - tags: List[str] - filter by tags (any match)
                - author: str - filter by author
                - min_rating: float - minimum rating
                - installed: bool - filter by installation status

        Returns:
            List of matching TemplateMetadata, sorted by relevance (downloads)
        """
        results: List[TemplateMetadata] = []
        query_lower = query.lower().strip()
        filters = filters or {}

        for template in self._registry.values():
            # Text search
            if query_lower:
                searchable = " ".join([
                    template.name.lower(),
                    template.description.lower(),
                    template.author.lower(),
                    " ".join(t.lower() for t in template.tags),
                    template.id.lower(),
                ])
                if query_lower not in searchable:
                    continue

            # Apply filters
            if "tags" in filters:
                filter_tags = {t.lower() for t in filters["tags"]}
                template_tags = {t.lower() for t in template.tags}
                if not filter_tags.intersection(template_tags):
                    continue

            if "author" in filters:
                if template.author.lower() != filters["author"].lower():
                    continue

            if "min_rating" in filters:
                if template.rating < filters["min_rating"]:
                    continue

            if "installed" in filters:
                if template.installed != filters["installed"]:
                    continue

            results.append(template)

        # Sort by downloads (most popular first)
        results.sort(key=lambda t: t.downloads, reverse=True)
        return results

    def install(self, template_id: str, version: Optional[str] = None) -> bool:
        """
        Install a template from the registry.

        Marks the template as installed and creates a local directory for it.

        Args:
            template_id: Template identifier to install
            version: Optional specific version to install (uses latest if not specified)

        Returns:
            True if installation succeeded, False if template not found
        """
        template = self._registry.get(template_id)
        if template is None:
            return False

        # Create installation directory
        install_dir = self.templates_dir / template_id.replace("/", "_")
        install_dir.mkdir(parents=True, exist_ok=True)

        # Update metadata
        template.installed = True
        template.install_path = str(install_dir)
        template.downloads += 1
        template.updated_at = datetime.now(timezone.utc).isoformat()

        if version:
            template.version = version

        self._save_registry()
        return True

    def uninstall(self, template_id: str) -> bool:
        """
        Uninstall a template.

        Removes the local installation and updates metadata.

        Args:
            template_id: Template identifier to uninstall

        Returns:
            True if uninstallation succeeded, False if template not found
        """
        template = self._registry.get(template_id)
        if template is None:
            return False

        # Remove installation directory if it exists
        if template.install_path:
            install_dir = Path(template.install_path)
            if install_dir.is_dir():
                shutil.rmtree(install_dir, ignore_errors=True)

        template.installed = False
        template.install_path = None
        self._save_registry()
        return True

    def list_installed(self) -> List[TemplateMetadata]:
        """
        List all installed templates.

        Returns:
            List of installed TemplateMetadata instances
        """
        return [t for t in self._registry.values() if t.installed]

    def list_all(self) -> List[TemplateMetadata]:
        """
        List all templates in the registry.

        Returns:
            List of all TemplateMetadata instances, sorted by name
        """
        return sorted(self._registry.values(), key=lambda t: t.name)

    def rate(self, template_id: str, rating: int) -> bool:
        """
        Rate a template (1-5 stars).

        Updates the template's average rating using incremental averaging.

        Args:
            template_id: Template identifier to rate
            rating: Rating value (1-5)

        Returns:
            True if rating was recorded, False if template not found

        Raises:
            ValueError: If rating is not between 1 and 5
        """
        if not 1 <= rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {rating}")

        template = self._registry.get(template_id)
        if template is None:
            return False

        # Incremental average calculation
        total_rating = template.rating * template.rating_count
        template.rating_count += 1
        template.rating = round((total_rating + rating) / template.rating_count, 2)
        template.updated_at = datetime.now(timezone.utc).isoformat()

        self._save_registry()
        return True

    def get_metadata(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full metadata for a template.

        Args:
            template_id: Template identifier

        Returns:
            Template metadata as dictionary, or None if not found
        """
        template = self._registry.get(template_id)
        if template is None:
            return None
        return template.model_dump()

    # ========================================================================
    # REGISTRY MANAGEMENT
    # ========================================================================

    def add_template(self, template: TemplateMetadata) -> None:
        """
        Add or update a template in the registry.

        Args:
            template: TemplateMetadata instance to add
        """
        self._registry[template.id] = template
        self._save_registry()

    def remove_template(self, template_id: str) -> bool:
        """
        Remove a template from the registry entirely.

        Args:
            template_id: Template identifier to remove

        Returns:
            True if template was found and removed, False otherwise
        """
        if template_id not in self._registry:
            return False

        # Uninstall first if installed
        template = self._registry[template_id]
        if template.installed and template.install_path:
            install_dir = Path(template.install_path)
            if install_dir.is_dir():
                shutil.rmtree(install_dir, ignore_errors=True)

        del self._registry[template_id]
        self._save_registry()
        return True

    def template_exists(self, template_id: str) -> bool:
        """
        Check if a template exists in the registry.

        Args:
            template_id: Template identifier to check

        Returns:
            True if template exists
        """
        return template_id in self._registry

    @property
    def template_count(self) -> int:
        """Total number of templates in the registry."""
        return len(self._registry)

    @property
    def installed_count(self) -> int:
        """Number of installed templates."""
        return sum(1 for t in self._registry.values() if t.installed)

    def seed_defaults(self) -> None:
        """
        Seed the registry with default built-in templates.

        Adds a set of starter templates that come bundled with TAC Bootstrap.
        Does not overwrite existing templates.
        """
        defaults = [
            TemplateMetadata(
                id="tac/fastapi-starter",
                name="FastAPI Starter",
                description="Production-ready FastAPI template with DDD architecture",
                version="1.1.0",
                author="TAC Bootstrap Team",
                tags=["python", "fastapi", "ddd", "api", "starter"],
            ),
            TemplateMetadata(
                id="tac/nextjs-starter",
                name="Next.js Starter",
                description="Next.js template with TypeScript and Tailwind CSS",
                version="1.1.0",
                author="TAC Bootstrap Team",
                tags=["typescript", "nextjs", "react", "frontend", "starter"],
            ),
            TemplateMetadata(
                id="tac/fullstack-starter",
                name="Fullstack Starter",
                description="FastAPI backend + Next.js frontend with orchestrator",
                version="1.1.0",
                author="TAC Bootstrap Team",
                tags=["python", "typescript", "fastapi", "nextjs", "fullstack"],
            ),
            TemplateMetadata(
                id="tac/cli-starter",
                name="CLI Tool Starter",
                description="Python CLI tool template with Typer and Rich",
                version="1.1.0",
                author="TAC Bootstrap Team",
                tags=["python", "cli", "typer", "rich", "starter"],
            ),
            TemplateMetadata(
                id="tac/microservice-starter",
                name="Microservice Starter",
                description="Microservice template with Docker, health checks, and observability",
                version="1.1.0",
                author="TAC Bootstrap Team",
                tags=["python", "docker", "microservice", "api", "observability"],
            ),
        ]

        for template in defaults:
            if template.id not in self._registry:
                self._registry[template.id] = template

        self._save_registry()
