"""
IDK: learning-service, tutorials, educational-mode, best-practices, architecture-patterns
Responsibility: Provides interactive tutorials, best practices guides, and architecture
                pattern explanations for new TAC Bootstrap users
Invariants: Content is built-in (no network required), supports multiple topics,
            tutorials have progressive difficulty levels

Example usage:
    from tac_bootstrap.application.learning_service import LearningService

    service = LearningService()
    content = service.get_topic("ddd")
    tutorial = service.get_tutorial("quick-start")
    topics = service.list_topics()
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LearningTopic(BaseModel):
    """A learning topic with structured content."""

    id: str = Field(..., description="Topic identifier")
    title: str = Field(..., description="Topic title")
    description: str = Field(default="", description="Brief description")
    difficulty: str = Field(default="beginner", description="beginner, intermediate, advanced")
    sections: List[Dict[str, str]] = Field(
        default_factory=list, description="Ordered list of sections with title and content"
    )
    examples: List[Dict[str, str]] = Field(
        default_factory=list, description="Code examples with title and code"
    )
    related_topics: List[str] = Field(
        default_factory=list, description="IDs of related topics"
    )
    tags: List[str] = Field(default_factory=list, description="Topic tags for search")


class Tutorial(BaseModel):
    """An interactive tutorial with steps."""

    id: str = Field(..., description="Tutorial identifier")
    title: str = Field(..., description="Tutorial title")
    description: str = Field(default="", description="Tutorial description")
    difficulty: str = Field(default="beginner", description="Difficulty level")
    estimated_minutes: int = Field(default=10, description="Estimated time in minutes")
    steps: List[Dict[str, str]] = Field(
        default_factory=list, description="Ordered tutorial steps with title, instruction, command"
    )
    prerequisites: List[str] = Field(
        default_factory=list, description="Required knowledge/setup"
    )


# Built-in learning topics
TOPICS: Dict[str, LearningTopic] = {
    "ddd": LearningTopic(
        id="ddd",
        title="Domain-Driven Design (DDD)",
        description="Learn how TAC Bootstrap implements DDD patterns for structured project architecture",
        difficulty="intermediate",
        sections=[
            {
                "title": "What is DDD?",
                "content": (
                    "Domain-Driven Design is a software design approach that focuses on "
                    "modeling software to match business domains. In TAC Bootstrap, DDD "
                    "structures your code into clear layers:\n\n"
                    "- **Domain**: Core business logic, entities, value objects\n"
                    "- **Application**: Use cases, services, orchestration\n"
                    "- **Infrastructure**: Database, external APIs, file system\n"
                    "- **Interfaces**: CLI, API endpoints, UI"
                ),
            },
            {
                "title": "DDD in TAC Bootstrap",
                "content": (
                    "When you create a project with --architecture ddd, TAC Bootstrap "
                    "generates:\n\n"
                    "  src/\n"
                    "    domain/       # Entities, value objects, repositories (interfaces)\n"
                    "    application/  # Services, DTOs, use cases\n"
                    "    infrastructure/ # Repository implementations, adapters\n"
                    "    interfaces/   # API routes, CLI commands\n\n"
                    "Each layer has clear dependency rules: inner layers never depend on "
                    "outer layers."
                ),
            },
            {
                "title": "Key Concepts",
                "content": (
                    "**Entities**: Objects with identity (User, Product, Order)\n"
                    "**Value Objects**: Immutable objects without identity (Email, Money)\n"
                    "**Aggregates**: Clusters of entities treated as a unit\n"
                    "**Repositories**: Abstraction over data persistence\n"
                    "**Services**: Domain logic that doesn't belong to an entity"
                ),
            },
        ],
        examples=[
            {
                "title": "Entity Example",
                "code": (
                    "from pydantic import BaseModel, Field\n"
                    "from uuid import UUID, uuid4\n\n"
                    "class Product(BaseModel):\n"
                    '    id: UUID = Field(default_factory=uuid4)\n'
                    '    name: str = Field(..., min_length=1)\n'
                    '    price: float = Field(..., gt=0)\n'
                    '    category: str = Field(default="general")\n'
                ),
            },
            {
                "title": "Repository Pattern",
                "code": (
                    "from abc import ABC, abstractmethod\n\n"
                    "class ProductRepository(ABC):\n"
                    "    @abstractmethod\n"
                    "    async def get_by_id(self, id: UUID) -> Product: ...\n\n"
                    "    @abstractmethod\n"
                    "    async def save(self, product: Product) -> None: ...\n"
                ),
            },
        ],
        related_topics=["clean-architecture", "hexagonal", "architecture"],
        tags=["ddd", "architecture", "domain", "design"],
    ),
    "architecture": LearningTopic(
        id="architecture",
        title="Architecture Patterns",
        description="Overview of all architecture patterns supported by TAC Bootstrap",
        difficulty="beginner",
        sections=[
            {
                "title": "Available Patterns",
                "content": (
                    "TAC Bootstrap supports 5 architecture patterns:\n\n"
                    "1. **Simple**: Flat structure, good for small projects\n"
                    "2. **Layered**: Traditional 3-layer (presentation, business, data)\n"
                    "3. **DDD**: Domain-Driven Design with bounded contexts\n"
                    "4. **Clean**: Clean Architecture with dependency inversion\n"
                    "5. **Hexagonal**: Ports and Adapters pattern"
                ),
            },
            {
                "title": "Choosing a Pattern",
                "content": (
                    "**Simple**: Prototype, script, small tool (< 5 files)\n"
                    "**Layered**: Small to medium API (5-20 files)\n"
                    "**DDD**: Medium to large domain-heavy apps (20+ files)\n"
                    "**Clean**: Large apps with multiple delivery mechanisms\n"
                    "**Hexagonal**: Large apps with many external integrations"
                ),
            },
        ],
        examples=[
            {
                "title": "Creating with Architecture",
                "code": (
                    "# Simple\n"
                    "tac-bootstrap init my-script --architecture simple\n\n"
                    "# DDD\n"
                    "tac-bootstrap init my-api --architecture ddd --framework fastapi\n\n"
                    "# Clean\n"
                    "tac-bootstrap init my-app --architecture clean --framework nextjs\n"
                ),
            },
        ],
        related_topics=["ddd", "clean-architecture", "hexagonal"],
        tags=["architecture", "patterns", "structure", "design"],
    ),
    "agentic-layer": LearningTopic(
        id="agentic-layer",
        title="The Agentic Layer",
        description="Understanding the AI-powered development layer that TAC Bootstrap generates",
        difficulty="beginner",
        sections=[
            {
                "title": "What is the Agentic Layer?",
                "content": (
                    "The Agentic Layer is a set of AI-powered development tools that "
                    "TAC Bootstrap generates for your project. It includes:\n\n"
                    "- **Slash Commands**: /prime, /scout, /feature, /implement, /test, etc.\n"
                    "- **ADW Workflows**: Automated development workflows (SDLC, patch)\n"
                    "- **Triggers**: Automated actions on events (cron, file changes)\n"
                    "- **Scripts**: Utility scripts for common operations"
                ),
            },
            {
                "title": "Components",
                "content": (
                    "**.claude/commands/**: 25+ slash commands for Claude Code\n"
                    "**.claude/hooks/**: Git hooks and automation scripts\n"
                    "**adws/**: AI Developer Workflows for automated SDLC\n"
                    "**scripts/**: Shell scripts for common operations\n"
                    "**config.yml**: Central configuration for all components"
                ),
            },
        ],
        examples=[
            {
                "title": "Using Slash Commands",
                "code": (
                    "# In Claude Code:\n"
                    "/prime                    # Load project context\n"
                    '/scout "add user auth"    # Find relevant files\n'
                    "/feature user-login       # Plan a feature\n"
                    "/implement                # Execute the plan\n"
                    "/test                     # Run tests\n"
                    "/review                   # Review changes\n"
                    "/ship                     # Create PR\n"
                ),
            },
        ],
        related_topics=["architecture", "workflows"],
        tags=["agentic", "commands", "workflows", "claude"],
    ),
    "workflows": LearningTopic(
        id="workflows",
        title="ADW Workflows",
        description="AI Developer Workflows for automated software development lifecycle",
        difficulty="intermediate",
        sections=[
            {
                "title": "What are ADW Workflows?",
                "content": (
                    "ADW (AI Developer Workflows) are automated development pipelines "
                    "that orchestrate multi-step tasks using Claude API. They handle "
                    "the full SDLC: planning, implementation, testing, review, and shipping."
                ),
            },
            {
                "title": "Available Workflows",
                "content": (
                    "**SDLC ISO**: Full lifecycle (plan -> build -> test -> review -> ship)\n"
                    "**Patch ISO**: Quick fixes (analyze -> fix -> test)\n"
                    "**Plan ISO**: Planning only (analyze -> plan -> document)\n\n"
                    "Each workflow runs in an isolated git worktree for safe parallel execution."
                ),
            },
            {
                "title": "Running Workflows",
                "content": (
                    "Workflows are triggered by:\n"
                    "- Manual execution via CLI\n"
                    "- GitHub issue assignment (cron trigger)\n"
                    "- Slash commands in Claude Code"
                ),
            },
        ],
        examples=[
            {
                "title": "Running SDLC Workflow",
                "code": (
                    "# Full SDLC for a GitHub issue\n"
                    "uv run adws/adw_sdlc_iso.py --issue 42\n\n"
                    "# Quick patch\n"
                    "uv run adws/adw_patch_iso.py --issue 15\n"
                ),
            },
        ],
        related_topics=["agentic-layer", "architecture"],
        tags=["adw", "workflow", "sdlc", "automation"],
    ),
    "testing": LearningTopic(
        id="testing",
        title="Testing Best Practices",
        description="Testing strategies and patterns for TAC Bootstrap projects",
        difficulty="intermediate",
        sections=[
            {
                "title": "Testing Philosophy",
                "content": (
                    "TAC Bootstrap encourages a testing-first approach:\n\n"
                    "1. **Unit Tests**: Test individual components in isolation\n"
                    "2. **Integration Tests**: Test component interactions\n"
                    "3. **E2E Tests**: Test full user workflows\n\n"
                    "The /test command runs your full test suite automatically."
                ),
            },
            {
                "title": "Test Organization",
                "content": (
                    "Tests mirror the source structure:\n"
                    "  tests/\n"
                    "    domain/       # Entity and value object tests\n"
                    "    application/  # Service tests (with mocked repos)\n"
                    "    infrastructure/ # Integration tests\n"
                    "    interfaces/   # API/CLI tests"
                ),
            },
        ],
        examples=[
            {
                "title": "Running Tests",
                "code": (
                    "# Run all tests\n"
                    "uv run pytest\n\n"
                    "# Run with coverage\n"
                    "uv run pytest --cov=src --cov-report=html\n\n"
                    "# Run specific test file\n"
                    "uv run pytest tests/test_user_service.py -v\n"
                ),
            },
        ],
        related_topics=["workflows", "architecture"],
        tags=["testing", "pytest", "quality", "tdd"],
    ),
    "configuration": LearningTopic(
        id="configuration",
        title="Configuration Guide",
        description="Understanding and customizing config.yml for your project",
        difficulty="beginner",
        sections=[
            {
                "title": "config.yml Structure",
                "content": (
                    "The config.yml file is the central configuration:\n\n"
                    "- **project**: Name, language, framework, architecture\n"
                    "- **paths**: Directory structure\n"
                    "- **commands**: Shell commands (start, test, lint, etc.)\n"
                    "- **agentic**: AI workflow settings\n"
                    "- **claude**: Claude Code settings and slash commands\n"
                    "- **orchestrator**: Dashboard/backend settings"
                ),
            },
            {
                "title": "Customizing Commands",
                "content": (
                    "After scaffolding, update commands for your specific project:\n\n"
                    "  commands:\n"
                    '    start: "uv run python -m app"\n'
                    '    test: "uv run pytest -v"\n'
                    '    lint: "uv run ruff check ."\n'
                    '    typecheck: "uv run mypy src/"'
                ),
            },
        ],
        examples=[
            {
                "title": "Regenerating from Config",
                "code": (
                    "# Edit config.yml, then regenerate\n"
                    "tac-bootstrap render config.yml\n\n"
                    "# Preview changes first\n"
                    "tac-bootstrap render config.yml --dry-run\n"
                ),
            },
        ],
        related_topics=["agentic-layer", "architecture"],
        tags=["config", "configuration", "yaml", "setup"],
    ),
}

# Built-in tutorials
TUTORIALS: Dict[str, Tutorial] = {
    "quick-start": Tutorial(
        id="quick-start",
        title="Quick Start Guide",
        description="Get up and running with TAC Bootstrap in 5 minutes",
        difficulty="beginner",
        estimated_minutes=5,
        prerequisites=["Python 3.10+", "uv package manager", "Claude Code"],
        steps=[
            {
                "title": "Install TAC Bootstrap",
                "instruction": "Install the CLI tool using pip or uv",
                "command": "uv pip install tac-bootstrap",
            },
            {
                "title": "Create Your First Project",
                "instruction": "Create a new Python FastAPI project with DDD architecture",
                "command": "tac-bootstrap init my-api --language python --framework fastapi --architecture ddd --no-interactive",
            },
            {
                "title": "Explore the Generated Structure",
                "instruction": "Navigate to the project and explore the directory tree",
                "command": "cd my-api && find . -type f -not -path './.git/*' | head -30",
            },
            {
                "title": "Review Configuration",
                "instruction": "Open config.yml to see your project configuration",
                "command": "cat config.yml",
            },
            {
                "title": "Use Slash Commands",
                "instruction": "Open Claude Code in the project directory and use /prime to load context",
                "command": "# In Claude Code: /prime",
            },
        ],
    ),
    "advanced": Tutorial(
        id="advanced",
        title="Advanced TAC Bootstrap Usage",
        description="Master advanced features: entity generation, workflows, and customization",
        difficulty="advanced",
        estimated_minutes=30,
        prerequisites=["Completed quick-start tutorial", "Basic Python knowledge"],
        steps=[
            {
                "title": "Generate an Entity",
                "instruction": "Generate a complete CRUD entity with all layers",
                "command": 'tac-bootstrap generate entity Product --fields "name:str:required,price:float:required,description:text" --no-interactive',
            },
            {
                "title": "Run ADW Workflow",
                "instruction": "Use the SDLC workflow for automated development",
                "command": "uv run adws/adw_sdlc_iso.py --issue 1",
            },
            {
                "title": "Create a Snapshot",
                "instruction": "Save a snapshot of your current project state",
                "command": 'tac-bootstrap snapshot create "before-refactor"',
            },
            {
                "title": "Run Validation",
                "instruction": "Validate your project configuration",
                "command": "tac-bootstrap validate --strict",
            },
            {
                "title": "Check Metrics",
                "instruction": "Generate project health metrics",
                "command": "tac-bootstrap metrics generate",
            },
            {
                "title": "Upgrade Agentic Layer",
                "instruction": "Upgrade to latest TAC Bootstrap templates",
                "command": "tac-bootstrap upgrade --dry-run",
            },
        ],
    ),
    "entity-tutorial": Tutorial(
        id="entity-tutorial",
        title="Entity Generation Tutorial",
        description="Step-by-step guide to generating CRUD entities",
        difficulty="intermediate",
        estimated_minutes=15,
        prerequisites=["Existing TAC Bootstrap project"],
        steps=[
            {
                "title": "Plan Your Entity",
                "instruction": "Decide on entity name, fields, and relationships",
                "command": "# Entity: Product with name, price, description, category",
            },
            {
                "title": "Generate with Wizard",
                "instruction": "Use the interactive wizard for entity generation",
                "command": "tac-bootstrap generate entity Product",
            },
            {
                "title": "Generate Non-Interactive",
                "instruction": "Or use the CLI directly with field definitions",
                "command": 'tac-bootstrap generate entity Product -c catalog --no-interactive --fields "name:str:required,price:float:required"',
            },
            {
                "title": "Review Generated Files",
                "instruction": "Check the generated domain model, service, repository, and routes",
                "command": "find src/domain/catalog -type f",
            },
            {
                "title": "Register Routes",
                "instruction": "Add the generated router to your main application",
                "command": "# In main.py: app.include_router(product_router)",
            },
        ],
    ),
}


class LearningService:
    """
    IDK: learning-core, educational-content, tutorial-engine, topic-browser
    Responsibility: Provides educational content, tutorials, and best practices for users
    Invariants: Content is built-in, topics are searchable, tutorials have ordered steps
    """

    def __init__(self) -> None:
        """Initialize learning service with built-in content."""
        self._topics = TOPICS
        self._tutorials = TUTORIALS

    def list_topics(self) -> List[LearningTopic]:
        """List all available learning topics.

        Returns:
            List of LearningTopic objects
        """
        return list(self._topics.values())

    def get_topic(self, topic_id: str) -> Optional[LearningTopic]:
        """Get a specific learning topic by ID.

        Args:
            topic_id: Topic identifier

        Returns:
            LearningTopic if found, None otherwise
        """
        return self._topics.get(topic_id)

    def search_topics(self, query: str) -> List[LearningTopic]:
        """Search topics by query string.

        Args:
            query: Search query

        Returns:
            List of matching topics
        """
        query_lower = query.lower()
        results = []
        for topic in self._topics.values():
            if (
                query_lower in topic.title.lower()
                or query_lower in topic.description.lower()
                or any(query_lower in tag for tag in topic.tags)
            ):
                results.append(topic)
        return results

    def list_tutorials(self) -> List[Tutorial]:
        """List all available tutorials.

        Returns:
            List of Tutorial objects
        """
        return list(self._tutorials.values())

    def get_tutorial(self, tutorial_id: str) -> Optional[Tutorial]:
        """Get a specific tutorial by ID.

        Args:
            tutorial_id: Tutorial identifier

        Returns:
            Tutorial if found, None otherwise
        """
        return self._tutorials.get(tutorial_id)

    def get_topics_by_difficulty(self, difficulty: str) -> List[LearningTopic]:
        """Get topics filtered by difficulty level.

        Args:
            difficulty: beginner, intermediate, or advanced

        Returns:
            List of topics at the specified difficulty
        """
        return [t for t in self._topics.values() if t.difficulty == difficulty]

    def get_related_topics(self, topic_id: str) -> List[LearningTopic]:
        """Get topics related to a given topic.

        Args:
            topic_id: The source topic ID

        Returns:
            List of related topics
        """
        topic = self._topics.get(topic_id)
        if not topic:
            return []
        return [
            self._topics[tid]
            for tid in topic.related_topics
            if tid in self._topics
        ]
