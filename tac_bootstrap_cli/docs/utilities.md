# LLM & TTS Utilities

TAC Bootstrap includes utility wrappers for LLM and TTS providers, enabling hooks and scripts to leverage AI capabilities.

## Overview

Utilities provide a unified interface for:
- **LLM**: Generate text, completions, and agent names
- **TTS**: Convert text to speech for notifications

Located in `.claude/hooks/utils/`

## LLM Utilities

### Location

```
.claude/hooks/utils/llm/
├── __init__.py
├── anth.py      # Anthropic (Claude)
├── oai.py       # OpenAI
└── ollama.py    # Ollama (local)
```

### Common Interface

All LLM providers implement the same interface:

```python
def prompt_llm(prompt_text: str) -> str | None:
    """Send prompt to LLM and get response."""

def generate_completion_message() -> str | None:
    """Generate a friendly completion message."""

def generate_agent_name() -> str | None:
    """Generate a creative agent name."""
```

### Anthropic (`anth.py`)

Uses Claude 3.5 Haiku for fast, cost-effective responses.

**Setup:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Usage:**
```python
from .utils.llm.anth import prompt_llm, generate_completion_message

# Basic prompt
response = prompt_llm("Summarize this code in one sentence")

# Completion message
message = generate_completion_message()
# → "All done! Ready for your next task."
```

**Configuration:**
- Model: `claude-3-5-haiku-20241022`
- Max tokens: 100
- Temperature: 0.7

### OpenAI (`oai.py`)

Uses GPT-4.1 Nano for fast responses.

**Setup:**
```bash
export OPENAI_API_KEY="sk-..."
```

**Usage:**
```python
from .utils.llm.oai import prompt_llm, generate_completion_message

response = prompt_llm("What's the best practice for error handling?")
```

**Configuration:**
- Model: `gpt-4.1-nano`
- Max tokens: 100
- Temperature: 0.7

### Ollama (`ollama.py`)

Uses local Ollama instance for offline/private inference.

**Setup:**
```bash
# Start Ollama server
ollama serve

# Pull a model
ollama pull llama3.2
```

**Usage:**
```python
from .utils.llm.ollama import prompt_llm, generate_completion_message

response = prompt_llm("Explain this function")
```

**Configuration:**
- Model: `llama3.2` (configurable)
- Host: `http://localhost:11434`

### Selecting Provider

Import from specific module:

```python
# Use Anthropic
from .utils.llm.anth import prompt_llm

# Use OpenAI
from .utils.llm.oai import prompt_llm

# Use Ollama (local)
from .utils.llm.ollama import prompt_llm
```

Or use environment-based selection:

```python
import os

provider = os.getenv("LLM_PROVIDER", "anth")

if provider == "anth":
    from .utils.llm.anth import prompt_llm
elif provider == "oai":
    from .utils.llm.oai import prompt_llm
else:
    from .utils.llm.ollama import prompt_llm
```

## TTS Utilities

### Location

```
.claude/hooks/utils/tts/
├── __init__.py
├── elevenlabs_tts.py    # ElevenLabs
├── openai_tts.py        # OpenAI TTS
└── pyttsx3_tts.py       # Local (offline)
```

### Common Interface

All TTS providers implement:

```python
def speak(text: str) -> bool:
    """Convert text to speech and play."""

def save_audio(text: str, path: str) -> bool:
    """Convert text to speech and save to file."""
```

### ElevenLabs (`elevenlabs_tts.py`)

High-quality, natural-sounding voices.

**Setup:**
```bash
export ELEVENLABS_API_KEY="..."
```

**Usage:**
```python
from .utils.tts.elevenlabs_tts import speak, save_audio

# Speak immediately
speak("Task completed successfully")

# Save to file
save_audio("Your report is ready", "output.mp3")
```

**Configuration:**
- Model: Turbo v2.5
- Voice: Configurable via `ELEVENLABS_VOICE_ID`

### OpenAI TTS (`openai_tts.py`)

