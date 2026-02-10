#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml", "psycopg2-binary", "claude-agent-sdk>=0.1.18"]
# ///

"""
ADW Ship Iso - AI Developer Workflow for shipping (merging) to main

Usage:
  uv run adw_ship_iso.py <issue-number> <adw-id>

Workflow:
1. Load state and validate worktree exists
2. Validate ALL state fields are populated (not None)
3. Perform manual git merge in main repository:
   - Fetch latest from origin
   - Checkout main
   - Merge feature branch
   - Push to origin/main
4. Post success message to issue

This workflow REQUIRES that all previous workflows have been run and that
every field in ADWState has a value. This is our final approval step.

Note: Merge operations happen in the main repository root, not in the worktree,
to preserve the worktree's state.
"""

import sys
import os
import logging
import json
import subprocess
from typing import Optional, Dict, Any, Tuple
from dotenv import load_dotenv

from adw_modules.state import ADWState
from adw_modules.github import (
    make_issue_comment,
    get_repo_url,
    extract_repo_path,
)
from adw_modules.workflow_ops import format_issue_message
from adw_modules.utils import setup_logger, check_env_vars
from adw_modules.worktree_ops import validate_worktree
from adw_modules.data_types import ADWStateData
from adw_modules.adw_db_bridge import (
    init_bridge, close_bridge,
    track_workflow_start, track_phase_update, track_workflow_end,
    track_agent_start, track_agent_end,
    log_event,
)

# Agent name constant
AGENT_SHIPPER = "shipper"


