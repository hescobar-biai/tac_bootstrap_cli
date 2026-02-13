#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
#     "pydantic",
#     "pyyaml",
#     "rich",
# ]
# ///

"""
ADW Local Trigger - 100% local SDLC workflow without GitHub dependency.

Runs all 5 SDLC phases locally using Claude Code CLI directly:
1. Plan - Generate implementation plan from task description or existing plan.md
2. Build - Implement the plan
3. Test - Run tests
4. Review - Review implementation
5. Document - Generate documentation

No GitHub issues, no remote API calls for tracking. Everything runs locally.

Usage:
    # From text task (generates plan first)
    uv run adws/adw_triggers/adw_local_trigger.py "Implement JWT authentication"

    # From existing plan file (skips plan phase)
    uv run adws/adw_triggers/adw_local_trigger.py --plan specs/plan.md

    # With AI docs loading
    uv run adws/adw_triggers/adw_local_trigger.py "Add dark mode" --load-docs "frontend,ui"

    # Skip phases
    uv run adws/adw_triggers/adw_local_trigger.py "Fix bug" --skip-test --skip-review

    # In isolated worktree
    uv run adws/adw_triggers/adw_local_trigger.py "Refactor auth" --worktree
"""

import sys
import os
import argparse
import logging
import time

from rich.console import Console
from rich.panel import Panel

console = Console()

# Add adws directory to path for module imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from adw_modules.agent import execute_template
from adw_modules.data_types import AgentTemplateRequest
from adw_modules.workflow_ops import ensure_adw_id, load_ai_docs, get_model_id
from adw_modules.utils import setup_logger, make_adw_id
try:
    from adw_modules.utils import strip_code_fences
except ImportError:
    import re as _re
    def strip_code_fences(text: str) -> str:
        text = text.strip()
        text = _re.sub(r"^```\w*\n?", "", text)
        text = _re.sub(r"\n?```$", "", text)
        return text.strip()
from adw_modules.state import ADWState
from adw_modules.worktree_ops import create_worktree, validate_worktree


def load_docs_context(
    topics: str, adw_id: str, logger: logging.Logger, working_dir: str = None,
) -> str | None:
    """Load AI documentation for given topics and return concatenated context."""
    topic_list = [t.strip() for t in topics.split(",") if t.strip()]
    if not topic_list:
        return None

    console.print(f"[blue]Loading AI docs: {', '.join(topic_list)}[/blue]")

    all_docs = []
    for topic in topic_list:
        response = load_ai_docs(topic, adw_id, logger, working_dir=working_dir)
        if response.success and response.output:
            all_docs.append(response.output)
            console.print(f"  [green]✓[/green] {topic}")
        else:
            console.print(f"  [yellow]⚠[/yellow] {topic} - failed to load")

    return "\n\n---\n\n".join(all_docs) if all_docs else None


