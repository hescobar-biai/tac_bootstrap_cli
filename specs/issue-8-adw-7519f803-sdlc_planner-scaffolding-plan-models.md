# Feature: Scaffolding Plan Models

## Metadata
issue_number: `8`
adw_id: `7519f803`
issue_json: `{"number":8,"title":"feat: #7 - TAREA 2.2: Crear modelos de plan de scaffolding","body":"## Summary\n\nThis PR implements Pydantic models for scaffolding plan operations, enabling the ScaffoldService to build a plan of operations before executing them. This allows for dry-run, preview, and idempotent scaffolding.\n\n## Implementation Plan\n\nSee: specs/issue-7-adw-72bb26fe-sdlc_planner-scaffolding-plan-models.md\n\n## Changes\n\n- Created specification document for scaffolding plan models\n- Defined FileAction enum with CREATE, OVERWRITE, PATCH, and SKIP actions\n- Implemented FileOperation model for individual file operations\n- Implemented DirectoryOperation model for directory creation\n- Implemented ScaffoldPlan model with helper methods and fluent interface\n\n## Key Features\n\n- FileAction enum: Supports multiple operation types\n- Fluent interface: Chain add_directory and add_file calls\n- Helper methods: Filter operations by type\n- Plan summary: Quick overview of operations\n\n## ADW Tracking\n\nADW ID: 72bb26fe\n\nCloses #7"}`

## Feature Description

Create Pydantic models for scaffolding plan operations in `tac_bootstrap/domain/plan.py`. These models enable the ScaffoldService to build a structured plan of operations before executing them, allowing for:

1. **Dry-run capability** - Preview operations without touching the filesystem
2. **Plan validation** - Verify operations before execution
3. **Idempotent scaffolding** - Safely re-run operations with proper skip/overwrite logic
4. **Conflict detection** - Identify duplicate or conflicting operations at plan time
5. **Progress tracking** - Monitor execution with clear operation states

The plan models provide a declarative interface for building project structures with support for directories, file creation, overwrites, patches, and executable permissions.

## User Story

As a **TAC Bootstrap CLI developer**
I want to **represent scaffolding operations as a structured, validated plan**
So that **I can preview, validate, and execute project generation safely with clear conflict resolution**

## Problem Statement

The ScaffoldService needs a robust data structure to represent complex project generation operations:

- Multiple directories at various nesting levels
- Files generated from Jinja2 templates with context variables
- Static content files without templates
- Files that should skip if they already exist (CREATE)
- Files that should overwrite existing content (OVERWRITE)
- Files that should append/patch existing content (PATCH)
- Executable permission management for scripts
- Path traversal prevention for security
- Conflict detection when multiple operations target the same path

Without structured plan models:
- Cannot preview what will be created before execution
- Cannot implement safe dry-run functionality
- Cannot detect conflicts between operations at plan time
- Cannot track operation states during execution
- Cannot ensure idempotent scaffolding (safe re-runs)
- Security vulnerabilities from path traversal attacks

## Solution Statement

Implement three Pydantic models with enhanced validation and security:

1. **FileAction Enum** - Defines operation types (CREATE, OVERWRITE, PATCH, SKIP) with clear semantics
2. **FileOperation Model** - Represents individual file operations with:
   - Path validation (relative paths only, no traversal)
   - Action type (CREATE, OVERWRITE, PATCH, SKIP)
   - Template or content specification
   - Optional metadata dict for extensibility
   - Executable flag for permissions
3. **DirectoryOperation Model** - Represents directory creation with:
   - Path validation (relative paths only, no traversal)
   - Recursive creation support (mkdir -p behavior)
   - Optional reason/documentation
4. **ScaffoldPlan Model** - Container with validation and query capabilities:
   - Fluent interface for building plans
   - Conflict detection for duplicate paths
   - Filtering methods by operation type
   - JSON serialization via Pydantic
   - Plan summary and statistics

Key design decisions from clarifications:
- **Validation**: Paths must be relative, no '..' traversal, non-empty
- **PATCH format**: Unified diff format (industry standard)
- **Conflict resolution**: Service layer handles based on configuration
- **Dependencies**: Sequential execution, directories before files
- **Serialization**: JSON via Pydantic's built-in support
- **SKIP logic**: Auto-determined at execution time, not in plan
- **Extensibility**: Metadata dict for future features

## Relevant Files

Files necessary for implementing the feature:

### Existing Files to Reference
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Existing domain model patterns
- `tac_bootstrap_cli/tac_bootstrap/domain/validators.py` - Validation utilities
- `tac_bootstrap_cli/pyproject.toml` - Verify Pydantic 2.5+ dependency
- `specs/issue-7-adw-72bb26fe-sdlc_planner-scaffolding-plan-models.md` - Original specification

### New Files
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Plan models (already implemented)

### Files to Update
None - models are already complete and integrated

## Implementation Plan

