---
doc_type: feature
adw_id: feature_Tac_9_task_20
date: 2026-01-26
idk:
  - slash-command
  - context-bundle
  - jsonl
  - session-recovery
  - jinja2-template
  - claude-code
tags:
  - feature
  - command-template
related_code:
  - .claude/commands/load_bundle.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2
---

# Load Bundle Command Template

**ADW ID:** feature_Tac_9_task_20
**Date:** 2026-01-26
**Specification:** specs/issue-261-adw-feature_Tac_9_task_20-sdlc_planner-load-bundle-command.md

## Overview

Created a Jinja2 template for the `/load_bundle` slash command that enables context recovery from previously saved context bundles. This command is the manual complement to the automatic `context_bundle_builder` hook, allowing users to restore file operation history from JSONL bundle files and re-read tracked files to recover working context.

## What Was Built

- Jinja2 command template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`
- Rendered example command at `.claude/commands/load_bundle.md` for this project
- Complete command structure with Variables, Instructions, Run, Examples, and Report sections
- Integration with existing context bundle storage pattern (`logs/context_bundles/session_{session_id}.jsonl`)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`: Jinja2 template for `/load_bundle` command following established command pattern
- `.claude/commands/load_bundle.md`: Rendered example of the command for TAC Bootstrap project

### Key Changes

- **Command Structure**: Follows the same pattern as `/background` command with Variables/Instructions/Run/Examples/Report sections
- **Flexible Arguments**: Accepts either `bundle_path` (direct file path) or `session_id` (constructs path), defaults to most recent bundle
- **JSONL Parsing**: Provides step-by-step instructions for reading and parsing JSONL entries with schema documentation
- **Graceful Error Handling**: Instructions for handling missing files, corrupted bundles, and partial context recovery
- **Operation Filtering**: Prioritizes 'read' and 'edit' operations with 'success' status for context restoration
- **Comprehensive Reporting**: Structured report format showing files restored, files missing, and operation summary

### JSONL Entry Schema

The command documents and works with the following JSONL structure:
```json
{
    "timestamp": "2024-01-26T14:30:45.123456",
    "operation": "read|write|edit|notebookedit",
    "file_path": "relative/path/to/file.py",
    "status": "success|error",
    "session_id": "uuid-string",
    "tool_input": {...}
}
```

## How to Use

### For Template Users (Generated Projects)

When TAC Bootstrap generates a new project with this template:

1. The `/load_bundle` command will be available in `.claude/commands/`
2. Users can invoke it in three ways:
   ```
   /load_bundle
   /load_bundle session_id=abc123-def456
   /load_bundle bundle_path=logs/context_bundles/session_xyz.jsonl
   ```
3. The command will restore context by re-reading files tracked in the bundle

### For Template Development (This Project)

The rendered command at `.claude/commands/load_bundle.md` serves as:
- Working example for testing the template
- Documentation reference for the command structure
- Demo of how the template renders with actual config

## Configuration

The template uses Jinja2 variables for project-specific customization:
- `{{ config.project.name }}` - Project name (if referenced in instructions)
- Template can be extended with additional config variables as needed

Storage path is standardized:
- Bundle location: `logs/context_bundles/session_{session_id}.jsonl`
- This path matches the `context_bundle_builder` hook implementation

## Testing

### Verify Template Syntax

Check that the Jinja2 template is valid:

```bash
cd tac_bootstrap_cli && uv run python -c "from jinja2 import Template; Template(open('tac_bootstrap/templates/claude/commands/load_bundle.md.j2').read())"
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Run Type Check

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Verify CLI Works

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing (if context bundles exist)

If you have context bundles from previous sessions:

```bash
# List available bundles
ls -lt logs/context_bundles/

# Test loading most recent bundle
# (Use the command as documented in .claude/commands/load_bundle.md)
```

## Notes

### Relationship to Context Bundle Hook

The `/load_bundle` command is the manual companion to the automatic `context_bundle_builder` hook:
- **Hook** (Task 17): Automatically tracks file operations → saves to JSONL
- **Command** (Task 20): Manually reads JSONL → restores context by re-reading files

This separation allows:
- Automatic tracking without user intervention during sessions
- Manual recovery when needed (after failures, for debugging)
- Flexibility in when and how context is restored

### Design Philosophy

- **Graceful Degradation**: Never fails completely if some files are missing; provides clear feedback about what succeeded/failed
- **Partial Recovery**: Allows context restoration even if only some files still exist
- **Operation Filtering**: Focuses on 'read' and 'edit' operations with 'success' status, skips failed writes
- **Human-Readable**: JSONL format is tool-friendly (jq, grep work) and human-readable for debugging

### Command Pattern Consistency

This template follows the established pattern seen in other commands:
- `/background` - Most similar structure (Variables/Instructions/Run/Examples/Report)
- `/feature` - Planning command with structured sections
- `/prime` - Context-loading command that reads multiple files

### Future Enhancements (Out of Scope)

Potential extensions not included in this implementation:
- Filtering by file pattern when loading
- Filtering by operation type (only load reads, not writes)
- Time-based filtering (only recent operations)
- Merging multiple bundles
- Interactive bundle selection UI
- Bundle diff/comparison tools
