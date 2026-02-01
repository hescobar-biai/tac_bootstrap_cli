---
doc_type: feature
adw_id: feature_Tac_12_task_33
date: 2026-01-31
idk:
  - text-to-speech
  - tts-synthesis
  - audio-generation
  - provider-integration
  - hook-utilities
  - elevenlabs
  - openai-tts
  - pyttsx3
  - lenient-error-handling
tags:
  - feature
  - hook-utilities
  - audio
  - tts
related_code:
  - .claude/hooks/utils/tts/__init__.py
  - .claude/hooks/utils/tts/elevenlabs_tts.py
  - .claude/hooks/utils/tts/openai_tts.py
  - .claude/hooks/utils/tts/pyttsx3_tts.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Create TTS Utilities Subdirectory

**ADW ID:** feature_Tac_12_task_33
**Date:** 2026-01-31
**Specification:** [issue-485-adw-feature_Tac_12_task_33-sdlc_planner-create-tts-utilities.md](../specs/issue-485-adw-feature_Tac_12_task_33-sdlc_planner-create-tts-utilities.md)

## Overview

Created a complete text-to-speech utilities module under `.claude/hooks/utils/tts/` providing composable, minimal TTS provider integrations for hook automation workflows. The feature offers three provider options (ElevenLabs, OpenAI, pyttsx3) with consistent function signatures and lenient error handling patterns suitable for notification and audio output use cases.

## What Was Built

- **ElevenLabs TTS Provider** - Cloud-based TTS using ElevenLabs Turbo v2.5 model with configurable voice IDs, outputs MP3 format
- **OpenAI TTS Provider** - Cloud-based TTS using OpenAI's API with multiple voice options and model selection, outputs MP3 format
- **pyttsx3 Offline TTS Provider** - Local system TTS without API dependencies, works across macOS, Windows, and Linux with speech rate and volume configuration
- **Package Initialization** - Central re-export module with convenient imports for all TTS functionality
- **Jinja2 Templates** - Four template files for CLI-based project generation (one for each provider plus package init)
- **Scaffold Integration** - Updated `scaffold_service.py` to include TTS utilities directory and all provider files during project generation

## Technical Implementation

### Files Modified

- `.claude/hooks/utils/tts/__init__.py` - Package initialization re-exporting `synthesize_speech()` and `save_audio_file()` from ElevenLabs provider
- `.claude/hooks/utils/tts/elevenlabs_tts.py` - ElevenLabs Turbo v2.5 integration with voice ID support and MP3 output
- `.claude/hooks/utils/tts/openai_tts.py` - OpenAI TTS wrapper with voice selection (alloy, echo, fable, onyx, nova, shimmer) and speed control
- `.claude/hooks/utils/tts/pyttsx3_tts.py` - Offline local TTS engine with cross-platform support and file output capability
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - Jinja2 template for package init
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` - Template for ElevenLabs provider
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` - Template for OpenAI provider
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2` - Template for pyttsx3 provider
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Updated to include TTS utilities in project scaffolding

### Key Changes

- **Modular Provider Architecture**: Each TTS provider maintains minimal responsibility with identical function signatures (`synthesize_speech()` and `save_audio_file()`)
- **Lenient Error Handling**: All providers return `None`/`False` on errors rather than raising exceptions, allowing consumers to decide error handling strategy
- **UV Script Format**: All provider files use UV script headers with explicit dependency declarations for reproducible execution
- **Environment Variable Authentication**: Cloud providers (ElevenLabs, OpenAI) load API keys from `.env` via python-dotenv
- **Cross-Platform File I/O**: Uses `pathlib.Path` for portable file operations across operating systems
- **API Lenience**: No validation of text length, voice parameters, or API limits at utility level - focuses on composition

## How to Use

### ElevenLabs Provider

```python
from tac_bootstrap.hooks.utils.tts import synthesize_speech, save_audio_file

# Synthesize to bytes (requires ELEVENLABS_API_KEY environment variable)
audio_bytes = synthesize_speech("Welcome to TAC Bootstrap", voice_id="EXAVITQu4vr4xnSDxMaL")
if audio_bytes:
    print(f"Generated {len(audio_bytes)} bytes of audio")

# Save directly to file
success = save_audio_file("Task complete!", "/tmp/notification.mp3")
if success:
    print("Audio saved successfully")
```

### OpenAI Provider

```python
from tac_bootstrap.hooks.utils.tts.openai_tts import synthesize_speech, save_audio_file

# Synthesize with voice options
audio_bytes = synthesize_speech("Hello", voice="nova", model="tts-1-hd", speed=0.9)

# Save with custom parameters
success = save_audio_file("Process finished", "/tmp/alert.mp3", voice="shimmer")
```

### pyttsx3 Offline Provider

```python
from tac_bootstrap.hooks.utils.tts.pyttsx3_tts import synthesize_speech, save_to_file

