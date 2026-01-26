---
doc_type: feature
adw_id: feature_Tac_9_task_10_v4
date: 2026-01-26
idk:
  - llm-wrapper
  - local-inference
  - ollama
  - openai-sdk
  - jinja2-template
  - model-integration
  - python-wrapper
tags:
  - feature
  - llm
  - local-development
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2
  - .claude/hooks/utils/llm/ollama.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2
---

# Ollama LLM Wrapper Template

**ADW ID:** feature_Tac_9_task_10_v4
**Date:** 2026-01-26
**Specification:** issue-251-adw-feature_Tac_9_task_10_v4-sdlc_planner-add-ollama-llm-wrapper.md

## Overview

Added a Jinja2 template for an Ollama local LLM wrapper that provides the same interface as existing cloud provider wrappers (OpenAI and Anthropic). This enables developers to prototype and test with local language models without requiring cloud API keys or internet connectivity.

The wrapper uses Ollama's OpenAI-compatible endpoint (`http://localhost:11434/v1`) and the OpenAI SDK, maintaining consistency with existing wrapper patterns while requiring no additional dependencies.

## What Was Built

- **Ollama Jinja2 Template** (`ollama.py.j2`) - Static Jinja2 template for local model inference
- **Rendered Wrapper** (`ollama.py`) - Runtime wrapper executable with three-function interface
- **Three-Function Interface:**
  - `prompt_llm(prompt_text: str) -> str | None` - Send prompts to local Ollama instance
  - `generate_completion_message() -> str | None` - Generate natural language completion messages
  - `main()` - CLI entry point for testing

## Technical Implementation

### Files Modified/Created

- **`tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2`** (NEW) - Jinja2 template source (121 lines)
- **`.claude/hooks/utils/llm/ollama.py`** (NEW) - Rendered template output (121 lines)

### Key Changes

1. **Template Implementation:**
   - Uses OpenAI SDK with Ollama's OpenAI-compatible endpoint
   - Hardcoded model: `llama3.2`
   - Hardcoded parameters: `max_tokens=100`, `temperature=0.7`
   - Dummy API key: `'ollama'` (Ollama doesn't validate keys)
   - Base URL: `http://localhost:11434/v1`

2. **Error Handling:**
   - All functions return `None` on exceptions
   - Graceful handling of connection failures, missing models, timeouts
   - Matches existing wrapper pattern exactly

3. **Function Signatures:**
   - `prompt_llm(prompt_text)` - Core prompting function
   - `generate_completion_message()` - Generates AI-assistant completion messages with optional name personalization
   - `main()` - CLI with support for `--completion` flag and direct prompts

4. **CLI Support:**
   - Command: `./ollama.py 'your prompt here'`
   - Command: `./ollama.py --completion`
   - Usage documentation on invalid arguments

### Dependencies

- **No new dependencies** - Uses existing packages:
  - `openai` (already in project)
  - `python-dotenv` (already in project)

## How to Use

### Basic Setup

Ensure Ollama is running locally:
```bash
ollama serve
```

Pull a model (if not already available):
```bash
ollama pull llama3.2
```

### Send a Prompt

```bash
python .claude/hooks/utils/llm/ollama.py "What is the capital of France?"
```

Expected output (if Ollama is running):
```
Paris
```

### Generate Completion Message

```bash
ENGINEER_NAME="Alice" python .claude/hooks/utils/llm/ollama.py --completion
```

This generates friendly completion messages, optionally including the engineer's name (~30% of the time).

### Use in Python Code

```python
import sys
sys.path.insert(0, '.claude/hooks/utils/llm')
from ollama import prompt_llm, generate_completion_message

# Direct prompting
response = prompt_llm("Explain quantum computing in one sentence")
print(response)

# Generate completion message
message = generate_completion_message()
print(message)  # e.g., "All done!" or "Ready to go, Alice!"
```

## Configuration

### Hardcoded Values

All parameters are hardcoded for simplicity:

```python
MODEL = "llama3.2"  # Change to other models if desired
max_tokens=100      # Maximum response length
temperature=0.7     # Creativity level (0-1)
```

### Environment Variables

- **`ENGINEER_NAME`** (optional) - Engineer's name for personalized completion messages
- **`OPENAI_API_KEY`** - Not required (uses dummy 'ollama' key)

### Alternative Models

The wrapper defaults to `llama3.2` but can be modified to use:
- `cogito:8b` - Faster inference
- `mistral` - General-purpose model
- `neural-chat` - Conversation-optimized
- `openchat` - Efficient and capable
- Any other model available in your Ollama installation

Change by editing `MODEL = "llama3.2"` to your preferred model.

## Testing

### Syntax Validation

```bash
python -m py_compile .claude/hooks/utils/llm/ollama.py
```

### Import Test

```bash
python -c "import sys; sys.path.insert(0, '.claude/hooks/utils/llm'); from ollama import prompt_llm, generate_completion_message, main; print('✓ All functions importable')"
```

### Manual Testing (requires Ollama running)

```bash
# Test basic prompt
python .claude/hooks/utils/llm/ollama.py "Hello, what's 2+2?"

# Test with engineer name
ENGINEER_NAME="DevTeam" python .claude/hooks/utils/llm/ollama.py --completion

# Test CLI help
python .claude/hooks/utils/llm/ollama.py
```

### Error Handling Test

Test graceful degradation when Ollama is not running:
```bash
# Kill Ollama or ensure it's not running
python .claude/hooks/utils/llm/ollama.py "test prompt"  # Returns None gracefully
```

### Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

## Notes

### Design Decisions

1. **OpenAI SDK over Official Ollama Package**
   - Maintains consistency with existing wrapper patterns
   - No new dependencies required
   - Ollama explicitly supports OpenAI-compatible endpoint integration

2. **Hardcoded Configuration**
   - Simplifies wrapper for development-only use case
   - Matches approach of `oai.py` (hardcodes `gpt-4o-mini`) and `anth.py` (hardcodes `claude-3-5-haiku-20241022`)
   - Can be modified for specific use cases

3. **Static Jinja2 Template**
   - No template variables required
   - Easier to understand and maintain
   - Variables can be added in future iterations

4. **Silent Error Handling**
   - Returns `None` on any exception
   - Allows graceful degradation in production workflows
   - Matches existing wrapper pattern

### Dependencies and Requirements

- **Python:** 3.8+
- **Ollama:** Running locally at `http://localhost:11434`
- **Packages:** `openai`, `python-dotenv` (already in project)

### Future Enhancements

- Environment variable configurability for model name
- Support for streaming responses
- Custom temperature/max_tokens via CLI flags
- Integration with other local LLM servers (LM Studio, LocalAI)
- Configuration file support for model selection

### Related Features

This wrapper completes the local development LLM integration suite:
- **oai.py** - OpenAI cloud models
- **anth.py** - Anthropic cloud models
- **ollama.py** - Local open-source models (NEW)

All three wrappers share the same interface, making it easy to switch between providers during development.
