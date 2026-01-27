# Scout - Parallel Codebase Exploration

Intelligently explore the codebase to identify relevant files for a given task using parallel search strategies. Based on the `Instructions` below, take the `Variables`, follow the `Workflow` section to launch parallel exploration agents, and then follow the `Report` section to report the results.

## Variables

USER_PROMPT: $1 (required - task description for file search)
SCALE: $2 (optional - number of parallel strategies, default: 4, range: 2-10)

## Instructions

This command implements TAC-10 Level 4 (Delegation Prompt) pattern specialized for codebase exploration. It launches multiple parallel exploration agents using different search strategies to maximize file discovery coverage.

### Purpose

The `/scout` command helps you quickly identify all files relevant to a specific task by:
- Running multiple independent search strategies in parallel
- Aggregating results with frequency-based relevance scoring
- Providing a structured report for easy review and action
- Using read-only exploration (no code modifications)

### When to Use This Command

Use `/scout` when:
- Starting work on a new feature or bug fix in an unfamiliar codebase
- You need to understand the scope of changes required
- You want to identify all potentially affected files before implementation
- You're planning a refactoring or architectural change
- You need to map dependencies and relationships for a specific concern

### When NOT to Use This Command

Do NOT use `/scout` when:
- You already know exactly which files to work with
- The task is trivial (single file, obvious location)
- You need to execute code or run tests (use appropriate tools instead)
- You're looking for a specific needle query (use Grep/Glob directly)

### Search Strategies

The command uses these core strategies (when SCALE=4):

1. **File Pattern Search**: Glob-based discovery using naming conventions and directory structure
2. **Content Search**: Grep-based discovery using keywords, function names, and class names
3. **Architectural Analysis**: Structure understanding through Read tool to map modules and relationships
4. **Dependency Mapping**: Finding imports, function calls, and cross-file references

### SCALE Parameter Behavior

- **SCALE < 2**: Error - recommend using direct exploration instead
- **SCALE = 2**: Use file patterns + content search (fastest)
- **SCALE = 3**: Add architectural analysis
- **SCALE = 4**: Use all 4 core strategies (default, recommended)
- **SCALE = 5-6**: Add granular strategies (test files, config files, type definitions)
- **SCALE > 6**: Add more specialized searches (documentation, migrations, API schemas)
- **SCALE > 10**: Cap at 10 and warn about resource constraints

## Workflow

### Step 1: Parse and Validate Input

- Extract USER_PROMPT from $1
- If USER_PROMPT is missing: abort with error message
- Extract SCALE from $2, default to 4 if not provided
- Validate SCALE:
  - If SCALE < 2: abort with error recommending direct exploration
  - If SCALE > 10: cap at 10 and warn user
  - Valid range: 2-10

### Step 2: Generate Strategy-Specific Prompts

Based on SCALE value, create distinct exploration prompts:

**Strategy 1 (File Patterns) - Always included:**
```
Find files matching patterns relevant to: {USER_PROMPT}

Use Glob tool to search for file patterns based on:
- Common naming conventions (e.g., *_test.py, *Service.ts, *Controller.java)
- Directory structure and organization
- File type patterns relevant to the task

Focus on discovering files by their location and naming, not content.
List all matching files with brief relevance notes.
```

**Strategy 2 (Content Search) - Always included:**
```
Search file contents for code relevant to: {USER_PROMPT}

Use Grep tool to search for:
- Keywords from the task description
- Function names, class names, method names
- Variable names, constants, configuration keys
- Comments or documentation mentioning related concepts

Use output_mode: "files_with_matches" to get file paths.
For important matches, use -A/-B flags to show context.
List all matching files with brief relevance notes.
```

**Strategy 3 (Architecture) - Included if SCALE >= 3:**
```
Analyze architectural patterns and module organization relevant to: {USER_PROMPT}

Use Read tool to:
- Understand project structure (read top-level directories, README, package.json, etc.)
- Identify key modules and their responsibilities
- Map architectural layers (domain, application, infrastructure, etc.)
- Find entry points and main orchestration files

Focus on understanding how the codebase is organized and which modules handle the concern.
List all relevant files with architectural context.
```

