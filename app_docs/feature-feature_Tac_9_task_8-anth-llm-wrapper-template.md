---
doc_type: feature
adw_id: feature_Tac_9_task_8
date: 2026-01-26
idk:
  - jinja2-template
  - llm-wrapper
  - anthropic-api
  - uv-script
  - hook-utilities
  - configuration-template
tags:
  - feature
  - templates
  - infrastructure
  - llm-integration
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2
  - .claude/hooks/utils/llm/anth.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2
---

# Anthropic LLM Wrapper Template (anth.py.j2)

**ADW ID:** feature_Tac_9_task_8
**Date:** 2026-01-26
**Specification:** specs/issue-239-adw-feature_Tac_9_task_8-sdlc_planner-anth-llm-wrapper-template.md

## Overview

This feature creates a Jinja2 template for the Anthropic LLM wrapper utility, providing a reusable interface for invoking Claude 3.5 Haiku through hook scripts. The template preserves the complete functionality of the source implementation while applying minimal Jinja2 templating to maintain consistency across generated projects.

## What Was Built

- **Anthropic LLM Wrapper Template** (`anth.py.j2`): A uv script template providing direct API access to Anthropic's Claude model
- **Three Core Functions**:
  - `prompt_llm(prompt_text)` - Direct LLM prompting for arbitrary text input
  - `generate_completion_message()` - AI-generated task completion messages with optional engineer name personalization
  - `generate_agent_name()` - Unique agent name generation
- **Executable Script Configuration**: uv script metadata block for standalone execution with Python 3.8+ and required dependencies (anthropic, python-dotenv)
- **Environment-Based Configuration**: Uses `ANTHROPIC_API_KEY` and `ENGINEER_NAME` environment variables at runtime

## Technical Implementation

### Files Modified

- `.claude/hooks/utils/llm/anth.py`: Rendered output file containing the complete implementation with all three functions and executable shebang

### Key Changes

- **Template Structure**: Minimal Jinja2 templating applied only to the module docstring (project name injection)
- **Shebang Preservation**: `#!/usr/bin/env -S uv run --script` maintained for standalone execution capability
- **Model Configuration**: Hardcoded `claude-3-5-haiku-20241022` model version as the stable interface
- **Silent Error Handling**: Functions return `None` on API errors, enabling graceful degradation in hook contexts
- **Script Metadata**: Complete uv script block preserved exactly for dependency management (`anthropic>=0.28.0`, `python-dotenv`)

## How to Use

### Direct LLM Prompting

```bash
# Execute the script with a prompt
./.claude/hooks/utils/llm/anth.py "Your prompt text here"
```

### Generate Completion Messages

```bash
# Generate an AI completion message
./.claude/hooks/utils/llm/anth.py --completion
```

The completion message respects the `ENGINEER_NAME` environment variable:

```bash
ENGINEER_NAME="Alex" ./.claude/hooks/utils/llm/anth.py --completion
```

### Python Integration

```python
from anth import prompt_llm, generate_completion_message, generate_agent_name

# Direct prompting
response = prompt_llm("What is Python?")

# Completion message generation
message = generate_completion_message()

# Error handling
if response is None:
    print("API error - ensure ANTHROPIC_API_KEY is set")
```

## Configuration

### Environment Variables

- **ANTHROPIC_API_KEY** (required): Your Anthropic API key for authentication
- **ENGINEER_NAME** (optional): Name to include in completion messages (≈30% inclusion rate)

### Model Configuration

The template hardcodes `claude-3-5-haiku-20241022` as the model version. This is intentional:
- Ensures consistency across all generated projects
- Provides a stable, proven interface
- Represents the fastest Anthropic model available

### Dependencies

The script requires:
- Python 3.8+
- `anthropic` package (≥0.28.0)
- `python-dotenv` (for `.env` file support)

These are specified in the uv script metadata block and managed automatically when executed with `uv run`.

## Testing

### Basic Functionality

```bash
# Test with API key in environment
ANTHROPIC_API_KEY="sk-..." ./.claude/hooks/utils/llm/anth.py "Hello, Claude!"
```

### Completion Message Generation

```bash
# Test completion message with engineer name
ANTHROPIC_API_KEY="sk-..." ENGINEER_NAME="Taylor" ./.claude/hooks/utils/llm/anth.py --completion
```

### Error Handling

```bash
# Test graceful degradation without API key
./.claude/hooks/utils/llm/anth.py "test"  # Should exit silently (returns None)
```

### Template Rendering Validation

```bash
# Validate Jinja2 syntax
python -c "from jinja2 import Environment, FileSystemLoader; env = Environment(loader=FileSystemLoader('tac_bootstrap_cli/tac_bootstrap/templates')); tmpl = env.get_template('claude/hooks/utils/llm/anth.py.j2'); print('Template syntax OK')"

# Verify rendered output has valid Python syntax
python -m py_compile .claude/hooks/utils/llm/anth.py
```

## Notes

### Design Philosophy

The template follows a **minimal templating approach**:
- Only the module docstring receives project-specific templating
- All business logic remains generic and reusable
- Configuration occurs at runtime through environment variables, not template variables
- This pattern maintains the wrapper as a standardized utility across projects

### Error Handling Strategy

The silent error handling (returning `None` instead of raising exceptions) is intentional:
- Allows workflows to continue gracefully if the API is unavailable
- Suitable for hook contexts where exceptions might halt workflows
- Callers can check for `None` responses and handle them appropriately

### API Implementation Details

- **Max Tokens**: Set to 100 for efficient API calls
- **Temperature**: Fixed at 0.7 for balanced creativity
- **Completion Message Logic**: 30% chance of including engineer name when available, with natural phrasing

### Future Extensibility

While the current implementation is production-ready, future iterations could add:
- Configurable model selection at runtime
- Token limit and temperature parameters
- Additional function templates for specialized use cases
- Logging and tracing for debugging hook execution
