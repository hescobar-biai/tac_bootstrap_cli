# Main CLI Commands Implementation

**ADW ID:** a83dbd52
**Date:** 2026-01-20
**Specification:** specs/issue-21-adw-a83dbd52-sdlc_planner-implement-main-cli-commands.md

## Overview

Implemented the 4 core CLI commands for TAC Bootstrap (`init`, `add-agentic`, `doctor`, `render`) that provide a complete user-facing interface for generating and managing Agentic Layers in projects. The commands use Typer for argument parsing and Rich for beautiful terminal output with panels, colors, and formatted messages.

## What Was Built

- **`init` command**: Create new projects with Agentic Layer from scratch
- **`add-agentic` command**: Inject Agentic Layer into existing repositories with auto-detection
- **`doctor` command**: Validate and diagnose existing Agentic Layer setups
- **`render` command**: Regenerate files from modified config.yml
- **`version` command**: Display version information with Rich formatting
- **Main callback**: Shows welcome panel when no command is provided
- Enhanced Rich console integration with panels, colored output, and error handling
- Placeholder service integration for future implementation (TAREA 4.2, FASE 6, FASE 7)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/interfaces/cli.py`: Expanded from minimal stub (23 lines) to complete CLI implementation (572 lines) with all 4 commands, Rich formatting, error handling, and placeholder service calls
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tac_bootstrap/__init__.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tac_bootstrap/__main__.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/pyproject.toml`: Added `types-PyYAML>=6.0.0` to dev dependencies, added mypy `disable_error_code` for import-untyped and misc
- `tac_bootstrap_cli/tests/test_cli.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tests/test_template_repo.py`: Code formatting cleanup (no functional changes)
- `tac_bootstrap_cli/tests/test_version.py`: Code formatting cleanup (no functional changes)

### Key Changes

1. **CLI Infrastructure Setup** (cli.py:1-35)
   - Imported Typer, Rich Console/Panel, Path, Optional, yaml
   - Imported domain models (Language, Framework, PackageManager, Architecture, TACConfig, etc.)
   - Created global Rich Console instance for formatted output
   - Configured Typer app with name, help text, completion disabled, and rich_markup_mode

2. **Main Callback with Welcome Panel** (cli.py:38-62)
   - Displays formatted welcome panel when no subcommand is invoked
   - Shows TAC Bootstrap version, description, and available commands
   - Uses Rich Panel with cyan border and formatted text

3. **Version Command** (cli.py:65-74)
   - Displays version in Rich Panel with cyan/green formatting
   - Uses `__version__` imported from tac_bootstrap package

4. **Init Command** (cli.py:77-221)
   - Arguments: `name` (required project name)
   - Options: `--output/-o`, `--language/-l`, `--framework/-f`, `--package-manager/-p`, `--architecture/-a`, `--interactive/--no-interactive`, `--dry-run`
   - Auto-detects package manager if not specified using `get_package_managers_for_language()`
   - Builds TACConfig with ProjectSpec, PathsSpec, CommandsSpec, ClaudeConfig defaults
   - Placeholder integration with ScaffoldService.build_plan() and apply_plan()
   - Dry-run mode shows preview panel with directories and files
   - Success panel displays stats (files/dirs created) and next steps
   - Graceful error handling for ImportError (service not implemented) and general exceptions

5. **Add-Agentic Command** (cli.py:224-357)
   - Arguments: `repo_path` (defaults to current directory)
   - Options: `--interactive/--no-interactive`, `--dry-run`, `--force/-f`
   - Validates repo_path exists and is a directory
   - Placeholder integration with DetectService for auto-detection
   - Displays auto-detection results panel (name, language, framework, package manager)
   - Builds TACConfig from detected settings in non-interactive mode
   - Calls build_plan() with `existing_repo=True` parameter
   - Dry-run shows preview of file actions (create/modify)
   - Graceful ImportError handling for DetectService (FASE 6)

6. **Doctor Command** (cli.py:360-455)
   - Arguments: `repo_path` (defaults to current directory)
   - Options: `--fix` (auto-fix issues)
   - Placeholder integration with DoctorService.diagnose()
   - Displays healthy panel (green) when all checks pass
   - Shows unhealthy panel (red) with counts of errors/warnings/info
   - Lists each issue with severity-based coloring (red=error, yellow=warning, blue=info) and icons (✗, ⚠, ℹ)
   - Displays suggestions with dim text
   - Auto-fix mode calls DoctorService.fix() and reports results
   - Exits with code 1 if unhealthy
   - Graceful ImportError handling for DoctorService (FASE 7)

7. **Render Command** (cli.py:458-568)
   - Arguments: `config_file` (defaults to config.yml)
   - Options: `--output/-o`, `--dry-run`, `--force/-f`
   - Validates config_file exists
   - Loads YAML with yaml.safe_load() and validates with TACConfig Pydantic model
   - Catches yaml.YAMLError and Pydantic validation errors with specific error messages
   - Determines target_dir (output_dir or config_file.parent)
   - Calls build_plan() with `existing_repo=True`
   - Dry-run shows preview of create/modify actions
   - Success panel shows stats (files created/modified)
   - Graceful ImportError handling for ScaffoldService (TAREA 4.2)

8. **Dependencies Added**
   - `types-PyYAML>=6.0.0` for mypy type checking of YAML library
   - mypy config updated to disable import-untyped and misc error codes (for placeholder service imports)

## How to Use

