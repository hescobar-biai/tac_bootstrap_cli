# Feature: Add elevenlabs_tts.py.j2 TTS wrapper template

## Metadata
issue_number: `254`
adw_id: `feature_Tac_9_task_13`
issue_json: `{"number":254,"title":"Add elevenlabs_tts.py.j2 TTS wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_13\n\n**Description:**\nCreate Jinja2 template for ElevenLabs TTS wrapper using Turbo v2.5 model.\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/elevenlabs_tts.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/elevenlabs_tts.py` (CREATE - rendered)"}`

## Feature Description

Create a Jinja2 template for an ElevenLabs TTS (Text-to-Speech) wrapper that follows the established uv run script pattern from LLM utilities. The template will generate a production-ready Python script that uses ElevenLabs' Turbo v2.5 model for fast, high-quality voice synthesis.

The implementation follows architectural patterns established by other LLM wrappers (openai/ollama) while adapting them appropriately for TTS semantics. It includes configurable voice selection (default: Rachel), MP3 audio format output, simple error handling, and both bytes-return and file-saving capabilities.

## User Story

As a **TAC Bootstrap user**
I want to **have a template that generates ElevenLabs TTS wrapper scripts**
So that **I can easily add text-to-speech capabilities to generated projects with minimal configuration**

## Problem Statement

Currently, the TTS utilities directory exists but lacks an ElevenLabs wrapper template. Users need a configurable, production-ready TTS wrapper that:
- Follows the established pattern of LLM utilities (dotenv, API key validation, main() CLI)
- Returns audio bytes for flexibility
- Supports file saving for convenience
- Includes optional voice control parameters
- Fails immediately with clear semantics on errors
- Uses sensible defaults (Rachel voice, MP3 format, Turbo v2.5 model)

## Solution Statement

Create `elevenlabs_tts.py.j2` template that mirrors LLM wrapper architecture but adapted for TTS:
- Main function: `synthesize_speech(text)` returns bytes (parallel to `prompt_llm()` returning string)
- Helper function: `synthesize_speech_to_file(text, filepath)` for convenience
- Module-level constants: `VOICE` (configurable default), `FORMAT` (MP3), `MODEL_ID` (eleven_turbo_v2_5)
- API key validation: Check ELEVENLABS_API_KEY before making API calls
- Error handling: Return None on any exception (consistent with LLM patterns)
- Optional kwargs: stability_level and similarity_boost as call-level parameters
- CLI interface: Test functionality via main() with argument parsing
- Dependencies: elevenlabs, python-dotenv

## Relevant Files

### Existing LLM Template Patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - OpenAI wrapper pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/ollama.py.j2` - Ollama wrapper pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2` - LLM utilities init

### Existing TTS Structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - TTS utilities init (already created)
- `.claude/hooks/utils/tts/elevenlabs_tts.py` - Will be rendered template output

### Source Reference
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/elevenlabs_tts.py` - Source implementation to adapt

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` - CREATE (Jinja2 template)
- `.claude/hooks/utils/tts/elevenlabs_tts.py` - CREATE (rendered output from template)

## Implementation Plan

### Phase 1: Template Foundation
- Read source ElevenLabs implementation
- Study LLM wrapper patterns (oai.py.j2 and ollama.py.j2)
- Understand Jinja2 variable usage (`{{ config.project.name }}`)
- Design template structure adapted for TTS

### Phase 2: Core Template Creation
- Create `elevenlabs_tts.py.j2` with:
  - uv run --script shebang and metadata
  - Module-level constants (VOICE, FORMAT, MODEL_ID)
  - Main function: `synthesize_speech(text, stability_level=0.5, similarity_boost=0.75)`
  - Helper function: `synthesize_speech_to_file(text, filepath, ...)`
  - API key validation and error handling
  - CLI interface in main()

### Phase 3: Integration
- Ensure template integrates with existing TTS utils structure
- Update `__init__.py.j2` if needed to export functions
- Test that template renders correctly with valid config
- Verify rendered output follows the source implementation pattern

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Read and Analyze Source Implementation
- Read `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/elevenlabs_tts.py` (source)
- Identify core components:
  - Dependency declarations in shebang
  - Environment variable handling
  - API client initialization with error handling
  - Text-to-speech conversion with ElevenLabs SDK
  - Voice ID and model configuration
  - Play/return audio capability
  - CLI interface

### Task 2: Study LLM Template Patterns
- Read `oai.py.j2` to understand:
  - Shebang format and comment-based metadata
  - Jinja2 variable usage (config context)
  - API key validation pattern
  - Error handling (return None on exception)
  - Main() CLI interface structure
- Read `ollama.py.j2` to understand:
  - Module-level constants (MODEL = "llama3.2")
  - How constants are used throughout
  - Different error handling for local vs remote

### Task 3: Design Template Structure
- Map source concepts to template patterns:
  - Source main() → synthesize_speech() + main()
  - Source error handling → return None pattern
  - Source voice_id parameter → VOICE constant
  - Source model_id → MODEL_ID constant
  - Source output_format → FORMAT constant
- Design function signatures:
  - `synthesize_speech(text, stability_level=0.5, similarity_boost=0.75)` → bytes or None
  - `synthesize_speech_to_file(text, filepath, stability_level=0.5, similarity_boost=0.75)` → bool
  - `main()` → CLI test interface
