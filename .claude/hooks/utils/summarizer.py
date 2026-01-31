#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "anthropic",
#     "python-dotenv",
# ]
# ///

"""
Event summarizer utility for Claude Code hooks.

This module provides a simple interface for generating AI-powered summaries
of events using Claude Haiku, following the hook utility pattern.
"""

import os
from typing import Optional
from dotenv import load_dotenv


def generate_event_summary(event_text: str) -> Optional[str]:
    """
    Generate a concise one-sentence summary of an event.

    Args:
        event_text: The event text to summarize

    Returns:
        A one-sentence summary (max 150 characters), or None on error
    """
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""Summarize the following event in exactly one sentence.
The summary must be concise, clear, and no more than 150 characters.

Event:
{event_text}

Return ONLY the summary sentence, with no additional text, quotes, or formatting."""

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = message.content[0].text.strip()

        # Validate length constraint
        if len(summary) > 150:
            summary = summary[:147] + "..."

        return summary

    except Exception:
        return None
