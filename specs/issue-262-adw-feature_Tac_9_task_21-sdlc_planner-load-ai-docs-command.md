# Feature: Add load_ai_docs.md.j2 Command Template

## Metadata
issue_number: `262`
adw_id: `feature_Tac_9_task_21`
issue_json: `{"number":262,"title":"Add load_ai_docs.md.j2 command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_21\n\n**Description:**\nCreate Jinja2 template for `/load_ai_docs` slash command. Enables loading documentation via sub-agents.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/load_ai_docs.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_ai_docs.md` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for the `/load_ai_docs` slash command that enables loading AI documentation into Claude Code context via specialized sub-agents. This command will allow agents to efficiently ingest documentation from the `ai_docs/doc/` directory (or custom configured path) to understand project-specific AI methodologies, patterns, and guidelines.

The template will follow the same structure as existing command templates (e.g., `load_bundle.md.j2`) and minimally parameterize only the values that vary per project: project name and documentation path. All agent instructions, command structure, and TAC methodology standards remain hardcoded to ensure consistency across generated projects.

## User Story
As a developer using TAC Bootstrap
I want to generate a `/load_ai_docs` command for my project
So that Claude Code agents can efficiently load and understand my project's AI documentation structure

## Problem Statement
Currently, TAC Bootstrap can generate 25+ slash commands but lacks a template for the `/load_ai_docs` command. This command is essential for projects following the TAC methodology as it enables agents to:
- Load documentation from standardized `ai_docs/doc/` structure
- Understand project-specific AI patterns and methodologies
- Utilize specialized exploration agents to efficiently parse large documentation sets
- Maintain context about TAC courses (1-8) and project-specific guidelines

Without this template, generated projects lack a critical command for documentation loading, forcing manual creation and reducing the value of the bootstrap generator.

## Solution Statement
Create a Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` that:

1. **Minimal Parameterization**: Template only values that vary per project
   - `{{ config.project.name }}` for project-specific references
   - `{{ config.project.ai_docs_path | default('ai_docs/doc') }}` for documentation path with sensible default

2. **Preserved Structure**: Keep command format consistent
   - Variables section defining `doc_filter` argument
   - Instructions section with agent configuration
   - Run section with step-by-step execution flow
   - Report section with output format

3. **Agent Integration**: Leverage Task tool with Explore agent
   - Use specialized exploration for efficient documentation scanning
   - Support filtering by document number (e.g., "1-3" for TAC courses 1-3)
   - Handle missing directories gracefully

4. **Reference Implementation**: Create rendered example
   - Generate `.claude/commands/load_ai_docs.md` in tac_bootstrap repo
   - Serves as testing artifact and user reference
   - Demonstrates proper template rendering

## Relevant Files
Files necessary for implementing the feature:

### Existing Templates (Reference)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` - Similar command structure, reference for Variables/Instructions/Run/Report sections
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Example of documentation loading patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` - Example of Task tool usage with agents

### Configuration Schema
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - May need to verify `config.project.ai_docs_path` is supported or add it
- `config.yml` - Check if `ai_docs_path` configuration exists

### Documentation
- `.claude/commands/load_bundle.md` - Reference for command format
- `ai_docs/doc/` - The directory structure this command will load

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` - Main Jinja2 template (CREATE)
- `.claude/commands/load_ai_docs.md` - Rendered example for tac_bootstrap repo (CREATE)

## Implementation Plan

### Phase 1: Foundation
1. Research existing command templates to understand structure and patterns
2. Verify configuration schema supports `ai_docs_path` or document default behavior
3. Understand the ai_docs directory structure (doc/1.md through doc/8.md for TAC courses)

### Phase 2: Core Implementation
1. Create the Jinja2 template with proper parameterization
2. Implement Variables, Instructions, Run, and Report sections
3. Configure Task tool integration with Explore agent
4. Add documentation path handling with sensible defaults

### Phase 3: Integration
1. Render the template for tac_bootstrap's own `.claude/commands/` directory
2. Verify template renders correctly with minimal/default config
3. Test that generated command follows TAC methodology standards

## Step by Step Tasks

### Task 1: Analyze Existing Command Templates
- Read `load_bundle.md.j2` to understand command structure
- Read `prime.md.j2` to see documentation loading patterns
- Read `background.md.j2` to understand Task tool usage
- Identify common patterns: Variables, Instructions, Run, Report sections
- Note how Jinja2 variables are used (e.g., `{{ config.project.name }}`)

