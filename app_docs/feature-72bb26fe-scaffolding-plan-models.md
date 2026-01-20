# Scaffolding Plan Models

**ADW ID:** 72bb26fe
**Date:** 2026-01-20
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/72bb26fe/specs/issue-7-adw-72bb26fe-sdlc_planner-scaffolding-plan-models.md

## Overview

This feature introduces a plan-based architecture for the TAC Bootstrap CLI scaffolding system. The new Pydantic models in `tac_bootstrap/domain/plan.py` represent a blueprint of all file and directory operations before execution, enabling preview, dry-run, and idempotent project generation.

## What Was Built

- **FileAction Enum** - Four operation types (CREATE, OVERWRITE, PATCH, SKIP) for file operations
- **FileOperation Model** - Represents individual file operations with path, action, template/content, and metadata
- **DirectoryOperation Model** - Represents directory creation with path and documentation
- **ScaffoldPlan Model** - Container for all operations with query methods, properties, and fluent interface

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py`: New file containing all scaffolding plan models (136 lines)

### Key Changes

**1. FileAction Enum (tac_bootstrap/domain/plan.py:12-17)**
- Inherits from `str, Enum` for proper JSON serialization
- Four actions: CREATE (skip if exists), OVERWRITE (replace), PATCH (append), SKIP (no-op)
- Used by FileOperation to determine operation type

**2. FileOperation Model (tac_bootstrap/domain/plan.py:20-33)**
- Required fields: `path` (relative from project root), `action` (FileAction enum)
- Optional fields: `template` (Jinja2 template name), `content` (static content), `reason` (documentation)
- `executable` flag for chmod +x support
- Custom `__str__` method returns `[{action}] {path}` format

**3. DirectoryOperation Model (tac_bootstrap/domain/plan.py:36-45)**
- Required field: `path` (relative from project root)
- Optional field: `reason` (purpose documentation)
- Custom `__str__` method returns `[mkdir] {path}/` format

**4. ScaffoldPlan Model (tac_bootstrap/domain/plan.py:48-136)**
- Contains lists of directories and files to process
- **Query Methods**: Filter files by action (get_files_to_create, get_files_to_overwrite, get_files_to_patch, get_files_skipped, get_executable_files)
- **Properties**: total_directories, total_files, summary (formatted string with counts)
- **Fluent Interface**: add_directory() and add_file() return self for method chaining

## How to Use

### Basic Plan Construction

```python
from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction

# Create empty plan
plan = ScaffoldPlan()

# Add operations one at a time
plan.add_directory('.claude/commands', 'Claude Code commands')
plan.add_file('.claude/settings.json', FileAction.CREATE, template='settings.j2')
plan.add_file('scripts/start.sh', FileAction.CREATE, executable=True)
```

### Fluent Interface (Method Chaining)

```python
plan = (ScaffoldPlan()
    .add_directory('.claude', 'Claude Code configuration')
    .add_directory('.claude/commands', 'Slash commands')
    .add_file('README.md', FileAction.CREATE, template='README.md.j2')
    .add_file('scripts/setup.sh', FileAction.CREATE, executable=True)
)
```

### Querying the Plan

```python
# Get summary
print(plan.summary)
# Output: "Plan: 2 directories, 2 files to create, 0 to patch, 0 skipped"

# Filter by operation type
for file_op in plan.get_files_to_create():
    print(f"Will create: {file_op.path}")

# Get executable files
for file_op in plan.get_executable_files():
    print(f"Make executable: {file_op.path}")

# Access properties
print(f"Total directories: {plan.total_directories}")
print(f"Total files: {plan.total_files}")
```

### Serialization

```python
import json

# Convert to dict
plan_dict = plan.model_dump()

# Convert to JSON
plan_json = json.dumps(plan.model_dump(), indent=2)
print(plan_json)
```

## Configuration

No configuration required. The models use Pydantic 2.5.0+ features and are available through:

```python
from tac_bootstrap.domain.plan import (
    ScaffoldPlan,
    FileAction,
    FileOperation,
    DirectoryOperation
)
```

## Testing

### Manual Verification

Verify imports work:
```bash
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; print('Imports OK')"
```

Test fluent interface:
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

Test query methods:
```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction

plan = ScaffoldPlan()
plan.add_file('a.txt', FileAction.CREATE)
plan.add_file('b.txt', FileAction.SKIP)
plan.add_file('c.sh', FileAction.CREATE, executable=True)

print(f'Create: {len(plan.get_files_to_create())}, Skip: {len(plan.get_files_skipped())}, Executable: {len(plan.get_executable_files())}')
"
```

### Unit Tests

No unit tests were created in this task. Future tasks will add comprehensive tests for:
- Model validation and field constraints
- Query method filtering logic
- Fluent interface chaining
- Serialization/deserialization
- Edge cases (empty plans, missing fields, etc.)

### Validation Commands

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Design Decisions

**1. Separation of Planning and Execution**
The models represent the "what" (plan), not the "how" (execution). This separation enables:
- Preview before execution (dry-run capability)
- Validation without filesystem operations
- Multiple execution strategies (parallel, sequential, with rollback)
- Progress tracking and reporting

**2. Fluent Interface Pattern**
Both add_directory() and add_file() return `self`, enabling natural method chaining:
```python
plan.add_directory('src').add_file('main.py').add_file('utils.py')
```

**3. Template vs Content Separation**
FileOperation supports both template-based files (Jinja2 rendering) and static files (direct content):
- `template`: Name of Jinja2 template to render
- `content`: Static string content
- Both optional, allowing flexibility for different file generation strategies

**4. Action-Based Filtering**
Query methods (get_files_to_create, etc.) enable easy filtering by operation type, useful for:
- Preview displays ("Will create 5 files, skip 2 existing files")
- Progress tracking during execution
- Selective execution (only create new files, skip overwrites)

**5. String Enum for Serialization**
FileAction inherits from `str, Enum` to ensure proper JSON serialization as strings rather than enum objects.

### Integration Points

These models will be used by:
- **ScaffoldService** (future task) - To build and execute plans
- **CLI commands** - To display plan previews before generation
- **Wizard** - To show what will be generated based on user selections
- **Validation** - To check plan validity before execution

### Future Enhancements

Potential improvements for future tasks:
- Validation ensuring exactly one of template/content is provided
- Path validation (no absolute paths, no parent directory traversal)
- Plan merging (combine multiple plans)
- Plan diff (compare two plans)
- Execution result tracking (success/failure per operation)
- Rollback support (undo executed plan)

### Dependencies

Uses existing dependencies from pyproject.toml:
- pydantic>=2.5.0 - Model definitions with Field()
- typing (stdlib) - Type hints (List, Optional)
- enum (stdlib) - FileAction enum
