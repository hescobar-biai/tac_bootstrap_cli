---
allowed-tools:
  - Task
  - Read
  - TodoWrite
description: Simplified workflow orchestrating scout exploration and direct build
argument-hint: "[task_description]"
model: sonnet
category: Orchestrator Commands
---

# Scout → Build Orchestrator (Simplified)

Execute a streamlined implementation workflow by orchestrating two sequential phases: parallel scout exploration and direct code generation. This command provides a fast path from discovery to implementation, skipping formal planning and review phases.

## Variables

TASK_DESCRIPTION: $1 (required - description of what to implement)

## Purpose

The `/orch_scout_and_build` command provides simplified pipeline automation by:
- Discovering all files relevant to your task through parallel scout exploration
- Implementing changes directly based on scout findings
- Skipping formal planning and review for faster execution
- Handling errors with fail-fast behavior

## When to Use This Command

Use `/orch_scout_and_build` when:
- You have a clear, straightforward implementation task
- You want fast execution without formal planning overhead
- The implementation is low-risk and doesn't require extensive review
- You need file discovery but don't want to create a formal plan document
- You're comfortable with the agent making implementation decisions based on scout findings

## When NOT to Use This Command

Do NOT use `/orch_scout_and_build` when:
- The task is complex and requires careful planning (use `/orch_plan_w_scouts_build_review`)
- You need quality review before considering the work complete (use `/orch_plan_w_scouts_build_review`)
- You already know which files to modify (use direct editing or `/build`)
- The task is trivial (use direct editing)
- You want a formal plan document for reference (use `/scout_plan_build`)

## Workflow Phases

**Phase 1: Scout (Parallel Exploration)**
- Launches parallel exploration agents with different search strategies
- Uses Glob for file patterns, Grep for content search, Read for analysis
- Aggregates results with relevance scoring
- Read-only codebase analysis

**Phase 2: Build (Direct Implementation)**
- Implements changes directly based on scout findings
- Shows clear progress during implementation
- Validates changes as they're made
- Reports implementation status

## Instructions

### Step 1: Initialize Todo List

Create todo list to track the 2-phase workflow:

```
Use TodoWrite tool to create:
- 🔍 Scout Phase: Parallel codebase exploration
- 🔨 Build Phase: Direct implementation
```

Set first todo (Scout Phase) to `in_progress`.

### Step 2: Validate Input Parameters

Extract and validate TASK_DESCRIPTION:

- Extract TASK_DESCRIPTION from $1
- If TASK_DESCRIPTION is missing or empty:
  - Report error: "ERROR: TASK_DESCRIPTION is required. Usage: /orch_scout_and_build \"task description\""
  - STOP - do not continue

### Step 3: Launch Scout Phase

Output progress message:
```
=== PHASE 1/2: SCOUT ===
Launching parallel codebase exploration...
Task: {TASK_DESCRIPTION}
```

Launch scout agent using Task tool:
- `subagent_type: "scout-report-suggest"`
- `model: "haiku"` (fast, cost-effective)
- `description: "Scout: parallel exploration"`
- `prompt`:
```
Find all files relevant to: {TASK_DESCRIPTION}

Use parallel exploration strategies:
- File pattern search (Glob for naming conventions and directory structure)
- Content search (Grep for keywords, functions, classes, imports)
- Architectural analysis (Read to understand module relationships)
- Dependency mapping (cross-file references)

Aggregate results with frequency-based relevance scoring.
List all relevant files with brief relevance notes.
Use thoroughness level: quick
```

Wait for scout agent to complete.

If scout fails:
- Report error: "ERROR: Scout phase failed. Unable to explore codebase."
- Show scout error details
- Mark scout todo as failed
- STOP - do not continue to build phase

Mark scout todo as completed, set build todo to `in_progress`.

### Step 4: Process Scout Results and Launch Build Phase

Output progress message:
```
=== PHASE 2/2: BUILD ===
Implementing changes based on scout findings...
```

Parse scout agent output to extract:
- List of relevant files found
- Relevance notes and context for each file
- Architectural patterns identified

Launch build agent using Task tool:
- `subagent_type: "general-purpose"`
- `model: "sonnet"` (balanced for implementation)
- `description: "Build: direct implementation"`
- `prompt`:
```
Implement the following task: {TASK_DESCRIPTION}

Scout exploration found these relevant files:
{scout_results_summary}

Follow the build workflow:
1. Analyze the task requirements
2. Review the files identified by scout exploration
3. Design implementation approach following existing patterns
4. Implement changes:
   - Show clear progress (e.g., "Implementing feature X...")
   - Complete each change fully before moving to next
   - Verify changes work as you go
   - Use appropriate tools (Read, Write, Edit, Bash, etc.)
5. Follow best practices and coding standards
6. If any step fails:
   - STOP immediately
   - Report what failed and why
   - Show what was completed successfully
7. After completion, report:
   - Implementation status (success or failure)
   - Changes made (git diff --stat)
   - Summary of implementation
   - Any validation performed

Use the scout findings to guide your implementation but make decisions directly without creating a formal plan document.
```

Wait for build agent to complete.

If build fails:
- Report error: "ERROR: Build phase failed during implementation."
- Show build error details
- Show what scout phase completed successfully
- Mark build todo as failed

Mark build todo as completed.

### Step 5: Report Final Status

Output comprehensive completion report:

```
=== WORKFLOW COMPLETE ===

Status: [SUCCESS or FAILED at {phase}]

Phase Results:
- Scout Phase: ✓ Complete (files discovered)
- Build Phase: [✓ Complete or ✗ Failed]

Implementation Summary:
{build_summary}

Changes Made:
{git_diff_stat_output}

Next Steps:
- Review changes manually
- Run tests with /test
- Run /review for quality assessment if desired
- Create commit with /commit
```

## Report

Provide a structured report of the workflow execution:

### Execution Status
- Overall Status: [SUCCESS or FAILED]
- Failed Phase: [None or Scout/Build]
- Completion: [2/2 phases or X/2 phases]

### Phase Details

**Scout Phase:**
- Status: [Complete/Failed]
- Files Discovered: {count}
- Relevant Files: {list or summary}

**Build Phase:**
- Status: [Complete/Failed/Skipped]
- Files Modified: {count or N/A}
- Lines Changed: {count or N/A}

### Git Changes
```
{output of git diff --stat if build completed}
```

### Implementation Summary
- Bullet point list of what was implemented (if build completed)
- Any issues encountered and resolutions
- Validation status (if applicable)

### Recommendations

If successful:
- Review the implementation manually to ensure it meets requirements
- Run tests with `/test` to validate functionality
- Consider using `/review` for quality assessment
- Create commit with `/commit` after validation

If failed:
- Review error messages for the failed phase
- Fix issues and retry:
  - Scout failed: Ensure task description is clear
  - Build failed: Fix issues and retry implementation

### Notes
- This workflow provides fast execution by skipping formal planning and review
- Best suited for straightforward tasks with clear requirements
- For complex tasks requiring formal planning, use `/orch_plan_w_scouts_build_review`
- For quality assurance, consider adding `/review` after this workflow completes
