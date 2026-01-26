# Feature: Add ollama.py.j2 Ollama LLM Wrapper Template

## Metadata
issue_number: `251`
adw_id: `feature_Tac_9_task_10_v2`
issue_json: `{"number":251,"title":"Add ollama.py.j2 Ollama LLM wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_10_v2\n\n**Description:**\nCreate Jinja2 template for Ollama local LLM wrapper. Provides same interface as cloud providers for local model inference.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/ollama.py` (CREATE - rendered)"}`

## Feature Description
This feature creates a Jinja2 template for the Ollama LLM wrapper utility (`ollama.py.j2`). The template preserves the complete functionality of the source implementation, providing two core functions: `prompt_llm()` for direct LLM prompting and `generate_completion_message()` for AI-friendly task completion messages. The template maintains minimal templating (shebang and docstring only) to ensure the wrapper remains a standardized, reusable utility across all generated projects. Unlike cloud providers (OpenAI, Anthropic), Ollama is a local inference engine accessed via HTTP API at `http://localhost:11434/v1`, with simplified configuration and no API authentication required. The template mirrors the interface of the OpenAI and Anthropic wrappers exactly for consistency.

## User Story
As a TAC Bootstrap developer
I want to create a Jinja2 template for the Ollama LLM wrapper
So that generated projects include a consistent, working utility for interacting with local Ollama models through hook scripts

## Problem Statement
The TAC Bootstrap CLI needs to template the Ollama LLM wrapper utility (`ollama.py`) for inclusion in generated projects. The source implementation exists at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` but has not yet been converted into a reusable Jinja2 template. Without this template, generated projects will lack a standardized way to interact with local Ollama models from hook scripts. The Ollama wrapper complements the OpenAI and Anthropic wrappers to provide developers with multiple LLM options (cloud, commercial, and local).

## Solution Statement
Create a Jinja2 template (`ollama.py.j2`) that:

1. Preserves the exact structure, logic, and both functions from the source implementation
2. Applies minimal templating only to the shebang line and docstring project name
3. Maintains the executable nature with uv script metadata (`#!/usr/bin/env -S uv run --script` and the `# /// script` block)
4. Uses the default endpoint `http://localhost:11434/v1` (configurable via `OLLAMA_BASE_URL` environment variable)
5. Uses the model identifier `ollama` (let the Ollama server handle model selection)
6. Keeps all environment variable handling (`OLLAMA_BASE_URL` for endpoint, optional `OLLAMA_API_KEY` for consistency) identical to source
7. Preserves the silent error handling strategy (returns `None` on API errors)
8. Includes both working functions: `prompt_llm()` and `generate_completion_message()`
9. Mirrors the OpenAI and Anthropic template structure exactly for consistency
10. Uses only standard dependencies: `python-dotenv` and `requests` for HTTP calls (no special Ollama SDK)

The template will be placed in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` and rendered during project generation to `.claude/hooks/utils/llm/ollama.py`.

## Relevant Files

### Existing Files (for context)
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` - Source implementation file with both functions
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/oai.py` - OpenAI implementation for reference
- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/llm/anth.py` - Anthropic implementation for reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - OpenAI template for pattern reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` - Anthropic template for pattern reference
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
3. Review the OpenAI and Anthropic templates to understand the exact pattern and conventions to follow
4. Understand Ollama's API differences (local, HTTP-based, model identifier semantics)

### Phase 2: Core Implementation
Create the Jinja2 template by preserving the source code with minimal templating.

**Tasks:**
1. Create `ollama.py.j2` template file in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/`
2. Copy complete source code from `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py`
3. Apply templating only to:
   - Shebang line: `#!/usr/bin/env -S uv run --script`
   - Module docstring: Use `{{ config.project.name }}` for project name
4. Verify both functions are present and unchanged:
   - `prompt_llm(prompt_text)` - Direct LLM prompting via Ollama HTTP API
   - `generate_completion_message()` - Task completion messages
5. Verify uv script metadata block is preserved exactly with standard dependencies only

### Phase 3: Integration & Validation
Ensure the template integrates correctly with the project structure.

**Tasks:**
1. Verify template rendering would produce valid Python executable
2. Test template syntax with Jinja2 validation
3. Verify consistency with the OpenAI and Anthropic template structure
4. Run tests to ensure no regressions

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Source Implementation
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/llm/ollama.py` completely
- Confirm both functions exist: `prompt_llm()`, `generate_completion_message()`
- Verify shebang line format: `#!/usr/bin/env -S uv run --script`
- Verify uv script metadata block with exact Python version and dependencies
- Note the default endpoint and model identifier used
- Verify the function uses HTTP requests (not a special SDK)
- Document any observations about the implementation

### Task 2: Verify Directory Structure
- Confirm directory `/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` exists
- Check if `__init__.py.j2` exists in that directory
- Verify parent directories exist and have appropriate permissions

### Task 3: Review OpenAI and Anthropic Template Patterns
- Read the OpenAI template file to understand the exact templating pattern
- Read the Anthropic template file to understand the exact templating pattern
- Identify the specific lines that use Jinja2 templating
- Note the structure for how docstrings are templated with `{{ config.project.name }}`
- Understand how the shebang and uv script metadata are preserved

