"""Tests for filesystem operations.

Comprehensive unit tests for FileSystem class including all CRUD operations,
permission handling, and idempotency.
"""

import os
import stat
import tempfile
from pathlib import Path

import pytest

from tac_bootstrap.infrastructure.fs import FileSystem


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def fs():
    """Create a FileSystem instance."""
    return FileSystem()


# ============================================================================
# TEST DIRECTORY OPERATIONS
# ============================================================================


class TestFileSystemDirectories:
    """Tests for directory operations."""

    def test_ensure_directory_creates_new(self, fs: FileSystem):
        """ensure_directory should create new directory."""
        with tempfile.TemporaryDirectory() as tmp:
            new_dir = Path(tmp) / "test_dir"
            assert not new_dir.exists()

            result = fs.ensure_directory(new_dir)

            assert result is True
            assert new_dir.is_dir()

    def test_ensure_directory_idempotent(self, fs: FileSystem):
        """ensure_directory should be idempotent."""
        with tempfile.TemporaryDirectory() as tmp:
            new_dir = Path(tmp) / "test_dir"

            # First call creates
            result1 = fs.ensure_directory(new_dir)
            assert result1 is True

            # Second call is idempotent
            result2 = fs.ensure_directory(new_dir)
            assert result2 is False
            assert new_dir.is_dir()

    def test_ensure_directory_creates_parents(self, fs: FileSystem):
        """ensure_directory should create parent directories."""
        with tempfile.TemporaryDirectory() as tmp:
            nested_dir = Path(tmp) / "parent" / "child" / "grandchild"
            assert not nested_dir.exists()

            result = fs.ensure_directory(nested_dir)

            assert result is True
            assert nested_dir.is_dir()
            assert (Path(tmp) / "parent").is_dir()
            assert (Path(tmp) / "parent" / "child").is_dir()

    def test_dir_exists_true(self, fs: FileSystem):
        """dir_exists should return True for existing directory."""
        with tempfile.TemporaryDirectory() as tmp:
            assert fs.dir_exists(Path(tmp)) is True

    def test_dir_exists_false(self, fs: FileSystem):
        """dir_exists should return False for non-existent directory."""
        with tempfile.TemporaryDirectory() as tmp:
            non_existent = Path(tmp) / "does_not_exist"
            assert fs.dir_exists(non_existent) is False

    def test_dir_exists_false_for_file(self, fs: FileSystem):
        """dir_exists should return False for files."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("test")

            assert fs.dir_exists(file_path) is False

    def test_remove_directory_empty(self, fs: FileSystem):
        """remove_directory should remove empty directory."""
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test_dir"
            test_dir.mkdir()

            result = fs.remove_directory(test_dir)

            assert result is True
            assert not test_dir.exists()

    def test_remove_directory_recursive(self, fs: FileSystem):
        """remove_directory with recursive should remove directory tree."""
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = Path(tmp) / "test_dir"
            test_dir.mkdir()
            (test_dir / "file.txt").write_text("test")
            (test_dir / "subdir").mkdir()

            result = fs.remove_directory(test_dir, recursive=True)

            assert result is True
            assert not test_dir.exists()

    def test_remove_directory_nonexistent(self, fs: FileSystem):
        """remove_directory should return False for non-existent directory."""
        with tempfile.TemporaryDirectory() as tmp:
            non_existent = Path(tmp) / "does_not_exist"

            result = fs.remove_directory(non_existent)

            assert result is False


# ============================================================================
# TEST FILE WRITE OPERATIONS
# ============================================================================


class TestFileSystemWrite:
    """Tests for file write operations."""

    def test_write_file_creates_new(self, fs: FileSystem):
        """write_file should create new file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "Hello, World!"

            fs.write_file(file_path, content)

            assert file_path.is_file()
            assert file_path.read_text() == content

    def test_write_file_overwrites_existing(self, fs: FileSystem):
        """write_file should overwrite existing file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("Original content")

            fs.write_file(file_path, "New content")

            assert file_path.read_text() == "New content"

    def test_write_file_creates_parents(self, fs: FileSystem):
        """write_file should create parent directories."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "parent" / "child" / "test.txt"

            fs.write_file(file_path, "test")

            assert file_path.is_file()
            assert file_path.read_text() == "test"

    def test_write_file_with_encoding(self, fs: FileSystem):
        """write_file should respect encoding parameter."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "Hello, 世界!"

            fs.write_file(file_path, content, encoding="utf-8")

            assert file_path.read_text(encoding="utf-8") == content


# ============================================================================
# TEST FILE READ OPERATIONS
# ============================================================================


class TestFileSystemRead:
    """Tests for file read operations."""

    def test_read_file_existing(self, fs: FileSystem):
        """read_file should read existing file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "Test content"
            file_path.write_text(content)

            result = fs.read_file(file_path)

            assert result == content

    def test_read_file_nonexistent_returns_none(self, fs: FileSystem):
        """read_file should return None for non-existent file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.txt"

            result = fs.read_file(file_path)

            assert result is None

    def test_read_file_nonexistent_with_default(self, fs: FileSystem):
        """read_file should return default for non-existent file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.txt"

            result = fs.read_file(file_path, default="DEFAULT")

            assert result == "DEFAULT"

    def test_read_file_with_encoding(self, fs: FileSystem):
        """read_file should respect encoding parameter."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "Hello, 世界!"
            file_path.write_text(content, encoding="utf-8")

            result = fs.read_file(file_path, encoding="utf-8")

            assert result == content

    def test_file_exists_true(self, fs: FileSystem):
        """file_exists should return True for existing file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("test")

            assert fs.file_exists(file_path) is True

    def test_file_exists_false(self, fs: FileSystem):
        """file_exists should return False for non-existent file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.txt"

            assert fs.file_exists(file_path) is False

    def test_file_exists_false_for_directory(self, fs: FileSystem):
        """file_exists should return False for directories."""
        with tempfile.TemporaryDirectory() as tmp:
            assert fs.file_exists(Path(tmp)) is False


# ============================================================================
# TEST APPEND FILE
# ============================================================================


class TestFileSystemAppend:
    """Tests for append_file operation."""

    def test_append_file_creates_new(self, fs: FileSystem):
        """append_file should create new file if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "First line"

            fs.append_file(file_path, content)

            assert file_path.is_file()
            assert file_path.read_text() == content

    def test_append_file_appends_to_existing(self, fs: FileSystem):
        """append_file should append to existing file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("First line")

            fs.append_file(file_path, "Second line")

            content = file_path.read_text()
            assert "First line" in content
            assert "Second line" in content

    def test_append_file_idempotent(self, fs: FileSystem):
        """append_file should be idempotent (no duplication)."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            content = "Unique line"

            fs.append_file(file_path, content)
            fs.append_file(file_path, content)
            fs.append_file(file_path, content)

            # Content should appear only once
            result = file_path.read_text()
            assert result.count(content.strip()) == 1

    def test_append_file_with_custom_separator(self, fs: FileSystem):
        """append_file should use custom separator."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("First")

            fs.append_file(file_path, "Second", separator=" | ")

            assert file_path.read_text() == "First | Second"

    def test_append_file_creates_parents(self, fs: FileSystem):
        """append_file should create parent directories."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "parent" / "child" / "test.txt"

            fs.append_file(file_path, "test")

            assert file_path.is_file()


