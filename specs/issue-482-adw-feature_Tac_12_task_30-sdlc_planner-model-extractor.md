# Feature: Create model_extractor.py Hook Utility

## Metadata
issue_number: `482`
adw_id: `feature_Tac_12_task_30`
issue_json: `[Task 30/49] [FEATURE] Create model_extractor.py hook utility`

## Feature Description
Create a lightweight utility module `model_extractor.py` that extracts Claude model names from session context files with file-based caching. This utility is called by hook scripts (particularly `send_event.py`) to identify which Claude model is executing the current session for event logging and analytics purposes.

The utility provides a single public function: `get_model_from_transcript(session_id: str) -> Optional[str]` which:
- Accepts a session ID string
- Reads model name from `.claude/session_context.json` or `agents/session_metadata/<session_id>.json`
- Caches extracted model in `.claude/data/claude-model-cache/<session_id>.txt`
- Returns model string (e.g., "claude-haiku-4-5-20251001") or None on any error
- Never raises exceptions; gracefully degrades to None on failures

## User Story
As a hook utility developer
I want to extract the current session's model name
So that I can log which Claude model executed a particular event or action

## Problem Statement
Hook scripts need to know which Claude model is running the current session for event observability and analytics. The model information is captured at session initialization but needs to be accessible from within hook scripts. A simple, lightweight utility with caching prevents repeated file I/O during high-frequency hook execution.

## Solution Statement
Implement `model_extractor.py` as a pure Python module (zero external dependencies) that:
1. Accepts session_id as parameter (callers provide this via environment/function args)
2. First checks if model is cached in `.claude/data/claude-model-cache/<session_id>.txt`
3. On cache miss, reads `.claude/session_context.json` or `agents/session_metadata/<session_id>.json`
4. Extracts the 'model' JSON field
5. Writes result to cache file
6. Returns model string or None; never raises exceptions
7. Auto-creates cache directory if needed; skips cache on creation failure

This follows the existing utility pattern (like `constants.py`, `summarizer.py`) used in hook infrastructure.

## Relevant Files
Archivos necesarios para implementar la feature:

### Existing Reference Files
- `/.claude/hooks/utils/constants.py` - Existing hook utility pattern (directory structure, imports, stdlib-only)
- `/.claude/hooks/utils/summarizer.py` - Existing hook utility pattern (error handling, graceful fallback)
- `/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:368-386` - Where hook utilities are registered
- `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Template for hook utilities
- `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py` - Reference implementation

### New Files to Create
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py` - Base utility implementation
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2` - Jinja2 template for CLI generation

### Files to Modify
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add model_extractor.py to hook utilities list (lines 368-386)

## Implementation Plan

### Phase 1: Understand Requirements
- Review reference implementation at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py`
- Understand session context file structure (.claude/session_context.json format)
- Verify cache directory path convention (.claude/data/claude-model-cache/)
- Confirm return type and error handling behavior (returns Optional[str], never raises)

### Phase 2: Base Implementation
- Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py`
- Implement `get_model_from_transcript(session_id: str) -> Optional[str]`
- Zero external dependencies (stdlib only: json, pathlib, os)
- Graceful error handling: return None on all failures
- File-based caching in .claude/data/claude-model-cache/<session_id>.txt
- Auto-create cache directory; skip caching on creation failure

### Phase 3: Template Creation
- Create `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- Use Jinja2 template format matching `constants.py.j2` pattern
- Template should include project metadata (config.project.name, etc.) in docstring
- No configuration variables in template logic; pure code with metadata

### Phase 4: Service Registration
- Update `scaffold_service.py:_add_claude_files()` method
- Add model_extractor.py to hook utilities file registration (after summarizer.py)
- Register with reason "Model extractor utility"

### Phase 5: Validation
- Verify file exists and has correct structure
- Test imports work: `from utils.model_extractor import get_model_from_transcript`
- Run linting and type checking
- Confirm no new dependencies added

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create Base Implementation
- Read reference file at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py`
- Understand the complete implementation logic:
  - Session context file paths
  - JSON parsing for model field
  - Cache structure (session_id.txt with model string)
  - Error handling (return None, not exceptions)
  - Directory auto-creation with fallback
- Create new file: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/model_extractor.py`
- Copy implementation from reference, ensuring:
  - Python 3.8+ compatibility
  - Only stdlib imports (json, pathlib, os)
  - Proper docstrings for public function
  - Graceful error handling on all I/O operations

