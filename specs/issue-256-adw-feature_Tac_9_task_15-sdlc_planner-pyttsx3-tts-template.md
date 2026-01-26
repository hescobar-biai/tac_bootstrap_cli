# Feature: Add pyttsx3_tts.py.j2 local TTS wrapper template

## Metadata
issue_number: `256`
adw_id: `feature_Tac_9_task_15`
issue_json: `{"number":256,"title":"Add pyttsx3_tts.py.j2 local TTS wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_15\n\n**Description:**\nCreate Jinja2 template for pyttsx3 local TTS wrapper (offline fallback).\n\n**Source:** `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/pyttsx3_tts.py`\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/pyttsx3_tts.py` (CREATE - rendered)"}`

## Feature Description
Create a Jinja2 template for a pyttsx3-based local text-to-speech wrapper that provides an offline TTS fallback option. This template will enable TAC Bootstrap CLI to generate local TTS functionality for projects that need offline speech synthesis capabilities, complementing existing cloud-based TTS options (OpenAI, ElevenLabs).

The template will produce a Python script that wraps the pyttsx3 library with configurable voice properties (rate, volume, voice selection), robust error handling for engine initialization failures, and support for both real-time playback and file saving.

## User Story
As a TAC Bootstrap CLI user
I want to generate a local TTS wrapper using pyttsx3
So that my project can have offline text-to-speech capabilities without requiring API keys or internet connectivity

## Problem Statement
Currently, TAC Bootstrap CLI provides templates for cloud-based TTS services (OpenAI TTS, ElevenLabs), but lacks an offline fallback option. Users need a local TTS solution that:
- Works without internet connectivity or API keys
- Provides cross-platform compatibility (macOS, Windows, Linux)
- Offers a consistent API interface with other TTS providers
- Handles system TTS engine dependencies gracefully
- Supports common voice customization options

## Solution Statement
Create a Jinja2 template (`pyttsx3_tts.py.j2`) that generates a Python script wrapping the pyttsx3 library. The template will:
- Use the same API interface as `openai_tts.py` template for drop-in compatibility
- Support configurable Jinja2 variables for voice properties with sensible defaults
- Include robust error handling for missing dependencies and engine initialization failures
- Provide both real-time playback (`speak()`) and file saving (`save_to_file()`) methods
- Follow the UV script format with inline dependency declarations
- Namespace configuration under `config.tts.pyttsx3` to distinguish from other TTS providers

## Relevant Files
Files necessary for implementing the feature:

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` - Reference for API interface and template structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` - Reference for template patterns
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - Package initialization
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/pyttsx3_tts.py` - Source reference implementation

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2` - Primary template to create
- `.claude/hooks/utils/tts/pyttsx3_tts.py` - Rendered example for this repository

## Implementation Plan

### Phase 1: Foundation
1. Study the source reference implementation at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/pyttsx3_tts.py`
2. Analyze existing TTS templates (`openai_tts.py.j2`, `elevenlabs_tts.py.j2`) to understand:
   - UV script format with inline dependencies
   - Function signature patterns
   - Error handling approaches
   - Jinja2 variable usage patterns
3. Review auto-resolved clarifications to understand requirements for:
   - Configurable properties (rate, volume, voice_index)
   - API interface consistency
   - Error handling strategies
   - File saving capabilities

### Phase 2: Core Implementation
1. Create the Jinja2 template file with:
   - UV script header with pyttsx3 dependency
   - Jinja2 variables for configuration with defaults:
     - `{{ config.tts.pyttsx3.rate | default(150) }}`
     - `{{ config.tts.pyttsx3.volume | default(0.9) }}`
     - `{{ config.tts.pyttsx3.voice_index | default(0) }}`
   - Project name interpolation: `{{ config.project.name }}`
2. Implement core functions:
   - `synthesize_speech(text: str) -> bool` - Real-time playback with error handling
   - `save_to_file(text: str, file_path: str) -> bool` - Save audio to file
3. Add robust error handling:
   - Try-except for pyttsx3 import with clear ImportError message
   - Try-except for engine initialization with system dependency guidance
   - Proper exception handling in both synthesis functions
4. Include documentation:
   - Module docstring explaining offline TTS usage
   - Function docstrings with parameters and return types
   - Usage examples in comments

### Phase 3: Integration
1. Render the template for this repository's own `.claude/hooks/utils/tts/pyttsx3_tts.py`
2. Verify the rendered file:
   - Has correct UV script headers
   - Contains valid Python syntax
   - Uses appropriate default values
   - Includes all error handling
3. Update package `__init__.py.j2` if needed to include pyttsx3 wrapper
4. Test template rendering with various configuration scenarios

## Step by Step Tasks

### Task 1: Analyze existing templates and source
- Read source file at `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/pyttsx3_tts.py`
- Study `openai_tts.py.j2` template structure
- Identify patterns for UV script format, error handling, and Jinja2 variables
- Document API interface requirements for consistency

### Task 2: Create pyttsx3_tts.py.j2 template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2`
- Add UV script header with pyttsx3 dependency
- Implement Jinja2 variables with defaults for rate, volume, voice_index
- Add project name interpolation in docstrings

