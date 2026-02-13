#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "pyyaml",
#     "rich",
# ]
# ///

"""
ADW SDLC Trigger - Execute the full SDLC workflow from a text task description.

Creates a GitHub issue from the task description, then runs all 5 phases sequentially:
1. Plan (isolated)
2. Build (isolated)
3. Test (isolated)
4. Review (isolated)
5. Document (isolated)

Usage:
    uv run adws/adw_triggers/adw_sdlc_trigger.py "Implement JWT authentication" "owner/repo"
    uv run adws/adw_triggers/adw_sdlc_trigger.py "Add dark mode toggle" "owner/repo" --load-docs "frontend,ui"
    uv run adws/adw_triggers/adw_sdlc_trigger.py "Fix pagination bug" "owner/repo" --skip-e2e
"""

import subprocess
import sys
import os
import re
import argparse

from rich.console import Console
from rich.panel import Panel

console = Console()

# Add adws directory to path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adw_modules.workflow_ops import ensure_adw_id
from adw_modules.utils import setup_logger


def create_github_issue(task_description: str, repo: str) -> str | None:
    """Create a GitHub issue from a task description using gh CLI.

    Args:
        task_description: The task text to use as issue title/body.
        repo: GitHub repository in owner/repo format.

    Returns:
        Issue number as string, or None on failure.
    """
    console.print(f"[bold blue]Creating GitHub issue...[/bold blue]")

    result = subprocess.run(
        [
            "gh", "issue", "create",
            "--repo", repo,
            "--title", task_description,
            "--body", f"Task created by ADW SDLC Trigger.\n\n{task_description}",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        console.print(f"[red]Failed to create issue: {result.stderr}[/red]")
        return None

    # gh issue create outputs the URL: https://github.com/owner/repo/issues/123
    match = re.search(r"/issues/(\d+)", result.stdout.strip())
    if match:
        return match.group(1)

    console.print(f"[red]Could not parse issue number from: {result.stdout}[/red]")
    return None


def run_phase(
    phase_name: str,
    script_name: str,
    issue_number: str,
    adw_id: str,
    script_dir: str,
    extra_args: list[str] | None = None,
    allow_failure: bool = False,
) -> bool:
    """Run a single SDLC phase.

    Args:
        phase_name: Display name for the phase.
        script_name: Script filename (e.g., "adw_plan_iso.py").
        issue_number: GitHub issue number.
        adw_id: ADW workflow ID.
        script_dir: Directory containing the phase scripts.
        extra_args: Additional CLI arguments for the phase.
        allow_failure: If True, continue on failure (e.g., tests).

    Returns:
        True if phase succeeded, False if failed.
    """
    console.rule(f"[bold]{phase_name}[/bold]")

    cmd = [
        "uv", "run",
        os.path.join(script_dir, script_name),
        issue_number,
        adw_id,
    ]
    if extra_args:
        cmd.extend(extra_args)

    console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")

    result = subprocess.run(cmd)

    if result.returncode == 2:
        console.print(f"[yellow]⏸️  {phase_name} paused - awaiting clarifications[/yellow]")
        sys.exit(2)
    elif result.returncode != 0:
        if allow_failure:
            console.print(f"[yellow]⚠️  {phase_name} failed but continuing[/yellow]")
            return False
        else:
            console.print(f"[red]❌ {phase_name} failed[/red]")
            return False

    console.print(f"[green]✅ {phase_name} completed[/green]")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="ADW SDLC Trigger - Full workflow from text task"
    )
    parser.add_argument("task", help="Task description text")
    parser.add_argument("repo", help="GitHub repository (owner/repo)")
    parser.add_argument("--load-docs", type=str, default=None,
                        help="Documentation topics to load (comma-separated)")
    parser.add_argument("--skip-e2e", action="store_true",
                        help="Skip E2E test execution")
    parser.add_argument("--skip-resolution", action="store_true",
                        help="Skip test failure resolution")
    parser.add_argument("--no-experts", action="store_true",
                        help="Disable TAC expert consultation")
    parser.add_argument("--no-expert-learn", action="store_true",
                        help="Disable TAC self-improve")

    args = parser.parse_args()

    console.print(Panel(
        f"[bold]Task:[/bold] {args.task}\n[bold]Repo:[/bold] {args.repo}",
        title="ADW SDLC Trigger",
        border_style="blue",
    ))

    # Step 1: Create GitHub issue
    issue_number = create_github_issue(args.task, args.repo)
    if not issue_number:
        console.print("[red]Failed to create GitHub issue. Aborting.[/red]")
        sys.exit(1)

    console.print(f"[green]Created issue #{issue_number}[/green]")

    # Step 2: Initialize ADW
    adw_id = ensure_adw_id(issue_number)
    console.print(f"[blue]ADW ID: {adw_id}[/blue]")

    logger = setup_logger(adw_id, "adw_sdlc_trigger")

    # Phase scripts directory (adws/)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Build phase-specific args
    plan_args = []
    if args.load_docs:
        plan_args.extend(["--load-docs", args.load_docs])
    if not args.no_experts:
        plan_args.append("--use-experts")

    review_args = []
    if args.skip_resolution:
        review_args.append("--skip-resolution")
    if not args.no_experts:
        review_args.append("--use-experts")

    document_args = []
    if not args.no_expert_learn:
        document_args.append("--expert-learn")

    # Step 3: Run all phases sequentially
    phases = [
        ("Plan Phase", "adw_plan_iso.py", plan_args, False),
        ("Build Phase", "adw_build_iso.py", [], False),
        ("Test Phase", "adw_test_iso.py", ["--skip-e2e"] if args.skip_e2e else [], True),
        ("Review Phase", "adw_review_iso.py", review_args, False),
        ("Document Phase", "adw_document_iso.py", document_args, False),
    ]

    results = {}
    for phase_name, script_name, extra_args, allow_failure in phases:
        success = run_phase(
            phase_name, script_name, issue_number, adw_id,
            script_dir, extra_args, allow_failure,
        )
        results[phase_name] = success

        if not success and not allow_failure:
            console.print(f"\n[red]Workflow aborted at {phase_name}[/red]")
            sys.exit(1)

    # Step 4: Summary
    console.print()
    console.print(Panel(
        "\n".join(
            f"{'✅' if ok else '❌'} {name}" for name, ok in results.items()
        ) + f"\n\n[bold]ADW ID:[/bold] {adw_id}\n[bold]Issue:[/bold] #{issue_number}",
        title="SDLC Workflow Complete",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
