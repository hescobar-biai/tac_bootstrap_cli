---
allowed-tools:
  - Task
  - Read
  - AskUserQuestion
description: One-shot agent execution pattern for single specialized agent tasks
argument-hint: "[agent_type] [task_description]"
model: sonnet
category: Orchestrator Commands
---

# One-Shot Agent Execution

Launch a single specialized agent to execute a focused task. This command provides a simple delegation pattern for tasks that benefit from a dedicated agent context but don't require multi-phase orchestration.

## Variables

AGENT_TYPE: $1 (required - type of agent to launch)
TASK_DESCRIPTION: $2 (required - description of what the agent should do)

## Purpose

The `/orch_one_shot_agent` command provides single-agent delegation by:
- Validating the agent type against available agent definitions
- Launching the appropriate specialized agent
- Providing clear task context to the agent
- Reporting agent results back to the user

## When to Use This Command

Use `/orch_one_shot_agent` when:
- You need a specialized agent for a focused task
- The task benefits from dedicated agent context and tools
- You want to delegate work to a specific agent type
- You don't need multi-phase orchestration (scout, plan, build, review)
- You want explicit control over which agent type to use

## When NOT to Use This Command

Do NOT use `/orch_one_shot_agent` when:
- The task requires multiple phases (use orchestration commands like `/orch_plan_w_scouts_build_review`)
- The task is simple enough to do directly (no need for agent delegation)
- You need multiple agents working in parallel (use `/parallel_subagents`)
- You need sequential multi-agent workflow (use other orchestration commands)

## Available Agent Types

Based on agent definitions in `.claude/agents/`:

- **build-agent**: Specialized for writing individual files based on detailed specifications
- **planner**: Creates structured implementation plans for features and tasks
- **scout-report-suggest**: Read-only codebase analysis and issue identification
- **scout-report-suggest-fast**: Fast read-only codebase scouting (uses haiku model)
- **docs-scraper**: Fetches and saves documentation from URLs as markdown
- **meta-agent**: Generates new agent definitions from natural language descriptions
- **playwright-validator**: Browser automation testing and validation
- **research-docs-fetcher**: Advanced documentation research and fetching

## Instructions

### Step 1: Validate Input Parameters

**Validate AGENT_TYPE:**
- Extract AGENT_TYPE from $1
- If AGENT_TYPE is missing or empty:
  - Report error: "ERROR: AGENT_TYPE is required. Usage: /orch_one_shot_agent [agent_type] [task_description]"
  - List available agent types from the list above
  - STOP - do not continue

**Validate TASK_DESCRIPTION:**
- Extract TASK_DESCRIPTION from $2
- If TASK_DESCRIPTION is missing or empty:
  - Report error: "ERROR: TASK_DESCRIPTION is required. Usage: /orch_one_shot_agent [agent_type] [task_description]"
  - STOP - do not continue

**Validate Agent Type Exists:**
- Check if AGENT_TYPE matches one of the available agent types (case-insensitive)
- If agent type not found:
  - Report error: "ERROR: Unknown agent type '{AGENT_TYPE}'"
  - List available agent types
  - Suggest closest match if there's a typo (e.g., "build" → "build-agent")
  - STOP - do not continue

### Step 2: Display Launch Message

Output clear message about what's being launched:

```
🚀 Launching {AGENT_TYPE} agent...
Task: {TASK_DESCRIPTION}
```

### Step 3: Launch Agent

Use Task tool to launch the specialized agent:

```
Task:
  subagent_type: "{AGENT_TYPE}"
  description: "One-shot: {truncated_task_description}"  # First 3-5 words
  model: [appropriate model based on agent type]
  prompt: "{TASK_DESCRIPTION}"
```

**Model Selection:**
- build-agent, planner, playwright-validator, meta-agent, research-docs-fetcher: `sonnet` (complex tasks)
- scout-report-suggest-fast, docs-scraper: `haiku` (fast tasks)
- scout-report-suggest: `sonnet` (thorough analysis)
- Default: `sonnet`

