# Feature: Add OpenAI TTS Wrapper Template

## Metadata
issue_number: `255`
adw_id: `feature_Tac_9_task_14`
issue_json: `{"number":255,"title":"Add openai_tts.py.j2 TTS wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_14\n\n**Description:**\nCreate Jinja2 template for OpenAI TTS wrapper supporting tts-1 and tts-1-hd models.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/openai_tts.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/openai_tts.py` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for an OpenAI TTS (Text-to-Speech) wrapper that mirrors the existing ElevenLabs TTS pattern. The template will provide a simple, consistent interface for synthesizing speech using OpenAI's TTS API, supporting both tts-1 (standard) and tts-1-hd (high definition) models. The wrapper will use OpenAI's six standard voices (alloy, echo, fable, onyx, nova, shimmer) and output MP3 audio files.

This template will be part of TAC Bootstrap's utility templates, allowing generated projects to easily integrate OpenAI TTS capabilities with minimal configuration.

## User Story
As a developer using TAC Bootstrap
I want to have an OpenAI TTS wrapper template
So that I can easily integrate OpenAI's text-to-speech capabilities into my generated projects with a simple, consistent API that matches the ElevenLabs pattern

## Problem Statement
Currently, TAC Bootstrap includes an ElevenLabs TTS template but lacks support for OpenAI's TTS service. OpenAI's TTS API is a popular, cost-effective alternative that many developers prefer. Without a template, users must manually implement OpenAI TTS integration, leading to inconsistent patterns and potential errors.

The existing ElevenLabs template establishes a clear pattern for TTS wrappers, but we need an equivalent template for OpenAI to give users flexibility in choosing their TTS provider.

## Solution Statement
Create a Jinja2 template `openai_tts.py.j2` that follows the same structure and conventions as the existing `elevenlabs_tts.py.j2` template. The template will:

1. Use the `openai` Python SDK for API communication
2. Provide two main functions: `synthesize_speech()` and `save_audio_file()`
3. Support all six OpenAI standard voices using voice names (not IDs)
4. Default to the `tts-1` model with optional `tts-1-hd` support via parameter
5. Include a `speed` parameter (default 1.0) for playback speed control
6. Output MP3 format audio (hardcoded for simplicity)
7. Use the standard `OPENAI_API_KEY` environment variable
8. Return `None`/`False` on errors (simple error handling)
9. Use non-streaming mode (collect full audio bytes)
10. Include proper docstrings and type hints

## Relevant Files
Files needed for implementing this feature:

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` - Reference pattern to follow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` - NEW template to create
- `.claude/hooks/utils/tts/openai_tts.py` - NEW rendered file for testing

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` - OpenAI TTS wrapper template
- `.claude/hooks/utils/tts/openai_tts.py` - Rendered version for local testing

## Implementation Plan

### Phase 1: Foundation
1. Examine the ElevenLabs TTS template structure to understand the pattern
2. Research OpenAI TTS API parameters and voice options
3. Define the template structure matching ElevenLabs conventions

### Phase 2: Core Implementation
1. Create the Jinja2 template with proper shebang and script dependencies
2. Implement `synthesize_speech()` function with OpenAI API integration
3. Implement `save_audio_file()` function for file operations
4. Add proper error handling and type hints

### Phase 3: Integration
1. Render the template locally for testing
2. Test with actual OpenAI API calls (if API key available)
3. Verify the template follows project conventions

## Step by Step Tasks

### Task 1: Create OpenAI TTS Template File
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2`
- Add shebang: `#!/usr/bin/env -S uv run --script`
- Add PEP 723 script block with dependencies: `openai`, `python-dotenv`
- Add imports: `os`, `pathlib.Path`, `dotenv.load_dotenv`

### Task 2: Implement synthesize_speech Function
- Create function signature: `def synthesize_speech(text: str, voice: str = "alloy", model: str = "tts-1", speed: float = 1.0) -> bytes | None:`
- Add docstring describing parameters and return value
- Load environment variables using `load_dotenv()`
- Get API key from `OPENAI_API_KEY` environment variable
- Return `None` if no API key
- Use try/except block for error handling
- Import and initialize OpenAI client
- Call `client.audio.speech.create()` with parameters: text, voice, model, speed
- Set response format to `mp3`
- Collect audio bytes from response
- Return audio bytes or `None` on error

