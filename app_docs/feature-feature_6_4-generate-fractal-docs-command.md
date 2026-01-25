# Generate Fractal Docs Slash Command

**ADW ID:** feature_6_4
**Date:** 2026-01-24
**Specification:** specs/issue-179-adw-feature_6_4-sdlc_planner-generate-fractal-docs-command.md

## Overview

This feature implements a Claude Code slash command (`/generate_fractal_docs`) that allows developers to invoke fractal documentation generation directly from their development workflow. The command acts as a defensive wrapper around the `scripts/run_generators.sh` orchestrator script, providing prerequisite validation, error handling, smart commit logic, and user guidance.

## What Was Built

- Jinja2 template for the slash command (`generate_fractal_docs.md.j2`)
- Rendered command file for the tac_bootstrap repository itself
- Integration with the documentation generator orchestrator from Task 6.3
- SCOPE argument support for full vs. incremental documentation generation
- Prerequisites validation to ensure the generator script exists
- Smart commit logic that only commits when changes actually exist
- User guidance through the review process

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/generate_fractal_docs.md.j2`: Jinja2 template for the slash command that will be rendered in generated projects
- `.claude/commands/generate_fractal_docs.md`: Rendered version of the command for use in the tac_bootstrap repository itself

### Key Changes

- **Template Structure**: Created a Claude Code slash command template following the existing pattern used by `/test` and `/commit` commands
- **SCOPE Argument**: Implemented argument handling with two modes:
  - "changed" (default): Runs `scripts/run_generators.sh --changed-only` for incremental updates
  - "full": Runs `scripts/run_generators.sh` to regenerate all documentation from scratch
- **Prerequisite Validation**: Added bash check to verify `scripts/run_generators.sh` exists before execution, with helpful error messages guiding users to run `tac-bootstrap init` if missing
- **Error Handling**: Added exit code checking after script execution to prevent proceeding to review/commit steps if generation fails
- **Smart Commit Logic**: Implemented `git diff --quiet docs/` check to only commit when documentation changes actually exist, avoiding empty commits
- **Config Integration**: Used `{{ config.paths.app_root | default("src") }}` pattern for safe template rendering across different project types

## How to Use

### Basic Usage

1. Generate or update documentation for changed files only (incremental):
   ```
   /generate_fractal_docs
   ```

2. Regenerate all documentation from scratch:
   ```
   /generate_fractal_docs full
   ```

### Workflow

When you run the command, it will:
1. Check that `scripts/run_generators.sh` exists (exits with helpful error if not)
2. Execute the documentation generator with appropriate flags
3. Display generation summary and prompt you to review files in `docs/`
4. Guide you to verify frontmatter YAML, IDK keywords, and overview sections
5. Automatically commit changes to `docs/` if any were made, or inform you if no changes exist

### Expected Output

- Updated/created markdown files in `docs/` directory
- One file per folder in your application root (e.g., `tac_bootstrap_cli/`)
- Each file contains:
  - Frontmatter with IDK keywords
  - Overview section describing folder contents
  - Module listings and descriptions

## Configuration

The command uses the following config values from `config.yml`:
- `config.paths.app_root`: Root directory of the application (defaults to "src" if not specified)

No additional configuration is required. The command inherits all configuration from `scripts/run_generators.sh`.

## Testing

The slash command can be tested by:

1. **Testing prerequisite validation**:
   ```bash
   # Temporarily rename the script
   mv scripts/run_generators.sh scripts/run_generators.sh.bak
   # Run command (should show helpful error)
   /generate_fractal_docs
   # Restore script
   mv scripts/run_generators.sh.bak scripts/run_generators.sh
   ```

2. **Testing SCOPE argument**:
   ```bash
   # Test default (changed only)
   /generate_fractal_docs

   # Test full regeneration
   /generate_fractal_docs full
   ```

3. **Testing smart commit**:
   ```bash
   # Run when no changes exist (should say "No changes")
   /generate_fractal_docs

   # Make a code change, run again (should commit)
   # Verify commit message: "docs: update fractal documentation"
   ```

4. **Manual verification**:
   - Verify generated markdown files in `docs/` directory
   - Check frontmatter YAML is valid
   - Verify IDK keywords are relevant
   - Confirm overview sections accurately describe folder contents

## Notes

### Design Decisions

- **Minimal validation in command**: The slash command is intentionally a thin wrapper. Complex validation (dependency checks, git fallback) belongs in `run_generators.sh`, not here.
- **SCOPE default is "changed"**: Most developers want incremental updates. Full regeneration is opt-in to avoid unnecessary processing.
- **Git fallback is transparent**: If git isn't initialized, `run_generators.sh` handles fallback to full mode automatically.
- **Commit both template and rendered**: Follows existing repo pattern where template (`.j2`) and rendered version coexist. This makes the command immediately usable in tac_bootstrap repo and serves as reference documentation.

### Integration Points

This command integrates with:
- `scripts/run_generators.sh` (Task 6.3): Orchestrator that handles actual documentation generation
- `scripts/gen_docstring_jsdocs.py` (Task 6.1): First generator in the pipeline
- `scripts/gen_docs_fractal.py` (Task 6.2): Second generator in the pipeline

### Future Enhancements

- Could add a `--dry-run` SCOPE option to preview changes without modifying files
- Could parse script output to show file count/summary in the command
- Could integrate with `/document` command for a complete documentation workflow
