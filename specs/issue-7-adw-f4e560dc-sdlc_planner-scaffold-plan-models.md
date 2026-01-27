# Feature: Create Scaffolding Plan Models

## Metadata
issue_number: `7`
adw_id: `f4e560dc`
issue_json: `{"number":7,"title":"TAREA 2.2: Crear modelos de plan de scaffolding","body":"# Prompt para Agente\n\n## Contexto\nEl ScaffoldService necesita construir un \"plan\" de operaciones antes de ejecutarlas.\nEste plan contiene listas de directorios a crear y archivos a generar/modificar.\nEsto permite hacer dry-run, mostrar preview, y mantener idempotencia.\n\n## Objetivo\nCrear modelos Pydantic que representen el plan de scaffolding con operaciones\nde archivos y directorios.\n\n## Archivo a Crear\n`/Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/domain/plan.py`\n\n## Contenido Completo\n\n```python\n\"\"\"Scaffolding plan models.\n\nThese models represent the plan of operations to execute when scaffolding\na project. The plan is built first, then can be previewed or executed.\n\"\"\"\nfrom enum import Enum\nfrom typing import Optional, List\nfrom pydantic import BaseModel, Field\n\n\nclass FileAction(str, Enum):\n    \"\"\"Type of file operation to perform.\"\"\"\n    CREATE = \"create\"    # Create new file (skip if exists)\n    OVERWRITE = \"overwrite\"  # Create or overwrite existing\n    PATCH = \"patch\"      # Append to existing file\n    SKIP = \"skip\"        # Skip this file\n\n\nclass FileOperation(BaseModel):\n    \"\"\"Single file operation in the scaffold plan.\n\n    Represents one file to be created, modified, or skipped.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    action: FileAction = Field(..., description=\"Type of operation\")\n    template: Optional[str] = Field(None, description=\"Jinja2 template name to render\")\n    content: Optional[str] = Field(None, description=\"Static content (if no template)\")\n    reason: Optional[str] = Field(None, description=\"Why this file is needed\")\n    executable: bool = Field(False, description=\"Make file executable after creation\")\n\n    def __str__(self) -> str:\n        return f\"[{self.action.value}] {self.path}\"\n\n\nclass DirectoryOperation(BaseModel):\n    \"\"\"Directory creation operation.\n\n    Represents a directory to be created.\n    \"\"\"\n    path: str = Field(..., description=\"Relative path from project root\")\n    reason: str = Field(\"\", description=\"Purpose of this directory\")\n\n    def __str__(self) -> str:\n        return f\"[mkdir] {self.path}/\"\n\n\nclass ScaffoldPlan(BaseModel):\n    \"\"\"Complete scaffold plan for generation.\n\n    Contains all directories and files to be created/modified.\n    The plan is built first, allowing preview and validation before execution.\n\n    Example:\n        ```python\n        plan = scaffold_service.build_plan(config)\n\n        # Preview what will be created\n        for dir_op in plan.directories:\n            print(f\"Will create: {dir_op.path}/\")\n\n        for file_op in plan.get_files_to_create():\n            print(f\"Will create: {file_op.path}\")\n\n        # Execute the plan\n        scaffold_service.apply_plan(plan, output_dir)\n        ```\n    \"\"\"\n    directories: List[DirectoryOperation] = Field(default_factory=list)\n    files: List[FileOperation] = Field(default_factory=list)\n\n    def get_files_to_create(self) -> List[FileOperation]:\n        \"\"\"Get files that will be created (new files only).\"\"\"\n        return [f for f in self.files if f.action == FileAction.CREATE]\n\n    def get_files_to_overwrite(self) -> List[FileOperation]:\n        \"\"\"Get files that will be overwritten.\"\"\"\n        return [f for f in self.files if f.action == FileAction.OVERWRITE]\n\n    def get_files_to_patch(self) -> List[FileOperation]:\n        \"\"\"Get files that will be patched (appended to).\"\"\"\n        return [f for f in self.files if f.action == FileAction.PATCH]\n\n    def get_files_skipped(self) -> List[FileOperation]:\n        \"\"\"Get files that will be skipped.\"\"\"\n        return [f for f in self.files if f.action == FileAction.SKIP]\n\n    def get_executable_files(self) -> List[FileOperation]:\n        \"\"\"Get files that need to be made executable.\"\"\"\n        return [f for f in self.files if f.executable]\n\n    @property\n    def total_directories(self) -> int:\n        \"\"\"Total number of directories to create.\"\"\"\n        return len(self.directories)\n\n    @property\n    def total_files(self) -> int:\n        \"\"\"Total number of file operations.\"\"\"\n        return len(self.files)\n\n    @property\n    def summary(self) -> str:\n        \"\"\"Get a summary of the plan.\"\"\"\n        creates = len(self.get_files_to_create())\n        patches = len(self.get_files_to_patch())\n        skips = len(self.get_files_skipped())\n        return (\n            f\"Plan: {self.total_directories} directories, \"\n            f\"{creates} files to create, {patches} to patch, {skips} skipped\"\n        )\n\n    def add_directory(self, path: str, reason: str = \"\") -> \"ScaffoldPlan\":\n        \"\"\"Add a directory to the plan (fluent interface).\"\"\"\n        self.directories.append(DirectoryOperation(path=path, reason=reason))\n        return self\n\n    def add_file(\n        self,\n        path: str,\n        action: FileAction = FileAction.CREATE,\n        template: Optional[str] = None,\n        content: Optional[str] = None,\n        reason: Optional[str] = None,\n        executable: bool = False,\n    ) -> \"ScaffoldPlan\":\n        \"\"\"Add a file operation to the plan (fluent interface).\"\"\"\n        self.files.append(FileOperation(\n            path=path,\n            action=action,\n            template=template,\n            content=content,\n            reason=reason,\n            executable=executable,\n        ))\n        return self\n```\n\n## Criterios de Aceptacion\n1. [ ] Archivo `plan.py` creado\n2. [ ] FileAction enum con todas las acciones\n3. [ ] Metodos helper en ScaffoldPlan funcionan\n4. [ ] Fluent interface permite encadenar add_directory/add_file\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\nuv run python -c \"\nfrom tac_bootstrap.domain.plan import ScaffoldPlan, FileAction\n\nplan = ScaffoldPlan()\nplan.add_directory('.claude/commands', 'Claude Code commands')\nplan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2')\nplan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True)\n\nprint(plan.summary)\nfor d in plan.directories:\n    print(d)\nfor f in plan.files:\n    print(f)\n\"\n```\n\n## NO hacer\n- No implementar la logica de ejecucion del plan (eso va en scaffold_service)"}`

## Feature Description
This feature creates Pydantic domain models that represent a scaffolding plan for project generation. The plan acts as a data structure that captures all file and directory operations that need to be performed, enabling preview (dry-run), validation, and idempotent execution. This is a critical piece of the domain layer that separates planning from execution, following the DDD principle of keeping business logic pure and testable.

## User Story
As a ScaffoldService developer
I want to build a complete plan of operations before executing them
So that I can preview what will be created, validate operations, and maintain idempotent behavior

## Problem Statement
The ScaffoldService needs a way to represent scaffolding operations (creating directories, generating files from templates, modifying existing files) as a data structure before executing them. Without this, the service would need to execute operations immediately, making it impossible to:
- Preview what will be created (dry-run mode)
- Validate operations before execution
- Maintain idempotency (skip files that already exist)
- Provide detailed progress reporting
- Rollback on errors

## Solution Statement
Create three Pydantic models in `tac_bootstrap/domain/plan.py`:

1. **FileAction** enum: Defines the types of file operations (CREATE, OVERWRITE, PATCH, SKIP)
2. **FileOperation** model: Represents a single file operation with path, action, template/content, reason, and executable flag
3. **DirectoryOperation** model: Represents a directory creation with path and reason
4. **ScaffoldPlan** model: Container for all operations with helper methods to filter and query operations

The ScaffoldPlan provides:
- Fluent interface for building plans (`add_directory()`, `add_file()`)
- Query methods to filter operations by type
- Summary property for reporting
- Clear separation between plan creation and execution

## Relevant Files

### Existing Files
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Existing domain models for reference on Pydantic patterns
- `tac_bootstrap_cli/tac_bootstrap/domain/__init__.py` - Domain layer initialization

### New Files
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - The scaffolding plan models

## Implementation Plan

### Phase 1: Foundation
Create the enum and basic operation models that represent individual operations.

**Tasks:**
1. Create `plan.py` with module docstring
2. Import required dependencies (Enum, Optional, List from typing; BaseModel, Field from pydantic)
3. Define FileAction enum with four actions: CREATE, OVERWRITE, PATCH, SKIP
4. Define FileOperation model with fields: path, action, template, content, reason, executable
5. Define DirectoryOperation model with fields: path, reason
6. Add `__str__` methods to both operation models for display

### Phase 2: Core Implementation
Create the main ScaffoldPlan model with all helper methods.

**Tasks:**
1. Define ScaffoldPlan model with directories and files lists
2. Add query methods: get_files_to_create(), get_files_to_overwrite(), get_files_to_patch(), get_files_skipped()
3. Add get_executable_files() method
4. Add @property methods: total_directories, total_files, summary
5. Add fluent interface methods: add_directory(), add_file()

### Phase 3: Integration
Verify the models work correctly and can be imported by other modules.

**Tasks:**
1. Test that models can be instantiated
2. Test fluent interface chaining
3. Test query methods return correct filtered results
4. Run verification commands from acceptance criteria
5. Verify models follow Pydantic best practices

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify File Exists
- Check if `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` already exists
- If it exists, verify it matches the specification
- If not, create it with proper module docstring

### Task 2: Create FileAction Enum
- Define FileAction as str, Enum with proper docstring
- Add four values: CREATE = "create", OVERWRITE = "overwrite", PATCH = "patch", SKIP = "skip"
- Add inline comments explaining each action

### Task 3: Create FileOperation Model
- Define FileOperation class inheriting from BaseModel
- Add docstring explaining it represents a single file operation
- Add fields with Field() descriptors:
  - path: str (required, relative path from project root)
  - action: FileAction (required, type of operation)
  - template: Optional[str] (Jinja2 template name)
  - content: Optional[str] (static content if no template)
  - reason: Optional[str] (why this file is needed)
  - executable: bool (default False, make file executable)
- Add `__str__` method returning formatted string like "[create] path/to/file"

### Task 4: Create DirectoryOperation Model
- Define DirectoryOperation class inheriting from BaseModel
- Add docstring explaining it represents a directory to be created
- Add fields:
  - path: str (required, relative path from project root)
  - reason: str (default "", purpose of directory)
- Add `__str__` method returning formatted string like "[mkdir] path/to/dir/"

### Task 5: Create ScaffoldPlan Model with Basic Structure
- Define ScaffoldPlan class inheriting from BaseModel
- Add comprehensive docstring with usage example
- Add two list fields with default_factory:
  - directories: List[DirectoryOperation]
  - files: List[FileOperation]

### Task 6: Add Query Methods to ScaffoldPlan
- Implement get_files_to_create() - filter files with CREATE action
- Implement get_files_to_overwrite() - filter files with OVERWRITE action
- Implement get_files_to_patch() - filter files with PATCH action
- Implement get_files_skipped() - filter files with SKIP action
- Implement get_executable_files() - filter files with executable=True

### Task 7: Add Property Methods to ScaffoldPlan
- Add @property total_directories - return len(self.directories)
- Add @property total_files - return len(self.files)
- Add @property summary - return formatted string with counts of directories, creates, patches, skips

### Task 8: Add Fluent Interface Methods
- Implement add_directory(path, reason="") - append DirectoryOperation, return self
- Implement add_file(path, action=CREATE, template=None, content=None, reason=None, executable=False) - append FileOperation, return self
- Ensure both methods return "ScaffoldPlan" for type hints (use string literal)

### Task 9: Run Validation Commands
- Execute verification command from acceptance criteria
- Verify fluent interface works (chaining add_directory/add_file)
- Verify summary property works
- Verify query methods filter correctly
- Execute all Validation Commands

## Testing Strategy

### Unit Tests
Future tests (not in this task) should cover:
- FileAction enum values
- FileOperation model validation
- DirectoryOperation model validation
- ScaffoldPlan query methods return correct filtered lists
- ScaffoldPlan fluent interface allows chaining
- ScaffoldPlan summary property formats correctly

### Edge Cases
- Empty ScaffoldPlan (no directories, no files) - should have summary showing zeros
- Plan with only directories, no files
- Plan with only files, no directories
- Files with template vs content (mutually exclusive in practice)
- Executable flag on non-script files (valid but unusual)

## Acceptance Criteria
1. File `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` exists
2. FileAction enum has all four actions: CREATE, OVERWRITE, PATCH, SKIP
3. FileOperation model has all required fields with proper types
4. DirectoryOperation model has path and reason fields
5. ScaffoldPlan has directories and files lists
6. All query methods work: get_files_to_create(), get_files_to_overwrite(), get_files_to_patch(), get_files_skipped(), get_executable_files()
7. Property methods work: total_directories, total_files, summary
8. Fluent interface allows chaining: `plan.add_directory(...).add_file(...)`
9. `__str__` methods on operations return formatted strings
10. Models follow Pydantic conventions with Field descriptors
11. Verification command from issue body runs successfully

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction, FileOperation, DirectoryOperation; print('Import successful')"` - Verify models can be imported
- `cd tac_bootstrap_cli && uv run python -c "from tac_bootstrap.domain.plan import ScaffoldPlan, FileAction; plan = ScaffoldPlan(); plan.add_directory('.claude/commands', 'Claude Code commands'); plan.add_file('.claude/settings.json', FileAction.CREATE, template='claude/settings.json.j2'); plan.add_file('scripts/start.sh', FileAction.CREATE, template='scripts/start.sh.j2', executable=True); print(plan.summary); [print(d) for d in plan.directories]; [print(f) for f in plan.files]"` - Run full verification from issue
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short -k plan` - Run tests if any exist for plan models
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/domain/plan.py` - Type check the module

## Notes
- This is TAREA 2.2 from PLAN_TAC_BOOTSTRAP.md
- The plan models are pure domain logic with no external dependencies except Pydantic
- The ScaffoldService (to be implemented later) will use these models to build and execute plans
- The fluent interface makes it easy to build plans programmatically
- The query methods enable selective execution and reporting
- The models are immutable after creation (no setters), modifications happen by building new instances
- Using string literal "ScaffoldPlan" in return types avoids forward reference issues
- The executable flag is particularly important for scripts like start.sh, build.sh, etc.
- The reason field is optional but valuable for documentation and debugging
