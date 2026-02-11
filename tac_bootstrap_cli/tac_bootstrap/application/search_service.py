"""
IDK: search-service, full-text-search, metadata-filtering, command-search, template-search
Responsibility: Provides full-text search with metadata filtering across commands, templates,
                and features in the TAC Bootstrap ecosystem
Invariants: Case-insensitive search, supports tag/model/framework/architecture filters,
            returns ranked results

Example usage:
    from tac_bootstrap.application.search_service import SearchService

    service = SearchService()
    results = service.search_commands(query="testing", tag="test", model="opus")
    results = service.search_templates(framework="fastapi", architecture="ddd")
    results = service.search_features(query="performance", tier="critical")
"""

import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    """A single search result entry."""

    name: str = Field(..., description="Item name")
    category: str = Field(..., description="Category: command, template, feature, workflow")
    description: str = Field(default="", description="Item description")
    tags: List[str] = Field(default_factory=list, description="Associated tags")
    relevance_score: float = Field(default=0.0, description="Relevance score (0-1)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    path: Optional[str] = Field(default=None, description="File path if applicable")


class SearchResults(BaseModel):
    """Collection of search results."""

    query: str = Field(default="", description="Original query string")
    total: int = Field(default=0, description="Total number of results")
    results: List[SearchResult] = Field(default_factory=list, description="Search result items")
    filters_applied: Dict[str, str] = Field(
        default_factory=dict, description="Filters that were applied"
    )


# Built-in command catalog for searching
COMMAND_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "/prime",
        "category": "command",
        "description": "Prepare context and load project knowledge",
        "tags": ["context", "setup", "initialization"],
        "metadata": {"model": "sonnet", "phase": "preparation"},
    },
    {
        "name": "/scout",
        "category": "command",
        "description": "Explore codebase to find relevant files for a task",
        "tags": ["exploration", "codebase", "search", "files"],
        "metadata": {"model": "sonnet", "phase": "exploration"},
    },
    {
        "name": "/feature",
        "category": "command",
        "description": "Plan and design a new feature",
        "tags": ["planning", "feature", "design"],
        "metadata": {"model": "opus", "phase": "planning"},
    },
    {
        "name": "/implement",
        "category": "command",
        "description": "Execute implementation plan",
        "tags": ["implementation", "coding", "build"],
        "metadata": {"model": "opus", "phase": "implementation"},
    },
    {
        "name": "/test",
        "category": "command",
        "description": "Run tests and validate implementation",
        "tags": ["testing", "validation", "quality"],
        "metadata": {"model": "sonnet", "phase": "testing"},
    },
    {
        "name": "/review",
        "category": "command",
        "description": "Review code changes and provide feedback",
        "tags": ["review", "quality", "feedback"],
        "metadata": {"model": "opus", "phase": "review"},
    },
    {
        "name": "/commit",
        "category": "command",
        "description": "Create a git commit with descriptive message",
        "tags": ["git", "commit", "version-control"],
        "metadata": {"model": "sonnet", "phase": "shipping"},
    },
    {
        "name": "/ship",
        "category": "command",
        "description": "Ship changes - create PR and merge",
        "tags": ["shipping", "pr", "merge", "deploy"],
        "metadata": {"model": "sonnet", "phase": "shipping"},
    },
    {
        "name": "/build",
        "category": "command",
        "description": "Build the project",
        "tags": ["build", "compile", "package"],
        "metadata": {"model": "sonnet", "phase": "building"},
    },
    {
        "name": "/start",
        "category": "command",
        "description": "Start the development server",
        "tags": ["start", "server", "development"],
        "metadata": {"model": "sonnet", "phase": "development"},
    },
    {
        "name": "adw_sdlc_iso",
        "category": "workflow",
        "description": "Full SDLC workflow: plan, build, test, review, document",
        "tags": ["sdlc", "full-cycle", "workflow", "automated"],
        "metadata": {"model": "opus", "phases": 5},
    },
    {
        "name": "adw_patch_iso",
        "category": "workflow",
        "description": "Quick patch workflow for small fixes",
        "tags": ["patch", "fix", "quick", "workflow"],
        "metadata": {"model": "sonnet", "phases": 3},
    },
    {
        "name": "adw_plan_iso",
        "category": "workflow",
        "description": "Isolated planning workflow",
        "tags": ["planning", "design", "workflow"],
        "metadata": {"model": "opus", "phases": 1},
    },
]

