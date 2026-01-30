# Find and Summarize

Find files matching a glob pattern and generate an AI-powered summary of their contents. Based on the `Instructions` below, take the `Variables`, follow the `Workflow` section to discover and analyze files, and then follow the `Report` section to report the results.

## Variables

PATTERN: $1 (required - glob pattern to search for files, e.g., "**/*.py", "src/**/service.ts")
FOCUS: $2 (optional - specific aspect to focus the summary on, e.g., "authentication logic", "error handling")

## Instructions

This command provides a lightweight, targeted file discovery and summarization capability. It accepts a glob pattern, finds matching files, reads them, and generates a comprehensive AI summary highlighting key findings, file purposes, and relationships.

### Purpose

The `/find_and_summarize` command helps you quickly understand groups of files by:
- Finding files that match a specific glob pattern
- Reading the content of discovered files (with reasonable limits)
- Generating a single, structured markdown summary
- Highlighting key patterns, relationships, and insights
- Providing a faster alternative to comprehensive exploration tools

### When to Use This Command

Use `/find_and_summarize` when:
- You know the file pattern you want to examine (e.g., all Python files, specific directory)
- You need a quick overview of what a set of files contains
- You want to understand the purpose and relationships of multiple files
- You're exploring a new area of the codebase with a targeted scope
- You need a simple, fast summary without heavyweight exploration

### When NOT to Use This Command

Do NOT use `/find_and_summarize` when:
- You need comprehensive multi-strategy exploration (use `/scout` instead)
- You already know the exact file and just need to read it (use Read tool directly)
- You need to execute code or run tests (use appropriate execution tools)
- The pattern would match hundreds of files (results would be too large)
- You need confidence scoring or frequency analysis across strategies

### How It Works

1. **Find**: Uses Glob tool to discover files matching the pattern
2. **Read**: Reads the content of relevant files (suggests limiting to ~20 files)
3. **Summarize**: Generates a structured markdown summary with:
   - Files found (count and list)
   - Summary of contents (aggregate overview)
   - Key findings (patterns, relationships, insights)

### Relationship to Other Commands

- **vs /scout**: `/scout` is comprehensive with parallel strategies and confidence scoring; `/find_and_summarize` is simpler and faster for known patterns
- **vs Read tool**: Read tool shows one file; `/find_and_summarize` summarizes multiple files
- **vs Grep/Glob**: Grep/Glob find files; `/find_and_summarize` finds AND explains them

## Workflow

### Step 1: Validate Input

- Extract PATTERN from $1
- If PATTERN is missing or empty: abort with error message explaining usage
- Extract optional FOCUS from $2 (can be empty)
- Validate that PATTERN is a reasonable glob pattern (contains wildcards or specific file references)

### Step 2: Find Files Using Glob

- Use Glob tool with the provided PATTERN
- If Glob fails: report error and suggest pattern corrections
- Count the number of files found
- If no files found: skip to Step 6 (report no matches)
- If files found: proceed to Step 3

### Step 3: Evaluate File Count

- If 1-20 files found: proceed to read all files
- If 21-50 files found: suggest reading first 20, warn user about large result set
- If >50 files found: suggest reading first 20, strongly recommend refining the pattern or using more specific filters

### Step 4: Read Files

