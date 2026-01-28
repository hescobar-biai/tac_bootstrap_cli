# Feature: Scaffold Plan Models

## Metadata
issue_number: `7`
adw_id: `fad257de`
issue_json: `{"number":7,"title":"TAREA 2.2: Crear modelos de plan de scaffolding","body":"# Prompt para Agente\n\n## Contexto\nEl ScaffoldService necesita construir un \"plan\" de operaciones antes de ejecutarlas.\nEste plan contiene listas de directorios a crear y archivos a generar/modificar.\nEsto permite hacer dry-run, mostrar preview, y mantener idempotencia.\n\n## Objetivo\nCrear modelos Pydantic que representen el plan de scaffolding con operaciones\nde archivos y directorios.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Scaffolding plan models.\n\nThese models represent the plan of operations to execute when scaffolding\na project. The plan is built first, then can be previewed or executed.\n\"\"\"\nfrom enum import Enum\nfrom typing import Optional, List\nfrom pydantic import BaseModel, Field\n\n\nclass FileAction(str, Enum):\n    \"\"\"Type of file operation to perform.\"\"\"\n    CREATE = \"create\"    # Create new file (skip if exists)\n    OVERWRITE = \"overwrite\"  # Create or overwrite existing\n    PATCH = \"patch\"      # Append to existing file\n    SKIP = \"skip\"        # Skip this file\n\n\nclass FileOperation(BaseModel):\n    \"\"\"Single file operation in the scaffold plan.\n\n    Represents one file to be created, modified, or skipped.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    action: FileAction = Field(..., description=\"Type of operation\")\n    template: Optional[str] = Field(None, description=\"Jinja2 template name to render\")\n    content: Optional[str] = Field(None, description=\"Static content (if no template)\")\n    reason: Optional[str] = Field(None, description=\"Why this file is needed\")\n    executable: bool = Field(False, description=\"Make file executable after creation\")\n\n    def __str__(self) -> str:\n        return f\"[{self.action.value}] {self.path}\"\n\n\nclass DirectoryOperation(BaseModel):\n    \"\"\"Directory creation operation.\n\n    Represents a directory to be created.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    reason: str = Field(\"\", description=\"Purpose of this directory\")\n\n    def __str__(self) -> str:\n        return f\"[mkdir] {self.path}/\"\n\n\nclass ScaffoldPlan(BaseModel):\n    \"\"\"Complete scaffold plan for generation.\n\n    Contains all directories and files to be created/modified.\n    The plan is built first, allowing preview and validation before execution.\n\n    Example:\n        ```python\n        plan = scaffold_service.build_plan(config)\n\n        # Preview what will be created\n        for dir_op in plan.directories:\n            print(f\"Will create: {dir_op.path}/\")\n\n        for file_op in plan.get_files_to_create():\n            print(f\"Will create: {file_op.path}\")\n\n        # Execute the plan\n        scaffold_service.apply_plan(plan, output_dir)\n        ```\n    \"\"\"\n    directories: List[DirectoryOperation] = Field(default_factory=list)\n    files: List[FileOperation] = Field(default_factory=list)\n\n    def get_files_to_create(self) -> List[FileOperation]:\n        \"\"\"Get files that will be created (new files only).\"\"\"\n        return [f for f in self.files if f.action == FileAction.CREATE]\n\n    def get_files_to_overwrite(self) -> List[FileOperation]:\n        \"\"\"Get files that will be overwritten.\"\"\"\n        return [f for f in self.files if f.action == FileAction.OVERWRITE]\n\n    def get_files_to_patch(self) -> List[FileOperation]:\n        \"\"\"Get files that will be patched (appended to).\"\"\"\n        return [f for f in self.files if f.action == FileAction.PATCH]\n\n    def get_files_skipped(self) -> List[FileOperation]:\n        \"\"\"Get files that will be skipped.\"\"\"\n        return [f for f in self.files if f.action == FileAction.SKIP]\n\n    def get_executable_files(self) -> List[FileOperation]:\n        \"\"\"Get files that need to be made executable.\"\"\"\n        return [f for f in self.files if f.executable]\n\n    @property\n    def total_directories(self) -> int:\n        \"\"\"Total number of directories to create.\"\"\"\n        return len(self.directories)\n\n    @property\n    def total_files(self) -> int:\n        \"\"\"Total number of file operations.\"\"\"\n        return len(self.files)\n\n    @property\n    def summary(self) -> str:\n        \"\"\"Get a summary of the plan.\"\"\"\n        creates = len(self.get_files_to_create())\n        patches = len(self.get_files_to_patch())\n        skips = len(self.get_files_skipped())\n        return (\n            f\"Plan: {self.total_directories} directories, \"\n            f\"{creates} files to create, {patches} to patch, {skips} skipped\"\n        )\n\n    def add_directory(self, path: str, reason: str = \"\") -> \"ScaffoldPlan\":\n        \"\"\"Add a directory to the plan (fluent interface).\"\"\"\n        self.directories.append(DirectoryOperation(path=path, reason=reason))\n        return self\n\n    def add_file(\n        self,\n        path: str,\n        action: FileAction = FileAction.CREATE,\n        template: Optional[str] = None,\n        content: Optional[str] = None,\n        reason: Optional[str] = None,\n        executable: bool = False,\n    ) -> \"ScaffoldPlan\":\n        \"\"\"Add a file operation to the plan (fluent interface).\"\"\"\n        self.files.append(FileOperation(\n            path=path,\n            action=action,\n            template=template,\n            content=content,\n            reason=reason,\n            executable=executable,\n        ))\n        return self\n```\n\n## Criterios de Aceptacion\n1. [ ] Archivo `plan.py` creado\n2. [ ] FileAction enum con todas las acciones\n3. [ ] Metodos helper en ScaffoldPlan funcionan\n4. [ ] Fluent interface permite encadenar add_directory/add_file\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv run python -c \"\nfrom tac_bootstrap.domain.plan import ScaffoldPlan, FileAction\n\nplan = ScaffoldPlan()\nplan.add_directory('.claude/commands', 'Claude Code commands')\nplan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2')\nplan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True)\n\nprint(plan.summary)\nfor d in plan.directories:\n    print(d)\nfor f in plan.files:\n    print(f)\n\"\n```\n\n## NO hacer\n- No implementar la logica de ejecucion del plan (eso va en scaffold_service)"}`

