---
doc_type: feature
adw_id: feature_Tac_9_task_15
date: 2026-01-26
idk:
  - jinja2-template
  - tts
  - offline-tts
  - pyttsx3
  - uv-script
  - template-generation
tags:
  - feature
  - tts
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2
  - .claude/hooks/utils/tts/pyttsx3_tts.py
---

# pyttsx3 Local TTS Template

**ADW ID:** feature_Tac_9_task_15
**Date:** 2026-01-26
**Specification:** specs/issue-256-adw-feature_Tac_9_task_15-sdlc_planner-pyttsx3-tts-template.md

## Overview

Added a Jinja2 template for pyttsx3-based local text-to-speech functionality. This provides TAC Bootstrap CLI users with an offline TTS option that works without API keys or internet connectivity, complementing existing cloud-based TTS services (OpenAI, ElevenLabs).

## What Was Built

- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2`
  - UV script format with inline pyttsx3 dependency declaration
  - Configurable voice properties (rate, volume, voice_index) via Jinja2 variables
  - Project name interpolation in docstrings

- **Rendered Example**: `.claude/hooks/utils/tts/pyttsx3_tts.py`
  - Functional Python script demonstrating template output
  - Ready-to-use for this repository

- **Core Functions**:
  - `synthesize_speech(text: str) -> bool` - Real-time playback
  - `save_to_file(text: str, file_path: str) -> bool` - Save audio to file

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2` (NEW): Jinja2 template for pyttsx3 TTS wrapper with configurable voice properties
- `.claude/hooks/utils/tts/pyttsx3_tts.py` (NEW): Rendered example implementation for TAC Bootstrap repository

### Key Changes

- Template uses UV script format with `# /// script` dependency block for automatic pyttsx3 installation
- Configurable Jinja2 variables under `config.tts.pyttsx3` namespace:
  - `rate` (default: 150 words/min)
  - `volume` (default: 0.9)
  - `voice_index` (default: 0)
- Robust error handling for ImportError (missing pyttsx3), RuntimeError (system TTS engine unavailable), and general exceptions
- Cross-platform support with system-specific TTS engines (macOS: NSSpeechSynthesizer, Windows: SAPI5, Linux: espeak)
- API interface matches existing TTS templates for drop-in compatibility

## How to Use

### As a TAC Bootstrap CLI User

1. When generating a new project or updating templates, the pyttsx3 TTS wrapper will be available at `.claude/hooks/utils/tts/pyttsx3_tts.py`

2. Configure voice properties in your project's configuration file:
```yaml
tts:
  pyttsx3:
    rate: 150      # Speech rate in words per minute
    volume: 0.9    # Volume level (0.0 to 1.0)
    voice_index: 0 # System voice index to use
```

3. Use the generated wrapper in your code:
```python
from utils.tts.pyttsx3_tts import synthesize_speech, save_to_file

# Real-time playback
success = synthesize_speech("Task completed successfully!")

# Save to file
success = save_to_file("Report ready", "notification.wav")
```

### System Requirements

- **macOS**: Uses NSSpeechSynthesizer (built-in, no installation needed)
- **Windows**: Uses SAPI5 (built-in, no installation needed)
- **Linux**: Requires espeak: `sudo apt-get install espeak`

## Configuration

The template supports the following Jinja2 variables with defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `config.project.name` | - | Project name for docstring interpolation |
| `config.tts.pyttsx3.rate` | 150 | Speech rate in words per minute |
| `config.tts.pyttsx3.volume` | 0.9 | Volume level (0.0 to 1.0) |
| `config.tts.pyttsx3.voice_index` | 0 | System voice index to use |

All TTS-specific settings are namespaced under `config.tts.pyttsx3` to distinguish from other TTS providers.

## Testing

### Test Template Rendering
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Test Linting
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Test Type Checking
```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Test CLI Functionality
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Test Rendered Script (Manual)
```bash
# Test real-time playback
python .claude/hooks/utils/tts/pyttsx3_tts.py "Test message"

# Test with UV (recommended)
uv run .claude/hooks/utils/tts/pyttsx3_tts.py "Hello from pyttsx3!"
```

Note: Manual testing requires the system TTS engine to be available. On Linux, ensure espeak is installed first.

## Notes

- This template provides an **offline fallback** to cloud-based TTS services, useful for environments without internet access or API keys
- The pyttsx3 library wraps platform-specific TTS engines, so voice quality and available voices vary by operating system
- Users can discover available voices by calling `engine.getProperty('voices')` in the rendered script
- The template follows the same API interface as `openai_tts.py.j2` for consistency across TTS providers
- Future enhancement: Could add a `list_voices()` function to help users discover available system voices
- No version pinning for pyttsx3 dependency - relies on UV's dependency resolution