# Play audio immediately (no file output)
success = synthesize_speech("Task starting")

# Save to file for later playback
success = save_to_file("Workflow complete", "/tmp/output.wav")
```

## Configuration

### Environment Variables

**ElevenLabs:**
- `ELEVENLABS_API_KEY` - Required for cloud-based synthesis

**OpenAI:**
- `OPENAI_API_KEY` - Required for cloud-based synthesis

**pyttsx3:**
- No environment variables required (offline operation)

### Voice Selection

**ElevenLabs:**
- Default voice ID: `EXAVITQu4vr4xnSDxMaL`
- Customizable via `voice_id` parameter

**OpenAI:**
- Voices: alloy, echo, fable, onyx, nova, shimmer
- Default: alloy
- Models: tts-1 (standard), tts-1-hd (high definition)
- Speed: 0.25 to 4.0 (default: 1.0)

**pyttsx3:**
- Voice selection by system availability
- Speech rate: 150 words per minute (default, configurable)
- Volume: 0.9 (0.0 to 1.0 scale)

## Testing

### Install Dependencies

```bash
# All providers
cd tac_bootstrap_cli && uv run pip install elevenlabs openai pyttsx3 python-dotenv

# Or individual providers
uv run pip install elevenlabs
uv run pip install openai
uv run pip install pyttsx3
```

### Test ElevenLabs Provider

```bash
# Requires ELEVENLABS_API_KEY in .env
uv run .claude/hooks/utils/tts/elevenlabs_tts.py << 'EOF'
from .elevenlabs_tts import synthesize_speech
audio = synthesize_speech("Testing ElevenLabs TTS")
assert audio is not None, "Failed to generate audio"
print("✓ ElevenLabs test passed")
EOF
```

### Test OpenAI Provider

```bash
# Requires OPENAI_API_KEY in .env
uv run .claude/hooks/utils/tts/openai_tts.py << 'EOF'
from .openai_tts import synthesize_speech
audio = synthesize_speech("Testing OpenAI TTS", voice="nova")
assert audio is not None, "Failed to generate audio"
print("✓ OpenAI test passed")
EOF
```

### Test pyttsx3 Provider

```bash
# No API key required
uv run .claude/hooks/utils/tts/pyttsx3_tts.py << 'EOF'
from .pyttsx3_tts import synthesize_speech
success = synthesize_speech("Testing offline TTS")
assert success is True, "Failed to synthesize speech"
print("✓ pyttsx3 test passed")
EOF
```

### Test Scaffold Integration

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "scaffold" --tb=short
```

### Full Validation

```bash
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short
uv run ruff check .
uv run mypy tac_bootstrap/
uv run tac-bootstrap --help
```

## Notes

### Design Patterns

- **Minimal and Composable**: TTS utilities are thin, focused building blocks without cross-cutting concerns like validation, logging, or caching
- **Lenient Error Handling**: Functions return `None`/`False` instead of raising exceptions, allowing consumers full control over error strategies
- **Provider Abstraction**: Consistent function signatures across all providers enable drop-in provider swapping
- **Environment-Driven Authentication**: API keys loaded from `.env` at runtime via python-dotenv for security
- **Cross-Platform Compatibility**: Uses `pathlib.Path` for portable file operations

### Provider-Specific Details

**ElevenLabs Turbo v2.5:**
- Output format: MP3 (44.1 kHz, 128 kbps)
- Requires: `ELEVENLABS_API_KEY` environment variable
- Audio return type: `bytes` from `synthesize_speech()`

**OpenAI TTS:**
- Output format: MP3
- Voice options: alloy, echo, fable, onyx, nova, shimmer
- Model options: tts-1 (standard, faster), tts-1-hd (higher quality)
- Speed range: 0.25 to 4.0x playback speed
- Requires: `OPENAI_API_KEY` environment variable

**pyttsx3 Offline:**
- Output format: WAV or platform-native (depends on system TTS engine)
- No API key required
- System Requirements:
  - macOS: Uses NSSpeechSynthesizer (built-in)
  - Windows: Uses SAPI5 (built-in)
  - Linux: Requires espeak (`sudo apt-get install espeak`)
- Returns `bool` (True/False) instead of bytes

### Integration Points

- TTS utilities are designed to integrate with `.claude/hooks/notification.py` for audio notification support
- Used by hooks that require audio output capabilities
- No client-side validation at utility level (providers are lenient by design)
- File paths use `pathlib.Path` for automatic parent directory creation

### Related Features

- **Task 32 (LLM Utilities)**: Established foundational patterns for provider modularization
- **Task 34 (Status Lines)**: Complementary hook utilities for status feedback
- **Future Consumers**: Hook implementations that leverage TTS utilities for audio notifications and spoken feedback

