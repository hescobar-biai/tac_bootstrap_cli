---
doc_type: feature
adw_id: feature_Tac_11_task_3
date: 2026-01-27
idk:
  - slash-command
  - parallel-exploration
  - codebase-analysis
  - task-delegation
  - exploration-strategy
  - frequency-scoring
  - subagent-orchestration
tags:
  - feature
  - slash-command
  - exploration
  - parallel
related_code:
  - .claude/commands/scout.md
  - specs/issue-328-adw-feature_Tac_11_task_3-sdlc_planner-scout-slash-command.md
---

# /scout Slash Command - Parallel Codebase Exploration

**ADW ID:** feature_Tac_11_task_3
**Date:** 2026-01-27
**Specification:** specs/issue-328-adw-feature_Tac_11_task_3-sdlc_planner-scout-slash-command.md

## Overview

The `/scout` slash command is a TAC-10 Level 4 (Delegation Prompt) that performs intelligent, parallel codebase exploration to identify files relevant to a given task. It launches multiple concurrent exploration agents using different search strategies (file patterns, content search, architectural analysis, dependency mapping) and aggregates results into a structured markdown report with frequency-based relevance scoring.

## What Was Built

- New slash command `.claude/commands/scout.md` implementing parallel codebase exploration
- Support for configurable SCALE parameter (2-10 parallel strategies)
- Four core exploration strategies optimized for different discovery patterns
- Structured output format with per-strategy findings and aggregated file lists
- Frequency-based relevance scoring to prioritize files found by multiple strategies
- Integration with existing TAC Bootstrap command ecosystem
- Updated CLAUDE.md documentation with /scout command reference

## Technical Implementation

### Files Modified

- `.claude/commands/scout.md`: Main slash command implementation with Variables, Instructions, Workflow, and Report sections
- `CLAUDE.md`: Added /scout to available commands section
- `specs/issue-328-adw-feature_Tac_11_task_3-sdlc_planner-scout-slash-command.md`: Feature specification
- `specs/issue-328-adw-feature_Tac_11_task_3-sdlc_planner-scout-slash-command-checklist.md`: Implementation checklist

### Key Changes

- **Parallel Agent Orchestration**: Uses Task tool with Explore subagent_type to launch multiple concurrent exploration agents in a single message, following the pattern from `/parallel_subagents` command

- **Multi-Strategy Search**: Implements 4 core strategies (expandable to 10) that cover complementary discovery patterns:
  - File patterns (Glob-based)
  - Content search (Grep-based)
  - Architectural analysis (Read-based structure mapping)
  - Dependency mapping (import/reference tracking)

- **Frequency-Based Scoring**: Aggregates results across all strategies and scores files by how many independent strategies discovered them, providing confidence-based prioritization

- **Read-Only Design**: Uses only Explore agents with read-only tools (Glob, Grep, Read), ensuring no code modifications during exploration

- **Structured Output**: Generates markdown reports in `agents/scout_files/` with timestamp-based naming, including per-strategy findings, aggregated file lists, and recommendations

## How to Use

### Basic Usage

```bash
/scout "task description"
```

Example:
```bash
/scout "implement user authentication"
```

This launches 4 parallel exploration agents (default SCALE) to find files relevant to implementing user authentication.

### With Custom SCALE

```bash
/scout "fix database connection pooling" 6
```

This launches 6 parallel strategies, including the 4 core strategies plus 2 additional granular searches.

### Understanding SCALE Parameter

- `SCALE=2`: Fastest, uses file patterns + content search only
- `SCALE=4`: Default, uses all 4 core strategies (recommended)
- `SCALE=6-10`: Adds specialized strategies (tests, configs, types, docs, etc.)

### Interpreting Results

The command generates a report in `agents/scout_files/relevant_files_YYYYMMDD_HHMMSS.md` with:

