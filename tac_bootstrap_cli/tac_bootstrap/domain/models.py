"""
TAC Bootstrap Configuration Models

Pydantic models representing the complete config.yml schema for TAC Bootstrap.
These models provide type safety, validation, and smart defaults for configuration.

Example usage:
    from tac_bootstrap.domain.models import TACConfig, Language, PackageManager

    config = TACConfig(
        project=ProjectSpec(
            name="my-app",
            language=Language.PYTHON,
            package_manager=PackageManager.UV
        ),
        commands=CommandsSpec(
            start="uv run python -m app",
            test="uv run pytest"
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name="my-app")
        )
    )
"""

import re
from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, Field, field_validator

from tac_bootstrap import __version__

# ============================================================================
# ENUMS - Configuration Option Types
# ============================================================================


class Language(str, Enum):
    """Supported programming languages for TAC Bootstrap projects."""

    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"


class Framework(str, Enum):
    """Web frameworks and project types supported per language."""

    # Python
    FASTAPI = "fastapi"
    DJANGO = "django"
    FLASK = "flask"
    # TypeScript/JavaScript
    NEXTJS = "nextjs"
    EXPRESS = "express"
    NESTJS = "nestjs"
    REACT = "react"
    VUE = "vue"
    # Go
    GIN = "gin"
    ECHO = "echo"
    # Rust
    AXUM = "axum"
    ACTIX = "actix"
    # Java
    SPRING = "spring"
    # No framework
    NONE = "none"


class Architecture(str, Enum):
    """Software architecture patterns."""

    SIMPLE = "simple"
    LAYERED = "layered"
    DDD = "ddd"
    CLEAN = "clean"
    HEXAGONAL = "hexagonal"


class PackageManager(str, Enum):
    """Package managers per language."""

    # Python
    UV = "uv"
    POETRY = "poetry"
    PIP = "pip"
    PIPENV = "pipenv"
    # TypeScript/JavaScript
    PNPM = "pnpm"
    NPM = "npm"
    YARN = "yarn"
    BUN = "bun"
    # Go
    GO_MOD = "go"
    # Rust
    CARGO = "cargo"
    # Java
    MAVEN = "maven"
    GRADLE = "gradle"


class ProjectMode(str, Enum):
    """Project initialization mode."""

    NEW = "new"
    EXISTING = "existing"


class AgenticProvider(str, Enum):
    """Agentic provider options."""

    CLAUDE_CODE = "claude_code"


class RunIdStrategy(str, Enum):
    """Run ID generation strategy for logging."""

    UUID = "uuid"
    TIMESTAMP = "timestamp"


class DefaultWorkflow(str, Enum):
    """Available ADW workflows."""

    SDLC_ISO = "sdlc_iso"
    PATCH_ISO = "patch_iso"
    PLAN_IMPLEMENT = "plan_implement"


class FieldType(str, Enum):
    """Field types for entity specification."""

    STR = "str"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    DATETIME = "datetime"
    UUID = "uuid"
    TEXT = "text"
    DECIMAL = "decimal"
    JSON = "json"


# ============================================================================
# SUB-MODELS - Configuration Section Models
# ============================================================================


class ProjectSpec(BaseModel):
    """
    Project metadata and settings.

    Attributes:
        name: Project name (will be sanitized for safe directory/package naming)
        mode: Project initialization mode (new or existing)
        repo_root: Repository root directory (default: ".")
        language: Programming language
        framework: Web framework or project type
        architecture: Software architecture pattern
        package_manager: Package/dependency manager
    """

    name: str = Field(..., description="Project name")
    mode: ProjectMode = Field(
        default=ProjectMode.NEW, description="Project initialization mode (new or existing)"
    )
    repo_root: str = Field(default=".", description="Repository root directory")
    language: Language = Field(..., description="Programming language")
    framework: Framework = Field(
        default=Framework.NONE, description="Web framework or project type"
    )
    architecture: Architecture = Field(
        default=Architecture.SIMPLE, description="Software architecture pattern"
    )
    package_manager: PackageManager = Field(..., description="Package/dependency manager")

    @field_validator("name")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        """
        Sanitize project name for safe directory and package naming.

        - Strips whitespace
        - Converts to lowercase
        - Replaces spaces with hyphens
        - Ensures non-empty
        """
        if not v or not v.strip():
            raise ValueError("Project name cannot be empty")
        sanitized = v.strip().lower().replace(" ", "-")
        return sanitized


