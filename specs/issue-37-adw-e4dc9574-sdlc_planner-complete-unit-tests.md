# Feature: Complete Unit Tests for TAC Bootstrap CLI

## Metadata
issue_number: `37`
adw_id: `e4dc9574`
issue_json: `{"number":37,"title":"TAREA 8.1: Tests unitarios completos","body":"# Prompt para Agente\n\n## Contexto\nNecesitamos tests unitarios para todos los modulos implementados para asegurar\ncalidad y prevenir regresiones.\n\n## Objetivo\nCrear tests unitarios completos para:\n- domain/models.py\n- domain/plan.py\n- application/scaffold_service.py\n- application/detect_service.py\n- application/doctor_service.py\n- infrastructure/template_repo.py\n- infrastructure/fs.py\n\n## Archivos a Crear\n\n### 1. `tests/test_models.py`\n\n```python\n\"\"\"Tests for domain models.\"\"\"\nimport pytest\nfrom tac_bootstrap.domain.models import (\n    TACConfig,\n    ProjectSpec,\n    CommandsSpec,\n    ClaudeConfig,\n    ClaudeSettings,\n    Language,\n    Framework,\n    PackageManager,\n    get_frameworks_for_language,\n    get_package_managers_for_language,\n    get_default_commands,\n)\n\n\nclass TestProjectSpec:\n    \"\"\"Tests for ProjectSpec model.\"\"\"\n\n    def test_name_sanitization(self):\n        \"\"\"Project name should be sanitized.\"\"\"\n        spec = ProjectSpec(\n            name=\"  My Project  \",\n            language=Language.PYTHON,\n            package_manager=PackageManager.UV,\n        )\n        assert spec.name == \"my-project\"\n\n    def test_empty_name_raises(self):\n        \"\"\"Empty name should raise ValueError.\"\"\"\n        with pytest.raises(ValueError):\n            ProjectSpec(\n                name=\"\",\n                language=Language.PYTHON,\n                package_manager=PackageManager.UV,\n            )\n\n\nclass TestTACConfig:\n    \"\"\"Tests for TACConfig model.\"\"\"\n\n    def test_minimal_config(self):\n        \"\"\"Minimal config should have defaults.\"\"\"\n        config = TACConfig(\n            project=ProjectSpec(\n                name=\"test\",\n                language=Language.PYTHON,\n                package_manager=PackageManager.UV,\n            ),\n            commands=CommandsSpec(start=\"echo start\", test=\"echo test\"),\n            claude=ClaudeConfig(settings=ClaudeSettings(project_name=\"test\")),\n        )\n        assert config.version == 1\n        assert config.paths.adws_dir == \"adws\"\n        assert config.agentic.provider.value == \"claude_code\"\n\n\nclass TestHelperFunctions:\n    \"\"\"Tests for helper functions.\"\"\"\n\n    def test_frameworks_for_python(self):\n        \"\"\"Python should have FastAPI, Django, Flask.\"\"\"\n        frameworks = get_frameworks_for_language(Language.PYTHON)\n        assert Framework.FASTAPI in frameworks\n        assert Framework.DJANGO in frameworks\n\n    def test_package_managers_for_typescript(self):\n        \"\"\"TypeScript should have pnpm, npm, yarn, bun.\"\"\"\n        managers = get_package_managers_for_language(Language.TYPESCRIPT)\n        assert PackageManager.PNPM in managers\n        assert PackageManager.NPM in managers\n\n    def test_default_commands_python_uv(self):\n        \"\"\"Python + UV should have correct defaults.\"\"\"\n        commands = get_default_commands(Language.PYTHON, PackageManager.UV)\n        assert \"uv run pytest\" in commands[\"test\"]\n        assert \"uv run ruff\" in commands[\"lint\"]\n```\n\n### 2. `tests/test_plan.py`\n\n```python\n\"\"\"Tests for scaffold plan models.\"\"\"\nimport pytest\nfrom tac_bootstrap.domain.plan import (\n    ScaffoldPlan,\n    FileOperation,\n    FileAction,\n    DirectoryOperation,\n)\n\n\nclass TestScaffoldPlan:\n    \"\"\"Tests for ScaffoldPlan model.\"\"\"\n\n    def test_empty_plan(self):\n        \"\"\"Empty plan should have zero counts.\"\"\"\n        plan = ScaffoldPlan()\n        assert plan.total_directories == 0\n        assert plan.total_files == 0\n\n    def test_add_directory_fluent(self):\n        \"\"\"add_directory should return self for chaining.\"\"\"\n        plan = ScaffoldPlan()\n        result = plan.add_directory(\"test\", \"Test dir\")\n        assert result is plan\n        assert plan.total_directories == 1\n\n    def test_add_file_fluent(self):\n        \"\"\"add_file should return self for chaining.\"\"\"\n        plan = ScaffoldPlan()\n        result = plan.add_file(\"test.txt\", FileAction.CREATE)\n        assert result is plan\n        assert plan.total_files == 1\n\n    def test_chaining(self):\n        \"\"\"Should support method chaining.\"\"\"\n        plan = (\n            ScaffoldPlan()\n            .add_directory(\"dir1\")\n            .add_directory(\"dir2\")\n            .add_file(\"file1.txt\")\n            .add_file(\"file2.txt\")\n        )\n        assert plan.total_directories == 2\n        assert plan.total_files == 2\n\n    def test_get_files_by_action(self):\n        \"\"\"Should filter files by action.\"\"\"\n        plan = ScaffoldPlan()\n        plan.add_file(\"create.txt\", FileAction.CREATE)\n        plan.add_file(\"skip.txt\", FileAction.SKIP)\n        plan.add_file(\"patch.txt\", FileAction.PATCH)\n\n        assert len(plan.get_files_to_create()) == 1\n        assert len(plan.get_files_skipped()) == 1\n        assert len(plan.get_files_to_patch()) == 1\n\n    def test_summary(self):\n        \"\"\"Summary should include counts.\"\"\"\n        plan = ScaffoldPlan()\n        plan.add_directory(\"dir\")\n        plan.add_file(\"file.txt\", FileAction.CREATE)\n        plan.add_file(\"skip.txt\", FileAction.SKIP)\n\n        summary = plan.summary\n        assert \"1 directories\" in summary\n        assert \"1 files to create\" in summary\n        assert \"1 skipped\" in summary\n```\n\n### 3. `tests/test_scaffold_service.py`\n\n```python\n\"\"\"Tests for scaffold service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\n\nfrom tac_bootstrap.application.scaffold_service import ScaffoldService\nfrom tac_bootstrap.domain.models import (\n    TACConfig,\n    ProjectSpec,\n    CommandsSpec,\n    ClaudeConfig,\n    ClaudeSettings,\n    Language,\n    PackageManager,\n)\n\n\n@pytest.fixture\ndef config():\n    \"\"\"Create a test config.\"\"\"\n    return TACConfig(\n        project=ProjectSpec(\n            name=\"test-project\",\n            language=Language.PYTHON,\n            package_manager=PackageManager.UV,\n        ),\n        commands=CommandsSpec(start=\"uv run python -m app\", test=\"uv run pytest\"),\n        claude=ClaudeConfig(settings=ClaudeSettings(project_name=\"test-project\")),\n    )\n\n\nclass TestScaffoldService:\n    \"\"\"Tests for ScaffoldService.\"\"\"\n\n    def test_build_plan_creates_directories(self, config):\n        \"\"\"build_plan should include required directories.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        dir_paths = [d.path for d in plan.directories]\n        assert \".claude\" in dir_paths\n        assert \".claude/commands\" in dir_paths\n        assert \"adws\" in dir_paths\n\n    def test_build_plan_creates_files(self, config):\n        \"\"\"build_plan should include required files.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        file_paths = [f.path for f in plan.files]\n        assert \".claude/settings.json\" in file_paths\n        assert \"config.yml\" in file_paths\n\n    def test_build_plan_marks_scripts_executable(self, config):\n        \"\"\"Script files should be marked executable.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        script_files = [f for f in plan.files if f.path.endswith(\".sh\")]\n        assert all(f.executable for f in script_files)\n\n    def test_apply_plan_creates_structure(self, config):\n        \"\"\"apply_plan should create directories and files.\"\"\"\n        service = ScaffoldService()\n        plan = service.build_plan(config)\n\n        with tempfile.TemporaryDirectory() as tmp:\n            result = service.apply_plan(plan, Path(tmp), config)\n\n            assert result.success\n            assert result.directories_created > 0\n            assert result.files_created > 0\n            assert (Path(tmp) / \".claude\").is_dir()\n            assert (Path(tmp) / \"config.yml\").is_file()\n```\n\n### 4. `tests/test_detect_service.py`\n\n```python\n\"\"\"Tests for detect service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\nimport json\n\nfrom tac_bootstrap.application.detect_service import DetectService\nfrom tac_bootstrap.domain.models import Language, PackageManager, Framework\n\n\nclass TestDetectService:\n    \"\"\"Tests for DetectService.\"\"\"\n\n    def test_detect_python_by_pyproject(self):\n        \"\"\"Should detect Python by pyproject.toml.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").write_text(\"[project]\\nname='test'\")\n            result = detector.detect(Path(tmp))\n\n            assert result.language == Language.PYTHON\n\n    def test_detect_uv_by_lock(self):\n        \"\"\"Should detect UV by uv.lock.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").touch()\n            (Path(tmp) / \"uv.lock\").touch()\n            result = detector.detect(Path(tmp))\n\n            assert result.package_manager == PackageManager.UV\n\n    def test_detect_typescript_by_tsconfig(self):\n        \"\"\"Should detect TypeScript by tsconfig.json.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"tsconfig.json\").write_text(\"{}\")\n            result = detector.detect(Path(tmp))\n\n            assert result.language == Language.TYPESCRIPT\n\n    def test_detect_nextjs_from_package_json(self):\n        \"\"\"Should detect Next.js framework.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"tsconfig.json\").write_text(\"{}\")\n            (Path(tmp) / \"package.json\").write_text(\n                json.dumps({\"dependencies\": {\"next\": \"^14.0.0\"}})\n            )\n            result = detector.detect(Path(tmp))\n\n            assert result.framework == Framework.NEXTJS\n\n    def test_detect_app_root(self):\n        \"\"\"Should detect src as app root.\"\"\"\n        detector = DetectService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            (Path(tmp) / \"pyproject.toml\").touch()\n            (Path(tmp) / \"src\").mkdir()\n            result = detector.detect(Path(tmp))\n\n            assert result.app_root == \"src\"\n```\n\n### 5. `tests/test_doctor_service.py`\n\n```python\n\"\"\"Tests for doctor service.\"\"\"\nimport pytest\nfrom pathlib import Path\nimport tempfile\nimport json\n\nfrom tac_bootstrap.application.doctor_service import DoctorService, Severity\n\n\nclass TestDoctorService:\n    \"\"\"Tests for DoctorService.\"\"\"\n\n    def test_diagnose_empty_directory(self):\n        \"\"\"Empty directory should have errors.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            report = doctor.diagnose(Path(tmp))\n\n            assert not report.healthy\n            assert any(i.severity == Severity.ERROR for i in report.issues)\n\n    def test_diagnose_valid_setup(self):\n        \"\"\"Valid setup should be healthy.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            tmp_path = Path(tmp)\n            # Create minimal valid structure\n            (tmp_path / \".claude\" / \"commands\").mkdir(parents=True)\n            (tmp_path / \".claude\" / \"hooks\").mkdir(parents=True)\n            (tmp_path / \".claude\" / \"settings.json\").write_text('{\"version\": 1}')\n            (tmp_path / \".claude\" / \"commands\" / \"prime.md\").write_text(\"# Prime\")\n            (tmp_path / \".claude\" / \"commands\" / \"test.md\").write_text(\"# Test\")\n            (tmp_path / \".claude\" / \"commands\" / \"commit.md\").write_text(\"# Commit\")\n            (tmp_path / \"config.yml\").write_text(\"project:\\n  name: test\\ncommands:\\n  start: echo\")\n\n            report = doctor.diagnose(tmp_path)\n\n            # Should have no errors (may have warnings for optional stuff)\n            errors = [i for i in report.issues if i.severity == Severity.ERROR]\n            assert len(errors) == 0\n\n    def test_fix_creates_directories(self):\n        \"\"\"fix() should create missing directories.\"\"\"\n        doctor = DoctorService()\n\n        with tempfile.TemporaryDirectory() as tmp:\n            report = doctor.diagnose(Path(tmp))\n            result = doctor.fix(Path(tmp), report)\n\n            # Should have fixed some directory issues\n            assert result.fixed_count > 0\n            assert (Path(tmp) / \".claude\").is_dir()\n```\n\n## Criterios de Aceptacion\n1. [ ] Tests para models.py cubren validacion y helpers\n2. [ ] Tests para plan.py cubren fluent interface y queries\n3. [ ] Tests para scaffold_service cubren build y apply\n4. [ ] Tests para detect_service cubren cada lenguaje\n5. [ ] Tests para doctor_service cubren diagnose y fix\n6. [ ] Coverage > 80%\n\n## Comandos de Verificacion\n```bash\ncd /Volumes/MAc1/Celes/tac_bootstrap/tac_bootstrap_cli\n\n# Run all tests\nuv run pytest tests/ -v\n\n# With coverage\nuv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing\n\n# Run specific test file\nuv run pytest tests/test_models.py -v\n```\n\n## NO hacer\n- No crear tests de integracion complejos\n- No mockear filesystem innecesariamente"}`

## Feature Description
Verify and validate comprehensive unit tests for all TAC Bootstrap CLI modules to ensure quality, prevent regressions, and maintain robust validation of the core functionality. All test files have been created, and this task focuses on verification, execution, and ensuring >80% code coverage.

## User Story
As a TAC Bootstrap CLI developer
I want to verify that comprehensive unit tests cover all modules
So that I can confidently make changes, prevent regressions, and ensure all functionality works correctly across different scenarios and edge cases

## Problem Statement
The TAC Bootstrap CLI has test files created for all critical modules (test_models.py, test_plan.py, test_scaffold_service.py, test_detect_service.py, test_doctor_service.py, test_template_repo.py, test_fs.py). However, we need to:
- Verify all tests are comprehensive and complete
- Execute all tests to ensure they pass
- Measure code coverage to ensure >80% threshold
- Identify and fill any coverage gaps
- Validate that tests follow best practices

## Solution Statement
Verify, execute, and validate existing comprehensive unit test suites for all 7 critical modules:
- Run all tests and ensure they pass
- Generate coverage reports and analyze results
- Identify any gaps in test coverage
- Add missing tests if coverage is below 80%
- Validate tests follow best practices (fixtures, tempfile, clear assertions)
- Ensure no integration tests in unit test suite
- Confirm tests are isolated and idempotent

## Relevant Files
Modules to test:
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - 656 lines of Pydantic models, enums, validators, and helper functions
- `tac_bootstrap_cli/tac_bootstrap/domain/plan.py` - 144 lines of scaffold plan models with fluent interface
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - 396 lines of plan building and applying logic
- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py` - 404 lines of technology stack detection
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py` - 423 lines of validation and health checking
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - 369 lines of Jinja2 template management
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py` - 223 lines of filesystem operations

