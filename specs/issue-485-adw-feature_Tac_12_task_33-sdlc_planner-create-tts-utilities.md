# Feature: Create TTS Utilities Subdirectory

## Metadata
issue_number: `485`
adw_id: `feature_Tac_12_task_33`
issue_json: `{"number": 485, "title": "[Task 33/49] [FEATURE] Create tts/ utilities subdirectory", "body": "## Description\n\nCreate text-to-speech utilities for hooks.\n\n## Files\n- **Base Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/`\n- **Template Directory:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/`\n\n## Key Features\n- TTS integration\n- Audio notification support\n- (Read TAC-12 contents for specifics)\n\n## Changes Required\n- Create directory and utility files in base repository\n- Create Jinja2 templates for CLI generation\n- Update `scaffold_service.py` to include directory creation and files\n\n## Reference\n`/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/tts/`\n\n## Wave 4 - Hook Utilities (Task 33 of 5)\n\n## Workflow Metadata\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_12_task_33"}`

## Feature Description

Task 33 creates a complete text-to-speech (TTS) utilities subdirectory to provide composable, minimal TTS provider integrations for use in hooks. This feature provides building blocks for audio-based notifications and TTS synthesis capabilities without cross-cutting concerns like validation, logging, or caching.

The TTS utilities follow the same patterns established by the LLM utilities (Task 32), creating a modular hierarchy where each provider is a separate module with consistent function signatures.

## User Story

As a hook developer
I want access to TTS synthesis utilities with multiple provider options
So that I can add audio output and notification capabilities to my automation workflows

## Problem Statement

Currently, there are no text-to-speech utilities available for hooks. Developers need a consistent interface to text-to-speech providers (ElevenLabs, OpenAI, pyttsx3) without having to manage provider-specific details, error handling, or API integration code.

## Solution Statement

Create a modular TTS utilities package under `.claude/hooks/utils/tts/` with:
1. **Provider modules** (elevenlabs_tts, openai_tts, pyttsx3_tts) - each provides `synthesize_speech()` and `save_audio_file()` functions
2. **Package initialization** - re-exports with aliased imports for convenient access
3. **Templates** - Jinja2 templates in the CLI for generating these utilities in new projects
4. **Scaffold integration** - Updated `scaffold_service.py` to include TTS utilities in project generation

Each provider maintains minimal responsibility:
- Returns None/False on error (no exceptions)
- No validation, logging, or caching at utility level
- Lenient failure allowing consumers to decide error handling strategy
- Provider-specific format documentation (ElevenLabs/OpenAI output MP3, pyttsx3 outputs WAV)

## Relevant Files

### Existing Base Implementations
- `.claude/hooks/utils/tts/__init__.py` - Package initialization with re-exports
- `.claude/hooks/utils/tts/elevenlabs_tts.py` - ElevenLabs Turbo v2.5 integration
- `.claude/hooks/utils/tts/openai_tts.py` - OpenAI TTS API wrapper
- `.claude/hooks/utils/tts/pyttsx3_tts.py` - Offline pyttsx3 local TTS engine

