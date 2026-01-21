# Bug: FileAction.SKIP incorrectly prevents file creation in existing repos

## Metadata
issue_number: `70`
adw_id: `b638d5b6`
issue_json: `{"number":70,"title":"Tarea 1: Corregir lógica de FileAction en scaffold_service.py","body":"## Descripción\nCambiar la lógica que determina la acción de archivos para repositorios existentes. Actualmente usa `SKIP` (nunca crea), debe usar `CREATE` (crea solo si no existe).\n\n### Prompt\n\n```\nNecesito corregir un bug en el archivo scaffold_service.py de TAC Bootstrap CLI.\n\n**Archivo**: tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py\n\n**Problema**: Cuando `existing_repo=True`, todos los archivos de templates se marcan con `FileAction.SKIP`, lo que significa que nunca se crean.\n\n**Solución**: Cambiar `FileAction.SKIP` por `FileAction.CREATE` en los siguientes métodos:\n\n1. `_add_claude_files()` - línea ~113\n2. `_add_adw_files()` - línea ~204\n3. `_add_script_files()` - línea ~284\n4. `_add_config_files()` - línea ~305\n5. `_add_structure_files()` - línea ~343\n\n**Patrón a buscar y reemplazar**:\n```python\n# ANTES\naction = FileAction.CREATE if not existing_repo else FileAction.SKIP\n\n# DESPUÉS\naction = FileAction.CREATE  # CREATE = solo crea si no existe (seguro para repos existentes)\n```\n\n**Nota**: `FileAction.CREATE` ya tiene la lógica correcta - solo crea archivos que NO existen, no sobrescribe archivos existentes del usuario.\n\n**Criterios de aceptación**:\n- [ ] Los 5 métodos usan `FileAction.CREATE` independiente de `existing_repo`\n- [ ] El parámetro `existing_repo` puede eliminarse o mantenerse para lógica futura\n- [ ] Los tests existentes siguen pasando"}`

## Bug Description
When TAC Bootstrap CLI scaffolds into an existing repository (`existing_repo=True`), all template files are marked with `FileAction.SKIP`. This prevents the CLI from creating ANY files in existing repos, even if they don't exist yet. Users expect missing files to be created while existing files are preserved.

The symptom is that running `tac-bootstrap` on an existing repository generates zero files, leaving the agentic layer incomplete.

## Problem Statement
The scaffold_service.py file uses incorrect logic to determine file actions:
```python
action = FileAction.CREATE if not existing_repo else FileAction.SKIP
```

This marks ALL files as SKIP when `existing_repo=True`, even if those files don't exist in the target directory. The result: no files are ever created in existing repositories.

## Solution Statement
Change the file action logic to always use `FileAction.CREATE` regardless of `existing_repo` status. The `FileAction.CREATE` enum already has the correct semantics per plan.py:16:
```python
CREATE = "create"  # Create new file (skip if exists)
```

This means CREATE is inherently safe - it only creates files that don't exist and skips files that do exist. The apply_plan logic at scaffold_service.py:466-469 confirms this:
```python
if file_path.exists() and file_op.action == FileAction.CREATE:
    if not force:
        result.files_skipped += 1
        continue
```

## Steps to Reproduce
1. Create a new directory with a git repository:
   ```bash
   mkdir test-existing-repo && cd test-existing-repo
   git init
   ```
2. Run TAC Bootstrap CLI targeting this existing repo
3. Observe that zero files are created because all operations are marked SKIP
4. Check plan.get_files_skipped() - all template files are in the skipped list

## Root Cause Analysis
The bug exists in 5 methods in scaffold_service.py that set `action` based on `existing_repo`:

1. **_add_claude_files()** - line 113
2. **_add_adw_files()** - line 204
3. **_add_script_files()** - line 284
4. **_add_config_files()** - line 305
5. **_add_structure_files()** - line 343

Each method contains:
```python
action = FileAction.CREATE if not existing_repo else FileAction.SKIP
```

