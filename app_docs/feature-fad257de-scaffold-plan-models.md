---
doc_type: feature
adw_id: fad257de
date: 2026-01-27
idk:
  - domain-model
  - pydantic
  - scaffolding
  - fluent-interface
  - validation
  - idempotency
tags:
  - feature
  - domain
related_code:
  - tac_bootstrap_cli/tac_bootstrap/domain/plan.py
  - specs/issue-7-adw-fad257de-sdlc_planner-scaffold-plan-models.md
  - specs/issue-7-adw-fad257de-sdlc_planner-scaffold-plan-models-checklist.md
---

# Scaffold Plan Models

**ADW ID:** fad257de
**Date:** 2026-01-27
**Specification:** specs/issue-7-adw-fad257de-sdlc_planner-scaffold-plan-models.md

## Overview

Scaffold plan domain models provide type-safe representation of file and directory operations when scaffolding new projects. The models enable building operation plans programmatically, previewing changes before execution, and ensuring idempotent scaffolding through structured operation tracking.

## What Was Built

- **FileAction enum** - Four operation types: CREATE, OVERWRITE, PATCH, SKIP
- **FileOperation model** - Represents single file operations with path, action, template, content, reason, and executable flag
- **DirectoryOperation model** - Represents directory creation with path and purpose
- **ScaffoldPlan model** - Container with helper methods for filtering operations, summary generation, and fluent builder interface

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py`: Complete scaffold plan domain models implementation (144 lines)
- `specs/issue-7-adw-fad257de-sdlc_planner-scaffold-plan-models.md`: Feature specification with acceptance criteria
- `specs/issue-7-adw-fad257de-sdlc_planner-scaffold-plan-models-checklist.md`: Validation checklist confirming all criteria met

### Key Changes

- Implemented FileAction enum extending str for JSON serialization compatibility
- Created FileOperation with Pydantic Field descriptors for validation and documentation
- Implemented DirectoryOperation with required path and optional reason fields
- Built ScaffoldPlan container with filter methods (get_files_to_create, get_files_to_overwrite, get_files_to_patch, get_files_skipped, get_executable_files)
- Added computed properties (total_directories, total_files, summary) for plan introspection
- Implemented fluent builder interface (add_directory, add_file) returning self for method chaining

## How to Use

### Building a Plan Programmatically

```python
from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction

# Create plan using fluent interface
plan = ScaffoldPlan()
plan.add_directory('.claude/commands', 'Claude Code commands')
plan.add_file(
    '.claude/settings.json',
    FileAction.CREATE,
    template='claude/settings.json.j2'
)
plan.add_file(
    'scripts/start.sh',
    FileAction.CREATE,
    template='scripts/start.sh.j2',
    executable=True
)

# Preview plan summary
print(plan.summary)
# Output: "Plan: 1 directories, 2 files to create, 0 to patch, 0 skipped"
```

### Filtering Operations

```python
# Get specific operation types
new_files = plan.get_files_to_create()
overwritten = plan.get_files_to_overwrite()
patched = plan.get_files_to_patch()
skipped = plan.get_files_skipped()
executables = plan.get_executable_files()

# Print operations
for dir_op in plan.directories:
    print(dir_op)  # [mkdir] .claude/commands/

for file_op in plan.files:
    print(file_op)  # [create] .claude/settings.json
```

### Preview Before Execution

```python
# Inspect plan before applying
for dir_op in plan.directories:
    print(f"Will create: {dir_op.path}/")

for file_op in plan.get_files_to_create():
    print(f"Will create: {file_op.path}")
```

## Configuration

No configuration required. Models use Pydantic defaults and validation.

### FileAction Values

- `CREATE`: Create new file, skip if exists (idempotent)
- `OVERWRITE`: Create or replace existing file
- `PATCH`: Append content to existing file
- `SKIP`: Mark file to be skipped

### Field Validation

All models use Pydantic Field descriptors:
- Required fields: path, action
- Optional fields: template, content, reason
- Boolean flags: executable (defaults to False)

## Testing

### Test Imports

```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction, FileOperation, DirectoryOperation; print('✓ Import successful')"
```

### Test Fluent Interface

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction

plan = ScaffoldPlan()
plan.add_directory('.claude/commands', 'Claude Code commands')
plan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2')
plan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True)

print(plan.summary)
for d in plan.directories:
    print(d)
for f in plan.files:
    print(f)
"
```

### Run Full Test Suite

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

## Notes

- Models follow Domain-Driven Design (DDD) principles as pure domain logic without filesystem operations
- Fluent interface pattern enables readable, chainable plan construction
- Type safety through Pydantic ensures validation at runtime
- Separation of concerns: models represent plans, ScaffoldService will execute them
- All acceptance criteria met and validated through automated tests
- Next implementation step: ScaffoldService will consume these models to build and apply plans