# Built-in template catalog
TEMPLATE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "fastapi-ddd",
        "category": "template",
        "description": "FastAPI project with DDD architecture",
        "tags": ["python", "fastapi", "ddd", "api"],
        "metadata": {"framework": "fastapi", "architecture": "ddd", "language": "python"},
    },
    {
        "name": "fastapi-simple",
        "category": "template",
        "description": "Simple FastAPI project",
        "tags": ["python", "fastapi", "simple", "api"],
        "metadata": {"framework": "fastapi", "architecture": "simple", "language": "python"},
    },
    {
        "name": "nextjs-react",
        "category": "template",
        "description": "Next.js React application",
        "tags": ["typescript", "nextjs", "react", "frontend"],
        "metadata": {"framework": "nextjs", "architecture": "simple", "language": "typescript"},
    },
    {
        "name": "express-layered",
        "category": "template",
        "description": "Express.js with layered architecture",
        "tags": ["javascript", "express", "layered", "api"],
        "metadata": {"framework": "express", "architecture": "layered", "language": "javascript"},
    },
    {
        "name": "django-clean",
        "category": "template",
        "description": "Django with clean architecture",
        "tags": ["python", "django", "clean", "web"],
        "metadata": {"framework": "django", "architecture": "clean", "language": "python"},
    },
    {
        "name": "gin-hexagonal",
        "category": "template",
        "description": "Go Gin with hexagonal architecture",
        "tags": ["go", "gin", "hexagonal", "api"],
        "metadata": {"framework": "gin", "architecture": "hexagonal", "language": "go"},
    },
]

