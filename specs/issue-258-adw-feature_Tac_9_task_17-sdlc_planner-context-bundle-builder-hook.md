# Feature: Context Bundle Builder Hook Template

## Metadata
issue_number: `258`
adw_id: `feature_Tac_9_task_17`
issue_json: `{"number":258,"title":"Add context_bundle_builder.py.j2 hook template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_17\n\n**Description:**\nCreate Jinja2 template for context bundle builder hook. Tracks Read/Write operations during sessions and saves to JSONL for context recovery.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/context_bundle_builder.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/context_bundle_builder.py` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for a Claude Code hook that tracks file operations (Read, Write, Edit, NotebookEdit) during agent sessions and saves them to session-specific JSONL files for context recovery. This enables agents to recover and understand what files were accessed during previous sessions, providing valuable context for debugging, continuation, and audit trails.

The hook captures minimal but essential information: timestamp, operation type, file path, status (success/error), and session ID. Data is stored in configurable scratchpad directories to avoid polluting the project workspace.

## User Story
As a TAC Bootstrap CLI user
I want my generated projects to track file operations during Claude Code sessions
So that I can recover context from previous sessions, debug agent behavior, and maintain an audit trail of all file manipulations

## Problem Statement
Claude Code sessions generate valuable context through file operations (reads, writes, edits), but this context is lost between sessions. When agents need to resume work, debug issues, or understand what was previously modified, there's no systematic way to recover this information. Additionally, for audit and compliance purposes, tracking file operations provides accountability.

Current limitations:
- No persistent record of which files were accessed during sessions
- Cannot trace back agent decisions to specific file reads
- Difficult to debug agent behavior without operation history
- No audit trail for file modifications
- Context is lost when sessions end or agents fail

## Solution Statement
Create a Jinja2 template (`context_bundle_builder.py.j2`) that generates a Claude Code tool-use-hook. This hook:

1. Intercepts tool execution events for Read, Write, Edit, and NotebookEdit operations
2. Extracts essential metadata (timestamp, operation, file_path, status, session_id)
3. Writes entries to session-specific JSONL files in the scratchpad directory
4. Handles errors silently to never block user workflows
5. Uses configurable paths via Jinja2 variables ({{ config.paths.scratchpad }})
6. Creates one JSONL file per session to avoid race conditions

The template follows existing hook patterns in the codebase while adapting the source implementation to use configuration variables and conform to TAC Bootstrap standards.

## Relevant Files
Files necessary to understand and implement this feature:

**Source Reference:**
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/context_bundle_builder.py` - Source implementation to adapt

**Existing Hook Templates (patterns to follow):**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/post_tool_use.py.j2` - Tool-use hook pattern with logging
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/user_prompt_submit.py.j2` - Session logging pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/notification.py.j2` - Error handling pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/pre_tool_use.py.j2` - Tool interception pattern

**Configuration Models:**
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig schema, PathsSpec for scratchpad path

**Project Configuration:**
- `config.yml` - Example configuration showing paths structure

**Testing References:**
- Existing hook template tests (if any) in `tac_bootstrap_cli/tests/`

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2` - Main Jinja2 template (CREATE)
- `.claude/hooks/context_bundle_builder.py` - Rendered example for this project (CREATE)

## Implementation Plan

### Phase 1: Foundation
**Goal:** Read and understand source implementation and existing patterns

1. Read the source implementation at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/context_bundle_builder.py`
2. Analyze existing hook templates to understand:
   - Jinja2 variable usage patterns ({{ config.* }})
   - Error handling conventions (silent failures to stderr)
   - Logging directory structure patterns
   - Session ID extraction patterns
3. Identify differences between source and template requirements:
   - Hardcoded paths vs configurable paths
   - Additional operations to track (Edit, NotebookEdit beyond Read/Write)
   - JSONL structure differences (if any)

### Phase 2: Core Implementation
**Goal:** Create the Jinja2 template with proper configuration variables

1. Create the template file structure following existing patterns
2. Convert source implementation to Jinja2 template:
   - Replace hardcoded `agents/context_bundles` with `{{ config.paths.scratchpad }}/context_bundles`
   - Add project name context: `{{ config.project.name }}`
   - Maintain core tracking logic
3. Extend operation tracking to handle all four operations:
   - Read - track with offset/limit parameters
   - Write - track with content_length
   - Edit - track with old_string/new_string presence (not content)
   - NotebookEdit - track with notebook_path and cell info
4. Implement JSONL structure:
   ```json
   {"timestamp": "ISO8601", "operation": "read|write|edit|notebookedit", "file_path": "relative_path", "status": "success|error", "session_id": "uuid"}
   ```
5. Add error handling:
   - Silent failures (sys.exit(0) on all errors)
   - Log errors to stderr for debugging
   - Never block tool execution

### Phase 3: Integration
**Goal:** Render template for this project and verify structure

1. Render the template for this project using current config.yml
2. Create `.claude/hooks/context_bundle_builder.py` as working example
3. Verify template variables are correctly interpolated
4. Test that scratchpad directory path is correctly configured
5. Add inline documentation explaining:
   - How the hook is triggered (tool-use-hook)
   - What operations are tracked
   - Where data is stored
   - How to recover context from JSONL files

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Read Source Implementation
- Read the source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/hooks/context_bundle_builder.py`
- Document core logic flow: input parsing, operation filtering, JSONL writing
- Identify hardcoded values that need to become Jinja2 variables
- Note current operations tracked (Read, Write) vs required (Read, Write, Edit, NotebookEdit)