### Templates to Create/Verify
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2`

### Scaffold Integration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Lines 404-416 (already contains TTS entries in `tts_utils` list)

### Reference Implementation
- `/Volumes/MAc1/Celes/TAC/tac-12/.claude/hooks/utils/tts/` - TAC-12 reference implementations

### New Files
No new files are needed - all base implementations already exist.

## Implementation Plan

### Phase 1: Verify Existing Base Implementations
- Confirm all base TTS files exist in `.claude/hooks/utils/tts/`
- Review each provider implementation against TAC-12 specifications
- Verify function signatures and error handling patterns

### Phase 2: Verify Templates
- Confirm all `.j2` templates exist in `tac_bootstrap_cli/templates/`
- Validate template structure matches base implementations
- Verify Jinja2 variable usage (`{{ config.project.name }}`)

### Phase 3: Verify Scaffold Integration
- Confirm directory creation in `scaffold_service.py` lines 115-117
- Confirm file creation in `scaffold_service.py` lines 403-416
- Validate all TTS files are referenced in scaffold

### Phase 4: Validation
- Run full test suite to ensure no regressions
- Verify scaffold can generate projects with TTS utilities
- Test that templates render correctly

## Step by Step Tasks

### Task 1: Verify Base Implementations Exist
- Check `.claude/hooks/utils/tts/__init__.py` exists with proper package structure
- Check `elevenlabs_tts.py` exists with `synthesize_speech()` and `save_audio_file()` functions
- Check `openai_tts.py` exists with provider-specific implementation
- Check `pyttsx3_tts.py` exists with offline local TTS capability
- Validate all files use lenient error handling (return None/False)

### Task 2: Verify Templates Exist
- Check all `.j2` files exist in `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/`
- Verify template structure mirrors base implementations
- Check `{{ config.project.name }}` placeholder usage in __init__.py.j2 and docstrings
- Confirm UV script metadata format in provider templates

### Task 3: Verify Scaffold Service Integration
- Check `.claude/hooks/utils/tts` directory is added to `scaffold_service.py` line 117
- Confirm `tts_utils` list at lines 404-408 includes all four files
- Verify file creation loop at lines 410-416 properly iterates
- Check that `FileAction.CREATE` is used to avoid overwrites

### Task 4: Run Validation Commands
- Execute `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Execute `cd tac_bootstrap_cli && uv run ruff check .`
- Execute `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Execute `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
- Verify template rendering produces valid Python code
- Verify function signatures are correct
- Verify error handling paths (returning None/False on exception)
- Verify directory creation and file I/O in save_audio_file functions

### Integration Tests
- Verify scaffold_service properly includes TTS directory
- Verify scaffold_service properly includes all TTS provider files
- Verify templates can be rendered with sample config
- Test that generated TTS code has no syntax errors

### Edge Cases
- Verify API key missing/invalid handled gracefully (silent failure)
- Verify audio file creation with non-existent parent directories
- Verify provider-specific limitations documented (voice IDs, language support)
- Verify cross-platform compatibility (pathlib usage for file paths)

## Acceptance Criteria

1. **Base implementations verified**: All four TTS files exist in `.claude/hooks/utils/tts/` with correct implementations
2. **Templates verified**: All four `.j2` templates exist in CLI templates directory with proper structure
3. **Scaffold integration verified**: `scaffold_service.py` includes TTS directory and files in appropriate lists
4. **Documentation complete**: Each provider documents its capabilities, output format, and language/voice support
5. **Validation passing**: All tests pass, no regressions introduced
6. **Error handling correct**: All providers use lenient error handling (return None/False, not exceptions)

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Design Patterns
- **Minimal and Composable**: TTS utilities are thin, focused building blocks with no cross-cutting concerns
- **Lenient Error Handling**: Returning None/False allows consumers to decide error handling strategy
- **Provider Abstraction**: Each provider maintains identical function signatures (synthesize_speech, save_audio_file)
- **Environment Variable Authentication**: API keys loaded from .env via python-dotenv
- **Cross-platform File I/O**: Using pathlib.Path for portable operations

### Provider-Specific Details
- **ElevenLabs**: Uses eleven_turbo_v2_5 model, outputs MP3 format, requires ELEVENLABS_API_KEY
- **OpenAI**: Configurable model (default tts-1), voice (default alloy), outputs MP3
- **pyttsx3**: Offline system TTS, no API key needed, outputs WAV/platform-native format

### Integration Points
- TTS utilities integrate with `.claude/hooks/notification.py` for audio notification support
- Used by hooks that need audio output capabilities
- No client-side validation of text length or voice parameters

### Related Tasks
- Task 32: Create LLM utilities subdirectory (foundational patterns)
- Task 34: Create status_lines directory
- Potential future: Hook consumers that leverage TTS utilities
