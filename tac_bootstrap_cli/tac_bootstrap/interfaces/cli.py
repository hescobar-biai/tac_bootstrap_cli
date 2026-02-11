"""CLI interface for TAC Bootstrap."""

import re
from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tac_bootstrap import __version__
from tac_bootstrap.application.migration_service import MigrationService
from tac_bootstrap.application.upgrade_service import UpgradeService
from tac_bootstrap.application.validation_service import ValidationLevel, ValidationService
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from tac_bootstrap.domain.entity_config import EntitySpec, FieldSpec, FieldType
from tac_bootstrap.domain.models import (
    Architecture,
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Framework,
    Language,
    OrchestratorConfig,
    PackageManager,
    PathsSpec,
    ProjectSpec,
    TACConfig,
    get_default_commands,
    get_package_managers_for_language,
)
from tac_bootstrap.infrastructure.ui_components import UIComponents

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
  [green]health-check[/green] Check system health and requirements
  [green]validate[/green]     Validate project configuration
  [green]render[/green]       Regenerate from config.yml
  [green]upgrade[/green]      Upgrade to latest TAC Bootstrap version
  [green]migrate[/green]      Migrate config schema to specific version
  [green]rollback[/green]     Rollback previous schema migration(s)
  [green]telemetry[/green]    Manage anonymous usage tracking
  [green]plugin[/green]       Manage plugins
  [green]template[/green]     Template store (search, install, rate)
  [green]security[/green]     Security scanning and auditing
  [green]docs[/green]         Generate project documentation
  [green]test-generate[/green] Generate test scaffolding
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
    with_orchestrator: bool = typer.Option(
        False, "--with-orchestrator", help="Include orchestrator backend and frontend (TAC-14)"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", help="Use interactive wizard"
    ),
    enhanced: bool = typer.Option(
        False, "--enhanced", "-e", help="Use enhanced wizard with Rich UI and previews"
    ),
    preview: bool = typer.Option(
        False, "--preview", help="Show directory tree preview without creating files"
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

        # Enhanced wizard with Rich UI and tree preview
        $ tac-bootstrap init my-app --enhanced

        # Show directory structure preview only
        $ tac-bootstrap init my-app --preview

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

        # Handle --preview: show directory tree without creating
        if preview:
            # Build a minimal config for preview
            preview_lang = language or Language.PYTHON
            preview_fw = framework or Framework.NONE
            preview_arch = architecture or Architecture.SIMPLE
            preview_pm = package_manager or PackageManager.UV
            preview_config = TACConfig(
                project=ProjectSpec(
                    name=name,
                    language=preview_lang,
                    framework=preview_fw,
                    architecture=preview_arch,
                    package_manager=preview_pm,
                ),
                paths=PathsSpec(app_root="src"),
                commands=CommandsSpec(start="", test=""),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name=name)),
                orchestrator=OrchestratorConfig(enabled=with_orchestrator),
            )
            UIComponents.show_project_tree_preview(preview_config)
            UIComponents.show_configuration_summary(preview_config)
            return

        if enhanced:
            from tac_bootstrap.interfaces.wizard import run_enhanced_init_wizard

            config = run_enhanced_init_wizard(
                name=name,
                language=language,
                framework=framework,
                package_manager=package_manager,
                architecture=architecture,
                with_orchestrator=with_orchestrator,
            )
            if config is None:
                # User cancelled
                raise typer.Exit(0)
        elif interactive:
            from tac_bootstrap.interfaces.wizard import run_init_wizard

            config = run_init_wizard(
                name=name,
                language=language,
                framework=framework,
                package_manager=package_manager,
                architecture=architecture,
                with_orchestrator=with_orchestrator,
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
                orchestrator=OrchestratorConfig(enabled=with_orchestrator),
            )

        # Run preflight validation checks before scaffolding
        template_repo = TemplateRepository()
        vs = ValidationService(template_repo)
        preflight_result = vs.run_preflight_checks(config, target_dir)

        if not preflight_result.valid:
            error_count = len(preflight_result.errors())
            console.print(
                f"\n[bold red]Preflight validation failed with {error_count} error(s):[/bold red]"
            )
            for issue in preflight_result.errors():
                console.print(f"  [red][x][/red] {issue.message}")
                if issue.suggestion:
                    console.print(f"      [dim]{issue.suggestion}[/dim]")
            for issue in preflight_result.warnings():
                console.print(f"  [yellow][!][/yellow] {issue.message}")
                if issue.suggestion:
                    console.print(f"      [dim]{issue.suggestion}[/dim]")
            console.print(
                "\n[dim]Fix the errors above and try again. "
                "Run 'tac-bootstrap validate' for detailed diagnostics.[/dim]"
            )
            raise typer.Exit(1)

        # Show warnings if any
        if preflight_result.warnings():
            for issue in preflight_result.warnings():
                console.print(f"  [yellow][!][/yellow] {issue.message}")

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

        # Show success using UIComponents for enhanced mode, standard display otherwise
        if enhanced:
            UIComponents.show_success_message(name, target_dir)
        else:
            success_text = f"""[bold green]Project created successfully![/bold green]

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

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def add_agentic(
    repo_path: Path = typer.Argument(
        Path("."), help="Repository path (default: current directory)"
    ),
    with_orchestrator: bool = typer.Option(
        False, "--with-orchestrator", help="Include orchestrator backend and frontend (TAC-14)"
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

            config = run_add_agentic_wizard(
                repo_path, detected, with_orchestrator=with_orchestrator
            )
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
                orchestrator=OrchestratorConfig(enabled=with_orchestrator),
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

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def generate(
    subcommand: str = typer.Argument(..., help="Subcommand (currently only 'entity' is supported)"),
    name: str = typer.Argument(..., help="Entity name in PascalCase (e.g., Product, UserProfile)"),
    capability: Annotated[Optional[str], typer.Option("--capability", "-c")] = None,
    fields: Annotated[Optional[str], typer.Option("--fields", "-f")] = None,
    authorized: Annotated[
        bool,
        typer.Option(
            "--authorized",
            help=(
                "Generate with multi-tenant authorization "
                "(organization-level isolation, JWT authentication)"
            ),
        ),
    ] = False,
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

        # With multi-tenant authorization (organization-level isolation)
        $ tac-bootstrap generate entity Product --authorized \\
          --fields "name:str:required,price:float:required"
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
    with_orchestrator: bool = typer.Option(
        False,
        "--with-orchestrator",
        help="Enable orchestrator (adds apps/orchestrator_3_stream/ and apps/orchestrator_db/)",
    ),
) -> None:
    """Upgrade agentic layer to latest TAC Bootstrap version.

    This command updates the adws/, .claude/, and scripts/ directories
    to the latest templates while preserving your project configuration.

    Examples:
        tac-bootstrap upgrade                          # Upgrade current directory
        tac-bootstrap upgrade ./my-project             # Upgrade specific project
        tac-bootstrap upgrade --dry-run                # Preview changes
        tac-bootstrap upgrade --no-backup              # Upgrade without backup
        tac-bootstrap upgrade --with-orchestrator      # Add orchestrator to project
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

    if not needs_upgrade and not force and not with_orchestrator:
        console.print("\n[green]Project is already up to date![/green]")
        raise typer.Exit(0)

    # Show changes preview
    console.print("\n[bold]Changes to be made:[/bold]")
    for change in service.get_changes_preview(with_orchestrator=with_orchestrator):
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
    success, message = service.perform_upgrade(
        backup=backup, with_orchestrator=with_orchestrator
    )

    if success:
        console.print(f"\n[green]✓ {message}[/green]")
        if backup:
            console.print("[dim]Backup preserved. Delete manually when confirmed working.[/dim]")
    else:
        console.print(f"\n[red]✗ {message}[/red]")
        raise typer.Exit(1)


@app.command()
def migrate(
    repo_path: Path = typer.Argument(
        Path("."),
        help="Project root directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    to_version: str = typer.Argument(..., help="Target schema version (e.g., 2)"),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-n",
        help="Preview changes without applying",
    ),
    backup: bool = typer.Option(
        True,
        "--backup/--no-backup",
        help="Create backup before migrating (default: enabled)",
    ),
) -> None:
    """
    Migrate config.yml to a specific schema version.

    Applies forward or backward schema migrations to transform config.yml
    between schema versions. Supports multi-step migration paths.

    Examples:
        tac-bootstrap migrate . 2                   # Migrate to schema v2
        tac-bootstrap migrate ./my-project 2        # Migrate specific project
        tac-bootstrap migrate . 2 --dry-run         # Preview migration changes
        tac-bootstrap migrate . 1 --no-backup       # Rollback to v1 without backup
    """
    project_path = repo_path.resolve()

    # Verify config.yml exists
    config_file = project_path / "config.yml"
    if not config_file.exists():
        console.print("[red]Error: No config.yml found. Is this a TAC Bootstrap project?[/red]")
        raise typer.Exit(1)

    service = MigrationService(project_path)
    current_version = service.detect_current_version()
    target = to_version

    console.print("\n[bold]TAC Bootstrap Schema Migration[/bold]")
    console.print(f"  Current schema version: [yellow]{current_version}[/yellow]")
    console.print(f"  Target schema version:  [green]{target}[/green]")

    # Check if already at target
    if current_version == target:
        console.print(
            f"\n[green]Already at schema version {target}. No migration needed.[/green]"
        )
        raise typer.Exit(0)

    # Check if migration path exists
    if not service.can_migrate(current_version, target):
        console.print(
            f"\n[red]Error: No migration path from version {current_version} "
            f"to {target}.[/red]"
        )
        raise typer.Exit(1)

    # Dry-run mode
    if dry_run:
        changes = service.dry_run(target)
        console.print("\n[bold]Preview of changes:[/bold]")
        for change in changes:
            console.print(f"  {change}")
        console.print("\n[yellow]Dry run - no changes made[/yellow]")
        raise typer.Exit(0)

    # Apply migration
    console.print("\n[bold]Applying migration...[/bold]")
    success, message = service.apply_migration(target, backup=backup)

    if success:
        console.print(f"\n[green]✓ {message}[/green]")
        if backup:
            console.print(
                "[dim]Config backup preserved. Delete manually when confirmed working.[/dim]"
            )
    else:
        console.print(f"\n[red]✗ {message}[/red]")
        raise typer.Exit(1)


