---
doc_type: feature
adw_id: chore_Tac_9_task_16
date: 2026-01-26
idk:
  - tts
  - template
  - jinja2
  - python-package
  - api-export
  - pyttsx3
  - openai-tts
  - elevenlabs-tts
tags:
  - feature
  - chore
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2
---

# TTS Package Init Template

**ADW ID:** chore_Tac_9_task_16
**Date:** 2026-01-26
**Specification:** specs/issue-257-adw-chore_Tac_9_task_16-sdlc_planner-add-tts-init-template.md

## Overview

Updated the TTS utilities package initialization template to export all three TTS engine implementations (pyttsx3, OpenAI, ElevenLabs) with an explicit public API. This enables generated projects to use any TTS backend through a unified interface.

## What Was Built

- Enhanced `__init__.py.j2` template with complete TTS module exports
- Added explicit `__all__` list for clean public API
- Implemented namespace-prefixed imports to avoid naming conflicts
- Updated docstring to document all available TTS implementations

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2`: Expanded from exporting only ElevenLabs functions to exporting all three TTS implementations with namespace prefixing

### Key Changes

- **Complete API exports**: Template now exports functions from all three TTS modules (pyttsx3, OpenAI, ElevenLabs)
- **Namespace prefixing**: Each import is prefixed with its TTS provider name (e.g., `pyttsx3_synthesize_speech`) to prevent naming collisions
- **Explicit `__all__` list**: Six exported functions clearly documented in `__all__` for clean public API
- **Enhanced docstring**: Documents all available TTS implementations with their function names
- **No side effects**: Pure import-only initialization following Python package best practices

## How to Use

When generating a new project with tac-bootstrap, the rendered TTS package allows importing any TTS backend:

1. **Use pyttsx3 (offline system TTS)**:
   ```python
   from utils.tts import pyttsx3_synthesize_speech, pyttsx3_save_to_file
   ```

2. **Use OpenAI TTS**:
   ```python
   from utils.tts import openai_synthesize_speech, openai_save_audio_file
   ```

3. **Use ElevenLabs TTS**:
   ```python
   from utils.tts import elevenlabs_synthesize_speech, elevenlabs_save_audio_file
   ```

## Configuration

The template uses the standard `config.project.name` Jinja2 variable for project-specific docstrings. No additional configuration is required.

## Testing

Validate the template implementation:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Check code quality:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test the CLI:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

This chore completes the TTS package structure by providing a unified interface to all TTS implementations. The namespace-prefixed approach allows users to choose their TTS backend explicitly while avoiding function name collisions between different providers. All three implementations share similar function names (`synthesize_speech`, `save_audio_file`/`save_to_file`) but are differentiated by their module prefix.
