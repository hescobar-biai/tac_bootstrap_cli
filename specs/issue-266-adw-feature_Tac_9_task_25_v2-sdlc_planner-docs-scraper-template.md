# Feature: Add docs-scraper.md.j2 Agent Template

## Metadata
issue_number: `266`
adw_id: `feature_Tac_9_task_25_v2`
issue_json: `{"number":266,"title":"Add docs-scraper.md.j2 agent template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_25_v2\n\nAdd docs-scraper.md.j2 agent template\n\n**Description:**\nCreate Jinja2 template for docs-scraper agent definition.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/docs-scraper.md` (CREATE - rendered)"}`

## Feature Description
Create a generic, reusable docs-scraper agent template as a Jinja2 template file that will be included in the TAC Bootstrap CLI generator. This agent template will provide instructions for scraping documentation from URLs and integrating them into project context. The template will be project-agnostic and configurable, allowing generated projects to customize it for their specific documentation needs.

This feature adds to the templates library that TAC Bootstrap uses to generate agentic layers for projects. The docs-scraper agent will be a self-contained markdown definition that explains how to fetch, process, and contextualize external documentation.

## User Story
As a developer using TAC Bootstrap to generate an agentic layer for my project
I want to have a docs-scraper agent template available
So that I can easily scrape and integrate external documentation (API docs, framework guides, etc.) into my project's AI context without having to write the agent definition from scratch

## Problem Statement
Currently, the TAC Bootstrap CLI lacks an agent template for documentation scraping. When developers need to integrate external documentation into their AI-assisted workflows, they must:
1. Manually create agent definitions from scratch
2. Figure out best practices for web scraping and context integration
3. Reinvent patterns that could be standardized across projects

This creates unnecessary friction and inconsistency in how projects handle external documentation integration.

## Solution Statement
Create a generic docs-scraper agent template (`docs-scraper.md.j2`) with minimal Jinja2 templating that:
1. Uses only `config.project.name` for project-specific customization
2. Provides clear, instructional content on how to scrape documentation URLs
3. Explains how to integrate scraped content into project context
4. Serves as both a template for generation and a working example in tac_bootstrap itself
5. Follows the same patterns as existing command templates (e.g., build.md.j2)

The template will be self-contained and instructional rather than pre-configured with hardcoded URLs, allowing maximum reusability across different projects and documentation sources.

## Relevant Files
Files necessary for implementing the feature:

### Existing Files to Reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/build.md.j2` - Example of minimal Jinja2 templating pattern
- `config.yml` - Contains project configuration structure (project.name available)
- `CLAUDE.md` - Project guidelines for template development

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Main template file (CREATE)
- `.claude/agents/docs-scraper.md` - Rendered version for tac_bootstrap's own use (CREATE)

## Implementation Plan

### Phase 1: Research and Design
Research existing template patterns and design the docs-scraper agent structure following TAC Bootstrap conventions.

### Phase 2: Template Creation
Create the Jinja2 template file with minimal templating (config.project.name only) and instructional content for documentation scraping.

### Phase 3: Rendered Example
Create a rendered version in .claude/agents/ to demonstrate the template works and provide a working example for the tac_bootstrap project itself.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create docs-scraper.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2`
- Use minimal Jinja2 templating with `{{ config.project.name }}` only
- Structure content as an instructional agent definition with:
  - Clear description of the agent's purpose
  - Instructions on how to use WebFetch or similar tools to scrape documentation URLs
  - Guidance on processing and integrating scraped content into project context
  - Examples of common documentation sources (API docs, framework guides)
  - Best practices for handling different documentation formats
- Follow the pattern from build.md.j2 for conditional rendering
- Keep content generic and project-agnostic

### Task 2: Create .claude/agents Directory Structure
- Create `.claude/agents/` directory if it doesn't exist
- Ensure proper directory permissions and .gitkeep if needed

### Task 3: Create Rendered Example
- Create rendered version at `.claude/agents/docs-scraper.md`
- Replace `{{ config.project.name }}` with "tac-bootstrap" from config.yml
- Ensure the rendered file demonstrates the template works correctly
- This provides a working example for the tac_bootstrap project itself

### Task 4: Validation
- Verify both files exist and have correct content
- Check that template uses only config.project.name
- Confirm rendered version has "tac-bootstrap" properly substituted
- Ensure content is instructional and generic (no hardcoded project-specific URLs)
- Run validation commands

## Testing Strategy

### Unit Tests
Not applicable for this feature - this is a static template file addition. Testing will be done through file validation and visual inspection.

### Edge Cases
- Template rendering with missing config values (should handle gracefully with Jinja2 defaults)
- Projects without internet access (agent should still provide useful instructions)
- Different types of documentation sources (HTML, markdown, PDF, API endpoints)

## Acceptance Criteria
1. Template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` exists
2. Template uses minimal Jinja2 templating (only `{{ config.project.name }}`)
3. Template content is instructional and explains:
   - How to scrape documentation URLs
   - How to integrate content into project context
   - Best practices for documentation handling
4. Rendered file `.claude/agents/docs-scraper.md` exists
5. Rendered file has "tac-bootstrap" substituted for config.project.name
6. Both files follow markdown format and TAC Bootstrap conventions
7. Content is generic and reusable across different projects
8. No hardcoded project-specific URLs or configuration

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Verify template exists
- `ls -la .claude/agents/docs-scraper.md` - Verify rendered file exists
- `cat tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Inspect template content
- `cat .claude/agents/docs-scraper.md` - Inspect rendered content
- `grep -c "{{ config.project.name }}" tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Verify Jinja2 variable usage
- `grep -c "tac-bootstrap" .claude/agents/docs-scraper.md` - Verify rendering

## Notes
- This feature does NOT require changes to the config schema - agents are self-contained markdown files
- The source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/docs-scraper.md` is inaccessible, so we create a generic template based on best practices
- The template follows the YAGNI principle - keeping it simple without adding unnecessary configuration
- Future enhancements could add more sophisticated features, but the initial implementation focuses on providing clear instructions
- The docs-scraper agent will be most useful for projects that need to integrate external documentation like:
  - API reference docs (REST, GraphQL)
  - Framework documentation (React, FastAPI, etc.)
  - Library documentation (Python packages, npm modules)
  - Internal company documentation
- The agent should emphasize using Claude Code's built-in WebFetch tool rather than external scraping libraries
