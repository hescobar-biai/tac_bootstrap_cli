# Feature: /scout Slash Command for Parallel Codebase Exploration

## Metadata
issue_number: `328`
adw_id: `feature_Tac_11_task_3`
issue_json: `{"number":328,"title":"Create /scout slash command in base repository*","body":"feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_11_task_3\n\nCreate a new slash command that performs parallel multi-model codebase search using external AI tools (gemini, opencode, codex, claude).\n\n**Files affected:**\n- `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/scout.md`\n\n**Implementation details:**\n- Purpose: Search codebase for files needed to complete a task\n- Variables: USER_PROMPT ($1), SCALE ($2, defaults to 4)\n- Output directory: `agents/scout_files/`\n- Workflow:\n  - Launch SCALE number of Task agents in parallel\n  - Each agent calls Bash to run: gemini, opencode, codex, claude CLI tools\n  - Collect outputs as structured file lists with offset/limit\n  - Run `git diff --stat` to verify no changes, reset if needed\n  - Write results to `agents/scout_files/relevant_files_<unique-id>.md`\n- Use model: claude-sonnet-4-5-20250929"}`

## Feature Description

Create a `/scout` slash command that performs intelligent, parallel codebase exploration to identify relevant files needed for a given task. The command leverages Claude Code's Task tool with Explore subagent_type to launch multiple concurrent exploration agents, each using different search strategies (file patterns, content search, architectural analysis, dependency mapping). Results are aggregated into a structured markdown report showing both per-strategy findings and a deduplicated file list with frequency-based relevance scoring.

This command enables developers to quickly discover which files they need to read or modify for a given task, reducing the time spent manually searching through codebases and improving task planning accuracy.

## User Story

As a developer working on a complex codebase
I want to quickly identify all files relevant to a specific task
So that I can understand scope, plan implementation, and avoid missing critical dependencies

## Problem Statement

When working on a new feature or bug fix in an unfamiliar codebase, developers often spend significant time:
- Searching for relevant files using multiple strategies (grep, find, architecture understanding)
- Missing important files that should be modified
- Not understanding the full scope of changes needed
- Repeating searches with different patterns to ensure completeness

Current tools require sequential manual searches, which is time-consuming and prone to missing files.

## Solution Statement

The `/scout` command addresses this by:
1. Launching multiple parallel exploration agents, each using different search strategies
2. Aggregating results from all strategies to maximize file discovery coverage
3. Providing frequency-based relevance scoring (files found by multiple strategies are more relevant)
4. Delivering structured markdown output for easy review and reference
5. Using pure read-only exploration (no external tools, no git modifications)

The command follows the pattern of existing parallel orchestration commands (like `/parallel_subagents`) while specializing in codebase exploration.

## Relevant Files

### Existing Files
- `.claude/commands/parallel_subagents.md` - Reference for parallel Task agent orchestration pattern
- `.claude/commands/feature.md` - Reference for command structure and format
- `.claude/commands/implement.md` - Reference for task execution patterns
- `.claude/settings.json` - Claude Code settings (may need to verify command registration)

### New Files
- `.claude/commands/scout.md` - Main slash command implementation

## Implementation Plan

### Phase 1: Foundation
1. Research existing parallel command patterns to understand Task tool usage
2. Design the exploration strategy decomposition (4 default strategies)
3. Design output format structure with per-strategy and aggregated sections

### Phase 2: Core Implementation
1. Create `.claude/commands/scout.md` with full command logic
2. Implement variable parsing (USER_PROMPT, SCALE with default=4)
3. Implement parallel Task agent launch with Explore subagent_type
4. Implement 4 exploration strategies:
   - Strategy 1: File pattern search (Glob-based discovery)
   - Strategy 2: Content search (Grep-based discovery)
   - Strategy 3: Architectural analysis (structure and organization)
   - Strategy 4: Dependency mapping (imports, references, calls)
5. Implement result aggregation logic
6. Implement output file generation with timestamp-based naming
7. Add user progress feedback

### Phase 3: Integration
1. Test command with various USER_PROMPT examples
2. Verify output format readability and usefulness
3. Document command usage in CLAUDE.md
4. Verify SCALE parameter behavior (subset strategies if SCALE < 4, additional strategies if SCALE > 4)

## Step by Step Tasks

### Task 1: Research and Design
- Read `.claude/commands/parallel_subagents.md` to understand parallel Task orchestration
- Read `.claude/commands/feature.md` to understand command structure
- Design 4 exploration strategies with clear, non-overlapping search criteria
- Design output markdown format with sections:
  - Search summary (timestamp, user prompt, scale)
  - Per-strategy findings (with relevance notes)
  - Aggregated file list (deduplicated with frequency count)
  - Recommendations for next steps

