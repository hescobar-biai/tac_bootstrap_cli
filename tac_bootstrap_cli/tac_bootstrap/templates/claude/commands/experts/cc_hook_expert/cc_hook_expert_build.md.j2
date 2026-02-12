---
allowed-tools: Read, Write, Edit, Bash, TodoWrite, Glob, Grep
description: Build hook implementation following expert plan
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# Purpose

This expert command guides AI agents through the implementation (build) phase of Claude Code hooks. This is the second step in the Plan-Build-Improve workflow cycle for hook development. The agent will execute the implementation plan created in the planning phase, write hook code following established patterns, integrate with settings.json, validate functionality, and troubleshoot issues.

## Usage

**When to use this command:**
- After completing the planning phase (`/cc_hook_expert_plan`)
- When you have a hook implementation plan ready to execute
- To build and validate a new Claude Code hook

**How to use:**
- `/cc_hook_expert_build` - Agent will search for plan in specs/ directory
- `/cc_hook_expert_build specs/hook-my-hook-plan.md` - Reference specific plan document
- `/cc_hook_expert_build "implement validation hook from plan"` - Provide build context

**What happens:**
This command executes the planned hook implementation step-by-step, validates functionality with tests and linting, integrates with settings.json, and ensures the hook works correctly before moving to the improvement phase.

**Workflow context:**
Plan (cc_hook_expert_plan) → **Build (cc_hook_expert_build)** → Improve (cc_hook_expert_improve)

## Variables

BUILD_CONTEXT: $ARGUMENTS
PROJECT_NAME: tac_bootstrap
TEST_COMMAND: uv run pytest

## Instructions

Follow this 4-phase workflow to implement the hook based on your plan:

### Phase 1: Review Plan

**Locate the implementation plan:**
- If BUILD_CONTEXT contains a file path (e.g., `specs/hook-validation-plan.md`), read that file
- Otherwise, search `specs/` directory for hook plan documents
- Use Glob or Grep to find plan files matching pattern: `specs/hook-*-plan.md` or `specs/*hook*plan*.md`

**Parse the plan:**
- Read the plan document thoroughly
- Identify key implementation decisions:
  - Hook name and file path
  - Hook type (PreToolUse, PostToolUse, Notification, etc.)
  - Matcher pattern
  - Input/output structure
  - Exit code strategy (0=allow, 1=warn, 2=block)
  - Error handling approach
  - Integration points (settings.json changes, dependencies)

**Set up task tracking:**
- Use TodoWrite to create tasks for each implementation step from the plan
- Break down into actionable items:
  - Create hook script file
  - Implement core logic
  - Add error handling
  - Update settings.json
  - Run tests
  - Validate integration
- Mark first task as in_progress before starting implementation

**Identify files to create/modify:**
- Hook script file (e.g., `.claude/hooks/pre_tool_use.py`)
- Settings configuration (`.claude/settings.json`)
- Any utility modules or shared code
- Test files if applicable

### Phase 2: Implement Hook

**Write the hook script following the plan:**

1. **Create hook file with proper structure:**
   - Use shebang: `#!/usr/bin/env -S uv run --script`
   - Add script metadata if using uv
   - Import required modules (json, sys, os, pathlib, etc.)
   - Import utilities if needed (e.g., from utils.constants import ensure_session_log_dir)

2. **Implement JSON input parsing:**
   ```python
   import json
   import sys

   def main():
       try:
           input_data = json.load(sys.stdin)
           tool_name = input_data.get('tool_name', '')
           tool_input = input_data.get('tool_input', {})
           session_id = input_data.get('session_id', 'unknown')
           # ... hook logic here
       except json.JSONDecodeError:
           sys.exit(0)  # Graceful failure
       except Exception:
           sys.exit(0)  # Graceful failure
   ```

3. **Implement hook logic based on plan:**
   - Follow the architecture designed in the plan
   - Implement validation, transformation, or observation logic
   - Use helper functions for complex logic (e.g., is_dangerous_command, check_file_access)
   - Add logging if specified in plan (write to session-specific logs)

4. **Implement exit code strategy:**
   - Exit 0: Allow operation to proceed (normal flow)
   - Exit 1: Show warning but allow operation (non-blocking warning)
   - Exit 2: Block operation completely (shows error to agent)
   - Use stderr for error messages: `print("BLOCKED: reason", file=sys.stderr)`
   - Use stdout for data output if hook modifies input

5. **Add error handling:**
   - Wrap main logic in try/except
   - Handle JSONDecodeError gracefully (exit 0 to not break workflow)
   - Handle expected exceptions with appropriate exit codes
   - Use graceful failures (exit 0) for unexpected errors to prevent blocking agent

