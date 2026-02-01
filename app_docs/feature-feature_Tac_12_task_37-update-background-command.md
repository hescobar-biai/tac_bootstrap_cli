---
doc_type: feature
adw_id: feature_Tac_12_task_37
date: 2026-01-31
idk:
  - background-command-execution
  - cli-automation
  - structured-reporting
  - bash-scripting
  - claude-integration
  - status-tracking
  - task-delegation
tags:
  - feature
  - cli
  - automation
  - documentation
related_code:
  - .claude/commands/background.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2
---

# Background Command Execution with TAC-12 Improvements

**ADW ID:** feature_Tac_12_task_37
**Date:** 2026-01-31
**Specification:** issue-489-adw-feature_Tac_12_task_37-sdlc_planner-update-background-command.md

## Overview

Replaced abstract Task Tool documentation with a concrete TAC-12 implementation for background command execution. The new documentation teaches users how to execute user prompts in the background using the `claude` CLI directly, with structured reporting, automatic status tracking, and comprehensive security guidance.

## What Was Built

The feature transforms the background command documentation from theoretical Task Tool concepts to practical bash-based automation with:

- Direct `claude` CLI invocation using `--dangerously-skip-permissions` flag
- Structured markdown report generation with timestamps and metadata
- Automatic file status renaming (`.complete.md` for success, `.failed.md` for failure)
- Clear security warnings about permission bypass implications
- Project-agnostic base documentation using shell variables ($1, $2, $3)
- Project-specific Jinja2 templating for generated projects
- Three practical examples covering different use cases
- Comprehensive directory structure and error handling documentation

## Technical Implementation

### Files Modified

- `.claude/commands/background.md`: Complete replacement with bash-based `claude` CLI implementation using shell variables
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2`: Template version with Jinja2 parameterization for `config.directories.agents`

### Key Changes

1. **Variable System**: Replaced Task Tool abstraction with explicit shell variables
   - `USER_PROMPT` ($1): The prompt/command to execute
   - `MODEL` ($2): Claude model selection (haiku/sonnet/opus) with sonnet default
   - `REPORT_FILE` ($3): Output file path for structured reports

2. **CLI Integration**: Direct `claude` CLI invocation with:
   - `--dangerously-skip-permissions` flag for full project access
   - `--append-system-prompt` for system context inclusion
   - Exit code capture for status determination (0 = success, non-zero = failure)

3. **Structured Reporting**: Timestamped markdown reports with:
   - Task metadata section (started time, model used, timestamp)
   - Original user prompt in code block
   - Full execution results from claude CLI
   - Completion status and exit code footer

4. **Status Tracking**: Automatic file renaming based on execution:
   - Success (exit code 0) → `.complete.md` extension
   - Failure (non-zero exit) → `.failed.md` extension
   - Fallback logging if rename operation fails

5. **Template Parameterization**: Jinja2 variables in template file:
   - `{{ config.directories.agents }}` for agent directory paths
   - Maintains shell variables as-is (not templated)
   - Clean separation between template-time and runtime variables

### Implementation Details

The bash script includes:
- Directory creation with `mkdir -p agents/background/`
- Timestamp generation: `TIMESTAMP=$(date +%a_%H_%M_%S)`
- Grouped output redirection: `{ ... } > "$REPORT_FILE" 2>&1`
- Exit code capture and conditional renaming logic
- Error handling with `2>/dev/null` and fallback append logic

## How to Use

### Basic Execution

1. Create the `agents/background/` directory:
   ```bash
   mkdir -p agents/background/
   ```

2. Execute a background task with a prompt:
   ```bash
   .claude/commands/background.md "Your analysis prompt here" "sonnet" "agents/background/task_report.md"
   ```

3. Monitor the report file:
   ```bash
   tail -f agents/background/task_report*.md
   ```

### Use Cases

**Complex Architecture Analysis**
```bash
USER_PROMPT="Analyze the authentication system architecture and identify security gaps"
MODEL="sonnet"
REPORT_FILE="agents/background/auth_security_review.md"
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

**API Documentation Generation**
```bash
USER_PROMPT="Review all API endpoints in src/api/ and generate comprehensive documentation"
MODEL="haiku"
REPORT_FILE="agents/background/api_docs_generation.md"
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

**Codebase Refactoring Analysis**
```bash
USER_PROMPT="Identify all occurrences of deprecated patterns in src/ and suggest refactoring strategy"
MODEL="opus"
REPORT_FILE="agents/background/refactoring_analysis.md"
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

## Configuration

### Model Selection

- `haiku`: Fast, lightweight model for quick analysis
- `sonnet`: Balanced default for most tasks
- `opus`: Powerful model for complex analysis

### Directory Structure

Reports are stored in `agents/background/` with automatic status tracking:
- `<taskname>.complete.md` - Successful execution
- `<taskname>.failed.md` - Execution errors or failures

### Report File Naming

Original filename structure: `agents/background/<task_name>_<timestamp>.md`
- Timestamp format: `$a_$H_$M_$S` (day_hour_minute_second)
- Automatically renamed post-execution based on exit code
- If rename fails, warning is appended to report

## Testing

### Verify Documentation Structure

```bash
# Check base file exists and contains required elements
grep -q "USER_PROMPT" .claude/commands/background.md && echo "✓ Variables documented"
grep -q "dangerously-skip-permissions" .claude/commands/background.md && echo "✓ Security warnings included"
grep -q ".complete.md" .claude/commands/background.md && echo "✓ Status tracking documented"
```

### Verify Template File

```bash
# Check template has Jinja2 variables
grep -q "{{ config.directories" tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2 && echo "✓ Template variables present"
```

### Test Basic Execution (if claude CLI available)

```bash
# Create test directory
mkdir -p agents/background/

# Execute a simple test prompt
.claude/commands/background.md "List the TAC Bootstrap directory structure" "haiku" "agents/background/test_report.md"

# Check report file was created and renamed
ls -la agents/background/test_report*.md
```

### Markdown Validation

```bash
# Verify markdown syntax is valid
file .claude/commands/background.md | grep text
file tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/background.md.j2 | grep text
```

## Notes

- **Security Consideration**: The `--dangerously-skip-permissions` flag bypasses all permission checks. Only use when running in isolated/trusted environments with authorized tasks.

- **Directory Prerequisite**: The `agents/background/` directory must exist before running background commands. The script creates it with `mkdir -p`, but users should understand this requirement.

- **File Renaming**: Automatic renaming (`.complete.md`/`.failed.md`) depends on successful `mv` operation. If it fails, a warning is appended and the original filename is preserved.

- **Model Defaults**: The MODEL variable defaults to 'sonnet' if not provided, providing a balanced default for most analysis tasks.

- **Template Consistency**: Both base file (`.claude/commands/background.md`) and template file (`.j2`) maintain identical structure and documentation. Only Jinja2 variables differ between them.

- **Future Enhancement**: Consider adding monitoring utilities or dashboard for tracking background task statuses across multiple concurrent executions.
