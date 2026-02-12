---
allowed-tools: Read, Glob, Grep, Task, EnterPlanMode, AskUserQuestion, TodoWrite
description: Plan hook implementation using expert methodology
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# Purpose

This expert command guides AI agents through the planning phase of implementing Claude Code hooks. This is the first step in the Plan-Build-Improve workflow cycle for hook development. The agent will explore hook requirements, understand existing patterns, design hook architecture, and create a structured implementation plan.

## Variables

HOOK_REQUIREMENTS: $ARGUMENTS
PROJECT_NAME: tac_bootstrap

## Instructions

Follow this 4-phase workflow to create a comprehensive hook implementation plan:

### Phase 1: Understand Requirements

**If HOOK_REQUIREMENTS is provided:**
- Parse the hook requirements from $ARGUMENTS
- Identify the hook type (PreToolUse, PostToolUse, Notification, Stop, SubagentStop, PreCompact, UserPromptSubmit)
- Determine the specific events or conditions that should trigger the hook
- Define what the hook should accomplish (validation, logging, modification, blocking, etc.)

**If HOOK_REQUIREMENTS is empty:**
- Use AskUserQuestion to gather:
  - What event should trigger this hook?
  - What should the hook accomplish?
  - Are there specific tools or patterns to watch for?
  - Should the hook block execution or just observe?

**Define success criteria:**
- What does successful hook implementation look like?
- How will the hook be tested?
- What edge cases need consideration?

### Phase 2: Explore Codebase

**Use Task tool with Explore agent to investigate:**
- Existing hooks in `.claude/hooks/` directory
- Hook configuration patterns in `.claude/settings.json`
- Similar hooks that accomplish related goals
- Integration points and hook matcher patterns

**Read key files:**
- `.claude/settings.json` - Understand hook configuration structure
- Existing hook files (pre_tool_use.py, post_tool_use.py, etc.) - Learn patterns
- `CLAUDE.md` - Understand project context and conventions

**Identify patterns:**
- Hook naming conventions (pre_tool_use, post_tool_use, notification, etc.)
- JSON input/output structure
- Error handling strategies (exit codes: 0=allow, 1=warning, 2=block)
- Logging and session management patterns
- Environment variables available ($CLAUDE_PROJECT_DIR, etc.)

### Phase 3: Design Architecture

**Hook Specification:**
- Hook name and file path (e.g., `.claude/hooks/pre_commit_validation.py`)
- Hook type and trigger event
- Matcher pattern (empty "" for all, or specific pattern)
- Command structure in settings.json

**Input/Output Design:**
- What data does the hook receive? (JSON stdin with tool_name, tool_input, session_id, etc.)
- What does the hook output? (stdout for data, stderr for errors)
- Exit code strategy (0, 1, or 2)

**Error Handling:**
- Graceful failure strategy (when to block vs warn)
- Error message format
- Logging approach

**Integration Points:**
- How does the hook integrate with settings.json?
- Does it require new permissions in settings.json?
- Does it need utility modules or shared code?

### Phase 4: Create Implementation Plan

**Use EnterPlanMode or write plan document to:**
- `specs/hook-{hook-name}-plan.md`

**Plan document should include:**

1. **Hook Specification**
   - Hook name and purpose
   - Trigger event and type
   - Success criteria

2. **Technical Design**
   - Input data structure
   - Output and exit code strategy
   - Error handling approach
   - Integration with settings.json

3. **Implementation Steps**
   - Step-by-step tasks to implement the hook
   - File creation/modification list
   - Configuration changes needed
   - Dependencies or utilities required

4. **Testing Strategy**
   - How to test the hook manually
   - Test cases to cover (success, failure, edge cases)
   - Validation commands

5. **Hook Patterns Reference**
   - Example code snippets from similar hooks
   - Common patterns to follow
   - Best practices identified during exploration

## Hook Patterns

### Common Hook Types (from settings.json)

1. **PreToolUse**: Runs before any tool is executed
   - Use for: validation, blocking dangerous commands, pre-processing
   - Exit 2 to block tool execution
   - Example: Prevent rm -rf, block .env file access

2. **PostToolUse**: Runs after tool execution
   - Use for: logging results, post-processing, cleanup
   - Cannot block execution (already happened)
   - Example: Track tool usage statistics

3. **Notification**: Runs on system notifications
   - Use for: external integrations, alerts
   - Example: Send notifications to external systems

4. **Stop**: Runs when chat session stops
   - Use for: cleanup, final reporting
   - Example: Generate session summary

5. **SubagentStop**: Runs when subagent completes
   - Use for: subagent result processing
   - Example: Aggregate subagent results

6. **PreCompact**: Runs before context compaction
   - Use for: save important context before summarization
   - Example: Archive detailed logs before compaction

7. **UserPromptSubmit**: Runs when user submits a prompt
   - Use for: prompt logging, pre-processing user input
   - Example: Track user requests for analytics

### Hook Naming Conventions

- Use snake_case: `pre_tool_use.py`, `post_tool_use.py`
- Match hook type: PreToolUse → pre_tool_use.py
- Descriptive names for custom hooks: `pre_commit_validation.py`, `security_check.py`

### Hook Configuration Structure (settings.json)

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

- **matcher**: Empty "" for all tools, or regex pattern for specific tools
- **type**: Usually "command" for shell commands
- **command**: Shell command to execute (use `|| true` for graceful failures)
- **$CLAUDE_PROJECT_DIR**: Environment variable pointing to project root

### Exit Code Strategy

- **Exit 0**: Allow operation to proceed normally
- **Exit 1**: Show warning but allow operation (appears in UI)
- **Exit 2**: Block operation and show error to agent

### JSON Input Structure

Hooks receive JSON on stdin with structure:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf something",
    "description": "..."
  },
  "session_id": "unique-session-id",
  ...
}
```

## Report

After creating the implementation plan, provide a concise report:

```
✅ Hook Implementation Plan Created

File: specs/hook-{name}-plan.md
Hook Type: {PreToolUse|PostToolUse|Notification|Stop|etc.}
Purpose: {brief description}
Key Components:
- {component 1}
- {component 2}
- {component 3}
Integration Points:
- {settings.json changes}
- {new files needed}
- {dependencies required}
```
