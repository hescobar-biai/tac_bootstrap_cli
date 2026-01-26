# Feature: Add ollama.py.j2 Ollama LLM Wrapper Template

## Metadata
issue_number: `251`
adw_id: `feature_Tac_9_task_10`
issue_json: `{"number":251,"title":"Add ollama.py.j2 Ollama LLM wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_10\n\n**Description:**\nCreate Jinja2 template for Ollama local LLM wrapper. Provides same interface as cloud providers for local model inference.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/ollama.py` (CREATE - rendered)"}`

## Feature Description
This feature creates a Jinja2 template for the Ollama LLM wrapper utility (`ollama.py.j2`). The template preserves the complete functionality of the source implementation, providing two core functions: `prompt_llm()` for direct LLM prompting and `generate_completion_message()` for AI-friendly task completion messages. The template maintains minimal templating (shebang and docstring only) to ensure the wrapper remains a standardized, reusable utility across all generated projects while preserving the standalone executable nature with uv script metadata. The template uses HTTP REST API to communicate with a local Ollama instance running on localhost:11434 (or remotely via OLLAMA_BASE_URL environment variable), defaulting to the 'mistral' model with environment variable override via OLLAMA_MODEL.

## User Story
As a TAC Bootstrap developer
I want to create a Jinja2 template for the Ollama LLM wrapper
So that generated projects include a consistent, working utility for interacting with local/remote Ollama instances through hook scripts