Wait for agent to complete.

### Step 4: Process Agent Results

**If agent succeeds:**
- Extract key results from agent output
- Present results in clear, structured format
- Highlight important findings or deliverables
- Show any files created/modified (if applicable)

**If agent fails:**
- Report error: "ERROR: {AGENT_TYPE} agent failed during execution."
- Show agent error details
- Provide context about what was attempted
- Suggest recovery steps if applicable

### Step 5: Report Status

Output completion report:

```
=== AGENT EXECUTION COMPLETE ===

Agent Type: {AGENT_TYPE}
Status: [SUCCESS or FAILED]

Agent Results:
{summary_of_agent_output}

[If files were modified/created:]
Changes Made:
{git_diff_stat_output or file list}

Next Steps:
[Contextual recommendations based on agent type and results]
```

## Report

Provide a structured report of the agent execution:

### Execution Status
- Agent Type: {AGENT_TYPE}
- Status: [SUCCESS or FAILED]
- Task: {TASK_DESCRIPTION}

### Agent Results

Summarize the agent's output based on agent type:

**For build-agent:**
- Files created/modified: {list}
- Implementation summary: {key points}
- Issues encountered: {if any}

**For planner:**
- Plan file location: {path}
- Plan summary: {key points}
- Steps identified: {count}

**For scout-report-suggest:**
- Issues found: {count}
- Files analyzed: {count}
- Key findings: {summary}
- Recommendations: {list}

**For docs-scraper:**
- Documentation saved to: {path}
- Content summary: {key points}

**For meta-agent:**
- Agent definition created: {path}
- Agent capabilities: {summary}

**For playwright-validator:**
- Tests executed: {count}
- Results: {pass/fail summary}
- Screenshots: {paths if any}

**For research-docs-fetcher:**
- Documentation sources: {list}
- Files created: {paths}
- Key findings: {summary}

### Git Changes (if applicable)
```
{output of git diff --stat if agent modified files}
```

### Recommendations

Provide next steps based on agent type and results:

**After build-agent:**
- Review created/modified files
- Run tests to validate implementation
- Consider code review

**After planner:**
- Review the generated plan
- Adjust if needed
- Execute plan with `/build {plan_path}`

**After scout-report-suggest:**
- Review identified issues
- Prioritize fixes
- Address recommendations

**After docs-scraper:**
- Review saved documentation
- Integrate into project docs
- Share with team if needed

**After meta-agent:**
- Review generated agent definition
- Test the new agent
- Adjust agent prompt if needed

**After playwright-validator:**
- Review test results
- Fix failing tests if any
- Review screenshots for visual validation

**After research-docs-fetcher:**
- Review fetched documentation
- Integrate relevant information
- Update project documentation

### Notes
- One-shot agent execution is ideal for focused, single-agent tasks
- For multi-phase workflows, consider orchestration commands
- For parallel agent execution, use `/parallel_subagents`
- Agents have access to tools specified in their definitions

## Examples

**Example 1: Scout codebase for authentication issues**
```
/orch_one_shot_agent scout-report-suggest "Find all authentication-related code and identify potential security issues"
```

**Example 2: Create plan for new feature**
```
/orch_one_shot_agent planner "Create implementation plan for adding user profile editing functionality"
```

**Example 3: Build specific file**
```
/orch_one_shot_agent build-agent "Create a new UserService class in src/services/user.service.ts with CRUD operations following existing service patterns"
```

**Example 4: Fetch external documentation**
```
/orch_one_shot_agent docs-scraper "Fetch and save documentation from https://docs.example.com/api to ai_docs/external/example-api.md"
```

**Example 5: Create new agent definition**
```
/orch_one_shot_agent meta-agent "Create an agent definition for a database migration validator that checks migration files for common issues"
```
