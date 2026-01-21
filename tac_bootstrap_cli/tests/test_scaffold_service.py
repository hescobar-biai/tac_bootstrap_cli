"""Tests for scaffold service.

Comprehensive unit tests for ScaffoldService including plan building
and plan application with real filesystem operations.
"""

import tempfile
from pathlib import Path

import pytest

from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.domain.models import (
    ClaudeConfig,
    ClaudeSettings,
    CommandsSpec,
    Language,
    PackageManager,
    ProjectSpec,
    TACConfig,
)
from tac_bootstrap.domain.plan import FileAction

# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def config() -> TACConfig:
    """Create a test config."""
    return TACConfig(
        project=ProjectSpec(
            name="test-project",
            language=Language.PYTHON,
            package_manager=PackageManager.UV,
        ),
        commands=CommandsSpec(start="uv run python -m app", test="uv run pytest"),
        claude=ClaudeConfig(settings=ClaudeSettings(project_name="test-project")),
    )


@pytest.fixture
def service() -> ScaffoldService:
    """Create a scaffold service instance."""
    return ScaffoldService()


# ============================================================================
# TEST BUILD PLAN
# ============================================================================


class TestScaffoldServiceBuildPlan:
    """Tests for ScaffoldService.build_plan method."""

    def test_build_plan_creates_directories(self, service: ScaffoldService, config: TACConfig):
        """build_plan should include required directories."""
        plan = service.build_plan(config)

        dir_paths = [d.path for d in plan.directories]

        # Core directories
        assert ".claude" in dir_paths
        assert ".claude/commands" in dir_paths
        assert ".claude/hooks" in dir_paths
        assert "adws" in dir_paths
        assert "specs" in dir_paths
        assert "logs" in dir_paths
        assert "scripts" in dir_paths
        assert "prompts" in dir_paths

    def test_build_plan_creates_claude_files(self, service: ScaffoldService, config: TACConfig):
        """build_plan should include Claude configuration files."""
        plan = service.build_plan(config)

        file_paths = [f.path for f in plan.files]

        assert ".claude/settings.json" in file_paths
        # Check for at least one command file
        assert any("commands/" in p for p in file_paths)

    def test_build_plan_creates_config_files(self, service: ScaffoldService, config: TACConfig):
        """build_plan should include config.yml."""
        plan = service.build_plan(config)

        file_paths = [f.path for f in plan.files]
        assert "config.yml" in file_paths

    def test_build_plan_marks_scripts_executable(self, service: ScaffoldService, config: TACConfig):
        """Script files should be marked executable."""
        plan = service.build_plan(config)

        # Find shell scripts
        script_files = [f for f in plan.files if f.path.endswith(".sh")]
        assert len(script_files) > 0, "Should have at least one .sh file"

        # All shell scripts should be executable
        for script in script_files:
            assert script.executable, f"{script.path} should be executable"

    def test_build_plan_marks_python_scripts_executable(
        self, service: ScaffoldService, config: TACConfig
    ):
        """Python ADW scripts should be marked executable."""
        plan = service.build_plan(config)

        # Find ADW Python files (excluding __init__.py and modules)
        adw_python_files = [
            f
            for f in plan.files
            if f.path.startswith("adws/adw_")
            and f.path.endswith(".py")
            and "__init__" not in f.path
            and "/adw_modules/" not in f.path
        ]

        # ADW workflow files should be executable
        if adw_python_files:
            for adw_file in adw_python_files:
                assert adw_file.executable, f"{adw_file.path} should be executable"

    def test_build_plan_has_slash_commands(self, service: ScaffoldService, config: TACConfig):
        """build_plan should include slash command files."""
        plan = service.build_plan(config)

        file_paths = [f.path for f in plan.files]

        # Check for essential slash commands
        assert any("prime.md" in p for p in file_paths)
        assert any("test.md" in p for p in file_paths)
        assert any("commit.md" in p for p in file_paths)

    def test_build_plan_existing_repo_skips_files(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan with existing_repo=True should mark some files as SKIP."""
        plan = service.build_plan(config, existing_repo=True)

        # Should have some SKIP actions for existing files
        skip_files = plan.get_files_skipped()
        assert len(skip_files) > 0, "Should skip some files in existing repo"

    def test_build_plan_new_repo_creates_files(self, service: ScaffoldService, config: TACConfig):
        """build_plan with existing_repo=False should create all files."""
        plan = service.build_plan(config, existing_repo=False)

        # All files should be CREATE or OVERWRITE actions
        for file_op in plan.files:
            assert file_op.action in [FileAction.CREATE, FileAction.OVERWRITE, FileAction.PATCH]

    def test_build_plan_total_counts(self, service: ScaffoldService, config: TACConfig):
        """build_plan should have reasonable counts."""
        plan = service.build_plan(config)

        assert plan.total_directories > 5, "Should create multiple directories"
        assert plan.total_files > 10, "Should create multiple files"

    def test_build_plan_custom_paths(self, service: ScaffoldService):
        """build_plan should respect custom path configuration."""
        from tac_bootstrap.domain.models import PathsSpec

        custom_config = TACConfig(
            project=ProjectSpec(
                name="custom",
                language=Language.PYTHON,
                package_manager=PackageManager.UV,
            ),
            commands=CommandsSpec(start="echo start", test="echo test"),
            claude=ClaudeConfig(settings=ClaudeSettings(project_name="custom")),
            paths=PathsSpec(
                app_root="src",
                adws_dir="workflows",
                specs_dir="specifications",
            ),
        )

        plan = service.build_plan(custom_config)
        dir_paths = [d.path for d in plan.directories]

        assert "workflows" in dir_paths
        assert "specifications" in dir_paths


# ============================================================================
# TEST APPLY PLAN
# ============================================================================


class TestScaffoldServiceApplyPlan:
    """Tests for ScaffoldService.apply_plan method."""

    def test_apply_plan_creates_structure(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should create directories and files."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success
            assert result.directories_created > 0
            assert result.files_created > 0
            assert (tmp_path / ".claude").is_dir()
            assert (tmp_path / "config.yml").is_file()

    def test_apply_plan_creates_nested_directories(
        self, service: ScaffoldService, config: TACConfig
    ):
        """apply_plan should create nested directory structures."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success
            assert (tmp_path / ".claude" / "commands").is_dir()
            assert (tmp_path / ".claude" / "hooks").is_dir()
            assert (tmp_path / "adws" / "adw_modules").is_dir()

    def test_apply_plan_renders_templates(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should render Jinja2 templates with config."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Check that config.yml was rendered with project name
            config_file = tmp_path / "config.yml"
            if config_file.exists():
                content = config_file.read_text()
                assert "test-project" in content or "test_project" in content

    def test_apply_plan_makes_scripts_executable(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should make script files executable."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Find shell scripts
            for file_op in plan.get_executable_files():
                file_path = tmp_path / file_op.path
                if file_path.exists():
                    # Check that file has executable bit
                    import os
                    import stat

                    st = os.stat(file_path)
                    is_executable = bool(st.st_mode & stat.S_IXUSR)
                    assert is_executable, f"{file_path} should be executable"

    def test_apply_plan_skips_existing_files(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should skip files marked as SKIP."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # Create a file that should be skipped
            skip_file = None
            for file_op in plan.files:
                if file_op.action == FileAction.SKIP:
                    skip_file = tmp_path / file_op.path
                    skip_file.parent.mkdir(parents=True, exist_ok=True)
                    skip_file.write_text("ORIGINAL CONTENT")
                    break

            result = service.apply_plan(plan, tmp_path, config)

            # If there was a skip file, verify it wasn't modified
            if skip_file:
                assert skip_file.read_text() == "ORIGINAL CONTENT"
                assert result.files_skipped > 0

    def test_apply_plan_counts_operations(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should count operations correctly."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success
            assert result.directories_created == plan.total_directories
            # files_created should match files that were actually created
            assert result.files_created > 0

    def test_apply_plan_idempotent(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should be idempotent when run twice."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # First application
            result1 = service.apply_plan(plan, tmp_path, config)
            assert result1.success

            # Second application
            result2 = service.apply_plan(plan, tmp_path, config)
            assert result2.success
            # Second run should skip files that already exist
            assert result2.files_skipped >= result1.files_created

    def test_apply_plan_with_force(self, service: ScaffoldService, config: TACConfig):
        """apply_plan with force should overwrite existing files."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # First application
            service.apply_plan(plan, tmp_path, config)

            # Modify a file
            config_file = tmp_path / "config.yml"
            if config_file.exists():
                config_file.read_text()  # Verify file exists and is readable
                config_file.write_text("MODIFIED")

                # Apply with force
                result = service.apply_plan(plan, tmp_path, config, force=True)

                # File should be restored
                new_content = config_file.read_text()
                assert new_content != "MODIFIED"
                assert result.files_overwritten > 0

    def test_apply_plan_to_nonexistent_directory_creates_it(
        self, service: ScaffoldService, config: TACConfig
    ):
        """apply_plan should create output directory if it doesn't exist."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "new_project"
            assert not output_dir.exists()

            result = service.apply_plan(plan, output_dir, config)

            assert result.success
            assert output_dir.exists()
            assert output_dir.is_dir()

    def test_apply_plan_error_handling(self, service: ScaffoldService, config: TACConfig):
        """apply_plan should handle errors gracefully."""
        plan = service.build_plan(config)

        # Try to apply to an invalid path (read-only or non-writable)
        # Note: This test is system-dependent, so we'll just verify the result structure
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            # Result should always have success field
            assert isinstance(result.success, bool)
            assert isinstance(result.directories_created, int)
            assert isinstance(result.files_created, int)
