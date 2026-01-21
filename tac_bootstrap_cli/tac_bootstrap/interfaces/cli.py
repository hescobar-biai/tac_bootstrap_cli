"""CLI interface for TAC Bootstrap."""

from pathlib import Path
from typing import Optional

import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from tac_bootstrap import __version__
from tac_bootstrap.domain.models import (
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    PackageManager,
    PathsSpec,
    ProjectSpec,
    TACConfig,
    get_default_commands,
    get_package_managers_for_language,
)

# Rich console for formatted output
console = Console()

# Typer app with metadata
app = typer.Typer(
    name="tac-bootstrap",
    help="Bootstrap Agentic Layer for Claude Code with TAC patterns",
    add_completion=False,
    rich_markup_mode="rich",
)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """
    Bootstrap Agentic Layer for Claude Code with TAC patterns.

    TAC Bootstrap generates AI-powered development workflows, slash commands,
    and templates for your project using Claude Code.
    """
    if ctx.invoked_subcommand is None:
        # Show welcome panel
        welcome_text = f"""[bold cyan]TAC Bootstrap v{__version__}[/bold cyan]

Bootstrap Agentic Layer for Claude Code with TAC patterns.

[bold]Available Commands:[/bold]
  [green]init[/green]         Create new project with Agentic Layer
  [green]add-agentic[/green]  Inject Agentic Layer into existing repo
  [green]doctor[/green]       Validate existing setup
  [green]render[/green]       Regenerate from config.yml
  [green]version[/green]      Show version

Use [cyan]tac-bootstrap --help[/cyan] for more information.
Use [cyan]tac-bootstrap COMMAND --help[/cyan] for command-specific help.
"""
        console.print(Panel(welcome_text, border_style="cyan", padding=(1, 2)))


@app.command()
def version() -> None:
    """
    Show version information.

    Examples:
        $ tac-bootstrap version
    """
    version_text = f"[bold cyan]TAC Bootstrap[/bold cyan] version [green]{__version__}[/green]"
    console.print(Panel(version_text, border_style="cyan"))


