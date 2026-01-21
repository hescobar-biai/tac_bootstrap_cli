"""Tests for scaffold plan models.

Comprehensive unit tests for ScaffoldPlan and related models,
including fluent interface, filtering methods, and summary generation.
"""


from tac_bootstrap.domain.plan import (
    DirectoryOperation,
    FileAction,
    FileOperation,
    ScaffoldPlan,
)

# ============================================================================
# TEST FILE OPERATION
# ============================================================================


class TestFileOperation:
    """Tests for FileOperation model."""

    def test_str_representation_create(self):
        """String representation should show action and path."""
        file_op = FileOperation(path="test.txt", action=FileAction.CREATE)
        assert str(file_op) == "[create] test.txt"

    def test_str_representation_overwrite(self):
        """String representation for overwrite action."""
        file_op = FileOperation(path="config.yml", action=FileAction.OVERWRITE)
        assert str(file_op) == "[overwrite] config.yml"

    def test_str_representation_patch(self):
        """String representation for patch action."""
        file_op = FileOperation(path="readme.md", action=FileAction.PATCH)
        assert str(file_op) == "[patch] readme.md"

    def test_str_representation_skip(self):
        """String representation for skip action."""
        file_op = FileOperation(path="existing.txt", action=FileAction.SKIP)
        assert str(file_op) == "[skip] existing.txt"

    def test_executable_defaults_false(self):
        """Executable should default to False."""
        file_op = FileOperation(path="test.txt", action=FileAction.CREATE)
        assert file_op.executable is False

    def test_executable_can_be_true(self):
        """Should allow setting executable to True."""
        file_op = FileOperation(path="script.sh", action=FileAction.CREATE, executable=True)
        assert file_op.executable is True


# ============================================================================
# TEST DIRECTORY OPERATION
# ============================================================================


class TestDirectoryOperation:
    """Tests for DirectoryOperation model."""

    def test_str_representation(self):
        """String representation should show mkdir and path."""
        dir_op = DirectoryOperation(path=".claude")
        assert str(dir_op) == "[mkdir] .claude/"

    def test_str_representation_with_nested_path(self):
        """Should handle nested directory paths."""
        dir_op = DirectoryOperation(path=".claude/commands")
        assert str(dir_op) == "[mkdir] .claude/commands/"

    def test_reason_defaults_empty(self):
        """Reason should default to empty string."""
        dir_op = DirectoryOperation(path="test")
        assert dir_op.reason == ""

    def test_reason_can_be_provided(self):
        """Should allow providing reason."""
        dir_op = DirectoryOperation(path=".claude", reason="Claude Code configuration")
        assert dir_op.reason == "Claude Code configuration"


# ============================================================================
# TEST SCAFFOLD PLAN
# ============================================================================


