# Feature: Add ollama.py.j2 Ollama LLM wrapper template

## Metadata
- **issue_number:** 251
- **adw_id:** feature_Tac_9_task_10_v4
- **issue_title:** Add ollama.py.j2 Ollama LLM wrapper template
- **issue_json:**
```json
{
  "number": 251,
  "title": "Add ollama.py.j2 Ollama LLM wrapper template",
  "body": "Create Jinja2 template for Ollama local LLM wrapper. Provides same interface as cloud providers for local model inference."
}
```

## Feature Description

Create a Jinja2 template for an Ollama local LLM wrapper that provides the same interface as existing cloud provider wrappers (OpenAI and Anthropic). The wrapper enables using Ollama's OpenAI-compatible endpoint for local model inference, allowing developers to test and prototype with local language models without requiring cloud API keys.

The implementation uses Ollama's OpenAI-compatible endpoint (`http://localhost:11434/v1`), maintaining consistency with existing wrapper patterns while requiring no new dependencies beyond `openai` and `python-dotenv`.

## User Story

As a **developer**
I want to **use local Ollama models via the same interface as OpenAI and Anthropic wrappers**
So that **I can prototype and test with local LLMs without cloud API dependencies during development**

## Problem Statement

The TAC Bootstrap project currently provides LLM wrappers for OpenAI (`oai.py.j2`) and Anthropic (`anth.py.j2`), but lacks a wrapper for local model inference. Developers who want to use local Ollama models during development either need to:
1. Implement their own wrapper each time
2. Maintain a separate local integration
3. Pay for cloud API calls during development and testing

An Ollama wrapper template would standardize local model usage and simplify the development workflow by providing a consistent interface across all provider options.

## Solution Statement

Create `ollama.py.j2` as a static Jinja2 template that:
- Mirrors the exact structure and interface of `oai.py` and `anth.py`
- Uses OpenAI SDK with Ollama's OpenAI-compatible endpoint (`http://localhost:11434/v1`)
- Implements the same three-function interface: `prompt_llm()`, `generate_completion_message()`, and `main()`
- Uses hardcoded model ('llama3.2') and parameters (max_tokens=100, temperature=0.7)
- Includes identical error handling: return `None` on any exception
- Provides a rendered version at `.claude/hooks/utils/llm/ollama.py`

The implementation is deliberately simple for local development only, with alternative models documented in comments.

## Relevant Files

### Existing LLM Wrappers (Reference)
- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2`** - OpenAI template pattern
- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2`** - Anthropic template pattern (if exists)
- **`.claude/hooks/utils/llm/oai.py`** - Rendered OpenAI wrapper
- **`.claude/hooks/utils/llm/anth.py`** - Rendered Anthropic wrapper

### Template Infrastructure
- **`tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`** - Template rendering system
- **`tac_bootstrap_cli/tac_bootstrap/application/generate_service.py`** - File generation service

### Tests
- **`tac_bootstrap_cli/tests/test_template_repo.py`** - Template rendering tests
- **`tac_bootstrap_cli/tests/`** - Test directory for new tests

