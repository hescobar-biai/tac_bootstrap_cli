# Background Command Execution

Execute user prompts in the background with structured reporting and automatic status tracking. This command uses the `claude` CLI directly to run analysis tasks without blocking your workflow, capturing results in timestamped report files that are automatically renamed based on execution status.

## Variables

- `USER_PROMPT` ($1): The prompt/command to execute in the background (required)
- `MODEL` ($2): Claude model to use - 'haiku' (fast), 'sonnet' (balanced), 'opus' (powerful). Defaults to 'sonnet'
- `REPORT_FILE` ($3): Output file path for structured report (required; must be in agents/background/ directory)

## Instructions

### When to Use Background Execution

- Long-running analysis tasks (complex codebase exploration, refactoring analysis)
- Extensive documentation generation or research
- Large-scale code reviews or security audits
- Tasks that don't require immediate interaction with the main workflow

### Security Implications

⚠️ **WARNING**: This command uses `--dangerously-skip-permissions` with the `claude` CLI. This bypasses permission checks for:
- Reading and writing files
- Executing system commands
- Accessing project context

**Only use this flag when**:
- You are running in an isolated/trusted environment
- You understand the security implications of skipping permission checks
- The background task is authorized to access the files/commands in your project

### Directory Structure Requirement

The `agents/background/` directory must exist before running background commands:

```bash
mkdir -p agents/background/
```

This directory stores all timestamped report files. Report files are automatically renamed:
- `.complete.md` - Task executed successfully (exit code 0)
- `.failed.md` - Task failed or encountered errors (non-zero exit code)

### Output File Behavior

- Reports are written to the path specified in `$REPORT_FILE`
- Original filename structure: `agents/background/<task_name>_<timestamp>.md`
- After execution, file is automatically renamed based on completion status
- If rename fails, the report remains with original filename and a warning is appended
- Monitor progress: Use `tail -f agents/background/*.md` to watch report files

## Run

```bash
#!/bin/bash

# Variables
USER_PROMPT="$1"
MODEL="${2:-sonnet}"
REPORT_FILE="$3"
TIMESTAMP=$(date +%a_%H_%M_%S)

# Ensure directory exists
mkdir -p agents/background/

# Build report file path with timestamp if not provided
if [ -z "$REPORT_FILE" ]; then
  REPORT_FILE="agents/background/analysis_${TIMESTAMP}.md"
fi

# Execute claude CLI in background with structured reporting
{
  echo "# Background Task Report"
  echo "**Started**: $(date)"
  echo "**Model**: $MODEL"
  echo "**Timestamp**: $TIMESTAMP"
  echo ""
  echo "## Task"
  echo '```'
  echo "$USER_PROMPT"
  echo '```'
  echo ""
  echo "## Results"
  echo ""

  # Execute the prompt using claude CLI
  claude "$USER_PROMPT" --model "$MODEL" --append-system-prompt 2>&1

  EXIT_CODE=$?

  echo ""
  echo "## Execution Status"
  echo "**Completed**: $(date)"
  echo "**Exit Code**: $EXIT_CODE"

} > "$REPORT_FILE" 2>&1

# Capture exit code from the background execution
FINAL_EXIT_CODE=$?

# Auto-rename based on completion status
if [ $FINAL_EXIT_CODE -eq 0 ]; then
  mv "$REPORT_FILE" "${REPORT_FILE%.md}.complete.md" 2>/dev/null || {
    echo "Warning: Failed to rename report file to .complete.md" >> "$REPORT_FILE"
  }
else
  mv "$REPORT_FILE" "${REPORT_FILE%.md}.failed.md" 2>/dev/null || {
    echo "Warning: Failed to rename report file to .failed.md" >> "$REPORT_FILE"
  }
fi
```

## Examples

### Example 1: Analyze Complex Architecture

```bash
USER_PROMPT="Analyze the authentication system architecture and identify security gaps"
MODEL="sonnet"
REPORT_FILE="agents/background/auth_security_review.md"

# Execute in background
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

Monitor the analysis:
```bash
tail -f agents/background/auth_security_review*.md
```

### Example 2: Generate API Documentation

```bash
USER_PROMPT="Review all API endpoints in src/api/ and generate comprehensive documentation"
MODEL="haiku"
REPORT_FILE="agents/background/api_docs_generation.md"

# Execute with quick model for faster turnaround
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

### Example 3: Codebase Refactoring Analysis

```bash
USER_PROMPT="Identify all occurrences of deprecated patterns in src/ and suggest refactoring strategy"
MODEL="opus"
REPORT_FILE="agents/background/refactoring_analysis.md"

# Use powerful model for comprehensive analysis
./background.sh "$USER_PROMPT" "$MODEL" "$REPORT_FILE" &
```

## Report

After executing a background task:

1. **Structured Report**: A markdown file with:
   - Task metadata (started time, model used, timestamp)
   - Original user prompt
   - Full execution results from claude CLI
   - Completion status and exit code

2. **File Status**:
   - Check `agents/background/` directory for report files
   - `.complete.md` files indicate successful execution
   - `.failed.md` files indicate errors or failures
   - Use `ls -ltr agents/background/` to see latest reports

3. **Monitor Progress**:
   - Watch in real-time: `tail -f agents/background/<filename>`
   - View completed reports: `cat agents/background/<filename>.complete.md`
   - Review failed reports: `cat agents/background/<filename>.failed.md`

4. **Expected Report Format**:
   - Header with task metadata
   - Original prompt in code block
   - Complete output from claude analysis
   - Footer with execution status and timestamp
