"""Git operations for ADW composable architecture.

Provides centralized git operations that build on top of github.py module.
"""

import subprocess
import json
import logging
from typing import Optional, Tuple

# Import GitHub functions from existing module
from adw_modules.github import get_repo_url, extract_repo_path, make_issue_comment
from adw_modules.utils import get_target_branch


def get_current_branch(cwd: Optional[str] = None) -> str:
    """Get current git branch name."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout.strip()


def push_branch(
    branch_name: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Push current branch to remote. Returns (success, error_message)."""
    result = subprocess.run(
        ["git", "push", "-u", "origin", branch_name],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def check_pr_exists(branch_name: str) -> Optional[str]:
    """Check if PR exists for branch. Returns PR URL if exists."""
    # Use github.py functions to get repo info
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None

    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo_path,
            "--head",
            branch_name,
            "--json",
            "url",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        prs = json.loads(result.stdout)
        if prs:
            return prs[0]["url"]
    return None


def create_branch(
    branch_name: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Create and checkout a new branch. Returns (success, error_message)."""
    # Create branch
    result = subprocess.run(
        ["git", "checkout", "-b", branch_name], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        # Check if error is because branch already exists
        if "already exists" in result.stderr:
            # Try to checkout existing branch
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if result.returncode != 0:
                return False, result.stderr
            return True, None
        return False, result.stderr
    return True, None


def commit_changes(
    message: str, cwd: Optional[str] = None
) -> Tuple[bool, Optional[str]]:
    """Stage all changes and commit. Returns (success, error_message)."""
    # Check if there are changes to commit
    result = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True, cwd=cwd
    )
    if not result.stdout.strip():
        return True, None  # No changes to commit

    # Stage all changes
    result = subprocess.run(
        ["git", "add", "-A"], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        return False, result.stderr

    # Commit
    result = subprocess.run(
        ["git", "commit", "-m", message], capture_output=True, text=True, cwd=cwd
    )
    if result.returncode != 0:
        return False, result.stderr
    return True, None


def get_pr_number(branch_name: str) -> Optional[str]:
    """Get PR number for a branch. Returns PR number if exists."""
    # Use github.py functions to get repo info
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None

    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo_path,
            "--head",
            branch_name,
            "--json",
            "number",
            "--limit",
            "1",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        prs = json.loads(result.stdout)
        if prs:
            return str(prs[0]["number"])
    return None


def approve_pr(pr_number: str, logger: logging.Logger) -> Tuple[bool, Optional[str]]:
    """Approve a PR. Returns (success, error_message)."""
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return False, f"Failed to get repo info: {e}"

    result = subprocess.run(
        [
            "gh",
            "pr",
            "review",
            pr_number,
            "--repo",
            repo_path,
            "--approve",
            "--body",
            "ADW Ship workflow approved this PR after validating all state fields.",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, result.stderr

    logger.info(f"Approved PR #{pr_number}")
    return True, None


def merge_pr(
    pr_number: str, logger: logging.Logger, merge_method: str = "squash"
) -> Tuple[bool, Optional[str]]:
    """Merge a PR. Returns (success, error_message).

    Args:
        pr_number: The PR number to merge
        logger: Logger instance
        merge_method: One of 'merge', 'squash', 'rebase' (default: 'squash')
    """
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return False, f"Failed to get repo info: {e}"

    # First check if PR is mergeable
    result = subprocess.run(
        [
            "gh",
            "pr",
            "view",
            pr_number,
            "--repo",
            repo_path,
            "--json",
            "mergeable,mergeStateStatus",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False, f"Failed to check PR status: {result.stderr}"

    pr_status = json.loads(result.stdout)
    if pr_status.get("mergeable") != "MERGEABLE":
        return (
            False,
            f"PR is not mergeable. Status: {pr_status.get('mergeStateStatus', 'unknown')}",
        )

    # Merge the PR
    merge_cmd = [
        "gh",
        "pr",
        "merge",
        pr_number,
        "--repo",
        repo_path,
        f"--{merge_method}",
    ]

    # Add auto-merge body
    merge_cmd.extend(
        ["--body", "Merged by ADW Ship workflow after successful validation."]
    )

    result = subprocess.run(merge_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr

    logger.info(f"Merged PR #{pr_number} using {merge_method} method")
    return True, None


def create_pr_direct(
    branch_name: str,
    issue_title: str,
    issue_number: str,
    logger: logging.Logger,
) -> Tuple[Optional[str], Optional[str]]:
    """Create PR directly using gh CLI in bash. Returns (pr_url, error_message).

    This approach is more reliable than using execute_template because:
    - Direct bash execution, no subprocess context issues
    - Simple gh pr create command
    - Direct error handling
    """
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        return None, f"Failed to get repo info: {e}"

    target_branch = get_target_branch()

    # Build PR title
    pr_title = f"[ADW] #{issue_number} - {issue_title}"[:100]  # GitHub has 100 char limit

    # Build PR body
    pr_body = f"Implements issue #{issue_number}\n\nAutomatically created by TAC ADW workflow."

    # Create PR using gh CLI
    cmd = [
        "gh",
        "pr",
        "create",
        "--repo", repo_path,
        "--title", pr_title,
        "--body", pr_body,
        "--base", target_branch,
        "--head", branch_name,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        error_msg = result.stderr or result.stdout
        logger.error(f"Failed to create PR: {error_msg}")
        return None, error_msg

    pr_url = result.stdout.strip()
    logger.info(f"Successfully created PR: {pr_url}")
    return pr_url, None


def finalize_git_operations(
    state: "ADWState", logger: logging.Logger, cwd: Optional[str] = None
) -> None:
    """Standard git finalization: push branch and create/update PR.

    IMPROVED VERSION:
    - Creates PR directly using gh CLI (more reliable)
    - Saves PR URL to state for later use (especially important for ship phase)
    - Better error handling and logging
    """
    target_branch = get_target_branch()
    branch_name = state.get("branch_name")
    if not branch_name:
        # Fallback: use current git branch if not target branch
        current_branch = get_current_branch(cwd=cwd)
        if current_branch and current_branch != target_branch:
            logger.warning(
                f"No branch name in state, using current branch: {current_branch}"
            )
            branch_name = current_branch
        else:
            logger.error(
                f"No branch name in state and current branch is {target_branch}, skipping git operations"
            )
            return

    # Always push
    success, error = push_branch(branch_name, cwd=cwd)
    if not success:
        logger.error(f"Failed to push branch: {error}")
        return

    logger.info(f"Pushed branch: {branch_name}")

    # Handle PR
    pr_url = check_pr_exists(branch_name)
    issue_number = state.get("issue_number")
    issue_title = state.get("issue_title", "Issue")
    adw_id = state.get("adw_id")

    if pr_url:
        logger.info(f"Found existing PR: {pr_url}")
        # Store PR URL in state for later use (important for ship phase)
        state.update(pr_url=pr_url)
        state.save("finalize_git_operations")
        # Post PR link for easy reference
        if issue_number and adw_id:
            make_issue_comment(issue_number, f"{adw_id}_ops: ✅ Pull request: {pr_url}")
    else:
        # Create new PR directly using gh CLI (no execute_template)
        if issue_number:
            pr_url, error = create_pr_direct(branch_name, issue_title, issue_number, logger)

            if pr_url:
                # Store PR URL in state for later use (important for ship phase)
                state.update(pr_url=pr_url)
                state.save("finalize_git_operations")
                logger.info(f"Created PR: {pr_url}")
                # Post new PR link
                if adw_id:
                    make_issue_comment(
                        issue_number, f"{adw_id}_ops: ✅ Pull request created: {pr_url}"
                    )
            else:
                logger.error(f"Failed to create PR: {error}")
                # Post error to issue
                if adw_id:
                    try:
                        make_issue_comment(
                            issue_number,
                            f"{adw_id}_ops: ⚠️ Failed to create PR: {error}\n\nPlease create PR manually or restart the workflow."
                        )
                    except:
                        pass
        else:
            logger.error("No issue number in state, cannot create PR")
