# Feature: Load Bundle Command Template

## Metadata
issue_number: `261`
adw_id: `feature_Tac_9_task_20`
issue_json: `{"number":261,"title":"Add load_bundle.md.j2 command template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_20\n\n**Description:**\nCreate Jinja2 template for `/load_bundle` slash command. Enables context recovery from previously saved context bundles.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/commands/load_bundle.md`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_bundle.md` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for the `/load_bundle` slash command that enables context recovery from previously saved context bundles. This command is the complement to the `context_bundle_builder` hook: while the hook automatically tracks file operations during sessions and saves them to JSONL files, this command allows users to manually recover that context by re-reading the tracked files.

The command provides a structured way to:
1. Locate context bundle files in `logs/context_bundles/`
2. Parse JSONL entries to understand what files were accessed
3. Re-read key files to restore working context
4. Handle missing files gracefully (files may have been deleted since bundle creation)

## User Story
As a Claude Code user
I want to load context from a previous session
So that I can continue work seamlessly, understand what files were accessed, and recover from interrupted sessions

## Problem Statement
When Claude Code sessions end or fail, the context built up during that session (files read, operations performed) is lost. While the `context_bundle_builder` hook automatically tracks this information to JSONL files, users need a convenient way to:

- Resume work from where they left off
- Understand what files a previous agent accessed
- Debug agent behavior by reviewing operation history
- Recover context after session failures or timeouts

Current limitations:
- No standardized way to load context bundles
- Users must manually parse JSONL files
- No guidance on which files to re-read
- Error handling for missing files is ad-hoc
- No integration with the existing bundle storage structure

## Solution Statement
Create a Jinja2 template (`load_bundle.md.j2`) that generates a `/load_bundle` slash command following the established command pattern (Variables/Instructions/Run/Examples/Report). This command:

1. Accepts a bundle path or session_id as argument
2. Reads JSONL file from `logs/context_bundles/session_{session_id}.jsonl`
3. Provides instructions to parse JSONL entries and re-read files
4. Handles missing files gracefully with clear reporting
5. Follows the same pattern as `/background` command for consistency
6. Uses configuration variables like `{{ config.project.name }}` for context

The template will be rendered for this repository to serve as documentation and a working example.

## Relevant Files
Files necessary to understand and implement this feature:

**Existing Command Templates (patterns to follow):**
- `.claude/commands/background.md` - Rendered example with Variables/Instructions/Run/Examples/Report structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` - Most recent command template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Another example of command structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime.md.j2` - Command that reads multiple files for context

**Context Bundle Hook (complementary feature):**
- `.claude/hooks/context_bundle_builder.py` - Hook that creates the JSONL bundles this command loads
- `specs/issue-258-adw-feature_Tac_9_task_17-sdlc_planner-context-bundle-builder-hook.md` - Hook documentation

**Configuration:**
- `config.yml` - Project configuration with paths

**Documentation:**
- `ai_docs/doc/plan_tasks_Tac_9.md` - TAC-9 task list (Task 20)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` - Jinja2 template (CREATE)
- `.claude/commands/load_bundle.md` - Rendered example for this project (CREATE)

## Implementation Plan

### Phase 1: Foundation
**Goal:** Understand context bundle structure and command patterns

1. Review context bundle JSONL structure from the hook implementation
2. Analyze `/background` command pattern (most similar/recent command)
3. Understand bundle storage location: `logs/context_bundles/session_{session_id}.jsonl`
4. Identify key sections needed: Variables, Instructions, Run, Examples, Report

### Phase 2: Core Implementation
**Goal:** Create the Jinja2 template with proper structure and instructions

1. Create template file following the `/background` pattern
2. Define Variables section (bundle_path or session_id argument)
3. Write Instructions explaining:
   - What context bundles are and why they're useful
   - Where bundle files are stored
   - How to find available bundles
   - JSONL structure and what each field means
4. Create Run section with step-by-step process:
   - Locate bundle file in `logs/context_bundles/`
   - Read and parse JSONL entries
   - Re-read files listed in the bundle
   - Handle missing files gracefully
   - Report summary of restored context
5. Add Examples showing common use cases:
   - Loading most recent session bundle
   - Loading specific session by ID
   - Handling missing files scenario
6. Define Report format for user feedback

### Phase 3: Integration
**Goal:** Render template for this project and validate

1. Render the template using current config.yml
2. Create `.claude/commands/load_bundle.md` as working example
3. Verify template variables are correctly interpolated
4. Ensure consistency with bundle hook implementation
5. Test that instructions are clear and actionable

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze Context Bundle Structure
- Read `.claude/hooks/context_bundle_builder.py` to understand JSONL format
- Document JSONL entry schema:
  - timestamp (ISO8601)
  - operation (read|write|edit|notebookedit)
  - file_path (relative path)
  - status (success|error)
  - session_id (uuid)
  - tool_input (optional metadata)
- Note storage location: `logs/context_bundles/session_{session_id}.jsonl`

### Task 2: Analyze Command Pattern
- Read `.claude/commands/background.md` for structure reference
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2` for Jinja2 patterns
- Extract standard sections: Variables, Instructions, Run, Examples, Report
- Note how arguments are documented using `$ARGUMENT` syntax
- Understand how to structure step-by-step instructions

### Task 3: Create Template File Structure
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`
- Add file header: `# Load Context Bundle`
- Add opening description explaining the command's purpose
- Structure with standard sections (Variables, Instructions, Run, Examples, Report)