### Task 2: Create Scout Command File
- Create `.claude/commands/scout.md`
- Add command metadata (title, description, purpose)
- Define variables section (USER_PROMPT as $1, SCALE as $2 with default 4)
- Document the command's purpose and usage

### Task 3: Implement Variable Parsing and Validation
- Add Instructions section with variable parsing logic
- Validate USER_PROMPT is provided (required)
- Parse SCALE with default value 4
- Add validation: if SCALE < 2, recommend direct exploration instead
- Add note: SCALE should be kept between 2-6 for reasonable performance

### Task 4: Implement Parallel Exploration Strategy
- Define 4 exploration strategies with specific prompts:
  - Strategy 1 (File Patterns): "Find files matching patterns relevant to: {USER_PROMPT}. Use Glob tool to search for file patterns. Focus on directory structure, naming conventions, and common file locations."
  - Strategy 2 (Content Search): "Search file contents for code relevant to: {USER_PROMPT}. Use Grep tool to search for keywords, function names, class names, and related terms."
  - Strategy 3 (Architecture): "Analyze architectural patterns and module organization relevant to: {USER_PROMPT}. Use Read tool to understand structure, identify key modules, and map relationships."
  - Strategy 4 (Dependencies): "Map dependencies and references relevant to: {USER_PROMPT}. Use Grep to find imports, function calls, and cross-file references."
- Document SCALE behavior: use subset if SCALE < 4, add more granular searches if SCALE > 4

### Task 5: Implement Workflow Section
- Add Workflow section with steps:
  - Step 1: Parse and validate USER_PROMPT and SCALE
  - Step 2: Generate strategy-specific prompts (map strategies to SCALE count)
  - Step 3: Launch parallel Task agents (CRITICAL: all in single message)
  - Step 4: Output progress message to user
  - Step 5: Wait for all agents to complete
  - Step 6: Aggregate results from all agent outputs
  - Step 7: Create deduplicated file list with frequency counts
  - Step 8: Generate output markdown
  - Step 9: Create `agents/scout_files/` directory (mkdir -p)
  - Step 10: Write results to `agents/scout_files/relevant_files_{timestamp}.md`

### Task 6: Implement Output Format
- Define markdown template structure:
```markdown
# Scout Report: {USER_PROMPT}

Generated: {timestamp}
Scale: {SCALE} parallel explorations

## Summary
Brief overview of search scope and approach

## Strategy Results

### Strategy 1: File Pattern Search
**Approach:** {description}
**Files Found:**
- `path/to/file1.py` - relevance note
- `path/to/file2.py` - relevance note

### Strategy 2: Content Search
...

## Aggregated File List
Files sorted by frequency (number of strategies that identified them):

**High Confidence (found by 3+ strategies):**
- `path/to/critical_file.py` [4/4 strategies]

**Medium Confidence (found by 2 strategies):**
- `path/to/related_file.py` [2/4 strategies]

**Low Confidence (found by 1 strategy):**
- `path/to/possible_file.py` [1/4 strategies]

## Recommendations
- Priority files to read: [list high confidence files]
- Suggested next steps: [based on findings]
```

### Task 7: Implement Report Section
- Add Report section that instructs agent to:
  - Show progress message: "Launching {SCALE} parallel exploration agents..."
  - After completion: "Exploration complete. Found {N} relevant files across {SCALE} strategies."
  - Output the final file path: `agents/scout_files/relevant_files_{timestamp}.md`
  - Provide brief summary of findings

### Task 8: Add Usage Examples and Documentation
- Add Examples section showing typical usage:
  - `/scout "add authentication to API endpoints"`
  - `/scout "fix database connection pooling" 6`
  - `/scout "implement caching layer"`
- Add Notes section with:
  - Recommended SCALE values (2-6)
  - Expected execution time considerations
  - How to interpret frequency scores
  - Limitations (read-only, no code modification)

### Task 9: Testing and Validation
- Test command with USER_PROMPT: "implement user authentication"
- Verify SCALE=2 (subset of strategies)
- Verify SCALE=4 (default, all strategies)
- Verify SCALE=6 (should add 2 more granular strategies)
- Verify output file is created in `agents/scout_files/`
- Verify timestamp format is correct (YYYYMMDD_HHMMSS)
- Verify markdown format is readable and well-structured
- Verify frequency scoring works correctly
- Verify parallel execution (all agents in single Task tool call)