### Task 3: Implement core TTS functions
- Create `synthesize_speech(text: str) -> bool` function
  - Initialize pyttsx3 engine with error handling
  - Configure voice properties from template variables
  - Implement real-time speech playback
  - Return success/failure boolean
- Create `save_to_file(text: str, file_path: str) -> bool` function
  - Use pyttsx3's `save_to_file()` method
  - Ensure parent directory creation
  - Return success/failure boolean

### Task 4: Add robust error handling
- Wrap pyttsx3 import in try-except with ImportError guidance
- Wrap engine initialization in try-except with clear error messages for:
  - macOS: nsss engine not available
  - Windows: sapi5 engine not available
  - Linux: espeak not installed
- Add exception handling in both synthesis functions

### Task 5: Add documentation and comments
- Write comprehensive module docstring
- Document each function with:
  - Purpose and usage
  - Parameters with types
  - Return values with types
  - Example usage
- Add inline comments for complex logic

### Task 6: Render template for this repository
- Use template to generate `.claude/hooks/utils/tts/pyttsx3_tts.py`
- Verify rendered output has:
  - Valid Python syntax
  - Correct default values
  - All error handling intact
  - Proper UV script format

### Task 7: Validation
Execute validation commands:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify rendered file: `python .claude/hooks/utils/tts/pyttsx3_tts.py "Test message"`

## Testing Strategy

### Unit Tests
- Template rendering test:
  - Verify template renders with default config
  - Verify template renders with custom config values
  - Verify all Jinja2 variables are replaced correctly
- Rendered file validation:
  - Verify UV script format is valid
  - Verify Python syntax is correct
  - Verify imports are present

### Edge Cases
- Missing pyttsx3 dependency - should fail with clear error message
- Engine initialization failure - should provide system-specific guidance
- Invalid voice_index - should handle gracefully or use default
- Invalid file path for save_to_file - should fail gracefully
- Empty text input - should handle appropriately
- Missing config values - should use defaults

### Manual Testing
- Test rendered script on macOS with default voice
- Test with custom rate/volume/voice_index values
- Test both `synthesize_speech()` and `save_to_file()` functions
- Verify audio output quality and parameters

## Acceptance Criteria
1. Template file `pyttsx3_tts.py.j2` exists in correct location
2. Template includes UV script header with pyttsx3 dependency
3. Template supports Jinja2 variables: `config.tts.pyttsx3.rate`, `config.tts.pyttsx3.volume`, `config.tts.pyttsx3.voice_index` with defaults
4. Template includes project name interpolation
5. Implements `synthesize_speech(text: str) -> bool` function
6. Implements `save_to_file(text: str, file_path: str) -> bool` function
7. Includes robust error handling for ImportError and engine initialization
8. Rendered file `.claude/hooks/utils/tts/pyttsx3_tts.py` is created and functional
9. All validation commands pass with zero regressions
10. Template follows same API interface as `openai_tts.py.j2` for consistency
11. Documentation is clear and comprehensive

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# Test rendered file (if pyttsx3 is available)
python .claude/hooks/utils/tts/pyttsx3_tts.py "Test message"
```

## Notes
- pyttsx3 is a cross-platform TTS library that uses system TTS engines:
  - macOS: NSSpeechSynthesizer (nsss)
  - Windows: Speech API (sapi5)
  - Linux: espeak
- Users must have the appropriate system TTS engine installed
- The template provides an offline fallback to cloud TTS services
- Consider documenting system prerequisites in generated comments
- Future enhancement: Could add voice listing functionality to help users discover available voices
- The template uses UV's inline script format for automatic dependency management
- No version pinning for pyttsx3 - relies on project's dependency management
