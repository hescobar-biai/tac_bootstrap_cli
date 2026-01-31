---
doc_type: feature
adw_id: feature_Tac_12_task_29
date: 2026-01-31
idk:
  - hook utility
  - event summarizer
  - Claude Haiku API
  - AI-powered summaries
  - Jinja2 templating
  - scaffold service integration
tags:
  - feature
  - hook utilities
  - TAC 12
related_code:
  - .claude/hooks/utils/summarizer.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Create summarizer.py Hook Utility

**ADW ID:** feature_Tac_12_task_29
**Date:** 2026-01-31
**Specification:** Issue #481

## Overview

Implemented a self-contained hook utility that generates concise AI-powered summaries of events using Claude Haiku. This utility follows existing hook utility patterns in the codebase and provides a simple, reusable interface for hooks that need to produce brief, human-readable summaries for logging, notifications, or event tracking.

## What Was Built

- **summarizer.py utility** - Core implementation in `.claude/hooks/utils/summarizer.py` with event summarization capability
- **Jinja2 template** - Generated template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2` for CLI scaffold
- **ScaffoldService integration** - Updated `scaffold_service.py` to include summarizer.py in hook utilities generation

## Technical Implementation

### Files Modified

- `.claude/hooks/utils/summarizer.py` - New hook utility for generating event summaries with Claude Haiku API integration
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/summarizer.py.j2` - Jinja2 template for CLI project generation
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Added summarizer.py to hook utilities list in `_add_hook_files()` method

### Key Changes

- **Event Summarization Function**: `generate_event_summary(event_text: str) -> Optional[str]` provides one-sentence summaries with maximum 150-character constraint
- **API Integration**: Uses Claude Haiku (claude-haiku-4-5-20251001) with environment-based authentication via `ANTHROPIC_API_KEY`
- **Silent Failure Pattern**: Returns `None` on any error, following existing hook utility conventions for graceful degradation
- **Length Validation**: Automatically truncates summaries exceeding 150 characters with ellipsis suffix
- **UV Script Header**: Includes embedded dependencies (`anthropic`, `python-dotenv`) for standalone execution

## How to Use

### Import and Call

```python
from .utils.summarizer import generate_event_summary

# Generate a summary of an event
event_text = "User submitted a form with validation errors on the login page"
summary = generate_event_summary(event_text)
if summary:
    print(f"Summary: {summary}")
```

### Environment Setup

The utility requires the `ANTHROPIC_API_KEY` environment variable to be set:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

If the key is not available, the function gracefully returns `None` without raising exceptions.

### Integration in Hooks

Use in any hook script that needs event summarization:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["anthropic", "python-dotenv"]
# ///

from utils.summarizer import generate_event_summary

event_description = "Git commit pushed to main branch with 5 files changed"
summary = generate_event_summary(event_description)
if summary:
    # Use summary in logging, notifications, etc.
    print(f"Event logged: {summary}")
```

## Configuration

### Environment Variables

- **ANTHROPIC_API_KEY**: Required for API authentication. If not set, function returns `None`.

### Model Parameters

- **Model**: `claude-haiku-4-5-20251001` (hardcoded)
- **Max Tokens**: 50 (optimized for one-sentence summaries)
- **Temperature**: 0.3 (low temperature for consistent, focused summaries)

### Output Constraints

- **Maximum Length**: 150 characters
- **Format**: Single sentence, no quotes or extra formatting
- **Truncation**: Automatically adds "..." if output exceeds limit

## Testing

### Unit Test - Basic Summarization

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_12_task_29
export ANTHROPIC_API_KEY="your-api-key-here"
python .claude/hooks/utils/summarizer.py
```

### Unit Test - Function Call

```bash
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/feature_Tac_12_task_29
python3 -c "
from dotenv import load_dotenv
load_dotenv()
import sys
sys.path.insert(0, '.claude/hooks/utils')
from summarizer import generate_event_summary
result = generate_event_summary('Test event for summarization')
print(f'Result: {result}')
print(f'Length: {len(result) if result else 0}')
"
```

### Integration Test - Scaffold Generation

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v -k "scaffold" --tb=short
```

### Validation Commands

Run these to ensure no regressions:

```bash
# Run full test suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Lint code
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Verify CLI functionality
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Silent Failure Pattern**: The utility follows existing hook utility conventions by returning `None` on any error rather than raising exceptions. This allows graceful degradation when the API is unavailable.
- **Hardcoded Model**: The Claude Haiku model version (claude-haiku-4-5-20251001) is intentionally hardcoded per specification. Future model updates are standard maintenance tasks.
- **Template Variable**: The Jinja2 template uses `{{ config.project.name }}` in the module docstring for project-specific identification during CLI scaffold generation.
- **Python 3.8+ Compatibility**: The UV script header specifies Python 3.8+ requirement to ensure broad compatibility across projects.
- **Single Responsibility**: The utility focuses exclusively on summarization without additional features (custom prompts, multiple output formats, etc.) to maintain simplicity and consistency with other hook utilities.
