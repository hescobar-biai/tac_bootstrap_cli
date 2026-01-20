# FileSystem Operations Module

**ADW ID:** b6479a0a
**Date:** 2026-01-20
**Specification:** specs/issue-30-adw-b6479a0a-sdlc_planner-filesystem-operations.md

## Overview

This feature implements a comprehensive filesystem operations module that provides the ScaffoldService with safe, idempotent, and cross-platform methods for creating, reading, writing, and managing files and directories during project scaffold generation.

## What Was Built

A complete `FileSystem` class in the infrastructure layer with the following capabilities:

- **Directory operations**: Idempotent directory creation with automatic parent directory handling
- **File writing**: Safe file creation with auto-parent directory creation
- **Idempotent appending**: Append content to files while avoiding duplication
- **Permission management**: Cross-platform executable permission setting
- **File reading**: Safe file reading with default value fallback
- **File manipulation**: Copy, remove files and directories
- **Cross-platform compatibility**: Built on `pathlib.Path` for Windows/Unix portability

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py`: **NEW** - Complete filesystem operations module (222 lines)
  - Implements `FileSystem` class with 10 public methods
  - Comprehensive docstrings with usage examples
  - Safe error handling for edge cases

### Key Changes

1. **Idempotent Operations**: Methods like `ensure_directory()` and `append_file()` are designed to be called multiple times without side effects
2. **Auto-parent Creation**: All write operations automatically create missing parent directories using `path.parent.mkdir(parents=True, exist_ok=True)`
3. **Smart Permission Handling**: `make_executable()` preserves existing permissions and conditionally adds execute permissions based on read permissions
4. **Duplicate Detection**: `append_file()` checks if content already exists before appending, preventing duplicate entries
5. **Safe Defaults**: Read operations return configurable default values instead of raising exceptions for missing files

## How to Use

### Basic File Operations

```python
from pathlib import Path
from tac_bootstrap.infrastructure.fs import FileSystem

fs = FileSystem()

# Create directories (idempotent)
fs.ensure_directory(Path("my_project/src/components"))

# Write a file (creates parent directories automatically)
fs.write_file(
    Path("my_project/README.md"),
    "# My Project\n\nWelcome!"
)

# Read a file (with safe default)
content = fs.read_file(Path("config.yml"), default="")

# Check if file/directory exists
if fs.file_exists(Path("package.json")):
    print("Found package.json")
```

### Idempotent Append

```python
# Append content without duplication
fs.append_file(
    Path(".gitignore"),
    "__pycache__/\n*.pyc",
    separator="\n"
)

# Calling again won't duplicate the content
fs.append_file(
    Path(".gitignore"),
    "__pycache__/\n*.pyc",  # Already present, no-op
    separator="\n"
)
```

### Make Scripts Executable

```python
# Add execute permissions to shell scripts
fs.write_file(Path("scripts/deploy.sh"), "#!/bin/bash\necho 'Deploying...'")
fs.make_executable(Path("scripts/deploy.sh"))

# Now the script can be executed directly
# ./scripts/deploy.sh
```

### Copy and Remove Operations

```python
# Copy files while preserving metadata
fs.copy_file(
    Path("template/config.yml"),
    Path("my_project/config.yml")
)

# Remove a file
was_removed = fs.remove_file(Path("temp.txt"))

# Remove directory recursively
fs.remove_directory(Path("build/"), recursive=True)
```

## Configuration

No configuration required. The module uses UTF-8 encoding by default for all text operations, which can be overridden via the `encoding` parameter on individual methods.

Default separator for `append_file()` is double newline (`"\n\n"`), configurable via the `separator` parameter.

## Integration with ScaffoldService

The `ScaffoldService` uses this module to execute file operations defined in scaffold plans:

```python
# In ScaffoldService.apply_plan()
from tac_bootstrap.infrastructure.fs import FileSystem

fs = FileSystem()

for file_op in plan.file_operations:
    if file_op.action == FileAction.CREATE:
        fs.write_file(file_op.path, file_op.content)
    elif file_op.action == FileAction.APPEND:
        fs.append_file(file_op.path, file_op.content)
```

## Testing

### Manual Testing

Test the module with an inline script:

```bash
cd tac_bootstrap_cli && uv run python -c "
from pathlib import Path
import tempfile
from tac_bootstrap.infrastructure.fs import FileSystem

fs = FileSystem()
with tempfile.TemporaryDirectory() as tmpdir:
    base = Path(tmpdir)

    # Test directory creation
    fs.ensure_directory(base / 'a/b/c')
    print(f'Created nested dir: {(base / \"a/b/c\").is_dir()}')

    # Test file write
    fs.write_file(base / 'test.txt', 'Hello World')
    print(f'File content: {(base / \"test.txt\").read_text()}')

    # Test idempotent append
    fs.append_file(base / 'notes.txt', 'First note')
    fs.append_file(base / 'notes.txt', 'Second note')
    fs.append_file(base / 'notes.txt', 'First note')  # Should not duplicate
    print(f'Notes file: {(base / \"notes.txt\").read_text()}')
"
```

### Unit Tests

Run the existing test suite:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Integration Test

Verify ScaffoldService integration:

```bash
cd tac_bootstrap_cli && uv run python -c "
from pathlib import Path
import tempfile
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.config import TACConfig, ProjectConfig

service = ScaffoldService()
config = TACConfig(project=ProjectConfig(name='test_project', root_dir=Path.cwd()))

with tempfile.TemporaryDirectory() as tmpdir:
    plan = service.build_plan(config, Path(tmpdir))
    result = service.apply_plan(plan)
    print(f'Success: {result.success}')
    print(f'Files created: {result.files_created}')
    print(f'Dirs created: {result.dirs_created}')
"
```

## Notes

- The module does NOT include git operations - those belong in a separate `git_adapter` module
- All operations use UTF-8 encoding by default for consistency across platforms
- The duplicate detection in `append_file()` uses substring matching (`content.strip() in existing`), which may produce false positives if the new content is a substring of existing content, but this is sufficient for current use cases
- `make_executable()` only adds execute permissions where read permissions already exist (following Unix security principles)
- Return values are provided only where useful (e.g., `ensure_directory()` returns `bool` to indicate if directory was created)
- The module silently handles edge cases like nonexistent files in `read_file()` and `make_executable()`, returning defaults or no-op respectively
