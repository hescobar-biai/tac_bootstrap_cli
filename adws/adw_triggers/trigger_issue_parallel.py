#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "schedule",
#     "python-dotenv",
#     "pydantic",
#     "pyyaml",
# ]
# ///

"""
Parallel ADW trigger system that processes multiple issues simultaneously.

Unlike trigger_issue_chain.py which processes issues sequentially (waiting for
each to close before starting the next), this trigger processes ALL open issues
in parallel, launching workflows concurrently.

Usage:
    uv run trigger_issue_parallel.py 123 456 789
    uv run trigger_issue_parallel.py --issues 123,456,789
    uv run trigger_issue_parallel.py --issues 123,456,789 --max-concurrent 3
    uv run trigger_issue_parallel.py --issues 123,456,789 --interval 30
    uv run trigger_issue_parallel.py --issues 123,456,789 --once
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Dict, List, Optional, Set, Tuple

import schedule
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from adw_modules.github import (
    ADW_BOT_IDENTIFIER,
    assign_issue_to_me,
    extract_repo_path,
    fetch_issue,
    fetch_issue_comments,
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

# Thread-safe tracking structures
issue_last_comment: Dict[int, Optional[int]] = {}
processed_new_issues: Set[int] = set()
active_workflows: Dict[int, str] = {}  # issue_number -> adw_id
tracking_lock = Lock()

# Graceful shutdown flag
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    print(f"\nINFO: Received signal {signum}, initiating graceful shutdown...")
    shutdown_requested = True


def parse_issue_list(raw_value: str) -> List[int]:
    """Parse a comma-separated list of issue numbers."""
    issues: List[int] = []
    for item in raw_value.split(","):
        value = item.strip()
        if not value:
            continue
        if not value.isdigit():
            raise argparse.ArgumentTypeError(f"Invalid issue number: {value}")
        issues.append(int(value))
    return issues


def parse_positional_issues(values: List[str]) -> List[int]:
    """Parse positional arguments that may be comma-separated or space-separated."""
    issues: List[int] = []
    for value in values:
        # Handle comma-separated values in a single argument
        if "," in value:
            for item in value.split(","):
                item = item.strip()
                if item and item.isdigit():
                    issues.append(int(item))
        elif value.isdigit():
            issues.append(int(value))
    return issues


def resolve_issue_list(args: argparse.Namespace) -> List[int]:
    """Build the list of issues from CLI arguments."""
    issue_list: List[int] = []
    if args.issues_csv:
        issue_list.extend(args.issues_csv)
    if args.issues:
        # Parse positional args that may contain comma-separated values
        issue_list.extend(parse_positional_issues(args.issues))

    if not issue_list:
        raise argparse.ArgumentTypeError("Provide at least one issue number.")

    # Remove duplicates while preserving order
    seen = set()
    unique_issues = []
    for issue in issue_list:
        if issue not in seen:
            seen.add(issue)
            unique_issues.append(issue)

    return unique_issues


def get_open_issues(issue_list: List[int]) -> List[int]:
    """Return all open issues from the list that are assigned to current user."""
    open_issues = []
    for issue_number in issue_list:
        try:
            issue = fetch_issue(str(issue_number), REPO_PATH)
            state = (issue.state or "").lower()
            if state == "open":
                if is_issue_assigned_to_me(str(issue_number), REPO_PATH):
                    open_issues.append(issue_number)
                else:
                    print(f"INFO: Issue #{issue_number} is open but not assigned to current user, skipping")
        except Exception as e:
            print(f"WARNING: Failed to fetch issue #{issue_number}: {e}")
    return open_issues


def is_workflow_active(issue_number: int) -> bool:
    """Check if a workflow is already running for this issue."""
    with tracking_lock:
        return issue_number in active_workflows


def mark_workflow_active(issue_number: int, adw_id: str):
    """Mark a workflow as active for an issue."""
    with tracking_lock:
        active_workflows[issue_number] = adw_id


def mark_workflow_complete(issue_number: int):
    """Mark a workflow as complete for an issue."""
    with tracking_lock:
        active_workflows.pop(issue_number, None)


def check_issue_for_workflow(issue_number: int) -> Optional[Dict]:
    """Check if an issue has a new workflow trigger in its body or latest comment.

    Returns a dict with workflow info if a trigger is found, None otherwise.
    Thread-safe implementation.
    """
    with tracking_lock:
        last_processed = issue_last_comment.get(issue_number)
        is_new = issue_number not in processed_new_issues

    comments = fetch_issue_comments(REPO_PATH, issue_number)

    if not comments:
        # New issue with no comments - check the issue body
        if not is_new:
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
                        with tracking_lock:
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
    if last_processed == comment_id:
        return None

    # Skip ADW bot comments to prevent loops
    if ADW_BOT_IDENTIFIER in comment_body:
        with tracking_lock:
            issue_last_comment[issue_number] = comment_id
        return None

    # Check if comment contains adw workflow trigger
    if "adw_" in comment_body.lower():
        temp_id = make_adw_id()
        extraction = extract_adw_info(comment_body, temp_id)
        if extraction.has_workflow:
            with tracking_lock:
                issue_last_comment[issue_number] = comment_id
            return {
                "workflow": extraction.workflow_command,
                "adw_id": extraction.adw_id,
                "model_set": extraction.model_set,
                "trigger_reason": f"Comment with {extraction.workflow_command} workflow",
            }

    # Update last processed comment even if no workflow found
    with tracking_lock:
        issue_last_comment[issue_number] = comment_id
    return None


def trigger_workflow(issue_number: int, workflow_info: Dict) -> Tuple[bool, str]:
    """Trigger an ADW workflow for a specific issue.

    Returns (success, message) tuple.
    """
    workflow = workflow_info["workflow"]
    provided_adw_id = workflow_info.get("adw_id")
    model_set = workflow_info.get("model_set")
    trigger_reason = workflow_info.get("trigger_reason", "")

    # Validate dependent workflows
    if workflow in DEPENDENT_WORKFLOWS:
        if not provided_adw_id:
            error_msg = f"{workflow} is a dependent workflow that requires an existing ADW ID"
            print(f"ERROR: {error_msg}")
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
            return False, error_msg

    # Use provided ADW ID or generate a new one
    adw_id = provided_adw_id or make_adw_id()

    # Mark workflow as active
    mark_workflow_active(issue_number, adw_id)

    # Manage ADW state
    if provided_adw_id:
        state = ADWState.load(provided_adw_id)
        if state:
            state.update(issue_number=str(issue_number), model_set=model_set)
        else:
            state = ADWState(provided_adw_id)
            state.update(adw_id=provided_adw_id, issue_number=str(issue_number), model_set=model_set)
        state.save("parallel_trigger")
    else:
        state = ADWState(adw_id)
        state.update(adw_id=adw_id, issue_number=str(issue_number), model_set=model_set)
        state.save("parallel_trigger")

    # Set up logger
    logger = setup_logger(adw_id, "parallel_trigger")
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
            f"🚀 ADW Parallel: Detected `{workflow}` workflow request\n\n"
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

        success_msg = f"Background process started (PID: {process.pid}) for issue #{issue_number} with ADW ID: {adw_id}"
        print(f"INFO: {success_msg}")
        logger.info(f"Background process started (PID: {process.pid})")
        return True, success_msg

    except Exception as e:
        error_msg = f"Exception while triggering workflow for issue #{issue_number}: {e}"
        print(f"ERROR: {error_msg}")
        logger.error(f"Exception: {e}")
        mark_workflow_complete(issue_number)
        return False, error_msg


def process_single_issue(issue_number: int) -> Tuple[int, bool, str]:
    """Process a single issue - designed for parallel execution.

    Returns (issue_number, success, message) tuple.
    """
    if shutdown_requested:
        return issue_number, False, "Shutdown requested"

    # Skip if workflow already active for this issue
    if is_workflow_active(issue_number):
        return issue_number, False, "Workflow already active"

    try:
        workflow_info = check_issue_for_workflow(issue_number)
        if workflow_info:
            success, message = trigger_workflow(issue_number, workflow_info)
            return issue_number, success, message
        return issue_number, False, "No workflow trigger found"
    except Exception as e:
        return issue_number, False, f"Error: {e}"


def check_and_process_issues_parallel(issue_list: List[int], max_concurrent: int):
    """Check all issues and process them in parallel."""
    if shutdown_requested:
        return

    start_time = time.time()
    print(f"INFO: Starting parallel issue check cycle (max concurrent: {max_concurrent})")

    try:
        # Get all open issues
        open_issues = get_open_issues(issue_list)
        if not open_issues:
            print("INFO: No open issues to process")
            return

        print(f"INFO: Found {len(open_issues)} open issues: {', '.join(str(i) for i in open_issues)}")

        # Process issues in parallel
        results = []
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            future_to_issue = {
                executor.submit(process_single_issue, issue): issue
                for issue in open_issues
            }

            for future in as_completed(future_to_issue):
                issue_number = future_to_issue[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"ERROR: Exception processing issue #{issue_number}: {e}")
                    results.append((issue_number, False, str(e)))

        # Summary
        triggered = [r for r in results if r[1]]
        skipped = [r for r in results if not r[1]]

        cycle_time = time.time() - start_time
        print(f"INFO: Parallel check complete ({cycle_time:.2f}s)")
        print(f"INFO: Triggered: {len(triggered)}, Skipped: {len(skipped)}")

        if triggered:
            print("INFO: Triggered workflows:")
            for issue_num, _, msg in triggered:
                print(f"  - Issue #{issue_num}: {msg[:80]}")

    except Exception as e:
        print(f"ERROR: Error during parallel check cycle: {e}")
        import traceback
        traceback.print_exc()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Parallel ADW trigger that processes multiple issues simultaneously.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    uv run trigger_issue_parallel.py 123 456 789
    uv run trigger_issue_parallel.py --issues 123,456,789
    uv run trigger_issue_parallel.py --issues 123,456,789 --max-concurrent 3
    uv run trigger_issue_parallel.py --issues 123,456,789 --interval 30

Supported workflows:
"""
        + "\n".join(f"    - {w}" for w in AVAILABLE_ADW_WORKFLOWS),
    )
    parser.add_argument(
        "issues",
        nargs="*",
        type=str,
        help="Issue numbers to process in parallel (space or comma separated)",
    )
    parser.add_argument(
        "--issues",
        dest="issues_csv",
        type=parse_issue_list,
        help="Comma-separated issue numbers to process (e.g. 12,34,56)",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=20,
        help="Polling interval in seconds (default: 20)",
    )
    parser.add_argument(
        "-m", "--max-concurrent",
        type=int,
        default=5,
        help="Maximum number of concurrent workflows (default: 5)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        default=False,
        help="Run a single parallel check cycle and exit (useful for testing)",
    )
    return parser.parse_args()


