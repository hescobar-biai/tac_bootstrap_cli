# Feature: Add meta-agent.md.j2 Agent Template

## Metadata
issue_number: `267`
adw_id: `feature_Tac_9_task_26`
issue_json: `{"number":267,"title":"Add meta-agent.md.j2 agent template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_26\n\n**Description:**\nCreate Jinja2 template for meta-agent definition.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/meta-agent.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/meta-agent.md` (CREATE - rendered)\n"}`

## Feature Description
Create a Jinja2 template for the meta-agent definition that will be used by TAC Bootstrap CLI to generate agent configuration files in target projects. The meta-agent is a specialized Claude Code sub-agent that acts as an agent architect, generating new sub-agent configuration files based on user descriptions.

The template will be placed in the templates directory structure and will use Jinja2 variables from the config object to allow customization for different projects. This complements the existing docs-scraper agent template and expands the TAC Bootstrap's capability to generate comprehensive agentic development environments.

## User Story
As a TAC Bootstrap CLI user
I want to generate a meta-agent configuration in my project
So that I can dynamically create new specialized agents using natural language descriptions within Claude Code

## Problem Statement
The TAC Bootstrap currently has a docs-scraper agent template, but lacks the meta-agent template that enables dynamic agent creation. Users need a meta-agent that can generate new specialized sub-agents on demand, following best practices for Claude Code agent architecture. Without this template, generated projects lack the meta-programming capability to evolve their agent ecosystem.

## Solution Statement
Create a Jinja2 template file `meta-agent.md.j2` based on the source file from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/meta-agent.md`. The template will:

1. Define the meta-agent's frontmatter (name, description, tools, model, color)
2. Specify the agent's purpose and workflow for creating new agents
3. Include instructions for analyzing user prompts and generating agent configurations
4. Use Jinja2 variables (config.project.name) for project-specific customization
5. Follow the established pattern from docs-scraper.md.j2 for consistency

The template will enable the CLI to generate functional meta-agents in target projects, preserving the agent architecture and delegation patterns of the TAC framework.

## Relevant Files
Files necessary for implementing this feature:

**Source Reference:**
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/meta-agent.md` - Source meta-agent definition (read to understand structure)
  - Contains frontmatter with agent metadata
  - Defines agent purpose, workflow, and output format
  - Lists tools needed and delegation description

**Existing Templates (for pattern reference):**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Existing agent template showing Jinja2 variable usage
  - Shows usage of {{ config.project.name }}
  - Demonstrates agent documentation structure
  - Provides formatting patterns

**Configuration:**
- `config.yml` - Project configuration defining available config variables
  - Defines config.project.name and other variables
  - Shows structure of config object

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` - The new Jinja2 template file (primary deliverable)

## Implementation Plan

### Phase 1: Foundation
1. Read and analyze the source meta-agent file from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/meta-agent.md` to understand its structure
2. If source file is inaccessible, design from scratch based on meta-agent patterns: agent orchestration, dynamic agent creation, delegation rules
3. Review docs-scraper.md.j2 to understand Jinja2 variable usage patterns
4. Review config.yml to identify available template variables

### Phase 2: Core Implementation
1. Create the directory structure if needed: `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/`
2. Create `meta-agent.md.j2` template file with:
   - Frontmatter section (name, description, tools, color, model)
   - Purpose section explaining meta-agent role
   - Workflow section with step-by-step instructions for agent creation
   - Output format section defining agent file structure
   - Jinja2 variables for project customization where appropriate

### Phase 3: Integration
1. Verify template syntax is valid Jinja2
2. Verify frontmatter follows YAML format
3. Ensure consistency with existing agent template patterns
4. Document template in comments if needed

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read and Analyze Source Material
- Attempt to read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/agents/meta-agent.md`
- If accessible, analyze its structure and content
- If inaccessible, proceed with design based on meta-agent architectural patterns
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` to understand template patterns
- Identify where Jinja2 variables should be used

### Task 2: Ensure Directory Structure Exists
- Verify `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/` directory exists
- Create directory if needed (should already exist from docs-scraper template)

### Task 3: Create meta-agent.md.j2 Template
- Create the file `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`
- Define frontmatter with:
  - name: meta-agent
  - description: Action-oriented delegation description
  - tools: Write, WebFetch, mcp__firecrawl-mcp__firecrawl_scrape, mcp__firecrawl-mcp__firecrawl_search, MultiEdit
  - color: cyan
  - model: opus
- Add Purpose section explaining meta-agent role as agent architect
- Add Workflow section with 10 steps for creating new agents:
  1. Get up-to-date documentation from Claude Code docs
  2. Analyze user's prompt for agent requirements
  3. Devise kebab-case agent name
  4. Select agent color from available options
  5. Write delegation description for frontmatter
  6. Infer necessary tools based on agent tasks
  7. Construct system prompt for new agent
  8. Provide numbered list of actions
  9. Incorporate domain-specific best practices
  10. Define output structure and assemble complete agent file
- Add Output Format section with example agent structure
- Use Jinja2 variable {{ config.project.name }} where project name is referenced
- Maintain markdown formatting and structure from source

### Task 4: Review and Validate Template
- Verify Jinja2 syntax is valid
- Verify YAML frontmatter format is correct
- Check consistency with docs-scraper.md.j2 patterns
- Ensure all sections are complete and clear
- Confirm template will generate valid Claude Code agent configuration

### Task 5: Run Validation Commands
- Execute all validation commands listed below to ensure zero regressions

## Testing Strategy

### Unit Tests
No unit tests required for this template-only feature. Template rendering will be validated through:
1. Jinja2 syntax validation (linting)
2. Manual review of template structure
3. Future integration tests when CLI uses the template

### Edge Cases
- Project name with special characters → Jinja2 variable should handle this
- Missing config variables → Template should have sensible defaults or fallbacks
- Template rendering in different project contexts → Use minimal config variables to ensure broad compatibility

## Acceptance Criteria
1. File `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` exists and is valid Jinja2 template
2. Template contains proper YAML frontmatter with name, description, tools, color, model fields
3. Template defines clear Purpose, Workflow, and Output Format sections
4. Template uses {{ config.project.name }} variable consistently with docs-scraper.md.j2
5. Template follows markdown structure matching source meta-agent.md file
6. Template includes all 10 workflow steps for agent creation
7. Frontmatter specifies correct tools: Write, WebFetch, firecrawl scrape/search, MultiEdit
8. All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This template is part of the TAC Bootstrap's agent template library
- The meta-agent enables meta-programming: an agent that creates other agents
- Future enhancement could include template rendering validation in CI/CD
- The rendered .claude/agents/meta-agent.md file should NOT be created in this task - it's only for CLI generation
- Keep minimal config variables to ensure template works across different project types
- Color choice (cyan) and model choice (opus) match the source file specifications
- The meta-agent uses opus model for better reasoning when architecting new agents