def get_target_branch() -> str:
    """Get target branch from config.yml, default to 'main'.

    Returns:
        Target branch name (e.g., 'main', 'master', 'develop')
    """
    try:
        import yaml
        config_path = os.path.join(get_main_repo_root(), "config.yml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get("agentic", {}).get("target_branch", "main")
    except Exception:
        return "main"


def get_main_repo_root() -> str:
    """Get the main repository root directory (parent of adws)."""
    # This script is in adws/, so go up one level to get repo root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cleanup_after_merge(adw_id: str, branch_name: str, logger: logging.Logger) -> Tuple[bool, Optional[str]]:
    """Clean up worktree and branches after successful merge.

    Args:
        adw_id: The ADW ID for the worktree
        branch_name: The feature branch to delete
        logger: Logger instance

    Returns:
        Tuple of (success, error_message)
    """
    repo_root = get_main_repo_root()
    errors = []

    # Step 1: Run purge_tree.sh to clean up worktree
    logger.info(f"Cleaning up worktree for {adw_id}...")
    purge_script = os.path.join(repo_root, "scripts", "purge_tree.sh")

    if os.path.exists(purge_script):
        result = subprocess.run(
            ["bash", purge_script, adw_id],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            errors.append(f"purge_tree.sh failed: {result.stderr}")
            logger.warning(f"purge_tree.sh failed: {result.stderr}")
        else:
            logger.info(f"✅ Worktree cleaned up")
    else:
        logger.warning(f"purge_tree.sh not found at {purge_script}")

    # Step 2: Delete remote branch
    logger.info(f"Deleting remote branch: {branch_name}...")
    result = subprocess.run(
        ["git", "push", "origin", "--delete", branch_name],
        capture_output=True, text=True, cwd=repo_root
    )
    if result.returncode != 0:
        # Check if branch doesn't exist (not an error)
        if "remote ref does not exist" in result.stderr:
            logger.info(f"Remote branch already deleted or doesn't exist")
        else:
            errors.append(f"Failed to delete remote branch: {result.stderr}")
            logger.warning(f"Failed to delete remote branch: {result.stderr}")
    else:
        logger.info(f"✅ Remote branch deleted")

    # Step 3: Clean up agents directory
    agents_dir = os.path.join(repo_root, "agents", adw_id)
    if os.path.exists(agents_dir):
        logger.info(f"Cleaning up agents directory: {agents_dir}...")
        try:
            import shutil
            shutil.rmtree(agents_dir)
            logger.info(f"✅ Agents directory cleaned up")
        except Exception as e:
            errors.append(f"Failed to clean agents dir: {e}")
            logger.warning(f"Failed to clean agents directory: {e}")

    if errors:
        return False, "; ".join(errors)
    return True, None


def manual_merge_to_target(branch_name: str, logger: logging.Logger) -> Tuple[bool, Optional[str]]:
    """Manually merge a branch to target branch using git commands.

    This runs in the main repository root, not in a worktree.

    Args:
        branch_name: The feature branch to merge
        logger: Logger instance

    Returns:
        Tuple of (success, error_message)
    """
    repo_root = get_main_repo_root()
    target_branch = get_target_branch()
    logger.info(f"Performing manual merge in main repository: {repo_root}")
    logger.info(f"Target branch: {target_branch}")
    
    try:
        # Save current branch to restore later
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=repo_root
        )
        original_branch = result.stdout.strip()
        logger.debug(f"Original branch: {original_branch}")
        
        # Step 1: Fetch latest from origin
        logger.info("Fetching latest from origin...")
        result = subprocess.run(
            ["git", "fetch", "origin"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to fetch from origin: {result.stderr}"
        
        # Step 2: Checkout target branch
        logger.info(f"Checking out {target_branch} branch...")
        result = subprocess.run(
            ["git", "checkout", target_branch],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            return False, f"Failed to checkout {target_branch}: {result.stderr}"

        # Step 3: Pull latest target branch
        logger.info(f"Pulling latest {target_branch}...")
        result = subprocess.run(
            ["git", "pull", "origin", target_branch],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to pull latest {target_branch}: {result.stderr}"
        
        # Step 4: Merge the feature branch (no-ff to preserve all commits)
        logger.info(f"Merging branch {branch_name} (no-ff to preserve all commits)...")
        result = subprocess.run(
            ["git", "merge", branch_name, "--no-ff", "-m", f"Merge branch '{branch_name}' via ADW Ship workflow"],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to merge {branch_name}: {result.stderr}"
        
        # Step 5: Push to origin/target_branch
        logger.info(f"Pushing to origin/{target_branch}...")
        result = subprocess.run(
            ["git", "push", "origin", target_branch],
            capture_output=True, text=True, cwd=repo_root
        )
        if result.returncode != 0:
            # Try to restore original branch
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
            return False, f"Failed to push to origin/{target_branch}: {result.stderr}"

        # Step 6: Restore original branch
        logger.info(f"Restoring original branch: {original_branch}")
        subprocess.run(["git", "checkout", original_branch], cwd=repo_root)

        logger.info(f"✅ Successfully merged and pushed to {target_branch}!")
        return True, None
        
    except Exception as e:
        logger.error(f"Unexpected error during merge: {e}")
        # Try to restore original branch
        try:
            subprocess.run(["git", "checkout", original_branch], cwd=repo_root)
        except:
            pass
        return False, str(e)


def validate_state_completeness(state: ADWState, logger: logging.Logger) -> tuple[bool, list[str]]:
    """Validate that all fields in ADWState have values (not None).

    Returns:
        tuple of (is_valid, missing_fields)
    """
    # Get the expected fields from ADWStateData model
    expected_fields = {
        "adw_id",
        "issue_number",
        "branch_name",
        "plan_file",
        "issue_class",
        "worktree_path",
    }

    missing_fields = []

    for field in expected_fields:
        value = state.get(field)
        if value is None:
            missing_fields.append(field)
            logger.warning(f"Missing required field: {field}")
        else:
            logger.debug(f"✓ {field}: {value}")

    return len(missing_fields) == 0, missing_fields


def validate_pr_exists(branch_name: str, logger: logging.Logger) -> tuple[bool, Optional[str], Optional[str]]:
    """Validate that PR exists for the branch before attempting merge.

    Returns:
        tuple of (pr_exists, pr_url, error_message)
    """
    try:
        repo_url = get_repo_url()
        repo_path = extract_repo_path(repo_url)
    except Exception as e:
        error_msg = f"Failed to get repo info: {e}"
        logger.error(error_msg)
        return False, None, error_msg

    # Use gh CLI to check if PR exists
    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo", repo_path,
            "--head", branch_name,
            "--json", "number,url,state",
            "--limit", "1",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        error_msg = f"Failed to check PR status: {result.stderr}"
        logger.error(error_msg)
        return False, None, error_msg

    try:
        prs = json.loads(result.stdout)
        if not prs:
            error_msg = f"No PR found for branch '{branch_name}'. The PR must be created in earlier phases."
            logger.error(error_msg)
            return False, None, error_msg

        pr = prs[0]
        pr_state = pr.get("state", "UNKNOWN")
        pr_url = pr.get("url", "")

        # Check if PR is in a valid state (not closed/merged already)
        if pr_state.upper() == "MERGED":
            error_msg = f"PR #{pr.get('number')} is already merged"
            logger.warning(error_msg)
            return True, pr_url, None  # Still return True since PR exists, just log warning

        if pr_state.upper() == "CLOSED":
            error_msg = f"PR #{pr.get('number')} is closed"
            logger.error(error_msg)
            return False, pr_url, error_msg

        logger.info(f"✅ PR found: {pr_url} (state: {pr_state})")
        return True, pr_url, None

    except json.JSONDecodeError as e:
        error_msg = f"Failed to parse PR response: {e}"
        logger.error(error_msg)
        return False, None, error_msg


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Parse command line args
    # INTENTIONAL: adw-id is REQUIRED - we need it to find the worktree and state
    if len(sys.argv) < 3:
        print("Usage: uv run adw_ship_iso.py <issue-number> <adw-id>")
        print("\nError: Both issue-number and adw-id are required")
        print("Run the complete SDLC workflow before shipping")
        sys.exit(1)
    
    issue_number = sys.argv[1]
    adw_id = sys.argv[2]
    
    # Try to load existing state
    temp_logger = setup_logger(adw_id, "adw_ship_iso")
    state = ADWState.load(adw_id, temp_logger)
    if not state:
        # No existing state found
        logger = setup_logger(adw_id, "adw_ship_iso")
        logger.error(f"No state found for ADW ID: {adw_id}")
        logger.error("Run the complete SDLC workflow before shipping")
        print(f"\nError: No state found for ADW ID: {adw_id}")
        print("Run the complete SDLC workflow before shipping")
        sys.exit(1)
    
    # Update issue number from state if available
    issue_number = state.get("issue_number", issue_number)

    # Set up logger with ADW ID
    logger = setup_logger(adw_id, "adw_ship_iso")

    # Check if ship phase already completed
    completed_phases = state.get("all_adws", [])
    if "adw_ship_iso" in completed_phases:
        logger.info("Ship phase already completed - nothing to do")
        print("✓ Ship phase already completed - branch already merged")
        try:
            make_issue_comment(
                issue_number,
                format_issue_message(
                    adw_id,
                    AGENT_SHIPPER,
                    "✓ Ship phase already completed - branch already merged to target"
                )
            )
        except Exception as e:
            logger.warning(f"Failed to post comment: {e}")
        sys.exit(0)

    logger.info(f"ADW Ship Iso starting - ID: {adw_id}, Issue: {issue_number}")

    # Initialize DB bridge for orchestrator dashboard tracking
    init_bridge()
    track_workflow_start(adw_id, "ship", issue_number, total_steps=1)
    track_phase_update(adw_id, "merge", "in_progress", 0)

    # Track that this ADW workflow has run
    state.append_adw_id("adw_ship_iso")
    
    # Validate environment
    check_env_vars(logger)
    
    # Post initial status
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, "ops", f"🚢 Starting ship workflow\n"
                           f"📋 Validating state completeness...")
    )
    
    # Step 1: Validate state completeness
    logger.info("Validating state completeness...")
    is_valid, missing_fields = validate_state_completeness(state, logger)
    
    if not is_valid:
        error_msg = f"State validation failed. Missing fields: {', '.join(missing_fields)}"
        logger.error(error_msg)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER, f"❌ {error_msg}\n\n"
                               "Please ensure all workflows have been run:\n"
                               "- adw_plan_iso.py (creates plan_file, branch_name, issue_class)\n"
                               "- adw_build_iso.py (implements the plan)\n" 
                               "- adw_test_iso.py (runs tests)\n"
                               "- adw_review_iso.py (reviews implementation)\n"
                               "- adw_document_iso.py (generates docs)")
        )
        sys.exit(1)
    
    logger.info("✅ State validation passed - all fields have values")

    # Step 2: Validate worktree exists
    valid, error = validate_worktree(adw_id, state)
    if not valid:
        logger.error(f"Worktree validation failed: {error}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER, f"❌ Worktree validation failed: {error}")
        )
        sys.exit(1)

    worktree_path = state.get("worktree_path")
    logger.info(f"✅ Worktree validated at: {worktree_path}")

    # Step 3: Get branch name
    branch_name = state.get("branch_name")
    logger.info(f"Preparing to merge branch: {branch_name}")

    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER, f"📋 State validation complete\n"
                           f"🔍 Preparing to merge branch: {branch_name}")
    )

    # Step 3.5: Validate PR exists before attempting merge (NEW - CRITICAL)
    logger.info(f"Validating that PR exists for branch: {branch_name}...")
    pr_exists, pr_url, pr_error = validate_pr_exists(branch_name, logger)

    if not pr_exists:
        error_msg = pr_error or "Unknown error validating PR"
        logger.error(f"PR validation failed: {error_msg}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER,
                               f"❌ **Cannot ship: PR not found**\n\n"
                               f"Error: {error_msg}\n\n"
                               f"The PR should have been created in earlier phases:\n"
                               f"- adw_plan_iso.py (creates PR)\n"
                               f"- adw_build_iso.py, adw_test_iso.py, adw_review_iso.py, adw_document_iso.py (update PR)\n\n"
                               f"**Solution**: Please verify that:\n"
                               f"1. Branch `{branch_name}` exists and is pushed to origin\n"
                               f"2. No network/auth issues preventing PR creation\n"
                               f"3. If PR was accidentally deleted, recreate it manually with `gh pr create`")
        )
        track_phase_update(adw_id, "merge", "failed", 0)
        track_workflow_end(adw_id, "failed", error_msg)
        close_bridge()
        sys.exit(1)

    logger.info(f"✅ PR validation passed: {pr_url}")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER, f"✅ PR validation passed\n"
                           f"📋 PR: {pr_url}")
    )
    
    # Step 4: Perform manual merge
    target_branch = get_target_branch()
    logger.info(f"Starting manual merge of {branch_name} to {target_branch}...")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER, f"🔀 Merging {branch_name} to {target_branch}...\n"
                           "Using manual git operations in main repository")
    )

    agent_id = track_agent_start(adw_id, "adw_ship_iso", model="claude-sonnet-4-5-20250929")
    log_event("adw_ship_iso", f"Ship merge started for {adw_id}")

    success, error = manual_merge_to_target(branch_name, logger)

    if not success:
        logger.error(f"Failed to merge: {error}")
        track_agent_end(agent_id, "failed")
        log_event("adw_ship_iso", f"Ship merge failed for {adw_id}", level="ERROR")
        track_phase_update(adw_id, "merge", "failed", 0)
        track_workflow_end(adw_id, "failed", error)
        close_bridge()
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_SHIPPER, f"❌ Failed to merge: {error}")
        )
        sys.exit(1)
    
    logger.info(f"✅ Successfully merged {branch_name} to {target_branch}")

    # Step 5: Cleanup after successful merge
    logger.info("Starting post-merge cleanup...")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER, "🧹 Starting post-merge cleanup...")
    )

    cleanup_success, cleanup_error = cleanup_after_merge(adw_id, branch_name, logger)

    if cleanup_success:
        cleanup_status = "✅ Worktree, branches, and agents cleaned up"
    else:
        cleanup_status = f"⚠️ Cleanup completed with warnings: {cleanup_error}"
        logger.warning(f"Cleanup warnings: {cleanup_error}")

    # Step 6: Post success message
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_SHIPPER,
                           f"🎉 **Successfully shipped!**\n\n"
                           f"✅ Validated all state fields\n"
                           f"✅ Merged branch `{branch_name}` to {target_branch}\n"
                           f"✅ Pushed to origin/{target_branch}\n"
                           f"{cleanup_status}\n\n"
                           f"🚢 Code has been deployed to production!")
    )

    # Save final state before cleanup (for reference)
    state.save("adw_ship_iso")

    # Track successful completion in orchestrator DB
    track_phase_update(adw_id, "merge", "completed", 1)
    track_workflow_end(adw_id, "completed")
    track_agent_end(agent_id, "completed")
    log_event("adw_ship_iso", f"Ship workflow completed for {adw_id}")
    close_bridge()

    # Post final state summary
    make_issue_comment(
        issue_number,
        f"{adw_id}_ops: 📋 Final ship state:\n```json\n{json.dumps(state.data, indent=2)}\n```"
    )

    logger.info("Ship workflow completed successfully")


if __name__ == "__main__":
    main()