1. **Strategy Results**: Per-strategy findings showing which approach discovered which files
2. **Aggregated File List**: Deduplicated list sorted by confidence:
   - High Confidence: Found by 3+ strategies
   - Medium Confidence: Found by 2 strategies
   - Low Confidence: Found by 1 strategy
3. **Recommendations**: Priority files to read and suggested next steps

## Configuration

### Variables

- `USER_PROMPT` ($1): Required. Task description for file search
- `SCALE` ($2): Optional. Number of parallel strategies (default: 4, range: 2-10)

### Output Directory

Results are automatically saved to:
```
agents/scout_files/relevant_files_YYYYMMDD_HHMMSS.md
```

The directory is created automatically if it doesn't exist.

### SCALE Behavior

| SCALE | Strategies Used |
|-------|----------------|
| 2 | File patterns + content search |
| 3 | Above + architectural analysis |
| 4 | Above + dependency mapping (default) |
| 5-6 | Above + granular searches (tests, configs) |
| 7-10 | Above + specialized searches (docs, migrations, schemas) |
| >10 | Capped at 10 with warning |

## Testing

### Manual Testing - Basic Usage

Test the command with a simple task description:

```bash
/scout "implement authentication"
```

Verify:
- 4 parallel agents launch successfully
- Output file is created in `agents/scout_files/`
- Markdown format is well-structured
- Files are categorized by confidence level

### Manual Testing - Custom SCALE

Test with different SCALE values:

```bash
/scout "add caching layer" 2
/scout "refactor user service" 6
```

Verify:
- SCALE=2 uses subset of strategies
- SCALE=6 adds additional granular strategies
- All agents complete successfully

### Manual Testing - Edge Cases

Test validation and error handling:

```bash
/scout
# Should error: USER_PROMPT is required

/scout "test task" 1
# Should error: SCALE must be >= 2

/scout "test task" 15
# Should cap at 10 and warn
```

### Verify Output Format

After running a scout command, check the output file:

```bash
ls -la agents/scout_files/
cat agents/scout_files/relevant_files_*.md
```

Verify the markdown contains:
- Search summary with timestamp and SCALE
- Per-strategy results sections
- Aggregated file list with frequency counts
- Recommendations section

## Notes

### Design Rationale

- **No External Tools**: Unlike the original issue description, this implementation uses Claude Code's built-in Task tool with Explore subagent_type instead of external CLI tools (gemini, opencode, etc.), providing more reliable and consistent results.

- **Read-Only by Design**: The Explore agent type ensures no code modifications occur during exploration, eliminating the need for git safety checks.

- **Frequency-Based Relevance**: Files discovered by multiple independent strategies are more likely to be truly relevant, providing a natural confidence scoring mechanism.

- **Timestamp-Based Naming**: Using `YYYYMMDD_HHMMSS` format creates human-readable, sortable filenames without requiring UUID libraries.

### When to Use vs. Direct Exploration

Use `/scout` when:
- Working with unfamiliar codebase
- Task scope is unclear
- Multiple approaches or patterns might be relevant
- You want comprehensive file discovery

Use direct Grep/Glob when:
- You know exactly what you're looking for
- Searching for a specific function/class/file
- Single search pattern is sufficient

### Performance Considerations

- SCALE=2-4: Completes quickly, suitable for most tasks
- SCALE=5-8: Takes longer but provides more comprehensive results
- SCALE>8: Use sparingly, mainly for complex architectural analysis

### Integration with Other Commands

The `/scout` output can inform:
- `/feature` - Use discovered files to plan feature implementation
- `/implement` - Know which files need modification
- `/review` - Understand which files to review for changes
- `/document` - Identify related code for documentation

### Future Enhancements

Potential improvements for future iterations:
- Result caching to avoid re-exploring same prompts
- Directory exclusion patterns (e.g., node_modules, .git)
- File type filtering
- JSON output format for programmatic consumption
- Auto-integration with /implement command
