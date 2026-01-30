---
doc_type: feature
adw_id: feature_Tac_12_task_11_2
date: 2026-01-30
idk:
  - context-bundle
  - session-recovery
  - jsonl-parsing
  - file-deduplication
  - slash-command
  - context-restoration
  - agent-workflow
tags:
  - feature
  - command
  - context-management
related_code:
  - .claude/commands/load_bundle.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2
  - .claude/commands/conditional_docs.md
  - .claude/hooks/context_bundle_builder.py
---

# Load Bundle Command

**ADW ID:** feature_Tac_12_task_11_2
**Date:** 2026-01-30
**Specification:** specs/issue-463-adw-feature_Tac_12_task_11_2-sdlc_planner-load-bundle-command.md

## Overview

The `/load_bundle` slash command enables Claude Code agents to restore session context by loading JSONL bundle files that track all file operations during a session. This critical feature supports session recovery, debugging agent behavior, and continuing interrupted work by intelligently deduplicating and restoring files with their original read parameters.

## What Was Built

- **Base Command File**: `.claude/commands/load_bundle.md` with complete context restoration logic
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2` for CLI generation
- **Conditional Documentation**: Updated `.claude/commands/conditional_docs.md` with load_bundle entry
- **Enhanced Bundle Schema**: Extended JSONL format to include user prompts for better context understanding
- **Smart File Deduplication**: Optimized file reading to avoid redundant operations and maximize context coverage

## Technical Implementation

### Files Modified

- `.claude/commands/load_bundle.md`: Base command implementation with enhanced deduplication logic, prompt tracking, and comprehensive error handling
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/load_bundle.md.j2`: Simplified template version using BUNDLE_PATH variable for CLI generation
- `.claude/commands/conditional_docs.md`: Added conditional documentation entry for load_bundle with 8 specific trigger conditions

### Key Changes

1. **Extended JSONL Schema**: Added `prompt` operation type and `prompt` field to track user requests throughout session history

2. **Smart File Deduplication Algorithm**:
   - Groups entries by `file_path` to identify unique files
   - Selects optimal read parameters per file:
     - Full file read if any entry has no limit/offset
     - Largest limit with `offset: 0` otherwise
     - Reads furthest into file if all have offsets > 0
   - Simplification: reads entire file if more than 3 entries exist

3. **Prompt Tracking**: Agents now read user prompts from bundle to understand the work story without acting on them, providing crucial context about what the previous agent was trying to accomplish

4. **Enhanced Reporting**: Extended report format to include:
   - User prompts encountered during session
   - Prompt operation counts alongside reads, writes, edits
   - Comprehensive operation summary

5. **Simplified Template Approach**: Template version uses `BUNDLE_PATH: $ARGUMENTS` for direct path specification, making it simpler for CLI-generated projects

## How to Use

### Basic Usage - Load Most Recent Bundle

```bash
/load_bundle
```

The agent will automatically find and load the most recent bundle from `logs/context_bundles/`.

### Load Specific Bundle by Path

```bash
/load_bundle logs/context_bundles/session_abc123-def456.jsonl
```

### What Happens

1. Agent locates the bundle file (explicit path or most recent)
2. Parses JSONL entries to extract file operations and user prompts
3. Deduplicates file entries and determines optimal read parameters
4. Reads each unique file only once with optimal coverage
5. Reports comprehensive summary including:
   - Bundle metadata (path, entry count, session ID)
   - User prompts encountered (the story of the work)
   - Files successfully restored
   - Files missing (handled gracefully)
   - Operation counts (reads, writes, edits, prompts)

## Configuration

### Bundle Storage Location

- **Base Repository**: `logs/context_bundles/session_{session_id}.jsonl`
- **Generated Projects**: `logs/context_bundles/session_{session_id}.jsonl`

### Allowed Tools

The command uses restricted tool access for safety:
- `Read`: For loading bundle files and restoring file context
- `Bash(ls*)`: For finding most recent bundle when no path specified

### Bundle Creation

Bundles are automatically created by the `context_bundle_builder` hook. No manual configuration required.

## Testing

### Test Loading Most Recent Bundle

```bash
# First, ensure bundles exist
ls -la logs/context_bundles/

# Load most recent bundle
/load_bundle
```

### Test Loading Specific Bundle

```bash
# Find available bundles
ls logs/context_bundles/session_*.jsonl

# Load specific bundle
/load_bundle logs/context_bundles/session_{session_id}.jsonl
```

### Verify Deduplication Logic

```bash
# Check a bundle has multiple reads of same file
cat logs/context_bundles/session_{session_id}.jsonl | grep '"file_path":"README.md"'

# Load bundle and verify file is read only once
/load_bundle logs/context_bundles/session_{session_id}.jsonl
```

### Test Error Handling

```bash
# Test missing bundle file
/load_bundle logs/context_bundles/nonexistent.jsonl

# Expected: Clear error message, no crash
```

### Integration Test with CLI Generation

```bash
# Verify template is included in scaffold
cd tac_bootstrap_cli
uv run pytest tests/ -v --tb=short -k scaffold

# Verify linting passes
uv run ruff check .

# Verify type checking passes
uv run mypy tac_bootstrap/
```

## Notes

### Design Decisions

1. **Static Template**: The Jinja2 template is nearly identical to the base command because bundle handling logic is universal across projects. No project-specific customization needed.

2. **Deduplication Priority**: Reading entire files when possible maximizes context restoration while minimizing Read tool calls, balancing completeness with efficiency.

3. **Prompt Tracking**: User prompts provide critical context about agent intentions without requiring agents to re-execute potentially dangerous or incomplete commands.

4. **Graceful Degradation**: Missing files are expected and handled gracefully since files may be deleted between bundle creation and restoration.

### Use Cases

- **Session Recovery**: Resume work after timeout, crash, or interruption
- **Agent Debugging**: Understand what files an agent accessed and what user requested
- **Context Handoff**: New agents can understand previous agent's work story
- **Behavior Analysis**: Review operation history to debug unexpected behavior

### Future Enhancements

The following features can be added without breaking changes:
- Bundle compression for large sessions
- Bundle filtering by operation type
- Bundle merging from multiple sessions
- Bundle expiration and cleanup policies

### Related Infrastructure

- `.claude/hooks/context_bundle_builder.py`: Creates JSONL bundles automatically
- `logs/context_bundles/`: Storage location for bundle files
- `conditional_docs.md`: Determines when to surface bundle documentation