## Feature Description
This feature provides domain models for representing a scaffold plan - a structured specification of all directories and files to be created when scaffolding a new project. The plan acts as a blueprint that can be previewed before execution, enabling dry-run capabilities and ensuring idempotent operations. The models use Pydantic for validation and provide a fluent interface for building plans programmatically.

## User Story
As a TAC Bootstrap CLI developer
I want domain models to represent scaffold plans
So that I can build, preview, and execute file/directory operations in a structured, type-safe way

## Problem Statement
The ScaffoldService needs a way to represent planned file and directory operations before executing them. Without proper domain models:
- There's no type-safe way to represent file operations (create, overwrite, patch, skip)
- Preview functionality and dry-run modes would be difficult to implement
- Ensuring idempotency requires tracking what operations will be performed
- Different file operations need different metadata (templates, executable flags, etc.)

## Solution Statement
Create Pydantic domain models in `tac_bootstrap/domain/plan.py` that represent:
1. **FileAction enum** - Defines the four types of file operations (CREATE, OVERWRITE, PATCH, SKIP)
2. **FileOperation** - Represents a single file operation with path, action type, template reference, content, and executable flag
3. **DirectoryOperation** - Represents a directory to be created with path and reason
4. **ScaffoldPlan** - Container for all operations with helper methods for filtering, summary, and a fluent builder interface

The models provide type safety, validation, and convenient methods for querying and building plans.

## Relevant Files
Files necessary for implementing the feature:

- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - **ALREADY EXISTS** - Contains all scaffold plan domain models
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - May need to export plan models
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Will consume these models (future task)

### New Files
None - the file `tac_bootstrap/domain/plan.py` already exists with complete implementation

## Implementation Plan

### Phase 1: Foundation
**STATUS: COMPLETED**
The foundation work is already complete. The file `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` exists with:
- All imports (Enum, BaseModel, Field from Pydantic)
- Complete type hints using Optional and List

### Phase 2: Core Implementation
**STATUS: COMPLETED**
All core models are implemented:
1. `FileAction` enum with four actions (CREATE, OVERWRITE, PATCH, SKIP)
2. `FileOperation` model with all required fields and `__str__` method
3. `DirectoryOperation` model with path and reason fields
4. `ScaffoldPlan` model with directories and files lists

### Phase 3: Integration
**STATUS: COMPLETED**
Helper methods are fully implemented:
- Filter methods: `get_files_to_create()`, `get_files_to_overwrite()`, `get_files_to_patch()`, `get_files_skipped()`, `get_executable_files()`
- Properties: `total_directories`, `total_files`, `summary`
- Fluent builder interface: `add_directory()`, `add_file()`

## Step by Step Tasks

### Task 1: Verify Existing Implementation
**STATUS: COMPLETED**
- File `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` exists at lines 1-144
- All models match the specification exactly
- Code follows proper Pydantic patterns with Field descriptors

### Task 2: Validate Model Functionality
**STATUS: PENDING**
Execute the validation commands to confirm:
- Models can be imported successfully
- Fluent interface works correctly
- Helper methods return expected results
- Summary formatting is correct

### Task 3: Run Validation Commands
Execute all validation commands to ensure zero regressions:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; print('Import successful')"
```

## Testing Strategy

### Unit Tests
Create tests in `tests/domain/test_plan.py`:
- Test FileAction enum values
- Test FileOperation creation and validation
- Test DirectoryOperation creation
- Test ScaffoldPlan helper methods
- Test fluent interface chaining
- Test summary formatting
- Test edge cases (empty plan, all skipped files, etc.)

### Edge Cases
- Empty ScaffoldPlan (no directories, no files)
- Plan with only SKIP operations
- Plan with executable files
- Plan with mixed action types
- Chaining multiple add_directory and add_file calls
- Files with templates vs static content

## Acceptance Criteria
- [x] File `tac_bootstrap/domain/plan.py` exists and is complete
- [x] FileAction enum defines CREATE, OVERWRITE, PATCH, SKIP
- [x] FileOperation model has all required fields (path, action, template, content, reason, executable)
- [x] DirectoryOperation model has path and reason fields
- [x] ScaffoldPlan has directories and files lists
- [x] Helper methods implemented: get_files_to_create(), get_files_to_overwrite(), get_files_to_patch(), get_files_skipped(), get_executable_files()
- [x] Properties implemented: total_directories, total_files, summary
- [x] Fluent interface methods: add_directory(), add_file()
- [x] All models use Pydantic BaseModel with Field descriptors
- [ ] Validation commands execute successfully
- [ ] Unit tests pass with 100% coverage

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Test imports
cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction, FileOperation, DirectoryOperation; print('✓ Import successful')"

# Test fluent interface (from issue)
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

# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes
- The implementation is already complete and matches the specification exactly
- The models follow Domain-Driven Design (DDD) principles with proper value objects
- Fluent interface pattern makes it easy to build plans programmatically
- All methods are well-documented with docstrings
- The code is type-safe with proper Optional and List type hints
- Next step: ScaffoldService will consume these models to build and execute plans
- The models are pure domain logic - no filesystem operations included (separation of concerns)
