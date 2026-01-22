"""Interactive wizard for TAC Bootstrap configuration.

Uses Rich for beautiful terminal UI with prompts and selections.
Provides guided step-by-step configuration for both new projects
and adding agentic layers to existing repositories.
"""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, TypeVar

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from tac_bootstrap.domain.models import (
    AgenticSpec,
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
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
) -> TACConfig:
    """Run wizard for adding agentic layer to existing project.

    Uses auto-detected settings as defaults, allowing the user to
    confirm or override each setting. Focuses on command configuration
    which is critical for existing projects.

    Args:
        repo_path: Path to existing repository
        detected: Auto-detected project settings (from DetectService)

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
    )

    # Show summary and confirm
    console.print("\n")
    _show_config_summary(config)

    if not Confirm.ask("\nProceed with this configuration?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(0)

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
