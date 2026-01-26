# Chore: Add __init__.py.j2 for TTS utilities package

## Metadata
issue_number: `257`
adw_id: `chore_Tac_9_task_16`
issue_json: `{"number":257,"title":"Add __init__.py.j2 for TTS utilities package","body":"chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_9_task_16\n\n**Description:**\nCreate package init file for TTS utilities with exports.\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` (CREATE)\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/hooks/utils/tts/__init__.py` (CREATE - rendered)"}`

## Chore Description
Update the existing `__init__.py.j2` template file to properly export all three TTS engine implementations (pyttsx3, openai, elevenlabs) with an explicit `__all__` list. The current template only exports elevenlabs functions, but needs to export the complete public API from all three TTS modules.

The template already exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` but only exports `elevenlabs_tts` functions. It needs to be updated to include exports from `pyttsx3_tts` and `openai_tts` modules as well.

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` - **PRIMARY FILE TO UPDATE** - Current template only exports elevenlabs functions, needs to export all TTS implementations
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/pyttsx3_tts.py.j2` - Pyttsx3 TTS implementation template (recently added)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/openai_tts.py.j2` - OpenAI TTS implementation template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/elevenlabs_tts.py.j2` - ElevenLabs TTS implementation template
- `.claude/hooks/utils/tts/__init__.py` - Rendered version to be updated as reference

### New Files
None - this is an update to existing template file.

## Step by Step Tasks

### Task 1: Read existing TTS module templates
- Read `pyttsx3_tts.py.j2` to identify exported functions/classes
- Read `openai_tts.py.j2` to identify exported functions/classes
- Read `elevenlabs_tts.py.j2` to verify exported functions/classes
- Document the public API for each module

### Task 2: Update __init__.py.j2 template
- Update the template to import from all three TTS modules
- Add explicit `__all__` list with all exported symbols
- Keep the Jinja2 variable `{{ config.project.name }}` in the docstring
- Ensure no version metadata or initialization side effects
- Follow Python package conventions with clean, minimal exports

### Task 3: Verify template structure
- Ensure the template uses only `{{ config.project.name }}` variable
- Verify no conditional logic is present (unconditional imports only)
- Check that docstring clearly describes the unified TTS interface
- Confirm `__all__` list is explicit and complete

### Task 4: Validate implementation
Execute validation commands to ensure no regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Auto-Resolved Clarifications Applied
1. **Exports**: Use explicit `__all__` list with from imports for clear public API
2. **No version metadata**: This is a utility package, not standalone library
3. **No initialization side effects**: Keep imports pure and side-effect-free
4. **No conditional logic**: Unconditional imports, users choose backends at runtime
5. **Discovered modules**: Three TTS implementations exist: pyttsx3, openai, elevenlabs

### Current State
- Template file already exists but is incomplete (only exports elevenlabs functions)
- Three TTS module templates are present in the directory
- Recent commit history shows pyttsx3 template was just added
- This chore completes the package structure by exposing all implementations

### Expected Outcome
After completion, the `__init__.py.j2` template will provide a clean, explicit public API that exports all TTS implementations, allowing users to import any TTS engine from the package root:

```python
from utils.tts import synthesize_speech, save_audio_file  # elevenlabs
from utils.tts import speak_text  # pyttsx3
from utils.tts import generate_speech  # openai
```
