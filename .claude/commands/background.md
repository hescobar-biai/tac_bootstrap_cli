# Background Agent Delegation

Delegate long-running tasks to background agents for out-of-loop execution. Based on the `Instructions` below, take the `Variables` follow the `Run` section to delegate a task to a background agent. Then follow the `Report` section to report the results of your work.

## Variables

task_description: $ARGUMENT
agent_type: $ARGUMENT (optional, defaults to 'general-purpose')
model: $ARGUMENT (optional: 'sonnet', 'haiku', 'opus')

## Instructions

- Background agents execute tasks asynchronously without blocking your main workflow
- Use background agents for:
  - Long-running test suites or builds
  - Extensive code analysis or refactoring
  - Large-scale searches or documentation generation
  - Complex multi-step tasks that don't require immediate interaction
- The agent will run in the background and save output to a file
- You can continue working while the background agent executes
- Check the output file periodically to monitor progress
- Use `tail -f <output_file>` to follow the agent's progress in real-time

## Run

1. Use the Task tool with `run_in_background: true` parameter:
   - Set `subagent_type` to the appropriate agent type (default: 'general-purpose')
   - Set `prompt` to the task description
   - Optionally set `model` to 'haiku' for quick tasks or 'opus' for complex ones
   - The tool will return an `output_file` path

2. Inform the user that the task is running in the background:
   - Provide the output file path
   - Explain they can check progress with: `tail -f <output_file>`
   - Note they'll be notified when the task completes

3. Continue with other work while the background agent runs

## Examples

**Example 1: Long-running test suite**
```
Task: Run the entire test suite including slow integration tests
Agent: general-purpose
Model: haiku (simple task execution)
```

**Example 2: Complex refactoring**
```
Task: Refactor the authentication module to use a new pattern across 20+ files
Agent: general-purpose
Model: sonnet (requires careful analysis and changes)
```

**Example 3: Documentation generation**
```
Task: Generate comprehensive API documentation for all endpoints
Agent: general-purpose
Model: haiku (straightforward documentation task)
```

## Report

Report to the user:
1. Confirmation that the background agent has been launched
2. The output file path where results will be saved
3. Command to monitor progress: `tail -f <output_file>`
4. Reminder that they'll be notified when the task completes

Format:
```
Background agent launched successfully.
Output file: <path_to_output_file>
Monitor progress: tail -f <path_to_output_file>
You'll be notified when the task completes.
```