**Strategy 4 (Dependencies) - Included if SCALE >= 4:**
```
Map dependencies and references relevant to: {USER_PROMPT}

Use Grep tool to find:
- Import statements (import, require, use, include)
- Function calls and method invocations
- Class instantiations and inheritance
- Cross-file references and dependencies

Trace both forward dependencies (what this imports) and backward dependencies (what imports this).
List all relevant files with dependency relationship notes.
```

**Strategy 5 (Test Files) - Included if SCALE >= 5:**
```
Find test files and test-related code relevant to: {USER_PROMPT}

Use Glob and Grep to search for:
- Test files (patterns: *test*, *spec*, __tests__/, tests/)
- Test utilities, fixtures, mocks
- Integration tests, E2E tests, unit tests

List all test files that would need to be updated or consulted.
```

**Strategy 6 (Configuration) - Included if SCALE >= 6:**
```
Find configuration files and settings relevant to: {USER_PROMPT}

Use Glob and Grep to search for:
- Config files (*.json, *.yaml, *.toml, *.ini, .env)
- Settings modules, constants files
- Environment-specific configurations
- Build configurations, deployment configs

List all configuration files that might need updates.
```

**Strategy 7 (Type Definitions) - Included if SCALE >= 7:**
```
Find type definitions, interfaces, and schemas relevant to: {USER_PROMPT}

Use Grep to search for:
- Type definitions (type, interface, schema)
- Data models, DTOs, entities
- API contracts, GraphQL schemas
- Protocol definitions

List all files defining types that relate to the task.
```

**Strategy 8 (Documentation) - Included if SCALE >= 8:**
```
Find documentation and comments relevant to: {USER_PROMPT}

Use Grep to search for:
- Markdown documentation files
- Inline code comments discussing the topic
- README files in relevant subdirectories
- API documentation, architecture decision records

List all documentation files that provide context.
```

**Strategy 9+ (Specialized) - Included if SCALE >= 9:**
Add more specialized searches based on common patterns:
- Database migrations and schema files
- API route definitions and controllers
- Frontend component files
- Build and deployment scripts

### Step 3: Launch Parallel Exploration Agents

- Create a single message with SCALE Task tool invocations
- CRITICAL: All agents must be launched in parallel (single message with multiple tool calls)
- For each agent (1 to SCALE):
  - Use `subagent_type: "Explore"`
  - Set `prompt` to the corresponding strategy prompt with USER_PROMPT interpolated
  - Set `description` to strategy name (e.g., "File Pattern Search", "Content Search")
  - Set `model: "haiku"` for faster execution (exploration is straightforward)
  - Set thoroughness level: "medium" (balance between speed and completeness)

### Step 4: Output Progress Message

Immediately after launching agents, output to user:
```
Launching {SCALE} parallel exploration agents to find files relevant to: "{USER_PROMPT}"

Strategies:
- Strategy 1: File Pattern Search
- Strategy 2: Content Search
- Strategy 3: Architectural Analysis (if SCALE >= 3)
- Strategy 4: Dependency Mapping (if SCALE >= 4)
- Strategy 5: Test Files (if SCALE >= 5)
- Strategy 6: Configuration (if SCALE >= 6)
- ... (list all active strategies)

This will take a moment as agents explore the codebase in parallel...
```

### Step 5: Wait for Agent Completion

- Wait for all Task agents to complete
- Handle partial failures gracefully:
  - If 1-2 agents fail: continue with successful results, note which strategies failed
  - If majority fail: report pattern and suggest alternative approach
  - If all fail: identify root cause and recommend manual exploration

### Step 6: Aggregate Results

For each successful agent:
- Parse the agent's output to extract file paths mentioned
- Extract relevance notes or context for each file
- Store files in a map with: file_path -> [strategy_names, relevance_notes]

### Step 7: Create Deduplicated File List with Frequency Scoring

