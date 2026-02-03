# Feature: Meta-Agent Generator Command

## Metadata
issue_number: `576`
adw_id: `feature_Tac_13_Task_14`
issue_json: `{"number": 576, "title": "[TAC-13] Task 14: Create meta-agent generator", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_14\n```\n\n**Description:**\nCreate meta-agent generator as template and implementation - agents that create agents.\n\n**Technical Steps:**\n\n#### A) Create Jinja2 Template in CLI\n\n1. **Create template file**:\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`\n\n2. **Register in scaffold_service.py**:\n   ```python\n   # TAC-13: Meta-Agent Generator\n   plan.add_file(\n       action=\"create\",\n       template=\"claude/commands/meta-agent.md.j2\",\n       path=\".claude/commands/meta-agent.md\",\n       reason=\"Meta-agent generator - agents that create agents\"\n   )\n   ```\n\n#### B) Create Implementation File in Repo Root\n\n1. **Create meta-agent generator**:\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/meta-agent.md`\n\n   **Content includes**:\n   - Phase 1: Analyze user's agent description\n   - Phase 2: Determine tools, model, personality\n   - Phase 3: Generate agent following standard template\n   - Phase 4: Write to `.claude/agents/<name>.md`\n\n   **Enforces format**:\n   - YAML frontmatter (name, description, tools, model, color)\n   - Purpose, Instructions, Workflow, Report sections\n\n   **Variables**: `AGENT_DESCRIPTION: $ARGUMENTS`, `AGENT_OUTPUT_PATH: .claude/agents/<name>.md`\n\n**Acceptance Criteria:**\n- ✅ **Template (.j2)** created in CLI templates\n- ✅ **Template registered** in scaffold_service.py\n- ✅ **Implementation file** in repo root\n- ✅ Generates valid agent files\n- ✅ Output immediately usable\n- ✅ Includes personality and behavior patterns\n- ✅ Follows agent definition schema\n\n**Validation Commands:**\n```bash\n# Verify template\ntest -f /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo \"✓ Template\"\n\n# Verify registration\ngrep -A 3 \"meta-agent.md.j2\" /Users/hernandoescobar/Documents/Celes\n\n[TRUNCATED - body exceeds 2000 chars]"}`

## Feature Description

The meta-agent generator is a specialized slash command (`/meta-agent`) that automates the creation of new agent definition files. It functions as an "agent that creates agents," enabling developers to generate complete, production-ready agent files from natural language descriptions. This meta-agentic capability is a core building block for scaling the TAC Bootstrap agentic layer.

The feature follows the established dual-strategy pattern: creating both a Jinja2 template for the CLI generator and an implementation file in the repository root. Generated agents follow a strict schema with YAML frontmatter and structured sections, ensuring consistency and immediate usability.

## User Story

As a TAC Bootstrap developer
I want to invoke `/meta-agent "description of my agent"`
So that I can automatically generate complete agent definition files without manually writing boilerplate structure

## Problem Statement

Currently, creating new agent definitions requires:
1. Manually copying structure from existing agents
2. Understanding the full agent schema (YAML frontmatter, sections, formatting)
3. Ensuring consistency with existing patterns
4. Creating both the base `.md` file and the `.j2` template

This manual process is error-prone, time-consuming, and creates friction for extending the agentic layer. As TAC-13 focuses on meta-agentics (agents creating agents), we need a streamlined, automated approach to agent generation.

## Solution Statement

Implement a `/meta-agent` slash command that:
1. Accepts a natural language description of the desired agent
2. Intelligently infers required tools, model selection, and personality traits
3. Generates a complete agent definition following the standard schema
4. Validates structure before writing to disk
5. Handles edge cases (existing files, minimal descriptions, directory creation)
6. Outputs immediately usable agent files in `.claude/agents/`

The solution leverages AI inference to determine appropriate tools based on the agent's purpose, auto-generates kebab-case names from descriptions, and validates output against the schema. It follows TAC-1's philosophy of "moving up the stack" by automating repetitive engineering tasks.

## Relevant Files

Existing files for pattern reference:
- `.claude/commands/meta-prompt.md` - Sibling meta-command for generating prompts, provides structural pattern
- `.claude/agents/meta-agent.md` - Existing meta-agent implementation (to be replaced/enhanced)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-prompt.md.j2` - Template pattern reference
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Registration point for new command template

Reference agents for examples:
- `.claude/agents/scout-report-suggest.md` - Read-only analysis pattern
- `.claude/agents/build-agent.md` - File creation pattern
- `.claude/agents/docs-scraper.md` - Web content workflow pattern

### New Files

1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2` - Jinja2 template for CLI generation
2. `.claude/commands/meta-agent.md` - Implementation file in repository root

