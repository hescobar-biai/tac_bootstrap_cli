# Feature: Create prime_cc.md Command File

## Metadata
issue_number: `465`
adw_id: `feature_Tac_12_task_13`
issue_json: `{"number":465,"title":"[Task 13/49] [FEATURE] Create prime_cc.md command file","body":"## Description\n\nCreate a specialized prime command for Claude Code codebase understanding.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/prime_cc.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`\n\n## Key Features\n- Specialized for Claude Code projects\n- Deep understanding of CC patterns\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/prime_cc.md`\n\n## Wave 1 - New Commands (Task 13 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_13"}`

## Feature Description
Create a specialized `/prime_cc` command that provides comprehensive understanding of Claude Code project structure, patterns, and configuration. This command extends the general `/prime` command with Claude Code-specific context loading including:
- Claude Code commands, hooks, agents, and output styles
- ADW workflows and automation patterns
- Tool usage preferences (Read, Edit, Bash, Grep, Glob)
- Project-specific Claude Code configuration
- Session recovery and context bundling mechanisms

The command will help Claude Code agents quickly gain deep understanding of the agentic layer architecture and available automation capabilities.

## User Story
As a Claude Code agent
I want to execute `/prime_cc` command
So that I can understand both general project context AND Claude Code-specific configuration, commands, hooks, and workflows in a single comprehensive context load

## Problem Statement
When Claude Code agents start working on a project, they need to understand:
1. General project context (README, config, architecture)
2. Available Claude Code slash commands and their purposes
3. Automation hooks and when they trigger
4. Output formatting styles and conventions
5. ADW workflows available for task automation
6. Tool usage best practices for Claude Code

Currently, agents must manually discover these by exploring `.claude/` directories or may miss important Claude Code patterns. This leads to inefficient tool usage and missed automation opportunities.

## Solution Statement
Create a specialized `/prime_cc` command that:
1. First executes the general `/prime` command for project context
2. Then loads Claude Code-specific configuration files systematically
3. Reports comprehensive understanding of both project and Claude Code setup
4. Provides clear examples of tool usage patterns and workflow commands

The command will use minimal Jinja2 templating (project name, description, paths) while keeping most content static for consistency. It will be included in all generated projects by default since it's self-documenting and valuable for Claude Code projects.

## Relevant Files
Files needed to implement this feature:

### Existing Files to Reference
- `.claude/commands/prime_cc.md` - Already exists in base repository (248 lines)
  - Contains complete command structure and examples
  - Will serve as reference for template creation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` - Already exists (282 lines)
  - Template version with Jinja2 variables
  - Uses `config.project.name`, `config.paths.*`, `config.commands.*`
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that builds scaffold plans
  - Contains list of commands in `_add_claude_files()` method (line 319)
  - Already includes `prime_cc` in commands list (line 319)
- `.claude/commands/prime.md` - General prime command for reference
  - Shows structure for context loading commands
- `.claude/settings.json` - Claude Code configuration
  - Shows permissions, hooks, and settings structure
- `CLAUDE.md` - Project guide for agents
  - Documents available commands and workflows

### New Files
None - all required files already exist! The `prime_cc` command is already implemented in both:
- Base repository: `.claude/commands/prime_cc.md`
- Template repository: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2`
- Service integration: Already listed in `scaffold_service.py` line 319

## Implementation Plan

### Phase 1: Verification
Verify that all files exist and are properly integrated.

### Phase 2: Testing
Test the command in a generated project to ensure it works correctly.

### Phase 3: Documentation
Update documentation to reference the new command.

## Step by Step Tasks

### Task 1: Verify Base Command File Exists
- Confirm `.claude/commands/prime_cc.md` exists in base repository
- Review content for completeness and accuracy
- Verify command follows standard format with Run, Read, Report sections
- Check that examples demonstrate Claude Code-specific patterns