### New Files to Create
- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`** - Jinja2 template (CREATE)
- **`.claude/hooks/utils/llm/ollama.py`** - Rendered template output (CREATE)

## Implementation Plan

### Phase 1: Foundation & Analysis
Understand the existing LLM wrapper patterns and template infrastructure:
- Review `oai.py.j2` and `anth.py` for interface and structure
- Understand Ollama's OpenAI-compatible API endpoint
- Verify template rendering infrastructure
- Identify Jinja2 variables used in existing templates

### Phase 2: Template Creation
Create the `ollama.py.j2` Jinja2 template:
- Use static structure (minimal Jinja2 templating)
- Implement three core functions: `prompt_llm()`, `generate_completion_message()`, `main()`
- Use OpenAI SDK with dummy 'ollama' API key
- Hardcode model ('llama3.2'), max_tokens (100), and temperature (0.7)
- Include identical error handling pattern (catch all exceptions, return None)
- Document alternative models in code comments

### Phase 3: Template Rendering
Render the template to create the runtime wrapper:
- Generate `.claude/hooks/utils/llm/ollama.py` from the template
- Ensure output matches expected structure and formatting
- Verify no Jinja2 variables remain (static template)

### Phase 4: Testing & Validation
Test the template and rendered output:
- Verify template renders without errors
- Test basic Python syntax and imports
- Validate that rendered file can be imported
- Test the wrapper interface matches existing wrappers
- Run existing test suite to ensure no regressions
- Validate all acceptance criteria

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Review Existing LLM Wrapper Patterns
- Read `oai.py.j2` template to understand structure and variables
- Read `.claude/hooks/utils/llm/oai.py` to see the rendered output
- Read `.claude/hooks/utils/llm/anth.py` to compare Anthropic wrapper
- Document the function signatures and error handling patterns
- Identify Jinja2 variables used (if any)

**Acceptance:** You understand the exact pattern and can replicate it

### Task 2: Create ollama.py.j2 Template File
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`
- Implement with:
  - Import statements: `from openai import OpenAI`, `import os`, `import sys`, `from dotenv import load_dotenv`
  - Model constant: `MODEL = "llama3.2"` with comment about alternatives
  - `prompt_llm(prompt_text: str) -> str | None` function
  - `generate_completion_message() -> str | None` function
  - `main()` CLI entry point function
  - Same interface signature as existing wrappers
  - Identical error handling: `except Exception: return None`
  - OpenAI client with: base_url="http://localhost:11434/v1", api_key="ollama"

**Acceptance:** Template file created with correct syntax and structure

### Task 3: Verify Template Syntax
- Validate Jinja2 template syntax with no rendering errors
- Check file uses proper Python formatting
- Verify imports are correct and complete
- Ensure function signatures match oai.py/anth.py pattern
- Confirm error handling matches existing pattern

**Acceptance:** Template is syntactically valid Python with valid Jinja2

### Task 4: Create Rendered ollama.py Output
- Manually render template or use template_repo to generate output
- Create `.claude/hooks/utils/llm/ollama.py` as the rendered version
- Verify rendered file has no Jinja2 template syntax remaining
- Ensure file is properly formatted and indented

**Acceptance:** `.claude/hooks/utils/llm/ollama.py` exists and is syntactically correct Python

### Task 5: Test Rendered Wrapper
- Verify the rendered Python file can be imported without errors
- Check that `prompt_llm`, `generate_completion_message`, and `main` are callable
- Validate function signatures match expected interface
- Run syntax check with `python -m py_compile`

**Acceptance:** Rendered wrapper imports successfully and functions are accessible

### Task 6: Validate Against Acceptance Criteria
- Verify template uses OpenAI SDK (not ollama package)
- Confirm hardcoded model is 'llama3.2'
- Check API key is literal string 'ollama'
- Verify base_url is 'http://localhost:11434/v1'
- Confirm max_tokens=100 and temperature=0.7
- Ensure error handling returns None on exception
- Validate three-function interface (prompt_llm, generate_completion_message, main)
- Check alternative models documented in comments

**Acceptance:** All acceptance criteria verified

