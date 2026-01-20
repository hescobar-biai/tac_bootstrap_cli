# Feature: Scaffolding Plan Models

## Metadata
issue_number: `7`
adw_id: `72bb26fe`
issue_json: `{"number":7,"title":"TAREA 2.2: Crear modelos de plan de scaffolding","body":"# Prompt para Agente\n\n## Contexto\nEl ScaffoldService necesita construir un \"plan\" de operaciones antes de ejecutarlas.\nEste plan contiene listas de directorios a crear y archivos a generar/modificar.\nEsto permite hacer dry-run, mostrar preview, y mantener idempotencia.\n\n## Objetivo\nCrear modelos Pydantic que representen el plan de scaffolding con operaciones\nde archivos y directorios.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Scaffolding plan models.\n\nThese models represent the plan of operations to execute when scaffolding\na project. The plan is built first, then can be previewed or executed.\n\"\"\"\nfrom enum import Enum\nfrom typing import Optional, List\nfrom pydantic import BaseModel, Field\n\n\nclass FileAction(str, Enum):\n    \"\"\"Type of file operation to perform.\"\"\"\n    CREATE = \"create\"    # Create new file (skip if exists)\n    OVERWRITE = \"overwrite\"  # Create or overwrite existing\n    PATCH = \"patch\"      # Append to existing file\n    SKIP = \"skip\"        # Skip this file\n\n\nclass FileOperation(BaseModel):\n    \"\"\"Single file operation in the scaffold plan.\n\n    Represents one file to be created, modified, or skipped.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    action: FileAction = Field(..., description=\"Type of operation\")\n    template: Optional[str] = Field(None, description=\"Jinja2 template name to render\")\n    content: Optional[str] = Field(None, description=\"Static content (if no template)\")\n    reason: Optional[str] = Field(None, description=\"Why this file is needed\")\n    executable: bool = Field(False, description=\"Make file executable after creation\")\n\n    def __str__(self) -> str:\n        return f\"[{self.action.value}] {self.path}\"\n\n\nclass DirectoryOperation(BaseModel):\n    \"\"\"Directory creation operation.\n\n    Represents a directory to be created.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    reason: str = Field(\"\", description=\"Purpose of this directory\")\n\n    def __str__(self) -> str:\n        return f\"[mkdir] {self.path}/\"\n\n\nclass ScaffoldPlan(BaseModel):\n    \"\"\"Complete scaffold plan for generation.\n\n    Contains all directories and files to be created/modified.\n    The plan is built first, allowing preview and validation before execution.\n\n    Example:\n        ```python\n        plan = scaffold_service.build_plan(config)\n\n        # Preview what will be created\n        for dir_op in plan.directories:\n            print(f\"Will create: {dir_op.path}/\")\n\n        for file_op in plan.get_files_to_create():\n            print(f\"Will create: {file_op.path}\")\n\n        # Execute the plan\n        scaffold_service.apply_plan(plan, output_dir)\n        ```\n    \"\"\"\n    directories: List[DirectoryOperation] = Field(default_factory=list)\n    files: List[FileOperation] = Field(default_factory=list)\n\n    def get_files_to_create(self) -> List[FileOperation]:\n        \"\"\"Get files that will be created (new files only).\"\"\"\n        return [f for f in self.files if f.action == FileAction.CREATE]\n\n    def get_files_to_overwrite(self) -> List[FileOperation]:\n        \"\"\"Get files that will be overwritten.\"\"\"\n        return [f for f in self.files if f.action == FileAction.OVERWRITE]\n\n    def get_files_to_patch(self) -> List[FileOperation]:\n        \"\"\"Get files that will be patched (appended to).\"\"\"\n        return [f for f in self.files if f.action == FileAction.PATCH]\n\n    def get_files_skipped(self) -> List[FileOperation]:\n        \"\"\"Get files that will be skipped.\"\"\"\n        return [f for f in self.files if f.action == FileAction.SKIP]\n\n    def get_executable_files(self) -> List[FileOperation]:\n        \"\"\"Get files that need to be made executable.\"\"\"\n        return [f for f in self.files if f.executable]\n\n    @property\n    def total_directories(self) -> int:\n        \"\"\"Total number of directories to create.\"\"\"\n        return len(self.directories)\n\n    @property\n    def total_files(self) -> int:\n        \"\"\"Total number of file operations.\"\"\"\n        return len(self.files)\n\n    @property\n    def summary(self) -> str:\n        \"\"\"Get a summary of the plan.\"\"\"\n        creates = len(self.get_files_to_create())\n        patches = len(self.get_files_to_patch())\n        skips = len(self.get_files_skipped())\n        return (\n            f\"Plan: {self.total_directories} directories, \"\n            f\"{creates} files to create, {patches} to patch, {skips} skipped\"\n        )\n\n    def add_directory(self, path: str, reason: str = \"\") -> \"ScaffoldPlan\":\n        \"\"\"Add a directory to the plan (fluent interface).\"\"\"\n        self.directories.append(DirectoryOperation(path=path, reason=reason))\n        return self\n\n    def add_file(\n        self,\n        path: str,\n        action: FileAction = FileAction.CREATE,\n        template: Optional[str] = None,\n        content: Optional[str] = None,\n        reason: Optional[str] = None,\n        executable: bool = False,\n    ) -> \"ScaffoldPlan\":\n        \"\"\"Add a file operation to the plan (fluent interface).\"\"\"\n        self.files.append(FileOperation(\n            path=path,\n            action=action,\n            template=template,\n            content=content,\n            reason=reason,\n            executable=executable,\n        ))\n        return self\n```\n\n## Criterios de Aceptacion\n1. [ ] Archivo `plan.py` creado\n2. [ ] FileAction enum con todas las acciones\n3. [ ] Metodos helper en ScaffoldPlan funcionan\n4. [ ] Fluent interface permite encadenar add_directory/add_file\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv run python -c \"\nfrom tac_bootstrap.domain.plan import ScaffoldPlan, FileAction\n\nplan = ScaffoldPlan()\nplan.add_directory('.claude/commands', 'Claude Code commands')\nplan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2')\nplan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True)\n\nprint(plan.summary)\nfor d in plan.directories:\n    print(d)\nfor f in plan.files:\n    print(f)\n\"\n```\n\n## NO hacer\n- No implementar la logica de ejecucion del plan (eso va en scaffold_service)"}`