def main():
    """Main entry point for the parallel trigger."""
    args = parse_args()
    issue_list = resolve_issue_list(args)
    interval = args.interval
    max_concurrent = args.max_concurrent

    current_user = get_current_gh_user()
    print("INFO: Starting ADW parallel issue trigger")
    print(f"INFO: Repository: {REPO_PATH}")
    print(f"INFO: Current user: {current_user or 'unknown'}")
    print(f"INFO: Only processing issues assigned to current user")
    print(f"INFO: Issue list: {', '.join(str(n) for n in issue_list)}")
    print(f"INFO: Max concurrent workflows: {max_concurrent}")
    print(f"INFO: Polling interval: {interval} seconds")
    print(f"INFO: Supported workflows: {len(AVAILABLE_ADW_WORKFLOWS)}")

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Single execution mode
    if args.once:
        print("INFO: Running single parallel check cycle (--once mode)")
        check_and_process_issues_parallel(issue_list, max_concurrent)
        print("INFO: Single cycle complete, exiting")
        return

    # Normal loop mode - schedule and run continuously
    schedule.every(interval).seconds.do(
        check_and_process_issues_parallel, issue_list, max_concurrent
    )

    # Run initial check immediately
    check_and_process_issues_parallel(issue_list, max_concurrent)

    # Main loop
    print("INFO: Entering main scheduling loop")
    while not shutdown_requested:
        schedule.run_pending()
        time.sleep(1)

    print("INFO: Shutdown complete")


if __name__ == "__main__":
    main()