**Follow naming conventions:**
- Use snake_case for hook files: `pre_tool_use.py`, `post_tool_use.py`, `security_check.py`
- Match hook type to filename (PreToolUse → pre_tool_use.py)
- Use descriptive names for custom hooks

**Integrate with .claude/settings.json:**

1. **Read current settings.json:**
   - Parse existing hook configuration
   - Identify where to add new hook entry

2. **Add hook configuration:**
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "",
           "hooks": [
             {
               "type": "command",
               "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
             }
           ]
         }
       ]
     }
   }
   ```
   - **matcher**: Empty `""` for all tools, or regex pattern for specific tools
   - **type**: Usually `"command"` for shell commands
   - **command**: Shell command with `|| true` for graceful failures
   - **$CLAUDE_PROJECT_DIR**: Environment variable (project root path)

3. **Update settings.json:**
   - Use Edit tool to add hook configuration
   - Preserve existing formatting and structure
   - Validate JSON syntax after editing

### Phase 3: Validate Implementation

**Run validation commands:**

1. **Execute tests:**
   - Run: `uv run pytest`
   - Verify all tests pass
   - Check for new test failures or regressions

2. **Run linting:**
   - Python: `ruff check .` or `pylint`
   - JavaScript/TypeScript: `eslint` or project linter
   - Check for code quality issues

3. **Run type checking (if applicable):**
   - Python: `mypy tac_bootstrap/` or project-specific path
   - TypeScript: `tsc --noEmit`
   - Verify type safety

4. **Manual smoke test:**
   - Test the hook by invoking a command that should trigger it
   - Verify hook executes and produces expected behavior:
     - PreToolUse: Does it block/allow correctly?
     - PostToolUse: Does it log/process correctly?
     - Notification: Does it handle notifications?
   - Check hook output (stdout/stderr)
   - Verify exit code behavior (0/1/2)

5. **Verify settings.json integration:**
   - Confirm hook appears in `.claude/settings.json`
   - Validate JSON syntax (settings.json is valid JSON)
   - Check matcher pattern is correct
   - Verify command path uses $CLAUDE_PROJECT_DIR

**Update TodoWrite:**
- Mark validation tasks as completed as you finish each step
- Note any issues discovered during validation

### Phase 4: Troubleshoot Issues

**If tests fail:**
- Read test output carefully
- Identify which tests are failing and why
- Fix implementation issues
- Re-run tests until all pass
- Update TodoWrite with fix status

**If hook doesn't trigger:**
- Check settings.json matcher pattern
- Verify hook is registered under correct hook type
- Test command manually: `cat test_input.json | .claude/hooks/your_hook.py`
- Check file permissions (hook script must be executable)
- Verify command path in settings.json

**If hook blocks incorrectly:**
- Review exit code logic (should be 0, 1, or 2)
- Check conditions that trigger blocking (exit 2)
- Verify error messages appear correctly
- Test with various inputs to validate behavior

**Common implementation errors:**

1. **JSON parsing failures:**
   - Malformed JSON input handling
   - Missing try/except for JSONDecodeError
   - Fix: Add robust error handling with graceful exit 0

2. **Incorrect exit codes:**
   - Using wrong exit code (should be 0, 1, or 2)
   - Not exiting at all (hangs)
   - Fix: Review exit code strategy in plan, ensure all code paths exit

3. **Permission issues:**
   - Script not executable
   - Fix: Check file permissions, ensure shebang is correct

4. **Import errors:**
   - Missing dependencies or utility modules
   - Fix: Install dependencies, verify import paths

5. **Settings.json syntax errors:**
   - Invalid JSON after editing
   - Fix: Validate JSON, check for missing commas, quotes, brackets

**Debugging steps:**

1. **Check hook logs/output:**
   - Look for error messages in stderr
   - Check session logs if hook writes logs
   - Review hook stdout for unexpected output

2. **Test hook script directly:**
   - Create sample JSON input file:
     ```json
     {
       "tool_name": "Bash",
       "tool_input": {"command": "echo test"},
       "session_id": "test-session"
     }
     ```
   - Run: `cat sample_input.json | .claude/hooks/your_hook.py`
   - Check exit code: `echo $?`
   - Verify output and errors

3. **Verify environment variables:**
   - Check $CLAUDE_PROJECT_DIR is available
   - Test hook command from settings.json manually

4. **Validate settings.json syntax:**
   - Use JSON validator or `jq` to check syntax
   - Ensure proper nesting and formatting

**Iteration guidance:**
- Fix issues one at a time
- Re-validate after each fix
- Update TodoWrite to track progress
- If major issues found, consider revisiting plan
- Once all validation passes, hook is ready for improvement phase (optional)

## Implementation Patterns

### Hook Code Structure

Standard hook script structure:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import os
from pathlib import Path

# Import utilities if needed
# from utils.constants import ensure_session_log_dir

def main():
    try:
        # 1. Parse JSON input from stdin
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        session_id = input_data.get('session_id', 'unknown')

        # 2. Implement hook logic
        # - Validation
        # - Transformation
        # - Logging
        # - etc.

        # 3. Handle blocking/warning conditions
        if should_block:
            print("BLOCKED: Reason for blocking", file=sys.stderr)
            sys.exit(2)  # Block operation

        if should_warn:
            print("WARNING: Reason for warning", file=sys.stderr)
            sys.exit(1)  # Warn but allow

        # 4. Optional: Output modified data
        # print(json.dumps(modified_data))

        # 5. Allow operation to proceed
        sys.exit(0)

    except json.JSONDecodeError:
        # Gracefully handle JSON errors
        sys.exit(0)
    except Exception:
        # Handle unexpected errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
```

