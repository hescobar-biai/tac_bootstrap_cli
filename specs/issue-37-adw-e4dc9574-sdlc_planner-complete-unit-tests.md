# Feature: Complete Unit Tests for TAC Bootstrap CLI

## Metadata
issue_number: `37`
adw_id: `e4dc9574`
issue_json: `{"number":37,"title":"TAREA 8.1: Tests unitarios completos","body":"# Prompt para Agente\n\n## Contexto\nNecesitamos tests unitarios para todos los modulos implementados para asegurar\ncalidad y prevenir regresiones.\n\n## Objetivo\nCrear tests unitarios completos para:\n- domain/models.py\n- domain/plan.py\n- application/scaffold_service.py\n- application/detect_service.py\n- application/doctor_service.py\n- infrastructure/template_repo.py\n- infrastructure/fs.py\n\n## Archivos a Crear\n\n### 1. `tests/test_models.py`\n\n```python\n\"\"\"Tests for domain models.\"\"\"\nimport pytest\nfrom tac_bootstrap.domain.models import (\n    TACConfig,\n    ProjectSpec,\n    CommandsSpec,\n    ClaudeConfig,\n    ClaudeSettings,\n    Language,\n    Framework,\n    PackageManager,\n    get_frameworks_for_language,\n    get_package_managers_for_language,\n    get_default_commands,\n)\n\n\nclass TestProjectSpec:\n    \"\"\"Tests for ProjectSpec model.\"\"\"\n\n    def test_name_sanitization(self):\n        \"\"\"Project name should be sanitized.\"\"\"\n        spec = ProjectSpec(\n            name=\"  My Project  \",\n            language=Language.PYTHON,\n            package_manager=PackageManager.UV,\n        )\n        assert spec.name == \"my-project\"\n\n    def test_empty_name_raises(self):\n        \"\"\"Empty name should raise ValueError.\"\"\"\n        with pytest.raises(ValueError):\n            ProjectSpec(\n                name=\"\",\n                language=Language.PYTHON,\n                package_manager=PackageManager.UV,\n            )\n\n\nclass TestTACConfig:\n    \"\"\"Tests for TACConfig model.\"\"\"\n\n    def test_minimal_config(self):\n        \"\"\"Minimal config should have defaults.\"\"\"\n        config = TACConfig(\n            project=ProjectSpec(\n                name=\"test\",\n                language=Language.PYTHON,\n                package_manager=PackageManager.UV,\n            ),\n            commands=CommandsSpec(start=\"echo start\", test=\"echo test\"),\n            claude=ClaudeConfig(settings=ClaudeSettings(project_name=\"test\")),\n        )\n        assert config.version == 1\n        assert config.paths.adws_dir == \"adws\"\n        assert config.agentic.provider.value == \"claude_code\"\n\n\nclass TestHelperFunctions:\n    \"\"\"Tests for helper functions.\"\"\"\n\n    def test_frameworks_for_python(self):\n        \"\"\"Python should have FastAPI, Django, Flask.\"\"\"\n        frameworks = get_frameworks_for_language(Language.PYTHON)\n        assert Framework.FASTAPI in frameworks\n        assert Framework.DJANGO in frameworks\n\n    def test_package_managers_for_typescript(self):\n        \"\"\"TypeScript should have pnpm, npm, yarn, bun.\"\"\"\n        managers = get_package_managers_for_language(Language.TYPESCRIPT)\n        assert PackageManager.PNPM in managers\n        assert PackageManager.NPM in managers\n\n    def test_default_commands_python_uv(self):\n        \"\"\"Python + UV should have correct defaults.\"\"\"\n        commands = get_default_commands(Language.PYTHON, PackageManager.UV)\n        assert \"uv run pytest\" in commands[\"test\"]\n        assert \"uv run ruff\" in commands[\"lint\"]\n```\n\n### 2. `tests/test_plan.py`\n\n```python\n\"\"\"Tests for scaffold plan models.\"\"\"\nimport pytest\nfrom tac_bootstrap.domain.plan import (\n    ScaffoldPlan,\n    FileOperation,\n    FileAction,\n    DirectoryOperation,\n)\n\n\nclass TestScaffoldPlan:\n    \"\"\"Tests for ScaffoldPlan model.\"\"\"\n\n    def test_empty_plan(self):\n        \"\"\"Empty plan should have zero counts.\"\"\"\n        plan = ScaffoldPlan()\n        assert plan.total_directories == 0\n        assert plan.total_files == 0\n\n    def test_add_directory_fluent(self):\n        \"\"\"add_directory should return self for chaining.\"\"\"\n        plan = ScaffoldPlan()\n        result = plan.add_directory(\"test\", \"Test dir\")\n        assert result is plan\n        assert plan.total_directories == 1\n\n    def test_add_file_fluent(self):\n        \"\"\"add_file should return self for chaining.\"\"\"\n        plan = ScaffoldPlan()\n        result = plan.add_file(\"test.txt\", FileAction.CREATE)\n        assert result is plan\n        assert plan.total_files == 1\n\n    def test_chaining(self):\n        \"\"\"Should support method chaining.\"\"\"\n        plan = (\n            ScaffoldPlan()\n            .add_directory(\"dir1\")\n            .add_directory(\"dir2\")\n            .add_file(\"file1.txt\")\n            .add_file(\"file2.txt\")\n        )\n        assert plan.total_directories == 2\n        assert plan.total_files == 2\n\n    def test_get_files_by_action(self):\n        \"\"\"Should filter files by action.\"\"\"\n        plan = ScaffoldPlan()\n        plan.add_file(\"create.txt\", FileAction.CREATE)\n        plan.add_file(\"skip.txt\", FileAction.SKIP)\n        plan.add_file(\"patch.txt\", FileAction.PATCH)\n\n        assert len(plan.get_files_to_create()) == 1\n        assert len(plan.get_files_skipped()) == 1\n        assert len(plan.get_files_to_patch()) == 1\n\n    def test_summary(self):\n        \"\"\"Summary should include counts.\"\"\"\n        plan = ScaffoldPlan()\n        plan.add_directory(\"dir\")\n        plan.add_file(\"file.txt\", FileAction.CREATE)\n        plan.add_file(\"skip.txt\", FileAction.SKIP)\n\n        summary = plan.summary\n        assert \"1 directories\" in summary\n        assert \"1 files to create\" in summary\n        assert \"1 skipped\" in summary\n```\n\n### 3. `tests/test_scaffold_service.py`\n\n```python\n\"\"\"Tests for scaffold service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\n\nfrom tac_bootstrap.application.scaffold_service import ScaffoldService\nfrom tac_bootstrap.domain.models import (\n    TACConfig,\n    ProjectSpec,\n    CommandsSpec,\n    ClaudeConfig,\n    ClaudeSettings,\n    Language,\n    PackageManager,\n)\n\n\n@pytest.fixture\ndef config():\n    \"\"\"Create a test config.\"\"\"\n    return TACConfig(\n        project=ProjectSpec(\n            name=\"test-project\",\n            language=Language.PYTHON,\n            package_manager=PackageManager.UV,\n        ),\n        commands=CommandsSpec(start=\"uv run python -m app\", test=\"uv run pytest\"),\n        claude=ClaudeConfig(settings=ClaudeSettings(project_name=\"test-project\")),\n    )\n\n\nclass TestScaffoldService:\n    \"\"\"Tests for ScaffoldService.\"\"\"\n\n    def test_build_plan_creates_directories(self, config):\n        \"\"\"build_plan should include required directories.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        dir_paths = [d.path for d in plan.directories]\n        assert \".claude\" in dir_paths\n        assert \".claude/commands\" in dir_paths\n        assert \"adws\" in dir_paths\n\n    def test_build_plan_creates_files(self, config):\n        \"\"\"build_plan should include required files.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        file_paths = [f.path for f in plan.files]\n        assert \".claude/settings.json\" in file_paths\n        assert \"config.yml\" in file_paths\n\n    def test_build_plan_marks_scripts_executable(self, config):\n        \"\"\"Script files should be marked executable.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        script_files = [f for f in plan.files if f.path.endswith(\".sh\")]\n        assert all(f.executable for f in script_files)\n\n    def test_apply_plan_creates_structure(self, config):\n        \"\"\"apply_plan should create directories and files.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        with tempfile.TemporaryDirectory() as tmp:\n            result = service.apply_plan(plan, Path(tmp), config)\n\n            assert result.success\n            assert result.directories_created > 0\n            assert result.files_created > 0\n            assert (Path(tmp) / \".claude\").is_dir()\n            assert (Path(tmp) / \"config.yml\").is_file()\n```\n\n### 4. `tests/test_detect_service.py`\n\n```python\n\"\"\"Tests for detect service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\nimport json\n\nfrom tac_bootstrap.application.detect_service import DetectService\nfrom tac_bootstrap.domain.models import Language, PackageManager, Framework\n\n\nclass TestDetectService:\n    \"\"\"Tests for DetectService.\"\"\"\n\n    def test_detect_python_by_pyproject(self):\n        \"\"\"Should detect Python by pyproject.toml.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").write_text(\"[project]\\nname='test'\")\n            result = detector.detect(Path(tmp))\n\n            assert result.language == Language.PYTHON\n\n    def test_detect_uv_by_lock(self):\n        \"\"\"Should detect UV by uv.lock.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").touch()\n            (Path(tmp) / \"uv.lock\").touch()\n            result = detector.detect(Path(tmp))\n\n            assert result.package_manager == PackageManager.UV\n\n    def test_detect_typescript_by_tsconfig(self):\n        \"\"\"Should detect TypeScript by tsconfig.json.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"tsconfig.json\").write_text(\"{}\")\n            result = detector.detect(Path(tmp))\n\n            assert result.language == Language.TYPESCRIPT\n\n    def test_detect_nextjs_from_package_json(self):\n        \"\"\"Should detect Next.js framework.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"tsconfig.json\").write_text(\"{}\")\n            (Path(tmp) / \"package.json\").write_text(\n                json.dumps({\"dependencies\": {\"next\": \"^14.0.0\"}})\n            )\n            result = detector.detect(Path(tmp))\n\n            assert result.framework == Framework.NEXTJS\n\n    def test_detect_app_root(self):\n        \"\"\"Should detect src as app root.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").touch()\n            (Path(tmp) / \"src\").mkdir()\n            result = detector.detect(Path(tmp))\n\n            assert result.app_root == \"src\"\n```\n\n### 5. `tests/test_doctor_service.py`\n\n```python\n\"\"\"Tests for doctor service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\nimport json\n\nfrom tac_bootstrap.application.doctor_service import DoctorService, Severity\n\n\nclass TestDoctorService:\n    \"\"\"Tests for DoctorService.\"\"\"\n\n    def test_diagnose_empty_directory(self):\n        \"\"\"Empty directory should have errors.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            report = doctor.diagnose(Path(tmp))\n\n            assert not report.healthy\n            assert any(i.severity == Severity.ERROR for i in report.issues)\n\n    def test_diagnose_valid_setup(self):\n        \"\"\"Valid setup should be healthy.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            tmp_path = Path(tmp)\n            # Create minimal valid structure\n            (tmp_path / \".claude\" / \"commands\").mkdir(parents=True)\n            (tmp_path / \".claude\" / \"hooks\").mkdir(parents=True)\n            (tmp_path / \".claude\" / \"settings.json\").write_text('{\"version\": 1}')\n            (tmp_path / \".claude\" / \"commands\" / \"prime.md\").write_text(\"# Prime\")\n            (tmp_path / \".claude\" / \"commands\" / \"test.md\").write_text(\"# Test\")\n            (tmp_path / \".claude\" / \"commands\" / \"commit.md\").write_text(\"# Commit\")\n            (tmp_path / \"config.yml\").write_text(\"project:\\n  name: test\\ncommands:\\n  start: echo\")\n\n            report = doctor.diagnose(tmp_path)\n\n            # Should have no errors (may have warnings for optional stuff)\n            errors = [i for i in report.issues if i.severity == Severity.ERROR]\n            assert len(errors) == 0\n\n    def test_fix_creates_directories(self):\n        \"\"\"fix() should create missing directories.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            report = doctor.diagnose(Path(tmp))\n            result = doctor.fix(Path(tmp), report)\n\n            # Should have fixed some directory issues\n            assert result.fixed_count > 0\n            assert (Path(tmp) / \".claude\").is_dir()\n```\n\n## Criterios de Aceptacion\n1. [ ] Tests para models.py cubren validacion y helpers\n2. [ ] Tests para plan.py cubren fluent interface y queries\n3. [ ] Tests para scaffold_service cubren build y apply\n4. [ ] Tests para detect_service cubren cada lenguaje\n5. [ ] Tests para doctor_service cubren diagnose y fix\n6. [ ] Coverage > 80%\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\n\n# Run all tests\nuv run pytest tests/ -v\n\n# With coverage\nuv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing\n\n# Run specific test file\nuv run pytest tests/test_models.py -v\n```\n\n## NO hacer\n- No crear tests de integracion complejos\n- No mockear filesystem innecesariamente"}`

## Feature Description
Implement comprehensive unit tests for all TAC Bootstrap CLI modules to ensure quality, prevent regressions, and provide robust validation of the core functionality. This includes tests for domain models (models, plan), application services (scaffold, detect, doctor), and infrastructure components (template repository, filesystem).

## User Story
As a TAC Bootstrap CLI developer
I want comprehensive unit tests for all modules
So that I can confidently make changes, prevent regressions, and ensure all functionality works correctly across different scenarios and edge cases

## Problem Statement
The TAC Bootstrap CLI currently has only 3 test files (test_cli.py, test_template_repo.py, test_version.py). The critical modules in domain/, application/, and infrastructure/ directories lack proper test coverage. This creates risks:
- Undetected bugs in core functionality (models validation, scaffold plan building, project detection)
- Difficulty refactoring or adding features without breaking existing functionality
- No validation of edge cases or error handling
- Unknown code coverage metrics
- Reduced confidence in code quality

## Solution Statement
Create comprehensive unit test suites for all 7 critical modules using pytest framework. Tests will:
- Cover all public methods and properties
- Test validation logic (models.py)
- Test fluent interface patterns (plan.py)
- Test service orchestration (scaffold_service.py, detect_service.py, doctor_service.py)
- Test template operations (template_repo.py - enhance existing tests)
- Test filesystem operations with real temporary directories (fs.py)
- Achieve >80% code coverage
- Use pytest fixtures for reusable test data
- Use tempfile for filesystem tests to avoid mocking
- Follow existing test patterns in test_template_repo.py

## Relevant Files
Modules to test:
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - 656 lines of Pydantic models, enums, validators, and helper functions
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - 144 lines of scaffold plan models with fluent interface
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - 396 lines of plan building and applying logic
- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py` - 404 lines of technology stack detection
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py` - 423 lines of validation and health checking
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - 369 lines of Jinja2 template management
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - 223 lines of filesystem operations

Existing test files (for reference):
- `tac_bootstrap_cli/tests/test_cli.py` - Basic CLI tests
- `tac_bootstrap_cli/tests/test_template_repo.py` - Template repository tests (to enhance)
- `tac_bootstrap_cli/tests/test_version.py` - Version tests

### New Files
- `tac_bootstrap_cli/tests/test_models.py` - Tests for domain/models.py (ProjectSpec validation, TACConfig defaults, helper functions)
- `tac_bootstrap_cli/tests/test_plan.py` - Tests for domain/plan.py (fluent interface, filtering methods, summary)
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - Tests for application/scaffold_service.py (build_plan, apply_plan)
- `tac_bootstrap_cli/tests/test_detect_service.py` - Tests for application/detect_service.py (language/framework/package manager detection)
- `tac_bootstrap_cli/tests/test_doctor_service.py` - Tests for application/doctor_service.py (diagnose, fix)
- `tac_bootstrap_cli/tests/test_fs.py` - Tests for infrastructure/fs.py (filesystem operations)

## Implementation Plan

### Phase 1: Foundation - Domain Model Tests
Set up test structure and implement tests for domain models, which are the foundation of all other components.

### Phase 2: Core Implementation - Service Tests
Implement tests for application services (scaffold, detect, doctor) and infrastructure components (fs).

### Phase 3: Integration - Coverage Validation
Run coverage reports, identify gaps, add missing tests to reach >80% coverage, and validate all tests pass.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Create test_models.py
Create `tac_bootstrap_cli/tests/test_models.py` with test classes:
- `TestProjectSpec`: Test name sanitization (whitespace, lowercase, hyphen replacement), empty name validation
- `TestTACConfig`: Test minimal config defaults (version=1, paths, agentic provider), full config creation
- `TestHelperFunctions`: Test `get_frameworks_for_language()` for all languages, test `get_package_managers_for_language()` for all languages, test `get_default_commands()` for Python+UV, TypeScript+pnpm, Go, Rust

### Task 2: Create test_plan.py
Create `tac_bootstrap_cli/tests/test_plan.py` with test classes:
- `TestFileOperation`: Test __str__ representation
- `TestDirectoryOperation`: Test __str__ representation
- `TestScaffoldPlan`: Test empty plan properties, test add_directory fluent interface, test add_file fluent interface, test method chaining, test get_files_to_create/overwrite/patch/skipped, test get_executable_files, test summary property

### Task 3: Create test_scaffold_service.py
Create `tac_bootstrap_cli/tests/test_scaffold_service.py` with:
- Pytest fixture for TACConfig
- `TestScaffoldService`: Test build_plan creates all required directories (.claude, adws, specs, etc.), test build_plan creates all required files (settings.json, config.yml), test build_plan marks .sh and .py scripts as executable, test apply_plan creates directory structure in temp dir, test apply_plan handles existing files (skip vs overwrite), test apply_plan with force flag

### Task 4: Create test_detect_service.py
Create `tac_bootstrap_cli/tests/test_detect_service.py` with:
- `TestDetectService`: Test detect Python by pyproject.toml/setup.py/requirements.txt, test detect TypeScript by tsconfig.json, test detect JavaScript by package.json, test detect Go by go.mod, test detect Rust by Cargo.toml, test detect UV by uv.lock, test detect Poetry by poetry.lock, test detect pnpm by pnpm-lock.yaml, test detect Next.js framework from package.json, test detect FastAPI from dependencies, test detect app_root (src/app), test detect commands from package.json scripts

### Task 5: Create test_doctor_service.py
Create `tac_bootstrap_cli/tests/test_doctor_service.py` with:
- `TestDoctorService`: Test diagnose empty directory reports errors, test diagnose valid setup is healthy, test diagnose missing .claude directory, test diagnose invalid settings.json, test diagnose missing essential commands, test diagnose non-executable hooks, test fix creates missing directories, test fix makes hooks executable, test fix reports success/failure counts

### Task 6: Create test_fs.py
Create `tac_bootstrap_cli/tests/test_fs.py` with:
- `TestFileSystem`: Test ensure_directory (creates, idempotent), test dir_exists, test write_file (creates parents, overwrites), test file_exists, test append_file (creates, appends, idempotent), test make_executable (adds permissions, preserves existing), test read_file (exists, doesn't exist with default), test copy_file, test remove_file (exists, doesn't exist), test remove_directory (empty, recursive)

### Task 7: Enhance test_template_repo.py
Review and enhance existing `tac_bootstrap_cli/tests/test_template_repo.py`:
- Add tests for case conversion filters (to_snake_case, to_kebab_case, to_pascal_case)
- Add tests for template_exists method
- Add tests for list_templates method
- Add tests for error handling (TemplateNotFoundError, TemplateRenderError)

### Task 8: Run All Validation Commands
Execute all validation commands to ensure tests pass and achieve coverage goals:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All tests should pass
- `cd tac_bootstrap_cli && uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing` - Coverage >80%
- `cd tac_bootstrap_cli && uv run pytest tests/test_models.py -v` - Models tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_plan.py -v` - Plan tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v` - Scaffold tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_detect_service.py -v` - Detect tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_doctor_service.py -v` - Doctor tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_fs.py -v` - Filesystem tests

