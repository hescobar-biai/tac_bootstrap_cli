# Feature: Add research-docs-fetcher Agent Template

## Metadata
issue_number: `268`
adw_id: `feature_Tac_9_task_27`
issue_json: `{"number":268,"title":"Add research-docs-fetcher.md.j2 agent template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_27\n\n***Description:**\nCreate Jinja2 template for research-docs-fetcher agent definition.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/research-docs-fetcher.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/research-docs-fetcher.md` (CREATE - rendered)\n"}`

## Feature Description
Create a Jinja2 template for the `research-docs-fetcher` agent definition that can be used by the TAC Bootstrap CLI generator to create this agent in generated projects. The research-docs-fetcher agent specializes in researching and fetching documentation from various sources (official docs, GitHub repos, API references) to integrate them into the project's AI-assisted development context.

This feature adds to the growing collection of agent templates (docs-scraper, meta-agent) that TAC Bootstrap can generate, enabling AI-powered documentation research workflows in generated projects.

## User Story
As a TAC Bootstrap user
I want the CLI to generate a research-docs-fetcher agent definition
So that my generated projects have an AI agent specialized in researching and fetching external documentation for integration into development workflows

## Problem Statement
The TAC Bootstrap CLI currently has two agent templates (docs-scraper, meta-agent) but lacks a template for a research-docs-fetcher agent. Users who want their generated projects to include an agent specialized in researching documentation sources (not just scraping known URLs, but actively researching where to find documentation) must manually create this agent definition after project generation, which defeats the purpose of using an automated generator.

## Solution Statement
Create a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2` that follows the existing pattern established by `docs-scraper.md.j2`. The template will:

1. Use minimal templating (only `{{ config.project.name }}` where project name is referenced)
2. Define a research-docs-fetcher agent with clear purpose, tools, and instructions
3. Focus on research capabilities: identifying documentation sources, evaluating quality, and fetching relevant content
4. Be language-agnostic (works for Python, TypeScript, Go, etc.)

Additionally, create a rendered example in `.claude/agents/research-docs-fetcher.md` for demonstration purposes, and add basic rendering tests following the existing test patterns.

## Relevant Files
Files necessary to implement the feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Primary reference for structure and templating pattern (similar agent type)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` - Secondary reference for frontmatter format if needed
- `tac_bootstrap_cli/tests/test_template_repo.py` - Test patterns to follow for template rendering tests
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - TemplateRepository implementation (no changes needed, just reference)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model (no changes needed, just reference)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2` (template)
- `.claude/agents/research-docs-fetcher.md` (rendered example for demonstration)

## Implementation Plan

### Phase 1: Foundation
1. Request source file content from user (since `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/research-docs-fetcher.md` is outside working directory and blocked by security constraints)
2. Analyze the source content to understand the agent's purpose, tools, and instructions
3. Study the `docs-scraper.md.j2` template pattern to understand templating approach

### Phase 2: Core Implementation
1. Create the Jinja2 template following the `docs-scraper.md.j2` pattern:
   - Use minimal templating (only `{{ config.project.name }}` where needed)
   - Keep agent instructions static (language-agnostic)
   - Maintain markdown format (not frontmatter-based like meta-agent)
   - Focus on research and discovery capabilities (vs. docs-scraper which focuses on scraping)

2. Render an example to `.claude/agents/research-docs-fetcher.md` using a sample config for demonstration purposes

### Phase 3: Integration
1. Add basic rendering tests to verify template correctness:
   - Template renders without errors
   - Project name is correctly substituted
   - Output is valid markdown
2. Run validation commands to ensure zero regressions

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Request Source Content
- Ask user to provide the content of `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/research-docs-fetcher.md`
- If unavailable, design agent based on name and similar patterns (research + documentation fetching)

### Task 2: Study Reference Templates
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` to understand structure
- Note minimal templating pattern (only `{{ config.project.name }}`)
- Identify differences between research-focused vs scraping-focused agents