### Task 2: Create Jinja2 Template
- Read existing template: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`
- Understand Jinja2 variable structure: `{{ config.project.name }}`
- Create file: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- Template content should:
  - Include project name in docstring: `{{ config.project.name }}`
  - Include uv script header with requires-python
  - Include complete model_extractor implementation
  - Preserve all docstrings and comments

### Task 3: Register in scaffold_service.py
- Read `scaffold_service.py:_add_claude_files()` method (around lines 368-386)
- Locate the hook utils file registration block
- Add new file registration after summarizer.py:
  ```python
  plan.add_file(
      ".claude/hooks/utils/model_extractor.py",
      action=action,
      template="claude/hooks/utils/model_extractor.py.j2",
      reason="Model extractor utility",
  )
  ```
- Verify indentation and syntax consistency with existing entries

### Task 4: Run Validation Commands
- Ensure file exists at both locations
- Verify imports: `cd tac_bootstrap_cli && python3 -c "from templates import model_extractor" 2>&1 | head -5`
- Check template exists: `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- Run linting on scaffold_service.py changes
- Confirm no syntax errors: `python3 -m py_compile tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`

## Testing Strategy

### Unit Tests
- Test `get_model_from_transcript()` with valid session_id
- Test cache hit (returns cached value without re-reading)
- Test cache miss (reads from session context, writes to cache)
- Test missing session context (returns None gracefully)
- Test malformed JSON in session context (returns None gracefully)
- Test missing 'model' field in JSON (returns None gracefully)
- Test I/O error on cache write (continues gracefully without cache)

### Edge Cases
- Session ID with special characters (should work as filename)
- Non-existent session context path (returns None)
- Cache directory creation failure (skips cache, returns value)
- Concurrent access to same cache file (file system handles atomicity)
- Cache file becomes stale between reads (TTL mechanism handles refresh)
- Empty session context file (returns None)
- Very long model names (cache stores full value)

## Acceptance Criteria
- ✓ Base implementation file created at `.claude/hooks/utils/model_extractor.py`
- ✓ Jinja2 template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2`
- ✓ `scaffold_service.py` updated to register model_extractor.py in hook utilities list
- ✓ Function signature: `get_model_from_transcript(session_id: str) -> Optional[str]`
- ✓ Cache stored in `.claude/data/claude-model-cache/<session_id>.txt`
- ✓ Returns None gracefully on all errors (no exceptions raised)
- ✓ Zero external dependencies (stdlib only)
- ✓ Auto-creates cache directory with `mkdir(parents=True, exist_ok=True)`
- ✓ Skips caching if directory creation fails
- ✓ Docstrings follow existing utility pattern
- ✓ All validation commands pass

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `ls -la .claude/hooks/utils/model_extractor.py` - Base file exists
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2` - Template exists
- `python3 -c "import json; exec(open('.claude/hooks/utils/model_extractor.py').read())" 2>&1 | head -5` - Base file has valid Python syntax
- `grep -n "model_extractor.py" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - File is registered in scaffold_service
- `cd tac_bootstrap_cli && python3 -m py_compile tac_bootstrap/application/scaffold_service.py` - scaffold_service has valid syntax
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short -k "model" 2>&1 || true` - Model extractor tests pass (if they exist)
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/application/scaffold_service.py` - Linting passes on modified file
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/application/scaffold_service.py` - Type checking passes

## Notes
- Implementation is based on reference at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/model_extractor.py`
- Session model is immutable per session, so no TTL needed (cache expires when session ends)
- Cache is optimization only; failures gracefully degrade to returning None
- This utility is part of Wave 4 (Hook Utilities) and is Task 30 of 5
- Called via Python import from hooks like `send_event.py`: `from utils.model_extractor import get_model_from_transcript`
- Related to previously implemented utilities: `summarizer.py` (Task 29) and before
- Follow-on tasks will implement other hook utilities in the wave
