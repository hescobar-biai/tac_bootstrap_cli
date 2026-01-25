# Documentation Generators Orchestration Script

**ADW ID:** feature_6_3
**Date:** 2026-01-24
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/feature_6_3/specs/issue-171-adw-feature_6_3-sdlc_planner-run-generators-orchestrator.md

## Overview

This feature provides a Bash orchestration script that executes two documentation generators in the correct sequence: inline docstring enrichment followed by fractal documentation generation. The script includes comprehensive preflight validation, flag propagation, and fail-fast error handling to ensure reliable documentation updates.

## What Was Built

- Jinja2 template for the orchestration script (`run_generators.sh.j2`)
- Rendered example script in project root (`scripts/run_generators.sh`)
- Preflight validation for dependencies and file existence
- Command-line flag parsing (`--dry-run`, `--changed-only`, `--help`)
- Sequential execution pipeline with progress reporting
- Comprehensive error handling with actionable messages

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2`: New Jinja2 template that renders the orchestration script with configurable REPO_ROOT from `config.paths.app_root`
- `scripts/run_generators.sh`: Rendered example of the orchestration script (executable) for validation in the TAC Bootstrap project itself
- `specs/issue-171-adw-feature_6_3-sdlc_planner-run-generators-orchestrator.md`: Complete feature specification with implementation plan
- `specs/issue-171-adw-feature_6_3-sdlc_planner-run-generators-orchestrator-checklist.md`: Acceptance criteria checklist

### Key Changes

1. **Fail-Fast Configuration**: Uses `set -euo pipefail` to stop execution on first error, preventing partial documentation updates
2. **Comprehensive Preflight Checks**: Validates python3, uv, generator script existence, REPO_ROOT existence, and creates DOCS_DIR if missing
3. **Smart Flag Propagation**:
   - `--dry-run` propagates to both generators for safe preview
   - `--changed-only` propagates only to docstring generator (fractal doesn't support it)
4. **Defensive Jinja2 Templating**: Template uses `config.paths.app_root | default('.')` filter for safe rendering when config is missing
5. **Sequential Pipeline**: Step 1 (docstrings) must complete before Step 2 (fractal) runs, ensuring fractal docs include enriched docstrings

## How to Use

### Basic Execution

Generate/update all documentation:

```bash
cd /path/to/project
./scripts/run_generators.sh
```

### Preview Mode (Dry-Run)

See what would change without modifying files:

```bash
./scripts/run_generators.sh --dry-run
```

### Incremental Updates

Only process files changed since last commit (faster for large projects):

```bash
./scripts/run_generators.sh --changed-only
```

Note: `--changed-only` only affects Step 1 (docstring enrichment). Step 2 (fractal docs) always processes all folders.

### Combined Flags

Preview incremental changes:

```bash
./scripts/run_generators.sh --dry-run --changed-only
```

### Get Help

```bash
./scripts/run_generators.sh --help
```

## Configuration

### Jinja2 Template Variables

The template (`run_generators.sh.j2`) uses the following from `config.yml`:

- `config.paths.app_root`: Root directory for code analysis (defaults to `.` if not specified)

### Runtime Configuration

Hardcoded in rendered script:

- `SCRIPTS_DIR`: Directory containing generator scripts (auto-detected via `dirname "$0"`)
- `DOCS_DIR`: Output directory for fractal docs (hardcoded to `docs`)

### Generator-Specific Flags

**Step 1 (gen_docstring_jsdocs.py):**
- `--repo`: Set to `$REPO_ROOT`
- `--mode`: Hardcoded to `complement` (only adds missing docstrings)
- `--changed-only`: Passed if user provides flag
- `--dry-run`: Passed if user provides flag

**Step 2 (gen_docs_fractal.py):**
- `--repo`: Hardcoded to `.` (current directory)
- `--docs-root`: Set to `$DOCS_DIR`
- `--include-root`: Set to `$REPO_ROOT`
- `--mode`: Hardcoded to `complement` (only adds missing docs)
- `--dry-run`: Passed if user provides flag

## Testing

### Validate Template Rendering

Check that the template renders correctly:

```bash
# Template should exist
ls -la tac_bootstrap_cli/tac_bootstrap/templates/scripts/run_generators.sh.j2

# Rendered script should exist and be executable
ls -la scripts/run_generators.sh
```

### Test Help Flag

```bash
bash scripts/run_generators.sh --help
```

Expected output: Usage message with options and examples

### Test Dry-Run Mode

Requires `.env` with `OPENAI_API_KEY`:

```bash
bash scripts/run_generators.sh --dry-run
```

Expected behavior:
- Step 1 shows which files would be enriched
- Step 2 shows which docs would be generated
- No files are modified

### Validate Shell Syntax

If shellcheck is installed:

```bash
shellcheck scripts/run_generators.sh
```

### Test Preflight Checks

The script validates dependencies before execution:

1. **Missing python3**: Script exits with error "python3 is required but not installed"
2. **Missing uv**: Script exits with error "uv is required but not installed" and shows install command
3. **Missing generator scripts**: Script exits with error showing which script is missing
4. **Missing REPO_ROOT**: Script exits with error "REPO_ROOT directory not found"

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

1. **No git dirty checks**: Omitted per spec clarifications - generators provide `--dry-run` for safety
2. **Simple language handling**: Unlike spec's defensive filters, current implementation doesn't pass `--languages` flag to docstring generator (uses generator's default)
3. **Hardcoded mode**: Both generators use `--mode complement` to only add missing documentation without overwriting existing
4. **Create DOCS_DIR automatically**: Standard behavior for documentation tools, prevents errors
5. **Warning for unknown flags**: Script warns but continues, allowing extensibility

### Limitations

1. **DOCS_DIR location**: Hardcoded to `docs`, not configurable via flag
2. **Verbosity**: No verbose/quiet modes, always shows progress echoes
3. **Selective execution**: Cannot skip individual steps (e.g., `--skip-docstrings`)
4. **No language configuration**: Docstring generator uses default language detection instead of template variable
5. **No timing info**: Doesn't report how long each step takes

### Future Enhancements

1. Add `--verbose` flag for detailed logging of each file processed
2. Add `--skip-docstrings` or `--skip-fractal` for selective execution
3. Add timing information for each step
4. Add git dirty check with `--force` override for extra safety
5. Add support for custom DOCS_DIR via `--docs-dir` flag
6. Add OPENAI_API_KEY validation before running generators
7. Add language configuration support via `config.project.language`
8. Support parallel execution if generators become independent

### Related Features

- **Feature 6.1**: gen_docstring_jsdocs.py template (Step 1 dependency)
- **Feature 6.2**: gen_docs_fractal.py template (Step 2 dependency)
- **Future**: `/document` slash command integration for Claude-based workflows

### Integration with TAC Bootstrap

When TAC Bootstrap CLI renders projects:

1. Template is rendered to `scripts/run_generators.sh` in target project
2. File permissions set to executable (chmod +x)
3. REPO_ROOT variable substituted from project's `config.yml`
4. Script becomes available for documentation automation in generated project
