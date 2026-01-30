# Feature: Load AI Documentation Command

## Metadata
issue_number: `462`
adw_id: `feature_Tac_12_task_10_2`
issue_json: `{"number":462,"title":"[Task 10/49] [FEATURE] Create load_ai_docs.md command file","body":"## Description\n\nCreate a command that loads AI documentation files into context.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_ai_docs.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`\n\n## Key Features\n- Loads documentation from ai_docs/ or similar\n- Context preparation for planning\n- allowed-tools: Read, Glob, Grep\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`\n\n## Wave 1 - New Commands (Task 10 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_10_2"}`

## Feature Description

Create a `/load_ai_docs` command that loads AI documentation files from the `ai_docs/doc/` directory into the agent's context using specialized exploration agents. This command efficiently ingests TAC methodology documentation (courses 1-8), project-specific AI patterns, and guidelines to help agents understand the project's AI development approach.

The command supports:
- Loading all documentation or filtering by document numbers
- Flexible filtering syntax (single doc, ranges, multiple ranges)
- Graceful handling of missing directories
- Summary reporting of loaded content

## User Story

As a developer using TAC Bootstrap
I want to load AI documentation into the agent's context before planning
So that the agent has access to TAC methodology, patterns, and project-specific guidelines when creating implementation plans

## Problem Statement

Agents working on TAC Bootstrap projects need access to AI methodology documentation to make informed decisions about:
- Architecture patterns following TAC principles
- Workflow patterns (ADW, SDLC, etc.)
- Testing strategies and best practices
- Project-specific AI development guidelines

Currently, agents must be manually directed to read specific documentation files, which is:
- Time-consuming (manually specifying each file)
- Error-prone (easy to miss relevant documentation)
- Inconsistent (different agents load different subsets)
- Not optimized for large documentation sets

## Solution Statement

Create a `/load_ai_docs` command that:
- Accepts optional filtering parameter (e.g., "1-3", "5", "1-3,5,7-8")
- Uses Task tool with Explore agent for efficient documentation scanning
- Loads documentation from configurable `ai_docs/doc/` directory
- Provides clear summary of loaded documents and key topics
- Gracefully handles missing directories with helpful error messages
- Follows patterns established in existing documentation loading commands

The implementation will:
- Use hardcoded path `ai_docs/doc/` in base repository
- Use configurable path `{{ config.ai_docs_path | default('ai_docs/doc') }}` in Jinja2 template
- Launch Explore agent with "medium" thoroughness for balanced scanning
- Report loaded files, key topics, and any missing documents
- Already registered in `scaffold_service.py` at line 320

**Reference Implementation:**
- `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md` - Complete working implementation

## Relevant Files

### Existing Files to Modify

1. **`tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`** (line 320)
   - Command already registered as `"load_ai_docs"` in commands list
   - No modification needed (validation check only)

### Existing Files - No Changes Required

2. **`.claude/commands/load_ai_docs.md`** (156 lines)
   - Base command file already exists with complete implementation
   - Uses Explore agent with filtering support
   - Needs review to ensure it matches requirements

3. **`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`** (156 lines)
   - Jinja2 template already exists
   - Needs review to ensure proper variable usage

### Reference Files

4. **`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`**
   - Reference implementation to compare against
   - May contain improvements or different patterns

## Implementation Plan

### Phase 1: Analysis and Comparison
- Read existing base command file `.claude/commands/load_ai_docs.md`
- Read existing Jinja2 template file
- Read reference implementation from TAC-12
- Compare implementations to identify differences
- Determine if updates are needed to match reference

### Phase 2: Update Base Command (if needed)
- Update `.claude/commands/load_ai_docs.md` to match reference patterns
- Ensure filtering syntax is correct (single, range, multiple ranges)
- Verify Explore agent usage with proper parameters
- Ensure error handling for missing directories
- Verify report format includes loaded docs, key topics, and missing docs

### Phase 3: Update Template (if needed)
- Update Jinja2 template to use configurable paths
- Ensure `{{ config.ai_docs_path | default('ai_docs/doc') }}` variable usage
- Preserve all workflow logic from base file
- Maintain hardcoded Explore agent type and thoroughness level

### Phase 4: Validation
- Verify command registration in `scaffold_service.py`
- Test base command in current repository
- Validate template syntax and rendering
- Run all validation commands

## Step by Step Tasks