### Phase 1: Foundation ✅ COMPLETED
Basic enum and operation models:
- ✅ FileAction enum with CREATE, OVERWRITE, PATCH, SKIP
- ✅ FileOperation model with path, action, template, content, executable
- ✅ DirectoryOperation model with path and reason
- ✅ __str__ methods for human-readable output

### Phase 2: Core Implementation ✅ COMPLETED
ScaffoldPlan container with query capabilities:
- ✅ ScaffoldPlan model with directories and files lists
- ✅ Filtering methods (get_files_to_create, get_files_to_overwrite, etc.)
- ✅ Property methods (total_directories, total_files, summary)
- ✅ Fluent interface (add_directory, add_file return self)

### Phase 3: Validation and Testing
Ensure models work correctly and handle edge cases:
- ✅ Import validation
- ✅ Model instantiation
- ✅ Fluent interface chaining
- ✅ JSON serialization
- Run full validation suite

## Step by Step Tasks

### Task 1: Verify Implementation Completeness ✅
- Read `tac_bootstrap_cli/tac_bootstrap/domain/plan.py`
- Confirm all models match specification
- Verify FileAction enum has all actions
- Verify FileOperation has all required fields
- Verify DirectoryOperation structure
- Verify ScaffoldPlan has all methods and properties

### Task 2: Test Model Imports
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction, FileOperation, DirectoryOperation; print('Imports OK')"`
- Verify no import errors
- Confirm all classes are accessible

### Task 3: Test Basic Instantiation
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan(); plan.add_directory('.claude/commands', 'Claude Code commands'); plan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2'); plan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True); print(plan.summary); [print(d) for d in plan.directories]; [print(f) for f in plan.files]"`
- Verify plan creation works
- Verify summary output is correct
- Verify operations print correctly

### Task 4: Test Fluent Interface Chaining
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_directory('.claude').add_directory('.claude/commands').add_file('README.md', FileAction.CREATE).add_file('LICENSE', FileAction.CREATE); print(f'{plan.total_directories} directories, {plan.total_files} files')"`
- Verify method chaining works
- Verify counts are accurate

### Task 5: Test Query Methods
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_file('new.txt', FileAction.CREATE).add_file('skip.txt', FileAction.SKIP).add_file('overwrite.txt', FileAction.OVERWRITE).add_file('patch.diff', FileAction.PATCH).add_file('script.sh', FileAction.CREATE, executable=True); print(f'Create: {len(plan.get_files_to_create())}'); print(f'Skip: {len(plan.get_files_skipped())}'); print(f'Overwrite: {len(plan.get_files_to_overwrite())}'); print(f'Patch: {len(plan.get_files_to_patch())}'); print(f'Executable: {len(plan.get_executable_files())}')"`
- Verify filtering by CREATE returns 2 (new.txt + script.sh)
- Verify filtering by SKIP returns 1
- Verify filtering by OVERWRITE returns 1
- Verify filtering by PATCH returns 1
- Verify executable filtering returns 1

### Task 6: Test JSON Serialization
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_directory('src').add_directory('tests').add_file('src/main.py', FileAction.CREATE).add_file('tests/test_main.py', FileAction.CREATE); import json; data = plan.model_dump(); print(json.dumps(data, indent=2)); restored = ScaffoldPlan(**data); print(f'Serialization OK: {restored.total_directories} dirs, {restored.total_files} files')"`
- Verify plan serializes to valid JSON
- Verify plan can be deserialized from JSON
- Verify round-trip preserves data

### Task 7: Test Edge Cases
- Run: `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; empty = ScaffoldPlan(); print(f'Empty plan: {empty.summary}'); dirs_only = ScaffoldPlan().add_directory('a').add_directory('b'); print(f'Dirs only: {dirs_only.summary}'); files_only = ScaffoldPlan().add_file('x.txt', FileAction.CREATE); print(f'Files only: {files_only.summary}')"`
- Verify empty plan works (0 directories, 0 files)
- Verify directories-only plan works
- Verify files-only plan works

### Task 8: Run Linting
- Run: `cd tac_bootstrap_cli && uv run ruff check .`
- Verify no linting errors in plan.py
- Fix any style issues if found

### Task 9: Run Type Checking
- Run: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Verify no type errors in plan.py
- Ensure all type hints are correct

### Task 10: Run Unit Tests
- Run: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Verify all existing tests pass
- Ensure no regressions introduced

### Task 11: Run Smoke Test
- Run: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
- Verify CLI still works
- Ensure no import errors from plan.py

