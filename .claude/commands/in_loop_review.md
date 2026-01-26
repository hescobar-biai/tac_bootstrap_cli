# In-Loop Review

Quick checkout and review workflow for agent work validation.

## Variables

branch: $ARGUMENTS

## Workflow

IMPORTANT: If no branch is provided, stop execution and report that the branch argument is required.

### Step 1: Pull and Checkout Branch
- Run `git fetch origin` to get remote changes
- Run `git checkout {branch}` to switch to target branch

### Step 2: Prepare Environment

**Install dependencies:**
- Run `` to sync dependencies

**Verify application:**
- Run `uv run tac-bootstrap --help --help` or equivalent to verify app works

### Step 3: Run Validation
- Run `uv run pytest` to run tests
- Run `uv run ruff check .` to verify linting

### Step 4: Manual Review
- The application is ready for manual review
- The engineer can test commands directly

## Report

Report steps taken to prepare the environment for review.