class PathsSpec(BaseModel):
    """
    Directory structure configuration.

    Defines all paths for the project structure including app root,
    agentic layer components, and auxiliary directories.
    """

    app_root: str = Field(..., description="Application root directory")
    agentic_root: str = Field(default=".", description="Agentic layer root directory")
    prompts_dir: str = Field(default="prompts", description="Prompts directory")
    adws_dir: str = Field(default="adws", description="AI Developer Workflows directory")
    specs_dir: str = Field(default="specs", description="Specifications directory")
    logs_dir: str = Field(default="logs", description="Logs directory")
    scripts_dir: str = Field(default="scripts", description="Scripts directory")
    worktrees_dir: str = Field(default="trees", description="Git worktrees directory")


class CommandsSpec(BaseModel):
    """
    Shell command mappings for common development tasks.

    These commands are used by Claude Code slash commands and ADW workflows.
    """

    start: str = Field(..., description="Command to start the application")
    test: str = Field(..., description="Command to run tests")
    lint: str = Field(default="", description="Command to run linter")
    typecheck: str = Field(default="", description="Command to run type checker")
    format: str = Field(default="", description="Command to format code")
    build: str = Field(default="", description="Command to build the project")


class WorktreeConfig(BaseModel):
    """
    Git worktree configuration for parallel development.

    Enables ADWs to work in isolated git worktrees for concurrent workflows.
    """

    enabled: bool = Field(default=True, description="Enable git worktrees")
    max_parallel: int = Field(default=5, description="Maximum parallel worktrees", ge=1, le=10)
    naming: str = Field(default="feat-{slug}-{timestamp}", description="Worktree naming pattern")


class LoggingConfig(BaseModel):
    """
    Logging configuration for agent execution tracking.
    """

    level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR)")
    capture_agent_transcript: bool = Field(
        default=True, description="Capture full agent conversation transcript"
    )
    run_id_strategy: RunIdStrategy = Field(
        default=RunIdStrategy.UUID, description="Run ID generation strategy"
    )


class SafetyConfig(BaseModel):
    """
    Safety constraints and guardrails for agent execution.

    Defines what agents can and cannot do to prevent unintended modifications.
    """

    require_tests_pass: bool = Field(
        default=True, description="Require tests to pass before completion"
    )
    require_review_artifacts: bool = Field(
        default=True, description="Require review artifacts before completion"
    )
    allowed_paths: List[str] = Field(
        default_factory=list, description="Paths agents are allowed to modify"
    )
    forbidden_paths: List[str] = Field(
        default_factory=list, description="Paths agents must not modify"
    )


class WorkflowsConfig(BaseModel):
    """
    ADW workflow configuration.

    Defines which workflows are available and which is the default.
    """

    default: DefaultWorkflow = Field(
        default=DefaultWorkflow.SDLC_ISO, description="Default workflow to use"
    )
    available: List[DefaultWorkflow] = Field(
        default_factory=lambda: [
            DefaultWorkflow.SDLC_ISO,
            DefaultWorkflow.PATCH_ISO,
            DefaultWorkflow.PLAN_IMPLEMENT,
        ],
        description="Available workflows",
    )


class ModelPolicy(BaseModel):
    """
    Model selection policy for different task types.
    """

    default: str = Field(default="sonnet", description="Default model for standard tasks")
    heavy: str = Field(default="opus", description="Model for complex/heavy tasks")
    fallback: str = Field(default="haiku", description="Fallback model when quota is exhausted")


