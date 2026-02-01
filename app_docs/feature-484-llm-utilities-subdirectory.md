---
doc_type: feature
adw_id: feature_Tac_12_task_32
date: 2026-01-31
idk:
  - LLM provider utilities
  - multi-provider abstraction
  - Jinja2 templates
  - scaffold service
  - Anthropic OpenAI Ollama
tags:
  - feature
  - llm-utilities
  - hook-infrastructure
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Feature: Create LLM Utilities Subdirectory

**ADW ID:** feature_Tac_12_task_32
**Date:** 2026-01-31
**Specification:** [issue-484-adw-feature_Tac_12_task_32-sdlc_planner-create-llm-utilities-subdirectory.md](specs/issue-484-adw-feature_Tac_12_task_32-sdlc_planner-create-llm-utilities-subdirectory.md)

## Overview

Created a comprehensive LLM utilities subdirectory with Jinja2 templates supporting three LLM providers (Anthropic, OpenAI, Ollama). This enables the TAC Bootstrap CLI to generate projects with multi-provider LLM integration for hook automation, establishing a composable interface that allows hooks to leverage different LLM backends.

## What Was Built

- **Multi-provider LLM abstraction** with unified `prompt_llm()` and `generate_completion_message()` interfaces
- **Three provider implementations** (Anthropic, OpenAI, Ollama) with provider-specific configuration
- **Jinja2 templates** mirroring base directory structure for CLI-generated projects
- **Scaffold service integration** to register and copy llm/ templates during project generation
- **Fail-fast error handling** returning None on API errors for graceful degradation

## Technical Implementation

### Files Modified/Created

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2` - Package initialization re-exporting all three providers with Anthropic as implicit default
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/anth.py.j2` - Anthropic provider using claude-3-5-haiku model
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - OpenAI provider using gpt-4o-mini model
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` - Ollama provider for local model inference
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Updated to register llm/ utilities in template list

### Key Changes

- **Provider Selection**: Three independent modules (anth, oai, ollama) can be imported directly or default through package exports
- **Environment Variables**: Each provider loads its own API key (ANTHROPIC_API_KEY, OPENAI_API_KEY) with None return on missing credentials
- **Completion Message Generation**: Common `generate_completion_message()` function supports optional ENGINEER_NAME environment variable for personalization
- **CLI Compatibility**: All providers include executable shebang and uv script preamble for direct execution
- **Template Structure**: Exact mirror of base directory implementations with Jinja2 placeholders for config values

## How to Use

### 1. Generate a Project with LLM Utilities

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap init --name my-project
```

The generated project will include `.claude/hooks/utils/llm/` with all three providers.

### 2. Use LLM Utilities in Generated Projects

Import providers in hooks:

```python
# Use default Anthropic provider
from llm import prompt_llm, generate_completion_message

# Or use specific provider
from llm.oai import prompt_llm
from llm.ollama import prompt_llm
```

### 3. Call LLM Functions

```bash
# Prompt an LLM
./anth.py "What is TAC Bootstrap?"

# Generate completion message
./anth.py --completion
```

## Configuration

Each provider uses environment variables for configuration:

- **Anthropic**: `ANTHROPIC_API_KEY` (required for anth provider)
- **OpenAI**: `OPENAI_API_KEY` (required for oai provider)
- **Ollama**: No API key needed; requires local Ollama instance at `http://localhost:11434`
- **Engineer Name**: `ENGINEER_NAME` (optional, personalizes completion messages)

## Testing

### Run Unit Tests

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli
uv run ruff check .
```

### Run Type Checking

```bash
cd tac_bootstrap_cli
uv run mypy tac_bootstrap/
```

### Smoke Test CLI

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap --help
```

### Verify Template Files Exist

```bash
ls -la tac_bootstrap/templates/claude/hooks/utils/llm/
```

Should show: `__init__.py.j2`, `anth.py.j2`, `oai.py.j2`, `ollama.py.j2`

## Notes

- The base directory files at `/.claude/hooks/utils/llm/` serve as the source of truth; templates must mirror these exactly
- Each provider is self-contained with no inter-provider dependencies or fallback chains
- The final import in `__init__.py.j2` (Anthropic) serves as the implicit default for `from llm import` statements
- All providers return `None` on errors rather than raising exceptions, enabling graceful degradation
- Ollama provider connects to local instance; ensure Ollama is running before using this provider
- This feature is part of Wave 4 - Hook Utilities (Task 32 of 49)
