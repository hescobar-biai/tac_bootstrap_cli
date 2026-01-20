# Git Adapter

**ADW ID:** 8a2e9cbb
**Date:** 2026-01-20
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/8a2e9cbb/specs/issue-32-adw-8a2e9cbb-sdlc_planner-git-adapter.md

## Overview

The Git Adapter provides a clean, safe abstraction layer for Git operations during project scaffolding and AI Developer Workflows (ADWs). It encapsulates subprocess calls to Git commands and provides structured results with consistent error handling.

## What Was Built

- **GitResult Dataclass**: Structured result type for all Git operations with `success`, `output`, and `error` fields
- **GitAdapter Class**: Main adapter providing 15+ Git operations
- **Repository Operations**: `init()`, `is_repo()` for repository management
- **Staging Operations**: `add()`, `add_all()` for staging changes
- **Commit Operations**: `commit()` with configurable options including empty commits
- **Status Operations**: `status()`, `has_changes()` for checking repository state
- **Branch Operations**: `get_current_branch()`, `branch_exists()`, `checkout()` with create option
- **Worktree Operations**: `create_worktree()`, `remove_worktree()`, `list_worktrees()` for parallel development
- **Remote Operations**: `get_remote_url()` for querying remote configurations
- **Robust Error Handling**: Catches `CalledProcessError` and `FileNotFoundError` (git not installed)

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`: Created new infrastructure module (267 lines)
  - Implements `GitResult` dataclass for structured return values
  - Implements `GitAdapter` class with 15 Git operations
  - Provides comprehensive docstrings and type hints

### Key Changes

1. **Structured Results**: All Git operations return `GitResult` instead of raw subprocess output, enabling consistent error handling across the codebase

2. **Stateless Design**: The adapter maintains only `repo_path` as state; each operation is independent and can fail gracefully without affecting internal state

3. **Defensive Programming**:
   - Base `_run()` method catches `FileNotFoundError` (git not installed) and `CalledProcessError` (command failures)
   - Methods that query state (like `branch_exists()`, `get_remote_url()`) use `check=False` to avoid exceptions on expected failures
   - All methods return structured data (`GitResult`, `bool`, `Optional[str]`, `List[str]`)

4. **Porcelain Parsing**: `list_worktrees()` uses `--porcelain` format for reliable machine-readable output parsing

5. **Smart Defaults**: Operations like `create_worktree()` default to creating new branches (`create_branch=True`) since this is the common ADW use case

## How to Use

### Basic Repository Operations

```python
from pathlib import Path
from tac_bootstrap.infrastructure.git_adapter import GitAdapter

# Initialize a new repository
adapter = GitAdapter(Path("my_project"))
result = adapter.init(initial_branch="main")
if result.success:
    print("Repository initialized")
else:
    print(f"Error: {result.error}")

# Check if path is a git repository
if adapter.is_repo():
    print("This is a git repository")
```

### Staging and Committing

```python
# Stage all changes
adapter.add_all()

# Stage specific files
adapter.add("src/main.py", "README.md")

# Create a commit
result = adapter.commit("Initial commit")
if result.success:
    print("Commit created successfully")

# Create an empty commit (useful for testing)
adapter.commit("Empty commit", allow_empty=True)
```

### Checking Repository Status

```python
# Get status (porcelain format for parsing)
result = adapter.status(porcelain=True)
print(result.output)

# Get human-readable status
result = adapter.status(porcelain=False)
print(result.output)

# Quick check for uncommitted changes
if adapter.has_changes():
    print("There are uncommitted changes")
```

### Branch Operations

```python
# Get current branch
branch = adapter.get_current_branch()
print(f"Current branch: {branch}")

# Check if branch exists
if adapter.branch_exists("feature-x"):
    print("Branch exists")

# Checkout existing branch
adapter.checkout("develop")

# Create and checkout new branch
adapter.checkout("feature-new", create=True)
```

### Worktree Operations (for ADWs)

```python
from pathlib import Path

# Create a new worktree with a new branch
result = adapter.create_worktree(
    path=Path("../my-feature-worktree"),
    branch="feature-x",
    create_branch=True
)

# List all worktrees
worktrees = adapter.list_worktrees()
for wt in worktrees:
    print(f"Worktree: {wt}")

# Remove a worktree
adapter.remove_worktree(Path("../my-feature-worktree"))

# Force remove worktree with uncommitted changes
adapter.remove_worktree(Path("../my-feature-worktree"), force=True)
```

### Remote Operations

```python
# Get origin URL
url = adapter.get_remote_url("origin")
if url:
    print(f"Origin URL: {url}")
else:
    print("No origin remote configured")
```

## Configuration

The GitAdapter requires no configuration files. It only needs:

1. **Git Installation**: Git must be installed and available in PATH
2. **Repository Path**: A valid Path object pointing to the repository (or where it will be created)

The adapter automatically:
- Detects if git is not installed (returns `GitResult(success=False, error="Git is not installed or not in PATH")`)
- Handles non-existent paths gracefully
- Uses the repository's `.git` directory for all operations via `cwd` parameter

## Testing

### Manual Testing

Test all operations in a temporary repository:

```bash
cd tac_bootstrap_cli && uv run python -c "
import tempfile
from pathlib import Path
from tac_bootstrap.infrastructure.git_adapter import GitAdapter

with tempfile.TemporaryDirectory() as tmp:
    adapter = GitAdapter(Path(tmp))

    # Test init
    print('Testing init...', adapter.init().success)

    # Test is_repo
    print('Testing is_repo...', adapter.is_repo())

    # Test current branch
    print('Testing get_current_branch...', adapter.get_current_branch())

    # Test staging and commit
    (Path(tmp) / 'test.txt').write_text('hello')
    adapter.add_all()
    print('Testing commit...', adapter.commit('Test commit').success)

    # Test status
    print('Testing has_changes...', adapter.has_changes())
"
```

### Automated Testing

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "git"
```

### Validation Commands

Run all validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Scope Limitations

The adapter intentionally does NOT implement operations requiring remote authentication:
- `push` - Requires authentication, outside scope
- `pull` / `fetch` - Remote operations not needed for scaffolding
- `clone` - Not needed for scaffolding (we create repos, not clone them)

### Design Decisions

1. **Why GitResult?** Provides consistent error handling across all Git operations without exceptions for expected failures

2. **Why stateless?** Each operation is independent, making the adapter safe to use in concurrent workflows (ADWs)

3. **Why text=True?** All output is captured as strings for easier parsing and display to users

4. **Why check=False for queries?** Methods like `branch_exists()` or `get_remote_url()` need to handle "not found" as a valid state, not an error

5. **Why porcelain format?** Machine-readable output is more reliable for parsing in `list_worktrees()` and `status()`

### Integration Points

This adapter is designed to be used by:
- **ScaffoldService**: For `git init` and initial commits during project generation
- **ADW Workflows**: For worktree management in isolated development environments
- **Future Tools**: Any component needing safe, structured Git operations

### Edge Cases Handled

- Git not installed: Returns `GitResult(success=False)` with descriptive error
- Non-existent branches: `branch_exists()` returns `False` without raising
- Non-existent remotes: `get_remote_url()` returns `None` without raising
- Detached HEAD: `get_current_branch()` returns `None`
- Empty worktree list: `list_worktrees()` returns `[]` if command fails
- Failed commits: Captured gracefully in `GitResult.error`
