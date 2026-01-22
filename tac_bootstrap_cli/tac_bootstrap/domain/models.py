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

from enum import Enum
from typing import Dict, List

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
    model_policy: ModelPolicy = Field(default=ModelPolicy(), description="Model selection policy")
    worktrees: WorktreeConfig = Field(
        default=WorktreeConfig(), description="Git worktree configuration"
    )
    logging: LoggingConfig = Field(default=LoggingConfig(), description="Logging configuration")
    safety: SafetyConfig = Field(default=SafetyConfig(), description="Safety constraints")
    workflows: WorkflowsConfig = Field(
        default=WorkflowsConfig(), description="Workflow configuration"
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
            version="0.2.0",
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

    model_config = {"extra": "forbid"}


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