def run_plan_phase(
    task: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
    ai_docs_context: str = None,
) -> str | None:
    """Run planning phase: generate implementation plan from task description.

    Returns:
        Path to the generated plan file, or None on failure.
    """
    console.rule("[bold]Plan Phase[/bold]")

    # Use /feature command which accepts a task description directly
    request = AgentTemplateRequest(
        agent_name="planner",
        slash_command="/feature",
        args=[task],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[red]Plan phase failed: {response.output[:200]}[/red]")
        return None

    # Extract plan file path from response
    plan_path = strip_code_fences(response.output)

    if not plan_path or not plan_path.endswith(".md"):
        console.print(f"[yellow]Could not extract plan path, using default[/yellow]")
        plan_path = "specs/plan.md"

    console.print(f"[green]✅ Plan created: {plan_path}[/green]")
    return plan_path


def run_build_phase(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
    ai_docs_context: str = None,
) -> bool:
    """Run build phase: implement the plan."""
    console.rule("[bold]Build Phase[/bold]")

    request = AgentTemplateRequest(
        agent_name="implementor",
        slash_command="/implement",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[red]Build phase failed: {response.output[:200]}[/red]")
        return False

    console.print("[green]✅ Build completed[/green]")
    return True


def run_test_phase(
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
) -> bool:
    """Run test phase."""
    console.rule("[bold]Test Phase[/bold]")

    request = AgentTemplateRequest(
        agent_name="tester",
        slash_command="/test",
        args=[],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[yellow]⚠️ Test phase failed (continuing): {response.output[:200]}[/yellow]")
        return False

    console.print("[green]✅ Tests passed[/green]")
    return True


def run_review_phase(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
) -> bool:
    """Run review phase."""
    console.rule("[bold]Review Phase[/bold]")

    request = AgentTemplateRequest(
        agent_name="reviewer",
        slash_command="/review",
        args=[adw_id, plan_file, "reviewer"],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[red]Review phase failed: {response.output[:200]}[/red]")
        return False

    console.print("[green]✅ Review completed[/green]")
    return True


def run_document_phase(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
) -> bool:
    """Run documentation phase."""
    console.rule("[bold]Document Phase[/bold]")

    request = AgentTemplateRequest(
        agent_name="documenter",
        slash_command="/document",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[red]Document phase failed: {response.output[:200]}[/red]")
        return False

    console.print("[green]✅ Documentation completed[/green]")
    return True


def run_commit_phase(
    adw_id: str,
    logger: logging.Logger,
    working_dir: str = None,
) -> bool:
    """Run commit phase to save all changes."""
    console.rule("[bold]Commit Phase[/bold]")

    request = AgentTemplateRequest(
        agent_name="committer",
        slash_command="/commit",
        args=[],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        console.print(f"[yellow]Commit phase: {response.output[:200]}[/yellow]")
        return False

    console.print("[green]✅ Changes committed[/green]")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="ADW Local Trigger - 100%% local SDLC workflow (no GitHub)"
    )
    parser.add_argument("task", nargs="?", default=None,
                        help="Task description text (generates plan)")
    parser.add_argument("--plan", type=str, default=None,
                        help="Path to existing plan.md file (skips plan phase)")
    parser.add_argument("--load-docs", type=str, default=None,
                        help="AI documentation topics to load (comma-separated)")
    parser.add_argument("--skip-test", action="store_true",
                        help="Skip test phase")
    parser.add_argument("--skip-review", action="store_true",
                        help="Skip review phase")
    parser.add_argument("--skip-document", action="store_true",
                        help="Skip documentation phase")
    parser.add_argument("--no-commit", action="store_true",
                        help="Skip auto-commit after each phase")
    parser.add_argument("--worktree", action="store_true",
                        help="Run in isolated worktree")

    args = parser.parse_args()

    # Validate: need either task or --plan
    if not args.task and not args.plan:
        parser.error("Provide a task description or --plan path")

    if args.plan and not os.path.exists(args.plan):
        parser.error(f"Plan file not found: {args.plan}")

    # Display what we're doing
    mode = f"Plan: {args.plan}" if args.plan else f"Task: {args.task}"
    console.print(Panel(
        f"[bold]Mode:[/bold] {'Existing plan' if args.plan else 'Generate plan'}\n"
        f"[bold]{mode}[/bold]\n"
        f"[bold]Docs:[/bold] {args.load_docs or 'none'}\n"
        f"[bold]Worktree:[/bold] {'yes' if args.worktree else 'no (current dir)'}",
        title="ADW Local Trigger",
        border_style="blue",
    ))

    # Initialize ADW
    adw_id = make_adw_id()
    logger = setup_logger(adw_id, "adw_local_trigger")

    # Initialize state
    state = ADWState(adw_id)
    state.update(adw_id=adw_id, workflow="local_trigger")
    state.save("adw_local_trigger")

    console.print(f"[blue]ADW ID: {adw_id}[/blue]")

    # Set up working directory
    working_dir = None
    if args.worktree:
        branch_name = f"local/{adw_id}"
        console.print(f"[blue]Creating worktree on branch: {branch_name}[/blue]")
        working_dir, error = create_worktree(adw_id, branch_name, logger)
        if error:
            console.print(f"[red]Failed to create worktree: {error}[/red]")
            sys.exit(1)
        console.print(f"[green]Worktree: {working_dir}[/green]")

        # Run setup_worktree.sh
        import subprocess
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(script_dir, "..", "scripts", "setup_worktree.sh")
        if os.path.exists(script_path):
            subprocess.run(["bash", script_path, working_dir], capture_output=True)

    # Load AI docs if requested
    ai_docs_context = None
    if args.load_docs:
        ai_docs_context = load_docs_context(
            args.load_docs, adw_id, logger, working_dir
        )

    # Track results
    results = {}
    plan_file = args.plan
    start_time = time.time()

    # Phase 1: PLAN
    if args.plan:
        console.print(f"[dim]Using existing plan: {args.plan}[/dim]")
        plan_file = args.plan
        results["Plan"] = True
    else:
        plan_file = run_plan_phase(
            args.task, adw_id, logger, working_dir, ai_docs_context
        )
        if not plan_file:
            console.print("[red]Plan phase failed. Aborting.[/red]")
            sys.exit(1)
        results["Plan"] = True

    # Phase 2: BUILD
    success = run_build_phase(plan_file, adw_id, logger, working_dir, ai_docs_context)
    results["Build"] = success
    if not success:
        console.print("[red]Build phase failed. Aborting.[/red]")
        sys.exit(1)

    # Phase 3: TEST (optional, allow failure)
    if args.skip_test:
        console.print("[dim]Skipping test phase[/dim]")
        results["Test"] = None
    else:
        results["Test"] = run_test_phase(adw_id, logger, working_dir)

    # Phase 4: REVIEW (optional)
    if args.skip_review:
        console.print("[dim]Skipping review phase[/dim]")
        results["Review"] = None
    else:
        success = run_review_phase(plan_file, adw_id, logger, working_dir)
        results["Review"] = success

    # Phase 5: DOCUMENT (optional)
    if args.skip_document:
        console.print("[dim]Skipping document phase[/dim]")
        results["Document"] = None
    else:
        success = run_document_phase(plan_file, adw_id, logger, working_dir)
        results["Document"] = success

    # Auto-commit
    if not args.no_commit:
        run_commit_phase(adw_id, logger, working_dir)

    # Summary
    elapsed = time.time() - start_time
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)

    summary_lines = []
    for name, ok in results.items():
        if ok is None:
            summary_lines.append(f"⏭️  {name} (skipped)")
        elif ok:
            summary_lines.append(f"✅ {name}")
        else:
            summary_lines.append(f"❌ {name}")

    console.print()
    console.print(Panel(
        "\n".join(summary_lines)
        + f"\n\n[bold]ADW ID:[/bold] {adw_id}"
        + f"\n[bold]Duration:[/bold] {mins}m {secs}s"
        + (f"\n[bold]Worktree:[/bold] {working_dir}" if working_dir else ""),
        title="Local SDLC Complete",
        border_style="green",
    ))


if __name__ == "__main__":
    main()