### Task 3: Create Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2`
- Follow docs-scraper structure: Description, Purpose, Tools, Instructions, Examples, Error Handling
- Focus on research capabilities:
  - Identifying where documentation exists (not just fetching known URLs)
  - Evaluating documentation quality and relevance
  - Discovering official vs community docs
  - Searching GitHub repos, package registries, etc.
- Use minimal templating: only `{{ config.project.name }}`

### Task 4: Render Example
- Create sample TACConfig for rendering
- Render template to `.claude/agents/research-docs-fetcher.md`
- Verify rendered output is valid markdown

### Task 5: Add Tests
- Add test methods to `tac_bootstrap_cli/tests/test_template_repo.py` following existing patterns:
  - `test_research_docs_fetcher_template_renders` - Verify template renders without errors
  - `test_research_docs_fetcher_template_substitutes_project_name` - Verify project name substitution
  - Include in existing test class or create new class if appropriate

### Task 6: Validate Implementation
- Run all validation commands (see Validation Commands section)
- Fix any issues found
- Ensure zero regressions in existing tests

## Testing Strategy

### Unit Tests
1. **Template Rendering Test**: Verify template renders without Jinja2 errors
   - Use TemplateRepository to render "claude/agents/research-docs-fetcher.md.j2"
   - Should not raise TemplateRenderError or TemplateNotFoundError

2. **Project Name Substitution Test**: Verify `{{ config.project.name }}` is correctly substituted
   - Render with TACConfig containing project.name = "test-app"
   - Assert "test-app" appears in rendered output
   - Assert no unrendered template variables remain (no `{{` or `}}`)

3. **Markdown Validity Test**: Verify output is valid markdown
   - Check for required sections: Description, Purpose, Tools, Instructions
   - Verify code blocks are properly formatted
   - Ensure consistent structure with docs-scraper

### Edge Cases
1. **Project names with special characters**: Test with names like "my-test_app", "MyApp", "app123"
2. **Minimal config**: Test with bare minimum TACConfig to ensure no missing fields cause errors
3. **Empty project name**: Should handle gracefully (though validation should prevent this upstream)

## Acceptance Criteria
1. ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/research-docs-fetcher.md.j2`
2. ✅ Template follows docs-scraper.md.j2 pattern (minimal templating, markdown format)
3. ✅ Template renders successfully with sample TACConfig
4. ✅ Rendered example exists at `.claude/agents/research-docs-fetcher.md`
5. ✅ Project name (`{{ config.project.name }}`) is correctly templated and substitutes properly
6. ✅ Agent definition is language-agnostic (works for Python, TypeScript, Go, etc.)
7. ✅ Agent focuses on research capabilities (finding docs) vs just scraping (fetching known URLs)
8. ✅ Tests added and passing (template rendering, project name substitution)
9. ✅ All validation commands pass with zero regressions
10. ✅ Template is discoverable via TemplateRepository.list_templates("claude")

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
1. **Source file unavailable**: The source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/research-docs-fetcher.md` is outside the working directory and cannot be read directly. If user cannot provide content, we can design a reasonable research-docs-fetcher agent based on:
   - The name and implied purpose (research + documentation fetching)
   - The existing docs-scraper pattern (but focused on research/discovery)
   - Common documentation research workflows

2. **Difference between research-docs-fetcher and docs-scraper**:
   - `docs-scraper`: Takes known URLs and scrapes/processes documentation
   - `research-docs-fetcher`: Actively researches WHERE to find documentation, evaluates sources, then fetches

3. **Template simplicity**: Following the established pattern, agent templates use minimal Jinja2 templating. Most content is static instructions. Only the project name needs to be templated.

4. **Language-agnostic design**: Documentation research is universal across programming languages, so the agent should not have language-specific logic or conditional blocks.

5. **Testing pattern**: Follow the existing test patterns in `test_template_repo.py`. Agent template tests are straightforward: render the template and verify no errors + correct substitution.

6. **No new dependencies**: This feature requires no additional libraries. Uses existing Jinja2 templating infrastructure.

7. **Future enhancement**: Consider adding conditional logic for framework-specific documentation sources (e.g., Django docs for Django projects, React docs for React projects), but keep simple for initial implementation.
