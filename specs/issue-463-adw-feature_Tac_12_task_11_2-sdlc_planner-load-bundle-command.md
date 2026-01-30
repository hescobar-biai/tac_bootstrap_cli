# Feature: Load Bundle Command

## Metadata
issue_number: `463`
adw_id: `feature_Tac_12_task_11_2`
issue_json: `{"number":463,"title":"[Task 11/49] [FEATURE] Create load_bundle.md command file","body":"## Description\n\nCreate a command that loads context bundles (pre-packaged file sets).\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/load_bundle.md`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`\n\n## Key Features\n- Pre-packaged context loading\n- Bundle definitions\n- allowed-tools: Read, Glob\n\n## Changes Required\n- Create command file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in commands list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md`\n\n## Wave 1 - New Commands (Task 11 of 13)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_11_2"}`

## Feature Description

Create the `/load_bundle` slash command that enables Claude Code agents to restore session context by loading JSONL bundle files. These bundles are automatically created by the `context_bundle_builder` hook and track all file operations (read, write, edit, notebookedit) during a session. This command is critical for session recovery, debugging agent behavior, and continuing interrupted work.

The feature consists of:
1. A base command file in `.claude/commands/load_bundle.md` (working version)
2. A Jinja2 template for CLI-generated projects
3. Integration in `scaffold_service.py` command list

## User Story

As a Claude Code agent
I want to load context bundles from previous sessions
So that I can recover context after failures, understand previous agent work, debug behavior, and resume interrupted tasks

## Problem Statement

When Claude Code sessions fail, timeout, or are interrupted, agents lose all context about what files were accessed and what operations were performed. Without a mechanism to restore this context:
- Agents cannot resume work efficiently after interruptions
- Debugging agent behavior requires manual file inspection
- Understanding what a previous agent did requires reading logs
- Session recovery is manual and error-prone

The `context_bundle_builder` hook solves half the problem by creating JSONL operation logs, but agents need a command to efficiently restore context from these bundles.

## Solution Statement

Create a `/load_bundle` slash command that:
1. Locates bundle files (most recent, by session_id, or explicit path)
2. Parses JSONL entries to extract file operations
3. Re-reads unique files to restore context
4. Handles missing files gracefully (files may have been deleted since bundle creation)
5. Reports detailed restoration summary

The command uses a static template (no project-specific Jinja2 variables) because bundle handling is universal across all projects. The only difference between the base command and template is that both are identical - templates just need to be properly placed for CLI generation.

## Relevant Files

Files necessary for implementing this feature:

- **Reference Implementation:**
  - `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md` - Production reference showing proven implementation

- **Base Repository:**
  - `.claude/commands/load_bundle.md` - Working command file for this repository
  - Purpose: Enables agents in tac_bootstrap repo to load bundles during development

- **Template Infrastructure:**
  - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` - Template for CLI generation
  - Purpose: Generated projects get this command when using `tac-bootstrap init`

- **Service Integration:**
  - `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:321` - Commands list
  - Purpose: Add "load_bundle" to commands array so template is included in scaffold plan

- **Related Infrastructure (already exists, no changes needed):**
  - `.claude/hooks/context_bundle_builder.py` - Creates the JSONL bundles
  - `logs/context_bundles/` - Storage location for bundle files
  - `agents/context_bundles/` - Mapped location in scaffold

### New Files

1. `.claude/commands/load_bundle.md` - Base command for tac_bootstrap repo
2. `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` - Template for generated projects

## Implementation Plan

### Phase 1: Foundation
Copy the reference implementation from tac-12 and adapt it to tac_bootstrap structure. The reference shows proven patterns for JSONL parsing, file restoration, and error handling that should be preserved.

### Phase 2: Core Implementation
Create both the base command file and the Jinja2 template. Since the command logic is universal (no project-specific customization needed), the template will be nearly identical to the base file with minimal Jinja2 markup.

### Phase 3: Integration
Update `scaffold_service.py` to include `load_bundle` in the commands list, ensuring generated projects receive this command. Verify the command works in both the base repository and in generated projects.

## Step by Step Tasks

### Task 1: Read reference implementation
- Read `/Volumes/MAc1/Celes/TAC/tac-12/.claude/commands/load_bundle.md` to understand the proven implementation
- Note the JSONL parsing approach
- Note the file restoration logic
- Note the error handling for missing files
- Note the reporting format

### Task 2: Create base command file
- Create `.claude/commands/load_bundle.md` in base repository
- Copy core logic from reference implementation
- Adapt paths to use `logs/context_bundles/` (base repo structure)
- Include frontmatter with description, argument-hint, and allowed-tools
- Include Variables section defining bundle_path and session_id parameters
- Include Instructions section explaining bundle format and use cases
- Include Run section with step-by-step execution logic
- Include Examples section showing different usage patterns
- Include Report section with output format specification
- Ensure graceful handling of missing files
- Document JSONL schema clearly

### Task 3: Create Jinja2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`
- Base content on the command file created in Task 2
- Template is static - no Jinja2 variables needed (bundle logic is universal)
- Paths use `logs/context_bundles/` which is standardized in scaffold
- Verify template renders correctly without project-specific customization
- Template should be nearly identical to base file

