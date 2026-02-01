# Feature: Create constants.py Hook Utility

## Metadata
issue_number: `483`
adw_id: `feature_Tac_12_task_31`
issue_json: `{"number": 483, "title": "[Task 31/49] [FEATURE] Create constants.py hook utility", "body": "## Description\n\nCreate a utility with shared constants for hooks.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/constants.py`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`\n\n## Key Features\n- Shared constant definitions\n- API endpoints\n- Default values\n\n## Changes Required\n- Create utility file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include in hook utilities list\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/constants.py`"}`

## Feature Description
This task involves creating a shared constants utility module for hook utilities in TAC Bootstrap. The constants.py file will provide centralized definitions for file system paths, default values, and safety configuration used across multiple hook utilities. This includes both the base implementation file and the Jinja2 template for CLI-generated projects, with proper integration into the scaffold_service.

## User Story
As a hook utility developer
I want to have centralized constant definitions
So that I can maintain consistent values across multiple hook utilities and avoid duplicating common configuration

## Problem Statement
Hook utilities currently lack a centralized location for shared constants like file paths, default timeouts, and safety thresholds. This leads to potential inconsistencies and makes it difficult to update values across multiple utilities.

## Solution Statement
Create a constants.py module that serves as a single source of truth for hook utility configuration. This includes:
1. A base constants.py file in `.claude/hooks/utils/` as the reference implementation
2. A Jinja2 template for CLI generation with proper variable substitution
3. Integration with scaffold_service.py to ensure constants.py is included in hook utility scaffolding

## Relevant Files

### Existing Files to Review
- `.claude/hooks/utils/` - Directory containing hook utility modules
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service responsible for scaffolding hook utilities
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/` - Template directory for hook utilities
- Reference: `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/constants.py` - External reference implementation

### New Files
- `.claude/hooks/utils/constants.py` - Base constants utility file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Jinja2 template for constants.py generation

## Implementation Plan

### Phase 1: Foundation
- Review existing hook utilities to understand required constants
- Study the reference implementation at `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/constants.py`
- Examine scaffold_service.py to understand integration pattern

### Phase 2: Core Implementation
- Create base constants.py file with shared definitions
- Create Jinja2 template with proper variable substitution
- Ensure constants are environment-agnostic and project-agnostic

### Phase 3: Integration
- Update scaffold_service.py to include constants.py in hook utilities list
- Verify proper template path and action type configuration
- Ensure constants.py is generated first before other utilities that may depend on it

## Step by Step Tasks

### Task 1: Review Reference Implementation and Patterns
- Examine the reference constants.py file to understand required constant definitions
- Review existing hook utilities to identify shared values that should be constants
- Study the scaffold_service.py to understand how utilities are scaffolded

### Task 2: Create Base constants.py File
- Create `.claude/hooks/utils/constants.py` with:
  - File system path definitions
  - Default values for hooks
  - Safety configuration and thresholds
  - Documentation for each constant group
- Follow Python best practices for constant definitions (UPPER_CASE naming)

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2`
- Implement proper Jinja2 variable substitution for project-specific values
- Ensure template uses `config` object pattern consistent with other templates
- Add comments explaining configurable values

### Task 4: Update scaffold_service.py Integration
- Verify scaffold_service.py includes constants.py in the hook utilities list
- Confirm correct action type and template path configuration
- Ensure constants.py is scaffolded with proper priority (likely first)

### Task 5: Validation and Testing
- Verify both files exist and are properly formatted
- Test template rendering with sample configuration
- Confirm integration in scaffold_service.py
- Run validation commands to ensure no regressions

## Testing Strategy

### Unit Tests
- Verify constants.py can be imported without errors
- Test that all constants have appropriate values
- Verify Jinja2 template renders correctly with sample config

### Integration Tests
- Verify scaffold_service.py correctly includes constants.py scaffolding action
- Test that generated constants.py from template matches expected format
- Verify no conflicts with other hook utilities

### Edge Cases
- Verify template handles projects with special characters in names
- Test with various configuration values
- Ensure constants don't conflict with Python builtins

## Acceptance Criteria
- Base constants.py file created at `.claude/hooks/utils/constants.py` with complete constant definitions
- Jinja2 template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` with proper syntax
- scaffold_service.py updated to include constants.py in hook utilities scaffolding
- All constants are properly documented with comments
- Template variables use consistent `config` object pattern
- No regressions in existing tests
- Code follows project style and conventions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- Constants should remain environment-agnostic; environment-specific values belong in configuration management
- API endpoints should not be included in constants.py; they belong in environment variables or dedicated config
- Timeout and retry values are service-dependent and should be defined where used, not globally
- This task is part of Wave 4 (Hook Utilities) - Task 31 of 5
- Ensure consistent naming conventions with existing utilities (kebab-case for files, UPPER_CASE for constants)
