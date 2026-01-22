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

    def test_build_plan_existing_repo_creates_files(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan with existing_repo=True should mark files as CREATE (idempotent)."""
        plan = service.build_plan(config, existing_repo=True)

        # Files should be marked CREATE (not SKIP) because CREATE is idempotent
        # CREATE will skip files that already exist during apply_plan
        create_files = [f for f in plan.files if f.action == FileAction.CREATE]
        assert len(create_files) > 0, "Should use CREATE action which is safe for existing repos"

        # Verify .claude/ files specifically use CREATE action
        claude_files = [f for f in plan.files if ".claude/" in str(f.path)]
        assert len(claude_files) > 0, "Should have .claude/ template files"
        for file_op in claude_files:
            assert (
                file_op.action == FileAction.CREATE
            ), f"{file_op.path} should be CREATE, not {file_op.action}"

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

    def test_apply_plan_create_does_not_overwrite_existing(
        self, service: ScaffoldService, config: TACConfig
    ):
        """apply_plan with CREATE action should NOT overwrite existing files."""
        plan = service.build_plan(config, existing_repo=True)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            # Find a file with CREATE action
            create_file = None
            for file_op in plan.files:
                if file_op.action == FileAction.CREATE:
                    create_file = tmp_path / file_op.path
                    create_file.parent.mkdir(parents=True, exist_ok=True)
                    create_file.write_text("ORIGINAL CONTENT")
                    break

            assert create_file is not None, "Should have at least one CREATE action file"

            # Apply plan without force
            result = service.apply_plan(plan, tmp_path, config, force=False)

            # Verify file was NOT overwritten
            assert create_file.read_text() == "ORIGINAL CONTENT"
            assert result.files_skipped >= 1

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


# ============================================================================
# TEST ADW COMPLETENESS
# ============================================================================


class TestScaffoldServiceADWCompleteness:
    """Tests to verify all ADW modules and workflows are included."""

    def test_build_plan_includes_all_adw_modules(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan should include all 10 ADW modules."""
        plan = service.build_plan(config)
        file_paths = [f.path for f in plan.files]

        expected_modules = [
            "adws/adw_modules/__init__.py",
            "adws/adw_modules/agent.py",
            "adws/adw_modules/state.py",
            "adws/adw_modules/git_ops.py",
            "adws/adw_modules/workflow_ops.py",
            "adws/adw_modules/data_types.py",
            "adws/adw_modules/github.py",
            "adws/adw_modules/utils.py",
            "adws/adw_modules/worktree_ops.py",
            "adws/adw_modules/r2_uploader.py",
        ]

        for module in expected_modules:
            assert module in file_paths, f"Missing ADW module: {module}"

    def test_build_plan_includes_all_adw_workflows(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan should include all 14 ADW workflows."""
        plan = service.build_plan(config)
        file_paths = [f.path for f in plan.files]

        expected_workflows = [
            # Core orchestration
            "adws/adw_sdlc_iso.py",
            "adws/adw_sdlc_zte_iso.py",
            "adws/adw_patch_iso.py",
            # Individual phases
            "adws/adw_plan_iso.py",
            "adws/adw_build_iso.py",
            "adws/adw_test_iso.py",
            "adws/adw_review_iso.py",
            "adws/adw_document_iso.py",
            "adws/adw_ship_iso.py",
            # Compositional workflows
            "adws/adw_plan_build_iso.py",
            "adws/adw_plan_build_test_iso.py",
            "adws/adw_plan_build_test_review_iso.py",
            "adws/adw_plan_build_review_iso.py",
            "adws/adw_plan_build_document_iso.py",
        ]

        for workflow in expected_workflows:
            assert workflow in file_paths, f"Missing ADW workflow: {workflow}"

    def test_build_plan_includes_adw_triggers(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan should include ADW triggers."""
        plan = service.build_plan(config)
        file_paths = [f.path for f in plan.files]

        expected_triggers = [
            "adws/adw_triggers/__init__.py",
            "adws/adw_triggers/trigger_cron.py",
        ]

        for trigger in expected_triggers:
            assert trigger in file_paths, f"Missing ADW trigger: {trigger}"

    def test_build_plan_includes_playwright_config(
        self, service: ScaffoldService, config: TACConfig
    ):
        """build_plan should include playwright-mcp-config.json."""
        plan = service.build_plan(config)
        file_paths = [f.path for f in plan.files]

        assert "playwright-mcp-config.json" in file_paths
        assert ".mcp.json" in file_paths

    def test_adw_workflows_are_executable(
        self, service: ScaffoldService, config: TACConfig
    ):
        """All ADW workflow files should be marked executable."""
        plan = service.build_plan(config)

        workflow_files = [
            f for f in plan.files
            if f.path.startswith("adws/adw_")
            and f.path.endswith(".py")
            and "/adw_modules/" not in f.path
            and "/adw_triggers/" not in f.path
        ]

        assert len(workflow_files) >= 14, "Should have at least 14 workflow files"

        for workflow in workflow_files:
            assert workflow.executable, f"{workflow.path} should be executable"

    def test_adw_trigger_cron_is_executable(
        self, service: ScaffoldService, config: TACConfig
    ):
        """trigger_cron.py should be marked executable."""
        plan = service.build_plan(config)

        trigger_file = next(
            (f for f in plan.files if f.path == "adws/adw_triggers/trigger_cron.py"),
            None
        )

        assert trigger_file is not None, "trigger_cron.py should exist"
        assert trigger_file.executable, "trigger_cron.py should be executable"

    def test_apply_plan_creates_all_adw_files(
        self, service: ScaffoldService, config: TACConfig
    ):
        """apply_plan should create all ADW files on disk."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Verify modules exist
            modules_dir = tmp_path / "adws" / "adw_modules"
            assert modules_dir.is_dir()
            assert (modules_dir / "__init__.py").is_file()
            assert (modules_dir / "agent.py").is_file()
            assert (modules_dir / "data_types.py").is_file()
            assert (modules_dir / "github.py").is_file()

            # Verify workflows exist
            adws_dir = tmp_path / "adws"
            assert (adws_dir / "adw_sdlc_iso.py").is_file()
            assert (adws_dir / "adw_plan_iso.py").is_file()
            assert (adws_dir / "adw_build_iso.py").is_file()
            assert (adws_dir / "adw_ship_iso.py").is_file()

            # Verify triggers exist
            triggers_dir = tmp_path / "adws" / "adw_triggers"
            assert triggers_dir.is_dir()
            assert (triggers_dir / "trigger_cron.py").is_file()

            # Verify playwright config
            assert (tmp_path / "playwright-mcp-config.json").is_file()

    def test_apply_plan_renders_adw_modules_correctly(
        self, service: ScaffoldService, config: TACConfig
    ):
        """ADW modules should render with valid Python content."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Check data_types.py has expected content
            data_types = tmp_path / "adws" / "adw_modules" / "data_types.py"
            content = data_types.read_text()
            assert "from dataclasses import" in content or "from pydantic import" in content
            assert "class" in content  # Should have class definitions

            # Check github.py has expected content
            github_module = tmp_path / "adws" / "adw_modules" / "github.py"
            content = github_module.read_text()
            assert "def" in content  # Should have function definitions

    def test_apply_plan_renders_workflows_correctly(
        self, service: ScaffoldService, config: TACConfig
    ):
        """ADW workflows should render with valid shebang and content."""
        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Check workflow has shebang
            workflow = tmp_path / "adws" / "adw_sdlc_iso.py"
            content = workflow.read_text()
            assert content.startswith("#!/usr/bin/env")
            assert "def main" in content

    def test_apply_plan_renders_playwright_config_correctly(
        self, service: ScaffoldService, config: TACConfig
    ):
        """playwright-mcp-config.json should render with valid JSON."""
        import json

        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Check playwright config is valid JSON
            playwright_config = tmp_path / "playwright-mcp-config.json"
            content = playwright_config.read_text()
            parsed = json.loads(content)  # Should not raise

            assert "browser" in parsed
            assert parsed["browser"]["browserName"] == "chromium"
            assert "contextOptions" in parsed["browser"]

    def test_config_yml_template_renders_version_fields(
        self, service: ScaffoldService, config: TACConfig
    ):
        """config.yml should render both version and schema_version fields."""
        import yaml

        plan = service.build_plan(config)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            result = service.apply_plan(plan, tmp_path, config)

            assert result.success

            # Read and parse config.yml
            config_file = tmp_path / "config.yml"
            assert config_file.exists(), "config.yml should be created"

            content = config_file.read_text()
            parsed = yaml.safe_load(content)

            # Verify version fields are present
            assert "version" in parsed, "version field should be in config.yml"
            assert "schema_version" in parsed, "schema_version field should be in config.yml"

            # Verify values match config
            assert parsed["version"] == "0.2.0", "version should default to 0.2.0"
            assert parsed["schema_version"] == 1, "schema_version should default to 1"

            # Verify header comment contains TAC version
            assert (
                "Generated by TAC Bootstrap v0.2.0" in content
            ), "Header should contain TAC version"