- Build a master list of all unique file paths
- For each file, count how many strategies found it (frequency score)
- Sort files by frequency (descending), then alphabetically
- Group files by confidence level:
  - High Confidence: found by (SCALE * 0.75) or more strategies
  - Medium Confidence: found by (SCALE * 0.4) to (SCALE * 0.74) strategies
  - Low Confidence: found by fewer than (SCALE * 0.4) strategies

### Step 8: Generate Output Markdown

Create markdown content with this structure:

```markdown
# Scout Report: {USER_PROMPT}

**Generated:** {timestamp in YYYY-MM-DD HH:MM:SS format}
**Scale:** {SCALE} parallel exploration strategies
**Status:** {X} of {SCALE} strategies completed successfully

---

## Summary

Explored the codebase using {SCALE} parallel search strategies to identify files relevant to: "{USER_PROMPT}"

{Brief overview of what was found - e.g., "Found {N} unique files across {M} successful strategies. High-confidence files indicate strong relevance."}

---

## Strategy Results

### Strategy 1: File Pattern Search
**Status:** {Success | Failed: reason}
**Files Found:** {count}

{If successful, list files with brief notes:}
- `path/to/file1.py` - {relevance note from agent}
- `path/to/file2.ts` - {relevance note from agent}

### Strategy 2: Content Search
**Status:** {Success | Failed: reason}
**Files Found:** {count}

{List files...}

### Strategy 3: Architectural Analysis
{Include if SCALE >= 3}

### Strategy 4: Dependency Mapping
{Include if SCALE >= 4}

{Continue for all strategies...}

---

## Aggregated File List

Total unique files discovered: {N}

### High Confidence (found by {threshold}+ strategies)

- `path/to/critical_file.py` **[{X}/{SCALE} strategies]**
  - Found by: Strategy 1, Strategy 2, Strategy 4
  - Relevance: {synthesized note from all strategies}

- `path/to/another_critical_file.ts` **[{X}/{SCALE} strategies]**
  - Found by: Strategy 1, Strategy 3
  - Relevance: {synthesized note}

### Medium Confidence (found by {threshold_min}-{threshold_max} strategies)

- `path/to/related_file.py` **[{X}/{SCALE} strategies]**
  - Found by: Strategy 2
  - Relevance: {note}

### Low Confidence (found by <{threshold} strategies)

- `path/to/possible_file.py` **[1/{SCALE} strategies]**
  - Found by: Strategy 3
  - Relevance: {note}

---

## Recommendations

### Priority Files to Read
{List high-confidence files that should be read first}

1. `path/to/critical_file.py` - {reason}
2. `path/to/another_critical_file.ts` - {reason}

### Suggested Next Steps

{Based on findings, suggest concrete next actions, e.g.:}
- Read the high-confidence files to understand current implementation
- Check test files to understand expected behavior
- Review configuration files for relevant settings
- Consider which files will need modifications
- Identify files that should be added to .gitignore if they don't exist

### Potential Gaps

{If certain types of files weren't found, note them:}
- No test files found for this concern (may need to create)
- No configuration files found (may need to add settings)
- No documentation found (may need to document)

---

## Execution Details

**Failed Strategies:** {count}
{If any failed, list them with error messages}

**Execution Time:** {duration if available}
**Output Path:** `agents/scout_files/relevant_files_{timestamp}.md`

---

*Generated by /scout command using parallel codebase exploration*
```

### Step 9: Create Output Directory

- Use Bash tool: `mkdir -p agents/scout_files`
- This ensures the directory exists without error if already present

### Step 10: Write Results to File

- Generate timestamp in format: YYYYMMDD_HHMMSS
- Create filename: `agents/scout_files/relevant_files_{timestamp}.md`
- Use Write tool to create the file with the generated markdown content
- Return the file path to user

## Report

After completing the workflow, report to the user:

```markdown
## Scout Exploration Complete

**Task:** {USER_PROMPT}
**Strategies:** {SCALE} parallel explorations
**Status:** {successful_count} of {SCALE} strategies completed

### Results Summary

- **Total files found:** {total_unique_files}
- **High confidence:** {high_confidence_count} files (found by {threshold}+ strategies)
- **Medium confidence:** {medium_confidence_count} files
- **Low confidence:** {low_confidence_count} files

### Priority Files

{List top 5 high-confidence files}

### Output Report

Full detailed report saved to:
**`agents/scout_files/relevant_files_{timestamp}.md`**

### Next Steps

{Provide 2-3 concrete next steps based on findings}
```

