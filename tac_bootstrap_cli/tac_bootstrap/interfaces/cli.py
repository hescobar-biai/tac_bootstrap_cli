"""CLI interface for TAC Bootstrap."""

import re
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from rich.console import Console
from rich.panel import Panel

from tac_bootstrap import __version__
from tac_bootstrap.application.upgrade_service import UpgradeService
from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType
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


def version_callback(value: bool) -> None:
    """Callback for --version flag."""
    if value:
        console.print(f"TAC Bootstrap v{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
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
  [green]generate[/green]     Generate code artifacts (entities, etc.)
  [green]doctor[/green]       Validate existing setup
  [green]render[/green]       Regenerate from config.yml
  [green]upgrade[/green]      Upgrade to latest TAC Bootstrap version
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
    language: Optional[Language] = typer.Option(
        None, "--language", "-l", help="Programming language (default: python)"
    ),
    framework: Optional[Framework] = typer.Option(
        None, "--framework", "-f", help="Web framework or project type (default: none)"
    ),
    package_manager: Optional[PackageManager] = typer.Option(
        None, "--package-manager", "-p", help="Package manager (auto-detected if not specified)"
    ),
    architecture: Optional[Architecture] = typer.Option(
        None, "--architecture", "-a", help="Software architecture pattern (default: simple)"
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
            # Use defaults for any unspecified options
            if language is None:
                language = Language.PYTHON
            if framework is None:
                framework = Framework.NONE
            if architecture is None:
                architecture = Architecture.SIMPLE

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


@app.command()
def generate(
    subcommand: str = typer.Argument(..., help="Subcommand (currently only 'entity' is supported)"),
    name: str = typer.Argument(..., help="Entity name in PascalCase (e.g., Product, UserProfile)"),
    capability: Annotated[Optional[str], typer.Option("--capability", "-c")] = None,
    fields: Annotated[Optional[str], typer.Option("--fields", "-f")] = None,
    authorized: Annotated[bool, typer.Option("--authorized")] = False,
    async_mode: Annotated[bool, typer.Option("--async")] = False,
    with_events: Annotated[bool, typer.Option("--with-events")] = False,
    interactive: Annotated[bool, typer.Option("--interactive/--no-interactive")] = True,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    force: Annotated[bool, typer.Option("--force")] = False,
) -> None:
    """
    Generate code artifacts from specifications.

    Currently supports generating CRUD entities with complete vertical slices
    (domain model, schemas, service, repository, routes).

    Examples:
        # Interactive mode (default) - launches wizard
        $ tac-bootstrap generate entity Product

        # Non-interactive with fields
        $ tac-bootstrap generate entity Product -c catalog --no-interactive \\
          --fields "name:str:required,price:float:required,description:text"

        # Preview without creating files
        $ tac-bootstrap generate entity Product --dry-run

        # With async repository and domain events
        $ tac-bootstrap generate entity Product --async --with-events

        # With authorization on create/update/delete endpoints
        $ tac-bootstrap generate entity Product --authorized
    """
    try:
        # Validate subcommand
        if subcommand != "entity":
            console.print(
                f"[red]Error:[/red] Unknown subcommand '{subcommand}'. "
                "Currently only 'entity' is supported."
            )
            console.print(
                "\n[yellow]Example:[/yellow] tac-bootstrap generate entity Product"
            )
            raise typer.Exit(1)

        # Auto-generate capability from entity name if not provided
        if capability is None:
            # Convert PascalCase to kebab-case: ProductCategory -> product-category
            capability = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
            console.print(f"[dim]Auto-generated capability: {capability}[/dim]")

        # Parse fields or launch wizard
        field_specs: list[FieldSpec] = []

        if fields:
            # Non-interactive mode: parse fields string
            # Format: "name:type:required,name:type"
            try:
                for field_def in fields.split(','):
                    parts = field_def.strip().split(':')
                    if len(parts) < 2:
                        console.print(
                            f"[red]Error:[/red] Invalid field definition '{field_def}'. "
                            "Expected format: name:type or name:type:required"
                        )
                        raise typer.Exit(1)

                    field_name = parts[0].strip()
                    field_type_str = parts[1].strip()
                    is_required = parts[2].strip().lower() == 'required' if len(parts) > 2 else True

                    # Map string type to FieldType
                    type_mapping = {
                        'str': FieldType.STRING,
                        'int': FieldType.INTEGER,
                        'float': FieldType.FLOAT,
                        'bool': FieldType.BOOLEAN,
                        'datetime': FieldType.DATETIME,
                        'uuid': FieldType.UUID,
                        'text': FieldType.TEXT,
                        'decimal': FieldType.DECIMAL,
                        'json': FieldType.JSON,
                    }

                    if field_type_str not in type_mapping:
                        console.print(
                            f"[red]Error:[/red] Unknown field type '{field_type_str}'. "
                            f"Supported types: {', '.join(type_mapping.keys())}"
                        )
                        raise typer.Exit(1)

                    field_specs.append(
                        FieldSpec(
                            name=field_name,
                            field_type=type_mapping[field_type_str],
                            required=is_required,
                        )
                    )

            except ValueError as e:
                console.print(f"[red]Error parsing fields:[/red] {e}")
                raise typer.Exit(1)

        elif interactive:
            # Interactive mode: launch wizard
            from tac_bootstrap.interfaces.entity_wizard import run_entity_field_wizard

            try:
                field_specs = run_entity_field_wizard()
            except (SystemExit, ValueError) as e:
                console.print(f"[yellow]Wizard cancelled or failed: {e}[/yellow]")
                raise typer.Exit(1)

        else:
            # Non-interactive mode without fields - error
            console.print(
                "[red]Error:[/red] --fields is required in non-interactive mode"
            )
            console.print(
                "\n[yellow]Example:[/yellow] tac-bootstrap generate entity Product "
                '--no-interactive --fields "name:str:required,price:float"'
            )
            raise typer.Exit(1)

        # Build EntitySpec
        try:
            entity_spec = EntitySpec(
                name=name,
                capability=capability,
                fields=field_specs,
                authorized=authorized,
                async_mode=async_mode,
                with_events=with_events,
            )
        except ValueError as e:
            console.print(f"[red]Invalid entity specification:[/red] {e}")
            raise typer.Exit(1)

        # Generate entity using EntityGeneratorService
        from tac_bootstrap.application.entity_generator_service import EntityGeneratorService

        service = EntityGeneratorService()
        target_dir = Path.cwd()

        try:
            result = service.generate(
                entity_spec=entity_spec,
                target_dir=target_dir,
                dry_run=dry_run,
                force=force,
            )

            if dry_run:
                # Show preview
                preview_text = f"""[bold]Dry Run - Preview[/bold]

[cyan]Entity:[/cyan] {entity_spec.name}
[cyan]Capability:[/cyan] {entity_spec.capability}
[cyan]Fields:[/cyan] {len(entity_spec.fields)}
[cyan]Async Mode:[/cyan] {entity_spec.async_mode}
[cyan]With Events:[/cyan] {entity_spec.with_events}
[cyan]Authorized:[/cyan] {entity_spec.authorized}

[bold]Would create:[/bold]
"""
                console.print(Panel(preview_text, border_style="yellow", title="Preview"))

                for file_path in result.files_created:
                    console.print(f"  📄 {file_path}")

                console.print("\n[dim]Run without --dry-run to create the files[/dim]")
                return

            # Show success
            success_text = f"""[bold green]✓ Entity generated successfully![/bold green]

[cyan]Entity:[/cyan] {entity_spec.name}
[cyan]Capability:[/cyan] {entity_spec.capability}
[cyan]Files Created:[/cyan] {len(result.files_created)}

[bold]Created Files:[/bold]
"""
            for file_path in result.files_created:
                success_text += f"  📄 {file_path}\n"

            success_text += """
[bold]Next Steps:[/bold]
  1. Register router in main.py:
     [dim]from interfaces.api.{capability}.{snake_name}_routes import router
     app.include_router(router)[/dim]

  2. Run database migrations (if using a database)
     [dim]alembic revision --autogenerate -m "Add {name}"
     alembic upgrade head[/dim]
"""

            if entity_spec.with_events:
                success_text += """
  3. Import and register domain events (if using event bus)
     [dim]from domain.{capability}.events.{snake_name}_events import *[/dim]
"""

            success_text = success_text.format(
                capability=entity_spec.capability.replace('-', '_'),
                snake_name=entity_spec.snake_name,
                name=entity_spec.name,
            )

            console.print(Panel(success_text, border_style="green", title="Success"))

        except ValueError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def upgrade(
    path: Path = typer.Argument(
        Path("."),
        help="Path to project to upgrade",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Show what would be changed without making changes",
    ),
    backup: bool = typer.Option(
        True,
        "--backup/--no-backup",
        help="Create backup before upgrading (default: enabled)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force upgrade even if versions match",
    ),
) -> None:
    """Upgrade agentic layer to latest TAC Bootstrap version.

    This command updates the adws/, .claude/, and scripts/ directories
    to the latest templates while preserving your project configuration.

    Examples:
        tac-bootstrap upgrade                    # Upgrade current directory
        tac-bootstrap upgrade ./my-project       # Upgrade specific project
        tac-bootstrap upgrade --dry-run          # Preview changes
        tac-bootstrap upgrade --no-backup        # Upgrade without backup
    """
    project_path = path.resolve()

    # Verify it's a TAC project
    config_file = project_path / "config.yml"
    if not config_file.exists():
        console.print("[red]Error: No config.yml found. Is this a TAC Bootstrap project?[/red]")
        raise typer.Exit(1)

    service = UpgradeService(project_path)

    # Check versions
    needs_upgrade, current_ver, target_ver = service.needs_upgrade()

    console.print("\n[bold]TAC Bootstrap Upgrade[/bold]")
    console.print(f"  Current version: [yellow]{current_ver}[/yellow]")
    console.print(f"  Target version:  [green]{target_ver}[/green]")

    if not needs_upgrade and not force:
        console.print("\n[green]Project is already up to date![/green]")
        raise typer.Exit(0)

    # Show changes preview
    console.print("\n[bold]Changes to be made:[/bold]")
    for change in service.get_changes_preview():
        console.print(f"  • {change}")

    if dry_run:
        console.print("\n[yellow]Dry run - no changes made[/yellow]")
        raise typer.Exit(0)

    # Confirm upgrade
    if not typer.confirm("\nProceed with upgrade?", default=True):
        console.print("[yellow]Upgrade cancelled[/yellow]")
        raise typer.Exit(0)

    # Perform upgrade
    console.print("\n[bold]Upgrading...[/bold]")
    success, message = service.perform_upgrade(backup=backup)

    if success:
        console.print(f"\n[green]✓ {message}[/green]")
        if backup:
            console.print("[dim]Backup preserved. Delete manually when confirmed working.[/dim]")
    else:
        console.print(f"\n[red]✗ {message}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
