---
doc_type: feature
adw_id: feature_Tac_9_task_9
date: 2026-01-26
idk:
  - jinja2-template
  - llm-wrapper
  - openai-api
  - uv-script-metadata
  - environment-configuration
tags:
  - feature
  - template
  - llm-integration
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2
---

# OpenAI LLM Wrapper Jinja2 Template

**ADW ID:** feature_Tac_9_task_9

**Date:** 2026-01-26

**Specification:** [issue-240-adw-feature_Tac_9_task_9-sdlc_planner-oai-llm-wrapper-template.md](../specs/issue-240-adw-feature_Tac_9_task_9-sdlc_planner-oai-llm-wrapper-template.md)

## Overview

This feature introduces a Jinja2 template (`oai.py.j2`) for generating OpenAI API wrapper utilities in TAC Bootstrap-generated projects. The template provides a standardized, executable Python script that mirrors the Anthropic wrapper's interface while using OpenAI's `gpt-4o-mini` model. The template preserves the complete functionality of the reference implementation with minimal templating, enabling consistent OpenAI integration across all generated projects.

## What Was Built

- **Jinja2 Template for OpenAI Wrapper**: Complete template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2`
- **Two Core Functions**: `prompt_llm()` for direct LLM prompting and `generate_completion_message()` for AI-friendly task completion messages
- **Minimal Templating Pattern**: Only docstring and shebang line use Jinja2 variables, maintaining utility simplicity
- **Valid Model Configuration**: Corrected model from non-existent 'gpt-4.1-nano' to 'gpt-4o-mini' (OpenAI's fastest/cheapest current model)
- **Executable Script Support**: Preserved uv script metadata block for standalone execution
- **Environment Variable Integration**: Full support for `OPENAI_API_KEY` and `ENGINEER_NAME` configuration

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2`: New Jinja2 template file containing the complete OpenAI wrapper implementation

### Key Changes

- **Template Structure**: Uses uv script shebang (`#!/usr/bin/env -S uv run --script`) with inline Python dependencies metadata
- **LLM Prompting**: `prompt_llm(prompt_text)` function makes OpenAI chat completions requests with `gpt-4o-mini` model, handling API errors gracefully by returning `None`
- **Completion Messages**: `generate_completion_message()` generates friendly completion messages with optional engineer name personalization using LLM
- **Configuration**: Environment variables (`OPENAI_API_KEY`, `ENGINEER_NAME`) handle runtime configuration without template variables
- **Jinja2 Variables**: Only `{{ config.project.name }}` templated in docstring; all code logic is generic and non-templated
- **CLI Interface**: `main()` function provides command-line testing with `--completion` flag for message generation

## How to Use

### In Template Rendering

The template is automatically rendered during project generation to `.claude/hooks/utils/llm/oai.py`. No manual setup required.

### In Generated Projects

Once rendered in a generated project, use the wrapper script:

```bash
# Direct LLM prompting
./.claude/hooks/utils/llm/oai.py "Your prompt here"

# Generate completion message
./.claude/hooks/utils/llm/oai.py --completion
```

### In Python Code

Import and use the functions:

```python
from utils.llm.oai import prompt_llm, generate_completion_message

# Direct prompting
response = prompt_llm("Explain this code snippet")

# Generate friendly completion message
message = generate_completion_message()
if message:
    print(message)  # e.g., "All set!", "Ready to go!"
```

## Configuration

### Environment Variables

- **`OPENAI_API_KEY`**: Required. OpenAI API key for authentication. Script silently returns `None` if not set.
- **`ENGINEER_NAME`**: Optional. Engineer's name for personalized completion messages. If set, ~30% of messages naturally include the name.

### Dependencies

The template specifies these uv script dependencies:
- `openai`: OpenAI Python SDK for API calls
- `python-dotenv`: Environment variable loading from `.env` files

### Model Selection

Uses `gpt-4o-mini` because:
- Fastest OpenAI model (lowest latency)
- Cheapest OpenAI model (lowest cost)
- Suitable for completion message generation tasks
- Maintains parity with Anthropic wrapper's philosophy of speed/cost balance

## Testing

### Validate Template Syntax

```bash
python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/oai.py.j2'); print('Template syntax OK')"
```

### Verify Template File Exists

```bash
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2
```

### Check Consistency with Anthropic Template

```bash
diff <(sed 's/openai/anthropic/g; s/gpt-4o-mini/claude-3-5-haiku/g' tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2) tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2 | head -20
```

### Run Project Tests

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_9_task_9 && python -m pytest tests/ -v --tb=short
```

## Notes

### Error Handling Strategy

The implementation uses silent error handling:
- Returns `None` instead of raising exceptions
- Allows graceful degradation when API is unavailable
- Permits workflows to continue without hard failures
- Callers can handle `None` responses appropriately

This approach is intentional and not configurable, treating missing API keys and network errors the same way.

### Parallel Implementation with Anthropic

This template mirrors the Anthropic template (`anth.py.j2`) exactly in structure:
- Identical function signatures and docstrings
- Identical error handling (silent returns of `None`)
- Identical Jinja2 templating patterns
- Only model name (`gpt-4o-mini` vs `claude-3-5-haiku`) and library imports differ

This consistency allows developers to understand both implementations and switch between them with minimal effort.

### Executable Script Design

The template preserves executable script design:
- Shebang `#!/usr/bin/env -S uv run --script` enables direct execution
- uv script metadata block (`# /// script`) provides inline dependency declaration
- Eliminates need for `chmod +x` or separate requirements files
- Matches the source implementation's design philosophy

This is essential for hook scripts that need direct execution without wrapper commands.

### Model Name Correction

The source implementation referenced 'gpt-4.1-nano' (non-existent). The correction to 'gpt-4o-mini' is deliberate:
- Aligns with actual available OpenAI models as of 2025
- Provides optimal speed/cost ratio for completion message generation
- Maintains consistency between OpenAI and Anthropic implementations
- Ensures generated projects have immediately usable wrappers
