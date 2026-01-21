# Feature: Create Template `install.md.j2`

## Metadata
issue_number: `44`
adw_id: `d450b40b`
issue_json: `{"number":44,"title":"TAREA 3: Crear Template `install.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/install.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /install.\n\nEste comando instala dependencias del proyecto:\n1. Detecta el package manager (uv, npm, poetry, etc.)\n2. Ejecuta el comando de instalación apropiado\n3. Verifica instalación exitosa\n4. Reporta cualquier error de dependencias\n\nVariables disponibles:\n- {{ config.project.package_manager }}\n- {{ config.project.language }}\n- {{ config.paths.app_root }}\n\nMapeo de package managers a comandos:\n- uv -> uv sync\n- poetry -> poetry install\n- pip -> pip install -r requirements.txt\n- npm -> npm install\n- pnpm -> pnpm install\n- yarn -> yarn install\n- bun -> bun install\n\nIncluye manejo de errores común (network, permissions, version conflicts).\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Soporta todos los package managers del enum\n- [ ] Incluye verificación post-instalación\n"}`

## Feature Description
Create a new Jinja2 template for the `/install` slash command that will be used by TAC Bootstrap to generate install command files for target projects. This template will enable Claude agents to install project dependencies using the appropriate package manager for each project.

The template is part of the TAC Bootstrap CLI system, which generates agentic layers for projects. This specific template will be rendered when users initialize or add agentic capabilities to their projects, providing them with a standardized `/install` command that intelligently handles dependency installation based on the project's package manager.

## User Story
As a TAC Bootstrap user
I want to have an `/install` command template in my generated agentic layer
So that Claude agents can install project dependencies correctly using the appropriate package manager for my project

## Problem Statement
The TAC Bootstrap CLI needs to generate slash command files for target projects. Currently, there is no template for the `/install` command, which is a critical command for setting up development environments and ensuring dependencies are properly installed.

Without this template:
- Users cannot have agents automatically install project dependencies
- There's no standardized way for agents to detect and use the correct package manager
- The generated agentic layer is incomplete for onboarding workflows
- Common installation errors are not handled consistently

## Solution Statement
Create a Jinja2 template file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` that:

1. Follows the same structure and format as existing command templates (test.md.j2, build.md.j2, lint.md.j2)
2. Uses Jinja2 variables from the config object to determine the package manager
3. Maps each package manager enum value to its corresponding install command
4. Provides clear instructions for agents on how to run installation and verify success
5. Includes error handling for common installation issues (network errors, permission errors, version conflicts)
6. Verifies that the installation completed successfully
7. Reports installation status and any errors clearly

The template will be rendered by the TemplateRepository infrastructure when generating agentic layers for target projects.

## Relevant Files
Files necessary for implementing this feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2` - Reference template showing standard structure and format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Reference template showing conditional command handling
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2` - Reference template showing error handling pattern
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Shows PackageManager enum with all supported package managers
- `config.yml` - Shows how config structure defines project.package_manager

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` - The new install command template

## Implementation Plan

### Phase 1: Foundation
1. Study the existing command templates (test.md.j2, build.md.j2, lint.md.j2) to understand:
   - File structure and markdown format
   - How Jinja2 variables are used
   - How conditional logic handles different scenarios
   - The standard sections (Variables, Instructions, Report)

2. Review the PackageManager enum in domain/models.py to understand all supported package managers

3. Review config.yml to understand how config.project.package_manager is defined

### Phase 2: Core Implementation
1. Create the install.md.j2 template file with:
   - Header and description
   - Variables section
   - Instructions section with:
     - Package manager detection using {{ config.project.package_manager }}
     - Conditional Jinja2 blocks for each package manager mapping to its install command
     - Error handling instructions for common issues
     - Post-installation verification instructions
   - Report section with expected output format

2. Ensure the template matches the style and structure of existing command templates

### Phase 3: Integration
1. Verify the template file is in the correct location within the templates directory structure
2. Ensure the file follows naming conventions (.md.j2 extension)
3. Validate that Jinja2 syntax is correct and will render without errors

## Step by Step Tasks

