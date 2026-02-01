# Chore: Create .claude/data/claude-model-cache directory with .gitkeep

## Metadata
issue_number: `488`
adw_id: `chore_Tac_12_task_36`
issue_json: `{"number": 488, "title": "[Task 36/49] [CHORE] Create .claude/data/claude-model-cache directory with .gitkeep", "body": "## Description\n\nCreate directory for model info cache.\n\n## Files\n- **Base:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/data/claude-model-cache/.gitkeep`\n- **Template:** `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`\n\n## Changes Required\n- Create directory and .gitkeep file in base repository\n- Create Jinja2 template for CLI generation\n- Update `scaffold_service.py` to include directory creation\n\n## Note\nUsed by model_extractor.py for caching\n\n## Wave 5 - Status Line & Data Directories (Task 36 of 3)\n\n## Workflow Metadata\n/chore\n/adw_sdlc_zte_iso\n/adw_id: chore_Tac_12_task_36"}`

## Chore Description

Create a new `.claude/data/claude-model-cache/` directory with `.gitkeep` file in both:
1. **Base repository** (TAC Bootstrap reference)
2. **CLI templates** (for generated projects)

This directory is used by `model_extractor.py` to cache model information, similar to the existing `sessions` directory created in Task 35.

## Relevant Files

### Files to Modify
- **`tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`** - Add directory creation to `_add_directories()` method (currently lines 104-171)
- **`scaffold_service.py` location in method** - Lines 104-171 handle directory creation

### Files to Create
- **`.claude/data/claude-model-cache/.gitkeep`** - Base repository marker file
- **`tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2`** - Jinja2 template for CLI

### Related Files (for context)
- **`tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/sessions/.gitkeep.j2`** - Template pattern to follow (Task 35)
- **`model_extractor.py`** - Consumes this directory (mentioned in issue description)

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create base directory with .gitkeep
- Create `.claude/data/claude-model-cache/` directory
- Create `.claude/data/claude-model-cache/.gitkeep` empty file
- Verify directory exists and is ready for Git tracking

### Task 2: Create Jinja2 template file
- Create `tac_bootstrap_cli/tac_bootstrap/templates/structure/.claude/data/claude-model-cache/.gitkeep.j2` (empty template file, matching sessions pattern)
- Verify template can be found by template loader

### Task 3: Update scaffold_service.py
- Add `(".claude/data/claude-model-cache", "Model cache storage")` to directories list in `_add_directories()` method
- Add `.gitkeep` file creation after existing data directory entries (around line 167-171)
- Pattern: `plan.add_file(".claude/data/claude-model-cache/.gitkeep", action=FileAction.CREATE, content="", reason="Keep empty directory in Git")`

### Task 4: Validate all changes
- Run tests to verify no regressions
- Verify scaffold_service.py syntax is correct
- Confirm directory structure is maintained

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

- This follows the same pattern as Task 35 (sessions directory)
- The `.gitkeep` file is empty and serves only to preserve the directory in Git
- Both base repository and CLI templates need matching changes
- Used by model_extractor.py, so this is a required data directory