### Task 2: Verify Configuration Schema
- Read `tac_bootstrap_cli/tac_bootstrap/domain/models.py`
- Check if `ai_docs_path` exists in project config schema
- If missing, document that default `'ai_docs/doc'` will be used
- Verify `config.project.name` is available

### Task 3: Create load_ai_docs.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`
- Add header: `# Load AI Documentation`
- Add description explaining the command loads docs via specialized agents
- Implement **Variables** section:
  - `doc_filter: $ARGUMENT (optional)` - Filter for specific documents (e.g., "1-3")
- Implement **Instructions** section:
  - Explain ai_docs structure (courses 1-8)
  - Note expected directory: `{{ config.project.ai_docs_path | default('ai_docs/doc') }}`
  - Document filtering syntax (e.g., "1-3" loads doc/1.md through doc/3.md)
  - Note to use Task tool with Explore agent for efficient loading
- Implement **Run** section:
  1. Determine documentation path from config (default: ai_docs/doc)
  2. Parse doc_filter argument if provided
  3. Use Task tool with subagent_type=Explore to scan documentation
  4. Load filtered documents (or all if no filter)
  5. Report summary of loaded documents
- Implement **Examples** section:
  - Example 1: Load all docs: `/load_ai_docs`
  - Example 2: Load specific docs: `/load_ai_docs doc_filter=1-3`
  - Example 3: Load single doc: `/load_ai_docs doc_filter=5`
- Implement **Report** section:
  - Format for listing loaded documents
  - Total count and file paths
  - Note if any documents were missing

### Task 4: Create Rendered Example
- Create `.claude/commands/load_ai_docs.md` with rendered content
- Replace `{{ config.project.name }}` with "TAC Bootstrap" or similar
- Replace `{{ config.project.ai_docs_path | default('ai_docs/doc') }}` with `ai_docs/doc`
- Ensure rendered file is valid Markdown and follows command structure
- This serves as reference implementation and testing artifact

### Task 5: Validation
- Run validation commands (listed below)
- Verify template file exists and has valid Jinja2 syntax
- Verify rendered file exists and has valid Markdown
- Check that template follows patterns from similar commands
- Ensure minimal parameterization (only project name and ai_docs path)

## Testing Strategy

### Unit Tests
No Python unit tests required for this feature as it's pure template creation. Testing occurs via:
1. Manual verification of Jinja2 syntax
2. Rendering validation with default config
3. Markdown linting of rendered output

### Edge Cases
1. **Missing ai_docs directory**: Command should include note that directory is expected, agent handles error at runtime
2. **Custom ai_docs path**: Template should support config override via `{{ config.project.ai_docs_path }}`
3. **No filter provided**: Should load all documents from ai_docs/doc
4. **Invalid filter syntax**: Agent instructions should handle gracefully
5. **Empty ai_docs directory**: Runtime agent handles with appropriate message

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`
- [ ] Template uses minimal parameterization: only `{{ config.project.name }}` and `{{ config.project.ai_docs_path | default('ai_docs/doc') }}`
- [ ] Template includes all required sections: Variables, Instructions, Run, Examples, Report
- [ ] Template configures Task tool with Explore agent for documentation loading
- [ ] Rendered example created at `.claude/commands/load_ai_docs.md`
- [ ] Rendered file has valid Markdown and follows TAC command structure
- [ ] Template follows patterns from similar commands (load_bundle, prime, background)
- [ ] Documentation path defaults to `ai_docs/doc` but supports config override
- [ ] Command structure preserved (agent types, model configs hardcoded)
- [ ] All validation commands pass

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2 && echo "Template exists"` - Verify template created
- `test -f .claude/commands/load_ai_docs.md && echo "Rendered file exists"` - Verify rendered file created

## Notes
- This template is part of Phase 9 (Task 21) in PLAN_TAC_BOOTSTRAP.md
- The command enables TAC methodology documentation loading via agents
- Keep template simple - over-parameterization makes it fragile
- Rendered file in `.claude/commands/` serves as both example and test artifact
- Generated projects get static copies users can customize freely
- No new Python dependencies required
- Template should work with existing TAC Bootstrap infrastructure
