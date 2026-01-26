#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

"""
pyttsx3 TTS Wrapper for TAC Bootstrap

This module provides offline text-to-speech synthesis using pyttsx3.
It offers an API-free alternative to cloud-based TTS services.

System Requirements:
- macOS: Uses NSSpeechSynthesizer (built-in)
- Windows: Uses SAPI5 (built-in)
- Linux: Requires espeak (install via: sudo apt-get install espeak)

Usage:
    from utils.tts.pyttsx3_tts import synthesize_speech, save_to_file

    # Real-time playback
    success = synthesize_speech("Hello, world!")

    # Save to file
    success = save_to_file("Hello, world!", "output.wav")
"""

from pathlib import Path


def synthesize_speech(text: str) -> bool:
    """
    Synthesize speech from text using pyttsx3 offline TTS for TAC Bootstrap.

    This function initializes the pyttsx3 engine, configures voice properties,
    and plays the speech immediately through the system's default audio output.

    Args:
        text (str): The text to synthesize and speak

    Returns:
        bool: True if successful, False if error

    Example:
        >>> synthesize_speech("Task complete!")
        True
    """
    try:
        import pyttsx3

        # Initialize TTS engine
        engine = pyttsx3.init()

        # Configure voice properties from template variables
        engine.setProperty('rate', 150)        # Speech rate (words per minute)
        engine.setProperty('volume', 0.9)    # Volume (0.0 to 1.0)

        # Set voice by index if multiple voices are available
        voices = engine.getProperty('voices')
        if voices and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)

        # Speak the text
        engine.say(text)
        engine.runAndWait()

        return True

    except ImportError:
        # pyttsx3 not installed (should be handled by UV)
        return False
    except RuntimeError as e:
        # Engine initialization failed - system TTS not available
        # macOS: nsss engine error
        # Windows: sapi5 engine error
        # Linux: espeak not installed
        return False
    except Exception:
        # Other errors (invalid text, engine errors, etc.)
        return False


def save_to_file(text: str, file_path: str) -> bool:
    """
    Synthesize speech and save to an audio file.

    This function generates speech using pyttsx3 and saves it to the specified
    file path. The output format is typically WAV or MP3 depending on system support.

    Args:
        text (str): The text to synthesize
        file_path (str): The path where to save the audio file

    Returns:
        bool: True if successful, False if error

    Example:
        >>> save_to_file("Hello!", "output.wav")
        True
    """
    try:
        import pyttsx3

        # Initialize TTS engine
        engine = pyttsx3.init()

        # Configure voice properties from template variables
        engine.setProperty('rate', 150)        # Speech rate (words per minute)
        engine.setProperty('volume', 0.9)    # Volume (0.0 to 1.0)

        # Set voice by index if multiple voices are available
        voices = engine.getProperty('voices')
        if voices and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)

        # Ensure parent directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

        # Save speech to file
        engine.save_to_file(text, file_path)
        engine.runAndWait()

        return True

    except ImportError:
        # pyttsx3 not installed (should be handled by UV)
        return False
    except RuntimeError as e:
        # Engine initialization failed - system TTS not available
        return False
    except Exception:
        # Other errors (invalid path, permission errors, etc.)
        return False