### Settings.json Integration Pattern

Adding a new hook to settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/post_tool_use.py || true"
          }
        ]
      }
    ]
  }
}
```

**Key points:**
- `matcher: ""` matches all tools (use regex for specific tools like `"Bash"`)
- `|| true` ensures hook failures don't break agent workflow
- `$CLAUDE_PROJECT_DIR` is project root path (environment variable)
- Multiple hooks can be added to same hook type

### Error Handling Pattern

Robust error handling for hooks:

```python
def main():
    try:
        # Main hook logic
        input_data = json.load(sys.stdin)

        # Your logic here
        if validation_failed:
            print("ERROR: Validation failed", file=sys.stderr)
            sys.exit(2)  # Block

        # Success
        sys.exit(0)

    except json.JSONDecodeError as e:
        # JSON parsing error - graceful failure
        print(f"Warning: JSON decode error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block agent

    except FileNotFoundError as e:
        # Expected error - handle appropriately
        print(f"ERROR: File not found: {e}", file=sys.stderr)
        sys.exit(1)  # Warn

    except Exception as e:
        # Unexpected error - graceful failure
        print(f"Warning: Unexpected error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block agent
```

### Logging Pattern

Session-based logging for hooks:

```python
from pathlib import Path
import json

def log_hook_data(session_id, data):
    """Log hook data to session-specific file."""
    log_dir = Path(f".claude/logs/{session_id}")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / 'hook_name.json'

    # Read existing log or initialize
    if log_path.exists():
        with open(log_path, 'r') as f:
            try:
                log_data = json.load(f)
            except json.JSONDecodeError:
                log_data = []
    else:
        log_data = []

    # Append new entry
    log_data.append(data)

    # Write back
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
```

## Quality Checks

Before marking implementation complete, verify:

**Code Quality:**
- [ ] Hook script follows established patterns
- [ ] Error handling is robust (graceful failures)
- [ ] Exit codes are correct (0/1/2)
- [ ] Code is clean and readable
- [ ] Comments explain complex logic

**Integration:**
- [ ] Hook is registered in `.claude/settings.json`
- [ ] Matcher pattern is correct
- [ ] Command uses `$CLAUDE_PROJECT_DIR`
- [ ] Command includes `|| true` for graceful failures

**Functionality:**
- [ ] Hook triggers on expected events
- [ ] Hook produces expected behavior (block/warn/allow)
- [ ] Error messages are clear and helpful
- [ ] Hook doesn't break agent workflow

**Testing:**
- [ ] All tests pass: `uv run pytest`
- [ ] Linting is clean (no new warnings/errors)
- [ ] Type checking passes (if applicable)
- [ ] Manual smoke test validates behavior

**Documentation:**
- [ ] Hook purpose is clear from code/comments
- [ ] Settings.json entry is documented (if needed)
- [ ] Any special configuration is noted

## Report

After completing the build phase, provide this report:

```
✅ Hook Implementation Complete

Hook: {hook-name}
Type: {PreToolUse|PostToolUse|Notification|etc.}
File: {.claude/hooks/hook-file.py}

Implementation Summary:
- {What the hook does}
- {Key features or validations}
- {Exit code strategy}

Files Created/Modified:
- {.claude/hooks/hook-file.py} - Hook implementation
- {.claude/settings.json} - Hook registration

Validation Results:
✅ Tests passed
✅ Linting clean
✅ Type checking passed (if applicable)
✅ Manual smoke test successful
✅ Settings.json integration verified

Next Steps:
- Hook is ready for use
- If refinements needed, use /cc_hook_expert_improve
- Monitor hook behavior in actual usage
```

Include any warnings, issues, or recommendations for improvement.