## Implementation Plan

### Phase 1: Foundation

1. **Study existing patterns**
   - Read `.claude/commands/meta-prompt.md` to understand meta-command structure
   - Review agent schema from `.claude/agents/*.md` files (YAML frontmatter + sections)
   - Analyze clarifications for edge case handling (overwrites, name generation, validation)

2. **Design agent specification**
   - Define YAML frontmatter structure: `allowed-tools`, `description`, `argument-hint`, `model`
   - Define Variables section: `AGENT_DESCRIPTION: $ARGUMENTS`
   - Design 4-phase workflow: analyze → determine → generate → write
   - Plan validation rules for generated agents

### Phase 2: Core Implementation

1. **Create implementation file** (`.claude/commands/meta-agent.md`)
   - Write YAML frontmatter with allowed-tools: Write, Read, Glob, Grep, AskUserQuestion
   - Document Variables section with AGENT_DESCRIPTION
   - Implement 4-phase Instructions:
     - **Phase 1**: Parse description, validate length (10+ chars), extract intent
     - **Phase 2**: Infer tools from purpose (mapping agent capabilities → Claude Code tools)
     - **Phase 3**: Generate agent following schema (YAML frontmatter + Purpose/Workflow/Instructions/Examples sections)
     - **Phase 4**: Check for existing file, create `.claude/agents/` if needed, write agent file
   - Define validation rules (YAML structure, required sections, no placeholders)
   - Include error handling guidance (vague descriptions, existing files, invalid tools)
   - Add Report section specifying output format

2. **Create template file** (`.j2` version)
   - Copy implementation content
   - Replace project-specific references with `{{ config.project.name }}`
   - Maintain identical structure to `.md` file
   - Keep minimal templating (most content is static)

### Phase 3: Integration

1. **Register in scaffold_service.py**
   - Add `"meta-agent"` to commands list (after `"meta-prompt"` around line 343)
   - Verify registration uses correct action (`"create"` or `"skip_if_exists"`)

2. **Update existing meta-agent file** (if needed)
   - Compare new implementation with `.claude/agents/meta-agent.md`
   - Note: The existing file is an agent definition, not a command - they serve different purposes
   - Ensure naming doesn't conflict (`.claude/commands/meta-agent.md` vs `.claude/agents/meta-agent.md`)

## Step by Step Tasks

### Task 1: Analyze Existing Patterns
- Read `.claude/commands/meta-prompt.md` to understand meta-command structure
- Review 3-5 agent files from `.claude/agents/` to extract schema patterns
- Document YAML frontmatter fields: name, description, tools, model, color
- Document required sections: Purpose, Workflow, Instructions, Examples
- Note validation requirements from auto-resolved clarifications

### Task 2: Create Implementation File
- Write `.claude/commands/meta-agent.md` following meta-prompt pattern
- Include YAML frontmatter:
  ```yaml
  allowed-tools:
    - Write
    - Read
    - Glob
    - Grep
    - AskUserQuestion
  description: "Generate new agent definitions from natural language descriptions"
  argument-hint: "[agent_description]"
  model: sonnet
  ```
- Define Variables section: `AGENT_DESCRIPTION: $ARGUMENTS`
- Implement Instructions with 4 phases:
  1. **Parse & Validate**: Check description length, extract purpose
  2. **Infer Configuration**: Map description to tools/model/personality
  3. **Generate Schema**: Create YAML frontmatter + Purpose/Workflow/Instructions/Examples
  4. **Write & Validate**: Check existing files, create directories, write agent
- Include validation checklist (YAML structure, required sections, no TODOs)
- Document error handling (vague input, conflicts, invalid tools)
- Define Report format (success confirmation, file paths, usage instructions)

### Task 3: Create Jinja2 Template
- Copy `.claude/commands/meta-agent.md` to `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`
- Replace hardcoded references:
  - "TAC Bootstrap" → `{{ config.project.name }}`
  - ".claude/agents/" → keep as-is (structural path)
- Maintain identical structure and formatting
- Verify template variables are minimal (most content is static)