### Task 1: Analyze Existing Implementations
- Read `.claude/commands/load_ai_docs.md` (current base implementation)
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` (current template)
- Read `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md` (reference implementation)
- Document differences between current and reference implementations
- Identify which version has the correct patterns

### Task 2: Determine Update Requirements
- Compare filtering syntax implementations
- Compare Explore agent usage patterns
- Compare error handling approaches
- Compare report formats
- Create list of specific changes needed (if any)

### Task 3: Update Base Command File (if needed)
- If differences found, update `.claude/commands/load_ai_docs.md`:
  - Ensure frontmatter includes correct allowed-tools (Task, Read, Glob)
  - Implement Variables section: `doc_filter: $ARGUMENT (optional)`
  - Implement filtering syntax:
    - No filter: load all documents
    - Single doc: `doc_filter=5` loads only doc/5.md
    - Range: `doc_filter=1-3` loads 1, 2, 3
    - Multiple ranges: `doc_filter=1-3,5,7-8` loads 1, 2, 3, 5, 7, 8
  - Use Task tool with `subagent_type=Explore` and `thoroughness=medium`
  - Handle missing directory gracefully with informative error
  - Report loaded files, key topics, and missing documents

### Task 4: Update Jinja2 Template (if needed)
- If differences found, update template to match base command
- Ensure path uses: `{{ config.ai_docs_path | default('ai_docs/doc') }}`
- Preserve all workflow logic from base file
- Maintain Explore agent configuration (type and thoroughness hardcoded)

### Task 5: Verify Scaffold Service Registration
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate line 320 in commands list
- Verify `"load_ai_docs"` is present in the list
- Confirm no changes needed (validation only)

### Task 6: Test Base Command
- Test command with no filter: `/load_ai_docs`
- Test command with single doc: `/load_ai_docs doc_filter=5`
- Test command with range: `/load_ai_docs doc_filter=1-3`
- Test command with multiple ranges: `/load_ai_docs doc_filter=1-2,5,7-8`
- Verify Explore agent launches correctly
- Verify output includes loaded files and key topics
- Test with missing directory to verify error handling

### Task 7: Run All Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- Verify zero regressions

## Testing Strategy

### Functional Tests
- Test loading all documentation (no filter)
- Test single document filter (e.g., "5")
- Test range filter (e.g., "1-3")
- Test multiple ranges filter (e.g., "1-3,5,7-8")
- Test missing directory handling
- Test empty directory handling

### Integration Tests
- Verify Explore agent receives correct prompt
- Verify thoroughness level is "medium"
- Verify agent output includes file summaries
- Verify error messages are clear and actionable

### Template Tests
- Verify template syntax is valid Jinja2
- Verify config variables render correctly
- Verify template output matches base command structure

### Edge Cases
- Non-existent ai_docs directory
- Empty ai_docs directory
- Invalid filter syntax (should fail gracefully)
- Filter requesting non-existent docs (should report missing)
- Very large documentation set (trust context window management)

## Acceptance Criteria

1. Base command file `.claude/commands/load_ai_docs.md` exists and matches reference patterns
2. Jinja2 template exists with proper variable configuration for paths
3. Command is registered in `scaffold_service.py` commands list (line 320)
4. Command supports optional filtering with syntax: single, range, multiple ranges
5. Command uses Task tool with `subagent_type=Explore` and `thoroughness=medium`
6. Command handles missing directories gracefully with clear error messages
7. Command reports:
   - Documentation path used
   - Filter applied (if any)
   - List of loaded files
   - Key topics identified
   - Missing documents (if any)
8. All validation commands pass with zero failures
9. Template uses `{{ config.ai_docs_path | default('ai_docs/doc') }}` for configurable path
10. Workflow logic is identical between base file and template

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Implementation Notes
- The command already exists in both base and template form
- Main task is to verify implementation matches reference patterns
- May need updates to align with reference implementation from TAC-12
- Command is already registered in scaffold_service.py (no changes needed)

### Design Decisions
- Uses hardcoded path `ai_docs/doc/` in base repository (TAC Bootstrap standard)
- Uses configurable path in template for flexibility across projects
- No size limits initially (trust LLM context window management)
- No custom paths in initial version (YAGNI principle)
- Filtering is optional (load all by default for comprehensive context)
- Explore agent with "medium" thoroughness balances speed and coverage

### Future Enhancements (Out of Scope)
- Support for custom documentation paths via user parameters
- Caching of loaded documentation for faster subsequent loads
- Document metadata extraction (author, date, version)
- Progress indicators during large documentation loads
- Incremental loading for very large documentation sets
- Integration with documentation versioning systems

### Reference Pattern Notes
The reference implementation from `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md` should be considered the canonical pattern for:
- Filtering syntax parsing
- Explore agent invocation
- Error message formatting
- Report structure and content
- Progress indicators
