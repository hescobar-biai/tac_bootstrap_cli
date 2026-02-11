"""Tests for the Comprehensive Testing Framework (Feature 9).

Comprehensive test suite covering test scaffolding generation for
unit, integration, E2E, and load tests, plus coverage config and CI workflows.
"""

from pathlib import Path

import pytest

from tac_bootstrap.application.test_generator import TestGenerator


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def test_gen() -> TestGenerator:
    """Create a TestGenerator instance."""
    return TestGenerator(
        project_name="test-project",
        language="python",
        framework="fastapi",
    )


@pytest.fixture
def simple_gen() -> TestGenerator:
    """Create a simple TestGenerator instance."""
    return TestGenerator(
        project_name="simple-app",
        language="python",
        framework="none",
    )


@pytest.fixture
def project_dir(tmp_path: Path) -> Path:
    """Create a temporary project directory."""
    return tmp_path


@pytest.fixture
def module_file(tmp_path: Path) -> Path:
    """Create a sample module file."""
    src = tmp_path / "src"
    src.mkdir()
    module = src / "user_service.py"
    module.write_text('"""User service module."""\n\nclass UserService:\n    pass\n')
    return module


# ============================================================================
# TEST UNIT TEST GENERATION
# ============================================================================


class TestUnitTestGeneration:
    """Tests for unit test scaffolding."""

    def test_generate_unit_tests_content(self, test_gen: TestGenerator, module_file: Path):
        """Should generate valid pytest unit test code."""
        content = test_gen.generate_unit_tests(module_file)
        assert "import pytest" in content
        assert "class TestUserService" in content
        assert "def test_creation" in content
        assert "def test_validation" in content

    def test_generate_unit_tests_to_file(
        self, test_gen: TestGenerator, module_file: Path, project_dir: Path
    ):
        """Should write unit test file to output directory."""
        output_dir = project_dir / "tests" / "unit"
        test_gen.generate_unit_tests(module_file, output_dir=output_dir)

        test_file = output_dir / "test_user_service.py"
        assert test_file.exists()
        content = test_file.read_text()
        assert "TestUserService" in content

    def test_generate_unit_tests_no_overwrite(
        self, test_gen: TestGenerator, module_file: Path, project_dir: Path
    ):
        """Should not overwrite existing test files without force."""
        output_dir = project_dir / "tests" / "unit"
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / "test_user_service.py"
        test_file.write_text("# existing content\n")

        test_gen.generate_unit_tests(module_file, output_dir=output_dir)
        assert test_file.read_text() == "# existing content\n"

    def test_generate_unit_tests_force_overwrite(
        self, test_gen: TestGenerator, module_file: Path, project_dir: Path
    ):
        """Should overwrite with force=True."""
        output_dir = project_dir / "tests" / "unit"
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / "test_user_service.py"
        test_file.write_text("# old content\n")

        test_gen.generate_unit_tests(module_file, output_dir=output_dir, force=True)
        content = test_file.read_text()
        assert "import pytest" in content

    def test_unit_test_has_fixtures(self, test_gen: TestGenerator, module_file: Path):
        """Generated tests should include fixtures."""
        content = test_gen.generate_unit_tests(module_file)
        assert "@pytest.fixture" in content
        assert "sample_data" in content

    def test_unit_test_has_error_handling(self, test_gen: TestGenerator, module_file: Path):
        """Generated tests should include error handling tests."""
        content = test_gen.generate_unit_tests(module_file)
        assert "test_error_handling" in content
        assert "pytest.raises" in content


# ============================================================================
# TEST INTEGRATION TEST GENERATION
# ============================================================================


class TestIntegrationTestGeneration:
    """Tests for integration test scaffolding."""

    def test_generate_fastapi_integration(self, test_gen: TestGenerator):
        """FastAPI integration tests should use TestClient."""
        content = test_gen.generate_integration_tests()
        assert "TestClient" in content
        assert "test_health_check" in content
        assert "TestCRUDEndpoints" in content

    def test_generate_generic_integration(self, simple_gen: TestGenerator):
        """Generic integration tests should use basic structure."""
        content = simple_gen.generate_integration_tests()
        assert "TestIntegration" in content
        assert "test_full_workflow" in content

    def test_integration_tests_to_file(
        self, test_gen: TestGenerator, project_dir: Path
    ):
        """Should write integration test files."""
        test_gen.generate_integration_tests(project_path=project_dir)

        int_dir = project_dir / "tests" / "integration"
        assert int_dir.is_dir()
        assert (int_dir / "__init__.py").exists()

    def test_integration_tests_auth_headers(self, test_gen: TestGenerator):
        """FastAPI integration should include auth headers fixture."""
        content = test_gen.generate_integration_tests()
        assert "auth_headers" in content
        assert "Authorization" in content


# ============================================================================
# TEST E2E TEST GENERATION
# ============================================================================


class TestE2ETestGeneration:
    """Tests for E2E test scaffolding."""

    def test_generate_e2e_tests(self, test_gen: TestGenerator):
        """E2E tests should reference Playwright."""
        content = test_gen.generate_e2e_tests()
        assert "playwright" in content.lower()
        assert "TestHomePage" in content
        assert "TestUserWorkflow" in content

    def test_e2e_tests_to_file(self, test_gen: TestGenerator, project_dir: Path):
        """Should write E2E test files."""
        test_gen.generate_e2e_tests(project_path=project_dir)

        e2e_dir = project_dir / "tests" / "e2e"
        assert e2e_dir.is_dir()
        assert (e2e_dir / "__init__.py").exists()

    def test_e2e_tests_project_name(self, test_gen: TestGenerator):
        """E2E tests should reference the project name."""
        content = test_gen.generate_e2e_tests()
        assert "test-project" in content