Existing comprehensive test files:
- `tac_bootstrap_cli/tests/test_models.py` - 377 lines - Tests for domain/models.py (ProjectSpec validation, TACConfig defaults, helper functions)
- `tac_bootstrap_cli/tests/test_plan.py` - 335 lines - Tests for domain/plan.py (fluent interface, filtering methods, summary)
- `tac_bootstrap_cli/tests/test_scaffold_service.py` - 378 lines - Tests for application/scaffold_service.py (build_plan, apply_plan, many tests skipped for integration)
- `tac_bootstrap_cli/tests/test_detect_service.py` - 520 lines - Tests for application/detect_service.py (language/framework/package manager detection)
- `tac_bootstrap_cli/tests/test_doctor_service.py` - 453 lines - Tests for application/doctor_service.py (diagnose, fix)
- `tac_bootstrap_cli/tests/test_template_repo.py` - 468 lines - Tests for infrastructure/template_repo.py (rendering, filters, discovery)
- `tac_bootstrap_cli/tests/test_fs.py` - 485 lines - Tests for infrastructure/fs.py (filesystem operations)
- `tac_bootstrap_cli/tests/test_cli.py` - Basic CLI tests
- `tac_bootstrap_cli/tests/test_version.py` - Version tests

### New Files
All test files already exist. No new files need to be created.

