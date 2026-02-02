# Chore: Update scaffold_service.py with new TAC-12 files

## Metadata
issue_number: `493`
adw_id: `chore_Tac_12_task_41`
issue_json: `{"number": 493, "title": "[Task 41/49] [CHORE] Update scaffold_service.py with new TAC-12 files", "body": "Update scaffold service to include ALL new TAC-12 files in generation."}`

## Chore Description

Update `scaffold_service.py` to ensure all TAC-12 new files are properly included in the scaffold generation process. This chore is part of Wave 7 (Configuration Updates) and is the 4th task of 4 in this wave.

The scaffold service is responsible for building and applying scaffold plans that generate the complete `.claude/`, `adws/`, and `scripts/` directory structure for new projects. We need to audit the current implementation and verify all TAC-12 files are included.

## Current Status

The scaffold_service.py file already includes:
- `.claude/agents/` directory creation ✓
- `.claude/status_lines/` directory - **MISSING**
- `.claude/data/sessions/` directory creation ✓
- `.claude/data/claude-model-cache/` directory creation ✓
- `.claude/hooks/utils/llm/` directory creation ✓
- `.claude/hooks/utils/tts/` directory creation ✓
- 13 new commands (Tasks 1-13) ✓
- 6 new agents (Tasks 14-19) ✓
- 9 new hooks (Tasks 20-28) ✓
- 5 new hook utilities (Tasks 29-33) ✓
- Status line file - **NEEDS VERIFICATION**
- Data directory .gitkeep files ✓

## Relevant Files

### Primary File
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Main scaffold service that defines directory creation and file generation

### Supporting Files (for context/templates)
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - ScaffoldPlan and FileAction definitions
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template repository
- `.claude/status_lines/` - Status line files in the repo (if exist)
- `adws/adw_modules/data_types.py` - Data types for TAC-12

### Template Files
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/templates/claude/` - Command and hook templates
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/templates/claude/agents/` - Agent templates
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/templates/claude/output-styles/` - Output style templates

## Step by Step Tasks

### Task 1: Analyze Current Status
- Read the full scaffold_service.py to understand current implementation
- Compare against issue requirements for missing directories and files
- Identify what needs to be added vs what's already present
- Document findings for each requirement

### Task 2: Add Missing `.claude/status_lines/` Directory
- Add directory entry to `_add_directories()` method
- Verify proper indentation and formatting
- Add .gitkeep file if necessary for empty directory preservation
- Update reason/comment to describe purpose: "Claude Code status line definitions"

### Task 3: Verify Status Line File Generation
- Check if status line files are being generated in `_add_claude_files()`
- Verify template reference if exists
- Add status line file generation if missing
- Ensure it uses proper action (FileAction.CREATE)

### Task 4: Audit Command Files
- Verify all 13 TAC-12 commands are in the commands list (Tasks 1-13)
- Check command templates exist in infrastructure/templates
- Verify file paths and action flags are correct

### Task 5: Audit Agent Files
- Verify all 6 TAC-12 agents are in the agents list (Tasks 14-19)
- Check agent template references
- Verify file paths and action flags are correct

### Task 6: Audit Hook Files
- Verify all 9 TAC-12 hooks are in the hooks list (Tasks 20-28)
- Check hook templates exist
- Verify executable=True flag for all hooks
- Verify action flags are correct

### Task 7: Audit Hook Utilities
- Verify 5 TAC-12 hook utilities are properly configured (Tasks 29-33)
- Check LLM utilities (llm/__init__.py, anth.py, oai.py, ollama.py)
- Check TTS utilities (tts/__init__.py, elevenlabs_tts.py, openai_tts.py, pyttsx3_tts.py)
- Verify action flags are correct

### Task 8: Verify Output Style Files
- Verify output style files are being generated
- Check that all presets are included
- Verify action flags are correct

### Task 9: Run Validation and Testing
- Run pytest to validate syntax and logic
- Run lint checks
- Verify smoke test with --help flag
- Execute validation commands (see Validation Commands section)

## Validation Commands

Validate the changes with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Run all unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Lint checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test for CLI
- `cd tac_bootstrap_cli && python -m pytest tests/application/test_scaffold_service.py -v` - Scaffold service tests only

## Notes

- This is Wave 7 (Configuration Updates), Task 41 of 49
- The scaffold service uses a builder pattern via ScaffoldPlan to track all operations
- FileAction enum defines behavior: CREATE (skip if exists), OVERWRITE, PATCH, SKIP
- All templates are Jinja2 files that use `config` context variable
- The service applies changes idempotently - plans can be re-applied safely
- Status lines are a new TAC-12 feature for CLI output customization
- Verify that directory creation happens before file creation in the plan
