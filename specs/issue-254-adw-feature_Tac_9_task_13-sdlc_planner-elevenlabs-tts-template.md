# Feature: Add elevenlabs_tts.py.j2 TTS wrapper template

## Metadata
issue_number: `254`
adw_id: `feature_Tac_9_task_13`
issue_json: `{"number":254,"title":"Add elevenlabs_tts.py.j2 TTS wrapper template","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_9_task_13\n\n**Description:**\nCreate Jinja2 template for ElevenLabs TTS wrapper using Turbo v2.5 model."}`

## Feature Description

Create a Jinja2 template for an ElevenLabs TTS wrapper module that provides a unified interface for text-to-speech synthesis. This template will follow the established pattern from LLM utilities (oai.py) with standalone functions for synthesis and file operations. The template will support the ElevenLabs Turbo v2.5 model with configurable voice selection and environment variable authentication.

## User Story
As a **developer building agentic projects**
I want to **use a standardized ElevenLabs TTS module in generated projects**
So that **I have a consistent interface for text-to-speech synthesis similar to LLM utilities**

## Problem Statement

Currently, TAC Bootstrap lacks a TTS wrapper template for ElevenLabs. Generated projects need access to text-to-speech capabilities with the same level of abstraction and consistency as the existing LLM utilities. The oai.py pattern (standalone functions with environment variable authentication and lenient error handling) should be extended to TTS implementations.

## Solution Statement

Create `elevenlabs_tts.py.j2` as a Jinja2 template in the tac_bootstrap_cli that:
1. Exposes two standalone functions: `synthesize_speech()` (returns bytes) and `save_audio_file()` (handles file I/O)
2. Follows the oai.py pattern for environment variable authentication (ELEVENLABS_API_KEY)
3. Hardcodes the Turbo v2.5 model with configurable voice_id parameter
4. Implements lenient error handling (returns None/False on errors)
5. Includes uv script dependencies declaration
6. Updates tts/__init__.py to export the new functions
7. Renders to .claude/hooks/utils/tts/ as reference implementation

## Relevant Files

### Existing References
- `.claude/hooks/utils/llm/oai.py` - Pattern for standalone LLM functions, error handling, environment variable usage
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/oai.py.j2` - Template structure reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - TTS module init template
- `/Volumes/MAc1/Celes/TAC/tac-9/.claude/utils/tts/elevenlabs_tts.py` - Source implementation reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` (CREATE) - Jinja2 template
- `.claude/hooks/utils/tts/elevenlabs_tts.py` (CREATE) - Rendered reference implementation

### Modified Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - Update to import elevenlabs functions

## Implementation Plan

### Phase 1: Foundation
- Analyze oai.py pattern for function structure, error handling, and environment variable usage
- Review source elevenlabs_tts.py to extract core logic
- Understand TTS module initialization structure
- Plan Jinja2 template structure with config variable usage

### Phase 2: Core Implementation
- Create elevenlabs_tts.py.j2 template with:
  - uv script dependencies declaration
  - synthesize_speech() function with voice_id parameter
  - save_audio_file() wrapper function
  - Environment variable authentication (ELEVENLABS_API_KEY)
  - Lenient error handling matching oai.py pattern
- Update tts/__init__.py.j2 to export functions
- Render template to .claude/hooks/utils/tts/elevenlabs_tts.py

### Phase 3: Integration
- Verify rendered output matches pattern
- Test function signatures and error handling
- Validate __init__.py imports are correct
- Run validation commands

## Step by Step Tasks