@app.command()
def init(
    name: str = typer.Argument(..., help="Project name"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output directory (default: ./{name})"
    ),
    language: Language = typer.Option(
        Language.PYTHON, "--language", "-l", help="Programming language"
    ),
    framework: Framework = typer.Option(
        Framework.NONE, "--framework", "-f", help="Web framework or project type"
    ),
    package_manager: Optional[PackageManager] = typer.Option(
        None, "--package-manager", "-p", help="Package manager (auto-detected if not specified)"
    ),
    architecture: Architecture = typer.Option(
        Architecture.SIMPLE, "--architecture", "-a", help="Software architecture pattern"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", help="Use interactive wizard"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without creating files"),
) -> None:
    """
    Create a new project with Agentic Layer.

    Scaffolds a new project directory with AI-powered development workflows,
    slash commands, templates, and configuration files.

    Examples:
        # Interactive mode (default)
        $ tac-bootstrap init my-app

        # Non-interactive with options
        $ tac-bootstrap init my-api --language python --framework fastapi \\
          --package-manager uv --architecture ddd --no-interactive

        # Preview without creating files
        $ tac-bootstrap init my-app --dry-run
    """
    try:
        # Determine target directory
        target_dir = output_dir or Path.cwd() / name
        target_dir = target_dir.resolve()

        if interactive:
            from tac_bootstrap.interfaces.wizard import run_init_wizard

            config = run_init_wizard(
                name=name,
                language=language,
                framework=framework,
                package_manager=package_manager,
                architecture=architecture,
            )
        else:
            # Non-interactive mode: build config from CLI arguments
            # Auto-detect package manager if not specified
            if package_manager is None:
                valid_pms = get_package_managers_for_language(language)
                if not valid_pms:
                    console.print(f"[red]No package managers available for {language.value}[/red]")
                    raise typer.Exit(1)
                package_manager = valid_pms[0]  # Use first as default
                console.print(f"[dim]Auto-detected package manager: {package_manager.value}[/dim]")

            # Build configuration
            default_cmds = get_default_commands(language, package_manager)
            config = TACConfig(
                project=ProjectSpec(
                    name=name,
                    language=language,
                    framework=framework,
                    architecture=architecture,
                    package_manager=package_manager,
                ),
                paths=PathsSpec(app_root="src"),
                commands=CommandsSpec(
                    start=default_cmds.get("start", ""),
                    test=default_cmds.get("test", ""),
                    lint=default_cmds.get("lint", ""),
                    typecheck=default_cmds.get("typecheck", ""),
                    format=default_cmds.get("format", ""),
                    build=default_cmds.get("build", ""),
                ),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name=name)),
            )

        # Import scaffold service (will fail if not implemented yet)
        try:
            from tac_bootstrap.application.scaffold_service import ScaffoldService

            service = ScaffoldService()
            plan = service.build_plan(config, existing_repo=False)

            if dry_run:
                # Show preview (use values from config which are guaranteed to be set)
                preview_text = f"""[bold]Dry Run - Preview[/bold]

[cyan]Target Directory:[/cyan] {target_dir}
[cyan]Project Name:[/cyan] {config.project.name}
[cyan]Language:[/cyan] {config.project.language.value}
[cyan]Framework:[/cyan] {config.project.framework.value}
[cyan]Package Manager:[/cyan] {config.project.package_manager.value}
[cyan]Architecture:[/cyan] {config.project.architecture.value}

[bold]Would create:[/bold]
"""
                console.print(Panel(preview_text, border_style="yellow", title="Preview"))

                # List directories and files from plan
                console.print("[bold cyan]Directories:[/bold cyan]")
                for dir_op in plan.directories:
                    console.print(f"  📁 {dir_op.path}")

                console.print("\n[bold cyan]Files:[/bold cyan]")
                for file_op in plan.files:
                    console.print(f"  📄 {file_op.path}")

                console.print("\n[dim]Run without --dry-run to create the project[/dim]")
                return

            # Apply plan
            result = service.apply_plan(plan, target_dir, config, force=False)

            # Show success
            success_text = f"""[bold green]✓ Project created successfully![/bold green]

[cyan]Location:[/cyan] {target_dir}
[cyan]Files Created:[/cyan] {result.files_created}
[cyan]Directories Created:[/cyan] {result.directories_created}

[bold]Next Steps:[/bold]
  1. cd {name}
  2. Review generated files
  3. Initialize git: git init
  4. Start development with Claude Code
"""
            console.print(Panel(success_text, border_style="green", title="Success"))

        except ImportError as e:
            console.print(f"[red]ScaffoldService not yet implemented: {e}[/red]")
            console.print("[yellow]This feature will be available in TAREA 4.2[/yellow]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def add_agentic(
    repo_path: Path = typer.Argument(
        Path("."), help="Repository path (default: current directory)"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", help="Use interactive wizard"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without modifying files"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),
) -> None:
    """
    Inject Agentic Layer into an existing repository.

    Auto-detects project settings (language, framework, package manager) and
    generates the Agentic Layer configuration files.

    Examples:
        # Add to current directory with auto-detection
        $ tac-bootstrap add-agentic

        # Add to specific repo
        $ tac-bootstrap add-agentic /path/to/repo

        # Preview changes without applying
        $ tac-bootstrap add-agentic --dry-run

        # Force overwrite existing files
        $ tac-bootstrap add-agentic --force
    """
    try:
        # Resolve to absolute path
        repo_path = repo_path.resolve()

        # Validate path exists
        if not repo_path.exists():
            console.print(f"[red]Error:[/red] Directory does not exist: {repo_path}")
            raise typer.Exit(1)

        if not repo_path.is_dir():
            console.print(f"[red]Error:[/red] Not a directory: {repo_path}")
            raise typer.Exit(1)

        # Auto-detect project settings
        try:
            from tac_bootstrap.application.detect_service import DetectService

            detector = DetectService()
            detected = detector.detect(repo_path)

            # Show auto-detection results
            framework_display = detected.framework.value if detected.framework else "None"
            detection_text = f"""[bold]Auto-Detection Results[/bold]

[cyan]Repository:[/cyan] {repo_path}
[cyan]Language:[/cyan] {detected.language.value}
[cyan]Framework:[/cyan] {framework_display}
[cyan]Package Manager:[/cyan] {detected.package_manager.value}
[cyan]App Root:[/cyan] {detected.app_root or "."}
"""
            console.print(Panel(detection_text, border_style="cyan", title="Detection"))

            if interactive:
                from tac_bootstrap.interfaces.wizard import run_add_agentic_wizard

                config = run_add_agentic_wizard(repo_path, detected)
            else:
                # Non-interactive mode: build config from detected settings
                # Use repo directory name as project name
                project_name = repo_path.name
                default_cmds = get_default_commands(detected.language, detected.package_manager)
                config = TACConfig(
                    project=ProjectSpec(
                        name=project_name,
                        language=detected.language,
                        framework=detected.framework or Framework.NONE,
                        package_manager=detected.package_manager,
                    ),
                    paths=PathsSpec(app_root=detected.app_root or "src"),
                    commands=CommandsSpec(
                        start=default_cmds.get("start", ""),
                        test=default_cmds.get("test", ""),
                        lint=default_cmds.get("lint", ""),
                        typecheck=default_cmds.get("typecheck", ""),
                        format=default_cmds.get("format", ""),
                        build=default_cmds.get("build", ""),
                    ),
                    claude=ClaudeConfig(settings=ClaudeSettings(project_name=project_name)),
                )

            # Build and apply plan
            from tac_bootstrap.application.scaffold_service import ScaffoldService

            service = ScaffoldService()
            plan = service.build_plan(config, existing_repo=True)

            if dry_run:
                # Show preview
                preview_text = f"""[bold]Dry Run - Preview[/bold]

[cyan]Target Repository:[/cyan] {repo_path}

[bold]Would create/modify:[/bold]
"""
                console.print(Panel(preview_text, border_style="yellow", title="Preview"))

                # Show directories
                for dir_op in plan.directories:
                    console.print(f"  📁 Create {dir_op.path}")

                # Show files
                for file_op in plan.files:
                    action = (
                        "📝 Modify"
                        if file_op.action.value in ("overwrite", "patch")
                        else "📄 Create"
                    )
                    console.print(f"  {action} {file_op.path}")

                console.print("\n[dim]Run without --dry-run to apply changes[/dim]")
                return

            # Apply plan
            result = service.apply_plan(plan, repo_path, config, force=force)

            # Show success
            success_text = f"""[bold green]✓ Agentic Layer added successfully![/bold green]

[cyan]Location:[/cyan] {repo_path}
[cyan]Files Created:[/cyan] {result.files_created}
[cyan]Files Modified:[/cyan] {result.files_overwritten}

[bold]Next Steps:[/bold]
  1. Review generated files in .claude/, adws/, scripts/
  2. Update config.yml with your specific commands
  3. Start using slash commands in Claude Code
"""
            console.print(Panel(success_text, border_style="green", title="Success"))

        except ImportError as e:
            console.print(f"[red]DetectService not yet implemented: {e}[/red]")
            console.print("[yellow]This feature will be available in FASE 6[/yellow]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def doctor(
    repo_path: Path = typer.Argument(
        Path("."), help="Repository path (default: current directory)"
    ),
    fix: bool = typer.Option(False, "--fix", help="Attempt to fix issues automatically"),
) -> None:
    """
    Validate existing Agentic Layer setup.

    Performs health checks on your Agentic Layer configuration and reports
    any issues with severity levels (error, warning, info).

    Examples:
        # Check current directory
        $ tac-bootstrap doctor

        # Check specific repo
        $ tac-bootstrap doctor /path/to/repo

        # Check and auto-fix issues
        $ tac-bootstrap doctor --fix
    """
    try:
        # Resolve to absolute path
        repo_path = repo_path.resolve()

        console.print(f"[cyan]Diagnosing:[/cyan] {repo_path}\n")

        # Run diagnostics
        try:
            from tac_bootstrap.application.doctor_service import DoctorService

            doctor_service = DoctorService()
            report = doctor_service.diagnose(repo_path)

            if report.healthy:
                # Show success
                success_text = """[bold green]✓ All checks passed![/bold green]

Your Agentic Layer setup is healthy.
"""
                console.print(Panel(success_text, border_style="green", title="Healthy"))
                return

            # Show issues
            error_count = sum(1 for issue in report.issues if issue.severity == "error")
            warning_count = sum(1 for issue in report.issues if issue.severity == "warning")
            info_count = sum(1 for issue in report.issues if issue.severity == "info")

            status_text = f"""[bold red]✗ Issues detected[/bold red]

[red]Errors:[/red] {error_count}
[yellow]Warnings:[/yellow] {warning_count}
[blue]Info:[/blue] {info_count}
"""
            console.print(Panel(status_text, border_style="red", title="Unhealthy"))

            # List each issue
            for issue in report.issues:
                if issue.severity == "error":
                    color = "red"
                    icon = "✗"
                elif issue.severity == "warning":
                    color = "yellow"
                    icon = "⚠"
                else:  # info
                    color = "blue"
                    icon = "ℹ"

                console.print(f"\n[{color}]{icon} [{issue.severity.upper()}][/{color}]")
                console.print(f"  {issue.message}")
                if issue.suggestion:
                    console.print(f"  [dim]Suggestion: {issue.suggestion}[/dim]")

            # Auto-fix if requested
            if fix:
                console.print("\n[cyan]Attempting to fix issues...[/cyan]")
                fix_result = doctor_service.fix(repo_path, report)
                console.print(f"[green]Fixed {fix_result.fixed_count} issues[/green]")

                if fix_result.failed_count > 0:
                    console.print(
                        f"[yellow]Failed to fix {fix_result.failed_count} issues[/yellow]"
                    )

            raise typer.Exit(1)

        except ImportError as e:
            console.print(f"[red]DoctorService not yet implemented: {e}[/red]")
            console.print("[yellow]This feature will be available in FASE 7[/yellow]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def render(
    config_file: Path = typer.Argument(
        Path("config.yml"), help="Configuration file path (default: config.yml)"
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory (default: same as config file location)",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without modifying files"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),
) -> None:
    """
    Regenerate Agentic Layer from config.yml.

    Reads an existing config.yml file and regenerates all Agentic Layer files
    based on the configuration. Useful after manually editing config.yml.

    Examples:
        # Regenerate from default config.yml
        $ tac-bootstrap render

        # Regenerate from specific config file
        $ tac-bootstrap render my-config.yml

        # Preview changes without applying
        $ tac-bootstrap render --dry-run

        # Force overwrite existing files
        $ tac-bootstrap render --force
    """
    try:
        # Resolve to absolute path
        config_file = config_file.resolve()

        # Validate config file exists
        if not config_file.exists():
            console.print(f"[red]Error:[/red] Config file does not exist: {config_file}")
            raise typer.Exit(1)

        # Load and parse YAML
        try:
            with open(config_file, "r") as f:
                raw_config = yaml.safe_load(f)

            # Validate with Pydantic
            config = TACConfig(**raw_config)

            console.print(f"[green]✓[/green] Loaded config from {config_file}")

        except yaml.YAMLError as e:
            console.print(f"[red]YAML Parse Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Config Validation Error:[/red] {e}")
            raise typer.Exit(1)

        # Determine target directory
        target_dir = output_dir or config_file.parent
        target_dir = target_dir.resolve()

        # Build plan
        try:
            from tac_bootstrap.application.scaffold_service import ScaffoldService

            service = ScaffoldService()
            plan = service.build_plan(config, existing_repo=True)

            if dry_run:
                # Show preview
                preview_text = f"""[bold]Dry Run - Preview[/bold]

[cyan]Config File:[/cyan] {config_file}
[cyan]Target Directory:[/cyan] {target_dir}
[cyan]Project:[/cyan] {config.project.name}

[bold]Would create/modify:[/bold]
"""
                console.print(Panel(preview_text, border_style="yellow", title="Preview"))

                # Show directories
                for dir_op in plan.directories:
                    console.print(f"  📁 Create {dir_op.path}")

                # Show files
                for file_op in plan.files:
                    action = (
                        "📝 Modify"
                        if file_op.action.value in ("overwrite", "patch")
                        else "📄 Create"
                    )
                    console.print(f"  {action} {file_op.path}")

                console.print("\n[dim]Run without --dry-run to apply changes[/dim]")
                return

            # Apply plan
            result = service.apply_plan(plan, target_dir, config, force=force)

            # Show success
            success_text = f"""[bold green]✓ Rendered successfully![/bold green]

[cyan]Target:[/cyan] {target_dir}
[cyan]Files Created:[/cyan] {result.files_created}
[cyan]Files Modified:[/cyan] {result.files_overwritten}

All files have been regenerated from {config_file.name}
"""
            console.print(Panel(success_text, border_style="green", title="Success"))

        except ImportError as e:
            console.print(f"[red]ScaffoldService not yet implemented: {e}[/red]")
            console.print("[yellow]This feature will be available in TAREA 4.2[/yellow]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
