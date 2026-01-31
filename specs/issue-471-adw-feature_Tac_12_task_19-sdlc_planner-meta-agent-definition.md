# Feature: Meta-Agent Definition

## Metadata
issue_number: `471`
adw_id: `feature_Tac_12_task_19`
issue_json: `{"number": 471, "title": "[Task 19/49] [FEATURE] Create meta-agent.md agent definition", "body": "## Description\n\nCreate a meta-agent that generates OTHER agents based on specifications.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/agents/meta-agent.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`\n\n## Key Features\n- Agent generation\n- Template-based agent creation\n- tools: Read, Write, Edit, Glob, Grep\n\n## Changes Required\n- Create agent file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in agents list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/agents/meta-agent.md`\n\n## Wave 2 - New Agents (Task 19 of 6)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_19"}`

## Feature Description
Create a specialized meta-agent that generates other agent definitions based on natural language specifications. This agent will streamline the process of creating new agents by automatically generating both the base markdown file (.md) and its corresponding Jinja2 template (.j2) following established patterns in the codebase. The meta-agent will accept flexible natural language prompts, perform basic validation, and support referencing existing agents as templates for creating variations.

## User Story
As a TAC Bootstrap developer
I want to generate new agent definitions using natural language specifications
So that I can quickly create consistent, well-structured agents without manually writing boilerplate markdown and templates

## Problem Statement
Creating new agent definitions requires:
1. Understanding the agent markdown format and structure
2. Manually writing both .md and .j2 files with consistent patterns
3. Ensuring all required sections (name, description, tools, instructions) are present
4. Converting the .md to a Jinja2 template with proper {{ config }} variables
5. Manually updating scaffold_service.py to register the new agent

This manual process is error-prone, time-consuming, and requires deep knowledge of existing patterns. A meta-agent can automate agent generation, enforce consistency, and accelerate development.

## Solution Statement
Implement a meta-agent.md file (and corresponding .j2 template) that:
- Accepts natural language specifications for agent creation
- Reads existing agents when specified to use as templates
- Generates both .md and .j2 files automatically
- Performs basic validation (required sections, known tool list)
- Asks for user confirmation before overwriting existing agents
- Supports flexible tool assignment from the Claude Code toolkit
- Follows established patterns from docs-scraper.md and scout-report-suggest.md

The meta-agent will focus solely on agent file generation, leaving scaffold_service.py updates as a manual step or future enhancement.

## Relevant Files
Files needed to implement this feature:

### Existing Pattern References
- `.claude/agents/docs-scraper.md` - Example of workflow-focused agent with multiple tools
- `.claude/agents/scout-report-suggest.md` - Example of YAML frontmatter format with focused purpose
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/docs-scraper.md.j2` - Template pattern example
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/scout-report-suggest.md.j2` - Template with frontmatter

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add meta-agent to agents list (lines 410-426)

### New Files
- `.claude/agents/meta-agent.md` - Base agent definition file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` - Jinja2 template version

## Implementation Plan

### Phase 1: Foundation
1. Study existing agent patterns to understand:
   - YAML frontmatter format vs. markdown-only format
   - Tool specification patterns
   - Instruction structure and detail level
   - Best practices from docs-scraper and scout-report-suggest
2. Identify available Claude Code tools for meta-agent use: Read, Write, Edit, Glob, Grep
3. Design meta-agent specification input format (natural language with key elements: name, description, tools, capabilities)

### Phase 2: Core Implementation
1. Create `.claude/agents/meta-agent.md` with:
   - YAML frontmatter (name, description, tools, model, color)
   - Clear purpose statement
   - Workflow for accepting specifications and generating agents
   - Instructions for reading reference agents
   - Basic validation logic (required sections, known tools)
   - Confirmation prompts before overwriting
   - Examples of generating agents from scratch and from templates
2. Create corresponding `.j2` template with {{ config }} variables where appropriate

### Phase 3: Integration
1. Update `scaffold_service.py` to include meta-agent in the agents list
2. Ensure both .md and .j2 files are included in scaffold plan

## Step by Step Tasks

### Task 1: Analyze Existing Agent Patterns
- Read `.claude/agents/docs-scraper.md` to understand workflow-style agent structure
- Read `.claude/agents/scout-report-suggest.md` to understand YAML frontmatter format
- Read corresponding .j2 templates to understand templatization patterns
- Document key structural elements and best practices

### Task 2: Create Meta-Agent Base Definition
- Create `.claude/agents/meta-agent.md` with:
  - YAML frontmatter: name, description, tools (Read, Write, Edit, Glob, Grep), model (sonnet), color
  - Purpose section explaining meta-agent role
  - Workflow section with steps:
    1. Accept natural language specification
    2. Parse agent requirements (name, description, tools, capabilities)
    3. Check for reference agent if specified
    4. Read reference agent and adapt if using template approach
    5. Validate basic requirements (sections, tools)
    6. Check for existing agent files and confirm overwrite
    7. Generate .md file content
    8. Generate .j2 template from .md
    9. Write both files
  - Instructions for natural language format
  - Examples of generating agents from scratch and from templates
  - Tool usage guidelines
  - Validation rules
  - Error handling

### Task 3: Create Meta-Agent Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`
- Convert static content from .md to use {{ config }} variables where appropriate
- Ensure template matches base file structure

### Task 4: Update Scaffold Service
- Add meta-agent to agents list in `scaffold_service.py` (around line 413)
- Entry format: `("meta-agent.md", "Agent generation from specifications")`
- Verify agents list alphabetical ordering if applicable

### Task 5: Validation and Testing
- Verify both .md and .j2 files exist and are properly formatted
- Check that scaffold_service.py includes meta-agent
- Run validation commands to ensure no regressions
- Test that generated files follow expected patterns

## Testing Strategy

### Unit Tests
- Verify meta-agent.md file exists at `.claude/agents/meta-agent.md`
- Verify meta-agent.md.j2 template exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2`
- Verify scaffold_service.py includes meta-agent in agents list
- Verify template renders correctly with sample TACConfig

### Edge Cases
- Meta-agent generating itself (recursive case) - should work normally
- Requesting agent with unknown tools - validation should catch
- Requesting agent with minimal specification - should generate with defaults
- Overwriting existing agent - should prompt for confirmation

## Acceptance Criteria
1. `.claude/agents/meta-agent.md` exists with complete agent definition including:
   - YAML frontmatter with name, description, tools, model, color
   - Clear purpose and workflow sections
   - Detailed instructions for agent generation
   - Examples of both scratch generation and template-based generation
   - Validation and error handling guidance
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/agents/meta-agent.md.j2` exists and correctly templates the base file
3. `scaffold_service.py` includes meta-agent in the agents list
4. All validation commands pass with zero errors
5. Files follow existing agent patterns and conventions
6. Meta-agent can accept natural language specifications
7. Meta-agent supports reading reference agents as templates
8. Meta-agent performs basic validation on generated agents
9. Meta-agent asks for confirmation before overwriting files

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The meta-agent focuses on generating agent definition files only
- Updating scaffold_service.py remains a manual step (could be automated in future)
- The agent uses Read/Write/Edit/Glob/Grep tools only (no Bash or external tools)
- Natural language specifications should include: agent name, description, tools needed, key capabilities
- Basic validation includes checking for required sections and known tools, but no strict schema
- Reference agent path can be external volume (may not be accessible) - fall back to existing patterns
- Support generating both YAML frontmatter style and markdown-only style based on specifications
- The meta-agent should be self-documenting with clear examples