### Task 2: Analyze Existing Hook Patterns
- Read `post_tool_use.py.j2` for tool-use-hook pattern and logging structure
- Read `user_prompt_submit.py.j2` for session logging and directory creation patterns
- Extract common patterns:
  - How {{ config.paths.* }} variables are used
  - How session directories are created
  - How errors are handled silently
  - How JSON/JSONL is structured

### Task 3: Create Template File
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/context_bundle_builder.py.j2`
- Add file header with:
  - Shebang: `#!/usr/bin/env python3`
  - Docstring explaining hook purpose
  - Reference to {{ config.project.name }}
  - Configuration paths used
- Structure file with clear sections: imports, helpers, main logic

### Task 4: Implement Operation Tracking Logic
- Implement tool_name filtering for: Read, Write, Edit, NotebookEdit
- Extract file_path from tool_input (varies by operation)
- Determine success/error status from tool_response
- Convert absolute paths to relative paths (relative to project root)
- Create minimal log entry dict with required fields

### Task 5: Implement JSONL Writing
- Use configurable path: `{{ config.paths.scratchpad }}/context_bundles/session_{session_id}.jsonl`
- Ensure directory creation with `mkdir(parents=True, exist_ok=True)`
- Append JSONL entries (one JSON object per line)
- Add timestamp in ISO8601 format
- Handle IOError gracefully (log to stderr, exit 0)

### Task 6: Add Error Handling
- Wrap main logic in try/except blocks
- Catch JSONDecodeError for input parsing
- Catch IOError for file operations
- Catch general Exception as fallback
- All errors log to stderr and exit(0) to never block

### Task 7: Render Template for This Project
- Create `.claude/hooks/context_bundle_builder.py` by rendering the template
- Use values from current `config.yml`:
  - paths.logs_dir or paths.scratchpad (determine which to use)
  - project.name
- Verify rendered file has no Jinja2 syntax remaining
- Verify paths are correctly interpolated

### Task 8: Add Documentation
- Add comprehensive docstring at file top explaining:
  - Hook trigger type (tool-use-hook)
  - Operations tracked and why
  - JSONL file location and format
  - How to recover context from files
  - Error handling philosophy
- Add inline comments for complex logic
- Document JSONL schema structure in comments

### Task 9: Validation and Testing
- Manually verify template syntax (no Jinja2 errors)
- Check rendered file is valid Python (syntax check)
- Verify all required operations are handled
- Ensure error handling covers all failure modes
- Run full validation suite (final task)

### Task 10: Execute Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Testing Strategy

### Unit Tests
Since this is a template file, testing focuses on:
1. **Template Syntax Validation**: Ensure Jinja2 template is syntactically valid
2. **Rendered Output Validation**: Verify rendered file is valid Python
3. **Variable Interpolation**: Check that all {{ config.* }} variables are replaced
4. **Path Construction**: Verify scratchpad path is correctly constructed

### Manual Testing
1. Render template with test config.yml
2. Verify rendered Python file has correct paths
3. Check that all four operations (Read, Write, Edit, NotebookEdit) are handled
4. Simulate hook execution with test JSON input
5. Verify JSONL file is created with correct structure

### Edge Cases
- Missing session_id in input (fallback to "unknown")
- File operations outside project directory (keep absolute path)
- Non-existent scratchpad directory (create with parents)
- Concurrent writes to same JSONL file (file append is atomic for small writes)
- Tool response missing success field (assume success)
- Input JSON parsing errors (exit gracefully)
- File write errors (log to stderr, don't block)

## Acceptance Criteria
1. Template file `context_bundle_builder.py.j2` created following existing hook patterns
2. Template uses Jinja2 variables: `{{ config.paths.scratchpad }}`, `{{ config.project.name }}`
3. All four operations tracked: Read, Write, Edit, NotebookEdit
4. JSONL structure includes: timestamp, operation, file_path, status, session_id
5. Errors are handled silently (stderr logging, exit 0)
6. Rendered example created at `.claude/hooks/context_bundle_builder.py`
7. Template renders without Jinja2 syntax errors
8. Rendered file is valid Python syntax
9. Comprehensive documentation in docstring and comments
10. All validation commands pass with zero regressions

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Configuration Path Considerations
The source implementation uses `agents/context_bundles`, but TAC Bootstrap projects should use the scratchpad directory pattern. Need to determine:
- Should we use `{{ config.paths.logs_dir }}/context_bundles` or a dedicated `{{ config.paths.scratchpad }}/context_bundles`?
- If `scratchpad` is not in PathsSpec, may need to add it or use logs_dir as fallback

Based on examination of existing templates, `logs_dir` is the standard location for session-specific data.

### Operation Tracking Details
- **Read**: Track offset/limit parameters to understand partial reads
- **Write**: Track content_length (not content) to avoid huge logs
- **Edit**: Track that edit occurred but not old_string/new_string content
- **NotebookEdit**: Track notebook_path and cell metadata

### JSONL Format Benefits
- One JSON object per line enables streaming reads
- Append-friendly (no need to read entire file to add entry)
- Line-atomic writes are safe for concurrent access
- Easy to process with standard tools (jq, grep, etc.)
- Smaller file size compared to pretty-printed JSON array

### Future Enhancements (Out of Scope)
- Context recovery CLI command to read and display JSONL logs
- Integration with /prime command to automatically inject context
- Compression/rotation of old JSONL files
- Filtering by file pattern or operation type
- Aggregate statistics (most-read files, write frequency, etc.)
