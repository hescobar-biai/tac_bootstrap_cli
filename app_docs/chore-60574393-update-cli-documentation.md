# Update CLI Documentation for add-agentic Command

**ADW ID:** 60574393
**Date:** 2026-01-21
**Specification:** specs/issue-76-adw-60574393-chore_planner-update-cli-documentation.md

## Overview

Updated the "For Existing Projects" section of the CLI README to document the `add-agentic` command's behavior, emphasizing safety guarantees, idempotency, and detailed file creation information.

## What Was Built

- Enhanced documentation explaining what files/directories are created by `add-agentic`
- Added safety guarantees (no overwrites, idempotent execution)
- Improved code example with inline comments describing the workflow
- Maintained consistency with existing documentation format

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/README.md` (lines 197-220): Replaced basic usage example with comprehensive documentation including:
  - List of all directories/directorios created (.claude/commands/, .claude/hooks/, adws/, scripts/)
  - List of all configuration files created (config.yml, constitution.md)
  - Auto-detection capabilities (language, framework, package manager)
  - Safety guarantees section
  - Additional usage examples

### Key Changes

- Added detailed inline bash comments explaining the `add-agentic` workflow in two sections:
  - **This will:** section documenting auto-detection and file creation
  - **Safe for existing repos:** section emphasizing non-destructive behavior
- Documented that 25+ slash commands are created in .claude/commands/
- Clarified idempotent behavior (can run multiple times safely)
- Preserved existing "Other usage examples" section for consistency

## How to Use

The updated documentation is now visible to users reading the README. No code changes were made to the CLI itself - this was a documentation-only update.

Users can verify the documentation by:

1. Reading the README:
   ```bash
   cat tac_bootstrap_cli/README.md
   ```

2. The documentation accurately describes the behavior implemented in ScaffoldService.

## Configuration

No configuration changes were required. This was a documentation update only.

## Testing

Validation commands were run to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

All tests pass with zero regressions.

## Notes

- This documentation aligns with the actual behavior implemented in ScaffoldService (using FileAction.CREATE for existing repos)
- The documentation emphasizes the three key user concerns addressed in issue #76:
  1. What files are created
  2. Safety for existing repositories
  3. Idempotency
- Format follows existing README conventions (bash comments with `#` prefix, code blocks)
- Future maintainers should update this section if new files/directories are added to the agentic layer generation
