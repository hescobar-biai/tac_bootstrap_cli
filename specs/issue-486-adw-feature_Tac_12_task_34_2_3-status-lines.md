# Feature: Create status_lines Directory and status_line_main.py

## Metadata
issue_number: `486`
adw_id: `feature_Tac_12_task_34_2_3`
issue_json: `[Task 34/49] [FEATURE] Create status_lines directory and status_line_main.py`

## Feature Description
Create a lightweight Python script that generates a dynamic status line displaying agent name, model, and git branch. This script will be used by Claude Code's status line configuration to show context information during agentic workflows. The implementation includes both the base script and Jinja2 templates for CLI generation.

## User Story
As a Claude Code user
I want to see status line information about my agent, model, and git branch
So that I can quickly understand the current execution context without switching windows

## Problem Statement
The TAC Bootstrap project needs a status line script that integrates with Claude Code's status bar. Currently, there's no mechanism to display dynamic agent/model/branch information in a single line format.

## Solution Statement
Create a lightweight, non-blocking Python script that:
1. Reads agent name from environment variables (with graceful fallback)
2. Queries the model information (with graceful fallback)
3. Retrieves current git branch via subprocess (with graceful fallback to 'unknown')
4. Outputs a single-line formatted status string: `Agent: <name> | Model: <model> | Branch: <branch>`
5. Follows existing hook patterns (pre_tool_use.py, post_tool_use.py)
6. Is configured as an executable uv run script in settings.json

## Relevant Files

### Existing Files (Reference)
- `.claude/hooks/pre_tool_use.py` - Existing hook pattern for error handling
- `.claude/hooks/post_tool_use.py` - Existing hook pattern for graceful degradation
- `.claude/settings.json` - Configuration that calls status_line_main.py
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service to update with directory/file creation

### New Files
- `.claude/status_lines/status_line_main.py` - Base status line script (executable)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2` - Jinja2 template for CLI generation

## Implementation Plan

### Phase 1: Foundation
- Review existing hook patterns in `.claude/hooks/` to understand error handling and graceful degradation
- Review `scaffold_service.py` to understand directory and file creation patterns
- Review `.claude/settings.json` to understand how status_line_main.py will be invoked

### Phase 2: Core Implementation
- Create `.claude/status_lines/` directory
- Implement `status_line_main.py` with environment variable reading, git branch detection, and formatted output
- Create Jinja2 template `status_line_main.py.j2` for CLI generation (using config context)
- Implement proper error handling with graceful fallbacks to 'unknown'

### Phase 3: Integration
- Update `scaffold_service.py._add_directories()` to create `status_lines` directory
- Update `scaffold_service.py._add_claude_files()` to include `status_line_main.py` file creation
- Verify shebang directive and executable permissions

## Step by Step Tasks

### Task 1: Analyze Existing Patterns
- Read `.claude/hooks/pre_tool_use.py` to understand error handling patterns
- Read `.claude/hooks/post_tool_use.py` to understand graceful degradation
- Review `.claude/settings.json` to locate statusLineCommand configuration
- Document the pattern for environment variable reading and subprocess calls

### Task 2: Create Directory and Base Script
- Create `.claude/status_lines/` directory
- Create `status_line_main.py` with:
  - Shebang: `#!/usr/bin/env python3`
  - Read CLAUDE_AGENT_NAME from environment (fallback: 'unknown')
  - Read CLAUDE_MODEL from environment (fallback: 'unknown')
  - Execute `git rev-parse --abbrev-ref HEAD` for branch (fallback: 'unknown')
  - Format output: `Agent: <name> | Model: <model> | Branch: <branch>`
  - Exit with code 0 always (non-blocking)
  - Handle all exceptions gracefully

### Task 3: Create Jinja2 Template
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/` directory
- Create `status_line_main.py.j2` template:
  - Use config.project.name, config.project.description for project context (if needed)
  - Keep template minimal; agent/model/branch are runtime values only
  - Match the base script structure exactly

### Task 4: Update scaffold_service.py
- Add `'status_lines'` to `_add_directories()` method (add alongside 'hooks', 'commands', 'agents')
- Add `'status_line_main.py'` to `_add_claude_files()` method (add alongside existing files)
- Verify directory creation order (status_lines directory must exist before file creation)

### Task 5: Validation
- Execute `uv run pytest tests/ -v --tb=short` to verify no regressions
- Execute `uv run ruff check .` for linting
- Execute `uv run mypy tac_bootstrap/` for type checking
- Test status_line_main.py directly: `uv run .claude/status_lines/status_line_main.py`
- Verify output format matches: `Agent: unknown | Model: unknown | Branch: unknown` (no env vars set)

## Testing Strategy

### Unit Tests
- Test status_line_main.py with various environment variable combinations
- Test graceful fallback when git command fails (non-git directory)
- Test output format consistency with pipe separators
- Test exit code is always 0

### Edge Cases
- Missing CLAUDE_AGENT_NAME environment variable → defaults to 'unknown'
- Missing CLAUDE_MODEL environment variable → defaults to 'unknown'
- Git not installed or current directory not a git repo → defaults to 'unknown'
- Detached HEAD state → outputs detached HEAD ref instead of branch name
- Empty or whitespace-only environment variables → treated as missing

## Acceptance Criteria
1. `.claude/status_lines/status_line_main.py` exists and is executable
2. Script outputs single-line formatted status: `Agent: <name> | Model: <model> | Branch: <branch>`
3. Script has shebang directive: `#!/usr/bin/env python3`
4. All exceptions are caught and result in graceful 'unknown' fallback
5. Exit code is always 0
6. `tac_bootstrap_cli/tac_bootstrap/templates/claude/status_lines/status_line_main.py.j2` template created
7. `scaffold_service.py` updated to create status_lines directory and file
8. All tests pass with zero regressions
9. Code passes ruff linting and mypy type checking

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `uv run .claude/status_lines/status_line_main.py` - Smoke test
- Verify output format: `Agent: unknown | Model: unknown | Branch: unknown`

## Notes
- Script follows existing hook patterns (pre_tool_use.py, post_tool_use.py) for consistency
- Environment variables CLAUDE_AGENT_NAME and CLAUDE_MODEL are set by Claude Code at runtime
- Git branch detection uses `git rev-parse --abbrev-ref HEAD` which handles most cases
- Status line is informational only—never blocks or fails (exit code 0 always)
- Jinja2 template keeps static context (project info); runtime values from environment/subprocess
- Shebang directive allows execution via `uv run` as configured in settings.json
- This is Wave 5, Task 34 of the TAC Bootstrap implementation plan
