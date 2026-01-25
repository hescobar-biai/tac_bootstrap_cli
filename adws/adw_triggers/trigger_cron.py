#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "schedule",
#     "python-dotenv",
#     "pydantic",
# ]
# ///

"""
Cron-based ADW trigger system for TAC Bootstrap.

Polls GitHub at a configurable interval to detect issues or comments
containing ADW workflow commands (e.g., adw_plan_iso, adw_sdlc_iso, etc.).

When a qualifying issue/comment is found, it triggers the corresponding workflow
using the same detection logic as the webhook trigger.

Usage:
    uv run trigger_cron.py                    # Default 20s interval
    uv run trigger_cron.py --interval 30      # Custom 30s interval
    uv run trigger_cron.py -i 60              # Custom 60s interval
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Optional, Set

import schedule
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adw_modules.github import (
    ADW_BOT_IDENTIFIER,
    assign_issue_to_me,
    extract_repo_path,
    fetch_issue_comments,
    fetch_open_issues,
    get_current_gh_user,
    get_repo_url,
    is_issue_assigned_to_me,
    make_issue_comment,
)
from adw_modules.state import ADWState
from adw_modules.utils import get_safe_subprocess_env, make_adw_id, setup_logger
from adw_modules.workflow_ops import AVAILABLE_ADW_WORKFLOWS, extract_adw_info

# Load environment variables from current or parent directories
load_dotenv()

# Default polling interval
DEFAULT_INTERVAL = 20

# Get repository URL from git remote
try:
    GITHUB_REPO_URL = get_repo_url()
    REPO_PATH = extract_repo_path(GITHUB_REPO_URL)
except ValueError as e:
    print(f"ERROR: {e}")
    sys.exit(1)

# Dependent workflows that require existing worktrees
DEPENDENT_WORKFLOWS = [
    "adw_build_iso",
    "adw_test_iso",
    "adw_review_iso",
    "adw_document_iso",
    "adw_ship_iso",
]

# Track issues with their last processed comment ID
issue_last_comment: Dict[int, Optional[int]] = {}
# Track issues that have been processed (no comments case)
processed_new_issues: Set[int] = set()

# Graceful shutdown flag
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    print(f"\nINFO: Received signal {signum}, initiating graceful shutdown...")
    shutdown_requested = True


def check_issue_for_workflow(issue_number: int) -> Optional[Dict]:
    """Check if an issue has a new workflow trigger in its body or latest comment.

    Returns a dict with workflow info if a trigger is found, None otherwise.
    """
    comments = fetch_issue_comments(REPO_PATH, issue_number)

    if not comments:
        # New issue with no comments - check the issue body
        if issue_number in processed_new_issues:
            return None

        # Fetch issue body via gh CLI
        try:
            result = subprocess.run(
                ["gh", "issue", "view", str(issue_number), "--repo", REPO_PATH, "--json", "body"],
                capture_output=True,
                text=True,
                env=get_safe_subprocess_env(),
            )
            if result.returncode == 0:
                import json
                issue_data = json.loads(result.stdout)
                issue_body = issue_data.get("body", "")

                # Skip ADW bot issues to prevent loops
                if ADW_BOT_IDENTIFIER in issue_body:
                    return None

                # Check if body contains adw workflow trigger
                if "adw_" in issue_body.lower():
                    temp_id = make_adw_id()
                    extraction = extract_adw_info(issue_body, temp_id)
                    if extraction.has_workflow:
                        processed_new_issues.add(issue_number)
                        return {
                            "workflow": extraction.workflow_command,
                            "adw_id": extraction.adw_id,
                            "model_set": extraction.model_set,
                            "trigger_reason": f"New issue with {extraction.workflow_command} workflow",
                        }
        except Exception as e:
            print(f"ERROR: Failed to fetch issue #{issue_number} body: {e}")
        return None

    # Has comments - check the latest one
    latest_comment = comments[-1]
    comment_body = latest_comment.get("body", "")
    comment_id = latest_comment.get("id")

    # Check if we've already processed this comment
    last_processed = issue_last_comment.get(issue_number)
    if last_processed == comment_id:
        return None

    # Skip ADW bot comments to prevent loops
    if ADW_BOT_IDENTIFIER in comment_body:
        issue_last_comment[issue_number] = comment_id
        return None

    # Check if comment contains adw workflow trigger
    if "adw_" in comment_body.lower():
        temp_id = make_adw_id()
        extraction = extract_adw_info(comment_body, temp_id)
        if extraction.has_workflow:
            issue_last_comment[issue_number] = comment_id
            return {
                "workflow": extraction.workflow_command,
                "adw_id": extraction.adw_id,
                "model_set": extraction.model_set,
                "trigger_reason": f"Comment with {extraction.workflow_command} workflow",
            }

    # Update last processed comment even if no workflow found
    issue_last_comment[issue_number] = comment_id
    return None


def trigger_workflow(issue_number: int, workflow_info: Dict) -> bool:
    """Trigger an ADW workflow for a specific issue."""
    workflow = workflow_info["workflow"]
    provided_adw_id = workflow_info.get("adw_id")
    model_set = workflow_info.get("model_set")
    trigger_reason = workflow_info.get("trigger_reason", "")

    # Validate dependent workflows
    if workflow in DEPENDENT_WORKFLOWS:
        if not provided_adw_id:
            print(f"ERROR: {workflow} is a dependent workflow that requires an existing ADW ID")
            try:
                make_issue_comment(
                    str(issue_number),
                    f"❌ Error: `{workflow}` is a dependent workflow that requires an existing ADW ID.\n\n"
                    f"To run this workflow, provide the ADW ID in your comment, for example:\n"
                    f"`{workflow} adw-12345678`\n\n"
                    f"The ADW ID should come from a previous workflow run (like `adw_plan_iso` or `adw_patch_iso`).",
                )
            except Exception as e:
                print(f"WARNING: Failed to post error comment: {e}")
            return False

    # Use provided ADW ID or generate a new one
    adw_id = provided_adw_id or make_adw_id()

    # Manage ADW state
    if provided_adw_id:
        state = ADWState.load(provided_adw_id)
        if state:
            state.update(issue_number=str(issue_number), model_set=model_set)
        else:
            state = ADWState(provided_adw_id)
            state.update(adw_id=provided_adw_id, issue_number=str(issue_number), model_set=model_set)
        state.save("cron_trigger")
    else:
        state = ADWState(adw_id)
        state.update(adw_id=adw_id, issue_number=str(issue_number), model_set=model_set)
        state.save("cron_trigger")

    # Set up logger
    logger = setup_logger(adw_id, "cron_trigger")
    logger.info(f"Triggering {workflow} for issue #{issue_number} (reason: {trigger_reason})")

    # Assign issue to current user
    try:
        assign_issue_to_me(str(issue_number))
    except Exception as e:
        logger.warning(f"Failed to assign issue: {e}")

    # Post comment to issue
    try:
        make_issue_comment(
            str(issue_number),
            f"🤖 ADW Cron: Detected `{workflow}` workflow request\n\n"
            f"Starting workflow with ID: `{adw_id}`\n"
            f"Workflow: `{workflow}` 🏗️\n"
            f"Model Set: `{model_set}` ⚙️\n"
            f"Reason: {trigger_reason}\n\n"
            f"Logs will be available at: `agents/{adw_id}/{workflow}/`",
        )
    except Exception as e:
        logger.warning(f"Failed to post issue comment: {e}")

    # Build and run the workflow command
    try:
        adws_dir = Path(__file__).parent.parent
        repo_root = adws_dir.parent
        trigger_script = adws_dir / f"{workflow}.py"

        cmd = ["uv", "run", str(trigger_script), str(issue_number), adw_id]

        print(f"INFO: Launching {workflow} for issue #{issue_number}")
        print(f"INFO: Command: {' '.join(cmd)}")
        print(f"INFO: Working directory: {repo_root}")

        # Launch in background
        process = subprocess.Popen(
            cmd,
            cwd=str(repo_root),
            env=get_safe_subprocess_env(),
            start_new_session=True,
        )

        print(f"INFO: Background process started (PID: {process.pid}) for issue #{issue_number} with ADW ID: {adw_id}")
        logger.info(f"Background process started (PID: {process.pid})")
        return True

    except Exception as e:
        print(f"ERROR: Exception while triggering workflow for issue #{issue_number}: {e}")
        logger.error(f"Exception: {e}")
        return False


def check_and_process_issues():
    """Main function that checks for issues and processes qualifying ones."""
    if shutdown_requested:
        return

    start_time = time.time()
    print(f"INFO: Starting issue check cycle")

    try:
        # Fetch all open issues
        issues = fetch_open_issues(REPO_PATH)

        if not issues:
            print(f"INFO: No open issues found")
            return

        triggered_count = 0

        for issue in issues:
            if shutdown_requested:
                print(f"INFO: Shutdown requested, stopping issue processing")
                break

            issue_number = issue.number
            if not issue_number:
                continue

            # Check if issue is assigned to current user
            if not is_issue_assigned_to_me(str(issue_number), REPO_PATH):
                continue

            # Check if issue has a workflow trigger
            workflow_info = check_issue_for_workflow(issue_number)
            if workflow_info:
                if trigger_workflow(issue_number, workflow_info):
                    triggered_count += 1

        cycle_time = time.time() - start_time
        if triggered_count > 0:
            print(f"INFO: Triggered {triggered_count} workflow(s) in {cycle_time:.2f}s")
        else:
            print(f"INFO: No new triggers found ({cycle_time:.2f}s)")

    except Exception as e:
        print(f"ERROR: Error during check cycle: {e}")
        import traceback
        traceback.print_exc()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Cron-based ADW trigger for TAC Bootstrap.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    uv run trigger_cron.py                    # Default interval
    uv run trigger_cron.py --interval 30      # Poll every 30 seconds
    uv run trigger_cron.py -i 60              # Poll every 60 seconds

Supported workflows:
"""
        + "\n".join(f"    - {w}" for w in AVAILABLE_ADW_WORKFLOWS),
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})",
    )
    return parser.parse_args()


def main():
    """Main entry point for the cron trigger."""
    args = parse_args()
    interval = args.interval

    current_user = get_current_gh_user()
    print(f"INFO: Starting ADW cron trigger for TAC Bootstrap")
    print(f"INFO: Repository: {REPO_PATH}")
    print(f"INFO: Current user: {current_user or 'unknown'}")
    print(f"INFO: Only processing issues assigned to current user")
    print(f"INFO: Polling interval: {interval} seconds")
    print(f"INFO: Supported workflows: {len(AVAILABLE_ADW_WORKFLOWS)}")

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Schedule the check function
    schedule.every(interval).seconds.do(check_and_process_issues)

    # Run initial check immediately
    check_and_process_issues()

    # Main loop
    print(f"INFO: Entering main scheduling loop")
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)

    print(f"INFO: Shutdown complete")


if __name__ == "__main__":
    main()