OpenAI's text-to-speech API.

**Setup:**
```bash
export OPENAI_API_KEY="sk-..."
```

**Usage:**
```python
from .utils.tts.openai_tts import speak, save_audio

speak("Build completed with no errors")
```

**Configuration:**
- Model: `tts-1` (fast) or `tts-1-hd` (quality)
- Voice: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

### pyttsx3 (`pyttsx3_tts.py`)

Offline TTS using system voices.

**Setup:**
```bash
pip install pyttsx3
```

**Usage:**
```python
from .utils.tts.pyttsx3_tts import speak

speak("No internet required")
```

**Features:**
- Works offline
- Uses system voices
- No API keys needed
- Cross-platform

**Configuration:**
- Rate: Adjustable speech rate
- Voice: System default or specified

## Use Cases

### Hook Notifications

```python
# In stop.py hook
from .utils.llm.anth import generate_completion_message
from .utils.tts.elevenlabs_tts import speak

message = generate_completion_message()
speak(message)
```

### Session Summaries

```python
# Generate and speak session summary
from .utils.llm.anth import prompt_llm
from .utils.tts.openai_tts import speak

summary = prompt_llm(f"Summarize in one sentence: {session_log}")
speak(summary)
```

### Error Alerts

```python
# Speak error notifications
from .utils.tts.pyttsx3_tts import speak

if test_failed:
    speak("Warning: Tests failed. Please check the output.")
```

### Agent Names

```python
# Generate creative agent names
from .utils.llm.anth import generate_agent_name

name = generate_agent_name()
# → "Phoenix", "Quantum", "Nexus"
```

## Environment Variables

### LLM

| Variable | Provider | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic | Claude API key |
| `OPENAI_API_KEY` | OpenAI | OpenAI API key |
| `OLLAMA_HOST` | Ollama | Ollama server URL |
| `LLM_PROVIDER` | All | Default provider selection |

### TTS

| Variable | Provider | Description |
|----------|----------|-------------|
| `ELEVENLABS_API_KEY` | ElevenLabs | API key |
| `ELEVENLABS_VOICE_ID` | ElevenLabs | Voice selection |
| `OPENAI_API_KEY` | OpenAI TTS | API key |
| `TTS_PROVIDER` | All | Default provider selection |

### Personalization

| Variable | Description |
|----------|-------------|
| `ENGINEER_NAME` | Name for personalized messages |

## Fallback Strategy

Implement graceful degradation:

```python
def speak_with_fallback(text):
    """Try providers in order until one works."""
    try:
        from .utils.tts.elevenlabs_tts import speak
        if speak(text):
            return True
    except:
        pass

    try:
        from .utils.tts.openai_tts import speak
        if speak(text):
            return True
    except:
        pass

    try:
        from .utils.tts.pyttsx3_tts import speak
        return speak(text)
    except:
        return False
```

## Adding Custom Providers

### LLM Provider Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["your-provider-sdk"]
# ///

import os

def prompt_llm(prompt_text: str) -> str | None:
    """Send prompt to LLM."""
    api_key = os.getenv("YOUR_API_KEY")
    if not api_key:
        return None

    try:
        # Your implementation
        response = your_sdk.complete(prompt_text)
        return response.text
    except Exception:
        return None

def generate_completion_message() -> str | None:
    """Generate completion message."""
    prompt = "Generate a short, friendly completion message..."
    return prompt_llm(prompt)
```

### TTS Provider Template

```python
#!/usr/bin/env -S uv run --script

import os

def speak(text: str) -> bool:
    """Convert text to speech and play."""
    try:
        # Your implementation
        audio = your_tts_sdk.synthesize(text)
        play_audio(audio)
        return True
    except Exception:
        return False

def save_audio(text: str, path: str) -> bool:
    """Save speech to file."""
    try:
        audio = your_tts_sdk.synthesize(text)
        with open(path, 'wb') as f:
            f.write(audio)
        return True
    except Exception:
        return False
```