### Task 12: Validation Complete
Execute all validation commands in sequence:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```
- Verify all commands pass with zero errors
- Confirm implementation is complete and ready

## Testing Strategy

### Unit Tests
Manual verification via command-line tests covers:
- Model imports and instantiation
- Fluent interface chaining
- Query methods (filtering by action)
- Property methods (counts, summary)
- JSON serialization/deserialization
- Edge cases (empty plans, partial plans)

Comprehensive unit tests will be added in future tasks when test infrastructure is established.

### Edge Cases Tested
1. **Empty plans** - No directories, no files
2. **Partial plans** - Only directories or only files
3. **Multiple actions** - Mix of CREATE, SKIP, OVERWRITE, PATCH
4. **Executable files** - Files with executable flag set
5. **Serialization** - JSON round-trip preserves data
6. **Chaining** - Fluent interface with multiple operations
7. **Filtering** - Query methods return correct subsets

### Security Considerations
Path validation (to be implemented in service layer):
- Reject absolute paths (starting with /)
- Reject paths with '..' traversal
- Validate paths are non-empty
- Ensure paths are within project boundary

## Acceptance Criteria

1. ✅ **File Exists** - `tac_bootstrap/domain/plan.py` is implemented
2. ✅ **Enum Complete** - FileAction has CREATE, OVERWRITE, PATCH, SKIP
3. ✅ **Models Valid** - FileOperation, DirectoryOperation, ScaffoldPlan are Pydantic models
4. ✅ **Query Methods** - get_files_to_create, get_files_to_overwrite, get_files_to_patch, get_files_skipped work
5. ✅ **Properties Work** - total_directories, total_files, summary return correct values
6. ✅ **Fluent Interface** - add_directory and add_file return self for chaining
7. ✅ **String Repr** - __str__ methods return formatted output
8. ✅ **Imports Work** - All classes importable from tac_bootstrap.domain.plan
9. **Verification Pass** - All manual test commands execute successfully
10. **No Regressions** - All validation commands pass (pytest, ruff, mypy, smoke test)

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

All commands must pass with no errors.

## Notes

### Implementation Status

The implementation is **COMPLETE**. The plan.py file exists with all required models:
- FileAction enum with all four actions
- FileOperation model with all fields
- DirectoryOperation model with path and reason
- ScaffoldPlan model with all methods and properties

This plan document serves to:
1. Document the implementation that was completed for issue #7
2. Provide validation steps to ensure correctness
3. Establish acceptance criteria for tracking purposes
4. Reference design decisions from the clarification phase

### Design Decisions Applied

Based on auto-resolved clarifications:

1. **Path Validation** - Model accepts any string, service layer will validate:
   - Relative paths only (no leading /)
   - No '..' traversal components
   - Non-empty paths

2. **PATCH Format** - Unified diff format:
   - Store in optional 'patch_content' field (to be added when needed)
   - Industry standard, human-readable
   - Compatible with git and patch command

3. **Conflict Resolution** - Service layer responsibility:
   - Model represents intent, not execution state
   - Filesystem state can change between plan creation and execution
   - Service has context for conflict resolution strategy

4. **No Size Limit** - No hard limit on plan operations:
   - Typical scaffolding: dozens to hundreds of files
   - Add warnings/limits only if real-world usage shows issues

5. **Minimal Metadata** - Simple fields with extensibility:
   - Core fields: action, path, template/content
   - Metadata dict for future additions
   - Prevents premature complexity

6. **Sequential Execution** - No explicit dependency system:
   - Operations execute in order added
   - Service ensures directories created before files
   - Covers 95% of use cases without complexity

7. **Duplicate Detection** - Plan validation time:
   - Raise ValidationError if duplicate target_path with different actions
   - Last operation wins if actions identical
   - Fail fast with clear error

8. **Recursive Directories** - mkdir -p behavior:
   - Store 'ensure_parents: bool = True' field
   - Matches user expectations and standard tooling
   - Reduces coupling between operations

9. **JSON Serialization** - Pydantic built-in:
   - model_dump_json() and model_validate_json()
   - Universal, human-readable
   - Sufficient for all requirements

10. **SKIP Auto-Detection** - Runtime determination:
    - Plan represents desired state
    - Service checks existence and adds SKIP to execution report
    - Keeps plans clean and filesystem-agnostic

### Dependencies

All dependencies already available in pyproject.toml:
- `pydantic>=2.5.0` - Model definitions and validation
- `typing` (stdlib) - Type hints (Optional, List)
- `enum` (stdlib) - Enum base class

No additional dependencies required.

### Future Integration

These models will integrate with:
- **ScaffoldService.build_plan()** - Construct plans from TACConfig (future task)
- **ScaffoldService.apply_plan()** - Execute plans and create files/directories (future task)
- **CLI preview commands** - Display plan before execution
- **Interactive wizard** - Show what will be generated based on user choices
- **Validation layer** - Path security checks, conflict detection
- **Execution reporter** - Track progress and outcomes

### Security Notes

Path validation requirements for service layer:
- **Prevent traversal** - Reject paths with '..'
- **Relative only** - Reject absolute paths (leading /)
- **Non-empty** - Reject empty path strings
- **Boundary check** - Ensure paths stay within project directory

These validations are deferred to service layer because:
- Filesystem constraints vary by OS
- Model validates structure, service validates existence/permissions
- Separation of concerns (model = intent, service = execution)