## Implementation Plan

### Phase 1: Test Verification
Verify all test files are comprehensive and cover the required functionality.

### Phase 2: Test Execution
Run all tests to ensure they pass and measure coverage.

### Phase 3: Coverage Analysis & Gap Filling
Analyze coverage report, identify gaps, and add missing tests if coverage is below 80%.

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Verify Existing Test Files Are Comprehensive
- Review `test_models.py` (377 lines) to ensure it covers:
  - ProjectSpec validation (name sanitization, empty names)
  - TACConfig defaults (version, paths, agentic provider)
  - CommandsSpec validation
  - All helper functions (get_frameworks_for_language, get_package_managers_for_language, get_default_commands)
  - All enums (Language, Framework, PackageManager, Architecture)

### Task 2: Verify test_plan.py Coverage
- Review `test_plan.py` (335 lines) to ensure it covers:
  - FileOperation and DirectoryOperation models
  - ScaffoldPlan fluent interface (add_directory, add_file chaining)
  - All filter methods (get_files_to_create/overwrite/patch/skipped, get_executable_files)
  - Summary property with correct counts
  - Edge cases (empty plan, complex chaining)

### Task 3: Verify test_scaffold_service.py Coverage
- Review `test_scaffold_service.py` (378 lines) to ensure it covers:
  - build_plan creates all required directories
  - build_plan creates all required files
  - build_plan marks scripts as executable
  - apply_plan creates directory structure (note: many integration tests are marked @pytest.mark.skip)
  - Understand which tests are unit vs integration

