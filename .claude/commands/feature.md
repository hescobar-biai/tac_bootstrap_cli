# Feature Planning

Create a plan to implement a new feature in tac-bootstrap following the specified format.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANT: You are creating a plan to implement a new feature for tac-bootstrap.
- The plan will be used to guide implementation with agentic coding.
- Create the plan in `specs/` with filename: `issue-{issue_number}-adw-{adw_id}-feature_planner-{descriptive-name}.md`
- Investigate the codebase to understand existing patterns before planning.
- IMPORTANT: Replace each <placeholder> in the format with real values.
- Use the reasoning model: think carefully about requirements and approach.
- Follow existing patterns and conventions in the project.
- If you need a new library, use `` and report it in Notes.
- Keep it simple - don't use unnecessary decorators.

## Relevant Files

Key files for tac-bootstrap:

- `CLAUDE.md` - Agent guide
- `config.yml` - Project configuration
- `tac_bootstrap_cli/` - Application source code

Read `.claude/commands/conditional_docs.md` for additional documentation.

## Plan Format

```md
# Feature: <feature name>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Feature Description
<describe the feature in detail, its purpose and value>

## User Story
As a <user type>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<clearly define the problem or opportunity this feature addresses>

## Solution Statement
<describe the proposed approach and how it solves the problem>

## Relevant Files
Files needed to implement the feature:

<list relevant files with description of why they are relevant>

### New Files
<list new files to be created>

## Implementation Plan

### Phase 1: Foundation
<foundational work before implementing the main feature>

### Phase 2: Core Implementation
<main feature implementation>

### Phase 3: Integration
<integration with existing functionality>

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: <name>
- <detail>
- <detail>

### Task 2: <name>
- <detail>

<The last step should execute Validation Commands>

## Testing Strategy

### Unit Tests
<required unit tests>

### Edge Cases
<edge cases to test>

## Acceptance Criteria
<specific and measurable criteria to consider the feature complete>

## Validation Commands
Run all commands to validate with zero regressions:

- `uv run pytest` - Run tests
- `uv run ruff check .` - Linting
- `uv run mypy tac_bootstrap_cli` - Type check

## Notes
<additional notes, future considerations, or relevant context>
```

## Feature
Extract feature details from the `issue_json` variable (parse JSON and use title and body fields).

## Report

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it following the Plan Format, then return ONLY the path

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the path like:
```
specs/issue-37-adw-e4dc9574-feature_planner-feature-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I can see that...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines

ONLY output the bare path. This is machine-parsed.
