"""Interactive wizard for TAC Bootstrap configuration.

Uses Rich for beautiful terminal UI with prompts and selections.
Provides guided step-by-step configuration for both new projects
and adding agentic layers to existing repositories.

Includes both the standard wizard (run_init_wizard) and the enhanced
wizard (run_enhanced_init_wizard) with Rich UI components, directory tree
preview, real-time validation feedback, and confirmation summary.
"""

from __future__ import annotations

import keyword
import re
from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, TypeVar

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

from tac_bootstrap.domain.entity_config import (
    RESERVED_FIELD_NAMES,
    EntitySpec,
    FieldSpec,
    FieldType,
)
from tac_bootstrap.domain.models import (
    AgenticSpec,
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    OrchestratorConfig,
    PackageManager,
    PathsSpec,
    ProjectMode,
    ProjectSpec,
    TACConfig,
    WorktreeConfig,
    get_default_commands,
    get_frameworks_for_language,
    get_package_managers_for_language,
)
from tac_bootstrap.infrastructure.ui_components import UIComponents

# Global console instance for consistent output
console = Console()

# Type variable for enum types (bound to Enum)
E = TypeVar("E", bound=Enum)


def select_from_enum(
    prompt: str,
    enum_class: Type[E],
    default: Optional[E] = None,
    filter_fn: Optional[Callable[[E], bool]] = None,
) -> E:
    """Interactive selection from enum values.

    Displays a numbered list of options in a Rich table format,
    allowing the user to select by number. The default option
    is visually marked with a green indicator.

    Args:
        prompt: Question to ask the user
        enum_class: Enum class to select from
        default: Default value to pre-select
        filter_fn: Optional function to filter valid options

    Returns:
        Selected enum value

    Example:
        >>> language = select_from_enum(
        ...     "What programming language?",
        ...     Language,
        ...     default=Language.PYTHON
        ... )
    """
    # Get all enum members as a list
    options: List[E] = list(enum_class)
    if filter_fn:
        options = [o for o in options if filter_fn(o)]

    if not options:
        raise ValueError(f"No valid options available for {enum_class.__name__}")

    # Build options table
    table = Table(show_header=False, box=None, padding=(0, 2))
    for i, opt in enumerate(options, 1):
        is_default = opt == default
        marker = "[green]>[/green]" if is_default else " "
        table.add_row(f"{marker} {i}.", f"[bold]{opt.value}[/bold]")

    console.print(f"\n[bold]{prompt}[/bold]")
    console.print(table)

    # Determine default selection number
    default_num = options.index(default) + 1 if default in options else 1

    # Get user selection
    choice = Prompt.ask(
        "Select option",
        default=str(default_num),
        choices=[str(i) for i in range(1, len(options) + 1)],
    )

    return options[int(choice) - 1]