### Task 10: Final Integration and Documentation
- Update CLAUDE.md to document the new `/scout` command
- Add to Commands Disponibles section
- Verify command works end-to-end
- Create example output file for reference

## Testing Strategy

### Unit Tests
Since this is a slash command (markdown-based prompt), testing is manual:
- Test variable parsing (USER_PROMPT required, SCALE defaults to 4)
- Test parallel agent launches (verify single message with multiple Task calls)
- Test output file creation and format
- Test SCALE parameter variations (2, 4, 6)
- Test with various USER_PROMPT values

### Integration Tests
- Run full command with real codebase
- Verify agents complete successfully
- Verify output markdown is well-formed
- Verify file paths are valid
- Verify frequency scoring is accurate

### Edge Cases
- USER_PROMPT missing (should show error)
- SCALE = 1 (should recommend direct exploration)
- SCALE > 10 (should cap at 10 or add note)
- No files found by any strategy (should report empty results gracefully)
- One or more agents fail (should report partial results)
- Very long USER_PROMPT (should handle gracefully)
- Special characters in USER_PROMPT (should escape properly)

## Acceptance Criteria

1. **Command Creation**
   - File `.claude/commands/scout.md` exists
   - Command follows standard slash command format with Variables, Instructions, Workflow, Report sections

2. **Functionality**
   - Command accepts USER_PROMPT as required parameter
   - Command accepts optional SCALE parameter (defaults to 4)
   - Command launches SCALE number of Task agents with Explore subagent_type in parallel (single message)
   - Each agent uses distinct exploration strategy

3. **Output Generation**
   - Output directory `agents/scout_files/` is created automatically
   - Output file is named `relevant_files_{timestamp}.md` with timestamp format YYYYMMDD_HHMMSS
   - Output markdown contains all required sections:
     - Search summary
     - Per-strategy results
     - Aggregated file list with frequency counts
     - Recommendations

4. **User Experience**
   - Command provides progress feedback during execution
   - Command reports completion with summary
   - Output is human-readable and actionable

5. **Documentation**
   - Command includes usage examples
   - Command includes notes on SCALE recommendations
   - CLAUDE.md is updated to list the new command

6. **Robustness**
   - Handles missing USER_PROMPT gracefully
   - Handles invalid SCALE values gracefully
   - Handles partial agent failures (some agents fail, others succeed)
   - Handles no files found scenario

## Validation Commands

Since this is a slash command template (not executable code), validation is manual:

1. **Manual Testing**
   - Run `/scout "implement authentication"` in a Claude Code session
   - Verify parallel agents launch
   - Verify output file is created in `agents/scout_files/`
   - Verify markdown format and content quality

2. **Code Quality**
   - Review `.claude/commands/scout.md` for completeness
   - Verify all required sections are present
   - Verify instructions are clear and actionable
   - Verify examples are helpful

3. **Integration Check**
   - Verify command is listed in CLAUDE.md
   - Verify command follows patterns from other commands (parallel_subagents, feature, etc.)
   - Verify no conflicts with existing commands

## Notes

### Implementation Approach
This command does NOT require external CLI tools (gemini, opencode, codex, claude). Instead, it uses Claude Code's built-in Task tool with Explore subagent_type, which provides robust codebase exploration using Glob, Grep, and Read tools.

### No Git Safety Checks Needed
The Explore agent is read-only by design. No git diff/reset is needed as no files will be modified.

### Timestamp Format
Using YYYYMMDD_HHMMSS format for unique IDs provides human-readable, sortable timestamps without needing UUID libraries.

### Frequency-Based Relevance
Files found by multiple independent search strategies are more likely to be truly relevant. This heuristic helps prioritize which files to read first.

### SCALE Flexibility
- SCALE < 4: Use subset of strategies (prioritize file patterns and content search)
- SCALE = 4: Use all 4 core strategies (default)
- SCALE > 4: Add more granular strategies (e.g., split content search into multiple keyword groups, add test file search, add config file search)

### Command Pattern
This command follows the TAC-10 Level 4 (Delegation Prompt) pattern similar to `/parallel_subagents`, but specialized for codebase exploration rather than general task decomposition.

### Future Enhancements
- Add caching of exploration results to avoid re-exploring same prompts
- Add support for excluding directories (e.g., node_modules, .git)
- Add support for filtering by file type
- Add support for outputting results in JSON format for programmatic consumption
- Add integration with other commands (e.g., auto-feed results to /implement)