@app.command()
def rollback(
    repo_path: Path = typer.Argument(
        Path("."),
        help="Project root directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    steps: int = typer.Option(
        1,
        "--steps",
        "-s",
        help="Number of schema versions to rollback",
        min=1,
    ),
    from_backup: bool = typer.Option(
        True,
        "--from-backup/--no-backup",
        help="Restore from backup if available (default: enabled)",
    ),
) -> None:
    """
    Rollback previous schema migration(s).

    Restores config.yml from a backup (if available) or applies backward
    migrations to undo schema changes.

    Examples:
        tac-bootstrap rollback                      # Rollback 1 step
        tac-bootstrap rollback . --steps 2          # Rollback 2 steps
        tac-bootstrap rollback . --no-backup        # Use backward migrations only
    """
    project_path = repo_path.resolve()

    # Verify config.yml exists
    config_file = project_path / "config.yml"
    if not config_file.exists():
        console.print("[red]Error: No config.yml found. Is this a TAC Bootstrap project?[/red]")
        raise typer.Exit(1)

    service = MigrationService(project_path)
    current_version = service.detect_current_version()

    console.print("\n[bold]TAC Bootstrap Schema Rollback[/bold]")
    console.print(f"  Current schema version: [yellow]{current_version}[/yellow]")
    console.print(f"  Steps to rollback: [cyan]{steps}[/cyan]")
    console.print(f"  From backup: [cyan]{from_backup}[/cyan]")

    # Perform rollback
    console.print("\n[bold]Rolling back...[/bold]")
    success, message = service.rollback_migration(steps=steps, from_backup=from_backup)

    if success:
        console.print(f"\n[green]✓ {message}[/green]")
    else:
        console.print(f"\n[red]✗ {message}[/red]")
        raise typer.Exit(1)


