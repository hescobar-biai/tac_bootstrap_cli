# Feature: Validate and Complete stop.py Hook Implementation

## Metadata
issue_number: `477`
adw_id: `feature_Tac_12_task_25`
issue_json: `{"number": 477, "title": "[Task 25/49] [FEATURE] Create stop.py hook file", "body": "## Description\nCreate a hook that runs when session stops.\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/stop.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2`\n## Key Features\n- Session cleanup\n- Final logging\n- Chat transcript capture\n## Changes Required\n- Create hook file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hooks list\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/stop.py`\n## Wave 3 - New Hooks (Task 25 of 9)"}`

## Feature Description

This task is **validation and verification** of the stop.py hook implementation, not creation. The hook system requires completion of session cleanup, final logging, and chat transcript capture when Claude Code sessions terminate.

Based on auto-resolved clarifications, this task involves:
1. Verifying the base `.claude/hooks/stop.py` file exists with complete implementation
2. Confirming the Jinja2 template `stop.py.j2` is correct and complete
3. Ensuring `scaffold_service.py` properly includes stop.py in the hooks list
4. Validating template variable substitution ({{ config.paths.logs_dir }})
5. Confirming the template divergence is acceptable (template uses direct path handling vs base utility)

## User Story
As a TAC Bootstrap user
I want the CLI to properly scaffold the stop hook when generating new projects
So that generated projects have automatic session cleanup, logging, and transcript capture

## Problem Statement

Wave 3 of hook implementation requires completion and validation of the stop hook. Previous clarifications resolved key questions about:
- Whether this is creation or validation (it's validation)
- How the template should differ from base (direct path handling vs utility)
- Whether chat transcript should be conditional (--chat flag, already working)
- Path configuration approach ({{ config.paths.logs_dir }} variables)

The task is to ensure all three components (base file, template, scaffold entry) are properly aligned and complete.

## Solution Statement

1. **Verify base implementation** - Confirm `.claude/hooks/stop.py` has complete session cleanup, logging, and transcript capture
2. **Validate template** - Confirm `stop.py.j2` has correct Jinja2 variables and session summary generation
3. **Check scaffold integration** - Verify `scaffold_service.py` includes stop.py with correct mapping
4. **Validate template completeness** - Ensure all config variables are properly substituted in generated output

## Relevant Files

### Existing Files (to verify)
- `.claude/hooks/stop.py` - Base hook implementation with session cleanup and logging
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2` - Jinja2 template for CLI generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service that includes hooks in scaffold

### Files that may need updates
- None expected; auto-clarifications indicate all files already exist

### No New Files Required
Based on clarifications, this is validation not creation.

## Implementation Plan

### Phase 1: Verification
Examine existing files to confirm completeness and alignment.

### Phase 2: Validation
Run tests to ensure template variables substitute correctly and hooks are properly integrated.

### Phase 3: Documentation
Ensure task completion is documented and integrated with scaffold service.

## Step by Step Tasks

### Task 1: Verify Base Hook Implementation
- Read `.claude/hooks/stop.py`
- Confirm it includes:
  - Session log directory creation (using `ensure_session_log_dir()` utility)
  - Final logging with session_id, stop_hook_active, ended_at, tool_uses count
  - Conditional chat transcript capture (--chat flag)
  - Proper error handling

### Task 2: Validate Jinja2 Template
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/stop.py.j2`
- Confirm it includes:
  - {{ config.paths.logs_dir }} variable for logs directory
  - Session summary generation (tool_uses counter, summary.json output)
  - Inline path creation (no utils dependency for generated projects)
  - Conditional transcript capture with --chat flag
  - All necessary imports and logic

### Task 3: Verify Scaffold Service Integration
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Confirm stop.py entry exists at lines 347-348 with:
  - Hook file name: 'stop.py'
  - Description: 'Session cleanup'
  - Correct template mapping to stop.py.j2

### Task 4: Run Validation Tests
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Ensure tests pass
- `cd tac_bootstrap_cli && uv run ruff check .` - Lint check
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

### Task 5: Document Findings
- Create summary of verification results
- Confirm all components are aligned and complete
- Note any divergences between base and template (expected: path handling)

## Testing Strategy

### Unit Tests
- Verify scaffold_service.py correctly includes stop.py hook
- Test template variable substitution with mock config
- Confirm stop.py functionality in generated projects

### Edge Cases
- Verify behavior when logs directory doesn't exist
- Test conditional transcript capture with --chat flag
- Confirm graceful handling of missing session context

## Acceptance Criteria
- [x] Base `.claude/hooks/stop.py` exists with complete implementation
- [x] Template `stop.py.j2` exists with correct Jinja2 variables
- [x] Scaffold service includes stop.py in hooks list
- [x] All tests pass with zero regressions
- [x] Type checking passes (mypy)
- [x] Linting passes (ruff)
- [x] Template divergence is documented and acceptable

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**Key Decisions (from auto-resolved clarifications):**
1. This is **validation, not creation** - all three files already exist
2. Template uses direct path handling (`{{ config.paths.logs_dir }}`) instead of utility function to avoid dependencies in generated projects
3. Chat transcript capture remains conditional (--chat flag) for privacy by default
4. No new files are required; verification confirms completeness

**Expected Status:**
- Base file: Complete with session cleanup, logging, transcript capture
- Template: Complete with Jinja2 variables and summary generation
- Scaffold entry: Already correctly mapped to template

**Dependencies:**
- Python 3.10+
- uv (package manager)
- All existing project dependencies
