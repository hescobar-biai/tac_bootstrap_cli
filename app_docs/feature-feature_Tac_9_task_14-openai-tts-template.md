---
doc_type: feature
adw_id: feature_Tac_9_task_14
date: 2026-01-26
idk:
  - template
  - jinja2
  - tts
  - openai
  - text-to-speech
  - audio-synthesis
tags:
  - feature
  - template
  - tts
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2
  - .claude/hooks/utils/tts/openai_tts.py
---

# OpenAI TTS Wrapper Template

**ADW ID:** feature_Tac_9_task_14
**Date:** 2026-01-26
**Specification:** specs/issue-255-adw-feature_Tac_9_task_14-sdlc_planner-openai-tts-template.md

## Overview

Created a Jinja2 template for OpenAI's Text-to-Speech API wrapper that provides a simple, consistent interface for synthesizing speech using OpenAI's TTS models. The template supports both tts-1 (standard) and tts-1-hd (high definition) models with all six standard voices, enabling generated projects to integrate OpenAI TTS capabilities with minimal configuration.

## What Was Built

- Jinja2 template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2`
- Rendered reference implementation at `.claude/hooks/utils/tts/openai_tts.py`
- Two main functions: `synthesize_speech()` and `save_audio_file()`
- PEP 723 script block for standalone execution with `uv run --script`
- Full type hints and comprehensive docstrings

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2`: New Jinja2 template for OpenAI TTS wrapper with project name interpolation
- `.claude/hooks/utils/tts/openai_tts.py`: Rendered reference implementation for testing and demonstration

### Key Changes

- **PEP 723 script block**: Enables standalone execution with `uv run --script`, declares dependencies on `openai` and `python-dotenv`
- **synthesize_speech()**: Core function that accepts text, voice (default: "alloy"), model (default: "tts-1"), and speed (default: 1.0), returning audio bytes in MP3 format or None on error
- **save_audio_file()**: Convenience function that synthesizes speech and saves to a file path, with automatic parent directory creation, returning boolean success/failure
- **Error handling**: Simple None/False returns on errors, letting OpenAI SDK handle API validation
- **Non-streaming mode**: Collects full audio bytes via `response.content` for consistency with ElevenLabs pattern
- **Environment variable**: Uses standard `OPENAI_API_KEY` (not templated) for API authentication

## How to Use

### As Template Developer

When TAC Bootstrap generates a project with the OpenAI TTS template:

1. The template automatically renders into the target project's `.claude/hooks/utils/tts/` directory
2. The rendered file includes the project name in docstrings via `{{ config.project.name }}`
3. Users configure their `OPENAI_API_KEY` in their project's `.env` file

### As End User (in Generated Project)

1. Set your OpenAI API key in the project's `.env` file:
```bash
echo "OPENAI_API_KEY=sk-..." >> .env
```

2. Import and use the functions in your Python code:
```python
from .claude.hooks.utils.tts.openai_tts import synthesize_speech, save_audio_file

# Synthesize to bytes
audio_bytes = synthesize_speech("Hello world", voice="alloy", model="tts-1")

# Save to file
success = save_audio_file("Hello world", "/path/to/output.mp3", voice="nova", model="tts-1-hd", speed=1.2)
```

3. Or use it standalone from the command line:
```bash
uv run .claude/hooks/utils/tts/openai_tts.py
```

## Configuration

### Function Parameters

**synthesize_speech(text, voice, model, speed)**
- `text` (str): Text to synthesize (limit: 4096 characters)
- `voice` (str): Voice name - Options: alloy, echo, fable, onyx, nova, shimmer (default: "alloy")
- `model` (str): TTS model - Options: tts-1 (standard), tts-1-hd (high definition) (default: "tts-1")
- `speed` (float): Playback speed, range 0.25 to 4.0 (default: 1.0)

**save_audio_file(text, file_path, voice, model, speed)**
- Same parameters as `synthesize_speech()` plus:
- `file_path` (str): Destination path for MP3 file (parent directories created automatically)

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (required)

### Output Format

- Hardcoded to MP3 format for simplicity and compatibility

## Testing

### Validate Template Syntax

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Verify Rendered Python File

```bash
python .claude/hooks/utils/tts/openai_tts.py
```

### Test with Actual API (requires OPENAI_API_KEY)

```bash
cd .claude/hooks/utils/tts
export OPENAI_API_KEY=sk-...
python -c "from openai_tts import save_audio_file; save_audio_file('Hello from OpenAI', '/tmp/test.mp3', voice='nova'); print('Audio saved to /tmp/test.mp3')"
```

### Linting and Type Checking

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test CLI

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

- **Voice parameter**: Uses voice names (not IDs) matching OpenAI's API design
- **Model parameter**: Defaults to tts-1 (faster/cheaper), allows override to tts-1-hd
- **Speed parameter**: Included for flexibility without adding complexity
- **Format**: MP3 hardcoded for simplicity and consistency with ElevenLabs pattern
- **Streaming**: Non-streaming only for consistency with existing TTS template pattern
- **Error handling**: Simple None/False returns; lets OpenAI SDK handle API validation
- **Environment variable**: Uses standard `OPENAI_API_KEY` (not templated)

### OpenAI TTS API Details

- **Voices**: alloy, echo, fable, onyx, nova, shimmer (six standard voices)
- **Models**: tts-1 (standard, faster, cheaper), tts-1-hd (high definition)
- **Speed range**: 0.25 to 4.0 (default: 1.0)
- **Formats supported**: mp3, opus, aac, flac (template uses mp3)
- **Text limit**: 4096 characters per request
- **Pricing**: $0.015 per 1K characters (tts-1), $0.030 per 1K characters (tts-1-hd)

### Pattern Consistency

This template follows the same structure as `elevenlabs_tts.py.j2`:
- PEP 723 script block for standalone execution
- Two main functions: synthesize and save
- Simple error handling (None/False returns)
- Environment variable for API key
- Non-streaming implementation
- MP3 output format