## Feature Description

Create Pydantic models in `tac_bootstrap/domain/plan.py` that represent the scaffolding plan - a blueprint of all file and directory operations that will be executed when generating a project structure. This plan-based architecture enables:

1. **Preview Before Execution** - Users can see exactly what will be created/modified before committing to changes
2. **Dry-Run Capability** - The plan can be validated without touching the filesystem
3. **Idempotency** - Operations can be safely re-run with proper skip/overwrite logic
4. **Separation of Concerns** - Planning logic (what to do) is decoupled from execution logic (how to do it)

The plan models will be used by the ScaffoldService (to be implemented in future tasks) to coordinate file generation, template rendering, and directory structure creation.

## User Story

As a **TAC Bootstrap CLI developer**
I want to **represent scaffolding operations as a structured plan**
So that **I can preview, validate, and execute project generation in a controlled, repeatable manner**

## Problem Statement

The ScaffoldService needs to generate complex project structures with:
- Multiple directories across different levels
- Files created from Jinja2 templates
- Files with static content
- Some files that should be skipped if they already exist
- Some files that need executable permissions

Currently, there's no data structure to represent this plan of operations. Without a plan model:
- We cannot preview what will be created before execution
- We cannot implement dry-run functionality
- We cannot track which operations succeeded/failed
- We cannot maintain idempotency (safe re-runs)

## Solution Statement

Create three Pydantic models that work together as a planning system:

1. **FileAction Enum** - Defines the type of file operation (CREATE, OVERWRITE, PATCH, SKIP)
2. **FileOperation Model** - Represents a single file operation with path, action, template/content, and metadata
3. **DirectoryOperation Model** - Represents a directory to create with path and purpose
4. **ScaffoldPlan Model** - Container for all operations with helper methods for querying, filtering, and fluent construction

The plan is built using a fluent interface, allowing natural chaining:
```python
plan = ScaffoldPlan()
plan.add_directory('.claude/commands', 'Claude Code commands')
    .add_file('.claude/settings.json', FileAction.CREATE, template='settings.j2')
    .add_file('scripts/start.sh', FileAction.CREATE, executable=True)
```

## Relevant Files

Files necessary for implementing the feature:

### Existing Files to Read
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Reference for Pydantic model patterns and existing domain model structure
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/pyproject.toml` - Verify Pydantic dependency availability (>=2.5.0)
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - Ensure domain package exists and can import new models

### New Files to Create
- `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - Complete plan models (main deliverable)

## Implementation Plan

### Phase 1: Foundation
Create the basic enum and model structure that represents individual operations:
- Define FileAction enum with CREATE, OVERWRITE, PATCH, SKIP actions
- Implement FileOperation model with path, action, template, content fields
- Implement DirectoryOperation model with path and reason fields
- Add __str__ methods for human-readable representation

### Phase 2: Core Implementation
Build the ScaffoldPlan container with query capabilities:
- Implement ScaffoldPlan model with directories and files lists
- Add filtering methods (get_files_to_create, get_files_to_overwrite, etc.)
- Add property methods (total_directories, total_files, summary)
- Implement fluent interface methods (add_directory, add_file)

### Phase 3: Integration
Validate the models integrate correctly with the existing codebase:
- Verify imports work correctly from domain package
- Test model instantiation and validation
- Test fluent interface chaining
- Run verification commands from issue
- Execute full validation suite

## Step by Step Tasks

IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create FileAction Enum
- Create `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py`
- Add module docstring explaining the plan models' purpose
- Import necessary types: `from enum import Enum`, `from typing import Optional, List`, `from pydantic import BaseModel, Field`
- Define FileAction enum inheriting from `str, Enum`
- Add four actions: CREATE, OVERWRITE, PATCH, SKIP with inline comments explaining each

### Task 2: Create FileOperation Model
- Define FileOperation class inheriting from BaseModel
- Add comprehensive docstring explaining it represents a single file operation
- Define fields using Field() with descriptions:
  - `path: str` - Relative path from project root (required)
  - `action: FileAction` - Type of operation (required)
  - `template: Optional[str]` - Jinja2 template name (optional)
  - `content: Optional[str]` - Static content if no template (optional)
  - `reason: Optional[str]` - Documentation of why file is needed (optional)
  - `executable: bool` - Whether to chmod +x after creation (default False)
- Implement `__str__` method returning `[{action}] {path}` format

### Task 3: Create DirectoryOperation Model
- Define DirectoryOperation class inheriting from BaseModel
- Add docstring explaining it represents a directory to create
- Define fields:
  - `path: str` - Relative path from project root (required)
  - `reason: str` - Purpose/documentation (default empty string)
- Implement `__str__` method returning `[mkdir] {path}/` format

### Task 4: Create ScaffoldPlan Model
- Define ScaffoldPlan class inheriting from BaseModel
- Add comprehensive docstring with usage example showing build/preview/execute workflow
- Define fields:
  - `directories: List[DirectoryOperation]` - List of directories to create (default empty list)
  - `files: List[FileOperation]` - List of file operations (default empty list)
- Implement query methods that filter files by action:
  - `get_files_to_create() -> List[FileOperation]` - Filter by CREATE action
  - `get_files_to_overwrite() -> List[FileOperation]` - Filter by OVERWRITE action
  - `get_files_to_patch() -> List[FileOperation]` - Filter by PATCH action
  - `get_files_skipped() -> List[FileOperation]` - Filter by SKIP action
  - `get_executable_files() -> List[FileOperation]` - Filter by executable flag

### Task 5: Add ScaffoldPlan Properties
- Implement `@property` decorated methods:
  - `total_directories -> int` - Return count of directories
  - `total_files -> int` - Return count of file operations
  - `summary -> str` - Return formatted summary string with counts by action

### Task 6: Implement Fluent Interface
- Implement `add_directory(path, reason="") -> ScaffoldPlan`:
  - Append DirectoryOperation to directories list
  - Return self for chaining
- Implement `add_file(path, action=CREATE, template=None, content=None, reason=None, executable=False) -> ScaffoldPlan`:
  - Append FileOperation to files list
  - Return self for chaining
- Both methods should enable chaining like: `plan.add_directory(...).add_file(...).add_file(...)`

### Task 7: Verify Model Imports and Instantiation
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction, FileOperation, DirectoryOperation; print('Imports OK')"`
- Verify no import errors
- Run the complete verification command from issue body
- Verify output shows plan summary and operation details

### Task 8: Test Fluent Interface Chaining
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_directory('.claude').add_directory('.claude/commands').add_file('README.md', FileAction.CREATE); print(f'{plan.total_directories} dirs, {plan.total_files} files')"`
- Verify chaining works and counts are correct