class TokenOptimizationConfig(BaseModel):
    """
    Token usage optimization settings.

    Controls various limits to reduce token consumption in ADW workflows.
    """

    max_issue_body_length: int = Field(
        default=2000, description="Truncate issue body to reduce token usage"
    )
    max_file_reference_size: int = Field(
        default=5000, description="Max chars per referenced file"
    )
    max_clarification_length: int = Field(
        default=1000, description="Max chars for clarification responses"
    )
    max_docs_planning: int = Field(
        default=2, description="Max documentation files to load in planning phase"
    )
    max_summary_tokens_planning: int = Field(
        default=200, description="Max tokens per doc summary in planning"
    )
    max_file_references: int = Field(
        default=3, description="Max number of files to load from issue references"
    )
    max_screenshots: int = Field(
        default=3, description="Max screenshots to upload in review phase"
    )


class AgenticSpec(BaseModel):
    """
    Agentic layer configuration.

    Comprehensive settings for the AI-powered development workflows.
    """

    provider: AgenticProvider = Field(
        default=AgenticProvider.CLAUDE_CODE, description="Agentic provider"
    )
    target_branch: str = Field(
        default="main",
        description="Target branch for merge/push operations (main, master, develop, etc.)",
    )
    cron_interval: int = Field(
        default=20,
        description="Polling interval in seconds for cron trigger (default: 20)",
        ge=5,
        le=3600,
    )
    model_policy: ModelPolicy = Field(default=ModelPolicy(), description="Model selection policy")
    worktrees: WorktreeConfig = Field(
        default=WorktreeConfig(), description="Git worktree configuration"
    )
    logging: LoggingConfig = Field(default=LoggingConfig(), description="Logging configuration")
    safety: SafetyConfig = Field(default=SafetyConfig(), description="Safety constraints")
    workflows: WorkflowsConfig = Field(
        default=WorkflowsConfig(), description="Workflow configuration"
    )
    token_optimization: TokenOptimizationConfig = Field(
        default=TokenOptimizationConfig(), description="Token usage optimization settings"
    )


class ClaudeSettings(BaseModel):
    """
    Claude Code .claude/settings.json configuration.
    """

    project_name: str = Field(..., description="Project name for Claude Code")
    preferred_style: str = Field(default="concise", description="Preferred communication style")
    allow_shell: bool = Field(default=True, description="Allow shell command execution")


class ClaudeCommandsConfig(BaseModel):
    """
    Slash command mappings for Claude Code.

    Maps command names to their prompt file paths.
    """

    prime: str = Field(default=".claude/commands/prime.md", description="Path to /prime command")
    start: str = Field(default=".claude/commands/start.md", description="Path to /start command")
    build: str = Field(default=".claude/commands/build.md", description="Path to /build command")
    test: str = Field(default=".claude/commands/test.md", description="Path to /test command")
    review: str = Field(default=".claude/commands/review.md", description="Path to /review command")
    ship: str = Field(default=".claude/commands/ship.md", description="Path to /ship command")


class ClaudeConfig(BaseModel):
    """
    Complete Claude Code configuration.

    Combines settings and command mappings.
    """

    settings: ClaudeSettings = Field(..., description="Claude Code settings")
    commands: ClaudeCommandsConfig = Field(
        default=ClaudeCommandsConfig(), description="Slash command mappings"
    )


class TemplatesConfig(BaseModel):
    """
    Template file paths for different document types.
    """

    plan_template: str = Field(
        default="prompts/templates/plan.md", description="Plan document template"
    )
    chore_template: str = Field(
        default="prompts/templates/chore.md", description="Chore document template"
    )
    feature_template: str = Field(
        default="prompts/templates/feature.md", description="Feature document template"
    )
    bug_template: str = Field(
        default="prompts/templates/bug.md", description="Bug document template"
    )
    review_template: str = Field(
        default="prompts/templates/review.md", description="Review document template"
    )


