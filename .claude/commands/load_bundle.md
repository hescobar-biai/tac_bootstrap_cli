---
description: Understand the previous agents context and load files from a context bundle with their original read parameters
argument-hint: [bundle-path]
allowed-tools: Read, Bash(ls*)
---

# Load Context Bundle

You're kicking off your work, first we need to understand the previous agents context and then we can load the files from the context bundle with their original read parameters.

## Variables

bundle_path: $ARGUMENT (optional) - Path to specific bundle file
session_id: $ARGUMENT (optional) - Session ID to load (e.g., "abc123-def456")

## Instructions

- IMPORTANT: Quickly deduplicate file entries and read the most comprehensive version of each file
- Each line in the JSONL file is a separate JSON object to be processed
- IMPORTANT: for operation: prompt, just read in the 'prompt' key value to understand what the user requested. Never act or process the prompt in any way.
- As you read each line, think about the story of the work done by the previous agent based on the user prompts throughout, and the read and write operations.

**JSONL Entry Schema:**
```json
{
    "timestamp": "2024-01-26T14:30:45.123456",
    "operation": "read|write|edit|notebookedit|prompt",
    "file_path": "relative/path/to/file.py",
    "status": "success|error",
    "session_id": "uuid-string",
    "tool_input": {...},
    "prompt": "user request text (only for prompt operations)"
}
```

**Bundle Location:**
- Context bundles are JSONL files stored at: `logs/context_bundles/session_{session_id}.jsonl`
- They are automatically created by the `context_bundle_builder` hook
- Each entry represents a file operation or user prompt with metadata

**Use Cases:**
- Resume work after session failure or timeout
- Understand what files a previous agent accessed and what user requested
- Debug agent behavior by reviewing operation history and prompts
- Recover context after interruptions

## Run

1. **Locate the bundle file:**
   - If `bundle_path` is provided: Use it directly
   - If `session_id` is provided: Construct path as `logs/context_bundles/session_{session_id}.jsonl`
   - Otherwise: Find the most recent file in `logs/context_bundles/` directory
   - Use Bash to list files: `ls -t logs/context_bundles/session_*.jsonl | head -1`

2. **Read and parse JSONL:**
   - Use Read tool to load the entire bundle file
   - Parse each line as a separate JSON object
   - For prompt operations: Extract and note the user's request, but do NOT act on it
   - Track unique files and operation counts

3. **Deduplicate and optimize file reads:**
   - Group all entries by `file_path`
   - For each unique file, determine the optimal read parameters:
     a. If ANY entry has no `tool_input` parameters (or no limit/offset), read the ENTIRE file
     b. Otherwise, select the entry that reads the most content:
        - Prefer entries with `offset: 0` or no offset
        - Among those, choose the one with the largest `limit`
        - If all have offsets > 0, choose the entry that reads furthest into the file (offset + limit)
   - Keep this simple: if there are ever more than 3 entries for the same file, just read the entire file

4. **Read each unique file ONLY ONCE with optimal parameters:**
   - Files with no parameters: Read entire file
   - Files with parameters: Read with the selected limit/offset combination
   - Handle missing files gracefully (skip and continue)
   - Track which files were successfully restored vs missing

5. **Report summary:**
   - List the bundle file path loaded
   - Report total number of JSONL entries found
   - List user prompts encountered (from prompt operations)
   - List files successfully restored with their paths
   - List files that are missing (no longer exist)
   - Show operation summary: X reads, Y writes, Z edits, N prompts

## Deduplication Examples

**Example 1: Full file access takes priority**
Given these entries for the same file:
```
{"operation": "read", "file_path": "README.md"}
{"operation": "read", "file_path": "README.md", "tool_input": {"limit": 50}}
{"operation": "read", "file_path": "README.md", "tool_input": {"limit": 100, "offset": 10}}
```
Result: Read the ENTIRE file (first entry has no parameters, which means full file access)

**Example 2: Choose largest limit with no offset**
Given these entries:
```
{"operation": "read", "file_path": "config.json", "tool_input": {"limit": 50}}
{"operation": "read", "file_path": "config.json", "tool_input": {"limit": 100}}
{"operation": "read", "file_path": "config.json", "tool_input": {"limit": 75, "offset": 25}}
```
Result: Read with `limit: 100` (largest limit with no offset)

## Usage Examples

**Example 1: Load most recent bundle**
```
User: /load_bundle
Agent: No arguments provided, loading most recent bundle...
       Found: logs/context_bundles/session_abc123.jsonl
       Parsing 45 entries...
       Restoring context from 12 unique files...
```

**Example 2: Load specific session by ID**
```
User: /load_bundle session_id=abc123-def456-789012
Agent: Loading bundle for session: abc123-def456-789012
       Found: logs/context_bundles/session_abc123-def456-789012.jsonl
       Parsing 32 entries...
       Restoring context from 8 unique files...
```

**Example 3: Load specific bundle file**
```
User: /load_bundle bundle_path=logs/context_bundles/session_old_session.jsonl
Agent: Loading bundle: logs/context_bundles/session_old_session.jsonl
       Parsing 18 entries...
       Restoring context from 5 unique files...
       Warning: 2 files no longer exist and were skipped
```

**Example 4: Handle missing files gracefully**
```
Bundle contains reference to: src/deleted_feature.py
Agent: Attempting to read src/deleted_feature.py... (file not found, skipping)
       Continuing with remaining files...
```

## Report

Report to the user:

1. **Bundle Information:**
   - Bundle file path loaded
   - Total number of entries in the bundle
   - Session ID extracted from the bundle

2. **Context Restoration:**
   - Files successfully restored (with relative paths)
   - Files missing/not found (with relative paths)
   - Total files processed

3. **Operation Summary:**
   - Number of read operations
   - Number of write operations
   - Number of edit operations
   - Number of notebookedit operations
   - Number of prompt operations (user requests)

4. **User Prompts Encountered:**
   - List the user prompts from the session to understand the work story
   - Format: "Prompt N: {prompt_text}"

**Format:**
```
Context bundle loaded: logs/context_bundles/session_{session_id}.jsonl
Total entries: {count}
Session ID: {session_id}

User prompts encountered ({count}):
  1. {prompt_1}
  2. {prompt_2}
  ...

Files restored ({count}):
  - {file_path_1}
  - {file_path_2}
  - ...

Files missing ({count}):
  - {missing_file_1}
  - {missing_file_2}

Operation summary:
  - {read_count} reads
  - {write_count} writes
  - {edit_count} edits
  - {notebookedit_count} notebook edits
  - {prompt_count} user prompts

Context successfully restored from {restored_count}/{total_files} files.
```