### Task 4: Register in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list (around line 343, after "meta-prompt")
- Add `"meta-agent"` to the list
- Verify the registration loop will create the file with correct action
- Save file

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo "✓ Template exists"`
- `grep -A 3 "meta-agent" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep -E "(meta-agent|template|reason)" && echo "✓ Registration found"`
- `test -f .claude/commands/meta-agent.md && echo "✓ Implementation exists"`
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check

### Task 6: Manual Smoke Test
- Test the command pattern: `/meta-agent "create a test-runner agent that runs pytest and reports failures"`
- Verify it follows the workflow phases
- Check generated output matches schema expectations
- Confirm error handling works for edge cases

## Testing Strategy

### Unit Tests

No additional unit tests required beyond existing scaffold_service.py tests, which validate:
- Template registration in plan building
- File creation with correct paths
- Action types (create vs skip_if_exists)

The command itself is a prompt-based tool, tested through manual invocation.

### Manual Testing Scenarios

1. **Minimal description**: `/meta-agent "docs updater"` - should ask clarifying questions
2. **Complete description**: `/meta-agent "create a test-runner agent that executes pytest tests, parses failures, and reports results. Needs Bash and Read tools."`
3. **Existing agent conflict**: Try creating agent that already exists - should prompt for confirmation
4. **Missing directory**: Ensure `.claude/agents/` is created if missing
5. **Invalid description**: Test with < 10 chars - should reject with helpful error

### Edge Cases

1. **Empty description**: Reject with minimum length requirement
2. **Agent name collision**: Prompt user for overwrite/rename/abort
3. **Invalid tool requested**: Suggest valid alternatives from Claude Code toolkit
4. **Vague description**: Use AskUserQuestion to clarify purpose and tools
5. **Directory doesn't exist**: Auto-create `.claude/agents/` with informative message

## Acceptance Criteria

- ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2`
- ✅ Template is registered in `scaffold_service.py` commands list
- ✅ Implementation file exists at `.claude/commands/meta-agent.md`
- ✅ Command follows 4-phase workflow: parse → infer → generate → write
- ✅ Generated agents include YAML frontmatter with all required fields
- ✅ Generated agents include Purpose, Workflow, Instructions, Examples sections
- ✅ Validation prevents writing agents with placeholders or incomplete structure
- ✅ Error handling covers: minimal descriptions, existing files, invalid tools, missing directories
- ✅ Auto-generates kebab-case names from descriptions
- ✅ Infers tools based on agent purpose using AI reasoning
- ✅ Output is immediately usable (no manual editing required)
- ✅ Personality and behavior patterns are inferred from agent purpose

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/meta-agent.md.j2 && echo "✓ Template"

# Verify registration in scaffold_service.py
grep -A 3 "meta-agent" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep -E "(meta-agent|template|reason)" && echo "✓ Registration"

# Verify implementation exists
test -f .claude/commands/meta-agent.md && echo "✓ Implementation"

# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Run linting
cd tac_bootstrap_cli && uv run ruff check .

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Verify command structure (YAML frontmatter, Variables, Instructions, Report)
grep -E "^(allowed-tools:|description:|argument-hint:|Variables|Instructions|Report)" .claude/commands/meta-agent.md && echo "✓ Structure"
```

## Notes

### Design Decisions

1. **Agent vs Command naming**: The `.claude/agents/meta-agent.md` file is an agent definition (used with `@meta-agent`), while `.claude/commands/meta-agent.md` is a slash command (used with `/meta-agent`). Both can coexist and serve different purposes.

2. **Tool inference**: The command uses AI reasoning to map agent descriptions to appropriate tools. For example:
   - "runs tests" → Bash tool
   - "updates files" → Edit, Read tools
   - "searches code" → Grep, Glob tools
   - "asks questions" → AskUserQuestion tool

3. **Name generation**: Auto-generates kebab-case names from descriptions with option to override via clarification questions if needed.

4. **Validation strictness**: Validates structure (YAML, sections) but not content quality - allows flexibility while preventing broken files.

5. **Directory creation**: Auto-creates `.claude/agents/` following "principle of least surprise" - users expect it to work without manual setup.

### Auto-Resolved Clarifications Applied

- Agent names auto-generated from descriptions using kebab-case
- Creates `.claude/agents/` directory automatically if needed
- AI inference determines tool selection based on purpose
- Validates YAML frontmatter and required sections (Purpose, Instructions, Workflow)
- Prompts before overwriting existing agents
- Requires minimum description quality (10+ chars) with helpful errors
- Generated agents follow YAML frontmatter + 4-section structure
- Immediately usable output, not auto-activated (requires user testing)
- Personality inferred from purpose (e.g., security → thorough/cautious)
- Fixed output path: `.claude/agents/<name>.md` (standardization)

### Future Enhancements

- Integration with scaffold_service.py to auto-register generated agents
- Support for agent variants/versioning (e.g., "agent-v2")
- Agent templates library for common patterns (CRUD, API client, validator)
- Agent composition (combining multiple agent patterns)
- Interactive wizard mode for agent generation

### Dependencies

No new dependencies required. Uses existing tools:
- Write, Read - File operations
- Glob, Grep - File discovery and search
- AskUserQuestion - User interaction for clarifications