class BootstrapConfig(BaseModel):
    """
    Bootstrap options for new projects.

    Controls what gets created during project initialization.
    """

    create_git_repo: bool = Field(default=True, description="Initialize git repository")
    initial_commit: bool = Field(default=True, description="Create initial commit")
    license: str = Field(default="MIT", description="License type (MIT, Apache-2.0, etc.)")
    readme: bool = Field(default=True, description="Generate README.md")


class OrchestratorConfig(BaseModel):
    """
    Orchestrator frontend configuration.

    Defines API endpoints, WebSocket settings, and port configuration
    for the orchestrator frontend application.
    """

    enabled: bool = Field(
        default=False,
        description="Enable orchestrator components (backend + frontend)"
    )
    api_base_url: str = Field(
        default="http://localhost:8000",
        description="Base URL for orchestrator API"
    )
    ws_base_url: str = Field(
        default="ws://localhost:8000",
        description="Base URL for WebSocket connection"
    )
    frontend_port: int = Field(
        default=5173,
        description="Port for frontend development server",
        ge=1024,
        le=65535
    )
    websocket_port: int = Field(
        default=8000,
        description="Port for WebSocket server",
        ge=1024,
        le=65535
    )
    database_url: str = Field(
        default="sqlite:///data/orchestrator.db",
        description="Database connection URL for orchestrator"
    )
    polling_interval: int = Field(
        default=5000,
        description="Polling interval in milliseconds for fallback polling",
        ge=100,
        le=60000
    )


class BootstrapMetadata(BaseModel):
    """
    Bootstrap generation metadata for audit trail and traceability.

    This model captures metadata about when and how a TAC Bootstrap project was
    generated, providing an audit trail for tracking versions, upgrades, and
    template changes over time.

    Attributes:
        generated_at: ISO8601 timestamp string indicating when the project was
            initially generated. Format: "2024-01-15T10:30:00.123456"
            Example: datetime.now().isoformat()

        generated_by: Identifier string for the TAC Bootstrap version that created
            the project. Format: "tac-bootstrap v{version}"
            Example: "tac-bootstrap v0.9.9"

        last_upgrade: Optional ISO8601 timestamp string for the last time the project
            was upgraded or regenerated. None if never upgraded.
            Example: "2024-02-20T14:45:00.789012" or None

        schema_version: Integer indicating the config.yml schema version. Used for
            migration and compatibility checks. Default: 2

        template_checksums: Dictionary mapping template file names to their MD5
            checksums. Used to detect template changes and determine if upgrades
            are needed. Tracks primary user-facing templates:
            - .claude/commands/*.md
            - adws/adw_*_iso.py
            - scripts/*.sh
            Example: {"adw_sdlc_iso.py": "a1b2c3d4...", "start.md": "e5f6g7h8..."}

    Example:
        metadata = BootstrapMetadata(
            generated_at="2024-01-15T10:30:00.123456",
            generated_by="tac-bootstrap v0.9.9",
            last_upgrade=None,
            schema_version=2,
            template_checksums={
                "adw_sdlc_iso.py": "a1b2c3d4e5f6g7h8",
                "start.md": "1a2b3c4d5e6f7g8h"
            }
        )

    Note:
        - Timestamps are stored as plain strings without validation
        - The generator is responsible for creating valid ISO8601 timestamps
        - Checksums use MD5 hash of full file content
        - Regeneration counts as an upgrade (updates last_upgrade)
    """

    generated_at: str = Field(
        ..., description="ISO8601 timestamp when project was generated"
    )
    generated_by: str = Field(
        ..., description="TAC Bootstrap version identifier"
    )
    last_upgrade: str | None = Field(
        default=None, description="ISO8601 timestamp of last upgrade"
    )
    schema_version: int = Field(
        default=2, description="Config schema version for migration tracking"
    )
    template_checksums: dict[str, str] = Field(
        default_factory=dict, description="Template name to MD5 checksum mapping"
    )


# ============================================================================
# ROOT MODEL - Complete Configuration
# ============================================================================


