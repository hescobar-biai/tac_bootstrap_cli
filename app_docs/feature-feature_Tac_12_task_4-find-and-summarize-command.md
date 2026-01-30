---
doc_type: feature
adw_id: feature_Tac_12_task_4
date: 2026-01-30
idk:
  - slash-command
  - file-discovery
  - glob-pattern
  - ai-summarization
  - codebase-exploration
  - jinja2-template
  - scaffold-service
tags:
  - feature
  - command
  - cli
related_code:
  - .claude/commands/find_and_summarize.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Find and Summarize Command

**ADW ID:** feature_Tac_12_task_4
**Date:** 2026-01-30
**Specification:** specs/issue-456-adw-feature_Tac_12_task_4-sdlc_planner-find-and-summarize-command.md

## Overview

Implemented the `/find_and_summarize` command, a lightweight file discovery and AI-powered summarization tool. This command enables users to search for files matching a glob pattern and receive structured summaries of their contents, purposes, and relationships. It provides a simpler, faster alternative to comprehensive exploration tools like `/scout` when users already know the file pattern they want to examine.

## What Was Built

- **Base Command File**: `.claude/commands/find_and_summarize.md` - Complete command specification with Variables, Instructions, Workflow, Report, Examples, and Notes sections
- **Jinja2 Template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2` - Template for CLI generation (identical to base since no config variables needed)
- **Service Registration**: Updated `scaffold_service.py` to include "find_and_summarize" in the commands list

## Technical Implementation

### Files Modified

- `.claude/commands/find_and_summarize.md`: New 326-line command specification file
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2`: New Jinja2 template (326 lines, identical to base)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added "find_and_summarize" to commands list (line 313)

### Key Changes

1. **Command Structure**: Created comprehensive command file following established patterns with YAML frontmatter approach transformed into markdown sections (Variables, Instructions, Workflow, Report)

2. **Two-Parameter Design**:
   - `PATTERN` ($1): Required glob pattern for file matching (e.g., `**/*.py`, `src/**/service.ts`)
   - `FOCUS` ($2): Optional focus area to emphasize specific aspects in summary (e.g., "authentication logic")

3. **Three-Step Workflow**:
   - **Find**: Uses Glob tool to discover files matching the pattern
   - **Read**: Reads content of ~20 files (suggested limit, agent decides)
   - **Summarize**: Generates structured markdown with Files Found, Summary of Contents, and Key Findings sections

4. **Edge Case Handling**:
   - No files found: Friendly message with pattern suggestions
   - Too many files (>50): Warning and recommendation to refine pattern
   - Read failures: Notes failed files but continues with successful reads

5. **Template Design**: No Jinja2 config variables needed since command is project-agnostic and generic

## How to Use

### Basic Usage

```bash
/find_and_summarize "**/*.py"
```

Finds all Python files in the codebase and provides a comprehensive summary.

### With Focus Parameter

```bash
/find_and_summarize "src/**/service.ts" "focusing on authentication logic"
```

Finds TypeScript service files and emphasizes authentication-related code in the summary.

### Other Examples

```bash
# Find markdown documentation
/find_and_summarize "docs/**/*.md"

# Find configuration files
/find_and_summarize "*.{json,yaml,yml,toml}"

# Find test files with focus
/find_and_summarize "**/*test*.py" "test coverage for authentication"
```

## Configuration

No configuration variables required. The command works out-of-the-box for any project after scaffold generation.

### Glob Pattern Syntax

- `*` - Matches any characters except directory separator
- `**` - Matches any characters including directory separators (recursive)
- `?` - Matches single character
- `{a,b}` - Matches either a or b
- `[abc]` - Matches any character in brackets

## Testing

### Validate Command Files Exist

```bash
ls -la .claude/commands/find_and_summarize.md
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/find_and_summarize.md.j2
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Run Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test CLI

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Testing (after scaffold generation)

Test edge cases:
1. Pattern with no matches: `/find_and_summarize "nonexistent/**/*.xyz"`
2. Pattern with many matches: `/find_and_summarize "**/*.md"`
3. Pattern with focus: `/find_and_summarize "**/*.py" "focusing on error handling"`
4. Invalid pattern: `/find_and_summarize ""`

## Notes

### Relationship to /scout Command

**Use `/scout` when:**
- You need comprehensive multi-strategy exploration
- You want confidence scoring and frequency analysis
- You need to map dependencies, architecture, tests, configs
- You don't know exactly what you're looking for

**Use `/find_and_summarize` when:**
- You know the file pattern you want to examine
- You need a quick summary of specific files
- You want a simpler, faster workflow
- You don't need parallel strategies or confidence scoring

### Design Decisions

1. **No Config Variables**: Command is generic and project-agnostic, so no Jinja2 variables needed
2. **Suggested ~20 File Limit**: Mentioned in instructions to guide agent, but not enforced - agent decides based on context
3. **Leverages Existing Tool Limits**: Read tool already handles large files (2000 lines default)
4. **Focus Parameter Optional**: Allows targeted summaries but works fine without it
5. **Markdown Output**: Consistent with other commands, readable, structured

### Best Practices

1. Be specific with patterns: `src/**/*.service.ts` is better than `**/*.ts`
2. Use focus for targeted summaries when looking for specific aspects
3. Refine broad patterns if you get too many files
4. Combine with other tools: Use `/find_and_summarize` for overview, then Read specific files for details
5. Check directories first with `ls` or Glob to understand structure

### Performance Considerations

- **1-10 files**: Very fast, seconds
- **11-20 files**: Fast, under a minute
- **21-50 files**: Moderate, may take 1-2 minutes
- **>50 files**: Slow, consider refining pattern or using first 20 only

### Integration with TAC-12 Plan

This command is **Task 4 of 49** in the TAC-12 integration plan (Wave 1 - New Commands). It follows the established pattern of:
1. Creating base command file in `.claude/commands/`
2. Creating Jinja2 template in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
3. Registering command in `scaffold_service.py` commands list

The implementation maintains consistency with previous commands (all_tools, build_in_parallel) and sets the pattern for remaining command integration tasks.