### Task 1: Analyze Reference Templates and Package Manager Enum
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/test.md.j2`
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2`
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/lint.md.j2`
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` to see PackageManager enum values
- Identify common patterns, structure, and Jinja2 usage

### Task 2: Create install.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2`
- Include all required sections:
  - Title: "Install"
  - Description: "Install project dependencies"
  - Variables section: document $ARGUMENTS parameter if needed
  - Instructions section:
    - Use Jinja2 conditionals to map package manager to install command:
      - `{% if config.project.package_manager == "uv" %}` -> `uv sync`
      - `{% elif config.project.package_manager == "poetry" %}` -> `poetry install`
      - `{% elif config.project.package_manager == "pip" %}` -> `pip install -r requirements.txt`
      - `{% elif config.project.package_manager == "npm" %}` -> `npm install`
      - `{% elif config.project.package_manager == "pnpm" %}` -> `pnpm install`
      - `{% elif config.project.package_manager == "yarn" %}` -> `yarn install`
      - `{% elif config.project.package_manager == "bun" %}` -> `bun install`
      - `{% elif config.project.package_manager == "go" %}` -> `go mod download`
      - `{% elif config.project.package_manager == "cargo" %}` -> `cargo build`
      - `{% elif config.project.package_manager == "maven" %}` -> `mvn install`
      - `{% elif config.project.package_manager == "gradle" %}` -> `gradle build`
      - `{% else %}` -> No package manager configured
    - Instructions for handling common installation errors:
      - Network connectivity issues
      - Permission errors
      - Version conflicts
      - Missing lock files
    - Instructions for verifying installation success
    - Note not to modify code files during installation
  - Report section:
    - Installation status (success/failed)
    - Dependencies installed count (if available)
    - Any warnings or errors
    - Verification result

### Task 3: Verify Template Quality
- Check that all Jinja2 variables use correct syntax
- Ensure conditional logic covers all PackageManager enum values
- Verify markdown formatting is consistent with other templates
- Confirm file uses correct variables from config object
- Ensure error handling instructions are comprehensive

### Task 4: Validate Implementation
- Run validation commands to ensure no regressions
- Verify the template file exists in the correct location
- Check that the template follows the same format as existing command templates

## Testing Strategy

### Unit Tests
While this task creates a template file (no unit tests for the template itself), validation will be done through:
- File existence check
- Template syntax validation (Jinja2 can render without errors)
- Comparison with reference templates to ensure consistency
- Verification that all PackageManager enum values are handled

### Edge Cases
- Package manager not configured (should show helpful message)
- Unsupported package manager (should have else clause)
- Installation failures (network, permissions, conflicts)
- Projects without lock files
- Projects with multiple potential package managers

## Acceptance Criteria
- Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2`
- Template uses correct Jinja2 variable syntax: `{{ config.project.package_manager }}`, `{{ config.project.language }}`, etc.
- Template follows the same structure and format as test.md.j2, build.md.j2, and lint.md.j2
- Template includes conditional handling for all package managers in the PackageManager enum:
  - UV (uv sync)
  - Poetry (poetry install)
  - Pip (pip install -r requirements.txt)
  - Pipenv (pipenv install)
  - NPM (npm install)
  - PNPM (pnpm install)
  - Yarn (yarn install)
  - Bun (bun install)
  - Go (go mod download)
  - Cargo (cargo build)
  - Maven (mvn install)
  - Gradle (gradle build)
- Template has clear sections: Variables, Instructions, Report
- Template includes instructions for error handling (network, permissions, version conflicts)
- Template includes instructions for post-installation verification
- Template instructs agents not to modify code during installation
- No syntax errors in Jinja2 template
- File uses .md.j2 extension following naming convention

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/install.md.j2` - Verify file exists

## Notes
- This is a template creation task, not a code implementation task
- The template will be used by the TemplateRepository to generate install commands for target projects
- The template should be simple and focused - it's a markdown file that agents will read as instructions
- Reference existing templates heavily to maintain consistency
- The actual dependency installation will happen in the target project, not in TAC Bootstrap itself
- This task is part of FASE 3 (Templates System) in the TAC Bootstrap roadmap
- The PackageManager enum in domain/models.py is the source of truth for supported package managers
- Some package managers (like cargo and gradle) combine build and dependency installation in a single command