class TACConfig(BaseModel):
    """
    Complete TAC Bootstrap configuration model.

    This is the root model that represents the entire config.yml schema.
    All configuration sections are validated and type-safe.

    Example:
        config = TACConfig(
            version="0.9.9",
            schema_version=1,
            project=ProjectSpec(
                name="my-app",
                language=Language.PYTHON,
                package_manager=PackageManager.UV
            ),
            paths=PathsSpec(app_root="src"),
            commands=CommandsSpec(
                start="uv run python -m app",
                test="uv run pytest"
            ),
            agentic=AgenticSpec(),
            claude=ClaudeConfig(
                settings=ClaudeSettings(project_name="my-app")
            ),
            templates=TemplatesConfig(),
            bootstrap=BootstrapConfig()
        )
    """

    version: str = Field(
        default=__version__,
        description="TAC Bootstrap version used to generate this project"
    )
    schema_version: int = Field(default=1, description="Configuration schema version")
    project: ProjectSpec = Field(..., description="Project metadata and settings")
    paths: PathsSpec = Field(
        default_factory=lambda: PathsSpec(
            app_root="src",
            agentic_root=".",
            prompts_dir="prompts",
            adws_dir="adws",
            specs_dir="specs",
            logs_dir="logs",
            scripts_dir="scripts",
            worktrees_dir="trees",
        ),
        description="Directory structure configuration",
    )
    commands: CommandsSpec = Field(..., description="Shell command mappings")
    agentic: AgenticSpec = Field(default=AgenticSpec(), description="Agentic layer configuration")
    claude: ClaudeConfig = Field(..., description="Claude Code configuration")
    templates: TemplatesConfig = Field(default=TemplatesConfig(), description="Template file paths")
    bootstrap: BootstrapConfig = Field(
        default=BootstrapConfig(), description="Bootstrap options for new projects"
    )
    orchestrator: OrchestratorConfig = Field(
        default=OrchestratorConfig(), description="Orchestrator frontend configuration"
    )
    metadata: BootstrapMetadata | None = Field(
        default=None, description="Bootstrap generation metadata for audit trail"
    )

    model_config = {"extra": "forbid"}


# ============================================================================
# ENTITY GENERATION MODELS
# ============================================================================


class FieldSpec(BaseModel):
    """
    Field specification for entity generation.

    Describes a single field in an entity including its type, constraints,
    and database settings.

    Attributes:
        name: Field name in snake_case
        type: Field data type
        nullable: Whether field can be null
        indexed: Whether to create database index
        max_length: Maximum length for string fields
        default: Default value for field
    """

    name: str = Field(..., description="Field name in snake_case")
    type: FieldType = Field(..., description="Field data type")
    nullable: bool = Field(default=False, description="Whether field can be null")
    indexed: bool = Field(default=False, description="Whether to create database index")
    max_length: int | None = Field(default=None, description="Maximum length for string fields")
    default: Any | None = Field(default=None, description="Default value for field")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """
        Validate field name is snake_case and not reserved.

        Reserved names (inherited from BaseEntity):
        - id, state, version, created_at, updated_at, deleted_at
        """
        if not v or not v.strip():
            raise ValueError("Field name cannot be empty")

        # Check for reserved names
        reserved = {"id", "state", "version", "created_at", "updated_at", "deleted_at"}
        if v.lower() in reserved:
            raise ValueError(
                f"Field name '{v}' is reserved (inherited from BaseEntity). "
                f"Reserved names: {', '.join(sorted(reserved))}"
            )

        # Validate snake_case format
        if not re.match(r"^[a-z][a-z0-9_]*$", v):
            raise ValueError(
                f"Field name '{v}' must be in snake_case format "
                "(lowercase letters, numbers, underscores, must start with letter)"
            )

        return v


