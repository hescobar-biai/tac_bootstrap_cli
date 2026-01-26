#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "python-dotenv",
# ]
# ///

import os
from pathlib import Path
from dotenv import load_dotenv


def synthesize_speech(text: str, voice: str = "alloy", model: str = "tts-1", speed: float = 1.0) -> bytes | None:
    """
    Synthesize speech from text using OpenAI TTS for TAC Bootstrap.

    Args:
        text (str): The text to synthesize
        voice (str): The voice to use (default: 'alloy')
                    Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): The model to use (default: 'tts-1')
                    Options: tts-1 (standard), tts-1-hd (high definition)
        speed (float): The playback speed (default: 1.0, range: 0.25 to 4.0)

    Returns:
        bytes: The audio data in MP3 format, or None if error
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.audio.speech.create(
            input=text,
            voice=voice,
            model=model,
            speed=speed,
            response_format="mp3",
        )

        # Collect all audio bytes
        audio_bytes = response.content
        return audio_bytes

    except Exception:
        return None


def save_audio_file(text: str, file_path: str, voice: str = "alloy", model: str = "tts-1", speed: float = 1.0) -> bool:
    """
    Synthesize speech and save to file.

    Args:
        text (str): The text to synthesize
        file_path (str): The path where to save the audio file
        voice (str): The voice to use (default: 'alloy')
                    Options: alloy, echo, fable, onyx, nova, shimmer
        model (str): The model to use (default: 'tts-1')
                    Options: tts-1 (standard), tts-1-hd (high definition)
        speed (float): The playback speed (default: 1.0, range: 0.25 to 4.0)

    Returns:
        bool: True if successful, False if error
    """
    try:
        audio_bytes = synthesize_speech(text, voice, model, speed)
        if audio_bytes is None:
            return False

        # Ensure parent directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Write audio to file
        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        return True

    except Exception:
        return False
