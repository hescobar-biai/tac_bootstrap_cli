# Chore: Create TTS Utilities Directory Structure in Templates

## Metadata
issue_number: `253`
adw_id: `chore_Tac_9_task_12`

## Chore Description
Create the `hooks/utils/tts/` directory in the templates with a Jinja2-templated `__init__.py.j2` file. This establishes a foundational directory structure for future text-to-speech utility implementations, following the pattern established by the existing `hooks/utils/llm/` utilities subdirectory.

The directory should be created as a placeholder with minimal content, ready to receive TTS implementations in future tasks.

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/__init__.py.j2` - Parent utilities package init file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/llm/__init__.py.j2` - Reference implementation pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/constants.py.j2` - Utilities constants file

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/__init__.py.j2` (CREATE)

## Step by Step Tasks

### Task 1: Verify parent directory structure
- Confirm that `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/` exists
- Verify the structure matches expected template layout with `__init__.py.j2` and `constants.py.j2`

### Task 2: Create TTS utilities directory
- Create the directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/utils/tts/`

### Task 3: Create `__init__.py.j2` file in TTS directory
- Create a minimal Jinja2-templated `__init__.py.j2` file following the pattern from `hooks/utils/llm/__init__.py.j2`
- Include docstring with project name placeholder: `{{ config.project.name }}`
- Provide brief documentation about TTS utilities purpose
- Include `__all__ = []` as placeholder for future exports

### Task 4: Validate directory structure
- Verify the `tts/` directory exists with `__init__.py.j2` file
- Confirm file is readable and has correct Jinja2 syntax

### Task 5: Run validation commands
- Execute tests to ensure no regressions
- Run linting checks on new file
- Verify project structure integrity

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- This is a foundational task that creates placeholder structure for future TTS implementations
- The `__init__.py.j2` file follows the Jinja2 template pattern used throughout the project
- No additional utility files are needed at this stage; implementations will be added in future tasks
- The structure mirrors the existing `hooks/utils/llm/` directory organization
- Parent directory `hooks/utils/` already exists and is fully functional
