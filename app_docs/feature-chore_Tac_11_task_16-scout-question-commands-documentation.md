---
doc_type: feature
adw_id: chore_Tac_11_task_16
date: 2026-01-27
idk:
  - slash-commands
  - agent-delegation
  - codebase-exploration
  - parallel-search
  - read-only-exploration
  - documentation
tags:
  - feature
  - documentation
  - commands
related_code:
  - .claude/commands/scout.md
  - .claude/commands/question.md
  - tac_bootstrap_cli/docs/commands.md
---

# Scout and Question Commands Documentation

**ADW ID:** chore_Tac_11_task_16
**Date:** 2026-01-27
**Specification:** specs/issue-356-adw-chore_Tac_11_task_16-sdlc_planner-document-scout-question-commands.md

## Overview

Added comprehensive documentation for two new slash commands (`/scout` and `/question`) to the TAC Bootstrap CLI documentation. The `/scout` command enables parallel codebase exploration with configurable search strategies to identify relevant files for a task, while `/question` provides read-only Q&A about project structure and architecture.

## What Was Built

- Documentation for `/scout` command including detailed subsection with parameters, search strategies, output format, and usage guidance
- Documentation for `/question` command with table entry and usage example
- Integration of both commands into the existing commands.md documentation structure
- Examples demonstrating TAC Bootstrap-specific use cases

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/docs/commands.md`: Main CLI documentation file updated with two new command entries
  - Added `/question <query>` to "Context Management Commands" table (line 107)
  - Added `/scout <task> [scale]` to "Agent Delegation Commands" table (line 140)
  - Created detailed subsection for `/scout` command (lines 171-209) with parameters, strategies, output format, and usage guidance

### Key Changes

- **Question command entry**: Simple table entry in "Context Management Commands" section describing read-only project exploration
- **Scout command subsection**: Comprehensive documentation including:
  - Two required/optional parameters: `<task>` (required task description) and `[scale]` (optional 2-10 parallel strategies, default 4)
  - Four core search strategies: file patterns (Glob), content search (Grep), architectural analysis, and dependency mapping
  - SCALE parameter behavior: higher values (5-10) enable specialized searches for tests, configuration, types, and documentation
  - Output details: generates `agents/scout_files/relevant_files_{timestamp}.md` with frequency-scored results grouped by confidence level
  - Usage guidance: when to use (unfamiliar codebase, scope understanding, dependency mapping) vs. when NOT to use (known files, trivial changes, specific queries)
- Three usage examples for each command demonstrating typical TAC Bootstrap scenarios

## How to Use

### Using /scout Command

1. **Basic usage with default scale (4 strategies):**
   ```bash
   /scout "add authentication to API endpoints"
   ```

2. **Thorough exploration with custom scale:**
   ```bash
   /scout "implement caching layer" 6
   ```

3. **Quick exploration (minimal strategies):**
   ```bash
   /scout "fix database connection pooling" 2
   ```

The command launches parallel exploration agents using different search strategies (file patterns, content search, architecture analysis, dependency mapping, and more based on scale). Results are saved to `agents/scout_files/relevant_files_{timestamp}.md` with files grouped by confidence level based on how many strategies found them.

### Using /question Command

1. **Ask about project structure:**
   ```bash
   /question What is the project structure?
   ```

The command uses read-only exploration to answer questions about the codebase, reading relevant files and providing structured responses with file references.

## Configuration

No configuration changes required. Both commands are available immediately after updating the documentation.

## Testing

### Verify documentation accuracy

```bash
cat tac_bootstrap_cli/docs/commands.md | grep -A 5 "/scout"
```

This should show the `/scout` entry in the Agent Delegation Commands table and the beginning of its detailed subsection.

```bash
cat tac_bootstrap_cli/docs/commands.md | grep "/question"
```

This should show the `/question` entry in the Context Management Commands table.

### Run validation commands

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

All tests should pass with no regressions.

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Linting should complete with no errors.

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

CLI should load successfully and display help information.

## Notes

- The `/scout` command is complex with multiple parameters and strategies, requiring a detailed subsection with comprehensive usage guidance
- The `/question` command is straightforward, requiring only a simple table entry with brief description
- Both commands are read-only exploration tools (no code modification capabilities)
- Documentation follows existing formatting patterns in commands.md (tables for simple commands, subsections for complex ones)
- Examples use TAC Bootstrap-specific scenarios consistent with CLAUDE.md project context
- The `/scout` command implements TAC-10 Level 4 (Delegation Prompt) pattern for parallel compute orchestration
- Higher SCALE values in `/scout` enable more specialized search strategies but take longer to execute
- Frequency scoring in `/scout` output helps prioritize which files are most relevant (found by multiple independent strategies)