- Use Read tool to read the content of files (up to ~20 files suggested)
- For each file:
  - Read the full content (respecting Read tool's default 2000-line limit)
  - Track which files were successfully read
  - Track which files failed to read (permissions, binary files, etc.)
- Handle read failures gracefully (note them but continue with successful reads)

### Step 5: Generate Summary

Analyze the read files and create a structured markdown summary with these sections:

**Files Found Section:**
- Total count of files matching the pattern
- List of all matched file paths (grouped by directory if helpful)
- Note any files that couldn't be read

**Summary of Contents Section:**
- Aggregate overview of what the files contain
- Common themes, purposes, or responsibilities
- If FOCUS parameter provided: emphasize aspects related to the focus area
- Technology stack, frameworks, or patterns identified
- Relationships between files (imports, dependencies, shared concepts)

**Key Findings Section:**
- Important patterns observed across files
- Notable implementations or approaches
- Potential concerns or areas of interest
- Architectural insights or design patterns
- Suggestions for further exploration if relevant

### Step 6: Handle Edge Cases

**No Files Found:**
- Provide friendly message explaining no matches
- Suggest refining the pattern
- Offer example patterns that might work better

**Pattern Too Broad:**
- If >50 files match, warn about result size
- Suggest more specific patterns
- Still provide summary of first ~20 files

**Read Failures:**
- Note which files couldn't be read and why
- Continue with successfully read files
- Include failed files in the report

## Report

After completing the workflow, output a markdown report with this structure:

```markdown
# Find and Summarize Report

**Pattern:** `{PATTERN}`
**Focus:** {FOCUS or "General overview"}
**Files Matched:** {count}
**Files Read:** {count}

---

## Files Found

{List all matched files, grouped by directory if helpful:}

- `path/to/file1.py`
- `path/to/file2.py`
- `another/path/file3.ts`

{If any files failed to read:}

**Could not read:**
- `binary/file.dat` - Binary file
- `restricted/file.txt` - Permission denied

---

## Summary of Contents

{Aggregate overview of what the files contain, written in narrative form}

{If FOCUS provided, emphasize relevant aspects}

Key characteristics:
- {Characteristic 1}
- {Characteristic 2}
- {Characteristic 3}

---

## Key Findings

### Patterns and Relationships

{Description of patterns observed across files}

### Notable Implementations

{Interesting or important code/approaches found}

### Architectural Insights

{Understanding of how files fit together, design patterns}

### Recommendations

{Suggestions for further exploration, potential concerns, or next steps}

---

*Generated by /find_and_summarize command*
```

If no files were found:

```markdown
# Find and Summarize Report

**Pattern:** `{PATTERN}`
**Files Matched:** 0

---

## No Files Found

No files matched the pattern `{PATTERN}`.

### Suggestions

- Check that the pattern is correct (wildcards: `*`, `**`, `?`)
- Verify you're in the correct directory
- Try a broader pattern: `**/{filename}` searches recursively
- Example patterns:
  - `**/*.py` - All Python files recursively
  - `src/**/*.ts` - TypeScript files in src/
  - `*.md` - Markdown files in current directory

---

*Generated by /find_and_summarize command*
```

## Examples

### Example 1: Find All Python Files

```
/find_and_summarize "**/*.py"
```

Finds all Python files in the codebase and provides a summary of their purposes and relationships.

### Example 2: Find Services with Focus

```
/find_and_summarize "src/**/service.ts" "focusing on authentication logic"
```

Finds all TypeScript service files in the src directory and emphasizes authentication-related code in the summary.

### Example 3: Find Markdown Documentation

```
/find_and_summarize "docs/**/*.md"
```

Finds all markdown files in the docs directory and summarizes the documentation structure and content.

### Example 4: Find Configuration Files

```
/find_and_summarize "*.{json,yaml,yml,toml}"
```

Finds configuration files in the current directory and summarizes their purposes and settings.

### Example 5: Find Test Files

```
/find_and_summarize "**/*test*.py" "test coverage for authentication"
```

Finds Python test files and focuses the summary on authentication test coverage.

## Notes

### Limitations

- **Read-only**: This command only reads files, it does not modify them
- **No execution**: Code is not executed, only analyzed statically
- **Suggested limit**: Reading ~20 files is suggested to avoid token overuse, but agent decides based on context
- **Large files**: Read tool's 2000-line default limit applies (can be adjusted if needed)
- **Binary files**: Cannot read binary files (images, compiled code, etc.)

### Best Practices

1. **Be specific with patterns**: `src/**/*.service.ts` is better than `**/*.ts`
2. **Use focus for targeted summaries**: Add a focus parameter when looking for specific aspects
3. **Refine broad patterns**: If you get too many files, narrow the pattern
4. **Combine with other tools**: Use `/find_and_summarize` for overview, then Read specific files for details
5. **Check directories first**: Use `ls` or Glob to understand structure before searching

### Pattern Syntax

Glob patterns support:
- `*` - Matches any characters except directory separator (e.g., `*.py`)
- `**` - Matches any characters including directory separators (e.g., `**/*.py`)
- `?` - Matches single character (e.g., `file?.txt`)
- `{a,b}` - Matches either a or b (e.g., `*.{js,ts}`)
- `[abc]` - Matches any character in brackets (e.g., `file[123].txt`)

### Integration with Other Commands

**After /find_and_summarize:**
- Use Read tool to examine specific files in detail
- Use `/scout` for comprehensive multi-strategy exploration
- Use `/feature` or `/implement` to plan work on discovered files
- Use Grep to search for specific content within the files

**Before /find_and_summarize:**
- Use `ls` or Glob to understand directory structure
- Use `/scout` if you don't know what pattern to search for
- Use Read on README or documentation to understand codebase organization

### Performance Considerations

- **1-10 files**: Very fast, seconds
- **11-20 files**: Fast, under a minute
- **21-50 files**: Moderate, may take 1-2 minutes
- **>50 files**: Slow, consider refining pattern or using first 20 only

Actual time depends on file sizes and content complexity.

### Future Enhancements

Potential improvements for future iterations:
- Add explicit `--max-files` parameter to override suggested limit
- Support `--exclude` patterns to filter out files (e.g., exclude tests)
- Option to save summary to a file vs. inline output
- Support for sorting files by different criteria (size, modification time)
- Integration with `/scout` results for targeted follow-up
- JSON output format for programmatic consumption

---

*This command provides lightweight file discovery and AI-powered summarization for targeted codebase exploration.*
