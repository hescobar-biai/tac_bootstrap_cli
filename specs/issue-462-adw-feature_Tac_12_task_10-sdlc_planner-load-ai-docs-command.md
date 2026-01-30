# Feature: Create load_ai_docs.md Command Template

## Metadata
issue_number: `462`
adw_id: `feature_Tac_12_task_10`
issue_json: `{"number":462,"title":"[Task 10/49] [FEATURE] Create load_ai_docs.md command file","body":"## Description\n\nCreate a command that loads AI documentation files into context.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_ai_docs.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`\n\n## Key Features\n- Loads documentation from ai_docs/ or similar\n- Context preparation for planning\n- allowed-tools: Read, Glob, Grep\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_ai_docs.md`\n\n## Wave 1 - New Commands (Task 10 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_10"}`

## Feature Description

The load_ai_docs command enables AI agents to efficiently load TAC methodology documentation and project-specific AI patterns into context. This is a critical command for preparing agents to work within the TAC framework, as it allows them to understand the AI development methodology, workflows, and best practices documented in the `ai_docs/doc/` directory.

The command uses the Explore agent to scan documentation files with support for flexible filtering (single docs, ranges, multiple ranges). It provides structured reporting of loaded content and handles edge cases like missing directories gracefully.

## User Story

As a TAC project developer
I want to load AI documentation into agent context with a single command
So that agents can reference TAC methodology and project patterns when planning and implementing features

## Problem Statement

TAC projects contain essential AI development documentation in the `ai_docs/doc/` directory (typically 8 numbered TAC course files plus custom documentation). Currently, there is no standardized command to efficiently load this documentation into agent context. Developers must manually ask agents to read documentation files, which is inefficient and error-prone. The documentation can be large, so naive reading approaches may exceed context limits.

Without this command:
- Documentation loading is inconsistent across projects
- Agents may not have access to critical TAC methodology
- Manual file-by-file loading wastes time
- No filtering support for selective documentation loading

## Solution Statement

Create a dedicated `/load_ai_docs` command that:
- Uses the Explore agent for efficient documentation scanning
- Supports flexible filtering syntax (single docs, ranges, multiple ranges)
- Provides clear reporting of loaded content
- Handles missing directories gracefully
- Works consistently across all TAC projects using standard `ai_docs/doc/` path

The template will be a static copy of the base command file (no Jinja2 variables) since the command uses TAC-standard paths that are consistent across all projects.

## Relevant Files

### Existing Files
- `.claude/commands/load_ai_docs.md` - Base command file (already complete)
  - Contains full implementation with Variables, Instructions, Run, Examples, Report sections
  - Uses fixed path `ai_docs/doc/` for TAC standard convention
  - Implements comprehensive filtering syntax

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2` - Template file (already exists, verified complete)
  - Static copy of base file with no Jinja2 variables
  - Follows pattern of commands that use standard TAC paths

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:317` - Service that generates commands
  - Command already registered in commands list
  - Will automatically generate file when scaffold runs

### New Files
None. All required files already exist.

## Implementation Plan

### Phase 1: Verification
Verify that all components are in place and correct:
- Base command file exists with complete implementation
- Template file exists and matches base file (static copy, no variables)
- scaffold_service.py includes load_ai_docs in commands list

### Phase 2: Validation
Validate the implementation meets all requirements:
- Template has no Jinja2 variables (static content)
- Base file includes all required sections
- Filtering syntax is documented and examples provided
- Error handling for missing directories is present
- Reporting format is well-defined

### Phase 3: Testing
Test the command through the CLI generation process:
- Run CLI to generate a test project
- Verify load_ai_docs.md is generated correctly
- Confirm content matches base file exactly
- Test in actual usage scenario if possible

## Step by Step Tasks

### Task 1: Verify Base Command File
- Read `.claude/commands/load_ai_docs.md`
- Confirm all sections present: Variables, Instructions, Run, Examples, Report
- Verify filtering syntax documentation is complete
- Verify error handling examples are present
- Confirm uses standard path `ai_docs/doc/`

### Task 2: Verify Template File
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`
- Confirm it's a static copy of base file (no Jinja2 variables)
- Verify content matches base file exactly
- Confirm no `{{ }}` template syntax present

### Task 3: Verify Scaffold Service Registration
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Confirm 'load_ai_docs' is in commands list
- Verify it's in correct position (TAC-9/10 section)
- Confirm no additional changes needed

### Task 4: Compare with Similar Commands
- Read another static template (e.g., `conditional_docs.md.j2` or `scout.md.j2`)
- Compare structure and approach
- Verify load_ai_docs follows same pattern

### Task 5: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required since this is template/configuration work. Existing scaffold service tests cover template generation.

### Integration Tests
- Generate test project using CLI
- Verify `.claude/commands/load_ai_docs.md` is created
- Confirm content matches base template
- Verify file is valid markdown

### Edge Cases
Edge cases are handled within the command itself:
- Missing `ai_docs/doc/` directory - error message with suggestion
- Invalid filter syntax - clear error reporting
- Large documentation sets - Explore agent handles efficiently
- No filter provided - loads all documents

## Acceptance Criteria

1. **Base Command File**
   - ✓ Exists at `.claude/commands/load_ai_docs.md`
   - ✓ Contains all required sections (Variables, Instructions, Run, Examples, Report)
   - ✓ Uses standard TAC path `ai_docs/doc/`
   - ✓ Implements filtering syntax (single, range, multiple ranges)
   - ✓ Includes error handling for missing directories

2. **Template File**
   - ✓ Exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_ai_docs.md.j2`
   - ✓ Is static copy with no Jinja2 variables
   - ✓ Matches base file exactly

3. **Scaffold Service**
   - ✓ Command registered in scaffold_service.py commands list
   - ✓ Located in correct section (TAC-9/10)

4. **Validation**
   - ✓ All validation commands pass
   - ✓ No regressions introduced
   - ✓ CLI help shows no errors

5. **Documentation**
   - ✓ Command includes comprehensive examples (5 scenarios)
   - ✓ Filtering syntax clearly documented
   - ✓ Report format well-defined

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Implementation Status
Based on auto-resolved clarifications, all required files already exist:
- Base command file is complete and correct
- Template file exists as static copy
- scaffold_service.py already includes the command

This task is primarily verification that the implementation is correct and complete.

### Design Decisions
1. **Static Template**: Unlike commands like `prime.md.j2` that use project-specific variables, load_ai_docs uses a fixed TAC-standard path (`ai_docs/doc/`), so no Jinja2 variables are needed.

2. **Filtering Approach**: The command implements a flexible filtering syntax supporting:
   - No filter: load all documents
   - Single doc: `5`
   - Range: `1-3`
   - Multiple ranges: `1-3,5,7-8`

3. **Explore Agent**: Uses Task tool with `subagent_type=Explore` at "medium" thoroughness for efficient documentation loading without context overflow.

4. **Error Handling**: Gracefully handles missing directories with helpful error messages suggesting creation of `ai_docs/doc/`.

### TAC Standard Paths
The `ai_docs/doc/` path is a TAC convention used across all projects:
- Numbered TAC courses: doc/1.md through doc/8.md
- Custom project documentation: additional .md files
- Consistent location ensures command works across all TAC projects

### Future Considerations
- Could add support for custom documentation paths (currently fixed to `ai_docs/doc/`)
- Could add topic-based filtering (currently number-based)
- Could integrate with context budgeting for very large doc sets
