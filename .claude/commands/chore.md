# Chore Planning

Create a plan to complete a maintenance task (chore) in tac-bootstrap using the specified format.

## Variables
issue_number: $1
adw_id: $2
issue_json: $3

## Instructions

- IMPORTANT: You are writing a plan to complete a chore for tac-bootstrap.
- The plan should be simple but precise to avoid wasting time.
- Create the plan in `specs/` with filename: `issue-{issue_number}-adw-{adw_id}-chore_planner-{descriptive-name}.md`
- Investigate the codebase and create a plan to complete the chore.
- IMPORTANT: Replace each <placeholder> in the format with real values.
- Use the reasoning model: think carefully about the steps.
- `adws/*.py` are uv single-file scripts. Run with `uv run <script_name>`.

## Relevant Files

Key files for tac-bootstrap:

- `CLAUDE.md` - Agent guide
- `config.yml` - Project configuration
- `tac_bootstrap_cli/` - Application source code
- `scripts/` - Utility scripts
- `adws/` - AI Developer Workflows

Read `.claude/commands/conditional_docs.md` for additional documentation.

## Plan Format

```md
# Chore: <chore name>

## Metadata
issue_number: `{issue_number}`
adw_id: `{adw_id}`
issue_json: `{issue_json}`

## Chore Description
<describe the chore in detail>

## Relevant Files
Files to complete the chore:

<list relevant files with description of why they are relevant>

### New Files
<list new files if required>

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: <name>
- <detail>

### Task 2: <name>
- <detail>

<The last step should execute Validation Commands>

## Validation Commands
Run all commands to validate with zero regressions:

- `uv run pytest` - Run tests
- `uv run ruff check .` - Linting

## Notes
<additional notes or relevant context>
```

## Chore
Extract chore details from the `issue_json` variable (parse JSON and use title and body fields).

## Report

CRITICAL OUTPUT FORMAT - You MUST follow this exactly:

1. First, check if a plan file already exists in `specs/` matching pattern: `issue-{issue_number}-adw-{adw_id}-*.md`
2. If plan file EXISTS: Return ONLY the relative path, nothing else
3. If plan file does NOT exist: Create it following the Plan Format, then return ONLY the path

YOUR FINAL OUTPUT MUST BE EXACTLY ONE LINE containing only the path like:
```
specs/issue-37-adw-e4dc9574-chore_planner-chore-name.md
```

DO NOT include:
- Any explanation or commentary
- Phrases like "Perfect!", "I found...", "The plan file is at..."
- Markdown formatting around the path
- Multiple lines

ONLY output the bare path. This is machine-parsed.