class TestScaffoldPlan:
    """Tests for ScaffoldPlan model."""

    def test_empty_plan(self):
        """Empty plan should have zero counts."""
        plan = ScaffoldPlan()
        assert plan.total_directories == 0
        assert plan.total_files == 0
        assert len(plan.directories) == 0
        assert len(plan.files) == 0

    def test_add_directory_fluent(self):
        """add_directory should return self for chaining."""
        plan = ScaffoldPlan()
        result = plan.add_directory("test", "Test dir")
        assert result is plan
        assert plan.total_directories == 1
        assert plan.directories[0].path == "test"
        assert plan.directories[0].reason == "Test dir"

    def test_add_file_fluent(self):
        """add_file should return self for chaining."""
        plan = ScaffoldPlan()
        result = plan.add_file("test.txt", FileAction.CREATE)
        assert result is plan
        assert plan.total_files == 1
        assert plan.files[0].path == "test.txt"
        assert plan.files[0].action == FileAction.CREATE

    def test_chaining_directories(self):
        """Should support chaining multiple directory additions."""
        plan = (
            ScaffoldPlan()
            .add_directory("dir1", "First directory")
            .add_directory("dir2", "Second directory")
            .add_directory("dir3")
        )
        assert plan.total_directories == 3
        assert plan.directories[0].path == "dir1"
        assert plan.directories[1].path == "dir2"
        assert plan.directories[2].path == "dir3"

    def test_chaining_files(self):
        """Should support chaining multiple file additions."""
        plan = (
            ScaffoldPlan()
            .add_file("file1.txt", FileAction.CREATE)
            .add_file("file2.txt", FileAction.OVERWRITE)
        )
        assert plan.total_files == 2
        assert plan.files[0].path == "file1.txt"
        assert plan.files[1].path == "file2.txt"

    def test_chaining_mixed(self):
        """Should support chaining directories and files together."""
        plan = (
            ScaffoldPlan()
            .add_directory("src")
            .add_file("src/main.py", FileAction.CREATE)
            .add_directory("tests")
            .add_file("tests/test_main.py", FileAction.CREATE)
        )
        assert plan.total_directories == 2
        assert plan.total_files == 2

    def test_get_files_to_create(self):
        """Should filter files by CREATE action."""
        plan = ScaffoldPlan()
        plan.add_file("create1.txt", FileAction.CREATE)
        plan.add_file("skip.txt", FileAction.SKIP)
        plan.add_file("create2.txt", FileAction.CREATE)
        plan.add_file("patch.txt", FileAction.PATCH)

        create_files = plan.get_files_to_create()
        assert len(create_files) == 2
        assert all(f.action == FileAction.CREATE for f in create_files)
        assert create_files[0].path == "create1.txt"
        assert create_files[1].path == "create2.txt"

    def test_get_files_to_overwrite(self):
        """Should filter files by OVERWRITE action."""
        plan = ScaffoldPlan()
        plan.add_file("create.txt", FileAction.CREATE)
        plan.add_file("overwrite1.txt", FileAction.OVERWRITE)
        plan.add_file("overwrite2.txt", FileAction.OVERWRITE)

        overwrite_files = plan.get_files_to_overwrite()
        assert len(overwrite_files) == 2
        assert all(f.action == FileAction.OVERWRITE for f in overwrite_files)

    def test_get_files_to_patch(self):
        """Should filter files by PATCH action."""
        plan = ScaffoldPlan()
        plan.add_file("create.txt", FileAction.CREATE)
        plan.add_file("patch1.txt", FileAction.PATCH)
        plan.add_file("patch2.txt", FileAction.PATCH)
        plan.add_file("patch3.txt", FileAction.PATCH)

        patch_files = plan.get_files_to_patch()
        assert len(patch_files) == 3
        assert all(f.action == FileAction.PATCH for f in patch_files)

    def test_get_files_skipped(self):
        """Should filter files by SKIP action."""
        plan = ScaffoldPlan()
        plan.add_file("create.txt", FileAction.CREATE)
        plan.add_file("skip1.txt", FileAction.SKIP)
        plan.add_file("skip2.txt", FileAction.SKIP)

        skipped_files = plan.get_files_skipped()
        assert len(skipped_files) == 2
        assert all(f.action == FileAction.SKIP for f in skipped_files)

    def test_get_executable_files(self):
        """Should filter executable files."""
        plan = ScaffoldPlan()
        plan.add_file("script1.sh", FileAction.CREATE, executable=True)
        plan.add_file("readme.md", FileAction.CREATE, executable=False)
        plan.add_file("script2.py", FileAction.CREATE, executable=True)

        executable_files = plan.get_executable_files()
        assert len(executable_files) == 2
        assert all(f.executable for f in executable_files)
        assert executable_files[0].path == "script1.sh"
        assert executable_files[1].path == "script2.py"

    def test_filter_methods_empty_plan(self):
        """Filter methods should return empty lists for empty plan."""
        plan = ScaffoldPlan()
        assert plan.get_files_to_create() == []
        assert plan.get_files_to_overwrite() == []
        assert plan.get_files_to_patch() == []
        assert plan.get_files_skipped() == []
        assert plan.get_executable_files() == []

    def test_summary_empty_plan(self):
        """Summary should describe empty plan."""
        plan = ScaffoldPlan()
        summary = plan.summary
        assert "0 directories" in summary
        assert "0 files to create" in summary
        assert "0 to patch" in summary
        assert "0 skipped" in summary

    def test_summary_with_data(self):
        """Summary should include counts."""
        plan = ScaffoldPlan()
        plan.add_directory("dir1")
        plan.add_directory("dir2")
        plan.add_file("file1.txt", FileAction.CREATE)
        plan.add_file("file2.txt", FileAction.CREATE)
        plan.add_file("file3.txt", FileAction.SKIP)
        plan.add_file("file4.txt", FileAction.PATCH)

        summary = plan.summary
        assert "2 directories" in summary
        assert "2 files to create" in summary
        assert "1 to patch" in summary
        assert "1 skipped" in summary

    def test_total_directories_property(self):
        """total_directories should return correct count."""
        plan = ScaffoldPlan()
        assert plan.total_directories == 0

        plan.add_directory("dir1")
        assert plan.total_directories == 1

        plan.add_directory("dir2")
        plan.add_directory("dir3")
        assert plan.total_directories == 3

    def test_total_files_property(self):
        """total_files should return correct count."""
        plan = ScaffoldPlan()
        assert plan.total_files == 0

        plan.add_file("file1.txt", FileAction.CREATE)
        assert plan.total_files == 1

        plan.add_file("file2.txt", FileAction.SKIP)
        plan.add_file("file3.txt", FileAction.PATCH)
        assert plan.total_files == 3

    def test_add_file_with_template(self):
        """Should support adding file with template."""
        plan = ScaffoldPlan()
        plan.add_file(
            "settings.json",
            FileAction.CREATE,
            template="claude/settings.json.j2",
            reason="Claude settings",
        )

        assert plan.files[0].template == "claude/settings.json.j2"
        assert plan.files[0].reason == "Claude settings"
        assert plan.files[0].content is None

    def test_add_file_with_content(self):
        """Should support adding file with static content."""
        plan = ScaffoldPlan()
        plan.add_file(
            "readme.txt",
            FileAction.CREATE,
            content="# README\n\nProject description",
            reason="Docs",
        )

        assert plan.files[0].content == "# README\n\nProject description"
        assert plan.files[0].template is None
        assert plan.files[0].reason == "Docs"

    def test_complex_plan_scenario(self):
        """Test a complex realistic scenario."""
        plan = (
            ScaffoldPlan()
            # Directories
            .add_directory(".claude", "Claude Code config")
            .add_directory(".claude/commands", "Slash commands")
            .add_directory("adws", "AI workflows")
            .add_directory("specs", "Specifications")
            # Files
            .add_file(
                ".claude/settings.json", FileAction.CREATE, template="claude/settings.json.j2"
            )
            .add_file("config.yml", FileAction.CREATE, template="config.yml.j2")
            .add_file("README.md", FileAction.SKIP, reason="User may have custom README")
            .add_file(".gitignore", FileAction.PATCH, content="# TAC Bootstrap\nlogs/\n")
            .add_file("scripts/setup.sh", FileAction.CREATE, executable=True)
        )

        # Verify structure
        assert plan.total_directories == 4
        assert plan.total_files == 5

        # Verify filters
        assert len(plan.get_files_to_create()) == 3
        assert len(plan.get_files_skipped()) == 1
        assert len(plan.get_files_to_patch()) == 1
        assert len(plan.get_executable_files()) == 1

        # Verify summary
        summary = plan.summary
        assert "4 directories" in summary
        assert "3 files to create" in summary
        assert "1 to patch" in summary
        assert "1 skipped" in summary