### Task 4: Verify test_detect_service.py Coverage
- Review `test_detect_service.py` (520 lines) to ensure it covers:
  - Language detection for all 6+ languages (Python, TypeScript, JavaScript, Go, Rust, Java)
  - Package manager detection for all managers (uv, poetry, pip, pnpm, npm, yarn, bun, cargo, maven, gradle)
  - Framework detection (FastAPI, Django, Flask, Next.js, NestJS, Express, React, Spring, etc.)
  - App root detection (src, app, lib)
  - Command detection from package.json scripts
  - Full scenarios with combined detection

### Task 5: Verify test_doctor_service.py Coverage
- Review `test_doctor_service.py` (453 lines) to ensure it covers:
  - diagnose empty directory (reports errors)
  - diagnose valid setup (healthy)
  - diagnose specific issues (missing directories, invalid JSON, missing commands, non-executable hooks)
  - fix creates directories
  - fix makes hooks executable
  - fix reports counts correctly
  - Issue severity classification
  - DiagnosticReport behavior

### Task 6: Verify test_template_repo.py Coverage
- Review `test_template_repo.py` (468 lines) to ensure it covers:
  - Case conversion filters (to_snake_case, to_kebab_case, to_pascal_case)
  - Template rendering (simple, multiline, nested, with filters)
  - Template discovery (template_exists, list_templates, get_template_content)
  - Error handling (TemplateNotFoundError, TemplateRenderError)
  - Autoescape configuration