## Problem Statement
The TAC Bootstrap CLI needs to template the Ollama LLM wrapper utility (`ollama.py`) for inclusion in generated projects. The source implementation exists at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` but has not yet been converted into a reusable Jinja2 template. Without this template, generated projects will lack a standardized way to interact with a local Ollama instance from hook scripts. This is valuable for developers who want to use local models instead of cloud APIs.

## Solution Statement
Create a Jinja2 template (`ollama.py.j2`) that:

1. Preserves the exact structure, logic, and both functions from the source implementation
2. Applies minimal templating only to the shebang line and docstring project name
3. Maintains the executable nature with uv script metadata (`#!/usr/bin/env -S uv run --script` and the `# /// script` block)
4. Uses HTTP REST API (urllib) to communicate with Ollama at localhost:11434 by default
5. Supports environment variable configuration: `OLLAMA_BASE_URL` (default: http://localhost:11434) and `OLLAMA_MODEL` (default: 'mistral')
6. Keeps all environment variable handling identical to Anthropic/OpenAI wrappers
7. Preserves the silent error handling strategy (returns `None` on API errors)
8. Includes both working functions: `prompt_llm()` and `generate_completion_message()`
9. Uses fixed parameters: temperature=0.7, max_tokens=100, timeout=30s
10. Mirrors the Anthropic and OpenAI template structures exactly for consistency

The template will be placed in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` and rendered during project generation to `.claude/hooks/utils/llm/ollama.py`.

## Relevant Files

### Existing Files (for context)
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` - Source implementation file with both functions
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/anth.py` - Parallel Anthropic implementation for reference
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` - Parallel OpenAI implementation for reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` - Anthropic template for reference pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - OpenAI template for reference pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Existing template structure
- `config.yml` - Project configuration file

### New Files
1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` (CREATE) - The Jinja2 template
2. `.claude/hooks/utils/llm/ollama.py` (CREATE - rendered output after project generation)

## Implementation Plan

### Phase 1: Foundation
Prepare the directory structure and examine the source implementation to understand the code thoroughly.

**Tasks:**
1. Verify source implementation exists and contains both functions
2. Confirm directory structure `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` exists
3. Review the Anthropic and OpenAI templates to understand the exact pattern and conventions to follow

### Phase 2: Core Implementation
Create the Jinja2 template by preserving the source code with minimal templating.

**Tasks:**
1. Create `ollama.py.j2` template file in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
2. Copy complete source code from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py`
3. Apply templating only to:
   - Shebang line: `#!/usr/bin/env -S uv run --script`
   - Module docstring: Use `{{ config.project.name }}` for project name
4. Verify both functions are present and unchanged:
   - `prompt_llm(prompt_text)` - Direct LLM prompting
   - `generate_completion_message()` - Task completion messages
5. Verify uv script metadata block is preserved exactly
6. Verify environment variable handling for OLLAMA_BASE_URL and OLLAMA_MODEL

### Phase 3: Integration & Validation
Ensure the template integrates correctly with the project structure.

**Tasks:**
1. Verify template rendering would produce valid Python executable
2. Test template syntax with Jinja2 validation
3. Verify consistency with the Anthropic and OpenAI template structures
4. Run tests to ensure no regressions

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Source Implementation
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` completely
- Confirm both functions exist: `prompt_llm()`, `generate_completion_message()`
- Verify shebang line format: `#!/usr/bin/env -S uv run --script`
- Verify uv script metadata block with exact Python version and dependencies
- Identify environment variable names used: OLLAMA_BASE_URL, OLLAMA_MODEL
- Verify default values: base_url=http://localhost:11434, model='mistral'
- Verify fixed parameters: temperature=0.7, max_tokens=100, timeout=30s
- Document any observations about the implementation

### Task 2: Verify Directory Structure
- Confirm directory `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` exists
- Check if `__init__.py.j2` exists in that directory
- Verify parent directories exist and have appropriate permissions

### Task 3: Review Reference Template Patterns
- Read the Anthropic template file to understand the exact templating pattern
- Read the OpenAI template file to understand OpenAI-specific pattern
- Identify the specific lines that use Jinja2 templating
- Note the structure for how docstrings are templated with `{{ config.project.name }}`
- Understand how the shebang and uv script metadata are preserved
- Document any differences between Anthropic and OpenAI patterns

### Task 4: Create ollama.py.j2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`
- Copy entire source code from the verified source file
- Replace docstring with: `"""Base Ollama LLM prompting method using local model for {{ config.project.name }}.`
- Keep shebang line identical: `#!/usr/bin/env -S uv run --script`
- Keep all code logic identical with NO changes to:
  - `prompt_llm()` function logic and implementation
  - `generate_completion_message()` function logic and implementation
  - Environment variable handling: `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `ENGINEER_NAME`
  - Error handling: Silent returns of `None`
  - `main()` CLI interface
  - uv script metadata block
  - HTTP REST API communication with urllib
- Verify template file has correct permissions (readable by template engine)

### Task 5: Validate Template Structure
- Check template syntax is valid Jinja2 (no syntax errors)
- Verify template would render correctly with sample config
- Verify rendered output would be valid Python syntax
- Verify rendered output would be executable

### Task 6: Verify Consistency with Reference Templates
- Compare line-by-line structure with both Anthropic and OpenAI templates
- Ensure all three templates follow identical patterns for:
  - Shebang line
  - Docstring with `{{ config.project.name }}`
  - uv script metadata block
  - Function signatures and error handling
  - Both functions present
- Document any intentional differences (e.g., model names, API endpoints, library imports)

### Task 7: Run Validation Commands
- Run Jinja2 syntax validation on the template
- Run Python syntax check on a rendered sample
- Verify template integration with existing hooks structure
- Run tests to ensure no regressions

## Testing Strategy

### Unit Tests
- Template Jinja2 syntax validation passes without errors
- Template renders with sample `config` object without errors
- Rendered Python file has valid syntax (can be parsed by Python AST)

### Edge Cases
- Template works with project names containing spaces
- Template works with project names containing special characters
- Shebang line is preserved in rendered output
- uv script metadata block is preserved exactly in rendered output
- Both functions are present in rendered output
- Environment variable defaults are correctly used in rendered output
- HTTP REST API endpoint construction is correct

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`
- [ ] Template contains both functions: `prompt_llm()`, `generate_completion_message()`
- [ ] Template preserves exact source implementation logic without modifications
- [ ] Environment variables configured: OLLAMA_BASE_URL (default: http://localhost:11434), OLLAMA_MODEL (default: 'mistral')
- [ ] Only shebang and docstring use Jinja2 templating
- [ ] uv script metadata block preserved exactly
- [ ] Rendered output is valid executable Python with correct shebang
- [ ] Template passes Jinja2 syntax validation
- [ ] Rendered sample output passes Python syntax validation
- [ ] Template structure mirrors Anthropic and OpenAI templates exactly
- [ ] HTTP REST API calls use urllib for communication
- [ ] Fixed parameters used: temperature=0.7, max_tokens=100, timeout=30s
- [ ] No test regressions in existing test suite

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_9_task_10 && python -m pytest tests/ -v --tb=short` - Run tests to verify no regressions
- `python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/ollama.py.j2'); print('Template syntax OK')"` - Validate Jinja2 syntax
- `python -c "import ast; code = open('tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2').read(); print('Template file exists')"` - Verify file exists
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/` - Lint template directory
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` - Verify directory structure

## Notes

### Model and Configuration Selection
The Ollama template uses:
- Default base URL: `http://localhost:11434` with environment variable `OLLAMA_BASE_URL` override
- Default model: `'mistral'` (lightweight, fast, widely available) with environment variable `OLLAMA_MODEL` override
- Fixed parameters: temperature=0.7, max_tokens=100, timeout=30s
- HTTP REST API via urllib for minimal dependencies

This approach:
- Supports both local and remote Ollama instances
- Maintains simplicity without additional LLM-specific libraries
- Mirrors the pattern of environment variable configuration used in Anthropic/OpenAI wrappers
- Uses sensible defaults while allowing customization

### Template Variables Philosophy
Only two template variables are used:
- `{{ config.project.name }}` in the module docstring
- The shebang line and all code logic are NOT templated

This follows the pattern of the Anthropic and OpenAI templates where utility code is kept generic and configuration-specific values are minimal. The wrapper uses environment variables (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `ENGINEER_NAME`) at runtime for configuration, not template variables.

### Parallel Implementation with Anthropic and OpenAI
This Ollama template is designed to mirror both the Anthropic (`anth.py.j2`) and OpenAI (`oai.py.j2`) templates exactly in structure:
- Identical function signatures
- Identical error handling (silent returns of `None`)
- Identical Jinja2 templating patterns
- Only the model name, API endpoint, and client library differ

This consistency makes it easy for developers to understand all three implementations and switch between them based on their preferences (cloud vs. local inference).

### HTTP REST API vs. Library
The template uses HTTP REST API via urllib instead of the `ollama-python` library because:
- Minimizes external dependencies
- Matches the pattern already established in the codebase
- Provides direct control over error handling and timeouts
- Keeps the implementation simple and transparent

### Error Handling Strategy
The silent error handling (returning `None` instead of raising exceptions) is intentional:
- Allows graceful degradation in hook contexts
- Permits workflows to continue if Ollama is unavailable
- Caller can handle `None` responses appropriately
- Not configurable - this is part of the design
- Consistent with Anthropic and OpenAI implementations

### Streaming Not Supported
The template implements complete responses only (no streaming) because:
- Simplifies implementation and error handling
- Matches existing Anthropic and OpenAI wrappers
- Streaming can be added as a future enhancement if needed
- Sufficient for task completion messages and general prompting
