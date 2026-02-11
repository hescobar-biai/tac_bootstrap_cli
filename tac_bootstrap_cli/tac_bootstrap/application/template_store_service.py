"""
IDK: template-management, template-search, template-install, template-rating
Responsibility: Provides high-level template store operations for CLI commands
Invariants: Delegates to TemplateStore for storage, provides formatted output,
            handles errors gracefully with user-friendly messages
"""

from typing import Any, Dict, List, Optional

from tac_bootstrap.infrastructure.template_store import TemplateMetadata, TemplateStore

# ============================================================================
# TEMPLATE STORE SERVICE
# ============================================================================


class TemplateStoreService:
    """
    IDK: template-store-facade, template-operations, cli-integration
    Responsibility: Provides application-level template management operations
                    including search, install, list, rate, and metadata retrieval
    Invariants: All operations return structured results, errors produce clear messages,
                store state is always consistent after operations
    """

    def __init__(self, store: Optional[TemplateStore] = None) -> None:
        """
        Initialize TemplateStoreService.

        Args:
            store: Optional TemplateStore instance (created with defaults if not provided)
        """
        self.store = store or TemplateStore()

    def search_templates(
        self,
        query: str = "",
        tags: Optional[List[str]] = None,
        author: Optional[str] = None,
        min_rating: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for templates matching the given criteria.

        Args:
            query: Search query string
            tags: Optional list of tags to filter by
            author: Optional author name to filter by
            min_rating: Optional minimum rating to filter by

        Returns:
            List of template metadata dictionaries sorted by relevance
        """
        filters: Dict[str, Any] = {}
        if tags:
            filters["tags"] = tags
        if author:
            filters["author"] = author
        if min_rating is not None:
            filters["min_rating"] = min_rating

        results = self.store.search(query=query, filters=filters)
        return [t.model_dump() for t in results]

    def install_template(
        self,
        template_id: str,
        version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Install a template from the registry.

        Handles the template_id:version format (e.g., "user/template:1.0.0").

        Args:
            template_id: Template identifier (may include :version suffix)
            version: Optional explicit version override

        Returns:
            Dict with 'success', 'message', and optional 'template' keys
        """
        # Parse template_id:version format
        parsed_id = template_id
        parsed_version = version

        if ":" in template_id and version is None:
            parts = template_id.split(":", 1)
            parsed_id = parts[0]
            parsed_version = parts[1]

        if not self.store.template_exists(parsed_id):
            return {
                "success": False,
                "message": f"Template '{parsed_id}' not found in registry. "
                "Use 'tac-bootstrap template search' to find available templates.",
            }

        success = self.store.install(parsed_id, version=parsed_version)
        if success:
            metadata = self.store.get_metadata(parsed_id)
            return {
                "success": True,
                "message": f"Template '{parsed_id}' installed successfully",
                "template": metadata,
            }
        else:
            return {
                "success": False,
                "message": f"Failed to install template '{parsed_id}'",
            }

    def uninstall_template(self, template_id: str) -> Dict[str, Any]:
        """
        Uninstall a template.

        Args:
            template_id: Template identifier to uninstall

        Returns:
            Dict with 'success' and 'message' keys
        """
        if not self.store.template_exists(template_id):
            return {
                "success": False,
                "message": f"Template '{template_id}' not found in registry",
            }

        success = self.store.uninstall(template_id)
        if success:
            return {
                "success": True,
                "message": f"Template '{template_id}' uninstalled successfully",
            }
        else:
            return {
                "success": False,
                "message": f"Failed to uninstall template '{template_id}'",
            }

    def list_installed_templates(self) -> List[Dict[str, Any]]:
        """
        List all installed templates.

        Returns:
            List of installed template metadata dictionaries
        """
        return [t.model_dump() for t in self.store.list_installed()]

    def list_all_templates(self) -> List[Dict[str, Any]]:
        """
        List all templates in the registry.

        Returns:
            List of all template metadata dictionaries
        """
        return [t.model_dump() for t in self.store.list_all()]

    def rate_template(self, template_id: str, rating: int) -> Dict[str, Any]:
        """
        Rate a template (1-5 stars).

        Args:
            template_id: Template identifier to rate
            rating: Rating value (1-5)

        Returns:
            Dict with 'success', 'message', and optional 'new_rating' keys
        """
        if not 1 <= rating <= 5:
            return {
                "success": False,
                "message": "Rating must be between 1 and 5",
            }

        if not self.store.template_exists(template_id):
            return {
                "success": False,
                "message": f"Template '{template_id}' not found in registry",
            }

        try:
            success = self.store.rate(template_id, rating)
            if success:
                metadata = self.store.get_metadata(template_id)
                new_rating = metadata.get("rating", 0.0) if metadata else 0.0
                return {
                    "success": True,
                    "message": f"Template '{template_id}' rated {rating}/5",
                    "new_rating": new_rating,
                }
            return {
                "success": False,
                "message": f"Failed to rate template '{template_id}'",
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e),
            }

    def get_template_info(self, template_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a template.

        Args:
            template_id: Template identifier

        Returns:
            Template metadata dictionary, or None if not found
        """
        return self.store.get_metadata(template_id)

    def add_template(
        self,
        template_id: str,
        name: str,
        description: str = "",
        author: str = "",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Add a new template to the registry.

        Args:
            template_id: Unique template identifier
            name: Human-readable template name
            description: Template description
            author: Template author
            version: Semantic version string
            tags: List of searchable tags

        Returns:
            Dict with 'success' and 'message' keys
        """
        try:
            template = TemplateMetadata(
                id=template_id,
                name=name,
                description=description,
                author=author,
                version=version,
                tags=tags or [],
            )
            self.store.add_template(template)
            return {
                "success": True,
                "message": f"Template '{template_id}' added to registry",
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to add template: {e}",
            }

    def seed_defaults(self) -> int:
        """
        Seed the registry with default templates.

        Returns:
            Number of templates in registry after seeding
        """
        self.store.seed_defaults()
        return self.store.template_count

    @property
    def template_count(self) -> int:
        """Total number of templates in registry."""
        return self.store.template_count

    @property
    def installed_count(self) -> int:
        """Number of installed templates."""
        return self.store.installed_count