### Task 1: Create elevenlabs_tts.py.j2 template
- Create file at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2`
- Include uv script dependencies block with elevenlabs and python-dotenv
- Implement `synthesize_speech(text: str, voice_id: str = 'EXAVITQu4vr4xnSDxMaL') -> bytes | None` function
  - Uses ELEVENLABS_API_KEY environment variable
  - Calls load_dotenv()
  - Uses eleven_turbo_v2_5 model
  - Returns audio bytes on success, None on error
  - Lenient error handling (try/except catching all exceptions)
- Implement `save_audio_file(text: str, file_path: str, voice_id: str = 'EXAVITQu4vr4xnSDxMaL') -> bool` function
  - Calls synthesize_speech() internally
  - Writes bytes to file
  - Returns True on success, False on error
  - Lenient error handling
- Include module docstring with {{ config.project.name }} reference
- Follow oai.py code style and structure exactly

### Task 2: Update tts/__init__.py.j2
- Modify `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2`
- Add import: `from .elevenlabs_tts import synthesize_speech, save_audio_file`
- Add `__all__ = ["synthesize_speech", "save_audio_file"]`
- Keep module docstring intact
- Maintain Jinja2 variable usage for project name

### Task 3: Render template to .claude/
- Create rendered output at `.claude/hooks/utils/tts/elevenlabs_tts.py`
- Replace all Jinja2 variables with actual values (e.g., {{ config.project.name }} -> "tac_bootstrap")
- Ensure file has executable permissions (chmod +x)
- Verify no Jinja2 syntax remains in rendered file
- Run the rendered script with test inputs to verify functionality

### Task 4: Validation
- Run all validation commands with zero failures
- Verify rendered elevenlabs_tts.py has correct shebang and dependencies
- Confirm __init__.py imports work correctly
- Test synthesize_speech() return type expectations
- Test save_audio_file() boolean return values
- Check error handling returns None/False on missing API key

## Testing Strategy

### Unit Tests
- Test synthesize_speech() with valid text input
- Test synthesize_speech() with missing ELEVENLABS_API_KEY (should return None)
- Test synthesize_speech() with different voice_id values
- Test save_audio_file() with valid text input (should return True)
- Test save_audio_file() with invalid file path (should return False)
- Test save_audio_file() with missing ELEVENLABS_API_KEY (should return False)
- Test imports from tts module work correctly

### Edge Cases
- Empty text input
- Very long text input
- Special characters in text
- Invalid file paths
- Missing dependencies (elevenlabs library not installed)
- Corrupted API key format
- Network timeout scenarios

## Acceptance Criteria

1. **Template Creation**: `elevenlabs_tts.py.j2` exists in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/`
2. **Function Signatures**: Both `synthesize_speech()` and `save_audio_file()` have correct signatures matching LLM pattern
3. **Error Handling**: Returns None for synthesis, False for file operations on any exception
4. **Dependencies**: uv script dependencies block includes elevenlabs and python-dotenv
5. **Environment Variable**: Uses ELEVENLABS_API_KEY with load_dotenv() pattern
6. **Voice Configuration**: Supports configurable voice_id with default 'EXAVITQu4vr4xnSDxMaL'
7. **Model**: Hardcodes eleven_turbo_v2_5 model
8. **Module Exports**: tts/__init__.py.j2 correctly imports and exports functions
9. **Rendered Output**: `.claude/hooks/utils/tts/elevenlabs_tts.py` is executable and valid Python
10. **Code Style**: Matches oai.py pattern and project conventions
11. **Jinja2 Rendering**: All {{ config }} variables properly replaced in rendered output
12. **No Regressions**: All validation commands pass with zero failures

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `python3 -m py_compile .claude/hooks/utils/tts/elevenlabs_tts.py` - Verify rendered file syntax
- `grep -c "{{" .claude/hooks/utils/tts/elevenlabs_tts.py` - Ensure no Jinja2 variables in rendered output (should be 0)

## Notes

- **uv Script Dependencies**: The elevenlabs library must be added to the script dependencies block matching the format used in oai.py.j2
- **Voice ID Default**: Using 'EXAVITQu4vr4xnSDxMaL' as sensible default, but projects can override via function parameter
- **Model Hardcoding**: Turbo v2.5 is specified in issue requirements and should not be configurable
- **Lenient Error Handling**: Pattern matches oai.py with bare `except` clause returning None/False
- **Load dotenv Pattern**: Consistent with oai.py, called at function start to support .env files
- **File Permissions**: Rendered .claude/ file should be executable like other utility scripts
- **No CLI Main Function**: Unlike source elevenlabs_tts.py, template doesn't need CLI interface - projects can add if needed
- **Future Expansion**: Structure allows for additional TTS providers (openai_tts.py, etc.) following same pattern
- **Config Variables**: Use {{ config.project.name }} in docstrings for per-project customization, matching LLM template pattern
