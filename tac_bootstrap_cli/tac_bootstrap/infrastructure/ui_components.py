"""
IDK: ui-components, rich-ui, interactive-wizard, terminal-visualization
Responsibility: Provides reusable Rich UI components for the interactive setup wizard
Invariants: Console rendering is consistent, no side effects on config objects

Reusable Rich UI components for TAC Bootstrap interactive wizards.
Includes branded banners, step progress headers, directory tree previews,
validation feedback, configuration summaries, and success messages.

Example usage:
    from tac_bootstrap.infrastructure.ui_components import UIComponents

    UIComponents.show_banner("TAC Bootstrap", "Interactive Setup Wizard")
    UIComponents.show_step_header(1, 7, "Project Name")
    UIComponents.show_validation_feedback("project_name", True, "Valid slug format")
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from tac_bootstrap.domain.models import Architecture, TACConfig


class UIComponents:
    """
    IDK: rich-ui, wizard-components, terminal-rendering, interactive-display
    Responsibility: Encapsulates reusable Rich UI components for wizard flows
    Invariants: All methods are static, no mutable state, per-call console
    """

    @staticmethod
    def show_banner(title: str, subtitle: Optional[str] = None) -> None:
        """Show branded banner with title and optional subtitle.

        Renders a centered, styled banner at the top of the wizard flow.
        Uses cyan for the title and dim style for the subtitle.

        Args:
            title: Main banner title text
            subtitle: Optional subtitle displayed below the title in dim style
        """
        console = Console()
        console.print()
        banner_text = f"[bold cyan]{title}[/bold cyan]"
        if subtitle:
            banner_text += f"\n[dim]{subtitle}[/dim]"
        console.print(
            Panel(
                banner_text,
                border_style="cyan",
                padding=(1, 4),
            ),
            justify="center",
        )
        console.print()

    @staticmethod
    def show_step_header(current: int, total: int, title: str) -> None:
        """Show step progress indicator with title.

        Displays a panel with step number (e.g., [1/7]) and the step title,
        providing visual progress feedback through the wizard flow.

        Args:
            current: Current step number (1-based)
            total: Total number of steps
            title: Description of the current step
        """
        console = Console()
        progress = f"[bold][{current}/{total}][/bold] {title}"
        console.print(Panel(progress, style="blue"))

    @staticmethod
    def show_project_tree_preview(config: TACConfig) -> None:
        """Display directory structure tree preview based on configuration.

        Renders a Rich Tree showing the expected project directory structure,
        adapting to the selected architecture, framework, and orchestrator settings.

        Structure varies based on:
        - Architecture: DDD adds src/ with domain/application/infrastructure layers
        - Architecture: Layered adds src/ with models/services/routes layers
        - Architecture: Clean adds src/ with entities/use_cases/adapters layers
        - Architecture: Simple shows a flat src/ directory
        - Orchestrator: When enabled, shows apps/ directory
        - Always includes: adws/, .claude/, scripts/, specs/, logs/, config.yml

        Args:
            config: TACConfig with project settings to determine structure
        """
        console = Console()
        tree = Tree(f"[bold green]{config.project.name}/[/bold green]")

        # Source directory structure based on architecture
        arch = config.project.architecture
        if arch == Architecture.DDD:
            src = tree.add("[yellow]src/[/yellow]")
            src.add("[dim]app/[/dim]")
            src.add("[dim]domain/[/dim]")
            src.add("[dim]application/[/dim]")
            src.add("[dim]infrastructure/[/dim]")
        elif arch == Architecture.CLEAN:
            src = tree.add("[yellow]src/[/yellow]")
            src.add("[dim]entities/[/dim]")
            src.add("[dim]use_cases/[/dim]")
            src.add("[dim]adapters/[/dim]")
            src.add("[dim]frameworks/[/dim]")
        elif arch == Architecture.LAYERED:
            src = tree.add("[yellow]src/[/yellow]")
            src.add("[dim]models/[/dim]")
            src.add("[dim]services/[/dim]")
            src.add("[dim]routes/[/dim]")
        elif arch == Architecture.HEXAGONAL:
            src = tree.add("[yellow]src/[/yellow]")
            src.add("[dim]domain/[/dim]")
            src.add("[dim]ports/[/dim]")
            src.add("[dim]adapters/[/dim]")
        else:
            # Simple architecture
            tree.add("[yellow]src/[/yellow]")

        # ADW workflows
        adws = tree.add("[yellow]adws/[/yellow]")
        adws.add("[dim]adw_sdlc_iso.py[/dim]")
        adws.add("[dim]adw_modules/[/dim]")
        adws.add("[dim]adw_triggers/[/dim]")

        # Claude configuration
        claude = tree.add("[yellow].claude/[/yellow]")
        claude.add("[dim]commands/[/dim]")
        claude.add("[dim]agents/[/dim]")
        claude.add("[dim]hooks/[/dim]")
        claude.add("[dim]settings.json[/dim]")

        # Standard directories
        tree.add("[yellow]scripts/[/yellow]")
        tree.add("[yellow]specs/[/yellow]")
        tree.add("[yellow]logs/[/yellow]")
        tree.add("[yellow]ai_docs/[/yellow]")
        tree.add("[yellow]app_docs/[/yellow]")

        # Orchestrator (conditional)
        if config.orchestrator.enabled:
            apps = tree.add("[yellow]apps/[/yellow]")
            apps.add("[dim]orchestrator_3_stream/[/dim]")
            apps.add("[dim]orchestrator_db/[/dim]")

        # Config files
        tree.add("[cyan]config.yml[/cyan]")
        tree.add("[cyan].gitignore[/cyan]")
        tree.add("[cyan].mcp.json[/cyan]")

        console.print(Panel(tree, title="[bold]Project Structure Preview[/bold]"))

    @staticmethod
    def prompt_with_suggestions(
        message: str,
        suggestions: List[str],
        default: Optional[str] = None,
    ) -> str:
        """Interactive prompt displaying suggestions below the input.

        Shows a prompt with an optional default value and a list of suggested
        values to help guide the user's input. Returns the user's input or
        the default value if the user presses Enter without typing.

        Args:
            message: Prompt message text
            suggestions: List of suggested values (up to 5 shown)
            default: Default value shown in brackets and used if input is empty

        Returns:
            User input string, or default value if empty input

        Example:
            >>> value = UIComponents.prompt_with_suggestions(
            ...     "Project name",
            ...     ["my-app", "api-service", "data-pipeline"],
            ...     default="my-app"
            ... )
        """
        console = Console()

        # Show suggestions
        if suggestions:
            suggestions_text = ", ".join(suggestions[:5])
            if len(suggestions) > 5:
                suggestions_text += ", ..."
            console.print(f"  [dim]Suggestions: {suggestions_text}[/dim]")

        # Build prompt
        full_message = f"{message}"
        if default:
            full_message += f" [dim]\\[{default}][/dim]"
        full_message += ": "

        try:
            value = console.input(full_message)
            return value.strip() if value.strip() else (default or "")
        except EOFError:
            return default or ""

    @staticmethod
    def show_validation_errors(errors: List[str]) -> None:
        """Display validation errors in a formatted red panel.

        Renders each error as a bullet point inside a red-bordered panel.
        Does nothing if the errors list is empty.

        Args:
            errors: List of error message strings to display
        """
        console = Console()
        if not errors:
            return

        error_text = "\n".join([f"[red]* {error}[/red]" for error in errors])
        console.print(
            Panel(
                error_text,
                title="[bold red]Validation Errors[/bold red]",
                style="red",
                border_style="red",
            )
        )

    @staticmethod
    def show_validation_feedback(field: str, is_valid: bool, message: Optional[str] = None) -> None:
        """Show inline validation feedback with check or cross mark.

        Displays a green checkmark for valid fields or a red cross for invalid
        fields, with an optional descriptive message.

        Args:
            field: Name of the field being validated
            is_valid: Whether the validation passed
            message: Optional message providing validation details
        """
        console = Console()
        if is_valid:
            symbol = "[green]v[/green]"
        else:
            symbol = "[red]x[/red]"
        text = f"  {symbol} {field}"
        if message:
            text += f": [dim]{message}[/dim]"
        console.print(text)

    @staticmethod
    def show_configuration_summary(config: TACConfig) -> None:
        """Display final configuration summary before confirmation.

        Renders a Rich Table showing all key configuration settings including
        project metadata, architecture, commands, worktree settings, and
        orchestrator status. Used as the final review step before creation.

        Args:
            config: Complete TACConfig to display
        """
        console = Console()

        table = Table(title="Project Configuration Summary", show_header=True)
        table.add_column("Setting", style="cyan", min_width=20)
        table.add_column("Value", style="green")

        # Project settings
        table.add_row("Project Name", config.project.name)
        table.add_row("Language", config.project.language.value)
        table.add_row("Framework", config.project.framework.value)
        table.add_row("Architecture", config.project.architecture.value)
        table.add_row("Package Manager", config.project.package_manager.value)

        # Commands
        if config.commands.start:
            table.add_row("Start Command", config.commands.start)
        if config.commands.test:
            table.add_row("Test Command", config.commands.test)
        if config.commands.lint:
            table.add_row("Lint Command", config.commands.lint)

        # Agentic settings
        table.add_row("Target Branch", config.agentic.target_branch)
        is_wt_enabled = config.agentic.worktrees.enabled
        worktree_status = "[green]Enabled[/green]" if is_wt_enabled else "Disabled"
        table.add_row("Worktrees", worktree_status)

        # Orchestrator
        if config.orchestrator.enabled:
            table.add_row("Orchestrator", "[green]Enabled[/green]")
        else:
            table.add_row("Orchestrator", "Disabled")

        console.print()
        console.print(table)
        console.print()

    @staticmethod
    def show_success_message(project_name: str, project_path: Path) -> None:
        """Show success message after project creation.

        Renders a green panel with the project name and location, followed
        by actionable next steps for the user.

        Args:
            project_name: Name of the created project
            project_path: Absolute path to the project directory
        """
        console = Console()
        console.print()
        console.print(
            Panel(
                f"[green bold]Project '{project_name}' created successfully![/green bold]\n"
                f"[dim]Location: {project_path}[/dim]",
                style="green",
            )
        )
        console.print()
        console.print("[bold]Next steps:[/bold]")
        console.print(f"  1. [cyan]cd {project_name}[/cyan]")
        console.print("  2. [cyan]tac-bootstrap doctor[/cyan]")
        console.print("  3. [cyan]uv run adws/adw_sdlc_iso.py --issue 1[/cyan]")
        console.print()

    @staticmethod
    def show_dry_run_preview(config: TACConfig, target_dir: Path) -> None:
        """Show dry run preview combining tree and summary.

        Displays a preview panel with target directory info, followed by
        the project tree preview and configuration summary. Used when
        --dry-run or --preview flags are passed.

        Args:
            config: TACConfig to preview
            target_dir: Target directory path
        """
        console = Console()
        preview_text = (
            f"[bold]Dry Run Preview[/bold]\n\n"
            f"[cyan]Target Directory:[/cyan] {target_dir}\n"
            f"[cyan]Project Name:[/cyan] {config.project.name}"
        )
        console.print(Panel(preview_text, border_style="yellow", title="Preview"))
        UIComponents.show_project_tree_preview(config)
        UIComponents.show_configuration_summary(config)
        console.print("[dim]Run without --dry-run to create the project[/dim]")
