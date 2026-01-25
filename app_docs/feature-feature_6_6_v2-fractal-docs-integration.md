# Fractal Documentation Scripts Integration

**ADW ID:** feature_6_6_v2
**Date:** 2026-01-24
**Specification:** specs/issue-195-adw-feature_6_6_v2-sdlc_planner-integrate-fractal-docs-scripts.md

## Overview

This feature integrates fractal documentation scripts into TAC Bootstrap's scaffolding system, automatically generating documentation generation tools when creating new projects. Projects scaffolded with `tac-bootstrap init` or `tac-bootstrap add-agentic` now include a complete fractal documentation system without manual intervention.

## What Was Built

- **Fractal docs script integration** in ScaffoldService
- **Automatic generation** of 3 Python/Bash scripts for documentation
- **Canonical IDK vocabulary** configuration file
- **Slash command** for fractal doc generation
- **Documentation output directory** structure

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added `_add_fractal_docs_scripts()` method and integration into `build_plan()`, removed duplicated script declarations from `_add_script_files()`

### Key Changes

- **New method `_add_fractal_docs_scripts()`** (lines 571-615): Declares 5 files and 1 directory for fractal documentation system
  - 3 executable scripts: `gen_docstring_jsdocs.py`, `gen_docs_fractal.py`, `run_generators.sh`
  - 1 configuration file: `canonical_idk.yml` (root level)
  - 1 slash command: `.claude/commands/generate_fractal_docs.md`
  - 1 directory: `docs/` for documentation output

- **Integration in `build_plan()`** (line 99): Calls `_add_fractal_docs_scripts()` after structure files are added

- **Removed duplicates from `_add_script_files()`** (lines 410-411): Removed `gen_docs_fractal.py` and `gen_docstring_jsdocs.py` to avoid duplication (now handled by fractal docs method)

- **Uses `FileAction.CREATE`**: Idempotent behavior - only creates files if they don't exist, safe for existing repositories

- **Scripts marked executable**: All three scripts use `executable=True` parameter for proper file permissions

## How to Use

### Generating a New Project with Fractal Docs

1. Create a new project with TAC Bootstrap:
```bash
tac-bootstrap init my-awesome-project
```

2. The following fractal documentation files are automatically generated:
   - `scripts/gen_docstring_jsdocs.py` - Generates IDK docstrings/JSDoc comments
   - `scripts/gen_docs_fractal.py` - Generates fractal documentation
   - `scripts/run_generators.sh` - Runs all documentation generators
   - `canonical_idk.yml` - Canonical IDK vocabulary configuration
   - `.claude/commands/generate_fractal_docs.md` - Slash command for doc generation
   - `docs/` - Output directory for generated documentation

### Using the Fractal Documentation System

1. Generate fractal documentation:
```bash
cd my-awesome-project
./scripts/run_generators.sh
```

2. Or use individual generators:
```bash
python scripts/gen_docstring_jsdocs.py
python scripts/gen_docs_fractal.py
```

3. From Claude Code, use the slash command:
```
/generate_fractal_docs
```

### Adding to Existing Projects

Run `tac-bootstrap add-agentic` in an existing repository to add the fractal documentation system:
```bash
cd existing-project
tac-bootstrap add-agentic
```

## Configuration

### canonical_idk.yml

The canonical IDK vocabulary file is generated at project root and defines the vocabulary used for fractal documentation. It contains:
- Core concepts and their definitions
- Relationships between concepts
- Documentation patterns

### Script Permissions

All three scripts (`*.py`, `*.sh`) are automatically marked as executable during scaffolding. No manual `chmod +x` required.

## Testing

Run the test suite to verify fractal docs integration:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "fractal"
```

Run full validation suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **No duplication**: The method ensures `gen_docs_fractal.py` and `gen_docstring_jsdocs.py` are only declared once (removed from `_add_script_files()`)
- **Idempotent**: Using `FileAction.CREATE` ensures files are only created if they don't exist, safe for re-scaffolding
- **Universal inclusion**: Fractal docs scripts are included in ALL scaffolded projects, not conditional based on configuration
- **Template organization**: Templates are stored in `templates/config/` for internal organization, but `canonical_idk.yml` is output to project root
- **Depends on templates**: Requires templates from tasks 6.1-6.5 to exist in `tac_bootstrap_cli/tac_bootstrap/templates/`
