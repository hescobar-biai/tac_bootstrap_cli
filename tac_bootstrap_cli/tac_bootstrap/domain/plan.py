"""Scaffolding plan models.

These models represent the plan of operations to execute when scaffolding
a project. The plan is built first, then can be previewed or executed.
"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class FileAction(str, Enum):
    """Type of file operation to perform."""
    CREATE = "create"    # Create new file (skip if exists)
    OVERWRITE = "overwrite"  # Create or overwrite existing
    PATCH = "patch"      # Append to existing file
    SKIP = "skip"        # Skip this file


class FileOperation(BaseModel):
    """Single file operation in the scaffold plan.

    Represents one file to be created, modified, or skipped.
    """
    path: str = Field(..., description="Relative path from project root")
    action: FileAction = Field(..., description="Type of operation")
    template: Optional[str] = Field(None, description="Jinja2 template name to render")
    content: Optional[str] = Field(None, description="Static content (if no template)")
    reason: Optional[str] = Field(None, description="Why this file is needed")
    executable: bool = Field(False, description="Make file executable after creation")

    def __str__(self) -> str:
        return f"[{self.action.value}] {self.path}"


class DirectoryOperation(BaseModel):
    """Directory creation operation.

    Represents a directory to be created.
    """
    path: str = Field(..., description="Relative path from project root")
    reason: str = Field("", description="Purpose of this directory")

    def __str__(self) -> str:
        return f"[mkdir] {self.path}/"


class ScaffoldPlan(BaseModel):
    """Complete scaffold plan for generation.

    Contains all directories and files to be created/modified.
    The plan is built first, allowing preview and validation before execution.

    Example:
        ```python
        plan = scaffold_service.build_plan(config)

        # Preview what will be created
        for dir_op in plan.directories:
            print(f"Will create: {dir_op.path}/")

        for file_op in plan.get_files_to_create():
            print(f"Will create: {file_op.path}")

        # Execute the plan
        scaffold_service.apply_plan(plan, output_dir)
        ```
    """
    directories: List[DirectoryOperation] = Field(default_factory=list)
    files: List[FileOperation] = Field(default_factory=list)

    def get_files_to_create(self) -> List[FileOperation]:
        """Get files that will be created (new files only)."""
        return [f for f in self.files if f.action == FileAction.CREATE]

    def get_files_to_overwrite(self) -> List[FileOperation]:
        """Get files that will be overwritten."""
        return [f for f in self.files if f.action == FileAction.OVERWRITE]

    def get_files_to_patch(self) -> List[FileOperation]:
        """Get files that will be patched (appended to)."""
        return [f for f in self.files if f.action == FileAction.PATCH]

    def get_files_skipped(self) -> List[FileOperation]:
        """Get files that will be skipped."""
        return [f for f in self.files if f.action == FileAction.SKIP]

    def get_executable_files(self) -> List[FileOperation]:
        """Get files that need to be made executable."""
        return [f for f in self.files if f.executable]

    @property
    def total_directories(self) -> int:
        """Total number of directories to create."""
        return len(self.directories)

    @property
    def total_files(self) -> int:
        """Total number of file operations."""
        return len(self.files)

    @property
    def summary(self) -> str:
        """Get a summary of the plan."""
        creates = len(self.get_files_to_create())
        patches = len(self.get_files_to_patch())
        skips = len(self.get_files_skipped())
        return (
            f"Plan: {self.total_directories} directories, "
            f"{creates} files to create, {patches} to patch, {skips} skipped"
        )

    def add_directory(self, path: str, reason: str = "") -> "ScaffoldPlan":
        """Add a directory to the plan (fluent interface)."""
        self.directories.append(DirectoryOperation(path=path, reason=reason))
        return self

    def add_file(
        self,
        path: str,
        action: FileAction = FileAction.CREATE,
        template: Optional[str] = None,
        content: Optional[str] = None,
        reason: Optional[str] = None,
        executable: bool = False,
    ) -> "ScaffoldPlan":
        """Add a file operation to the plan (fluent interface)."""
        self.files.append(FileOperation(
            path=path,
            action=action,
            template=template,
            content=content,
            reason=reason,
            executable=executable,
        ))
        return self