# Feature catalog
FEATURE_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "scaffolding",
        "category": "feature",
        "description": "Project scaffolding with templates and configuration",
        "tags": ["scaffolding", "init", "setup", "generation"],
        "metadata": {"tier": "core", "status": "stable"},
    },
    {
        "name": "validation",
        "category": "feature",
        "description": "Configuration and system requirement validation",
        "tags": ["validation", "health-check", "doctor", "quality"],
        "metadata": {"tier": "core", "status": "stable"},
    },
    {
        "name": "entity-generation",
        "category": "feature",
        "description": "CRUD entity code generation with vertical slices",
        "tags": ["entity", "crud", "generation", "code"],
        "metadata": {"tier": "core", "status": "stable"},
    },
    {
        "name": "upgrade",
        "category": "feature",
        "description": "Upgrade agentic layer to latest version",
        "tags": ["upgrade", "update", "migration", "version"],
        "metadata": {"tier": "core", "status": "stable"},
    },
    {
        "name": "telemetry",
        "category": "feature",
        "description": "Anonymous usage tracking and analytics",
        "tags": ["telemetry", "analytics", "tracking", "performance"],
        "metadata": {"tier": "optional", "status": "stable"},
    },
    {
        "name": "orchestrator",
        "category": "feature",
        "description": "Backend orchestrator with WebSocket notifications",
        "tags": ["orchestrator", "backend", "websocket", "dashboard"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "i18n",
        "category": "feature",
        "description": "Multi-language support for CLI output",
        "tags": ["i18n", "language", "translation", "internationalization"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "ai-generation",
        "category": "feature",
        "description": "AI-assisted code generation using Claude API",
        "tags": ["ai", "generation", "code", "claude", "api"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "snapshots",
        "category": "feature",
        "description": "Project history and snapshot management",
        "tags": ["snapshot", "backup", "restore", "history", "version"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "metrics",
        "category": "feature",
        "description": "Project analytics, complexity, and health metrics",
        "tags": ["metrics", "analytics", "complexity", "coverage", "performance"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "recommendations",
        "category": "feature",
        "description": "Smart recommendations for project improvements",
        "tags": ["recommend", "suggest", "improve", "security", "performance"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
    {
        "name": "web-dashboard",
        "category": "feature",
        "description": "Web UI for project management and monitoring",
        "tags": ["dashboard", "web", "ui", "monitoring", "management"],
        "metadata": {"tier": "premium", "status": "stable"},
    },
]


class SearchService:
    """
    IDK: search-core, full-text-search, metadata-filter, result-ranking
    Responsibility: Searches across commands, templates, and features with filtering and ranking
    Invariants: Case-insensitive, returns results sorted by relevance, supports multiple filters
    """

    def __init__(self) -> None:
        """Initialize search service with built-in catalogs."""
        self._commands = COMMAND_CATALOG
        self._templates = TEMPLATE_CATALOG
        self._features = FEATURE_CATALOG
        self._all_items = self._commands + self._templates + self._features

    def _compute_relevance(self, item: Dict[str, Any], query: str) -> float:
        """Compute relevance score for an item against a query.

        Args:
            item: Catalog item
            query: Search query

        Returns:
            Relevance score between 0 and 1
        """
        if not query:
            return 0.5  # Default score when no query

        query_lower = query.lower()
        score = 0.0

        # Name match (highest weight)
        name = item.get("name", "").lower()
        if query_lower == name:
            score += 1.0
        elif query_lower in name:
            score += 0.8
        elif any(q in name for q in query_lower.split()):
            score += 0.6

        # Description match
        desc = item.get("description", "").lower()
        if query_lower in desc:
            score += 0.4
        elif any(q in desc for q in query_lower.split()):
            score += 0.2

        # Tag match
        tags = [t.lower() for t in item.get("tags", [])]
        for tag in tags:
            if query_lower == tag:
                score += 0.6
            elif query_lower in tag:
                score += 0.3

        # Normalize to 0-1
        return min(score, 1.0)

    def _matches_filters(self, item: Dict[str, Any], **filters: Optional[str]) -> bool:
        """Check if item matches all provided filters.

        Args:
            item: Catalog item
            **filters: Key-value filter pairs

        Returns:
            True if item matches all filters
        """
        metadata = item.get("metadata", {})
        tags = [t.lower() for t in item.get("tags", [])]

        for key, value in filters.items():
            if value is None:
                continue
            value_lower = value.lower()

            if key == "tag":
                if not any(value_lower in t for t in tags):
                    return False
            elif key == "category":
                if item.get("category", "").lower() != value_lower:
                    return False
            elif key in metadata:
                if str(metadata[key]).lower() != value_lower:
                    return False

        return True

    def search(
        self,
        query: str = "",
        category: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 20,
        **filters: Optional[str],
    ) -> SearchResults:
        """Search across all catalogs with optional filters.

        Args:
            query: Search query string
            category: Filter by category (command, template, feature, workflow)
            tag: Filter by tag
            limit: Maximum results to return
            **filters: Additional metadata filters

        Returns:
            SearchResults with ranked results
        """
        all_filters = {"category": category, "tag": tag, **filters}
        applied_filters = {k: v for k, v in all_filters.items() if v is not None}

        results: List[SearchResult] = []

        for item in self._all_items:
            if not self._matches_filters(item, **all_filters):
                continue

            relevance = self._compute_relevance(item, query) if query else 0.5

            if relevance > 0 or not query:
                results.append(
                    SearchResult(
                        name=item["name"],
                        category=item.get("category", "unknown"),
                        description=item.get("description", ""),
                        tags=item.get("tags", []),
                        relevance_score=relevance,
                        metadata=item.get("metadata", {}),
                        path=item.get("path"),
                    )
                )

        # Sort by relevance
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        results = results[:limit]

        return SearchResults(
            query=query,
            total=len(results),
            results=results,
            filters_applied=applied_filters,
        )

    def search_commands(
        self,
        query: str = "",
        tag: Optional[str] = None,
        model: Optional[str] = None,
    ) -> SearchResults:
        """Search within commands and workflows.

        Args:
            query: Search query
            tag: Filter by tag
            model: Filter by model (opus, sonnet, haiku)

        Returns:
            SearchResults filtered to commands/workflows
        """
        return self.search(
            query=query,
            tag=tag,
            model=model,
            category=None,  # Include both commands and workflows
        )

    def search_templates(
        self,
        query: str = "",
        framework: Optional[str] = None,
        architecture: Optional[str] = None,
        language: Optional[str] = None,
    ) -> SearchResults:
        """Search within templates.

        Args:
            query: Search query
            framework: Filter by framework
            architecture: Filter by architecture
            language: Filter by programming language

        Returns:
            SearchResults filtered to templates
        """
        return self.search(
            query=query,
            category="template",
            framework=framework,
            architecture=architecture,
            language=language,
        )

    def search_features(
        self,
        query: str = "",
        tier: Optional[str] = None,
        status: Optional[str] = None,
    ) -> SearchResults:
        """Search within features.

        Args:
            query: Search query
            tier: Filter by tier (core, optional, premium)
            status: Filter by status (stable, beta, experimental)

        Returns:
            SearchResults filtered to features
        """
        return self.search(
            query=query,
            category="feature",
            tier=tier,
            status=status,
        )
