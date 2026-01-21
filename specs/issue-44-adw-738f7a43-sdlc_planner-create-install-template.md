# Feature: Create install.md.j2 Template

## Metadata
issue_number: `44`
adw_id: `738f7a43`
issue_json: `{"number":44,"title":"TAREA 3: Crear Template `install.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/install.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /install.\n\nEste comando instala dependencias del proyecto:\n1. Detecta el package manager (uv, npm, poetry, etc.)\n2. Ejecuta el comando de instalación apropiado\n3. Verifica instalación exitosa\n4. Reporta cualquier error de dependencias\n\nVariables disponibles:\n- {{ config.project.package_manager }}\n- {{ config.project.language }}\n- {{ config.paths.app_root }}\n\nMapeo de package managers a comandos:\n- uv -> uv sync\n- poetry -> poetry install\n- pip -> pip install -r requirements.txt\n- npm -> npm install\n- pnpm -> pnpm install\n- yarn -> yarn install\n- bun -> bun install\n\nIncluye manejo de errores común (network, permissions, version conflicts).\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Soporta todos los package managers del enum\n- [ ] Incluye verificación post-instalación\n"}`

## Feature Description
This task involves creating a Jinja2 template for the `/install` slash command that will be generated when TAC Bootstrap creates an agentic layer for new projects. The template will provide a focused, streamlined command specifically for installing project dependencies.

The install command template should:
- Detect the package manager from configuration
- Execute the appropriate installation command
- Verify successful installation
- Report any dependency errors
- Support all package managers defined in the PackageManager enum

This is distinct from the `/prepare_app` command which handles full application preparation including migrations, builds, and startup validation.

## User Story
As a TAC Bootstrap user
I want a `/install` command template that installs my project's dependencies
So that generated agentic layers can quickly install dependencies without full environment setup

## Problem Statement
While TAC Bootstrap has a comprehensive `/prepare_app` command, users often need a simpler, faster command that only installs dependencies without the overhead of environment validation, migrations, and startup checks. The `/install` command should be a lightweight, focused alternative that:
- Completes quickly
- Focuses solely on dependency installation
- Provides clear error reporting for installation issues
- Works across all supported package managers

## Solution Statement
Create a new Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` that renders a focused installation command. The template will:
- Use conditional Jinja2 blocks based on `config.project.package_manager.value`
- Map each PackageManager enum value to its installation command
- Include error handling for common installation issues (network failures, permission errors, version conflicts)
- Provide post-installation verification
- Follow the same structural pattern as existing command templates

## Relevant Files
Files necessary for implementing the feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` - **New file to create**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Reference for simple command pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2` - Reference for package manager conditionals
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - PackageManager enum definition (lines 82-101)
- `config.yml` - Shows the structure of config variables used in templates

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` - The new template file

## Implementation Plan

### Phase 1: Template Creation
Create the basic template structure following the pattern of existing command templates.

### Phase 2: Package Manager Mapping
Implement conditional blocks for all package managers in the PackageManager enum:
- Python: uv, poetry, pip, pipenv
- JavaScript/TypeScript: pnpm, npm, yarn, bun
- Go: go
- Rust: cargo
- Java: maven, gradle

### Phase 3: Error Handling & Verification
Add common error handling guidance and post-installation verification steps.

## Step by Step Tasks

### Task 1: Create install.md.j2 template file
- Create new file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2`
- Add header and description following test.md.j2 pattern
- Define the command's purpose: focused dependency installation

### Task 2: Implement package manager conditional blocks
- Add Jinja2 conditionals for each PackageManager enum value
- Map to installation commands:
  - `uv` → `uv sync`
  - `poetry` → `poetry install`
  - `pip` → `pip install -r requirements.txt`
  - `pipenv` → `pipenv install`
  - `pnpm` → `pnpm install`
  - `npm` → `npm install`
  - `yarn` → `yarn install`
  - `bun` → `bun install`
  - `go` → `go mod download`
  - `cargo` → `cargo build`
  - `maven` → `mvn dependency:resolve`
  - `gradle` → `gradle build --refresh-dependencies`
- Include `cd {{ config.paths.app_root }}` before each command

### Task 3: Add error handling guidance
- Document common installation errors:
  - Network failures (unreachable registry, timeouts)
  - Permission errors (write access to cache/lock files)
  - Version conflicts (incompatible dependencies)
  - Missing lock files or manifests
- Provide troubleshooting steps for each error type

### Task 4: Add post-installation verification
- Verify installation success by checking:
  - Exit code of installation command
  - Presence of dependency artifacts (node_modules, venv, etc.)
  - Lock file creation/update
- Report installation summary

### Task 5: Add Report section
- Follow the pattern of other templates
- Include sections for:
  - Dependencies installed: count/status
  - Installation time: approximate duration
  - Warnings: any non-critical issues
  - Errors: critical failures if any

### Task 6: Validate template rendering
- Test template renders without errors
- Verify all PackageManager enum values are covered
- Check that variables are correctly referenced
- Run validation commands (linting, type checking, tests)

## Testing Strategy

### Unit Tests
Create test cases in `tests/infrastructure/test_template_repo.py`:
- Test template renders for each package manager
- Test template with minimal config
- Test template with missing optional fields
- Verify output contains correct installation commands

### Edge Cases
- Package manager not in enum (should fail validation at config level)
- Empty app_root path (should use current directory)
- Missing package manager configuration (should be caught by Pydantic validation)

### Manual Testing
Render the template with various configurations:
```python
from tac_bootstrap.domain.models import TACConfig, ProjectSpec, PathsSpec, PackageManager, Language
from tac_bootstrap.infrastructure.template_repo import TemplateRepository

# Test with uv
config = TACConfig(
    project=ProjectSpec(name="test", language=Language.PYTHON, package_manager=PackageManager.UV),
    paths=PathsSpec(app_root="app"),
    commands={"start": "uv run python", "test": "uv run pytest"},
    claude=ClaudeConfig(settings=ClaudeSettings(project_name="test"))
)

repo = TemplateRepository()
rendered = repo.render_command_template("install.md.j2", config)
print(rendered)
```

## Acceptance Criteria
- [x] Template file created at correct path
- [x] Template renders without Jinja2 errors
- [x] All 12 PackageManager enum values have corresponding installation commands
- [x] Each installation command includes `cd {{ config.paths.app_root }}`
- [x] Error handling section documents common installation issues
- [x] Post-installation verification steps included
- [x] Report section follows template pattern
- [x] Template uses config variables correctly
- [x] Passes all validation commands

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This template is simpler than `/prepare_app` by design - it focuses only on dependency installation
- The `/prepare_app` command can internally call `/install` if desired, or remain comprehensive
- Installation commands follow official documentation for each package manager
- The template should be idempotent - running multiple times should be safe
- Some package managers (cargo, gradle) run build as part of dependency resolution - this is intentional
- For Go, `go mod download` is preferred over `go mod tidy` to avoid modifying go.mod
