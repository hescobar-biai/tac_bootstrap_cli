# Feature: Create Template `prepare_app.md.j2`

## Metadata
issue_number: `43`
adw_id: `073aa60c`
issue_json: `{"number":43,"title":"TAREA 2: Crear Template `prepare_app.md.j2`","body":"**Archivo a crear:** `tac_bootstrap/templates/claude/commands/prepare_app.md.j2`\n\n**Prompt:**\n```\nCrea el template Jinja2 para el comando slash /prepare_app.\n\nEste comando prepara la aplicación para ejecución:\n1. Verifica dependencias instaladas\n2. Configura variables de entorno necesarias\n3. Ejecuta migraciones si aplica\n4. Valida que la app puede iniciarse\n\nUsa como referencia:\n- tac_bootstrap/templates/claude/commands/start.md.j2\n- El comando /prepare_app en ../../.claude/commands/prepare_app.md\n\nVariables disponibles:\n- {{ config.project.name }}\n- {{ config.project.language }}\n- {{ config.project.framework }}\n- {{ config.commands.start }}\n- {{ config.paths.app_root }}\n\nEl comando debe ser idempotente (ejecutar múltiples veces no causa problemas).\n```\n\n**Criterios de aceptación:**\n- [ ] Template renderiza sin errores\n- [ ] Cubre preparación para diferentes lenguajes\n- [ ] Es idempotente"}`

## Feature Description
Create a Jinja2 template for the `/prepare_app` slash command that will be used by TAC Bootstrap CLI to generate project-specific preparation commands. This template prepares an application environment for execution by verifying dependencies, configuring environment variables, running migrations, and validating the application can start.

The template must be parametric and support multiple languages, frameworks, and package managers through Jinja2 templating with the `config` context variable containing the complete TACConfig model.

## User Story
As a developer using TAC Bootstrap
I want to have a `/prepare_app` command automatically generated for my project
So that I can quickly prepare my application environment before running or testing, regardless of the project's language or framework

## Problem Statement
Currently, TAC Bootstrap generates various slash commands for Claude Code integration, but the `/prepare_app` template is missing. This command is essential for:
1. Ensuring all dependencies are installed before running the app
2. Setting up environment variables and configuration
3. Running database migrations or other setup steps
4. Validating the application can start successfully
5. Providing an idempotent operation that can be run multiple times safely

Without this template, generated projects lack a standardized way to prepare their application environment, forcing developers to manually create project-specific preparation scripts.

## Solution Statement
Create a parametric Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2` that:
1. Uses the existing `.claude/commands/prepare_app.md` as a reference for structure
2. Adapts to different project configurations via `config.*` variables
3. Generates language-specific dependency installation commands
4. Includes framework-specific preparation steps (e.g., migrations for Django/Rails)
5. Validates the application can start using `config.commands.start`
6. Maintains idempotency - safe to run multiple times
7. Follows the same pattern as existing command templates like `start.md.j2`

## Relevant Files
Files necessary for implementing the feature:

### Existing Reference Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/start.md.j2` - Similar template structure to follow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/commit.md.j2` - Example of template patterns
- `.claude/commands/prepare_app.md` - Original prepare_app command (non-templated version)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig models showing available variables

### Related Template Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/*.md.j2` - Other command templates for consistency

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2` - The template to create

## Implementation Plan

### Phase 1: Foundation
1. Read and analyze reference files to understand template patterns
2. Identify all `config.*` variables needed for prepare_app functionality
3. Map language/package manager combinations to dependency installation commands
4. Determine framework-specific preparation steps

### Phase 2: Core Implementation
1. Create the `prepare_app.md.j2` template file
2. Implement conditional logic for different languages using Jinja2
3. Add package manager-specific dependency installation commands
4. Include framework-specific steps (migrations, builds, etc.)
5. Add validation step using `config.commands.start`

### Phase 3: Integration
1. Verify template syntax is valid Jinja2
2. Test template rendering with sample configurations
3. Ensure idempotency of all operations
4. Validate against acceptance criteria

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze Reference Files
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/start.md.j2` to understand template structure
- Read `.claude/commands/prepare_app.md` to understand the non-templated version
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py` to identify available config variables
- Document the pattern used in existing templates

### Task 2: Design Template Logic
- Map Language enum values to package managers (Python→uv/pip/poetry, TypeScript→npm/pnpm/bun, etc.)
- Identify dependency installation commands per package manager
- Determine framework-specific preparation needs (Django migrations, Next.js build, etc.)
- Plan conditional logic structure in Jinja2

### Task 3: Create Base Template Structure
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2`
- Add markdown header with command name
- Add instructions section with numbered steps
- Add report section template