- Note: TTS returns bytes unlike LLM's string return

### Task 4: Create elevenlabs_tts.py.j2 Template
- Create file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2`
- Structure:
  1. Shebang and metadata (uv run --script)
  2. Dependencies comment block
  3. Imports (os, sys, pathlib, dotenv)
  4. Module constants:
     - `VOICE = "Rachel"` (configurable default)
     - `FORMAT = "mp3_44100_128"` (MP3 format)
     - `MODEL_ID = "eleven_turbo_v2_5"` (Turbo v2.5)
  5. `synthesize_speech(text, stability_level=0.5, similarity_boost=0.75)` function:
     - Load dotenv
     - Check ELEVENLABS_API_KEY
     - Initialize ElevenLabs client
     - Call text_to_speech.convert() with parameters
     - Return audio bytes
     - Catch exceptions → return None
  6. `synthesize_speech_to_file(text, filepath, ...)` helper:
     - Call synthesize_speech()
     - Write to file if successful
     - Return True/False
  7. `main()` function:
     - Parse command-line arguments
     - Test with example text or provided text
     - Support `--file` flag to save to file
     - Error messages with clear guidance
  8. `if __name__ == "__main__"`: Call main()
- Use Jinja2 variables: `{{ config.project.name }}` in docstrings

### Task 5: Verify Template Syntax and Content
- Ensure Jinja2 syntax is valid
- Verify all imports match elevenlabs SDK API
- Check error handling matches LLM patterns
- Confirm docstrings explain functionality
- Validate that dependencies are listed in comment block

### Task 6: Validate with Rendered Output
- Verify the template will render correctly with config context
- Check that `{{ config.project.name }}` placeholders are appropriate
- Ensure no syntax errors in generated Python code

### Task 7: Run Validation Commands
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run tests
- `cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/claude/hooks/utils/tts/` - Lint templates
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/templates/` - Type check
- Verify no regressions in existing TTS/LLM template tests

## Testing Strategy

### Unit Tests
- Test template renders without Jinja2 errors
- Test rendered script syntax is valid Python
- Test synthesize_speech() with mock ElevenLabs client
- Test error handling (missing API key, API failures)
- Test synthesize_speech_to_file() helper function
- Test main() CLI with various arguments

### Edge Cases
- Missing ELEVENLABS_API_KEY environment variable
- Empty text input
- Invalid file path for saving
- API rate limiting (should return None)
- ElevenLabs SDK not installed (ImportError)
- Network failures (should return None)
- Invalid stability_level or similarity_boost values

## Acceptance Criteria

1. ✅ Template file created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2`
2. ✅ Template follows established LLM wrapper pattern (uv run script, error handling, main() CLI)
3. ✅ Template includes configurable VOICE constant (default: Rachel)
4. ✅ Template includes FORMAT constant (MP3 format)
5. ✅ Template uses MODEL_ID: eleven_turbo_v2_5
6. ✅ Main function `synthesize_speech(text, stability_level=0.5, similarity_boost=0.75)` returns bytes or None
7. ✅ Helper function `synthesize_speech_to_file(text, filepath, ...)` provided
8. ✅ API key validation before making calls (returns None if missing)
9. ✅ Error handling catches all exceptions and returns None
10. ✅ Dependencies listed in comment block: elevenlabs, python-dotenv
11. ✅ Template uses Jinja2 variable {{ config.project.name }} in appropriate places
12. ✅ main() function provides CLI interface for testing
13. ✅ Rendered template renders correctly without Jinja2 errors
14. ✅ All existing tests pass (zero regressions)
15. ✅ Template follows project code style (ruff, mypy)

## Validation Commands
Validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check tac_bootstrap/templates/
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/templates/
```

## Notes

### Key Decisions
1. **Bytes return vs file saving**: Primary function returns bytes for flexibility. Helper function provided for file saving convenience. Mirrors LLM pattern (string return with helper for specialized use).
2. **Configurable defaults**: VOICE, FORMAT, MODEL_ID as module constants allow one-line changes without code modification. Follows MODEL pattern in ollama.py.j2.
3. **Optional parameters at call level**: stability_level and similarity_boost as kwargs in synthesize_speech(), not module constants. These are call-specific concerns, not module configuration.
4. **Error handling**: Return None on any exception (consistent with oai.py and ollama.py). No cascading fallbacks to other TTS providers. Keep single-purpose and simple.
5. **ElevenLabs API**: Uses voice_id from constant, not from SDK's pre-defined Voice enum, for simplicity and maintainability.

### Adaptation from Source
- Source uses `elevenlabs.play()` for playback; template returns bytes for flexibility
- Source uses sys.exit(1) on errors; template returns None (LLM pattern)
- Source has hardcoded voice_id (WejK3H1m7MI9CHnIjW9K); template uses VOICE constant for configurability
- Source shows example messages; template keeps pure implementation (messages only in main())

### Future Considerations
- Could add support for other models (standard, multilingual) via MODEL_ID parameter
- Could add other voice options (openai_tts.py already exists as separate template)
- Could add audio streaming for long texts (future optimization)
- Consider webhook integration with ADW triggers (separate feature)

### Dependencies
- elevenlabs: Latest version supporting Turbo v2.5
- python-dotenv: For environment variable loading
- No new dependencies needed (elevenlabs is third-party package)