@app.command()
def health_check(
    repo_path: Path = typer.Argument(
        Path("."), help="Project root (default: current directory)"
    ),
) -> None:
    """
    Check system health and requirements.

    Validates that all required system dependencies are installed and meet
    minimum version requirements for TAC Bootstrap project generation.

    Checks:
    - git >= 2.30
    - python >= 3.10
    - Package manager (uv, npm, yarn, pnpm, bun)
    - gh CLI (if orchestrator is enabled)

    Examples:
        # Check current directory
        $ tac-bootstrap health-check

        # Check specific project
        $ tac-bootstrap health-check /path/to/repo
    """
    try:
        repo_path = repo_path.resolve()
        console.print(f"[cyan]Checking system health for:[/cyan] {repo_path}\n")

        # Try to load config from repo if available
        config_file = repo_path / "config.yml"
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    raw_config = yaml.safe_load(f)
                config = TACConfig(**raw_config)
                console.print(f"[dim]Loaded config from {config_file}[/dim]\n")
            except Exception:
                # Fall back to minimal config for system checks
                config = TACConfig(
                    project=ProjectSpec(
                        name="health-check",
                        language=Language.PYTHON,
                        package_manager=PackageManager.UV,
                    ),
                    commands=CommandsSpec(start="", test=""),
                    claude=ClaudeConfig(settings=ClaudeSettings(project_name="health-check")),
                )
        else:
            config = TACConfig(
                project=ProjectSpec(
                    name="health-check",
                    language=Language.PYTHON,
                    package_manager=PackageManager.UV,
                ),
                commands=CommandsSpec(start="", test=""),
                claude=ClaudeConfig(settings=ClaudeSettings(project_name="health-check")),
            )

        template_repo = TemplateRepository()
        vs = ValidationService(template_repo)
        result = vs.validate_system_requirements(config)

        # Build results table
        table = Table(title="System Requirements", border_style="cyan")
        table.add_column("Tool", style="bold")
        table.add_column("Required")
        table.add_column("Status")

        checks_info = [("git", ">= 2.30"), ("python", ">= 3.10")]
        if config.project.package_manager == PackageManager.UV:
            checks_info.append(("uv", "any"))
        if config.project.package_manager in ValidationService.JS_PACKAGE_MANAGERS:
            checks_info.append((config.project.package_manager.value, "any"))
        if config.orchestrator.enabled:
            checks_info.append(("gh", "any"))

        for tool_name, required_ver in checks_info:
            tool_issues = [
                i for i in result.issues if tool_name in i.message.lower()
            ]
            if tool_issues:
                issue = tool_issues[0]
                if issue.severity == "error":
                    table.add_row(tool_name, required_ver, "[red]FAIL[/red]")
                else:
                    table.add_row(tool_name, required_ver, "[yellow]WARN[/yellow]")
            else:
                table.add_row(tool_name, required_ver, "[green]OK[/green]")

        console.print(table)
        console.print()

        if result.valid:
            console.print(
                Panel(
                    "[bold green]All system requirements met![/bold green]",
                    border_style="green",
                    title="Health Check",
                )
            )
        else:
            error_count = len(result.errors())
            warning_count = len(result.warnings())
            status_lines = f"[bold red]Issues found[/bold red]\n\n"
            status_lines += f"[red]Errors:[/red] {error_count}\n"
            status_lines += f"[yellow]Warnings:[/yellow] {warning_count}\n"
            for issue in result.issues:
                color = "red" if issue.severity == "error" else "yellow"
                status_lines += (
                    f"\n[{color}][{issue.severity.upper()}][/{color}] {issue.message}"
                )
                if issue.suggestion:
                    status_lines += f"\n  [dim]{issue.suggestion}[/dim]"

            console.print(
                Panel(status_lines, border_style="red", title="Health Check")
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def validate(
    repo_path: Path = typer.Argument(
        Path("."), help="Project root (default: current directory)"
    ),
    strict: bool = typer.Option(
        False, "--strict", help="Run strict validation (all warnings become errors)"
    ),
) -> None:
    """
    Validate project configuration and requirements.

    Runs comprehensive validation including system requirements, project name,
    project path, config compatibility, filesystem, and git checks.

    Examples:
        # Validate current directory
        $ tac-bootstrap validate

        # Validate specific project
        $ tac-bootstrap validate /path/to/repo

        # Strict mode (warnings become errors)
        $ tac-bootstrap validate --strict
    """
    try:
        repo_path = repo_path.resolve()
        console.print(f"[cyan]Validating:[/cyan] {repo_path}\n")

        # Load config
        config_file = repo_path / "config.yml"
        if not config_file.exists():
            console.print(
                f"[red]Error:[/red] No config.yml found at {repo_path}"
            )
            console.print(
                "[dim]Run 'tac-bootstrap init' to create a new project "
                "or 'tac-bootstrap add-agentic' to add to existing repo[/dim]"
            )
            raise typer.Exit(1)

        try:
            with open(config_file, "r") as f:
                raw_config = yaml.safe_load(f)
            config = TACConfig(**raw_config)
        except yaml.YAMLError as e:
            console.print(f"[red]YAML Parse Error:[/red] {e}")
            raise typer.Exit(1)
        except Exception as e:
            console.print(f"[red]Config Validation Error:[/red] {e}")
            raise typer.Exit(1)

        if strict:
            config = config.model_copy(update={"validation_mode": "strict"})

        template_repo = TemplateRepository()
        vs = ValidationService(template_repo)
        result = vs.run_preflight_checks(config, repo_path)

        level_order = [
            ValidationLevel.SYSTEM,
            ValidationLevel.DOMAIN,
            ValidationLevel.TEMPLATE,
            ValidationLevel.FILESYSTEM,
            ValidationLevel.GIT,
        ]

        has_issues = False
        for level in level_order:
            level_issues = [i for i in result.issues if i.level == level]
            if not level_issues:
                continue
            has_issues = True
            console.print(f"\n[bold]{level.value.upper()} Checks:[/bold]")
            for issue in level_issues:
                if issue.severity == "error":
                    color = "red"
                    icon = "x"
                else:
                    color = "yellow"
                    icon = "!"
                console.print(f"  [{color}][{icon}][/{color}] {issue.message}")
                if issue.suggestion:
                    console.print(f"      [dim]{issue.suggestion}[/dim]")

        console.print()

        if result.valid and not has_issues:
            console.print(
                Panel(
                    "[bold green]All validations passed![/bold green]\n\n"
                    f"Project '{config.project.name}' is ready for scaffolding.",
                    border_style="green",
                    title="Validation Result",
                )
            )
        elif result.valid:
            warning_count = len(result.warnings())
            console.print(
                Panel(
                    f"[bold green]Validation passed with {warning_count} "
                    f"warning(s)[/bold green]\n\n"
                    f"Project '{config.project.name}' can proceed, "
                    "but consider addressing the warnings above.",
                    border_style="yellow",
                    title="Validation Result",
                )
            )
        else:
            error_count = len(result.errors())
            warning_count = len(result.warnings())
            console.print(
                Panel(
                    f"[bold red]Validation failed[/bold red]\n\n"
                    f"[red]Errors:[/red] {error_count}\n"
                    f"[yellow]Warnings:[/yellow] {warning_count}\n\n"
                    "Fix the errors above before proceeding.",
                    border_style="red",
                    title="Validation Result",
                )
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def telemetry(
    action: str = typer.Argument(
        ...,
        help="Action to perform: enable, disable, status, or clear",
    ),
) -> None:
    """
    Manage CLI telemetry settings.

    TAC Bootstrap includes opt-in anonymous usage tracking to help improve
    the tool. Telemetry is DISABLED by default and never collects sensitive
    data (file paths, project names, credentials, or exception messages).

    Examples:
        $ tac-bootstrap telemetry enable    # Turn on tracking
        $ tac-bootstrap telemetry disable   # Turn off tracking
        $ tac-bootstrap telemetry status    # Show current status and stats
        $ tac-bootstrap telemetry clear     # Delete all collected data
    """
    from tac_bootstrap.infrastructure.telemetry import TelemetryService

    service = TelemetryService()

    if action == "enable":
        service.opt_in()
        console.print(
            Panel(
                "[bold green]Telemetry enabled[/bold green]\n\n"
                "Anonymous usage data will be collected locally.\n"
                "No sensitive data (paths, credentials, etc.) is ever tracked.\n"
                f"Data stored at: [dim]{service.storage_dir}[/dim]",
                border_style="green",
                title="Telemetry",
            )
        )

    elif action == "disable":
        service.opt_out()
        console.print(
            Panel(
                "[bold yellow]Telemetry disabled[/bold yellow]\n\n"
                "No data will be collected.\n"
                "Use [cyan]tac-bootstrap telemetry clear[/cyan] to delete existing data.",
                border_style="yellow",
                title="Telemetry",
            )
        )

    elif action == "status":
        stats = service.get_statistics()
        if not stats.get("enabled", False):
            status_text = (
                "[bold]Status:[/bold] [yellow]Disabled[/yellow]\n\n"
                "Telemetry is currently disabled.\n"
                "Use [cyan]tac-bootstrap telemetry enable[/cyan] to opt in."
            )
        else:
            status_text = (
                f"[bold]Status:[/bold] [green]Enabled[/green]\n\n"
                f"[cyan]Total Events:[/cyan] {stats.get('total_events', 0)}\n"
                f"[cyan]Events Today:[/cyan] {stats.get('events_today', 0)}\n"
                f"[cyan]Log Files:[/cyan] {stats.get('log_files', 0)}\n"
                f"[cyan]Avg Duration:[/cyan] {stats.get('avg_duration_ms', 0):.1f} ms\n"
            )
            commands = stats.get("commands", {})
            if commands:
                status_text += "\n[bold]Command Usage:[/bold]\n"
                for cmd, count in sorted(
                    commands.items(), key=lambda x: x[1], reverse=True
                ):
                    status_text += f"  {cmd}: {count}\n"

            errors = stats.get("errors", {})
            if errors:
                status_text += "\n[bold]Error Types:[/bold]\n"
                for err, count in sorted(
                    errors.items(), key=lambda x: x[1], reverse=True
                ):
                    status_text += f"  {err}: {count}\n"

            status_text += f"\n[dim]Data location: {service.storage_dir}[/dim]"

        console.print(Panel(status_text, border_style="cyan", title="Telemetry Status"))

    elif action == "clear":
        files_deleted = service.clear_data()
        console.print(
            Panel(
                f"[bold green]Telemetry data cleared[/bold green]\n\n"
                f"Deleted {files_deleted} file(s) from {service.storage_dir}",
                border_style="green",
                title="Telemetry",
            )
        )

    else:
        console.print(
            f"[red]Error:[/red] Unknown action '{action}'. "
            "Use: enable, disable, status, or clear"
        )
        raise typer.Exit(1)


# ============================================================================
# PLUGIN COMMANDS
# ============================================================================


@app.command()
def plugin(
    action: str = typer.Argument(
        ...,
        help="Action: list, info <name>, enable <name>, disable <name>",
    ),
    name: Optional[str] = typer.Argument(None, help="Plugin name (for info/enable/disable)"),
    plugins_dir: Optional[Path] = typer.Option(
        None, "--plugins-dir", help="Custom plugins directory"
    ),
) -> None:
    """
    Manage TAC Bootstrap plugins.

    Plugins extend TAC Bootstrap with custom hooks that execute
    during project generation lifecycle events.

    Examples:
        $ tac-bootstrap plugin list
        $ tac-bootstrap plugin info example-plugin
        $ tac-bootstrap plugin enable example-plugin
        $ tac-bootstrap plugin disable example-plugin
    """
    try:
        from tac_bootstrap.application.plugin_service import PluginService

        service = PluginService()

        # Determine plugins directory
        pdir = plugins_dir or Path.cwd() / "plugins"
        if pdir.is_dir():
            service.load_plugins(pdir)

        if action == "list":
            plugins = service.list_plugins()
            if not plugins:
                console.print("[yellow]No plugins found.[/yellow]")
                console.print(f"[dim]Looking in: {pdir}[/dim]")
                return

            table = Table(title="Installed Plugins", border_style="cyan")
            table.add_column("Name", style="bold")
            table.add_column("Version")
            table.add_column("Author")
            table.add_column("Status")
            table.add_column("Hooks")

            for p in plugins:
                status = "[green]Enabled[/green]" if p.enabled else "[red]Disabled[/red]"
                hooks_str = ", ".join(p.hooks.keys()) if p.hooks else "-"
                table.add_row(p.name, p.version, p.author, status, hooks_str)

            console.print(table)
            console.print(f"\n[dim]Total: {service.plugin_count} plugin(s), "
                          f"{service.enabled_count} enabled[/dim]")

        elif action == "info":
            if not name:
                console.print("[red]Error:[/red] Plugin name required for 'info'")
                raise typer.Exit(1)
            p = service.get_plugin(name)
            if p is None:
                console.print(f"[red]Plugin '{name}' not found[/red]")
                raise typer.Exit(1)
            info = f"""[bold]{p.name}[/bold] v{p.version}
[cyan]Author:[/cyan] {p.author}
[cyan]Description:[/cyan] {p.description}
[cyan]Status:[/cyan] {"Enabled" if p.enabled else "Disabled"}
[cyan]Hooks:[/cyan] {', '.join(p.hooks.keys()) if p.hooks else 'None'}"""
            if p.load_error:
                info += f"\n[red]Error:[/red] {p.load_error}"
            console.print(Panel(info, border_style="cyan", title="Plugin Info"))

        elif action == "enable":
            if not name:
                console.print("[red]Error:[/red] Plugin name required")
                raise typer.Exit(1)
            if service.enable_plugin(name):
                console.print(f"[green]Plugin '{name}' enabled[/green]")
            else:
                console.print(f"[red]Plugin '{name}' not found[/red]")
                raise typer.Exit(1)

        elif action == "disable":
            if not name:
                console.print("[red]Error:[/red] Plugin name required")
                raise typer.Exit(1)
            if service.disable_plugin(name):
                console.print(f"[yellow]Plugin '{name}' disabled[/yellow]")
            else:
                console.print(f"[red]Plugin '{name}' not found[/red]")
                raise typer.Exit(1)

        else:
            console.print(
                f"[red]Error:[/red] Unknown action '{action}'. "
                "Use: list, info, enable, or disable"
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# TEMPLATE STORE COMMANDS
# ============================================================================


@app.command()
def template(
    action: str = typer.Argument(
        ...,
        help="Action: search, install, list, rate, info",
    ),
    query: Optional[str] = typer.Argument(None, help="Search query or template ID"),
    rating: Optional[int] = typer.Option(None, "--rating", "-r", help="Rating (1-5)"),
    installed_only: bool = typer.Option(
        False, "--installed", help="Show only installed templates"
    ),
) -> None:
    """
    Manage the template store (search, install, rate templates).

    The template store provides reusable project templates that can be
    searched, installed, and rated.

    Examples:
        $ tac-bootstrap template search "fastapi auth"
        $ tac-bootstrap template install tac/fastapi-starter
        $ tac-bootstrap template list --installed
        $ tac-bootstrap template rate tac/fastapi-starter --rating 5
        $ tac-bootstrap template info tac/fastapi-starter
    """
    try:
        from tac_bootstrap.application.template_store_service import TemplateStoreService

        service = TemplateStoreService()

        # Ensure defaults are seeded
        if service.template_count == 0:
            service.seed_defaults()

        if action == "search":
            search_query = query or ""
            results = service.search_templates(search_query)

            if not results:
                console.print(f"[yellow]No templates found for '{search_query}'[/yellow]")
                return

            table = Table(title=f"Templates matching '{search_query}'", border_style="cyan")
            table.add_column("ID", style="bold")
            table.add_column("Name")
            table.add_column("Version")
            table.add_column("Rating")
            table.add_column("Downloads")
            table.add_column("Tags")

            for t in results:
                rating_str = f"{t['rating']:.1f}" if t['rating'] > 0 else "-"
                tags_str = ", ".join(t.get("tags", [])[:3])
                table.add_row(
                    t["id"], t["name"], t["version"],
                    rating_str, str(t["downloads"]), tags_str,
                )

            console.print(table)

        elif action == "install":
            if not query:
                console.print("[red]Error:[/red] Template ID required")
                raise typer.Exit(1)
            result = service.install_template(query)
            if result["success"]:
                console.print(f"[green]{result['message']}[/green]")
            else:
                console.print(f"[red]{result['message']}[/red]")
                raise typer.Exit(1)

        elif action == "list":
            if installed_only:
                templates = service.list_installed_templates()
                title = "Installed Templates"
            else:
                templates = service.list_all_templates()
                title = "All Templates"

            if not templates:
                console.print("[yellow]No templates found[/yellow]")
                return

            table = Table(title=title, border_style="cyan")
            table.add_column("ID", style="bold")
            table.add_column("Name")
            table.add_column("Version")
            table.add_column("Installed")

            for t in templates:
                installed_str = "[green]Yes[/green]" if t["installed"] else "[dim]No[/dim]"
                table.add_row(t["id"], t["name"], t["version"], installed_str)

            console.print(table)
            console.print(f"\n[dim]Total: {len(templates)} template(s)[/dim]")

        elif action == "rate":
            if not query:
                console.print("[red]Error:[/red] Template ID required")
                raise typer.Exit(1)
            if rating is None:
                console.print("[red]Error:[/red] --rating value required (1-5)")
                raise typer.Exit(1)
            result = service.rate_template(query, rating)
            if result["success"]:
                console.print(f"[green]{result['message']}[/green]")
            else:
                console.print(f"[red]{result['message']}[/red]")
                raise typer.Exit(1)

        elif action == "info":
            if not query:
                console.print("[red]Error:[/red] Template ID required")
                raise typer.Exit(1)
            info = service.get_template_info(query)
            if info is None:
                console.print(f"[red]Template '{query}' not found[/red]")
                raise typer.Exit(1)
            rating_str = f"{info['rating']:.1f}" if info['rating'] > 0 else "Not rated"
            info_text = f"""[bold]{info['name']}[/bold] ({info['id']})
[cyan]Version:[/cyan] {info['version']}
[cyan]Author:[/cyan] {info['author']}
[cyan]Description:[/cyan] {info['description']}
[cyan]Rating:[/cyan] {rating_str} ({info['rating_count']} ratings)
[cyan]Downloads:[/cyan] {info['downloads']}
[cyan]Tags:[/cyan] {', '.join(info.get('tags', []))}
[cyan]Installed:[/cyan] {'Yes' if info['installed'] else 'No'}"""
            console.print(Panel(info_text, border_style="cyan", title="Template Info"))

        else:
            console.print(
                f"[red]Error:[/red] Unknown action '{action}'. "
                "Use: search, install, list, rate, or info"
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# SECURITY COMMANDS
# ============================================================================


@app.command()
def security(
    action: str = typer.Argument(
        ...,
        help="Action: audit, scan-templates, report",
    ),
    repo_path: Path = typer.Argument(
        Path("."), help="Project path (default: current directory)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for report"
    ),
) -> None:
    """
    Security scanning and auditing tools.

    Scans project files for security issues including hardcoded secrets,
    SQL injection, XSS vulnerabilities, and OWASP Top 10 compliance.

    Examples:
        $ tac-bootstrap security audit
        $ tac-bootstrap security scan-templates
        $ tac-bootstrap security report --output security-report.txt
    """
    try:
        from tac_bootstrap.application.security_service import SecurityService

        service = SecurityService()
        target_path = repo_path.resolve()

        if action == "audit":
            console.print(f"[cyan]Running security audit on:[/cyan] {target_path}\n")

            report = service.generate_security_report(target_path)

            console.print(f"[dim]Files scanned: {report.total_files_scanned}[/dim]")

            if not report.has_issues:
                console.print(
                    Panel(
                        "[bold green]No security issues found![/bold green]",
                        border_style="green",
                        title="Security Audit",
                    )
                )
                return

            # Show issues
            for issue in report.issues:
                severity = issue.severity.value.upper()
                if issue.severity.value in ("critical", "high"):
                    color = "red"
                elif issue.severity.value == "medium":
                    color = "yellow"
                else:
                    color = "blue"

                console.print(f"  [{color}][{severity}][/{color}] {issue.message}")
                if issue.file_path:
                    console.print(f"    [dim]File: {issue.file_path}:{issue.line_number}[/dim]")
                if issue.suggestion:
                    console.print(f"    [dim]Fix: {issue.suggestion}[/dim]")

            report.compute_summary()
            console.print(
                f"\n[bold]Summary:[/bold] {report.total_issues} issue(s) found"
            )
            for sev, count in sorted(report.summary.items()):
                console.print(f"  {sev.upper()}: {count}")

        elif action == "scan-templates":
            console.print(f"[cyan]Scanning templates for vulnerabilities:[/cyan] {target_path}\n")

            issues = service.scan_templates(target_path)

            if not issues:
                console.print("[green]No template vulnerabilities found[/green]")
                return

            for issue in issues:
                severity = issue.severity.value.upper()
                console.print(f"  [{severity}] {issue.message}")
                if issue.file_path:
                    console.print(f"    File: {issue.file_path}:{issue.line_number}")
                if issue.suggestion:
                    console.print(f"    Fix: {issue.suggestion}")

            console.print(f"\n[bold]Total: {len(issues)} vulnerability(ies) found[/bold]")

        elif action == "report":
            console.print(f"[cyan]Generating security report for:[/cyan] {target_path}\n")

            report = service.generate_security_report(target_path)
            text = service.format_report_text(report)

            if output:
                output.write_text(text, encoding="utf-8")
                console.print(f"[green]Report written to {output}[/green]")
            else:
                console.print(text)

        else:
            console.print(
                f"[red]Error:[/red] Unknown action '{action}'. "
                "Use: audit, scan-templates, or report"
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# DOCS COMMANDS
# ============================================================================


@app.command()
def docs(
    action: str = typer.Argument(
        ...,
        help="Action: generate, serve, new-adr",
    ),
    repo_path: Path = typer.Argument(
        Path("."), help="Project path (default: current directory)"
    ),
    with_diagrams: bool = typer.Option(
        True, "--with-diagrams/--no-diagrams", help="Include Mermaid diagrams"
    ),
    port: int = typer.Option(3000, "--port", "-p", help="Port for docs server"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="ADR title"),
) -> None:
    """
    Generate and manage project documentation.

    Auto-generates API docs, architecture docs, ADRs, and Mermaid diagrams.

    Examples:
        $ tac-bootstrap docs generate
        $ tac-bootstrap docs generate --with-diagrams
        $ tac-bootstrap docs serve --port 3000
        $ tac-bootstrap docs new-adr --title "Use PostgreSQL"
    """
    try:
        from tac_bootstrap.application.docs_generator import DocsGenerator

        target_path = repo_path.resolve()

        # Try to load project config
        config = None
        config_file = target_path / "config.yml"
        project_name = target_path.name
        language = "python"
        framework = "none"
        architecture = "simple"

        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    raw_config = yaml.safe_load(f)
                from tac_bootstrap.domain.models import TACConfig
                config = TACConfig(**raw_config)
                project_name = config.project.name
                language = config.project.language.value
                framework = config.project.framework.value
                architecture = config.project.architecture.value
            except Exception:
                pass

        generator = DocsGenerator(
            project_name=project_name,
            language=language,
            framework=framework,
            architecture=architecture,
            config=config,
        )

        if action == "generate":
            console.print(f"[cyan]Generating documentation for:[/cyan] {target_path}\n")

            files = generator.generate_all(
                target_path,
                force=force,
                with_diagrams=with_diagrams,
            )

            if not files:
                console.print(
                    "[yellow]No new files generated (all exist already). "
                    "Use --force to overwrite.[/yellow]"
                )
                return

            console.print(f"[green]Generated {len(files)} documentation file(s):[/green]")
            for f in files:
                console.print(f"  {f.relative_to(target_path)}")

        elif action == "serve":
            docs_dir = target_path / "docs"
            if not docs_dir.is_dir():
                console.print("[yellow]No docs/ directory found. Run 'docs generate' first.[/yellow]")
                raise typer.Exit(1)
            generator.serve_docs(docs_dir, port=port)

        elif action == "new-adr":
            if not title:
                console.print("[red]Error:[/red] --title is required for new-adr")
                raise typer.Exit(1)

            docs_dir = target_path / "docs"
            adr_dir = docs_dir / "adr"
            adr_dir.mkdir(parents=True, exist_ok=True)

            number = generator.get_next_adr_number(docs_dir)
            content = generator.generate_adr(
                decision=title,
                context="(Add context here)",
                consequence="(Add consequences here)",
                number=number,
            )

            # Generate filename from title
            slug = title.lower().replace(" ", "-")[:50]
            filename = f"{number:04d}-{slug}.md"
            adr_path = adr_dir / filename
            adr_path.write_text(content, encoding="utf-8")

            console.print(f"[green]Created ADR:[/green] {adr_path.relative_to(target_path)}")

        else:
            console.print(
                f"[red]Error:[/red] Unknown action '{action}'. "
                "Use: generate, serve, or new-adr"
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# TEST GENERATION COMMANDS
# ============================================================================


@app.command(name="test-generate")
def test_generate(
    test_type: str = typer.Argument(
        ...,
        help="Test type: unit, integration, e2e, load, coverage, all",
    ),
    repo_path: Path = typer.Argument(
        Path("."), help="Project path (default: current directory)"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing files"),
) -> None:
    """
    Generate test scaffolding for your project.

    Creates test templates for various testing types including unit,
    integration, E2E, load testing, and coverage configuration.

    Examples:
        $ tac-bootstrap test-generate unit
        $ tac-bootstrap test-generate integration
        $ tac-bootstrap test-generate e2e
        $ tac-bootstrap test-generate load
        $ tac-bootstrap test-generate coverage
        $ tac-bootstrap test-generate all
    """
    try:
        from tac_bootstrap.application.test_generator import TestGenerator

        target_path = repo_path.resolve()

        # Try to load project config
        project_name = target_path.name
        language = "python"
        framework = "none"
        config = None

        config_file = target_path / "config.yml"
        if config_file.exists():
            try:
                with open(config_file, "r") as f:
                    raw_config = yaml.safe_load(f)
                from tac_bootstrap.domain.models import TACConfig
                config = TACConfig(**raw_config)
                project_name = config.project.name
                language = config.project.language.value
                framework = config.project.framework.value
            except Exception:
                pass

        generator = TestGenerator(
            project_name=project_name,
            language=language,
            framework=framework,
            config=config,
        )

        if test_type == "unit":
            content = generator.generate_unit_tests(
                module_path=Path("app"),
                output_dir=target_path / "tests" / "unit",
                force=force,
            )
            console.print("[green]Unit test template generated[/green]")
            console.print(f"  tests/unit/test_app.py")

        elif test_type == "integration":
            generator.generate_integration_tests(
                project_path=target_path, force=force
            )
            console.print("[green]Integration test template generated[/green]")

        elif test_type == "e2e":
            generator.generate_e2e_tests(
                project_path=target_path, force=force
            )
            console.print("[green]E2E test template generated[/green]")

        elif test_type == "load":
            generator.generate_load_tests(
                project_path=target_path, force=force
            )
            console.print("[green]Load test template generated[/green]")

        elif test_type == "coverage":
            generator.setup_coverage_config(target_path, force=force)
            console.print("[green]Coverage configuration created[/green]")
            console.print("  .coveragerc")

        elif test_type == "all":
            files = generator.generate_all(target_path, force=force)
            console.print(f"[green]Generated {len(files)} test file(s):[/green]")
            for f in files:
                try:
                    console.print(f"  {f.relative_to(target_path)}")
                except ValueError:
                    console.print(f"  {f}")

        else:
            console.print(
                f"[red]Error:[/red] Unknown test type '{test_type}'. "
                "Use: unit, integration, e2e, load, coverage, or all"
            )
            raise typer.Exit(1)

    except SystemExit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


# ============================================================================
# PHASE 3: PREMIUM FEATURES & POLISH COMMANDS
# ============================================================================


# --- Feature 11: Config / Language Management ---

config_app = typer.Typer(
    name="config",
    help="Manage CLI configuration settings",
)
app.add_typer(config_app, name="config")


@config_app.command("set")
def config_set(
    key: str = typer.Argument(..., help="Configuration key (e.g., language)"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """
    Set a CLI configuration value.

    Examples:
        $ tac-bootstrap config set language es
        $ tac-bootstrap config set language zh
    """
    supported_keys = {"language"}
    if key not in supported_keys:
        console.print(
            f"[red]Error:[/red] Unknown configuration key '{key}'. "
            f"Supported keys: {', '.join(supported_keys)}"
        )
        raise typer.Exit(1)

    if key == "language":
        from tac_bootstrap.infrastructure.i18n import I18nService, SUPPORTED_LANGUAGES

        i18n = I18nService()
        if value not in SUPPORTED_LANGUAGES:
            console.print(
                f"[red]Error:[/red] Unsupported language '{value}'. "
                f"Supported: {', '.join(SUPPORTED_LANGUAGES.keys())}"
            )
            raise typer.Exit(1)
        i18n.set_language(value)
        lang_name = SUPPORTED_LANGUAGES[value]
        console.print(
            Panel(
                f"[bold green]Language set to {lang_name} ({value})[/bold green]",
                border_style="green",
                title="Configuration",
            )
        )


@config_app.command("get")
def config_get(
    key: str = typer.Argument(..., help="Configuration key to retrieve"),
) -> None:
    """
    Get a CLI configuration value.

    Examples:
        $ tac-bootstrap config get language
    """
    if key == "language":
        from tac_bootstrap.infrastructure.i18n import I18nService

        i18n = I18nService()
        console.print(
            f"[cyan]language[/cyan] = [green]{i18n.current_language}[/green] "
            f"({i18n.current_language_name})"
        )
    else:
        console.print(f"[red]Error:[/red] Unknown configuration key '{key}'")
        raise typer.Exit(1)


@config_app.command("list")
def config_list() -> None:
    """
    List all CLI configuration values.

    Examples:
        $ tac-bootstrap config list
    """
    from tac_bootstrap.infrastructure.i18n import I18nService

    i18n = I18nService()

    table = Table(title="CLI Configuration", border_style="cyan")
    table.add_column("Key", style="bold")
    table.add_column("Value", style="green")
    table.add_column("Description")

    table.add_row(
        "language",
        f"{i18n.current_language} ({i18n.current_language_name})",
        "CLI output language",
    )

    console.print(table)


# --- Feature 12: Dashboard ---

dashboard_app = typer.Typer(
    name="dashboard",
    help="Web dashboard for project management",
)
app.add_typer(dashboard_app, name="dashboard")


@dashboard_app.command("start")
def dashboard_start(
    port: int = typer.Option(3000, "--port", "-p", help="Dashboard port (default: 3000)"),
    host: str = typer.Option(
        "127.0.0.1", "--host", help="Dashboard host (default: 127.0.0.1)"
    ),
) -> None:
    """
    Start the web dashboard.

    Examples:
        $ tac-bootstrap dashboard start
        $ tac-bootstrap dashboard start --port 8080
    """
    try:
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        server = DashboardServer(host=host, port=port)
        result = server.start()

        if result["status"] == "already_running":
            console.print(
                Panel(
                    f"[yellow]Dashboard is already running[/yellow]\n\n"
                    f"[cyan]URL:[/cyan] {result['url']}\n"
                    f"[cyan]PID:[/cyan] {result['pid']}",
                    border_style="yellow",
                    title="Dashboard",
                )
            )
        else:
            console.print(
                Panel(
                    f"[bold green]Dashboard started successfully[/bold green]\n\n"
                    f"[cyan]URL:[/cyan] {result['url']}\n"
                    f"[cyan]PID:[/cyan] {result['pid']}\n\n"
                    f"Open [bold]{result['url']}[/bold] in your browser.",
                    border_style="green",
                    title="Dashboard",
                )
            )
    except Exception as e:
        console.print(f"[red]Error starting dashboard:[/red] {e}")
        raise typer.Exit(1)


@dashboard_app.command("stop")
def dashboard_stop() -> None:
    """
    Stop the web dashboard.

    Examples:
        $ tac-bootstrap dashboard stop
    """
    try:
        from tac_bootstrap.infrastructure.web_server import DashboardServer

        server = DashboardServer()
        result = server.stop()

        if result["status"] == "not_running":
            console.print("[yellow]Dashboard is not running[/yellow]")
        elif result["status"] == "stopped":
            console.print(
                Panel(
                    f"[bold green]Dashboard stopped[/bold green]\n"
                    f"PID {result['pid']} terminated.",
                    border_style="green",
                    title="Dashboard",
                )
            )
        else:
            console.print(f"[red]Error:[/red] {result.get('message', 'Unknown error')}")
            raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@dashboard_app.command("status")
def dashboard_status() -> None:
    """
    Show dashboard status.

    Examples:
        $ tac-bootstrap dashboard status
    """
    from tac_bootstrap.infrastructure.web_server import DashboardServer

    server = DashboardServer()
    status_info = server.get_status()

    if status_info["running"]:
        console.print(
            Panel(
                f"[bold green]Dashboard is running[/bold green]\n\n"
                f"[cyan]URL:[/cyan] {status_info['url']}\n"
                f"[cyan]PID:[/cyan] {status_info.get('pid', 'unknown')}\n"
                f"[cyan]Port:[/cyan] {status_info['port']}",
                border_style="green",
                title="Dashboard Status",
            )
        )
    else:
        console.print(
            Panel(
                "[yellow]Dashboard is not running[/yellow]\n\n"
                "Start with: [cyan]tac-bootstrap dashboard start[/cyan]",
                border_style="yellow",
                title="Dashboard Status",
            )
        )


# --- Feature 13: Search ---

search_app = typer.Typer(
    name="search",
    help="Search commands, templates, and features",
)
app.add_typer(search_app, name="search")


@search_app.command("commands")
def search_commands_cmd(
    query: str = typer.Argument("", help="Search query"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    model: Optional[str] = typer.Option(None, "--model", "-m", help="Filter by model"),
) -> None:
    """
    Search available commands and workflows.

    Examples:
        $ tac-bootstrap search commands "testing"
        $ tac-bootstrap search commands --tag "testing" --model "opus"
    """
    from tac_bootstrap.application.search_service import SearchService

    service = SearchService()
    results = service.search_commands(query=query, tag=tag, model=model)

    if results.total == 0:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    table = Table(title=f"Search Results ({results.total})", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("Tags", style="dim")

    for r in results.results:
        table.add_row(r.name, r.category, r.description, ", ".join(r.tags[:3]))

    console.print(table)


@search_app.command("templates")
def search_templates_cmd(
    query: str = typer.Argument("", help="Search query"),
    framework: Optional[str] = typer.Option(
        None, "--framework", "-f", help="Filter by framework"
    ),
    arch: Optional[str] = typer.Option(
        None, "--arch", "-a", help="Filter by architecture"
    ),
) -> None:
    """
    Search available templates.

    Examples:
        $ tac-bootstrap search templates --framework fastapi --arch ddd
    """
    from tac_bootstrap.application.search_service import SearchService

    service = SearchService()
    results = service.search_templates(query=query, framework=framework, architecture=arch)

    if results.total == 0:
        console.print("[yellow]No matching templates found[/yellow]")
        return

    table = Table(title=f"Templates ({results.total})", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Description")
    table.add_column("Tags", style="dim")

    for r in results.results:
        table.add_row(r.name, r.description, ", ".join(r.tags[:4]))

    console.print(table)


@search_app.command("features")
def search_features_cmd(
    query: str = typer.Argument("", help="Search query"),
    tier: Optional[str] = typer.Option(
        None, "--tier", help="Filter by tier (core, optional, premium)"
    ),
) -> None:
    """
    Search available features.

    Examples:
        $ tac-bootstrap search features "performance" --tier premium
    """
    from tac_bootstrap.application.search_service import SearchService

    service = SearchService()
    results = service.search_features(query=query, tier=tier)

    if results.total == 0:
        console.print("[yellow]No matching features found[/yellow]")
        return

    table = Table(title=f"Features ({results.total})", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Tier")
    table.add_column("Description")
    table.add_column("Status")

    for r in results.results:
        tier_val = r.metadata.get("tier", "")
        status_val = r.metadata.get("status", "")
        table.add_row(r.name, tier_val, r.description, status_val)

    console.print(table)


# --- Feature 14: Snapshots ---

snapshot_app = typer.Typer(
    name="snapshot",
    help="Manage project snapshots",
)
app.add_typer(snapshot_app, name="snapshot")


@snapshot_app.command("create")
def snapshot_create(
    name: str = typer.Argument(..., help="Snapshot name"),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path (default: current directory)"
    ),
    description: str = typer.Option("", "--desc", "-d", help="Snapshot description"),
) -> None:
    """
    Create a named snapshot of the project.

    Examples:
        $ tac-bootstrap snapshot create "initial-setup"
    """
    try:
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService()
        metadata = service.create_snapshot(project_path.resolve(), name, description)

        console.print(
            Panel(
                f"[bold green]Snapshot '{name}' created successfully[/bold green]\n\n"
                f"[cyan]Files:[/cyan] {metadata.file_count}\n"
                f"[cyan]Size:[/cyan] {metadata.total_size_bytes:,} bytes\n"
                f"[cyan]Created:[/cyan] {metadata.created_at}",
                border_style="green",
                title="Snapshot Created",
            )
        )
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error creating snapshot:[/red] {e}")
        raise typer.Exit(1)


@snapshot_app.command("list")
def snapshot_list(
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path (default: current directory)"
    ),
) -> None:
    """
    List all snapshots for a project.

    Examples:
        $ tac-bootstrap snapshot list
    """
    from tac_bootstrap.application.snapshot_service import SnapshotService

    service = SnapshotService()
    snapshots = service.list_snapshots(project_path.resolve())

    if not snapshots:
        console.print("[yellow]No snapshots found for this project[/yellow]")
        return

    table = Table(title=f"Project Snapshots ({len(snapshots)})", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Files")
    table.add_column("Size")
    table.add_column("Created")
    table.add_column("Description", style="dim")

    for snap in snapshots:
        size_str = f"{snap.total_size_bytes:,} B"
        if snap.total_size_bytes > 1_000_000:
            size_str = f"{snap.total_size_bytes / 1_000_000:.1f} MB"
        elif snap.total_size_bytes > 1_000:
            size_str = f"{snap.total_size_bytes / 1_000:.1f} KB"

        table.add_row(
            snap.name,
            str(snap.file_count),
            size_str,
            snap.created_at[:19],
            snap.description[:40] if snap.description else "",
        )

    console.print(table)


@snapshot_app.command("diff")
def snapshot_diff(
    name1: str = typer.Argument(..., help="First snapshot name (baseline)"),
    name2: str = typer.Argument(..., help="Second snapshot name (comparison)"),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Show differences between two snapshots.

    Examples:
        $ tac-bootstrap snapshot diff initial-setup after-changes
    """
    try:
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService()
        diff_result = service.diff_snapshots(name1, name2, project_path.resolve())

        summary = (
            f"[bold]Comparing:[/bold] {diff_result.snapshot1} -> {diff_result.snapshot2}\n\n"
            f"[green]Added:[/green] {len(diff_result.added)}\n"
            f"[red]Removed:[/red] {len(diff_result.removed)}\n"
            f"[yellow]Modified:[/yellow] {len(diff_result.modified)}\n"
            f"[dim]Unchanged:[/dim] {diff_result.unchanged}"
        )
        console.print(Panel(summary, border_style="cyan", title="Snapshot Diff"))

        if diff_result.added:
            console.print("\n[bold green]Added files:[/bold green]")
            for f in diff_result.added:
                console.print(f"  + {f}")

        if diff_result.removed:
            console.print("\n[bold red]Removed files:[/bold red]")
            for f in diff_result.removed:
                console.print(f"  - {f}")

        if diff_result.modified:
            console.print("\n[bold yellow]Modified files:[/bold yellow]")
            for f in diff_result.modified:
                console.print(f"  ~ {f}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@snapshot_app.command("restore")
def snapshot_restore(
    name: str = typer.Argument(..., help="Snapshot name to restore"),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Restore a project from a snapshot.

    Examples:
        $ tac-bootstrap snapshot restore initial-setup
    """
    try:
        from tac_bootstrap.application.snapshot_service import SnapshotService

        service = SnapshotService()

        if not typer.confirm(
            f"Restore snapshot '{name}'? A backup will be created first.", default=True
        ):
            console.print("[yellow]Restore cancelled[/yellow]")
            raise typer.Exit(0)

        result = service.restore_snapshot(name, project_path.resolve())

        console.print(
            Panel(
                f"[bold green]Snapshot '{name}' restored successfully[/bold green]\n\n"
                f"[cyan]Files Restored:[/cyan] {result['files_restored']}\n"
                f"[cyan]Backup Created:[/cyan] {result['backup_name']}",
                border_style="green",
                title="Restored",
            )
        )
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@snapshot_app.command("delete")
def snapshot_delete(
    name: str = typer.Argument(..., help="Snapshot name to delete"),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Delete a snapshot.

    Examples:
        $ tac-bootstrap snapshot delete old-snapshot
    """
    from tac_bootstrap.application.snapshot_service import SnapshotService

    service = SnapshotService()
    deleted = service.delete_snapshot(name, project_path.resolve())

    if deleted:
        console.print(f"[green]Snapshot '{name}' deleted[/green]")
    else:
        console.print(f"[yellow]Snapshot '{name}' not found[/yellow]")


# --- Feature 15: AI Generation ---

ai_app = typer.Typer(
    name="ai",
    help="AI-assisted code generation",
)
app.add_typer(ai_app, name="ai")


@ai_app.command("generate:endpoint")
def ai_generate_endpoint(
    path: str = typer.Option(..., "--path", help="URL path (e.g., /users)"),
    method: str = typer.Option("GET", "--method", "-m", help="HTTP method"),
    project_path: Path = typer.Option(
        Path("."), "--project", "-p", help="Project path"
    ),
) -> None:
    """
    Generate an API endpoint using AI.

    Examples:
        $ tac-bootstrap ai generate:endpoint --path /users --method GET
    """
    from tac_bootstrap.application.ai_generator import AIGeneratorService

    service = AIGeneratorService()
    if not service.is_configured:
        console.print(
            "[red]Error:[/red] Claude API key not configured. "
            "Set ANTHROPIC_API_KEY environment variable."
        )
        raise typer.Exit(1)

    console.print(f"[cyan]Generating {method} endpoint for {path}...[/cyan]")
    result = service.generate_endpoint(
        path=path, method=method, project_path=project_path
    )

    if result.success:
        console.print(
            Panel(
                f"[bold green]Endpoint generated[/bold green]\n\n"
                f"[cyan]Path:[/cyan] {path}\n"
                f"[cyan]Method:[/cyan] {method}\n"
                f"[cyan]File:[/cyan] {result.file_path}\n\n"
                f"[bold]Generated Code:[/bold]\n{result.code[:2000]}",
                border_style="green",
                title="AI Generation",
            )
        )
    else:
        console.print(f"[red]Error:[/red] {result.error}")
        raise typer.Exit(1)


@ai_app.command("generate:migration")
def ai_generate_migration(
    migration_type: str = typer.Option(
        "add-column", "--type", help="Migration type"
    ),
    name: str = typer.Option(..., "--name", help="Column/table name"),
    data_type: str = typer.Option("string", "--data-type", help="Data type"),
    project_path: Path = typer.Option(
        Path("."), "--project", "-p", help="Project path"
    ),
) -> None:
    """
    Generate a database migration using AI.

    Examples:
        $ tac-bootstrap ai generate:migration --type add-column --name email
    """
    from tac_bootstrap.application.ai_generator import AIGeneratorService

    service = AIGeneratorService()
    if not service.is_configured:
        console.print(
            "[red]Error:[/red] Claude API key not configured. "
            "Set ANTHROPIC_API_KEY environment variable."
        )
        raise typer.Exit(1)

    console.print(
        f"[cyan]Generating {migration_type} migration for '{name}'...[/cyan]"
    )
    result = service.generate_migration(
        migration_type=migration_type,
        name=name,
        data_type=data_type,
        project_path=project_path,
    )

    if result.success:
        console.print(
            Panel(
                f"[bold green]Migration generated[/bold green]\n\n"
                f"[bold]Generated Code:[/bold]\n{result.code[:2000]}",
                border_style="green",
                title="AI Generation",
            )
        )
    else:
        console.print(f"[red]Error:[/red] {result.error}")
        raise typer.Exit(1)


@ai_app.command("suggest:refactor")
def ai_suggest_refactor(
    file: Path = typer.Option(..., "--file", "-f", help="File to analyze"),
    project_path: Path = typer.Option(
        Path("."), "--project", "-p", help="Project path"
    ),
) -> None:
    """
    Get AI-powered refactoring suggestions.

    Examples:
        $ tac-bootstrap ai suggest:refactor --file src/app.py
    """
    from tac_bootstrap.application.ai_generator import AIGeneratorService

    service = AIGeneratorService()
    if not service.is_configured:
        console.print("[red]Error:[/red] Claude API key not configured.")
        raise typer.Exit(1)

    console.print(f"[cyan]Analyzing {file}...[/cyan]")
    suggestions = service.suggest_refactor(
        file_path=file, project_path=project_path
    )

    if not suggestions:
        console.print("[green]No refactoring suggestions - code looks good![/green]")
        return

    for i, suggestion in enumerate(suggestions, 1):
        color = (
            "red"
            if suggestion.severity == "critical"
            else ("yellow" if suggestion.severity == "warning" else "blue")
        )
        console.print(
            f"\n[{color}][{i}] [{suggestion.severity.upper()}] "
            f"{suggestion.category}[/{color}]"
        )
        console.print(f"  {suggestion.description}")
        if suggestion.reasoning:
            console.print(f"  [dim]Reason: {suggestion.reasoning}[/dim]")


@ai_app.command("suggest:tests")
def ai_suggest_tests(
    module: Path = typer.Option(
        ..., "--module", "-m", help="Module to generate tests for"
    ),
    project_path: Path = typer.Option(
        Path("."), "--project", "-p", help="Project path"
    ),
) -> None:
    """
    Get AI-generated test suggestions.

    Examples:
        $ tac-bootstrap ai suggest:tests --module src/domain/user.py
    """
    from tac_bootstrap.application.ai_generator import AIGeneratorService

    service = AIGeneratorService()
    if not service.is_configured:
        console.print("[red]Error:[/red] Claude API key not configured.")
        raise typer.Exit(1)

    console.print(f"[cyan]Generating test suggestions for {module}...[/cyan]")
    suggestions = service.suggest_tests(
        module_path=module, project_path=project_path
    )

    if not suggestions:
        console.print("[yellow]No test suggestions generated[/yellow]")
        return

    for i, test_suggestion in enumerate(suggestions, 1):
        console.print(
            Panel(
                f"[bold]{test_suggestion.test_name}[/bold]\n"
                f"[dim]{test_suggestion.description}[/dim]\n"
                f"[cyan]Type:[/cyan] {test_suggestion.test_type} | "
                f"[cyan]Priority:[/cyan] {test_suggestion.priority}\n\n"
                f"```python\n{test_suggestion.test_code[:1000]}\n```",
                border_style="cyan",
                title=f"Test Suggestion {i}",
            )
        )


# --- Feature 16: Learn ---

@app.command()
def learn(
    topic: Optional[str] = typer.Option(
        None, "--topic", "-t", help="Topic to learn about"
    ),
) -> None:
    """
    Interactive learning mode.

    Examples:
        $ tac-bootstrap learn --topic ddd
        $ tac-bootstrap learn --topic architecture
    """
    from tac_bootstrap.application.learning_service import LearningService

    service = LearningService()

    if topic:
        topic_content = service.get_topic(topic)
        if topic_content is None:
            console.print(f"[red]Topic '{topic}' not found[/red]")
            console.print("\n[bold]Available topics:[/bold]")
            for t in service.list_topics():
                console.print(f"  [green]{t.id}[/green] - {t.title}")
            raise typer.Exit(1)

        console.print(
            Panel(
                f"[bold cyan]{topic_content.title}[/bold cyan]\n"
                f"[dim]{topic_content.description}[/dim]\n"
                f"[dim]Difficulty: {topic_content.difficulty}[/dim]",
                border_style="cyan",
            )
        )

        for section in topic_content.sections:
            console.print(f"\n[bold]{section['title']}[/bold]")
            console.print(section["content"])

        if topic_content.examples:
            console.print("\n[bold cyan]Examples:[/bold cyan]")
            for example in topic_content.examples:
                console.print(f"\n[bold]{example['title']}[/bold]")
                console.print(f"[dim]{example['code']}[/dim]")

        if topic_content.related_topics:
            console.print(
                f"\n[dim]Related topics: "
                f"{', '.join(topic_content.related_topics)}[/dim]"
            )
    else:
        # List all topics
        topics = service.list_topics()
        table = Table(title="Available Learning Topics", border_style="cyan")
        table.add_column("Topic ID", style="bold green")
        table.add_column("Title")
        table.add_column("Difficulty")
        table.add_column("Description", style="dim")

        for t in topics:
            table.add_row(t.id, t.title, t.difficulty, t.description[:60])

        console.print(table)
        console.print("\n[dim]Use: tac-bootstrap learn --topic <id>[/dim]")


@app.command(name="tutorial")
def tutorial_cmd(
    tutorial_type: str = typer.Option(
        "quick-start", "--type", "-t", help="Tutorial type"
    ),
) -> None:
    """
    Run an interactive tutorial.

    Examples:
        $ tac-bootstrap tutorial --type quick-start
        $ tac-bootstrap tutorial --type advanced
    """
    from tac_bootstrap.application.learning_service import LearningService

    service = LearningService()
    tut = service.get_tutorial(tutorial_type)

    if tut is None:
        console.print(f"[red]Tutorial '{tutorial_type}' not found[/red]")
        console.print("\n[bold]Available tutorials:[/bold]")
        for t in service.list_tutorials():
            console.print(
                f"  [green]{t.id}[/green] - {t.title} ({t.estimated_minutes} min)"
            )
        raise typer.Exit(1)

    console.print(
        Panel(
            f"[bold cyan]{tut.title}[/bold cyan]\n"
            f"[dim]{tut.description}[/dim]\n"
            f"Difficulty: {tut.difficulty} | Est. time: {tut.estimated_minutes} min",
            border_style="cyan",
            title="Tutorial",
        )
    )

    if tut.prerequisites:
        console.print("\n[bold]Prerequisites:[/bold]")
        for prereq in tut.prerequisites:
            console.print(f"  - {prereq}")

    for i, step in enumerate(tut.steps, 1):
        console.print(
            f"\n[bold cyan]Step {i}/{len(tut.steps)}:[/bold cyan] {step['title']}"
        )
        console.print(f"  {step['instruction']}")
        if step.get("command"):
            console.print(f"  [dim]$ {step['command']}[/dim]")


# --- Feature 17: Team ---

team_app = typer.Typer(
    name="team",
    help="Team collaboration features",
)
app.add_typer(team_app, name="team")


@team_app.command("share")
def team_share(
    user: str = typer.Option(
        ..., "--user", "-u", help="Email address to share with"
    ),
    role: str = typer.Option(
        "contributor", "--role", "-r",
        help="Role: owner, admin, contributor, viewer",
    ),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Share project with a team member.

    Examples:
        $ tac-bootstrap team share --user alice@company.com
    """
    try:
        from tac_bootstrap.application.team_service import TeamService

        service = TeamService()
        member = service.share_project(project_path.resolve(), user, role)

        console.print(
            Panel(
                f"[bold green]Project shared with {user}[/bold green]\n"
                f"[cyan]Role:[/cyan] {member.role}\n"
                f"[cyan]Added:[/cyan] {member.added_at}",
                border_style="green",
                title="Shared",
            )
        )
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@team_app.command("list-shared")
def team_list_shared(
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    List team members for a project.

    Examples:
        $ tac-bootstrap team list-shared
    """
    from tac_bootstrap.application.team_service import TeamService

    service = TeamService()
    members = service.list_shared(project_path.resolve())

    if not members:
        console.print("[yellow]No team members for this project[/yellow]")
        return

    table = Table(title="Team Members", border_style="cyan")
    table.add_column("Email", style="bold")
    table.add_column("Role")
    table.add_column("Added")
    table.add_column("Last Sync", style="dim")

    for m in members:
        table.add_row(
            m.email,
            m.role,
            m.added_at[:19],
            m.last_sync[:19] if m.last_sync else "Never",
        )

    console.print(table)


@team_app.command("sync")
def team_sync(
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Sync changes with team.

    Examples:
        $ tac-bootstrap team sync
    """
    from tac_bootstrap.application.team_service import TeamService

    service = TeamService()
    result = service.sync_changes(project_path.resolve())

    if result.success:
        console.print(
            Panel(
                f"[bold green]Sync completed[/bold green]\n"
                f"[dim]{result.message}[/dim]",
                border_style="green",
                title="Team Sync",
            )
        )
    else:
        console.print("[red]Sync failed[/red]")
        raise typer.Exit(1)


@team_app.command("notify")
def team_notify(
    message: str = typer.Option(
        ..., "--message", "-m", help="Notification message"
    ),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Send a notification to the team.

    Examples:
        $ tac-bootstrap team notify --message "Updated API schema"
    """
    from tac_bootstrap.application.team_service import TeamService

    service = TeamService()
    notif = service.notify_team(project_path.resolve(), message)

    console.print(f"[green]Notification sent:[/green] {notif.message}")


# --- Feature 18: Metrics ---

metrics_app = typer.Typer(
    name="metrics",
    help="Project analytics and metrics",
)
app.add_typer(metrics_app, name="metrics")


@metrics_app.command("generate")
def metrics_generate(
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Generate project metrics.

    Examples:
        $ tac-bootstrap metrics generate
    """
    from tac_bootstrap.application.metrics_service import MetricsService

    service = MetricsService()
    console.print("[cyan]Generating project metrics...[/cyan]")

    metrics = service.generate_metrics(project_path.resolve())

    # Health score panel
    grade_color = (
        "green"
        if metrics.health_score >= 70
        else ("yellow" if metrics.health_score >= 40 else "red")
    )
    console.print(
        Panel(
            f"[bold {grade_color}]{metrics.health_grade}[/bold {grade_color}] "
            f"Health Score: [{grade_color}]{metrics.health_score}/100[/{grade_color}]",
            border_style=grade_color,
            title="Project Health",
        )
    )

    # Complexity table
    table = Table(title="Code Metrics", border_style="cyan")
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Source Files", str(metrics.source_file_count))
    table.add_row("Test Files", str(metrics.test_file_count))
    table.add_row("Total Lines", str(metrics.complexity.total_lines))
    table.add_row("Functions", str(metrics.complexity.total_functions))
    table.add_row("Classes", str(metrics.complexity.total_classes))
    table.add_row("Avg File Length", f"{metrics.complexity.average_file_length:.1f}")
    table.add_row("Avg Complexity", f"{metrics.complexity.average_complexity:.2f}")
    table.add_row("Dependencies", str(metrics.dependencies.total_dependencies))

    console.print(table)

    # Recommendations
    if metrics.recommendations:
        console.print("\n[bold]Recommendations:[/bold]")
        for rec in metrics.recommendations:
            console.print(f"  - {rec}")

    # Save to history
    service.save_metrics_history(project_path.resolve(), metrics)


@metrics_app.command("show")
def metrics_show(
    metric: str = typer.Option(
        "complexity", "--metric", "-m",
        help="Metric to show (complexity, coverage)",
    ),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Show specific project metrics.

    Examples:
        $ tac-bootstrap metrics show --metric complexity
    """
    from tac_bootstrap.application.metrics_service import MetricsService

    service = MetricsService()

    if metric == "complexity":
        complexity = service.get_complexity_metrics(project_path.resolve())

        console.print(
            Panel(
                f"[bold]Code Complexity Analysis[/bold]\n\n"
                f"[cyan]Files:[/cyan] {complexity.total_files}\n"
                f"[cyan]Total Lines:[/cyan] {complexity.total_lines}\n"
                f"[cyan]Average Complexity:[/cyan] {complexity.average_complexity:.2f}",
                border_style="cyan",
                title="Complexity Metrics",
            )
        )

        if complexity.most_complex_files:
            table = Table(title="Most Complex Files", border_style="yellow")
            table.add_column("File", style="bold")
            table.add_column("Lines")
            table.add_column("Functions")
            table.add_column("Complexity", style="yellow")

            for fm in complexity.most_complex_files[:10]:
                table.add_row(
                    fm.path,
                    str(fm.total_lines),
                    str(fm.functions),
                    f"{fm.complexity_score:.1f}",
                )
            console.print(table)
    else:
        console.print(
            f"[yellow]Metric '{metric}' display not yet implemented[/yellow]"
        )


@metrics_app.command("history")
def metrics_history(
    days: int = typer.Option(
        30, "--days", "-d", help="Number of days of history"
    ),
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Show metrics history.

    Examples:
        $ tac-bootstrap metrics history --days 30
    """
    from tac_bootstrap.application.metrics_service import MetricsService

    service = MetricsService()
    history_data = service.get_metrics_history(project_path.resolve(), days=days)

    if not history_data:
        console.print(
            "[yellow]No metrics history found. "
            "Run 'tac-bootstrap metrics generate' first.[/yellow]"
        )
        return

    table = Table(title=f"Metrics History (last {days} days)", border_style="cyan")
    table.add_column("Date", style="bold")
    table.add_column("Health")
    table.add_column("Grade")
    table.add_column("Files")
    table.add_column("Lines")
    table.add_column("Complexity")

    for entry in history_data[-20:]:
        table.add_row(
            entry.get("timestamp", "")[:10],
            str(entry.get("health_score", 0)),
            entry.get("health_grade", ""),
            str(entry.get("total_files", 0)),
            str(entry.get("total_lines", 0)),
            f"{entry.get('avg_complexity', 0):.2f}",
        )

    console.print(table)


# --- Feature 19: Recommendations ---

@app.command()
def recommend(
    project_path: Path = typer.Option(
        Path("."), "--path", "-p", help="Project path"
    ),
) -> None:
    """
    Get smart recommendations for project improvements.

    Analyzes security, structure, testing, performance, and dependencies.

    Examples:
        $ tac-bootstrap recommend
        $ tac-bootstrap recommend --path /my/project
    """
    from tac_bootstrap.application.recommendation_service import RecommendationService

    service = RecommendationService()
    console.print("[cyan]Analyzing project for recommendations...[/cyan]\n")
    report = service.analyze(project_path.resolve())

    if report.total == 0:
        console.print(
            Panel(
                "[bold green]No recommendations - your project looks great![/bold green]",
                border_style="green",
                title="Recommendations",
            )
        )
        return

    # Summary
    console.print(
        Panel(
            f"[bold]Found {report.total} recommendation(s)[/bold]\n\n"
            f"[red]Critical:[/red] {report.critical}\n"
            f"[yellow]Warnings:[/yellow] {report.warnings}\n"
            f"[blue]Info:[/blue] {report.info}",
            border_style="cyan",
            title="Recommendations",
        )
    )

    # Details
    for rec in report.recommendations:
        if rec.severity == "critical":
            color = "red"
            icon = "[X]"
        elif rec.severity == "warning":
            color = "yellow"
            icon = "[!]"
        else:
            color = "blue"
            icon = "[i]"

        console.print(
            f"\n[{color}]{icon} [{rec.severity.upper()}] {rec.title}[/{color}]"
        )
        if rec.description:
            console.print(f"  {rec.description}")
        if rec.suggestion:
            console.print(f"  [dim]Suggestion: {rec.suggestion}[/dim]")
        if rec.file_path:
            console.print(f"  [dim]File: {rec.file_path}[/dim]")


# --- Feature 20: Community ---

community_app = typer.Typer(
    name="community",
    help="Community plugins, templates, and achievements",
)
app.add_typer(community_app, name="community")


@community_app.command("share")
def community_share(
    plugin_name: str = typer.Option(
        ..., "--plugin", help="Plugin name to share"
    ),
    description: str = typer.Option(
        "", "--desc", "-d", help="Plugin description"
    ),
    category: str = typer.Option(
        "general", "--category", "-c", help="Plugin category"
    ),
) -> None:
    """
    Share a plugin to the community registry.

    Examples:
        $ tac-bootstrap community share --plugin my-auth-plugin
    """
    try:
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService()
        item = service.share_plugin(
            name=plugin_name, description=description, category=category
        )

        console.print(
            Panel(
                f"[bold green]Plugin '{item.name}' shared successfully[/bold green]\n"
                f"[cyan]Category:[/cyan] {item.category}\n"
                f"[cyan]Type:[/cyan] {item.item_type}",
                border_style="green",
                title="Community Share",
            )
        )
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@community_app.command("publish")
def community_publish(
    template_name: str = typer.Option(
        ..., "--template", help="Template name to publish"
    ),
    description: str = typer.Option(
        "", "--desc", "-d", help="Template description"
    ),
    category: str = typer.Option(
        "general", "--category", "-c", help="Template category"
    ),
) -> None:
    """
    Publish a template to the community.

    Examples:
        $ tac-bootstrap community publish --template my-template
    """
    try:
        from tac_bootstrap.application.community_service import CommunityService

        service = CommunityService()
        item = service.publish_template(
            name=template_name, description=description, category=category
        )

        console.print(
            Panel(
                f"[bold green]Template '{item.name}' published[/bold green]\n"
                f"[cyan]Category:[/cyan] {item.category}",
                border_style="green",
                title="Community Publish",
            )
        )
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@community_app.command("browse")
def community_browse(
    category: Optional[str] = typer.Option(
        None, "--category", "-c", help="Filter by category"
    ),
    query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Search query"
    ),
) -> None:
    """
    Browse community templates and plugins.

    Examples:
        $ tac-bootstrap community browse --category authentication
    """
    from tac_bootstrap.application.community_service import CommunityService

    service = CommunityService()
    templates = service.browse_templates(category=category, query=query)
    plugins = service.browse_plugins(category=category, query=query)

    all_items = templates + plugins
    if not all_items:
        console.print("[yellow]No items found matching your criteria[/yellow]")
        return

    table = Table(title="Community Items", border_style="cyan")
    table.add_column("Name", style="bold green")
    table.add_column("Type")
    table.add_column("Category")
    table.add_column("Description")
    table.add_column("Rating", style="yellow")

    for item in all_items:
        rating_str = f"{item.rating:.1f}/5" if item.rating > 0 else "-"
        table.add_row(
            item.name,
            item.item_type,
            item.category,
            item.description[:50],
            rating_str,
        )

    console.print(table)


@community_app.command("awards")
def community_awards() -> None:
    """
    View achievements and badges.

    Examples:
        $ tac-bootstrap community awards
    """
    from tac_bootstrap.application.community_service import CommunityService

    service = CommunityService()
    awards = service.get_awards()

    table = Table(title="Achievements", border_style="cyan")
    table.add_column("Badge", style="bold")
    table.add_column("Name")
    table.add_column("Description")
    table.add_column("Points")
    table.add_column("Status")

    for award in awards:
        status_str = (
            "[green]Earned[/green]" if award.earned else "[dim]Locked[/dim]"
        )
        table.add_row(
            award.icon, award.name, award.description, str(award.points), status_str
        )

    console.print(table)

    # Show total points
    total = sum(a.points for a in awards if a.earned)
    console.print(f"\n[bold cyan]Total Points:[/bold cyan] {total}")


if __name__ == "__main__":
    app()