This logic is **fundamentally wrong** because:
- `FileAction.SKIP` means "never create this file under any circumstances"
- `FileAction.CREATE` means "create if missing, skip if exists" (idempotent)
- The `existing_repo` flag should NOT determine the action; the presence/absence of the file should

The correct approach is to always use `FileAction.CREATE` because it already has built-in idempotency. The `apply_plan` method correctly checks if files exist before creating them.

**Exception:** _add_config_files() has special handling for config.yml and .gitignore which should be preserved.

## Relevant Files
Files required to fix the bug:

- **tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py** - Contains the 5 methods with incorrect logic (lines 113, 204, 284, 305, 343)
- **tac_bootstrap_cli/tac_bootstrap/domain/plan.py** - Defines FileAction enum and semantics (reference only, no changes needed)
- **tac_bootstrap_cli/tests/test_scaffold_service.py** - Tests that validate behavior, particularly test_build_plan_existing_repo_skips_files (line 134) which currently expects SKIP behavior

### New Files
No new files required.

## Step by Step Tasks

### Task 1: Update _add_claude_files() method
- Read scaffold_service.py:111-201 to confirm current line
- Replace line 113 from:
  ```python
  action = FileAction.CREATE if not existing_repo else FileAction.SKIP
  ```
  to:
  ```python
  action = FileAction.CREATE  # CREATE = only creates if file doesn't exist (safe for existing repos)
  ```

### Task 2: Update _add_adw_files() method
- Replace line 204 from:
  ```python
  action = FileAction.CREATE if not existing_repo else FileAction.SKIP
  ```
  to:
  ```python
  action = FileAction.CREATE  # CREATE = only creates if file doesn't exist (safe for existing repos)
  ```

### Task 3: Update _add_script_files() method
- Replace line 284 from:
  ```python
  action = FileAction.CREATE if not existing_repo else FileAction.SKIP
  ```
  to:
  ```python
  action = FileAction.CREATE  # CREATE = only creates if file doesn't exist (safe for existing repos)
  ```

### Task 4: Update _add_config_files() method
- Replace line 305 from:
  ```python
  action = FileAction.CREATE if not existing_repo else FileAction.SKIP
  ```
  to:
  ```python
  action = FileAction.CREATE  # CREATE = only creates if file doesn't exist (safe for existing repos)
  ```
- Note: config.yml already has special OVERWRITE logic at line 310, .gitignore has PATCH logic at line 334 - these should remain unchanged

### Task 5: Update _add_structure_files() method
- Replace line 343 from:
  ```python
  action = FileAction.CREATE if not existing_repo else FileAction.SKIP
  ```
  to:
  ```python
  action = FileAction.CREATE  # CREATE = only creates if file doesn't exist (safe for existing repos)
  ```

### Task 6: Update test expectations
- Read tests/test_scaffold_service.py:134-142 (test_build_plan_existing_repo_skips_files)
- This test currently expects files to be SKIPped in existing repos
- Update the test to verify that files are marked CREATE but will be skipped during apply_plan if they already exist
- The test should validate that apply_plan correctly skips existing files, not that build_plan marks them as SKIP

### Task 7: Run validation commands
- Execute all validation commands below to ensure zero regressions
- All tests must pass
- No linting or type errors
- CLI smoke test must work

## Validation Commands
Execute all commands to validate the fix with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v --tb=short` - Scaffold service tests
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes
- The `existing_repo` parameter can remain in the method signatures for potential future use (e.g., different README templates, conditional logic)
- The fix is surgical: change only the 5 action assignments, add comments for clarity
- FileAction.CREATE is already idempotent by design - it checks file existence in apply_plan before creating
- This fix enables TAC Bootstrap to safely scaffold into existing repos by creating missing files while preserving existing ones
- After this fix, users can run `tac-bootstrap` on existing projects to add the agentic layer without losing any existing files