# ============================================================================
# TEST LOAD TEST GENERATION
# ============================================================================


class TestLoadTestGeneration:
    """Tests for load test scaffolding."""

    def test_generate_load_tests(self, test_gen: TestGenerator):
        """Load tests should reference Locust and include standalone option."""
        content = test_gen.generate_load_tests()
        assert "locust" in content.lower() or "Locust" in content
        assert "run_simple_load_test" in content

    def test_load_tests_to_file(self, test_gen: TestGenerator, project_dir: Path):
        """Should write load test files."""
        test_gen.generate_load_tests(project_path=project_dir)

        load_dir = project_dir / "tests" / "load"
        assert load_dir.is_dir()
        assert (load_dir / "test_load.py").exists()

    def test_load_tests_has_metrics(self, test_gen: TestGenerator):
        """Load tests should track performance metrics."""
        content = test_gen.generate_load_tests()
        assert "avg_time" in content
        assert "requests_per_second" in content


# ============================================================================
# TEST COVERAGE CONFIGURATION
# ============================================================================


class TestCoverageConfig:
    """Tests for coverage.py configuration setup."""

    def test_setup_coverage_config(self, test_gen: TestGenerator, project_dir: Path):
        """Should create .coveragerc file."""
        config_path = test_gen.setup_coverage_config(project_dir)
        assert config_path.exists()
        assert config_path.name == ".coveragerc"

    def test_coverage_config_content(self, test_gen: TestGenerator, project_dir: Path):
        """Coverage config should have correct settings."""
        test_gen.setup_coverage_config(project_dir)
        content = (project_dir / ".coveragerc").read_text()
        assert "source = src" in content
        assert "fail_under = 80" in content
        assert "show_missing = True" in content

    def test_coverage_config_project_name(self, test_gen: TestGenerator, project_dir: Path):
        """Coverage config should reference project name."""
        test_gen.setup_coverage_config(project_dir)
        content = (project_dir / ".coveragerc").read_text()
        assert "test-project" in content


# ============================================================================
# TEST CI WORKFLOW
# ============================================================================


class TestCIWorkflow:
    """Tests for GitHub Actions CI workflow setup."""

    def test_setup_ci_workflow(self, test_gen: TestGenerator, project_dir: Path):
        """Should create .github/workflows/ci.yml."""
        workflow_path = test_gen.setup_ci_workflow(project_dir)
        assert workflow_path.exists()

    def test_ci_workflow_content(self, test_gen: TestGenerator, project_dir: Path):
        """CI workflow should contain test and lint steps."""
        test_gen.setup_ci_workflow(project_dir)
        content = (project_dir / ".github" / "workflows" / "ci.yml").read_text()
        assert "pytest" in content
        assert "ruff" in content
        assert "mypy" in content

    def test_ci_workflow_python_versions(self, test_gen: TestGenerator, project_dir: Path):
        """CI workflow should test multiple Python versions."""
        test_gen.setup_ci_workflow(project_dir)
        content = (project_dir / ".github" / "workflows" / "ci.yml").read_text()
        assert "3.10" in content
        assert "3.12" in content


# ============================================================================
# TEST GENERATE ALL
# ============================================================================


class TestGenerateAll:
    """Tests for comprehensive test generation."""

    def test_generate_all_creates_files(self, test_gen: TestGenerator, project_dir: Path):
        """generate_all should create all test files."""
        files = test_gen.generate_all(project_dir)
        assert len(files) >= 6  # unit, integration, e2e, load, coverage, ci, conftest

    def test_generate_all_creates_conftest(self, test_gen: TestGenerator, project_dir: Path):
        """generate_all should create conftest.py."""
        test_gen.generate_all(project_dir)
        conftest = project_dir / "tests" / "conftest.py"
        assert conftest.exists()
        content = conftest.read_text()
        assert "project_root" in content

    def test_generate_all_creates_init_files(self, test_gen: TestGenerator, project_dir: Path):
        """generate_all should create __init__.py files."""
        test_gen.generate_all(project_dir)
        assert (project_dir / "tests" / "unit" / "__init__.py").exists()

    def test_generate_all_no_overwrite(self, test_gen: TestGenerator, project_dir: Path):
        """generate_all should not overwrite without force."""
        test_gen.generate_all(project_dir)
        first_count = len(list(project_dir.rglob("*.py")))

        # Second call should not create more files
        test_gen.generate_all(project_dir, force=False)
        second_count = len(list(project_dir.rglob("*.py")))
        assert first_count == second_count

    def test_generator_with_config(self):
        """Generator should extract values from config object."""

        class MockProject:
            name = "config-project"
            language = type("L", (), {"value": "typescript"})()
            framework = type("F", (), {"value": "nextjs"})()

        class MockConfig:
            project = MockProject()

        gen = TestGenerator(config=MockConfig())
        assert gen.project_name == "config-project"
        assert gen.language == "typescript"
        assert gen.framework == "nextjs"