def run_init_wizard(
    name: str,
    language: Optional[Language] = None,
    framework: Optional[Framework] = None,
    package_manager: Optional[PackageManager] = None,
    architecture: Optional[Architecture] = None,
    with_orchestrator: bool = False,
) -> TACConfig:
    """Run interactive wizard for project initialization.

    Guides the user through configuring a new project step by step,
    asking for language, framework, package manager, architecture,
    commands, and worktree preferences.

    Args:
        name: Project name (already provided via CLI)
        language: Pre-selected language (or None to ask)
        framework: Pre-selected framework (or None to ask)
        package_manager: Pre-selected package manager (or None to ask)
        architecture: Pre-selected architecture (or None to ask)

    Returns:
        Configured TACConfig ready for scaffolding

    Raises:
        SystemExit: If user cancels at confirmation prompt
    """
    # Welcome panel
    console.print(
        Panel.fit(
            f"[bold blue]Creating new project:[/bold blue] {name}\n\n"
            "Let's configure your Agentic Layer!",
            title="🚀 TAC Bootstrap Wizard",
        )
    )

    # Step 1: Language
    if language is None:
        language = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )
    console.print(f"  [green]✓[/green] Language: {language.value}")

    # Step 2: Framework (filtered by language)
    if framework is None:
        valid_frameworks = get_frameworks_for_language(language)
        framework = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.NONE,
            filter_fn=lambda f: f in valid_frameworks,
        )
    console.print(f"  [green]✓[/green] Framework: {framework.value}")

    # Step 3: Package Manager (filtered by language)
    if package_manager is None:
        valid_managers = get_package_managers_for_language(language)
        default_pm = valid_managers[0] if valid_managers else None
        package_manager = select_from_enum(
            "What package manager?",
            PackageManager,
            default=default_pm,
            filter_fn=lambda p: p in valid_managers,
        )
    console.print(f"  [green]✓[/green] Package Manager: {package_manager.value}")

    # Step 4: Architecture
    if architecture is None:
        architecture = select_from_enum(
            "What architecture pattern?",
            Architecture,
            default=Architecture.SIMPLE,
        )
    console.print(f"  [green]✓[/green] Architecture: {architecture.value}")

    # Step 5: Commands Configuration (with smart defaults)
    console.print("\n[bold]Commands Configuration[/bold]")
    console.print("[dim]These commands will be used by Claude Code and ADW workflows[/dim]\n")

    default_commands = get_default_commands(language, package_manager)

    start_cmd = Prompt.ask(
        "  Start command",
        default=default_commands.get("start", ""),
    )
    test_cmd = Prompt.ask(
        "  Test command",
        default=default_commands.get("test", ""),
    )
    lint_cmd = Prompt.ask(
        "  Lint command (optional)",
        default=default_commands.get("lint", ""),
    )

    # Step 6: Worktrees
    use_worktrees = Confirm.ask(
        "\nEnable git worktrees for parallel workflows?",
        default=True,
    )

    # Step 7: Target Branch
    target_branch = Prompt.ask(
        "Target branch for merge/push (main, master, develop)",
        default="main",
    )
    console.print(f"  [green]✓[/green] Target Branch: {target_branch}")

    # Build configuration object
    config = TACConfig(
        project=ProjectSpec(
            name=name,
            mode=ProjectMode.NEW,
            language=language,
            framework=framework,
            architecture=architecture,
            package_manager=package_manager,
        ),
        paths=PathsSpec(
            app_root="src" if architecture != Architecture.SIMPLE else ".",
        ),
        commands=CommandsSpec(
            start=start_cmd,
            test=test_cmd,
            lint=lint_cmd,
        ),
        agentic=AgenticSpec(
            target_branch=target_branch,
            worktrees=WorktreeConfig(enabled=use_worktrees, max_parallel=5),
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name=name),
        ),
        orchestrator=OrchestratorConfig(enabled=with_orchestrator),
    )

    # Show summary and confirm
    console.print("\n")
    _show_config_summary(config)

    if not Confirm.ask("\nProceed with this configuration?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(0)

    return config


def run_add_agentic_wizard(
    repo_path: Path,
    detected: Any,  # DetectedProject type not implemented yet (FASE 6)
    with_orchestrator: bool = False,
) -> TACConfig:
    """Run wizard for adding agentic layer to existing project.

    Uses auto-detected settings as defaults, allowing the user to
    confirm or override each setting. Focuses on command configuration
    which is critical for existing projects.

    Args:
        repo_path: Path to existing repository
        detected: Auto-detected project settings (from DetectService)
        with_orchestrator: Whether to include orchestrator components

    Returns:
        Configured TACConfig for the existing project

    Raises:
        SystemExit: If user cancels at confirmation prompt

    Note:
        The `detected` parameter uses a string literal type hint because
        DetectedProject is not yet implemented (FASE 6). This allows
        the code to pass type checking without the actual type.
    """
    # Welcome panel
    console.print(
        Panel.fit(
            f"[bold blue]Adding Agentic Layer to:[/bold blue] {repo_path.name}\n\n"
            "Review detected settings and customize commands.",
            title="🔧 TAC Bootstrap Wizard",
        )
    )

    # Step 1: Confirm or change language
    language = select_from_enum(
        "Programming language (detected):",
        Language,
        default=detected.language,
    )
    console.print(f"  [green]✓[/green] Language: {language.value}")

    # Step 2: Confirm or change framework
    valid_frameworks = get_frameworks_for_language(language)
    framework = select_from_enum(
        "Framework (detected):",
        Framework,
        default=detected.framework or Framework.NONE,
        filter_fn=lambda f: f in valid_frameworks,
    )
    console.print(f"  [green]✓[/green] Framework: {framework.value}")

    # Step 3: Confirm or change package manager
    valid_managers = get_package_managers_for_language(language)
    package_manager = select_from_enum(
        "Package manager (detected):",
        PackageManager,
        default=detected.package_manager,
        filter_fn=lambda p: p in valid_managers,
    )
    console.print(f"  [green]✓[/green] Package Manager: {package_manager.value}")

    # Step 4: Commands - most important for existing projects
    console.print("\n[bold]Configure Commands[/bold]")
    console.print("[dim]These commands will be used by Claude Code and ADW workflows[/dim]\n")

    default_commands = get_default_commands(language, package_manager)

    start_cmd = Prompt.ask(
        "  Start command",
        default=detected.commands.get("start", default_commands.get("start", "")),
    )
    test_cmd = Prompt.ask(
        "  Test command",
        default=detected.commands.get("test", default_commands.get("test", "")),
    )
    lint_cmd = Prompt.ask(
        "  Lint command",
        default=detected.commands.get("lint", default_commands.get("lint", "")),
    )
    build_cmd = Prompt.ask(
        "  Build command",
        default=detected.commands.get("build", default_commands.get("build", "")),
    )

    # Step 5: Worktrees
    use_worktrees = Confirm.ask(
        "\nEnable git worktrees for parallel workflows?",
        default=True,
    )

    # Step 6: Target Branch
    target_branch = Prompt.ask(
        "Target branch for merge/push (main, master, develop)",
        default="main",
    )
    console.print(f"  [green]✓[/green] Target Branch: {target_branch}")

    # Build configuration object
    config = TACConfig(
        project=ProjectSpec(
            name=repo_path.name,
            mode=ProjectMode.EXISTING,
            repo_root=str(repo_path),
            language=language,
            framework=framework,
            package_manager=package_manager,
        ),
        paths=PathsSpec(
            app_root=detected.app_root or "src",
        ),
        commands=CommandsSpec(
            start=start_cmd,
            test=test_cmd,
            lint=lint_cmd,
            build=build_cmd,
        ),
        agentic=AgenticSpec(
            target_branch=target_branch,
            worktrees=WorktreeConfig(enabled=use_worktrees, max_parallel=5),
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name=repo_path.name),
        ),
        orchestrator=OrchestratorConfig(enabled=with_orchestrator),
    )

    # Show summary and confirm
    console.print("\n")
    _show_config_summary(config)

    if not Confirm.ask("\nProceed with this configuration?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(0)

    return config


# ============================================================================
# Enhanced Init Wizard with Rich UI Components
# ============================================================================


def get_frameworks_for_language_display(language: str) -> List[str]:
    """Get available framework display names for a given language string.

    Maps a language string to its valid frameworks and returns their
    display-friendly names (capitalized).

    Args:
        language: Language string value (e.g., "python", "typescript")

    Returns:
        List of framework display names for the language
    """
    language_map = {
        "python": ["FastAPI", "Django", "Flask", "None"],
        "typescript": ["Next.js", "Express", "NestJS", "React", "Vue", "None"],
        "javascript": ["Next.js", "Express", "React", "Vue", "None"],
        "go": ["Gin", "Echo", "None"],
        "rust": ["Axum", "Actix", "None"],
        "java": ["Spring", "None"],
    }
    return language_map.get(language, ["None"])


def get_managers_for_language_display(language: str) -> List[str]:
    """Get package manager display names for a given language string.

    Args:
        language: Language string value (e.g., "python", "typescript")

    Returns:
        List of package manager display names for the language
    """
    manager_map = {
        "python": ["uv", "poetry", "pip", "pipenv"],
        "typescript": ["pnpm", "npm", "yarn", "bun"],
        "javascript": ["pnpm", "npm", "yarn", "bun"],
        "go": ["go"],
        "rust": ["cargo"],
        "java": ["maven", "gradle"],
    }
    return manager_map.get(language, [])


def _validate_project_name(name: str) -> tuple[bool, str]:
    """Validate project name for safe directory and package naming.

    Checks that the name is non-empty, contains only valid characters,
    and can be used as a directory name.

    Args:
        name: Project name to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.
    """
    if not name or not name.strip():
        return False, "Project name cannot be empty"

    sanitized = name.strip().lower().replace(" ", "-")

    # Check for valid slug format
    if not re.match(r"^[a-z][a-z0-9-]*$", sanitized):
        return (
            False,
            "Project name must start with a letter and contain only "
            "lowercase letters, numbers, and hyphens.",
        )

    # Check reasonable length
    if len(sanitized) > 100:
        return False, "Project name must be 100 characters or fewer"

    return True, ""


def run_enhanced_init_wizard(
    name: str,
    language: Optional[Language] = None,
    framework: Optional[Framework] = None,
    package_manager: Optional[PackageManager] = None,
    architecture: Optional[Architecture] = None,
    with_orchestrator: bool = False,
) -> Optional[TACConfig]:
    """Enhanced interactive wizard with Rich UI components and previews.

    Provides a multi-step wizard with:
    1. Branded banner
    2. Step progress headers
    3. Real-time validation feedback
    4. Smart default suggestions
    5. Directory tree preview
    6. Configuration summary
    7. Final confirmation

    The flow is:
    Step 1: Project name validation (with feedback)
    Step 2: Language selection
    Step 3: Framework selection (filtered by language)
    Step 4: Architecture selection
    Step 5: Package manager (auto-suggested)
    Step 6: Orchestrator enabled?
    Step 7: Preview directory tree + configuration summary + confirm

    Args:
        name: Project name (already provided via CLI)
        language: Pre-selected language (or None to ask)
        framework: Pre-selected framework (or None to ask)
        package_manager: Pre-selected package manager (or None to ask)
        architecture: Pre-selected architecture (or None to ask)
        with_orchestrator: Whether to include orchestrator components

    Returns:
        Configured TACConfig ready for scaffolding, or None if user cancels.

    Raises:
        SystemExit: If user cancels at confirmation prompt
    """
    total_steps = 7

    # Banner
    UIComponents.show_banner(
        "TAC Bootstrap Project Generator",
        "Interactive Setup Wizard",
    )

    # Step 1: Validate project name
    UIComponents.show_step_header(1, total_steps, "Project Name")

    is_valid, error_msg = _validate_project_name(name)
    if is_valid:
        UIComponents.show_validation_feedback("Project name", True, f"'{name}' is valid")
    else:
        UIComponents.show_validation_feedback("Project name", False, error_msg)
        console.print(f"[red]Error: {error_msg}[/red]")
        raise SystemExit(1)

    # Step 2: Language
    if language is None:
        UIComponents.show_step_header(2, total_steps, "Programming Language")
        language = select_from_enum(
            "What programming language?",
            Language,
            default=Language.PYTHON,
        )
    else:
        UIComponents.show_step_header(2, total_steps, "Programming Language")
    UIComponents.show_validation_feedback("Language", True, language.value)

    # Step 3: Framework (filtered by language)
    if framework is None:
        UIComponents.show_step_header(3, total_steps, "Framework")
        valid_frameworks = get_frameworks_for_language(language)
        framework = select_from_enum(
            "What framework?",
            Framework,
            default=Framework.NONE,
            filter_fn=lambda f: f in valid_frameworks,
        )
    else:
        UIComponents.show_step_header(3, total_steps, "Framework")
    UIComponents.show_validation_feedback("Framework", True, framework.value)

    # Step 4: Architecture
    if architecture is None:
        UIComponents.show_step_header(4, total_steps, "Architecture")
        architecture = select_from_enum(
            "What architecture pattern?",
            Architecture,
            default=Architecture.SIMPLE,
        )
    else:
        UIComponents.show_step_header(4, total_steps, "Architecture")
    UIComponents.show_validation_feedback("Architecture", True, architecture.value)

    # Step 5: Package Manager (auto-suggested based on language)
    if package_manager is None:
        UIComponents.show_step_header(5, total_steps, "Package Manager")
        valid_managers = get_package_managers_for_language(language)
        default_pm = valid_managers[0] if valid_managers else None
        package_manager = select_from_enum(
            "What package manager?",
            PackageManager,
            default=default_pm,
            filter_fn=lambda p: p in valid_managers,
        )
    else:
        UIComponents.show_step_header(5, total_steps, "Package Manager")
    UIComponents.show_validation_feedback("Package Manager", True, package_manager.value)

    # Step 6: Orchestrator
    UIComponents.show_step_header(6, total_steps, "AI Developer Workflows (ADW)")
    if not with_orchestrator:
        with_orchestrator = Confirm.ask("Enable ADW orchestrator?", default=False)
    orchestrator_status = "Enabled" if with_orchestrator else "Disabled"
    UIComponents.show_validation_feedback("Orchestrator", True, orchestrator_status)

    # Commands Configuration (smart defaults)
    console.print("\n[bold]Commands Configuration[/bold]")
    console.print("[dim]These commands will be used by Claude Code and ADW workflows[/dim]\n")

    default_commands = get_default_commands(language, package_manager)

    start_cmd = Prompt.ask(
        "  Start command",
        default=default_commands.get("start", ""),
    )
    test_cmd = Prompt.ask(
        "  Test command",
        default=default_commands.get("test", ""),
    )
    lint_cmd = Prompt.ask(
        "  Lint command (optional)",
        default=default_commands.get("lint", ""),
    )

    # Worktrees
    use_worktrees = Confirm.ask(
        "\nEnable git worktrees for parallel workflows?",
        default=True,
    )

    # Target Branch
    target_branch = Prompt.ask(
        "Target branch for merge/push (main, master, develop)",
        default="main",
    )

    # Build configuration object
    config = TACConfig(
        project=ProjectSpec(
            name=name,
            mode=ProjectMode.NEW,
            language=language,
            framework=framework,
            architecture=architecture,
            package_manager=package_manager,
        ),
        paths=PathsSpec(
            app_root="src" if architecture != Architecture.SIMPLE else ".",
        ),
        commands=CommandsSpec(
            start=start_cmd,
            test=test_cmd,
            lint=lint_cmd,
        ),
        agentic=AgenticSpec(
            target_branch=target_branch,
            worktrees=WorktreeConfig(enabled=use_worktrees, max_parallel=5),
        ),
        claude=ClaudeConfig(
            settings=ClaudeSettings(project_name=name),
        ),
        orchestrator=OrchestratorConfig(enabled=with_orchestrator),
    )

    # Step 7: Preview and confirmation
    UIComponents.show_step_header(7, total_steps, "Project Preview")
    UIComponents.show_project_tree_preview(config)
    UIComponents.show_configuration_summary(config)

    # Final confirmation
    if not Confirm.ask("\n[bold]Create project with this configuration?[/bold]", default=True):
        console.print("[yellow]Project creation cancelled.[/yellow]")
        return None

    return config


def _show_config_summary(config: TACConfig) -> None:
    """Display configuration summary table.

    Shows a formatted table with all key configuration settings
    for user review before proceeding.

    Args:
        config: TACConfig object to display
    """
    table = Table(title="Configuration Summary", show_header=True)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Project Name", config.project.name)
    table.add_row("Language", config.project.language.value)
    table.add_row("Framework", config.project.framework.value)
    table.add_row("Package Manager", config.project.package_manager.value)
    table.add_row("Architecture", config.project.architecture.value)
    table.add_row("Start Command", config.commands.start)
    table.add_row("Test Command", config.commands.test)
    table.add_row("Target Branch", config.agentic.target_branch)
    table.add_row("Worktrees Enabled", str(config.agentic.worktrees.enabled))

    console.print(table)


# ============================================================================
# Helper Functions for Entity Wizard
# ============================================================================


def _to_kebab_case(name: str) -> str:
    """Convert PascalCase to kebab-case.

    Args:
        name: PascalCase string (e.g., "UserProfile")

    Returns:
        kebab-case string (e.g., "user-profile")

    Examples:
        >>> _to_kebab_case("UserProfile")
        'user-profile'
        >>> _to_kebab_case("Product")
        'product'
        >>> _to_kebab_case("OAuth2Client")
        'o-auth2-client'
    """
    # Insert hyphen before uppercase letters (except at start)
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def _validate_entity_name_format(name: str) -> tuple[bool, str]:
    """Validate entity name is PascalCase and not a Python keyword.

    Args:
        name: Entity name to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    Examples:
        >>> _validate_entity_name_format("Product")
        (True, '')
        >>> _validate_entity_name_format("product")
        (False, 'Entity name must be PascalCase...')
        >>> _validate_entity_name_format("Class")
        (False, 'Entity name is a Python keyword...')
    """
    # Check minimum length
    if len(name) < 2:
        return False, "Entity name must be at least 2 characters long"

    # Check PascalCase pattern
    if not re.match(r"^[A-Z][a-zA-Z0-9]*$", name):
        return (
            False,
            "Entity name must be PascalCase (start with uppercase letter, "
            "followed by letters and numbers). Examples: Product, UserProfile, OAuth2Client",
        )

    # Check Python keywords
    if keyword.iskeyword(name.lower()):
        return (
            False,
            f"Entity name '{name}' is a Python reserved keyword and cannot be used. "
            "Choose a different name.",
        )

    return True, ""


def _validate_field_name_format(name: str) -> tuple[bool, str]:
    """Validate field name is snake_case and not reserved.

    Args:
        name: Field name to validate

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    Examples:
        >>> _validate_field_name_format("user_name")
        (True, '')
        >>> _validate_field_name_format("UserName")
        (False, 'Field name must be snake_case...')
        >>> _validate_field_name_format("id")
        (False, 'Field name is reserved...')
    """
    # Check snake_case pattern
    if not re.match(r"^[a-z][a-z0-9_]*$", name):
        return (
            False,
            "Field name must be snake_case (lowercase with underscores). "
            "Examples: user_name, email_address, is_active",
        )

    # Check Python keywords
    if keyword.iskeyword(name):
        return (
            False,
            f"Field name '{name}' is a Python reserved keyword and cannot be used. "
            "Choose a different name.",
        )

    # Check reserved field names
    if name in RESERVED_FIELD_NAMES:
        return (
            False,
            f"Field name '{name}' is reserved by BaseEntity. "
            f"Reserved names: {', '.join(RESERVED_FIELD_NAMES)}",
        )

    # Check SQLAlchemy conflicts
    sqlalchemy_conflicts = ("query", "metadata", "registry", "mapper")
    if name in sqlalchemy_conflicts:
        return (
            False,
            f"Field name '{name}' conflicts with SQLAlchemy attributes. "
            f"Reserved names: {', '.join(sqlalchemy_conflicts)}",
        )

    return True, ""


def _show_entity_summary(entity_spec: EntitySpec) -> None:
    """Display entity specification summary tables.

    Shows two tables:
    1. Entity metadata (name, capability, options)
    2. Fields list with all properties

    Args:
        entity_spec: EntitySpec object to display
    """
    # Table 1: Entity metadata
    meta_table = Table(title="Entity Configuration", show_header=True)
    meta_table.add_column("Setting", style="cyan")
    meta_table.add_column("Value", style="green")

    meta_table.add_row("Entity Name", entity_spec.name)
    meta_table.add_row("Capability", entity_spec.capability)
    meta_table.add_row("Field Count", str(len(entity_spec.fields)))
    meta_table.add_row("Authentication", "✓" if entity_spec.authorized else "✗")
    meta_table.add_row("Async Mode", "✓" if entity_spec.async_mode else "✗")
    meta_table.add_row("Domain Events", "✓" if entity_spec.with_events else "✗")
    meta_table.add_row("Table Name", entity_spec.table_name)

    console.print(meta_table)
    console.print()

    # Table 2: Fields
    fields_table = Table(title="Fields", show_header=True)
    fields_table.add_column("Name", style="cyan")
    fields_table.add_column("Type", style="magenta")
    fields_table.add_column("Required", style="green")
    fields_table.add_column("Unique", style="cyan")
    fields_table.add_column("Indexed", style="yellow")
    fields_table.add_column("Max Length", style="blue")

    for field in entity_spec.fields:
        required_marker = "[green]✓[/green]" if field.required else "✗"
        unique_marker = "[cyan]✓[/cyan]" if field.unique else "✗"
        indexed_marker = "[yellow]✓[/yellow]" if field.indexed else "✗"
        max_len = str(field.max_length) if field.max_length else "-"

        fields_table.add_row(
            field.name,
            field.field_type.value,
            required_marker,
            unique_marker,
            indexed_marker,
            max_len,
        )

    console.print(fields_table)


def run_entity_wizard() -> EntitySpec | None:
    """Run interactive wizard for entity specification.

    Guides the user through creating a complete entity specification
    for CRUD code generation. Includes validation, defaults, and
    a summary confirmation before returning the spec.

    Returns:
        EntitySpec object if confirmed, None if cancelled

    Example:
        >>> entity = run_entity_wizard()
        >>> if entity:
        ...     print(f"Created entity: {entity.name}")
    """
    # Welcome panel
    console.print(
        Panel.fit(
            "[bold blue]Entity Generator Wizard[/bold blue]\n\n"
            "Let's create a new CRUD entity with guided prompts.",
            title="🚀 TAC Bootstrap",
        )
    )

    # Step 1: Entity Name (PascalCase)
    console.print("\n[bold]Step 1: Entity Name[/bold]")
    console.print("[dim]Enter entity name in PascalCase (e.g., Product, UserProfile)[/dim]\n")

    entity_name = ""
    while True:
        name_input = Prompt.ask("  Entity name")
        is_valid, error_msg = _validate_entity_name_format(name_input)

        if is_valid:
            entity_name = name_input
            console.print(f"  [green]✓[/green] Entity: {entity_name}")
            break
        else:
            console.print(f"  [red]✗[/red] {error_msg}")
            console.print()

    # Step 2: Capability Name (kebab-case)
    console.print("\n[bold]Step 2: Capability Name[/bold]")
    console.print(
        "[dim]Capability groups related entities "
        "(e.g., catalog, user-management)[/dim]\n"
    )

    default_capability = _to_kebab_case(entity_name)
    capability = Prompt.ask(
        "  Capability name",
        default=default_capability,
    )
    console.print(f"  [green]✓[/green] Capability: {capability}")

    # Step 3: Fields
    console.print("\n[bold]Step 3: Define Fields[/bold]")
    console.print("[dim]Add at least one field to your entity[/dim]\n")

    fields: list[FieldSpec] = []

    while True:
        # If this is not the first iteration and user doesn't want more fields, break
        if fields and not Confirm.ask("  Add another field?", default=True):
            break

        console.print()
        console.print(f"[bold cyan]Field #{len(fields) + 1}[/bold cyan]")

        # Field name
        field_name = ""
        while True:
            name_input = Prompt.ask("    Field name (snake_case)")
            is_valid, error_msg = _validate_field_name_format(name_input)

            if is_valid:
                field_name = name_input
                break
            else:
                console.print(f"    [red]✗[/red] {error_msg}")

        # Field type
        field_type = select_from_enum(
            "    Field type",
            FieldType,
            default=FieldType.STRING,
        )

        # Required
        required = Confirm.ask("    Required?", default=True)

        # Unique
        unique = Confirm.ask("    Unique?", default=False)

        # Indexed
        indexed = Confirm.ask("    Indexed?", default=False)

        # Max length (only for STRING and TEXT types)
        max_length: int | None = None
        if field_type in (FieldType.STRING, FieldType.TEXT):
            if Confirm.ask("    Set max length?", default=False):
                max_length = IntPrompt.ask(
                    "      Max length",
                    default=255 if field_type == FieldType.STRING else 1000,
                )

        # Create field spec
        field_spec = FieldSpec(
            name=field_name,
            field_type=field_type,
            required=required,
            unique=unique,
            indexed=indexed,
            max_length=max_length,
        )
        fields.append(field_spec)
        console.print(f"    [green]✓[/green] Added field: {field_name}")

    # Validate at least one field
    if not fields:
        console.print("[red]Entity must have at least one field.[/red]")
        console.print("[yellow]Wizard cancelled.[/yellow]")
        return None

    # Step 4: Additional Options
    console.print("\n[bold]Step 4: Additional Options[/bold]\n")

    enable_auth = Confirm.ask(
        "  Generate with authentication templates?",
        default=False,
    )

    enable_async = Confirm.ask(
        "  Use async repository pattern?",
        default=False,
    )

    enable_events = Confirm.ask(
        "  Include domain events support?",
        default=False,
    )

    # Step 5: Summary and Confirmation
    console.print("\n")

    # Build the entity spec
    entity_spec = EntitySpec(
        name=entity_name,
        capability=capability,
        fields=fields,
        authorized=enable_auth,
        async_mode=enable_async,
        with_events=enable_events,
    )

    _show_entity_summary(entity_spec)

    console.print()
    if not Confirm.ask("Proceed with this configuration?", default=True):
        # Ask if they want to edit or cancel
        if Confirm.ask("Edit configuration? (No = Cancel)", default=True):
            console.print("[yellow]Restarting wizard...[/yellow]\n")
            return run_entity_wizard()  # Recursive call to restart
        else:
            console.print("[yellow]Wizard cancelled.[/yellow]")
            return None

    console.print("[green]✓ Entity specification created successfully![/green]")
    return entity_spec
