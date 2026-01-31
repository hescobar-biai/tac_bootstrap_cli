#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Model Extractor Utility
Extracts model name from Claude Code session context with file-based caching.
"""

import json
import os
from pathlib import Path
from typing import Optional


def get_model_from_transcript(session_id: str) -> Optional[str]:
    """
    Extract model name from session context with file-based caching.

    Reads the model name from .claude/session_context.json or
    agents/session_metadata/<session_id>.json and caches it in
    .claude/data/claude-model-cache/<session_id>.txt for fast retrieval.

    Args:
        session_id: The Claude session ID

    Returns:
        Model name string (e.g., "claude-haiku-4-5-20251001") or None on error.
        Never raises exceptions; gracefully degrades to None on failures.
    """
    try:
        # Try to get cached model first
        cache_dir = Path(__file__).parent.parent.parent / "data" / "claude-model-cache"
        cache_file = cache_dir / f"{session_id}.txt"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    cached_model = f.read().strip()
                    if cached_model:
                        return cached_model
            except (IOError, OSError):
                # Cache read failed, will try to extract fresh
                pass

        # Cache miss or unreadable - extract from session context
        model = _extract_model_from_session()

        if model:
            # Try to cache the result
            try:
                cache_dir.mkdir(parents=True, exist_ok=True)
                with open(cache_file, 'w') as f:
                    f.write(model)
            except (IOError, OSError):
                # Cache write failed, not critical - continue without cache
                pass

        return model

    except Exception:
        # Graceful degradation - never raise exceptions
        return None


def _extract_model_from_session() -> Optional[str]:
    """
    Extract model name from session context file.

    Tries two locations:
    1. .claude/session_context.json (standard location)
    2. agents/session_metadata/<session_id>.json (alternative location)

    Returns:
        Model name string or None if not found or on error.
    """
    try:
        # Try standard location: .claude/session_context.json
        session_context_path = Path.cwd() / ".claude" / "session_context.json"

        if session_context_path.exists():
            try:
                with open(session_context_path, 'r') as f:
                    data = json.load(f)
                    model = data.get('model')
                    if model and isinstance(model, str) and model != 'unknown':
                        return model
            except (json.JSONDecodeError, IOError, OSError):
                pass

        # No valid model found
        return None

    except Exception:
        return None