### Task 2: Verify Template File Exists
- Confirm `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` exists
- Review Jinja2 template variables used:
  - `{{ config.project.name }}`
  - `{{ config.project.language }}`
  - `{{ config.project.architecture }}`
  - `{{ config.project.package_manager }}`
  - `{{ config.paths.adws_dir }}`
  - `{{ config.paths.scripts_dir }}`
  - `{{ config.paths.specs_dir }}`
  - `{{ config.commands.start }}`
  - `{{ config.commands.test }}`
  - `{{ config.commands.lint }}`
  - `{{ config.commands.build }}`
- Verify conditional sections use `{% if config.paths.adws_dir %}` pattern
- Ensure template maintains same structure as base file

### Task 3: Verify Scaffold Service Integration
- Confirm `scaffold_service.py` includes `prime_cc` in commands list
- Verify it's in the correct position in the list (line 319)
- Check that template file path matches expected pattern: `claude/commands/prime_cc.md.j2`
- Ensure action is set to `FileAction.CREATE` (only creates if not exists)

### Task 4: Test Command in Base Repository
- Execute `/prime_cc` command in this repository
- Verify it:
  - First runs `/prime` for general context
  - Then reads `.claude/commands/**` files
  - Reads `.claude/settings.json`
  - Reads automation hooks
  - Provides comprehensive report with project summary, commands, hooks, workflows

### Task 5: Test Template Generation
- Run validation commands to ensure CLI works correctly
- Verify template can be rendered with sample configuration
- Check that generated output matches expected format

### Task 6: Update Documentation References
- Verify CLAUDE.md mentions `/prime_cc` command in available commands list
- Ensure command is documented with purpose: "Claude Code-optimized context"
- Check that prime.md references prime_cc as available alternative

### Task 7: Run Full Validation Suite
- Execute all validation commands to ensure no regressions
- Verify tests pass
- Check linting passes
- Confirm type checking passes

## Testing Strategy

### Unit Tests
No new unit tests required - command files are templates and don't require logic tests.

### Integration Tests
- Test that base command file loads correctly when executed
- Verify template renders correctly with various config inputs
- Confirm scaffold service includes file in generated projects

### Edge Cases
- Empty or minimal project configuration - template should handle gracefully
- Missing optional paths (adws_dir, scripts_dir) - conditionals should work
- Project without ADW workflows - should omit ADW sections

### Manual Testing
1. Execute `/prime_cc` in base repository
2. Verify comprehensive output covers all sections
3. Confirm tool usage patterns are clear
4. Check that examples are helpful and accurate

## Acceptance Criteria
- [ ] `.claude/commands/prime_cc.md` exists in base repository with complete content
- [ ] `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` exists with proper Jinja2 templating
- [ ] `scaffold_service.py` includes `prime_cc` in commands list
- [ ] `/prime_cc` command executes successfully in base repository
- [ ] Command provides comprehensive report covering:
  - Project configuration summary
  - Available slash commands count and list
  - Claude Code permissions and settings
  - Automation hooks and purposes
  - ADW workflows (if applicable)
  - CLI development commands
  - Tool usage best practices
- [ ] Template uses minimal templating (only project-specific values)
- [ ] Command includes clear examples of usage patterns
- [ ] Documentation references the new command
- [ ] All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# All files exist verification
ls -la .claude/commands/prime_cc.md
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2

# Test the command in base repository
cat .claude/commands/prime_cc.md

# Run CLI tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes
**IMPORTANT DISCOVERY:** All required files already exist!

After investigation, I discovered that:
1. `.claude/commands/prime_cc.md` is already implemented (248 lines)
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_cc.md.j2` is already implemented (282 lines)
3. `scaffold_service.py` already includes `prime_cc` in the commands list at line 319

This task appears to already be complete. The implementation plan focuses on verification and testing rather than creation. The files were likely created in a previous task or as part of TAC-12 integration work.

The command provides comprehensive Claude Code context loading including:
- Project configuration (name, language, architecture, package manager)
- Available slash commands discovery
- Claude Code settings and permissions
- Automation hooks and their purposes
- ADW workflows (conditionally included)
- CLI development commands (start, test, lint, build, typecheck)
- Tool usage patterns and best practices
- Examples of command usage

The template uses Jinja2 variables appropriately for project-specific values while keeping most content static for consistency across all generated projects.