### Task 4: Create ollama.py.j2 Template
- Create file `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`
- Copy entire source code from the verified source file
- Apply templating to docstring: `"""Base Ollama LLM prompting method for local model inference in {{ config.project.name }}.`
- Keep shebang line identical: `#!/usr/bin/env -S uv run --script`
- Keep all code logic identical with NO changes to:
  - `prompt_llm()` function logic and implementation
  - `generate_completion_message()` function logic and implementation
  - Environment variable handling: `OLLAMA_BASE_URL`, optional `OLLAMA_API_KEY`
  - Error handling: Silent returns of `None`
  - `main()` CLI interface
  - uv script metadata block with standard dependencies only
- Verify template file has correct permissions (readable by template engine)

### Task 5: Validate Template Structure
- Check template syntax is valid Jinja2 (no syntax errors)
- Verify template would render correctly with sample config
- Verify rendered output would be valid Python syntax
- Verify rendered output would be executable

### Task 6: Verify Consistency with OpenAI and Anthropic Templates
- Compare line-by-line structure of all three templates
- Ensure all templates follow identical patterns for:
  - Shebang line
  - Docstring with `{{ config.project.name }}`
  - uv script metadata block
  - Function signatures and error handling
- Document any intentional differences (e.g., endpoint URL, model identifier, imports)

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
- Default endpoint is `http://localhost:11434/v1` in rendered output
- Model identifier is `ollama` in rendered output

## Acceptance Criteria
- [ ] Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`
- [ ] Template contains both functions: `prompt_llm()`, `generate_completion_message()`
- [ ] Template preserves exact source implementation logic without modifications
- [ ] Default endpoint is set to `http://localhost:11434/v1` (configurable via `OLLAMA_BASE_URL`)
- [ ] Model identifier is `ollama` (server-managed model selection)
- [ ] Only shebang and docstring use Jinja2 templating
- [ ] uv script metadata block preserved exactly with only standard dependencies
- [ ] Rendered output is valid executable Python with correct shebang
- [ ] Template passes Jinja2 syntax validation
- [ ] Rendered sample output passes Python syntax validation
- [ ] Template structure mirrors OpenAI and Anthropic templates exactly
- [ ] No test regressions in existing test suite

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_9_task_10_v2 && python -m pytest tests/ -v --tb=short` - Run tests to verify no regressions
- `python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/ollama.py.j2'); print('Template syntax OK')"` - Validate Jinja2 syntax
- `python -c "import ast; code = open('tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2').read(); print('Template file exists')"` - Verify file exists
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/` - Lint template directory
- `ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/` - Verify directory structure

## Notes

### Ollama Architecture
Ollama is a local LLM inference engine that:
- Runs as a standalone service (separate from the application)
- Exposes an OpenAI-compatible API at `http://localhost:11434/v1`
- Manages its own model downloads and switching
- Requires no API key authentication
- Is designed for development and local deployment

This simplifies the wrapper compared to cloud APIs because:
- No SDK dependency needed (uses plain HTTP via `requests`)
- No API key management required
- Reduced error cases (local service, fewer network timeouts)
- Server handles model selection based on deployment config

### Endpoint Configuration
The template uses `http://localhost:11434/v1` as the default endpoint:
- The `/v1` suffix indicates OpenAI-compatible API format
- Configurable via `OLLAMA_BASE_URL` environment variable for non-standard deployments
- Matches the environment variable pattern used in OpenAI and Anthropic implementations
- Allows users to customize without code changes

### Model Identifier Philosophy
The template uses `ollama` as the model identifier:
- Unlike cloud providers where you specify exact model names (e.g., `gpt-4o-mini`, `claude-3-5-haiku`)
- Ollama's OpenAI-compatible API uses `ollama` as a special identifier
- The actual model selection is handled server-side based on Ollama's configuration
- This is idiomatic for Ollama and simplest for users

### Template Variables Philosophy
Only two template variables are used:
- `{{ config.project.name }}` in the module docstring
- The shebang line and all code logic are NOT templated

This follows the pattern of the OpenAI and Anthropic templates where utility code is kept generic and configuration-specific values are minimal. The wrapper uses environment variables (`OLLAMA_BASE_URL`, optional `OLLAMA_API_KEY`) at runtime for configuration, not template variables.

### Parallel Implementation with OpenAI and Anthropic
This Ollama template is designed to mirror the OpenAI and Anthropic templates exactly in structure:
- Identical function signatures
- Identical error handling (silent returns of `None`)
- Identical Jinja2 templating patterns
- Only the API endpoint, model identifier, and HTTP client implementation differ

This consistency makes it easy for developers to understand all three implementations and switch between them.

### Executable Script Preservation
The template preserves the uv script metadata block (`# /// script`) because:
- This is essential for running the script as a standalone executable
- The shebang `#!/usr/bin/env -S uv run --script` enables direct execution
- This matches the source implementation's design as a utility script

### Error Handling Strategy
The silent error handling (returning `None` instead of raising exceptions) is intentional:
- Allows graceful degradation in hook contexts
- Permits workflows to continue if Ollama service is unavailable
- Caller can handle `None` responses appropriately
- Not configurable - this is part of the design

### Dependencies
Unlike cloud SDKs, Ollama wrapper uses only standard dependencies:
- `python-dotenv` - For environment variable loading (consistent with other wrappers)
- `requests` - For HTTP API calls (standard library alternative available but requests is standard)
- No Ollama-specific SDK needed (uses OpenAI-compatible API)