### Task 4: Implement Dependency Installation Logic
- Add conditional blocks for different package managers using `{% if config.project.package_manager == PackageManager.UV %}`
- Include commands for: uv sync, npm install, pip install, go mod download, cargo build, etc.
- Ensure commands are idempotent (use sync, install flags that don't fail if already installed)

### Task 5: Add Framework-Specific Preparation
- Add conditional blocks for frameworks requiring special setup
- Django: `{{ config.project.package_manager_prefix }} python manage.py migrate`
- Rails: `bundle exec rails db:migrate`
- Next.js: `{{ config.commands.build }}` if build command exists
- Make all steps optional based on framework detection

### Task 6: Add Environment Validation
- Check for required environment files (.env, config files)
- Validate configuration is present
- Add optional warning if files are missing

### Task 7: Add Application Start Validation
- Use `{{ config.commands.start }} &` to start app in background (if applicable)
- Add timeout and health check
- Verify app responds or logs show successful start
- Clean up background process

### Task 8: Test Template Rendering
- Create test script to render template with various config combinations
- Test Python + UV + FastAPI configuration
- Test TypeScript + PNPM + Next.js configuration
- Test Go + go mod configuration
- Verify all renderings are valid markdown and commands are correct

### Task 9: Validate Idempotency
- Review all commands to ensure they can be run multiple times
- Verify dependency installs don't fail if already installed
- Ensure migrations are safe to re-run
- Confirm no destructive operations are included

### Task 10: Execute Validation Commands
- Run all validation commands listed below
- Fix any errors or warnings
- Ensure zero regressions

## Testing Strategy

### Unit Tests
Since this is a template file, testing will be done through:
1. Manual rendering with pytest tests that:
   - Load the template using TemplateRepository
   - Render with various TACConfig fixtures
   - Validate output contains expected commands
   - Verify Jinja2 syntax is valid

2. Integration tests in `tests/infrastructure/test_template_repo.py`:
   ```python
   def test_prepare_app_template_renders_python_uv():
       config = TACConfig(...)
       template_repo = TemplateRepository()
       content = template_repo.render("claude/commands/prepare_app.md.j2", config=config)
       assert "uv sync" in content
   ```

### Edge Cases
1. **Missing optional commands**: Config without build or test commands
2. **Minimal configuration**: Project with Language.PYTHON, PackageManager.UV, Framework.NONE
3. **Complex configuration**: Full-featured web app with database, migrations, build steps
4. **No framework**: Generic projects without web framework
5. **Multiple package managers**: Ensure correct one is selected from config

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2`
- [ ] Template renders without Jinja2 syntax errors for all language/framework combinations
- [ ] Template includes dependency installation for all supported package managers (uv, npm, pnpm, bun, pip, poetry, go mod, cargo, maven)
- [ ] Template includes framework-specific preparation (Django migrations, Next.js builds, etc.) as conditional blocks
- [ ] Template validates application can start using `config.commands.start`
- [ ] All operations are idempotent - safe to run multiple times
- [ ] Template follows same structure and style as existing command templates (`start.md.j2`, `commit.md.j2`)
- [ ] Template uses `config.*` variables correctly (config.project.name, config.project.language, config.project.framework, config.commands.start, config.paths.app_root)
- [ ] Template includes a "Report" section for command output
- [ ] Documentation/comments explain conditional logic where needed

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The template should be defensive: check for existence of files/commands before using them
- Use Jinja2 filters like `| default("value")` for optional config values
- Reference the TACConfig Pydantic models to ensure variable names match exactly
- Consider that this command will be used both for new projects and existing projects
- The command should provide helpful error messages if preparation fails
- Since this is part of FASE 3 (Templates), ensure it follows patterns established in previous template creation tasks
- The template is part of the Agentic Layer - it will be used by AI agents, so clear instructions are critical
