# Feature: Find and Summarize Command

## Metadata
issue_number: `456`
adw_id: `feature_Tac_12_task_4`
issue_json: `{"number":456,"title":"[Task 4/49] [FEATURE] Create find_and_summarize.md command file","body":"## Description\n\nCreate a command that searches for files and generates AI summaries.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/find_and_summarize.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`\n\n## Key Features\n- allowed-tools: Glob, Grep, Read\n- File discovery with patterns\n- AI-powered summarization\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/find_and_summarize.md`\n\n## Wave 1 - New Commands (Task 4 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_4"}`

## Feature Description

Create a `/find_and_summarize` command that enables users to discover files matching glob patterns and receive AI-generated summaries of their contents. This command provides a read-only exploration capability that helps users understand file purposes and relationships without manual inspection.

The command accepts a glob pattern to search for files, reads relevant matches, and produces a single comprehensive markdown summary highlighting key findings, file purposes, and relationships.

## User Story

As a developer working in a codebase
I want to find files matching a pattern and get an AI summary of what they contain
So that I can quickly understand the purpose and content of multiple files without reading each one individually

## Problem Statement

Developers often need to discover and understand groups of related files in a codebase. Manually finding files with glob patterns or grep, then reading each one individually is time-consuming. There is no efficient way to get a high-level overview of multiple files' purposes and relationships.

The existing `/scout` command provides comprehensive parallel exploration with multiple strategies and confidence scoring, which is powerful but heavyweight for simpler use cases where the user already knows the file pattern they want to examine.

## Solution Statement

Create a lightweight `/find_and_summarize` command that:
1. Accepts a glob pattern as input (e.g., `**/*.py`, `src/*/service.ts`)
2. Uses the Glob tool to find matching files
3. Reads relevant files (suggesting a limit of ~20 files to avoid token overuse)
4. Generates a single markdown summary with sections:
   - Files found (count and list)
   - Summary of contents (aggregate overview)
   - Key findings (important patterns, relationships, insights)

This provides a simpler, faster alternative to `/scout` for targeted file discovery and summarization.

## Relevant Files

Files necessary for implementing the feature:

### Base Repository Command File
- `.claude/commands/find_and_summarize.md` - The actual command file used in this repository
  - Currently does not exist, needs to be created
  - Will define the command's variables, instructions, workflow, and report structure
  - Should follow the same YAML frontmatter + markdown pattern as other commands

### Template File for CLI Generation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2` - Jinja2 template
  - Currently does not exist, needs to be created
  - Will be used by the CLI to generate the command file in target projects
  - Based on auto-resolved clarifications: no config variables needed (generic command)

### Service Registration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that builds scaffold plans
  - Lines 279-324: `commands` list where `find_and_summarize` needs to be added
  - Pattern: command name added to list, then loop creates file with template (lines 326-332)

### Reference Commands for Pattern
- `.claude/commands/scout.md` - Similar file discovery command, good structural reference
- `.claude/commands/tools.md` or other simple commands - Good for basic frontmatter pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2` - Template reference

### New Files
- `.claude/commands/find_and_summarize.md` - New base command file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2` - New template file

## Implementation Plan

### Phase 1: Foundation
1. Review existing command structure and patterns
   - Read `.claude/commands/scout.md` to understand comprehensive command structure
   - Read a simpler command (e.g., `.claude/commands/tools.md`) for basic frontmatter pattern
   - Read corresponding `.j2` templates to understand template conventions

2. Review scaffold service registration pattern
   - Read `scaffold_service.py` lines 279-332 to confirm command registration approach
   - Verify that simply adding "find_and_summarize" to the commands list is sufficient

### Phase 2: Core Implementation
1. Create base command file `.claude/commands/find_and_summarize.md`
   - Include YAML frontmatter with command metadata (name, allowed-tools, description)
   - Define Variables section (glob pattern as $1, optional focus area as $2)
   - Write Instructions section explaining purpose, when to use, when not to use
   - Write Workflow section with step-by-step execution logic
   - Write Report section defining output format
   - Include usage examples
   - Add notes on limitations and best practices