### Create New Project

```bash
# Interactive mode (wizard - not yet implemented)
cd tac_bootstrap_cli && uv run tac-bootstrap init my-app

# Non-interactive with defaults
cd tac_bootstrap_cli && uv run tac-bootstrap init my-app --no-interactive

# Specify all options
cd tac_bootstrap_cli && uv run tac-bootstrap init my-api \
  --language python \
  --framework fastapi \
  --package-manager uv \
  --architecture ddd \
  --no-interactive

# Preview without creating files
cd tac_bootstrap_cli && uv run tac-bootstrap init my-app --dry-run --no-interactive
```

### Inject Agentic Layer into Existing Repo

```bash
# Add to current directory (auto-detection - not yet implemented)
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic

# Add to specific repo
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic /path/to/repo

# Preview changes
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic --dry-run

# Force overwrite existing files
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic --force
```

### Validate Setup

```bash
# Check current directory (not yet implemented)
cd tac_bootstrap_cli && uv run tac-bootstrap doctor

# Check specific repo
cd tac_bootstrap_cli && uv run tac-bootstrap doctor /path/to/repo

# Auto-fix issues
cd tac_bootstrap_cli && uv run tac-bootstrap doctor --fix
```

### Regenerate from Config

```bash
# Regenerate from default config.yml (not yet implemented)
cd tac_bootstrap_cli && uv run tac-bootstrap render

# Use specific config file
cd tac_bootstrap_cli && uv run tac-bootstrap render my-config.yml

# Preview changes
cd tac_bootstrap_cli && uv run tac-bootstrap render --dry-run

# Force overwrite
cd tac_bootstrap_cli && uv run tac-bootstrap render --force
```

### Show Version

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap version
```

### Get Help

```bash
# General help
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Command-specific help
cd tac_bootstrap_cli && uv run tac-bootstrap init --help
cd tac_bootstrap_cli && uv run tac-bootstrap add-agentic --help
cd tac_bootstrap_cli && uv run tac-bootstrap doctor --help
cd tac_bootstrap_cli && uv run tac-bootstrap render --help
```

## Configuration

No additional configuration required. Commands use:
- Domain models from `tac_bootstrap.domain.models`
- Helper functions: `get_package_managers_for_language()`, `get_default_commands()`
- Rich Console for output formatting

## Testing

### Manual Testing (Current)

```bash
cd tac_bootstrap_cli

# Test help messages
uv run tac-bootstrap --help
uv run tac-bootstrap init --help
uv run tac-bootstrap add-agentic --help
uv run tac-bootstrap doctor --help
uv run tac-bootstrap render --help

# Test version command
uv run tac-bootstrap version

# Test main callback (no command)
uv run tac-bootstrap

# Type checking
uv run mypy tac_bootstrap/

# Linting
uv run ruff check .

# Format check
uv run ruff format --check .
```

### Unit Tests (Future)

Unit tests will be written when placeholder services are implemented:
- TAREA 4.2: ScaffoldService (used by `init` and `render`)
- FASE 6: DetectService (used by `add-agentic`)
- FASE 7: DoctorService (used by `doctor`)

## Notes

### Placeholder Services

This implementation provides the CLI interface, but the following services are placeholders that will fail at runtime with clear error messages:

1. **ScaffoldService** (`tac_bootstrap.application.scaffold_service`)
   - Used by: `init`, `render`
   - Will be implemented in: TAREA 4.2
   - Error message: "ScaffoldService not yet implemented: {ImportError}"

2. **DetectService** (`tac_bootstrap.application.detect_service`)
   - Used by: `add-agentic`
   - Will be implemented in: FASE 6
   - Error message: "DetectService not yet implemented: {ImportError}"

3. **DoctorService** (`tac_bootstrap.application.doctor_service`)
   - Used by: `doctor`
   - Will be implemented in: FASE 7
   - Error message: "DoctorService not yet implemented: {ImportError}"

4. **Wizard Functions** (`tac_bootstrap.interfaces.wizard`)
   - Used by: `init`, `add-agentic` (interactive mode)
   - Will be implemented in: TAREA 4.3
   - Current behavior: Shows "Interactive wizard not yet implemented" message

### Design Decisions

1. **Typer for CLI**: Modern framework with auto-generated help, type validation, and excellent UX
2. **Rich for Output**: Beautiful formatting with colors, panels, and better UX than plain print
3. **Dry-run Universal**: All destructive commands support --dry-run for safe preview
4. **Interactive by Default**: Commands use wizard by default (when implemented), can disable with --no-interactive
5. **Graceful Degradation**: Placeholder service imports fail with clear, helpful error messages indicating when feature will be available
6. **Consistent Error Handling**: All commands use try/except with Rich error formatting and typer.Exit(1)
7. **Auto-detection**: Package manager is auto-detected if not specified using language-specific defaults

### Future Enhancements (Out of Scope)

- `update` command: Update Agentic Layer to new template versions
- `list` command: List projects with Agentic Layer
- Custom template directories support
- Plugin system for command extensions

### Related Files

- Domain Models: tac_bootstrap_cli/tac_bootstrap/domain/models.py
- Plan Models: tac_bootstrap_cli/tac_bootstrap/domain/plan.py
- Implementation Plan: PLAN_TAC_BOOTSTRAP.md (TAREA 4.1)
- Specification: specs/issue-21-adw-a83dbd52-sdlc_planner-implement-main-cli-commands.md
