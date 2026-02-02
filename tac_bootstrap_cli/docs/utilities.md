# LLM, TTS & Observability Utilities

TAC Bootstrap includes utility wrappers for LLM, TTS, and observability, enabling hooks and scripts to leverage AI capabilities and monitoring infrastructure.

## Overview

Utilities provide a unified interface for:
- **LLM**: Generate text, completions, and agent names
- **TTS**: Convert text to speech for notifications
- **Observability**: Event summarization, model tracking, and configuration management

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

## Observability Utilities

Observability utilities enable hooks to track events, summarize context, and integrate with monitoring infrastructure.

### Location

```
.claude/hooks/utils/
├── constants.py       # Configuration constants and session utilities
├── summarizer.py      # AI-powered event summarization
└── model_extractor.py # LLM model detection and utilities (planned)
```

### Configuration Constants (`constants.py`)

Provides shared configuration and session management utilities for hooks.

**Location:** `.claude/hooks/utils/constants.py`

**Key Functions:**

```python
def get_session_log_dir(session_id: str) -> Path:
    """Get the log directory for a specific session."""

def ensure_session_log_dir(session_id: str) -> Path:
    """Ensure the log directory for a session exists."""
```

**Usage Example:**

```python
from utils.constants import ensure_session_log_dir

# In a hook that needs to log session data
session_id = input_data.get('session_id', 'unknown')
log_dir = ensure_session_log_dir(session_id)
log_file = log_dir / 'my_hook.json'

with open(log_file, 'w') as f:
    json.dump(hook_data, f)
```

**Configuration:**

The base log directory can be customized via environment variable:

```bash
export CLAUDE_HOOKS_LOG_DIR="/path/to/custom/logs"
```

Default: `logs/` in the current working directory

**Output Structure:**

All session logs are organized by session ID:

```
logs/
├── session-abc-123/
│   ├── hook_logs.json
│   ├── pre_compact.json
│   ├── subagent_stop.json
│   └── chat.json
├── session-def-456/
│   ├── hook_logs.json
│   └── user_prompt_submit.json
```

### Event Summarization (`summarizer.py`)

Provides AI-powered summarization of events using Claude Haiku for generating concise, one-sentence summaries.

**Location:** `.claude/hooks/utils/summarizer.py`

**Functions:**

```python
def generate_event_summary(event_text: str) -> Optional[str]:
    """
    Generate a concise one-sentence summary of an event.

    Args:
        event_text: The event text to summarize

    Returns:
        A one-sentence summary (max 150 characters), or None on error
    """
```

**Setup:**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Usage Example:**

```python
from utils.summarizer import generate_event_summary

# Summarize a lengthy event
event_description = """
User executed multiple file operations: created config.json,
updated main.py with new error handling, ran tests which passed 97/100.
Session focused on error handling improvements.
"""

summary = generate_event_summary(event_description)
# → "Session improved error handling with 97% test pass rate."
```

**Configuration:**

- Model: `claude-haiku-4-5-20251001`
- Max tokens: 50
- Temperature: 0.3 (for consistency)
- Max length: 150 characters (auto-truncated if exceeded)

**Return Value:**

- On success: Summary string (≤150 characters)
- On error: `None` (graceful failure when API key missing or unavailable)

**Integration with Hooks:**

Example: Use summarizer in a custom hook to create concise audit logs

```python
import json
import sys
from utils.summarizer import generate_event_summary
from utils.constants import ensure_session_log_dir

def main():
    input_data = json.load(sys.stdin)
    session_id = input_data.get('session_id')

    # Summarize the event
    event_text = input_data.get('details', '')
    summary = generate_event_summary(event_text)

    # Log with summary
    log_dir = ensure_session_log_dir(session_id)
    log_file = log_dir / 'summarized_events.json'

    entry = {
        'timestamp': datetime.now().isoformat(),
        'original': event_text[:200] + '...' if len(event_text) > 200 else event_text,
        'summary': summary
    }

    # Write to log...
```

### Cross-Reference with Hooks

These observability utilities are used by the TAC-12 hooks to provide comprehensive monitoring:

- **send_event.py**: Uses constants for session directory management
- **session_start.py**: Captures initial context (git, model, project)
- **pre_compact.py**: Uses constants for session-aware logging
- **subagent_stop.py**: Logs subagent completion with session isolation
- **user_prompt_submit.py**: Uses constants for audit trail storage

See [Additional TAC-12 Hooks](hooks.md#additional-tac-12-hooks) for detailed integration patterns.

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

### Session Context Tracking

```python
# Use constants to organize session logs
from utils.constants import ensure_session_log_dir
import json

session_id = "session-abc-123"
log_dir = ensure_session_log_dir(session_id)

# All logs for this session are automatically organized
config_log = log_dir / "config.json"
metrics_log = log_dir / "metrics.json"
```

### Event Summarization in Hooks

```python
# Use summarizer to create concise audit logs
from utils.summarizer import generate_event_summary
from utils.constants import ensure_session_log_dir
import json
from datetime import datetime

session_id = input_data.get('session_id')
log_dir = ensure_session_log_dir(session_id)

# Summarize lengthy operation
event_summary = generate_event_summary(long_event_description)

# Log the summary
audit_entry = {
    'timestamp': datetime.now().isoformat(),
    'summary': event_summary,
    'full_details': long_event_description
}

with open(log_dir / 'audit.json', 'w') as f:
    json.dump([audit_entry], f)
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