class EntitySpec(BaseModel):
    """
    Entity specification for code generation.

    Describes a complete entity to be generated including its name,
    capability grouping, and field definitions.

    Attributes:
        name: Entity name in PascalCase (e.g., "Product")
        capability: Capability grouping in kebab-case (e.g., "catalog")
        fields: List of field specifications

    Properties:
        snake_name: Entity name in snake_case (e.g., "product")
        plural_name: Pluralized entity name (e.g., "products")
        table_name: Database table name (same as plural_name)
    """

    name: str = Field(..., description="Entity name in PascalCase")
    capability: str = Field(..., description="Capability grouping in kebab-case")
    fields: List[FieldSpec] = Field(..., description="List of field specifications")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate entity name is PascalCase."""
        if not v or not v.strip():
            raise ValueError("Entity name cannot be empty")

        # Validate PascalCase format
        if not re.match(r"^[A-Z][a-zA-Z0-9]*$", v):
            raise ValueError(
                f"Entity name '{v}' must be in PascalCase format "
                "(must start with uppercase letter, contain only letters and numbers)"
            )

        return v

    @field_validator("capability")
    @classmethod
    def validate_capability(cls, v: str) -> str:
        """Validate capability is kebab-case."""
        if not v or not v.strip():
            raise ValueError("Capability cannot be empty")

        # Validate kebab-case format
        if not re.match(r"^[a-z][a-z0-9-]*$", v):
            raise ValueError(
                f"Capability '{v}' must be in kebab-case format "
                "(lowercase letters, numbers, hyphens, must start with letter)"
            )

        return v

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, v: List[FieldSpec]) -> List[FieldSpec]:
        """Validate that fields list is not empty."""
        if not v:
            raise ValueError("Entity must have at least one field")
        return v

    @property
    def snake_name(self) -> str:
        """
        Convert PascalCase to snake_case.

        Example: "ProductCategory" -> "product_category"
        """
        # Insert underscore before uppercase letters (except first)
        s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", self.name)
        # Insert underscore before uppercase letters followed by lowercase
        s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    @property
    def plural_name(self) -> str:
        """
        Simple pluralization (name + s).

        Example: "product" -> "products"
        """
        return f"{self.snake_name}s"

    @property
    def table_name(self) -> str:
        """
        Database table name (plural_name).

        Example: "products"
        """
        return self.plural_name


# ============================================================================
# HELPER FUNCTIONS - Smart Defaults
# ============================================================================


def get_frameworks_for_language(language: Language) -> List[Framework]:
    """
    Get valid frameworks for a given language.

    Args:
        language: Programming language

    Returns:
        List of valid frameworks for the language
    """
    mapping = {
        Language.PYTHON: [
            Framework.FASTAPI,
            Framework.DJANGO,
            Framework.FLASK,
            Framework.NONE,
        ],
        Language.TYPESCRIPT: [
            Framework.NEXTJS,
            Framework.EXPRESS,
            Framework.NESTJS,
            Framework.REACT,
            Framework.VUE,
            Framework.NONE,
        ],
        Language.JAVASCRIPT: [
            Framework.NEXTJS,
            Framework.EXPRESS,
            Framework.REACT,
            Framework.VUE,
            Framework.NONE,
        ],
        Language.GO: [Framework.GIN, Framework.ECHO, Framework.NONE],
        Language.RUST: [Framework.AXUM, Framework.ACTIX, Framework.NONE],
        Language.JAVA: [Framework.SPRING, Framework.NONE],
    }
    return mapping.get(language, [Framework.NONE])


def get_package_managers_for_language(language: Language) -> List[PackageManager]:
    """
    Get valid package managers for a given language.

    Args:
        language: Programming language

    Returns:
        List of valid package managers for the language
    """
    mapping = {
        Language.PYTHON: [
            PackageManager.UV,
            PackageManager.POETRY,
            PackageManager.PIP,
            PackageManager.PIPENV,
        ],
        Language.TYPESCRIPT: [
            PackageManager.PNPM,
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.BUN,
        ],
        Language.JAVASCRIPT: [
            PackageManager.PNPM,
            PackageManager.NPM,
            PackageManager.YARN,
            PackageManager.BUN,
        ],
        Language.GO: [PackageManager.GO_MOD],
        Language.RUST: [PackageManager.CARGO],
        Language.JAVA: [PackageManager.MAVEN, PackageManager.GRADLE],
    }
    return mapping.get(language, [])


def get_default_commands(language: Language, package_manager: PackageManager) -> Dict[str, str]:
    """
    Get default command mappings for language/package manager combination.

    Args:
        language: Programming language
        package_manager: Package manager

    Returns:
        Dictionary of default commands (start, test, lint, etc.)
    """
    # Python commands
    if language == Language.PYTHON:
        if package_manager == PackageManager.UV:
            return {
                "start": "uv run python -m app",
                "test": "uv run pytest",
                "lint": "uv run ruff check .",
                "typecheck": "uv run mypy .",
                "format": "uv run ruff format .",
                "build": "uv build",
            }
        elif package_manager == PackageManager.POETRY:
            return {
                "start": "poetry run python -m app",
                "test": "poetry run pytest",
                "lint": "poetry run ruff check .",
                "typecheck": "poetry run mypy .",
                "format": "poetry run ruff format .",
                "build": "poetry build",
            }
        elif package_manager == PackageManager.PIP:
            return {
                "start": "python -m app",
                "test": "pytest",
                "lint": "ruff check .",
                "typecheck": "mypy .",
                "format": "ruff format .",
                "build": "python -m build",
            }

    # TypeScript/JavaScript commands
    elif language in (Language.TYPESCRIPT, Language.JAVASCRIPT):
        if package_manager == PackageManager.PNPM:
            return {
                "start": "pnpm dev",
                "test": "pnpm test",
                "lint": "pnpm lint",
                "typecheck": "pnpm typecheck",
                "format": "pnpm format",
                "build": "pnpm build",
            }
        elif package_manager == PackageManager.NPM:
            return {
                "start": "npm run dev",
                "test": "npm test",
                "lint": "npm run lint",
                "typecheck": "npm run typecheck",
                "format": "npm run format",
                "build": "npm run build",
            }
        elif package_manager == PackageManager.YARN:
            return {
                "start": "yarn dev",
                "test": "yarn test",
                "lint": "yarn lint",
                "typecheck": "yarn typecheck",
                "format": "yarn format",
                "build": "yarn build",
            }
        elif package_manager == PackageManager.BUN:
            return {
                "start": "bun run dev",
                "test": "bun test",
                "lint": "bun run lint",
                "typecheck": "bun run typecheck",
                "format": "bun run format",
                "build": "bun run build",
            }

    # Go commands
    elif language == Language.GO:
        return {
            "start": "go run .",
            "test": "go test ./...",
            "lint": "golangci-lint run",
            "typecheck": "go vet ./...",
            "format": "go fmt ./...",
            "build": "go build",
        }

    # Rust commands
    elif language == Language.RUST:
        return {
            "start": "cargo run",
            "test": "cargo test",
            "lint": "cargo clippy",
            "typecheck": "cargo check",
            "format": "cargo fmt",
            "build": "cargo build --release",
        }

    # Java commands
    elif language == Language.JAVA:
        if package_manager == PackageManager.MAVEN:
            return {
                "start": "mvn spring-boot:run",
                "test": "mvn test",
                "lint": "mvn checkstyle:check",
                "typecheck": "mvn compile",
                "format": "mvn spotless:apply",
                "build": "mvn package",
            }
        elif package_manager == PackageManager.GRADLE:
            return {
                "start": "gradle bootRun",
                "test": "gradle test",
                "lint": "gradle checkstyleMain",
                "typecheck": "gradle compileJava",
                "format": "gradle spotlessApply",
                "build": "gradle build",
            }

    # Default fallback
    return {
        "start": "",
        "test": "",
        "lint": "",
        "typecheck": "",
        "format": "",
        "build": "",
    }