If there were failures:
```
⚠️ **Note:** {failed_count} strategies failed to complete. Results may be incomplete.
Failed strategies: {list failed strategy names}
```

If no files were found:
```
⚠️ **No files found** matching the search criteria across any strategy.
This could mean:
- The task description is too vague or uses unfamiliar terminology
- The codebase doesn't yet have code related to this concern
- Try refining your USER_PROMPT with more specific keywords or concepts
```

## Examples

### Example 1: Basic Usage (Default Scale)
```
/scout "add authentication to API endpoints"
```
Launches 4 strategies (file patterns, content search, architecture, dependencies) to find all files related to authentication and API endpoints.

### Example 2: Thorough Exploration
```
/scout "implement caching layer" 6
```
Launches 6 strategies including test files and configuration to get comprehensive coverage.

### Example 3: Quick Exploration
```
/scout "fix database connection pooling" 2
```
Launches only 2 strategies (file patterns and content search) for faster results.

### Example 4: Complex Feature
```
/scout "migrate from REST API to GraphQL" 8
```
Launches 8 strategies including documentation to understand full scope of migration.

## Notes

### Performance Considerations

- **SCALE=2-3**: Fast (~30-60 seconds), good for quick orientation
- **SCALE=4** (default): Balanced (~1-2 minutes), recommended for most tasks
- **SCALE=5-6**: Thorough (~2-3 minutes), good for complex features
- **SCALE=7-10**: Comprehensive (~3-5 minutes), use when you need complete coverage

Actual time depends on codebase size and complexity.

### Interpreting Frequency Scores

Files found by multiple independent strategies are more likely to be truly relevant:
- **High confidence (75%+ strategies)**: Almost certainly needs to be read/modified
- **Medium confidence (40-74% strategies)**: Probably relevant, worth reviewing
- **Low confidence (<40% strategies)**: Possibly relevant, review if high-priority files aren't sufficient

### Limitations

- Read-only exploration (no code execution or modification)
- May miss files that are only dynamically referenced
- Performance depends on codebase size (large repos take longer)
- Requires clear, specific task descriptions for best results
- Does not understand runtime behavior or execution paths

### Best Practices

1. **Be specific in USER_PROMPT**: "add JWT authentication to user login endpoint" is better than "add auth"
2. **Use appropriate SCALE**: Start with default (4), increase if results incomplete
3. **Review high-confidence files first**: These are most likely to be relevant
4. **Cross-reference strategies**: If a file appears in multiple strategies, understand why
5. **Check for gaps**: Note what types of files are missing (tests, configs, docs)

### Integration with Other Commands

After running `/scout`, you can:
- Use `/feature` to plan implementation based on discovered files
- Use `/implement` to execute changes on identified files
- Use `/review` to validate changes across all affected files
- Manually read high-confidence files to understand implementation

### Troubleshooting

**Problem:** No files found
- **Solution:** Refine USER_PROMPT with more specific keywords, technology names, or domain concepts

**Problem:** Too many files found (hundreds)
- **Solution:** Be more specific in USER_PROMPT, or focus on highest-confidence files only

**Problem:** Some strategies fail
- **Solution:** Review failure messages, may indicate codebase structure issues or need different search approach

**Problem:** Irrelevant files in results
- **Solution:** Focus on high-confidence files, ignore low-confidence results, refine USER_PROMPT

### Future Enhancements

Potential improvements for future versions:
- Cache exploration results to avoid re-exploring same prompts
- Support for excluding directories (node_modules, .git, vendor)
- Support for filtering by file type or size
- JSON output format for programmatic consumption
- Integration with /implement to auto-feed discovered files
- Learning from user feedback (which files were actually useful)

---

*This command follows TAC-10 Level 4 (Delegation Prompt) pattern for parallel compute orchestration, specialized for codebase exploration.*
