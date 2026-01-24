"""
IDK: filesystem-operations, file-io, directory-creation, safe-writes, idempotent-operations
Responsibility: Provides safe, idempotent filesystem operations for file and directory management
Invariants: Creates parent directories automatically, operations are cross-platform compatible
"""

import os
import shutil
import stat
from pathlib import Path
from typing import Optional


class FileSystem:
    """
    IDK: filesystem-adapter, file-operations, directory-operations
    Responsibility: Encapsulates filesystem operations for scaffold generation safely
    Invariants: Write operations create parent dirs, operations are idempotent
    """

    def ensure_directory(self, path: Path) -> bool:
        """Ensure a directory exists, creating it and parent directories if needed.

        This operation is idempotent - it succeeds whether the directory already
        exists or needs to be created.

        Args:
            path: Path to the directory to create

        Returns:
            True if the directory was created, False if it already existed
        """
        if path.is_dir():
            return False
        path.mkdir(parents=True, exist_ok=True)
        return True

    def dir_exists(self, path: Path) -> bool:
        """Check if a directory exists.

        Args:
            path: Path to check

        Returns:
            True if path exists and is a directory, False otherwise
        """
        return path.is_dir()

    def write_file(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        """Write content to a file, creating parent directories if needed.

        If the file already exists, it will be overwritten.
        Parent directories are created automatically.

        Args:
            path: Path to the file to write
            content: Content to write to the file
            encoding: Text encoding to use (default: utf-8)
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)

    def file_exists(self, path: Path) -> bool:
        """Check if a file exists.

        Args:
            path: Path to check

        Returns:
            True if path exists and is a file, False otherwise
        """
        return path.is_file()

    def append_file(
        self, path: Path, content: str, encoding: str = "utf-8", separator: str = "\n\n"
    ) -> None:
        """Append content to a file, avoiding duplication.

        This operation is idempotent - if the content (stripped of whitespace)
        is already present in the file, nothing is added.

        If the file doesn't exist, it is created with the content.
        If it exists but doesn't contain the content, the content is appended
        with a separator between the existing content and the new content.

        Args:
            path: Path to the file
            content: Content to append
            encoding: Text encoding to use (default: utf-8)
            separator: Separator to use between existing and new content (default: double newline)

        Example:
            >>> fs = FileSystem()
            >>> fs.append_file(Path("notes.txt"), "First note")
            >>> fs.append_file(Path("notes.txt"), "Second note")
            >>> fs.append_file(Path("notes.txt"), "First note")  # No duplication
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.is_file():
            existing = path.read_text(encoding=encoding)
            # Check if content is already present (idempotent)
            if content.strip() in existing:
                return
            # Append with separator
            updated = existing + separator + content
            path.write_text(updated, encoding=encoding)
        else:
            # Create new file
            path.write_text(content, encoding=encoding)

    def make_executable(self, path: Path) -> None:
        """Add execute permissions to a file.

        This method adds execute permissions while preserving existing permissions.
        Execute permission is added for user, and conditionally for group/other
        based on whether they have read permission.

        Logic:
        - Always add execute for user (S_IXUSR)
        - If group has read, add execute for group (S_IXGRP)
        - If other has read, add execute for other (S_IXOTH)

        If the file doesn't exist, this method returns silently without error.

        Args:
            path: Path to the file to make executable
        """
        if not path.is_file():
            return

        current_mode = path.stat().st_mode
        new_mode = current_mode | stat.S_IXUSR  # Add execute for user

        # Add execute for group if group has read
        if current_mode & stat.S_IRGRP:
            new_mode |= stat.S_IXGRP

        # Add execute for other if other has read
        if current_mode & stat.S_IROTH:
            new_mode |= stat.S_IXOTH

        os.chmod(path, new_mode)

    def read_file(
        self, path: Path, encoding: str = "utf-8", default: Optional[str] = None
    ) -> Optional[str]:
        """Read content from a file.

        If the file doesn't exist, returns the default value instead of raising an error.

        Args:
            path: Path to the file to read
            encoding: Text encoding to use (default: utf-8)
            default: Value to return if file doesn't exist (default: None)

        Returns:
            File content as string, or default value if file doesn't exist
        """
        if not path.is_file():
            return default
        return path.read_text(encoding=encoding)

    def copy_file(self, src: Path, dst: Path) -> None:
        """Copy a file from source to destination, preserving metadata.

        Parent directories of the destination are created automatically.

        Args:
            src: Source file path
            dst: Destination file path
        """
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    def remove_file(self, path: Path) -> bool:
        """Remove a file if it exists.

        Args:
            path: Path to the file to remove

        Returns:
            True if the file was removed, False if it didn't exist
        """
        if path.is_file():
            path.unlink()
            return True
        return False

    def remove_directory(self, path: Path, recursive: bool = False) -> bool:
        """Remove a directory.

        Args:
            path: Path to the directory to remove
            recursive: If True, remove directory and all contents recursively.
                      If False, only remove empty directories.

        Returns:
            True if the directory was removed, False if it didn't exist
        """
        if not path.is_dir():
            return False

        if recursive:
            shutil.rmtree(path)
        else:
            path.rmdir()
        return True
