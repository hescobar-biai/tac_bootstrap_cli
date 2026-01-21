"""Git operations adapter for TAC Bootstrap.

This module provides a clean abstraction layer for common Git operations used
during project scaffolding and AI Developer Workflows (ADWs). It encapsulates
subprocess calls to git commands and provides structured results.

Example:
    >>> from pathlib import Path
    >>> adapter = GitAdapter(Path("my_project"))
    >>> result = adapter.init()
    >>> if result.success:
    ...     adapter.add_all()
    ...     adapter.commit("Initial commit")
"""

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class GitResult:
    """Structured result from a Git operation.

    Attributes:
        success: Whether the git command succeeded (exit code 0)
        output: Standard output from the command
        error: Error message if the command failed
    """

    success: bool
    output: str = ""
    error: str = ""


class GitAdapter:
    """Adapter for Git operations during scaffolding and workflows.

    This class provides a clean interface to common git operations without
    requiring direct subprocess management. All operations return GitResult
    for consistent error handling.

    Example:
        >>> adapter = GitAdapter(Path("my_project"))
        >>> result = adapter.init()
        >>> adapter.add_all()
        >>> adapter.commit("Initial commit")
    """

    def __init__(self, repo_path: Path):
        """Initialize the GitAdapter.

        Args:
            repo_path: Path to the git repository (or where it will be created)
        """
        self.repo_path = repo_path

    def _run(self, *args: str, check: bool = True) -> GitResult:
        """Execute a git command and return structured result.

        Args:
            *args: Git command arguments (e.g., "init", "-b", "main")
            check: If False, don't raise on non-zero exit codes

        Returns:
            GitResult with success status, output, and error message
        """
        try:
            result = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=check,
            )
            return GitResult(
                success=result.returncode == 0,
                output=result.stdout.strip(),
                error=result.stderr.strip(),
            )
        except subprocess.CalledProcessError as e:
            return GitResult(
                success=False,
                output=e.stdout.strip() if e.stdout else "",
                error=e.stderr.strip() if e.stderr else str(e),
            )
        except FileNotFoundError:
            return GitResult(success=False, error="Git is not installed or not in PATH")

    def is_repo(self) -> bool:
        """Check if the current path is a git repository.

        Returns:
            True if .git directory exists, False otherwise
        """
        return (self.repo_path / ".git").exists()

    def init(self, initial_branch: str = "main") -> GitResult:
        """Initialize a new git repository.

        Args:
            initial_branch: Name of the initial branch (default: "main")

        Returns:
            GitResult indicating success or failure
        """
        return self._run("init", "-b", initial_branch)

    def add(self, *paths: str) -> GitResult:
        """Stage specific files for commit.

        Args:
            *paths: File paths to stage (relative to repo root)

        Returns:
            GitResult indicating success or failure
        """
        return self._run("add", *paths)

    def add_all(self) -> GitResult:
        """Stage all changes (tracked and untracked files).

        Returns:
            GitResult indicating success or failure
        """
        return self._run("add", "-A")

    def commit(self, message: str, allow_empty: bool = False) -> GitResult:
        """Create a commit with the staged changes.

        Args:
            message: Commit message
            allow_empty: Allow commit with no changes (default: False)

        Returns:
            GitResult indicating success or failure
        """
        args = ["commit", "-m", message]
        if allow_empty:
            args.append("--allow-empty")
        return self._run(*args)

    def status(self, porcelain: bool = True) -> GitResult:
        """Get repository status.

        Args:
            porcelain: Use machine-readable format (default: True)

        Returns:
            GitResult with status output
        """
        args = ["status"]
        if porcelain:
            args.append("--porcelain")
        return self._run(*args)

    def has_changes(self) -> bool:
        """Check if there are uncommitted changes.

        Returns:
            True if there are uncommitted changes, False otherwise
        """
        result = self.status()
        return result.success and bool(result.output)

    def get_current_branch(self) -> Optional[str]:
        """Get the name of the current branch.

        Returns:
            Branch name, or None if not in a repository or detached HEAD
        """
        result = self._run("branch", "--show-current", check=False)
        return result.output if result.success and result.output else None

    def branch_exists(self, branch: str) -> bool:
        """Check if a branch exists.

        Args:
            branch: Branch name to check

        Returns:
            True if branch exists, False otherwise
        """
        result = self._run("rev-parse", "--verify", branch, check=False)
        return result.success

    def checkout(self, branch: str, create: bool = False) -> GitResult:
        """Checkout a branch.

        Args:
            branch: Branch name to checkout
            create: Create the branch if it doesn't exist (default: False)

        Returns:
            GitResult indicating success or failure
        """
        args = ["checkout"]
        if create:
            args.append("-b")
        args.append(branch)
        return self._run(*args)

    def create_worktree(self, path: Path, branch: str, create_branch: bool = True) -> GitResult:
        """Create a new worktree.

        Args:
            path: Path where the worktree will be created
            branch: Branch name for the worktree
            create_branch: Create a new branch (default: True)

        Returns:
            GitResult indicating success or failure
        """
        args = ["worktree", "add", str(path)]
        if create_branch:
            args.extend(["-b", branch])
        else:
            args.append(branch)
        return self._run(*args)

    def remove_worktree(self, path: Path, force: bool = False) -> GitResult:
        """Remove a worktree.

        Args:
            path: Path to the worktree to remove
            force: Force removal even with uncommitted changes (default: False)

        Returns:
            GitResult indicating success or failure
        """
        args = ["worktree", "remove", str(path)]
        if force:
            args.append("--force")
        return self._run(*args)

    def list_worktrees(self) -> List[str]:
        """List all worktrees in the repository.

        Returns:
            List of worktree paths
        """
        result = self._run("worktree", "list", "--porcelain", check=False)
        if not result.success:
            return []

        worktrees = []
        for line in result.output.split("\n"):
            if line.startswith("worktree "):
                worktrees.append(line.split("worktree ", 1)[1])
        return worktrees

    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get the URL of a remote.

        Args:
            remote: Name of the remote (default: "origin")

        Returns:
            Remote URL, or None if remote doesn't exist
        """
        result = self._run("remote", "get-url", remote, check=False)
        return result.output if result.success and result.output else None