## Testing Strategy

### Unit Tests
Each module will have focused unit tests:
- **Models**: Validation logic, field defaults, sanitization, helper functions
- **Plan**: Fluent interface, filtering, summary generation
- **Scaffold Service**: Plan building logic, plan application, file handling
- **Detect Service**: Language detection, framework detection, package manager detection, command detection
- **Doctor Service**: Diagnostic checks, auto-fix functionality, issue reporting
- **Template Repo**: Template rendering, filters, error handling (enhance existing)
- **Filesystem**: All CRUD operations, permission handling, idempotency

### Edge Cases
Critical edge cases to test:
- Empty/whitespace strings in ProjectSpec.name
- Missing directories when writing files (auto-creation)
- Existing files when applying scaffold plan (skip vs overwrite)
- Invalid JSON/YAML in doctor service checks
- Non-executable scripts requiring permission fix
- Template files that don't exist
- Idempotent operations (append_file, ensure_directory)
- Multiple languages/frameworks in detect service
- Permission errors (where applicable)

## Acceptance Criteria
1. `tests/test_models.py` covers all Pydantic models, validators, and 3 helper functions (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
2. `tests/test_plan.py` covers ScaffoldPlan fluent interface, all filter methods (get_files_to_create/overwrite/patch/skipped), and summary property
3. `tests/test_scaffold_service.py` covers build_plan (directories, files, executable marking) and apply_plan (creation, skipping, overwriting)
4. `tests/test_detect_service.py` covers detection for all 6 languages (Python, TypeScript, JavaScript, Go, Rust, Java), all major package managers, and frameworks
5. `tests/test_doctor_service.py` covers diagnose (all check types) and fix (directory creation, permission fixing) methods
6. `tests/test_fs.py` covers all 10 FileSystem methods (ensure_directory, write_file, append_file, make_executable, read_file, copy_file, remove_file, remove_directory, dir_exists, file_exists)
7. Enhanced `tests/test_template_repo.py` covers case conversion filters
8. All tests pass: `uv run pytest tests/ -v`
9. Code coverage >80%: `uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing`
10. No test uses excessive mocking - prefer real filesystem operations with tempfile

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All unit tests pass
- `cd tac_bootstrap_cli && uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing` - Coverage report >80%
- `cd tac_bootstrap_cli && uv run pytest tests/test_models.py -v` - Domain models tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_plan.py -v` - Scaffold plan tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_scaffold_service.py -v` - Scaffold service tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_detect_service.py -v` - Detect service tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_doctor_service.py -v` - Doctor service tests
- `cd tac_bootstrap_cli && uv run pytest tests/test_fs.py -v` - Filesystem tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting passes
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking passes

## Notes
- Follow existing test patterns in `test_template_repo.py` for consistency
- Use `tempfile.TemporaryDirectory()` for filesystem tests instead of mocking
- Use pytest fixtures for reusable test data (e.g., TACConfig)
- Use descriptive test names following "should" pattern in docstrings
- Group related tests in classes (e.g., TestProjectSpec, TestTACConfig)
- Test both happy paths and error cases
- Avoid integration tests - focus on unit testing individual methods
- The issue body contains complete example code for most tests - use as reference
- pytest-cov should already be available (check pyproject.toml dependencies)
- All tests should run in isolation without side effects
