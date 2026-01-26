---
doc_type: feature
adw_id: feature_Tac_9_task_13
date: 2026-01-26
idk:
  - elevenlabs
  - text-to-speech
  - tts-wrapper
  - jinja2-template
  - api-integration
  - environment-variable
  - audio-synthesis
tags:
  - feature
  - tts
  - template
  - api-wrapper
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2
  - .claude/hooks/utils/tts/elevenlabs_tts.py
---

# ElevenLabs TTS Template Wrapper

**ADW ID:** feature_Tac_9_task_13
**Date:** 2026-01-26
**Specification:** specs/issue-254-adw-feature_Tac_9_task_13-sdlc_planner-elevenlabs-tts-template.md

## Overview

This feature adds a Jinja2 template for an ElevenLabs Text-to-Speech (TTS) wrapper module that provides a standardized interface for audio synthesis in generated projects. The template follows the established pattern from LLM utilities (oai.py) with standalone functions, environment variable authentication, and lenient error handling using the Turbo v2.5 model.

## What Was Built

- Jinja2 template (`elevenlabs_tts.py.j2`) for ElevenLabs TTS integration
- Two standalone functions: `synthesize_speech()` and `save_audio_file()`
- Reference implementation rendered to `.claude/hooks/utils/tts/`
- Updated TTS module exports to include new functions
- uv script dependencies declaration for ElevenLabs SDK

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2`: New Jinja2 template with TTS wrapper implementation
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2`: Updated to export elevenlabs functions
- `.claude/hooks/utils/tts/elevenlabs_tts.py`: Rendered reference implementation
- `.claude/hooks/utils/tts/__init__.py`: Updated exports

### Key Changes

- **Function Pattern**: Follows oai.py pattern with standalone functions returning bytes/bool
- **Environment Authentication**: Uses `ELEVENLABS_API_KEY` environment variable with `load_dotenv()` support
- **Model Hardcoding**: Implements eleven_turbo_v2_5 model with MP3 44.1kHz 128kbps output format
- **Lenient Error Handling**: Returns `None` for synthesis errors and `False` for file operation errors
- **Voice Configuration**: Supports configurable `voice_id` parameter with default 'EXAVITQu4vr4xnSDxMaL'
- **uv Script Support**: Includes dependencies block for elevenlabs and python-dotenv libraries

## How to Use

### In Generated Projects

When generating a new project with TAC Bootstrap, the ElevenLabs TTS wrapper will be available at `.claude/hooks/utils/tts/elevenlabs_tts.py`:

1. **Set up API credentials**:
   ```bash
   export ELEVENLABS_API_KEY="your_api_key_here"
   ```
   Or add to `.env` file:
   ```
   ELEVENLABS_API_KEY=your_api_key_here
   ```

2. **Import and use in hooks**:
   ```python
   from .utils.tts import synthesize_speech, save_audio_file

   # Synthesize speech and get audio bytes
   audio_bytes = synthesize_speech("Hello world")

   # Or save directly to file
   success = save_audio_file("Hello world", "output.mp3")
   ```

3. **Customize voice** (optional):
   ```python
   audio_bytes = synthesize_speech("Hello world", voice_id="custom_voice_id")
   ```

### Function Signatures

- `synthesize_speech(text: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> bytes | None`
  - Returns audio bytes in MP3 format on success
  - Returns `None` on error (missing API key, network issues, etc.)

- `save_audio_file(text: str, file_path: str, voice_id: str = "EXAVITQu4vr4xnSDxMaL") -> bool`
  - Creates parent directories automatically if needed
  - Returns `True` on success
  - Returns `False` on error

## Configuration

### Required Environment Variables

- `ELEVENLABS_API_KEY`: Your ElevenLabs API key (required for all operations)

### Default Settings

- **Model**: eleven_turbo_v2_5 (hardcoded, not configurable)
- **Output Format**: MP3, 44.1kHz, 128kbps
- **Default Voice**: EXAVITQu4vr4xnSDxMaL (Rachel voice)

### Customization in Template

The template uses Jinja2 variable `{{ config.project.name }}` in the module docstring, which will be replaced with the actual project name during generation.

## Testing

### Test Template Rendering

Verify the template renders correctly with project configuration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Test Rendered Implementation

Check that the rendered file has no Jinja2 syntax remaining:

```bash
grep -c "{{" .claude/hooks/utils/tts/elevenlabs_tts.py
```

Expected output: `0`

### Validate Python Syntax

Verify the rendered file is valid Python:

```bash
python3 -m py_compile .claude/hooks/utils/tts/elevenlabs_tts.py
```

### Code Quality Checks

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Manual Function Testing

Test the functions with a valid API key:

```bash
uv run .claude/hooks/utils/tts/elevenlabs_tts.py
```

Then in Python:
```python
from .claude.hooks.utils.tts import synthesize_speech, save_audio_file

# Test synthesis
audio = synthesize_speech("Test message")
assert audio is not None
assert isinstance(audio, bytes)

# Test file saving
success = save_audio_file("Test message", "/tmp/test_output.mp3")
assert success is True
```

## Notes

- **Pattern Consistency**: This template follows the exact same pattern as `oai.py` for LLM utilities, ensuring developers have a consistent experience across different API integrations
- **Lenient Error Handling**: Uses bare `except` clause to catch all exceptions and return None/False, prioritizing robustness over specific error messages
- **No CLI Interface**: Unlike some source implementations, this template provides only the library functions - generated projects can add CLI wrappers if needed
- **Voice ID Selection**: The default voice ID 'EXAVITQu4vr4xnSDxMaL' (Rachel) is a high-quality English voice suitable for most use cases
- **Future Expansion**: The TTS module structure allows for additional TTS providers (openai_tts.py, google_tts.py, etc.) following the same pattern
- **Dependencies Management**: Using uv script dependencies ensures the elevenlabs library is available when running as standalone script
- **File Path Handling**: `save_audio_file()` automatically creates parent directories using `Path.mkdir(parents=True, exist_ok=True)`