### Task 3: Implement save_audio_file Function
- Create function signature: `def save_audio_file(text: str, file_path: str, voice: str = "alloy", model: str = "tts-1", speed: float = 1.0) -> bool:`
- Add docstring describing parameters and return value
- Use try/except block for error handling
- Call `synthesize_speech()` with provided parameters
- Return `False` if `audio_bytes` is `None`
- Ensure parent directory exists using `Path(file_path).parent.mkdir(parents=True, exist_ok=True)`
- Write audio bytes to file in binary mode
- Return `True` on success, `False` on error

### Task 4: Render Template Locally for Testing
- Create `.claude/hooks/utils/tts/` directory if it doesn't exist
- Manually render the template without Jinja2 variables (use literal project name for testing)
- Save as `.claude/hooks/utils/tts/openai_tts.py`
- Verify the file is valid Python and follows the same pattern as `elevenlabs_tts.py`

### Task 5: Validation and Testing
- Run all validation commands to ensure zero regressions
- Verify template syntax is valid Jinja2
- Verify rendered file is valid Python
- Check that the template follows project conventions (type hints, docstrings, error handling)
- Confirm template matches ElevenLabs pattern structure

## Testing Strategy

### Unit Tests
Manual testing of the template:
1. Verify Jinja2 template syntax is valid
2. Verify rendered Python file has correct syntax
3. Verify all functions have proper type hints
4. Verify docstrings are complete and accurate
5. If OPENAI_API_KEY available, test actual API calls with `synthesize_speech()`
6. If OPENAI_API_KEY available, test `save_audio_file()` creates valid MP3 files

### Edge Cases
1. Missing API key - should return `None`/`False`
2. Invalid voice name - let OpenAI API return error, return `None`/`False`
3. Invalid model - let OpenAI API return error, return `None`/`False`
4. Network errors - should return `None`/`False`
5. File system errors (permissions) - should return `False`
6. Empty text input - let OpenAI API handle, return `None`/`False`
7. Text exceeding OpenAI's 4096 character limit - let API handle, return `None`/`False`

## Acceptance Criteria
1. ✅ Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2`
2. ✅ Template follows same structure as `elevenlabs_tts.py.j2`
3. ✅ Includes PEP 723 script block with `openai` and `python-dotenv` dependencies
4. ✅ `synthesize_speech()` function accepts: text, voice (default "alloy"), model (default "tts-1"), speed (default 1.0)
5. ✅ `synthesize_speech()` returns `bytes | None` with proper error handling
6. ✅ `save_audio_file()` function accepts: text, file_path, voice, model, speed
7. ✅ `save_audio_file()` returns `bool` (True on success, False on error)
8. ✅ Uses `OPENAI_API_KEY` environment variable (not templated)
9. ✅ Outputs MP3 format (hardcoded)
10. ✅ Non-streaming implementation (collects full bytes)
11. ✅ All functions have proper docstrings and type hints
12. ✅ Template uses Jinja2 variable `{{ config.project.name }}` in docstrings
13. ✅ Rendered file `.claude/hooks/utils/tts/openai_tts.py` is valid Python
14. ✅ All validation commands pass with zero regressions

## Validation Commands
Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test
- `python .claude/hooks/utils/tts/openai_tts.py` - Verify rendered file is valid Python

## Notes

### OpenAI TTS API Details
- Six standard voices: alloy, echo, fable, onyx, nova, shimmer
- Two models: tts-1 (standard, faster, cheaper), tts-1-hd (high definition)
- Speed range: 0.25 to 4.0 (default 1.0)
- Formats: mp3, opus, aac, flac (we use mp3)
- Text limit: 4096 characters
- Pricing: $0.015 per 1K characters (tts-1), $0.030 per 1K characters (tts-1-hd)

### Design Decisions
1. **Voice parameter**: Use voice names (not IDs) matching OpenAI's design
2. **Model parameter**: Default to tts-1 (faster/cheaper), allow override
3. **Speed parameter**: Useful feature that doesn't add complexity
4. **Format**: Hardcode MP3 for simplicity (matches ElevenLabs pattern)
5. **Streaming**: Non-streaming only for consistency with ElevenLabs pattern
6. **Error handling**: Simple None/False returns, let API handle validation
7. **Environment variable**: Use standard OPENAI_API_KEY (not templated)

### Future Enhancements
- Could add streaming support if needed
- Could make format configurable
- Could add response_format parameter for different formats
- Could add explicit text length validation
- Could add voice preview/selection helper
