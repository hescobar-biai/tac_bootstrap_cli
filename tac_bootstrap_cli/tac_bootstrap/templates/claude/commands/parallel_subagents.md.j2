# Parallel Subagents

Launch multiple agents in parallel to solve complex tasks through decomposition and orchestration. Based on the `Instructions` below, take the `Variables`, follow the `Workflow` section to launch parallel agents, and then follow the `Report` section to report the results of your work.

## Variables

PROMPT_REQUEST: $1 (task description)
COUNT: $2 (number of agents, default: 3, range: 2-10)

## Instructions

This command implements TAC-10 Level 4 (Delegation Prompt) pattern for compute orchestration.

### When to Use This Command

Use parallel subagents when:
- The task can be naturally decomposed into independent subtasks
- Subtasks can execute simultaneously without blocking each other
- You need to maximize throughput for complex multi-domain work
- The task involves multiple concerns (e.g., backend + frontend + tests + docs)

### When NOT to Use This Command

Do NOT use parallel subagents when:
- The task is simple or straightforward (use direct implementation instead)
- Subtasks have strong sequential dependencies (Task B requires Task A output)
- The task is inherently serial (e.g., step-by-step refactoring with shared state)
- COUNT=1 (this is an error case - use Task tool directly instead)

### Decomposition Strategy

When designing agent prompts, follow these principles:
- **By domain/concern**: Split by natural boundaries (API, UI, database, tests)
- **Minimum overlap**: Each agent owns distinct deliverables
- **Clear deliverables**: Each agent produces concrete, mergeable artifacts
- **Resilience**: Design so partial failures don't block everything

### COUNT Validation

- If COUNT not specified: default to 3
- If COUNT < 2: error (recommend using Task tool directly)
- If COUNT > 10: cap at 10 (warn about resource constraints)
- Valid range: 2-10 agents

## Workflow

### Step 1: Parse Input

- Extract and validate PROMPT_REQUEST from $1
- Determine COUNT:
  - If $2 not provided: set COUNT=3 (default)
  - If $2 provided: validate it's an integer in range [2, 10]
  - If COUNT=1: abort with error message recommending Task tool
  - If COUNT>10: cap at 10 and warn user
- Confirm the task is suitable for parallelization:
  - Can it be decomposed into independent subtasks?
  - If not suitable: warn user but continue (delegate decision to user)

### Step 2: Design Agent Prompts

- Analyze PROMPT_REQUEST to identify natural decomposition boundaries
- Create COUNT distinct agent prompts, each with:
  - **Specific scope**: Clear boundaries and deliverables
  - **Context**: Enough information to work independently
  - **Success criteria**: What constitutes completion
- Ensure minimal overlap between agent responsibilities
- Design for resilience: partial failures should not block overall progress

### Step 3: Launch Parallel Agents

- Use the Task tool to launch all COUNT agents in parallel
- CRITICAL: Send a single message with multiple Task tool invocations (one per agent)
- For each agent:
  - Set `subagent_type: "general-purpose"` (or appropriate type)
  - Set `prompt` to the designed agent-specific prompt
  - Set `description` to a short summary (3-5 words)
  - Optionally set `model: "haiku"` for simple tasks or `model: "sonnet"` for complex ones
- DO NOT launch agents sequentially - use parallel invocation

### Step 4: Collect & Summarize

- Wait for all agents to complete
- Collect results from each agent
- Handle partial failures:
  - If some agents succeed: aggregate successful results and report failures
  - If all agents fail: identify common pattern and report root cause
- Synthesize results into coherent summary following Report format

## Report

Structure your report as follows:

### Agent Results

For each agent, create a section:

```markdown
## Agent N: [Task Name]

- [Key finding or deliverable 1]
- [Key finding or deliverable 2]
- [Key finding or deliverable 3]
- Status: [Success | Failed: reason]
```

### Overall Summary

```markdown
## Overall Summary

[Synthesize the collective findings from all agents into a coherent narrative]

### Key Achievements
- [Major accomplishment 1]
- [Major accomplishment 2]

### Issues Encountered
- [Issue 1 and resolution approach]

### Next Steps
- [Recommended follow-up action 1]
- [Recommended follow-up action 2]
```

### Error Handling

- If 1-2 agents fail: Continue with successful results, note failures
- If majority fail: Report pattern, suggest alternative approach
- If all fail: Identify root cause, recommend different strategy or tool