2. Create template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`
   - Copy structure from base command file
   - Since no config variables are needed (per auto-resolved clarifications), template should be nearly identical to base
   - Ensure Jinja2 syntax is valid (even if no variables are used)

### Phase 3: Integration
1. Update `scaffold_service.py` to register the command
   - Add "find_and_summarize" to the commands list (around line 298)
   - Verify the command gets included in scaffold plan generation

2. Validate integration
   - The command will be automatically processed by the existing loop (lines 326-332)
   - No additional code changes needed beyond adding to the list

## Step by Step Tasks

### Task 1: Create Base Command File
Create `.claude/commands/find_and_summarize.md` with complete structure:
- Add frontmatter with metadata (name, description, allowed-tools: [Glob, Grep, Read])
- Define Variables: PATTERN ($1 required), FOCUS ($2 optional)
- Write Instructions:
  - Purpose: Find files and generate AI summary
  - When to use: Quick targeted discovery of files by pattern
  - When NOT to use: Complex multi-strategy exploration (use /scout), single known file (use Read)
  - How it works: Glob → Read → Summarize
- Write Workflow:
  - Step 1: Validate PATTERN parameter
  - Step 2: Use Glob tool with PATTERN
  - Step 3: Handle no files found case (friendly message)
  - Step 4: Read first ~20 files (suggest limit in instructions, let agent decide)
  - Step 5: Generate markdown summary with sections:
    - Files Found (count and list)
    - Summary of Contents (aggregate overview based on FOCUS if provided)
    - Key Findings (patterns, relationships, insights)
- Write Report section defining output format
- Add Examples:
  - `/find_and_summarize "**/*.py"` - Find all Python files
  - `/find_and_summarize "src/**/service.ts" "focusing on authentication logic"` - With focus
  - `/find_and_summarize "*.md"` - Find markdown files in current directory
- Add Notes section:
  - Limitations (read-only, no execution, ~20 file suggested limit)
  - Best practices (be specific with patterns, use focus for targeted summaries)
  - Integration with other commands (use /scout for comprehensive exploration)

### Task 2: Create Jinja2 Template File
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`:
- Copy the entire content from `.claude/commands/find_and_summarize.md`
- Since no config variables are needed (per auto-resolved clarifications), the template is identical to the base file
- Validate Jinja2 syntax (ensure no accidental template syntax errors)

### Task 3: Update Scaffold Service Registration
Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`:
- Locate the `commands` list (around line 279)
- Add `"find_and_summarize"` to the list in alphabetical order (after "feature", before "generate_branch_name")
- No other changes needed - the existing loop at lines 326-332 will handle the rest

### Task 4: Validation
Execute validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run all unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Run linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Run type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test CLI

## Testing Strategy

### Unit Tests
No dedicated unit tests required for this task since:
- The command file is a markdown document (no executable code to test)
- The template is a Jinja2 file rendering markdown (no logic to test)
- The scaffold service already has tests for command registration pattern

### Edge Cases
Test the command manually after implementation:
1. Pattern with no matches: verify friendly "no files found" message
2. Pattern with many matches (>20 files): verify agent limits appropriately
3. Pattern with focus area: verify summary respects the focus
4. Invalid pattern: verify graceful error handling
5. Very large files: verify Read tool's existing 2000-line limit handles this

## Acceptance Criteria

1. ✅ Base command file `.claude/commands/find_and_summarize.md` exists and follows standard structure
   - Contains valid YAML frontmatter with name, description, allowed-tools
   - Defines PATTERN and FOCUS variables
   - Includes clear Instructions, Workflow, Report, Examples, and Notes sections
   - Follows patterns established by existing commands

2. ✅ Template file `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2` exists
   - Content matches base command file (no config variables needed)
   - Valid Jinja2 syntax

3. ✅ `scaffold_service.py` updated to register the command
   - "find_and_summarize" added to commands list
   - Alphabetically sorted

4. ✅ All validation commands pass with zero regressions
   - pytest passes
   - ruff check passes
   - mypy passes
   - CLI help displays correctly

5. ✅ Command is functionally correct when used
   - Accepts glob pattern as input
   - Finds files using Glob tool
   - Reads relevant files (respecting reasonable limits)
   - Generates markdown summary with required sections
   - Handles edge cases gracefully (no matches, many matches, large files)

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Relationship to /scout Command

The `/find_and_summarize` command is intentionally simpler and more lightweight than `/scout`:

**Use /scout when:**
- You need comprehensive multi-strategy exploration
- You want confidence scoring and frequency analysis
- You need to map dependencies, architecture, tests, configs, etc.
- You don't know exactly what you're looking for

**Use /find_and_summarize when:**
- You know the file pattern you want to examine
- You need a quick summary of a specific set of files
- You want a simpler, faster workflow
- You don't need parallel strategies or confidence scoring

### Design Decisions

1. **No config variables**: The command is generic and project-agnostic, so no Jinja2 config variables are needed
2. **Suggested ~20 file limit**: Mentioned in command description to guide agent, but not enforced - agent decides based on context
3. **Leverages existing tool limits**: Read tool already handles large files (2000 lines default), so no special handling needed
4. **Focus parameter optional**: Allows targeted summaries (e.g., "focusing on authentication") but works fine without it
5. **Markdown output**: Consistent with other commands, readable, structured

### Future Enhancements

Potential improvements for future iterations:
- Add optional max-files parameter to explicitly limit file count
- Support for excluding patterns (e.g., ignore test files)
- Option to save summary to a file vs. inline output
- Integration with /scout results (e.g., summarize high-confidence files)
- Support for sorting files by different criteria (name, size, modification time)
