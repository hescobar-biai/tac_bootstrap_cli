# Feature: Add docs-scraper.md.j2 Agent Template

## Metadata
issue_number: `266`
adw_id: `feature_Tac_9_task_25`
issue_json: `{"number":266,"title":"Add docs-scraper.md.j2 agent template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_25\n\nAdd docs-scraper.md.j2 agent template\n\n**Description:**\nCreate Jinja2 template for docs-scraper agent definition.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/docs-scraper.md` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for the docs-scraper agent definition that can be used by TAC Bootstrap CLI to generate documentation scraping agents in target projects. This template will enable projects to have a specialized agent that fetches and saves documentation from URLs as properly formatted markdown files for offline reference and analysis.

The template conversion follows TAC Bootstrap's pattern: source files from `.claude/`, `adws/`, and `scripts/` serve as templates that get parameterized with Jinja2 variables for generation into target projects.

## User Story
As a TAC Bootstrap CLI user
I want to generate a docs-scraper agent in my project
So that I can automatically fetch and save documentation from URLs as markdown files for offline reference

## Problem Statement
TAC Bootstrap CLI needs to provide a docs-scraper agent template that:
1. Can be rendered with project-specific configuration (project name, output directory)
2. Maintains the full functionality of the source agent definition
3. Follows existing template patterns in the codebase
4. Can be validated by rendering it in the bootstrap repo itself (dogfooding)

Currently, the template infrastructure exists (`tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/`) but the docs-scraper template is missing.

## Solution Statement
Convert the source docs-scraper agent definition from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md` into a Jinja2 template with minimal variable substitution:

1. Create `docs-scraper.md.j2` template with Jinja2 variables for:
   - Project-specific references (use `config.project.name` where applicable)
   - Output directory paths (already hardcoded as `ai_docs/` which is standard)
   - Keep all agent functionality, tools, workflow, and best practices static

2. Render the template for the bootstrap repo itself at `.claude/agents/docs-scraper.md` to validate it works and dogfood our own templates

3. Follow existing template patterns (observed in commands templates which use minimal Jinja2)

## Relevant Files
Files necessary to implement the feature:

- **Source file** (READ):
  - `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md` - Source agent definition to convert

- **Template directory** (CONTEXT):
  - `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` - Target directory for .j2 template
  - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/*.j2` - Reference patterns for Jinja2 usage

- **Configuration** (CONTEXT):
  - `config.yml` - Contains `config.project.name`, `config.project.description` variables
  - `tac_bootstrap_cli/tac_bootstrap/domain/config.py` - Config schema (if exists)

- **Test infrastructure** (CONTEXT):
  - `tac_bootstrap_cli/tests/test_*.py` - Existing test patterns to follow if adding tests

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Jinja2 template (CREATE)
- `.claude/agents/docs-scraper.md` - Rendered version for bootstrap repo (CREATE)

## Implementation Plan

### Phase 1: Read and Understand Source
Read the source agent definition and understand its structure, identifying minimal project-specific elements that need parameterization.

### Phase 2: Create Template
Convert the source to a Jinja2 template with minimal variable substitution, maintaining all functionality while parameterizing only project-specific references.

### Phase 3: Validate Template
Render the template using bootstrap repo's own config to create `.claude/agents/docs-scraper.md` and verify it works correctly (dogfooding).

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read source agent definition
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md` to understand content structure
- If source unavailable, fallback to check if `.claude/agents/docs-scraper.md` exists locally
- Identify which parts need project-specific parameterization (project name references)
- Identify which parts should remain static (tools, workflow, best practices)

### Task 2: Create Jinja2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`
- Convert source to Jinja2 template with minimal variables:
  - Use `{{ config.project.name }}` for project-specific name references (if any)
  - Keep `ai_docs/` as OUTPUT_DIRECTORY (standard path, no need to parameterize)
  - Keep all tools, model, color, purpose, workflow, and best practices static
  - Maintain YAML frontmatter structure (name, description, tools, model, color)
- Follow patterns from existing command templates for Jinja2 syntax

### Task 3: Render template for bootstrap repo
- Manually render the template using bootstrap repo config values:
  - config.project.name = "tac-bootstrap"
  - config.project.description = (from config.yml or CLAUDE.md)
- Create `.claude/agents/docs-scraper.md` with rendered content
- This validates the template works and provides immediate usability in bootstrap repo

### Task 4: Verify template structure
- Verify `.j2` template has proper Jinja2 syntax
- Verify rendered `.claude/agents/docs-scraper.md` has valid YAML frontmatter
- Verify rendered version maintains all functionality from source
- Ensure no broken variable references or syntax errors

### Task 5: Run validation commands
- Execute all validation commands to ensure zero regressions
- Confirm template files are properly created

## Testing Strategy

### Unit Tests
If test infrastructure exists for template rendering:
- Add test case for `docs-scraper.md.j2` template rendering
- Verify template renders without errors
- Verify rendered output has valid YAML frontmatter
- Follow patterns from existing template tests

If no test infrastructure exists:
- Skip automated testing (out of scope for single template task)
- Manual validation via rendered `.claude/agents/docs-scraper.md` is sufficient

### Edge Cases
- Template should render correctly with different project names
- YAML frontmatter should remain valid after rendering
- No Jinja2 syntax errors or undefined variable references

## Acceptance Criteria
- ✅ Template file created: `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`
- ✅ Rendered file created: `.claude/agents/docs-scraper.md` with bootstrap repo config
- ✅ Template uses minimal Jinja2 variables (only for project-specific elements)
- ✅ Template maintains all agent functionality from source (tools, workflow, best practices)
- ✅ Rendered file has valid YAML frontmatter
- ✅ No syntax errors in template or rendered output
- ✅ All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a template conversion task, not an agent design task
- Keep changes minimal - only parameterize what's necessary for different projects
- The source agent definition is authoritative for functionality
- Bootstrap repo should dogfood its own templates (render for itself)
- OUTPUT_DIRECTORY is `ai_docs/` which is standard across projects
- Most agent definitions are largely static with minimal project customization needed
- Follow existing patterns from command templates for Jinja2 usage
- If source file is unavailable, ask user for alternative source or content
