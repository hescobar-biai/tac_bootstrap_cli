# Feature: Add prime_cc.md.j2 Command Template

## Metadata
issue_number: `263`
adw_id: `feature_Tac_9_task_22`
issue_json: `{"number":263,"title":"Add prime_cc.md.j2 command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_22\n\n**Description:**\nCreate Jinja2 template for `/prime_cc` slash command. Provides Claude Code-specific context priming.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/prime_cc.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_cc.md` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for the `/prime_cc` slash command that provides Claude Code-specific context priming. This command will help Claude Code agents quickly understand a project's structure, tools, workflows, and conventions with a focus on CLI-based development patterns unique to Claude Code.

The template will build upon the existing `/prime` command pattern while adding Claude Code-specific optimizations around tool usage (Read, Edit, Bash, Grep, Glob), terminal-based workflows, and repository navigation shortcuts.

## User Story
As a developer using Claude Code CLI
I want a `/prime_cc` command that provides Claude Code-optimized context
So that the agent understands my project structure, CLI workflows, and available tools effectively

## Problem Statement
Claude Code operates in a CLI environment with specific tools and interaction patterns that differ from web-based Claude. Currently, there's no dedicated command that primes the agent with both project context AND Claude Code-specific workflow optimizations. The generic `/prime` command doesn't emphasize CLI workflows, tool usage patterns, or terminal-based development practices.

Developers need a way to quickly onboard Claude Code agents to their projects with context that's optimized for CLI-based agentic development.

## Solution Statement
Create a `prime_cc.md.j2` Jinja2 template that:
1. Builds on the proven structure from the source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/prime_cc.md`
2. Parameterizes project-specific values using Jinja2 variables (project name, commands, paths)
3. Keeps Claude Code-specific instructions static and universal
4. Follows the same pattern as `load_ai_docs.md.j2` for consistency
5. Generates a rendered version for tac_bootstrap itself as validation

The template will include sections for:
- Running initial discovery commands
- Reading key project files
- Understanding repository structure
- Learning CLI workflows and tools
- Reporting project understanding

## Relevant Files

### Existing Reference Files
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/prime_cc.md` - Source reference file (if accessible)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` - Pattern reference for template structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Existing prime command template
- `.claude/commands/prime.md` - Current prime command (rendered)
- `config.yml` - Configuration values for parameterization

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Jinja2 template (CREATE)
- `.claude/commands/prime_cc.md` - Rendered command for tac_bootstrap (CREATE)

## Implementation Plan

### Phase 1: Foundation
1. Read source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/prime_cc.md` if accessible
2. Study `load_ai_docs.md.j2` template pattern for Jinja2 structure
3. Review `prime.md` to understand existing priming approach
4. Identify project-specific values to parameterize from config.yml

### Phase 2: Core Implementation
1. Create `prime_cc.md.j2` template with:
   - Frontmatter with description
   - Run section with discovery commands
   - Read section listing key files
   - Understand section with project context
   - Report section for agent output
2. Parameterize dynamic values:
   - `{{ config.project.name }}`
   - `{{ config.project.description }}`
   - `{{ config.commands.* }}`
   - `{{ config.paths.* }}`
3. Keep static content for Claude Code best practices

### Phase 3: Integration
1. Render template using tac_bootstrap's config.yml
2. Create `.claude/commands/prime_cc.md` as validation
3. Verify template renders without errors
4. Validate markdown formatting in rendered output

## Step by Step Tasks

### Task 1: Analyze Source and References
- Attempt to read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/prime_cc.md`
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` for template pattern
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` for priming approach
- Read `config.yml` to identify available configuration variables
- Document key insights and parameterization strategy

### Task 2: Create prime_cc.md.j2 Template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`
- Add frontmatter with description: "Gain a general understanding of the codebase with a focus on Claude Code improvements"
- Implement Run section:
  - Execute `/prime` command first
  - Read additional Claude Code-specific files
- Implement Read section:
  - `.claude/commands/**` - All available commands
  - `.claude/output-styles/**` - Output formatting styles
  - `.claude/hooks/` - Automation hooks
  - `.claude/settings.json` - Permissions and configuration
- Implement Report section:
  - Summary of project structure
  - Available Claude Code commands
  - CLI workflows and tools
  - Key files and patterns

### Task 3: Parameterize Dynamic Values
- Replace hardcoded project name with `{{ config.project.name }}`
- Use `{{ config.paths.* }}` for directory references
- Use `{{ config.commands.* }}` for command references
- Keep Claude Code-specific instructions static

### Task 4: Render Template for tac_bootstrap
- Load `config.yml` configuration
- Render `prime_cc.md.j2` with tac_bootstrap config
- Write output to `.claude/commands/prime_cc.md`
- Verify file is created and well-formatted

### Task 5: Validation
- Verify template renders without Jinja2 errors
- Check rendered markdown has valid syntax
- Ensure all sections are present (Run, Read, Report)
- Validate parameterized values are correctly substituted
- Run validation commands (see below)

## Testing Strategy

### Unit Tests
No unit tests required for this feature (template-only change). Validation is done through:
1. Template rendering without errors
2. Manual review of rendered output
3. Markdown syntax validation

### Edge Cases
1. **Source file inaccessible**: Create template based on `/prime` pattern + Claude Code optimizations
2. **Missing config values**: Use sensible defaults or empty strings
3. **Invalid Jinja2 syntax**: Validate template renders successfully
4. **Markdown formatting issues**: Ensure proper section headers and code blocks

## Acceptance Criteria
1. ✅ Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`
2. ✅ Template follows same structure as `load_ai_docs.md.j2`
3. ✅ Template includes frontmatter, Run, Read, and Report sections
4. ✅ Project-specific values are parameterized with Jinja2 variables
5. ✅ Claude Code-specific instructions remain static
6. ✅ Rendered file created at `.claude/commands/prime_cc.md`
7. ✅ Rendered output is valid markdown
8. ✅ Template renders without Jinja2 errors
9. ✅ All validation commands pass

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Configuration Variables Used
Based on `config.yml`:
- `config.project.name` - "tac-bootstrap"
- `config.project.description` - (if available)
- `config.paths.app_root` - "tac_bootstrap_cli"
- `config.paths.agentic_root` - "."
- `config.paths.adws_dir` - "adws"
- `config.paths.specs_dir` - "specs"
- `config.commands.start` - "uv run tac-bootstrap --help"
- `config.commands.test` - "uv run pytest"

### Claude Code-Specific Optimizations
The template should emphasize:
1. **Tool Usage**: Read, Edit, Bash, Grep, Glob over other approaches
2. **CLI Workflows**: Terminal-based development patterns
3. **File Navigation**: Quick access to `.claude/` configuration
4. **Command Discovery**: Understanding available slash commands
5. **Hook System**: Awareness of automation triggers

### Template Consistency
Follow patterns from `load_ai_docs.md.j2`:
- Clear section headers (## Variables, ## Instructions, ## Run, ## Examples, ## Report)
- Detailed explanations in Instructions section
- Multiple examples showing common usage patterns
- Structured Report format with bullet points

### Future Enhancements
- Add support for project-type specific priming (web app vs CLI vs library)
- Include detection of testing frameworks and CI/CD setup
- Auto-discover project conventions from existing code
