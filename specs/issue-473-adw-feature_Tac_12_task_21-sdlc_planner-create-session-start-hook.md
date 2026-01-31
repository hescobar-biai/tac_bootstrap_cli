# Feature: Create session_start.py hook file

## Metadata
issue_number: `473`
adw_id: `feature_Tac_12_task_21`
issue_json: `{"number": 473, "title": "[Task 21/49] [FEATURE] Create session_start.py hook file", "body": "## Description\n\nCreate SessionStart hook for initializing session context.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/session_start.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2`\n\n## Key Features\n- Captures git branch, model, project metadata\n- Writes to session storage\n\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/session_start.py`\n\n## Wave 3 - New Hooks (Task 21 of 9)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_21"}`

## Feature Description
Create a session_start.py hook that captures session initialization context and writes it to a JSON file. This hook executes when a Claude Code session starts, capturing critical metadata including git branch, model name, project name, session timestamp, and current working directory. This context enables better session tracking, debugging, and observability.

The hook follows established patterns from send_event.py, using graceful error handling, the uv run shebang pattern, and local JSON storage.

## User Story
As a TAC Bootstrap user
I want my Claude Code sessions to automatically capture initialization context
So that I can track session metadata, debug issues, and maintain an audit trail

## Problem Statement
When Claude Code sessions start, there's no automatic capture of session context (git branch, model, project metadata). This makes it difficult to:
- Track which sessions worked on which branches
- Debug session-specific issues
- Audit agentic work
- Correlate session logs with project state

## Solution Statement
Create a session_start.py hook that:
1. Executes automatically when Claude Code sessions initialize
2. Captures git branch (with graceful fallback for non-git repos)
3. Captures current model name from Claude environment
4. Captures project name from config.yml
5. Records session timestamp in ISO format
6. Records current working directory
7. Writes all metadata to `.claude/session_context.json` as a flat dictionary
8. Handles all errors gracefully without breaking the session

## Relevant Files
Files necessary for implementing this feature:

### Existing files to reference:
- `.claude/hooks/send_event.py` - Pattern reference for hook structure, error handling, and uv shebang
- `.claude/hooks/utils/constants.py` - Utility functions for session log directory management
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service to update with new hook
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/send_event.py.j2` - Template pattern reference
- `config.yml` - Project configuration schema (project.name field)

### New Files
- `.claude/hooks/session_start.py` - Base implementation of session_start hook
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Base Hook Implementation
Create the session_start.py hook in the base repository following the established pattern from send_event.py. This hook will be executable and use the uv run shebang pattern for dependency management.

Key implementation details:
- Use `#!/usr/bin/env -S uv run --script` shebang
- Include inline script dependencies (PyYAML for config parsing)
- Capture git branch with subprocess, fallback to "unknown" on error
- Read project name from config.yml using PyYAML
- Get model name from CLAUDE_MODEL environment variable (fallback to "unknown")
- Write flat JSON dictionary to `.claude/session_context.json`
- All operations wrapped in try-except with graceful error handling
- Exit with status 0 (success) even on errors to avoid breaking session

### Phase 2: Template Creation
Create the Jinja2 template that mirrors the base implementation. The template should be minimal with no complex logic, using only project.name variable for consistency with other templates.

Template considerations:
- Use `{{ config.project.name }}` for project name in comments/docstrings
- Keep template logic minimal - most code is static
- Follow exact same structure as base implementation
- Maintain consistency with send_event.py.j2 template patterns

### Phase 3: Integration
Update scaffold_service.py to include session_start.py in the hooks list, ensuring it's generated when users bootstrap new projects.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create base hook implementation
- Create `.claude/hooks/session_start.py` with uv shebang pattern
- Add script dependencies inline (PyYAML for config parsing)
- Implement git branch capture using subprocess (git rev-parse --abbrev-ref HEAD)
- Add try-except wrapper for git command with "unknown" fallback
- Implement config.yml parsing to extract project name
- Add try-except for config parsing with "unknown" fallback
- Capture model from CLAUDE_MODEL env var with "unknown" fallback
- Capture current working directory using os.getcwd()
- Generate ISO timestamp using datetime.now(timezone.utc).isoformat()
- Create session context dictionary with all metadata
- Write dictionary to `.claude/session_context.json` using json.dump
- Wrap all operations in top-level try-except for graceful error handling
- Ensure hook always exits with status 0
- Make file executable (chmod +x)