# ============================================================================
# TEST EXECUTABLE PERMISSIONS
# ============================================================================


class TestFileSystemExecutable:
    """Tests for make_executable operation."""

    def test_make_executable_adds_permission(self, fs: FileSystem):
        """make_executable should add execute permission."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "script.sh"
            file_path.write_text("#!/bin/bash\necho 'test'")

            # Remove execute permissions
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)

            # Verify not executable
            st = os.stat(file_path)
            assert not (st.st_mode & stat.S_IXUSR)

            # Make executable
            fs.make_executable(file_path)

            # Verify executable
            st = os.stat(file_path)
            assert st.st_mode & stat.S_IXUSR

    def test_make_executable_preserves_existing_permissions(self, fs: FileSystem):
        """make_executable should preserve existing permissions."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "script.sh"
            file_path.write_text("#!/bin/bash")

            # Set specific permissions
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)

            fs.make_executable(file_path)

            st = os.stat(file_path)
            # Should still have read for user and group
            assert st.st_mode & stat.S_IRUSR
            assert st.st_mode & stat.S_IRGRP
            # Should have execute for user
            assert st.st_mode & stat.S_IXUSR

    def test_make_executable_nonexistent_file(self, fs: FileSystem):
        """make_executable should handle non-existent file gracefully."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.sh"

            # Should not raise error
            fs.make_executable(file_path)


# ============================================================================
# TEST FILE COPY AND REMOVE
# ============================================================================


class TestFileSystemCopyRemove:
    """Tests for copy_file and remove_file operations."""

    def test_copy_file(self, fs: FileSystem):
        """copy_file should copy file to destination."""
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "source.txt"
            dst = Path(tmp) / "dest.txt"
            content = "Test content"
            src.write_text(content)

            fs.copy_file(src, dst)

            assert dst.is_file()
            assert dst.read_text() == content

    def test_copy_file_creates_parent_dirs(self, fs: FileSystem):
        """copy_file should create parent directories for destination."""
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "source.txt"
            dst = Path(tmp) / "parent" / "child" / "dest.txt"
            src.write_text("test")

            fs.copy_file(src, dst)

            assert dst.is_file()
            assert dst.read_text() == "test"

    def test_copy_file_preserves_metadata(self, fs: FileSystem):
        """copy_file should preserve file metadata."""
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "source.txt"
            dst = Path(tmp) / "dest.txt"
            src.write_text("test")

            # Make source executable
            os.chmod(src, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

            fs.copy_file(src, dst)

            # Destination should also be executable
            st = os.stat(dst)
            assert st.st_mode & stat.S_IXUSR

    def test_remove_file_removes_existing(self, fs: FileSystem):
        """remove_file should remove existing file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("test")

            result = fs.remove_file(file_path)

            assert result is True
            assert not file_path.exists()

    def test_remove_file_nonexistent(self, fs: FileSystem):
        """remove_file should return False for non-existent file."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "nonexistent.txt"

            result = fs.remove_file(file_path)

            assert result is False


# ============================================================================
# TEST EDGE CASES
# ============================================================================


class TestFileSystemEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_write_empty_file(self, fs: FileSystem):
        """write_file should handle empty content."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "empty.txt"

            fs.write_file(file_path, "")

            assert file_path.is_file()
            assert file_path.read_text() == ""

    def test_append_empty_content(self, fs: FileSystem):
        """append_file should handle empty content."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "test.txt"
            file_path.write_text("Original")

            fs.append_file(file_path, "")

            # Should not modify file when appending empty
            # (empty content is already "in" the file)
            content = file_path.read_text()
            assert "Original" in content

    def test_multiline_content(self, fs: FileSystem):
        """FileSystem should handle multiline content."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "multiline.txt"
            content = "Line 1\nLine 2\nLine 3"

            fs.write_file(file_path, content)

            assert file_path.read_text() == content

    def test_unicode_content(self, fs: FileSystem):
        """FileSystem should handle Unicode content."""
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "unicode.txt"
            content = "Hello 世界 🌍 مرحبا"

            fs.write_file(file_path, content)

            assert fs.read_file(file_path) == content