### Task 7: Run Full Test Suite
Execute validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports
cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2
```

**Acceptance:** All tests pass with zero errors and warnings

## Testing Strategy

### Unit Tests
- Template rendering tests in `test_template_repo.py`:
  - Test `ollama.py.j2` renders without errors
  - Test rendered output contains expected functions
  - Test no Jinja2 variables remain in output

### Integration Tests
- Verify rendered wrapper imports successfully
- Test function calls don't raise exceptions (graceful error handling)
- Validate function interface consistency with `oai.py` and `anth.py`

### Edge Cases
- Handling when Ollama server is not running (graceful None return)
- Empty or invalid prompts (graceful None return)
- Malformed API responses (caught by exception handler)
- Missing OPENAI_API_KEY environment variable (should still work with dummy key)

### Manual Testing
- Python syntax validation: `python -m py_compile`
- Import test: `python -c "from ollama import prompt_llm"`
- Type checking: `mypy` on the generated file

## Acceptance Criteria

✓ **File Creation:**
  - `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` exists
  - `.claude/hooks/utils/llm/ollama.py` exists and is properly rendered

✓ **Template Specification:**
  - Uses OpenAI SDK (not official ollama package)
  - Hardcoded model: `llama3.2`
  - Hardcoded API key: `'ollama'` (literal string)
  - Hardcoded base_url: `'http://localhost:11434/v1'`
  - Hardcoded parameters: `max_tokens=100`, `temperature=0.7`
  - No per-deployment model configurability

✓ **Function Interface:**
  - `prompt_llm(prompt_text: str) -> str | None` exists
  - `generate_completion_message() -> str | None` exists
  - `main()` entry point exists
  - Signatures match `oai.py` and `anth.py` exactly

✓ **Error Handling:**
  - All functions return `None` on exceptions (no error details exposed)
  - Catches and silently handles: connection errors, model not found, timeouts
  - Matches bare `except Exception: return None` pattern

✓ **Documentation:**
  - Alternative models (e.g., 'cogito:8b') documented in comments
  - OpenAI endpoint explained in comments
  - Dummy API key rationale documented

✓ **Code Quality:**
  - No Jinja2 template syntax remains in rendered file
  - Python 3.10+ compatible syntax
  - Proper imports and dependencies
  - Follows existing code style and patterns
  - Passes `ruff check` linting
  - Passes `mypy` type checking (if applicable)

✓ **No Regressions:**
  - All existing tests pass
  - No changes to other LLM wrappers
  - No new dependencies required (uses existing `openai` and `python-dotenv`)

## Validation Commands

Run these commands to verify the implementation:

```bash
# Test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports

# Syntax validation
python -m py_compile .claude/hooks/utils/llm/ollama.py

# File existence checks
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2
ls -la .claude/hooks/utils/llm/ollama.py

# Import test
python -c "import sys; sys.path.insert(0, '.claude/hooks/utils/llm'); from ollama import prompt_llm, generate_completion_message, main; print('✓ All functions importable')"

# Quick smoke test (if Ollama running)
python .claude/hooks/utils/llm/ollama.py --help
```

## Notes

### Dependencies
- **New dependencies:** None
- **Existing dependencies used:**
  - `openai` (already in project)
  - `python-dotenv` (already in project)
  - `requests` (indirectly through openai, already available)

### Design Decisions

1. **OpenAI SDK vs Official Ollama Package**
   - Choice: OpenAI SDK with OpenAI-compatible endpoint
   - Rationale: Maintains consistency with existing patterns, no new dependencies, Ollama specifically supports this integration

2. **Hardcoded Model vs Configuration**
   - Choice: Hardcoded 'llama3.2'
   - Rationale: Simplicity for development-only wrapper, matches how `oai.py` hardcodes 'gpt-4o-mini' and `anth.py` hardcodes 'claude-3-5-haiku-20241022'

3. **API Key: Literal 'ollama' String**
   - Choice: Use literal string 'ollama'
   - Rationale: Ollama local server doesn't validate keys, descriptive value, matches spec

4. **Error Handling: Silent None Returns**
   - Choice: Catch all exceptions, return None
   - Rationale: Matches existing pattern exactly, development-only code doesn't need detailed error types

5. **Jinja2 Variables: None (Static Template)**
   - Choice: Keep template static, no {{ config }} variables
   - Rationale: Simple static template like `anth.py`, variables can be added later if needed

### Alternative Models
The wrapper defaults to 'llama3.2' but can easily be modified to use other models:
- `cogito:8b` - Faster inference
- `mistral` - Good general purpose
- `neural-chat` - Optimized for conversation
- `openchat` - Small but capable

Users can modify the `MODEL = "llama3.2"` line to use their preferred model.

### Future Enhancements
- Environment variable configurability for model name
- Support for streaming responses
- Custom temperature/max_tokens via CLI flags
- Support for additional Ollama-specific endpoints
- Integration with other local LLM servers (LM Studio, LocalAI, etc.)

### Related Issues
- Issue #250: Added OpenAI LLM wrapper template
- Issue #249: Added Anthropic LLM wrapper template
- This issue (251): Adds Ollama LLM wrapper template

### Testing Considerations
- Template rendering tests should verify no Jinja2 syntax in output
- Import tests should work without Ollama server running (graceful handling)
- If Ollama is running locally, can test actual API calls
- Error handling tests should verify None returns on connection failures