### Task 2: Create Jinja2 template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/session_start.py.j2`
- Copy base implementation structure
- Use `{{ config.project.name }}` variable in comments/docstrings
- Ensure template renders identical functional code to base implementation
- Keep Jinja2 logic minimal (only project name reference)

### Task 3: Update scaffold service
- Edit `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Add `("session_start.py", "Session initialization context capture")` to hooks list (around line 356)
- Maintain alphabetical or logical ordering within hooks list
- Ensure new hook is registered in `_add_claude_files` method

### Task 4: Validation
- Run validation commands to ensure zero regressions
- Test base hook execution: `uv run .claude/hooks/session_start.py`
- Verify session_context.json is created in .claude/ directory
- Verify JSON structure contains all required fields
- Run pytest to ensure scaffold service tests pass
- Run ruff check and mypy for code quality
- Run CLI smoke test to ensure CLI still works

## Testing Strategy

### Unit Tests
Since the hook is a standalone script, testing focuses on:
1. File creation and permissions (executable bit set)
2. Template rendering (validates Jinja2 syntax)
3. Scaffold service integration (hook appears in plan)

### Integration Tests
Manual testing after implementation:
1. Execute hook directly: `uv run .claude/hooks/session_start.py`
2. Verify `.claude/session_context.json` exists and contains valid JSON
3. Verify JSON has required keys: git_branch, model, project_name, timestamp, cwd
4. Test in non-git directory (should use "unknown" for branch)
5. Test with missing config.yml (should use "unknown" for project_name)
6. Test with missing CLAUDE_MODEL env var (should use "unknown" for model)

### Edge Cases
- Non-git repository: Hook should create session_context.json with git_branch="unknown"
- Missing config.yml: Hook should use project_name="unknown"
- Missing environment variables: Hook should use "unknown" fallbacks
- Permission errors writing JSON: Hook logs error to stderr but exits 0
- Malformed config.yml: Hook catches YAML parse error, uses "unknown"

## Acceptance Criteria
1. ✅ Base hook file `.claude/hooks/session_start.py` exists and is executable
2. ✅ Hook uses `#!/usr/bin/env -S uv run --script` shebang pattern
3. ✅ Hook captures git branch using subprocess with error handling
4. ✅ Hook reads project name from config.yml using PyYAML
5. ✅ Hook captures model from CLAUDE_MODEL environment variable
6. ✅ Hook captures current working directory
7. ✅ Hook generates ISO timestamp
8. ✅ Hook writes all metadata to `.claude/session_context.json` as flat dictionary
9. ✅ Hook handles all errors gracefully with "unknown" fallbacks
10. ✅ Hook always exits with status 0 (non-blocking)
11. ✅ Template file `session_start.py.j2` exists and mirrors base implementation
12. ✅ Template uses `{{ config.project.name }}` variable appropriately
13. ✅ `scaffold_service.py` includes session_start.py in hooks list
14. ✅ All validation commands pass with zero errors

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `uv run .claude/hooks/session_start.py` - Test base hook execution
- `test -f .claude/session_context.json && echo "Session context file created"` - Verify file creation
- `cat .claude/session_context.json` - Verify JSON structure
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Hook follows Wave 3 pattern from TAC-12 implementation plan
- This is task 21 of 49 in the overall TAC Bootstrap implementation
- Hook is non-blocking and session-safe (always exits 0)
- JSON file is overwritten on each session start (not merged/appended)
- Future enhancement: Could integrate with send_event.py for remote observability
- Future enhancement: Could capture additional metadata (Python version, OS, etc.)
- Reference implementation exists at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/session_start.py` but is not required for this task
