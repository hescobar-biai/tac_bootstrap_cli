# Feature: Create llm/ utilities subdirectory

## Metadata
issue_number: `484`
adw_id: `feature_Tac_12_task_32`
issue_json: `[Task 32/49] [FEATURE] Create llm/ utilities subdirectory`

## Feature Description
Create LLM-related utilities for hooks, establishing a subdirectory structure with Jinja2 templates for the CLI generator. This includes three provider implementations (Anthropic, OpenAI, Ollama) that handle completion message generation through a minimal, composable interface.

## User Story
As a CLI generator developer
I want to create LLM utility templates for hook scaffolding
So that generated projects can leverage multiple LLM providers for hook automation

## Problem Statement
The hook utilities structure needs a dedicated LLM subdirectory with provider-specific implementations. Currently, base directory files exist at `/.claude/hooks/utils/llm/` but corresponding Jinja2 templates are not properly set up for the CLI generator. The scaffold_service.py needs to be updated to handle llm/ directory creation during project generation.

## Solution Statement
Implement a three-provider approach (Anthropic, OpenAI, Ollama) with minimal, self-contained modules. Each provider exposes `prompt_llm()` and `generate_completion_message()` functions. The `__init__.py` re-exports all three providers, using Anthropic as the implicit default through the last import. Templates mirror the base directory structure exactly, ensuring fidelity in generated projects. The scaffold_service.py copies all template files during project generation.

## Relevant Files
Key files for implementing this feature:

- `/.claude/hooks/utils/llm/` - Base directory (source of truth for implementations)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` - Jinja2 template directory
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Service responsible for copying templates
- `tac_bootstrap_cli/tac_bootstrap/domain/config.py` - Configuration models
- `PLAN_TAC_BOOTSTRAP.md` - Master plan with all tasks and wave information

### New Files
Template files to create in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`:
- `__init__.py.j2` - Package initialization re-exporting all three providers
- `anth.py.j2` - Anthropic provider implementation
- `oai.py.j2` - OpenAI provider implementation
- `ollama.py.j2` - Ollama provider implementation

## Implementation Plan

### Phase 1: Foundation
- Examine base directory files at `/.claude/hooks/utils/llm/` to understand current implementations
- Verify scaffold_service.py infrastructure for template handling
- Ensure templates directory structure is properly organized

### Phase 2: Core Implementation
- Create `__init__.py.j2` template with re-exports from all three providers
- Create `anth.py.j2` template for Anthropic provider implementation
- Create `oai.py.j2` template for OpenAI provider implementation
- Create `ollama.py.j2` template for Ollama provider implementation

### Phase 3: Integration
- Update scaffold_service.py to include llm/ directory creation and file copies
- Verify all templates are properly registered in the scaffold service
- Test template generation with CLI to ensure correctness

## Step by Step Tasks
Execute each step in order.

### Task 1: Examine base directory implementations
- Read `/.claude/hooks/utils/llm/__init__.py` to understand structure and provider re-exports
- Read `/.claude/hooks/utils/llm/anth.py` to document Anthropic implementation
- Read `/.claude/hooks/utils/llm/oai.py` to document OpenAI implementation
- Read `/.claude/hooks/utils/llm/ollama.py` to document Ollama implementation

### Task 2: Create __init__.py.j2 template
- Create template that re-exports from all three providers
- Ensure Anthropic is the implicit default through last import
- Add docstring documenting provider usage and name collision handling

### Task 3: Create anth.py.j2 template
- Implement `prompt_llm()` function using Anthropic client
- Implement `generate_completion_message()` helper function
- Use ANTHROPIC_API_KEY environment variable
- Return None on any exception (fail fast)

### Task 4: Create oai.py.j2 template
- Implement `prompt_llm()` function using OpenAI client
- Implement `generate_completion_message()` helper function
- Use OPENAI_API_KEY environment variable
- Return None on any exception (fail fast)

### Task 5: Create ollama.py.j2 template
- Implement `prompt_llm()` function using Ollama HTTP API
- Implement `generate_completion_message()` helper function
- Use provider-specific environment variables
- Return None on any exception (fail fast)

### Task 6: Verify scaffold_service.py registration
- Check that scaffold_service.py includes llm/ directory creation
- Verify all four template files are registered for copying
- Ensure templates directory contains all .j2 files

### Task 7: Run validation tests
- Execute `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Execute `cd tac_bootstrap_cli && uv run ruff check .`
- Execute `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Execute `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
- Test template file existence in templates directory
- Test scaffold_service.py correctly copies llm/ templates
- Test generated __init__.py properly re-exports all three providers
- Test each provider module can be imported independently

### Edge Cases
- Verify template rendering with special characters in config values
- Test scaffold_service behavior when templates directory is missing
- Test provider error handling when API keys are missing
- Verify each provider returns None on exceptions (broad error catching)

## Acceptance Criteria
- All four template files exist in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
- Templates are exact mirrors of base directory implementations (with Jinja2 placeholders)
- scaffold_service.py is updated to copy llm/ directory during project generation
- Generated projects contain properly functioning llm/ utilities with all three providers
- All unit tests pass with zero regressions
- Linting and type checking pass without errors
- CLI smoke test executes successfully

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The base directory files at `/.claude/hooks/utils/llm/` are the source of truth; templates must mirror these exactly
- Each provider uses provider-specific environment variables (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
- No centralized configuration is needed; each provider initializes itself at import/call time
- Hooks should fail fast on errors; no fallback chains or retry logic
- The current three-provider approach is sufficient; no additional helper functions or abstractions needed beyond prompt_llm() and generate_completion_message()
- The last import in __init__.py (Anthropic) serves as the implicit default for direct `from llm import prompt_llm` calls
- This is part of Wave 4 - Hook Utilities (Task 32 of 5)