### Task 4: Implement Variables Section
- Define `bundle_path: $ARGUMENT (optional)` - path to bundle file
- Define `session_id: $ARGUMENT (optional)` - session ID to load
- Document that one of the arguments should be provided
- Explain default behavior (load most recent bundle if none specified)

### Task 5: Implement Instructions Section
- Explain what context bundles are (JSONL files tracking file operations)
- Describe where bundles are stored: `logs/context_bundles/`
- Explain JSONL structure and what each field means
- Clarify use cases:
  - Resume work after session failure
  - Understand previous agent behavior
  - Recover context for debugging
- Note graceful handling of missing files

### Task 6: Implement Run Section
- Step 1: Locate bundle file
  - If bundle_path provided, use it directly
  - If session_id provided, construct path: `logs/context_bundles/session_{session_id}.jsonl`
  - Otherwise, find most recent file in `logs/context_bundles/`
- Step 2: Verify bundle file exists
  - Check file existence
  - Report error if missing
- Step 3: Read and parse JSONL
  - Read file line by line
  - Parse each JSON entry
  - Extract file paths and operations
- Step 4: Re-read key files
  - Prioritize files with 'read' or 'edit' operations
  - Use Read tool to restore file contents to context
  - Track which files exist vs missing
- Step 5: Report summary
  - List files successfully restored
  - List files that are missing
  - Show operation counts by type

### Task 7: Implement Examples Section
- Example 1: Load most recent bundle
  - No arguments provided
  - Show finding latest session file
- Example 2: Load specific session
  - Provide session_id
  - Show loading that specific bundle
- Example 3: Handle missing files
  - Bundle references deleted file
  - Show graceful error message and continue

### Task 8: Implement Report Section
- Define output format with:
  - Bundle file path loaded
  - Number of entries found
  - Files successfully restored (with paths)
  - Files missing (with paths)
  - Operation summary (X reads, Y writes, Z edits)
- Include example report output

### Task 9: Render Template for This Project
- Render template using config.yml values
- Create `.claude/commands/load_bundle.md`
- Verify no Jinja2 syntax remains
- Verify paths are correct
- Ensure {{ config.project.name }} is properly interpolated

### Task 10: Validation
- Manually review template syntax
- Check rendered file is properly formatted markdown
- Verify consistency with `/background` command structure
- Ensure instructions are clear and actionable
- Confirm bundle storage path matches hook implementation

### Task 11: Execute Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Template Testing
Since this is a command template (documentation), testing focuses on:
1. **Template Syntax**: Ensure Jinja2 template is valid
2. **Rendering**: Verify template renders without errors using test config
3. **Variable Interpolation**: Check all {{ config.* }} variables are replaced
4. **Markdown Formatting**: Verify rendered output is valid markdown

### Manual Validation
1. Render template with project config.yml
2. Review rendered command for clarity and completeness
3. Verify instructions match the bundle hook implementation
4. Check that bundle path references are consistent
5. Ensure error handling guidance is appropriate

### Edge Cases
Command should provide guidance for:
- Bundle file doesn't exist (wrong session_id or path)
- JSONL is malformed or corrupted
- Files referenced in bundle no longer exist
- Empty bundle (no operations tracked)
- Multiple bundle files (how to choose)
- Bundle from different project (absolute paths)

## Acceptance Criteria
1. Template file `load_bundle.md.j2` created following `/background` command pattern
2. Template includes all standard sections: Variables, Instructions, Run, Examples, Report
3. Instructions clearly explain context bundles and JSONL structure
4. Run section provides step-by-step guidance for loading bundles
5. Bundle storage path matches hook implementation: `logs/context_bundles/`
6. Error handling for missing files is documented
7. Examples cover common use cases (recent bundle, specific session, missing files)
8. Template uses Jinja2 variables appropriately (e.g., `{{ config.project.name }}`)
9. Rendered example created at `.claude/commands/load_bundle.md`
10. Template renders without Jinja2 syntax errors
11. Rendered file is properly formatted markdown
12. All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Relationship to Context Bundle Hook
The `/load_bundle` command is the manual companion to the automatic `context_bundle_builder` hook:
- **Hook**: Automatically tracks file operations → saves to JSONL
- **Command**: Manually reads JSONL → restores context by re-reading files

This separation allows:
- Automatic tracking without user intervention
- Manual recovery when needed
- Flexibility in when/how context is restored

### Bundle Storage Consistency
The hook uses `logs/context_bundles/session_{session_id}.jsonl`. This command MUST reference the same path structure to ensure consistency between save and load operations.

### JSONL Benefits for Context Recovery
- Line-by-line processing (can handle large files)
- Each entry is self-contained
- Easy to filter by operation type or file pattern
- Human-readable for debugging
- Tool-friendly (jq, grep work out of the box)

### Graceful Degradation Philosophy
Following the hook's error handling philosophy, this command should:
- Never fail completely if some files are missing
- Provide clear feedback about what succeeded/failed
- Allow partial context recovery
- Be forgiving of JSONL parsing errors

### Future Enhancements (Out of Scope)
- Filtering by file pattern when loading
- Filtering by operation type (only loads reads, not writes)
- Time-based filtering (only recent operations)
- Merge multiple bundles
- Interactive bundle selection
- Bundle diff/comparison