### Task 7: Verify test_fs.py Coverage
- Review `test_fs.py` (485 lines) to ensure it covers:
  - Directory operations (ensure_directory, dir_exists, remove_directory)
  - File write operations (write_file, creates parents, encoding)
  - File read operations (read_file, file_exists, with defaults)
  - Append operations (append_file, idempotency, custom separator)
  - Executable permissions (make_executable, preserves permissions)
  - Copy and remove operations
  - Edge cases (empty content, unicode, multiline)

### Task 8: Run All Tests and Generate Coverage Report
Execute all validation commands:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Verify all tests pass
- `cd tac_bootstrap_cli && uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing` - Generate coverage report
- Analyze coverage percentage for each module
- Identify uncovered lines

### Task 9: Add Missing Tests (If Coverage < 80%)
If coverage is below 80%:
- Identify specific uncovered lines from coverage report
- Add targeted tests for uncovered code paths
- Focus on critical business logic and edge cases
- Re-run coverage to verify improvement

### Task 10: Final Validation
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - All tests pass
- `cd tac_bootstrap_cli && uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing` - Coverage >80%
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting passes
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking passes
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

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
1. [x] `tests/test_models.py` (377 lines) covers all Pydantic models, validators, and helper functions - VERIFIED
2. [x] `tests/test_plan.py` (335 lines) covers ScaffoldPlan fluent interface and all filter methods - VERIFIED
3. [x] `tests/test_scaffold_service.py` (378 lines) covers build_plan and apply_plan (many integration tests skipped) - VERIFIED
4. [x] `tests/test_detect_service.py` (520 lines) covers all languages, package managers, and frameworks - VERIFIED
5. [x] `tests/test_doctor_service.py` (453 lines) covers diagnose and fix methods comprehensively - VERIFIED
6. [x] `tests/test_fs.py` (485 lines) covers all 10 FileSystem methods - VERIFIED
7. [x] `tests/test_template_repo.py` (468 lines) covers rendering, filters, and error handling - VERIFIED
8. [ ] All tests pass: `uv run pytest tests/ -v` - NEEDS EXECUTION
9. [ ] Code coverage >80%: `uv run pytest tests/ --cov=tac_bootstrap --cov-report=term-missing` - NEEDS VERIFICATION
10. [x] Tests use real filesystem operations with tempfile (no excessive mocking) - VERIFIED
11. [ ] No linting errors: `uv run ruff check .` - NEEDS VERIFICATION
12. [ ] No type checking errors: `uv run mypy tac_bootstrap/` - NEEDS VERIFICATION

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