### Task 4: Update scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate commands list in `_add_claude_files` method (around line 279-333)
- Add `"load_bundle"` to the commands array in appropriate location
- Place it logically near `load_ai_docs` (both are context loading commands)
- Ensure consistent formatting with existing entries
- Verify the template path matches: `claude/commands/load_bundle.md.j2`

### Task 5: Verify integration
- Check that template file exists at expected path
- Verify `scaffold_service.py` includes "load_bundle" in commands list
- Confirm the loop that creates command files (lines 335-342) will process load_bundle
- Check that file action is CREATE (creates if doesn't exist)
- Check that reason text is appropriate: "Load bundle slash command" or similar

### Task 6: Update conditional_docs.md
- Read `.claude/commands/conditional_docs.md` to understand format
- Add entry for load_bundle.md with appropriate conditions
- Conditions should include:
  - When working with session recovery features
  - When debugging agent behavior
  - When working with context bundle infrastructure
  - When working with the context_bundle_builder hook

### Task 7: Test base command
- Verify `.claude/commands/load_bundle.md` exists and is readable
- Test the command works as a slash command: `/load_bundle`
- Verify it can locate and read bundle files
- Verify it handles missing bundle_path gracefully
- Verify it reports correct summary information

### Task 8: Validate template rendering
- Run validation commands to ensure no regressions
- Verify template file is syntactically correct
- Verify scaffold service properly includes the command
- Check that generated projects would receive the command

## Testing Strategy

### Unit Tests

No unit tests required for this feature because:
- Commands are markdown files with embedded instructions for agents
- No executable Python code is being added
- Testing would require integration tests with Claude Code runtime

### Edge Cases

1. **Missing bundle file:**
   - User provides session_id that doesn't exist
   - Command should report error clearly
   - Should not crash or show stack trace

2. **Empty bundle file:**
   - Bundle file exists but has no entries
   - Command should report "0 entries found"
   - Should complete successfully with empty result

3. **Malformed JSONL:**
   - Bundle contains invalid JSON on some lines
   - Command should skip malformed lines with warning
   - Should continue processing valid entries

4. **Missing files in bundle:**
   - Bundle references files that have been deleted
   - Command should skip missing files gracefully
   - Should report which files are missing in summary

5. **No arguments provided:**
   - User runs `/load_bundle` with no parameters
   - Command should find most recent bundle automatically
   - Should use `ls -t logs/context_bundles/session_*.jsonl | head -1`

6. **Bundle path vs session_id:**
   - User provides both bundle_path and session_id
   - Command should prioritize bundle_path (explicit > implicit)
   - Should ignore session_id if bundle_path is provided

## Acceptance Criteria

1. **Base command file exists and works:**
   - `.claude/commands/load_bundle.md` exists
   - Command is accessible as `/load_bundle` in base repository
   - Command can locate bundle files automatically (most recent)
   - Command can load specific session by session_id parameter
   - Command can load explicit path via bundle_path parameter

2. **Template file exists and is valid:**
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` exists
   - Template is valid Jinja2 (renders without errors)
   - Template content matches base command (static, no variables)

3. **Integration is complete:**
   - `scaffold_service.py` includes "load_bundle" in commands list
   - Command appears near other context commands (load_ai_docs)
   - Generated projects will receive this command file

4. **Documentation is updated:**
   - `conditional_docs.md` includes load_bundle.md entry
   - Conditions are clear and specific
   - Documentation explains when to read the command file

5. **Functional requirements met:**
   - Command parses JSONL entries correctly
   - Command extracts unique file paths
   - Command re-reads files to restore context
   - Command handles missing files gracefully (skip with warning)
   - Command reports detailed summary:
     - Bundle path
     - Total entries
     - Session ID
     - Files restored (with paths)
     - Files missing (with paths)
     - Operation counts (reads, writes, edits, notebookedits)

6. **No regressions introduced:**
   - All validation commands pass
   - Existing commands still work
   - Template rendering doesn't break
   - Scaffold service builds valid plans

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

1. **Bundle structure is already established:**
   - JSONL format with timestamp, operation, file_path, status, session_id, tool_input
   - Created by `context_bundle_builder` hook (already exists)
   - Stored in `logs/context_bundles/` directory
   - No changes to bundle format needed

2. **Template is static (no Jinja2 variables):**
   - Bundle handling is universal across projects
   - No project-specific paths needed (logs/context_bundles/ is standardized)
   - Template should be nearly identical to base command file
   - This is consistent with load_ai_docs.md.j2 which only uses config.ai_docs_path

3. **Path mapping in scaffold:**
   - Base repo uses: `logs/context_bundles/`
   - Generated projects use: `agents/context_bundles/` (via scaffold)
   - Command needs to work with whatever path exists in target project
   - Actually both use `logs/context_bundles/` - checked scaffold_service.py directories

4. **Command should be resilient:**
   - Missing files are normal (files may be deleted after bundle creation)
   - Malformed JSONL lines should be skipped with warnings
   - Empty bundles should complete successfully
   - Missing bundle files should report clear errors

5. **Integration pattern:**
   - Follow existing pattern in scaffold_service.py
   - Commands list is simple string array
   - Loop automatically creates plan entries for each command
   - Template path is constructed as `claude/commands/{cmd}.md.j2`

6. **Future considerations:**
   - Bundle compression for large sessions (not in this feature)
   - Bundle filtering by operation type (not in this feature)
   - Bundle merging from multiple sessions (not in this feature)
   - These can be added later without breaking changes
