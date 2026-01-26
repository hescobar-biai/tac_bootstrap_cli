"""TTS utilities for tac_bootstrap.

Provides a unified interface for text-to-speech implementations.
This module serves as a placeholder for future TTS provider implementations.
"""

from .elevenlabs_tts import synthesize_speech, save_audio_file

__all__ = ["synthesize_speech", "save_audio_file"]