### Current Status
All test files have been created and are comprehensive (>2600 lines total across 7 test files):

1. **test_models.py** (377 lines) - ✅ Complete
   - ProjectSpec validation with name sanitization (whitespace, spaces to hyphens, lowercase)
   - TACConfig defaults (version, paths, agentic provider)
   - Helper functions for all languages (Python, TypeScript, JavaScript, Go, Rust, Java)
   - CommandsSpec required and optional fields
   - Edge cases (empty names, whitespace-only names)

2. **test_plan.py** (335 lines) - ✅ Complete
   - FileOperation and DirectoryOperation string representations
   - ScaffoldPlan fluent interface with method chaining
   - All filtering methods (create, overwrite, patch, skip, executable)
   - Count properties and summary generation
   - Complex realistic scenarios with nested operations

3. **test_scaffold_service.py** (378 lines) - ✅ Complete (with skipped integration tests)
   - build_plan creates all required directories and files
   - Marks scripts (.sh, .py ADWs) as executable
   - Handles existing vs new repo scenarios
   - Custom path configuration
   - Integration tests marked as @pytest.mark.skip (requires real templates)

4. **test_detect_service.py** (520 lines) - ✅ Complete
   - Language detection for 6+ languages (Python, TypeScript, JavaScript, Go, Rust, Java)
   - Package manager detection (uv, poetry, pip, pnpm, npm, yarn, bun, cargo, maven, gradle)
   - Framework detection (FastAPI, Django, Flask, Next.js, NestJS, Express, React, Spring)
   - App root detection (src, app, lib)
   - Command detection from package.json scripts
   - Full end-to-end scenarios with combined detection

5. **test_doctor_service.py** (453 lines) - ✅ Complete
   - Diagnose empty directories (reports errors)
   - Diagnose valid setups (healthy)
   - Specific issue detection (missing directories, invalid JSON, missing commands, non-executable hooks)
   - Fix operations (creates directories, makes hooks executable)
   - Issue severity classification
   - Idempotency of fix operations
   - DiagnosticReport behavior

6. **test_fs.py** (485 lines) - ✅ Complete
   - Directory operations (ensure_directory, dir_exists, remove_directory)
   - File write operations (creates parents, handles encoding)
   - File read operations (with defaults)
   - Append operations (idempotent, custom separator)
   - Executable permissions (preserves existing permissions)
   - Copy and remove operations
   - Edge cases (empty content, Unicode, multiline)

7. **test_template_repo.py** (468 lines) - ✅ Complete
   - Case conversion filters (snake_case, kebab-case, PascalCase)
   - Template rendering (simple, multiline, nested, with filters)
   - Template discovery (exists, list, get content)
   - Error handling (TemplateNotFoundError, TemplateRenderError)
   - Autoescape configuration

### Best Practices Followed
- ✅ Use `tempfile.TemporaryDirectory()` for filesystem tests (no excessive mocking)
- ✅ Use pytest fixtures for reusable test data (e.g., TACConfig, sample_config)
- ✅ Descriptive test names with docstrings
- ✅ Tests grouped in classes by functionality
- ✅ Both happy paths and error cases covered
- ✅ Edge cases tested (empty strings, Unicode, permissions, idempotency)

### Integration Tests
Many integration tests in `test_scaffold_service.py` are marked `@pytest.mark.skip(reason="Requires real templates - integration test")` because they:
- Require real templates to be present in the templates directory
- Test the full end-to-end scaffolding process
- Are integration tests rather than unit tests
- Keeping them skipped is the correct approach for this unit test suite

### Main Focus
**This task is about VERIFICATION and EXECUTION, not creation:**
1. ✅ All test files created
2. 🔄 Run tests to ensure they pass
3. 🔄 Generate coverage report
4. 🔄 Verify coverage >80%
5. 🔄 Add missing tests only if gaps are found

### Dependencies
- pytest-cov is available in dev dependencies (pyproject.toml)
- All tests run in isolation using temporary directories
- No external dependencies or mocking required for most tests
