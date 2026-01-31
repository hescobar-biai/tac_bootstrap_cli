---
doc_type: feature
adw_id: feature_Tac_12_task_30
date: 2026-01-31
idk:
  - model-extraction
  - session-context
  - file-based-caching
  - hook-utilities
  - observability
tags:
  - feature
  - hook-utility
  - analytics
related_code:
  - .claude/hooks/utils/model_extractor.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Model Extractor Hook Utility

**ADW ID:** feature_Tac_12_task_30
**Date:** 2026-01-31
**Specification:** specs/issue-482-adw-feature_Tac_12_task_30-sdlc_planner-model-extractor.md

## Overview

Created a lightweight utility module `model_extractor.py` that extracts Claude model names from session context files with file-based caching. This utility is called by hook scripts to identify which Claude model is executing the current session for event logging and analytics purposes. The implementation provides robust error handling with graceful degradation and zero external dependencies.

## What Was Built

- **Model Extractor Utility** - Core Python module (`model_extractor.py`) that extracts and caches model information
- **Jinja2 Template** - Template file (`model_extractor.py.j2`) for CLI-based project generation with project metadata
- **Service Registration** - Integration in `scaffold_service.py` to register the utility in the hook infrastructure

## Technical Implementation

### Files Created

- `.claude/hooks/utils/model_extractor.py` - Base utility implementation with caching logic
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2` - Jinja2 template for generated projects

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Added registration of `model_extractor.py` to hook utilities list

### Key Features

- **Single Public Function**: `get_model_from_transcript(session_id: str) -> Optional[str]`
- **File-Based Caching**: Caches extracted model in `.claude/data/claude-model-cache/<session_id>.txt` for fast retrieval
- **Session Context Reading**: Reads model name from `.claude/session_context.json`
- **Graceful Error Handling**: Never raises exceptions; returns `None` on any failure (file not found, malformed JSON, I/O errors)
- **Zero External Dependencies**: Uses only Python standard library (`json`, `pathlib`, `os`)
- **Auto-Directory Creation**: Automatically creates cache directory with `mkdir(parents=True, exist_ok=True)`
- **Cache Optimization**: Skips caching gracefully if directory creation fails

### Implementation Details

The utility follows a two-phase approach:

1. **Cache Check Phase**
   - First attempts to read from `.claude/data/claude-model-cache/<session_id>.txt`
   - Returns immediately if valid cached model found

2. **Extraction Phase** (on cache miss)
   - Reads `.claude/session_context.json` to extract model field
   - Validates model is a non-empty string and not 'unknown'
   - Attempts to cache the result for future calls
   - Returns extracted model or `None` if not found

All I/O operations are wrapped in try-except blocks to ensure the utility never crashes the calling hook script.

## How to Use

### Basic Usage

```python
from utils.model_extractor import get_model_from_transcript

# Get model for a specific session
model = get_model_from_transcript(session_id="some-session-id")
if model:
    print(f"Running on: {model}")
else:
    print("Model information unavailable")
```

### In Hook Scripts

Hook scripts like `send_event.py` can call this utility to include model information in event payloads:

```python
from utils.model_extractor import get_model_from_transcript

def send_event(event_type: str, data: dict) -> None:
    """Send event with model information."""
    session_id = os.getenv('CLAUDE_SESSION_ID')
    model = get_model_from_transcript(session_id)

    event_payload = {
        'type': event_type,
        'model': model,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }

    # Send to event logging service
    log_event(event_payload)
```

## Configuration

### Cache Directory Structure

The utility automatically creates and manages the cache directory:

```
.claude/data/claude-model-cache/
├── session-1.txt
├── session-2.txt
└── session-3.txt
```

Each cache file contains a single line with the model name (e.g., `claude-haiku-4-5-20251001`).

### Environment

The utility reads from:
- **Primary**: `.claude/session_context.json` - Main session metadata file
- **Cache**: `.claude/data/claude-model-cache/<session_id>.txt` - Model cache

No environment variables or configuration files are required.

## Testing

### Verify Installation

```bash
# Check base file exists
ls -la .claude/hooks/utils/model_extractor.py

# Check template exists
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/model_extractor.py.j2

# Verify syntax
python3 -c "import json; exec(open('.claude/hooks/utils/model_extractor.py').read())"
```

### Verify Service Registration

```bash
# Check model_extractor is registered in scaffold_service.py
grep -n "model_extractor.py" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py

# Verify scaffold_service has valid Python syntax
cd tac_bootstrap_cli && python3 -m py_compile tac_bootstrap/application/scaffold_service.py
```

### Run Linting and Type Checking

```bash
# Check code style
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/application/scaffold_service.py

# Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/application/scaffold_service.py
```

### Manual Functionality Test

Create a test script to verify the utility works:

```bash
# Create a temporary session context for testing
mkdir -p .claude
cat > .claude/session_context.json << 'EOF'
{
  "session_id": "test-session-123",
  "model": "claude-haiku-4-5-20251001",
  "timestamp": "2026-01-31T00:00:00Z"
}
EOF

# Test the utility
python3 -c "
import sys
sys.path.insert(0, '.claude/hooks/utils')
from model_extractor import get_model_from_transcript
model = get_model_from_transcript('test-session-123')
print(f'Model: {model}')
assert model == 'claude-haiku-4-5-20251001', 'Cache test failed'
print('✓ Cache test passed')
"
```

## Notes

### Design Decisions

- **Session Immutability**: Model name is immutable per session, so cache never needs TTL refresh—cache expires when session ends
- **Graceful Degradation**: All failures return `None` rather than raising exceptions, allowing hook scripts to continue functioning even if model extraction fails
- **Optimization Over Correctness**: Cache is purely an optimization; correctness doesn't depend on successful caching
- **Zero Dependencies**: Uses only Python standard library to minimize bootstrap overhead for hook execution

### Integration Pattern

This utility follows the existing hook utility pattern established by:
- `constants.py` - Shared constants for hooks
- `summarizer.py` - Text summarization utility

All hook utilities are:
- Registered in `scaffold_service.py`
- Templated with Jinja2 for project customization
- Pure Python with no external dependencies
- Included in the `.claude/hooks/utils/` directory structure

### Related Tasks

This is Task 30 in the Wave 4 (Hook Utilities) implementation phase:
- **Task 29**: Create `summarizer.py` hook utility (completed)
- **Task 30**: Create `model_extractor.py` hook utility (current)
- **Task 31+**: Additional hook utilities (pending)

### Future Enhancements

Potential improvements for future iterations:
- TTL-based cache invalidation for sessions lasting longer than expected
- Model name validation against known Claude model versions
- Cache statistics tracking (hits/misses) for observability
- Fallback to environment variables if session context unavailable