### Task 9: Test Query Methods
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_file('a.txt', FileAction.CREATE).add_file('b.txt', FileAction.SKIP).add_file('c.sh', FileAction.CREATE, executable=True); print(f'Create: {len(plan.get_files_to_create())}, Skip: {len(plan.get_files_skipped())}, Executable: {len(plan.get_executable_files())}')"`
- Verify filtering methods return correct counts

### Task 10: Test Pydantic Serialization
- Run: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan().add_directory('src').add_file('main.py', FileAction.CREATE); import json; print(json.dumps(plan.model_dump(), indent=2))"`
- Verify plan can be serialized to JSON correctly

### Task 11: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- Run unit tests: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- Run linting: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run ruff check .`
- Run type checking: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- Run smoke test: `cd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
Since the issue explicitly states "No implementar la logica de ejecucion del plan", this task focuses only on model creation. Future tasks will add comprehensive tests for:
- FileAction enum values
- FileOperation and DirectoryOperation validation
- ScaffoldPlan query methods
- Fluent interface chaining
- Serialization/deserialization

For this task, manual verification commands (Tasks 7-10) serve as smoke tests.

### Edge Cases
The models should handle:
- Empty plans (no directories, no files)
- Plans with only directories or only files
- Files with neither template nor content (both None)
- Files with both template and content (both specified - validation TBD)
- Executable files with different actions
- Very long paths
- Special characters in paths (will be validated during execution, not in model)

## Acceptance Criteria

1. **File Created** - `/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py` exists with complete implementation
2. **Enum Complete** - FileAction has all four actions (CREATE, OVERWRITE, PATCH, SKIP)
3. **Models Valid** - FileOperation, DirectoryOperation, and ScaffoldPlan are valid Pydantic models
4. **Query Methods Work** - All get_files_* methods filter correctly by action
5. **Properties Work** - total_directories, total_files, and summary return correct values
6. **Fluent Interface Works** - add_directory and add_file return self for chaining
7. **String Representation** - __str__ methods return expected format
8. **Imports Work** - Can import all models from tac_bootstrap.domain.plan
9. **Verification Commands Pass** - All commands from issue body execute successfully
10. **No Regressions** - All validation commands pass (pytest, ruff, mypy, smoke test)

## Validation Commands

Execute all commands to validate with zero regressions:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Tests unitarios
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type check
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

### Important Implementation Details

1. **No Execution Logic** - This task creates ONLY the data models. Do not implement:
   - Directory creation logic
   - File writing logic
   - Template rendering logic
   - Filesystem operations
   All execution logic will be implemented in the ScaffoldService (future task).

2. **No Test Files** - Per established pattern from previous tasks, do not create test files yet. Manual verification commands are sufficient for this task.

3. **Pydantic V2 Syntax** - Use Pydantic 2.5.0+ features:
   - Field() for field definitions
   - model_dump() for serialization
   - BaseModel for all models
   - Proper type hints with Optional, List

4. **String Enum Pattern** - FileAction inherits from `str, Enum` to ensure proper serialization to JSON strings rather than enum objects.

### Design Decisions

1. **Fluent Interface** - The add_directory and add_file methods return `self` to enable method chaining, making plan construction more natural and concise.

2. **Separate Template and Content** - FileOperation has both `template` and `content` fields (both optional) to support:
   - Template-based files: specify template name, content rendered later
   - Static files: specify content directly
   - Future: validation could ensure exactly one is provided

3. **Action-Based Filtering** - The get_files_* methods enable easy querying of the plan by operation type, which will be useful for:
   - Preview display (showing what will be created vs skipped)
   - Progress tracking during execution
   - Dry-run reporting

4. **Executable Flag** - Separate from action to support executable files with any action type (CREATE, OVERWRITE, etc.)

### Dependencies Already Available

Per `pyproject.toml`, these dependencies are already installed:
- pydantic>=2.5.0 - For model definitions
- typing (stdlib) - For type hints

### Future Integration

These models will be used by:
- **ScaffoldService.build_plan()** - To construct plans from TACConfig
- **ScaffoldService.apply_plan()** - To execute plans and create files/directories
- **CLI commands** - To display plan previews before execution
- **Wizard** - To show what will be generated based on user choices
