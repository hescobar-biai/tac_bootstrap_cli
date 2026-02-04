#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW SDLC ZTE Iso - Zero Touch Execution: Complete SDLC with automatic shipping

Usage: uv run adw_sdlc_zte_iso.py <issue-number> [adw-id] [--load-docs TOPICS] [--skip-e2e] [--skip-resolution]

Options:
  --load-docs TOPICS    Manual override for documentation topics (comma-separated)
                        If not specified, topics are auto-detected from issue (TAC-9)
  --skip-e2e           Skip E2E test execution
  --skip-resolution    Skip test failure resolution

This script runs the complete ADW SDLC pipeline with automatic shipping:
1. adw_plan_iso.py - Planning phase (isolated)
2. adw_build_iso.py - Implementation phase (isolated)
3. adw_test_iso.py - Testing phase (isolated)
4. adw_review_iso.py - Review phase (isolated)
5. adw_document_iso.py - Documentation phase (isolated)
6. adw_ship_iso.py - Ship phase (approve & merge PR)

ZTE = Zero Touch Execution: The entire workflow runs to completion without
human intervention, automatically shipping code to production if all phases pass.

The scripts are chained together via persistent state (adw_state.json).
Each phase runs on the same git worktree with dedicated ports.
"""

import subprocess
import sys
import os

# Add the parent directory to Python path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adw_modules.workflow_ops import ensure_adw_id, detect_relevant_docs
from adw_modules.github import make_issue_comment, fetch_issue, get_repo_url, extract_repo_path
from adw_modules.utils import get_target_branch, setup_logger
from adw_modules.state import ADWState


def main():
    """Main entry point."""
    # Check for flags
    skip_e2e = "--skip-e2e" in sys.argv
    skip_resolution = "--skip-resolution" in sys.argv

    # TAC-13: Enabled by default for orchestrated workflows (opt-out)
    use_experts = "--no-experts" not in sys.argv
    expert_learn = "--no-expert-learn" not in sys.argv

    # Check for manual docs override (TAC-9 hybrid approach)
    manual_docs = None
    if "--load-docs" in sys.argv:
        idx = sys.argv.index("--load-docs")
        if idx + 1 < len(sys.argv):
            manual_docs = sys.argv[idx + 1]
            sys.argv.pop(idx)  # Remove --load-docs
            sys.argv.pop(idx)  # Remove the topic value

    # Remove flags from argv
    if skip_e2e:
        sys.argv.remove("--skip-e2e")
    if skip_resolution:
        sys.argv.remove("--skip-resolution")
    if "--no-experts" in sys.argv:
        sys.argv.remove("--no-experts")
    if "--no-expert-learn" in sys.argv:
        sys.argv.remove("--no-expert-learn")

    if len(sys.argv) < 2:
        target_branch = get_target_branch()
        print(
            "Usage: uv run adw_sdlc_zte_iso.py <issue-number> [adw-id] [--load-docs TOPICS] [--skip-e2e] [--skip-resolution] [--no-experts] [--no-expert-learn]"
        )
        print("\n🚀 Zero Touch Execution: Complete SDLC with automatic shipping")
        print("\nThis runs the complete isolated Software Development Life Cycle:")
        print("  1. Plan (isolated)")
        print("  2. Build (isolated)")
        print("  3. Test (isolated)")
        print("  4. Review (isolated)")
        print("  5. Document (isolated)")
        print("  6. Ship (approve & merge PR) 🚢")
        print("\nOptions:")
        print("  --load-docs TOPICS    Manual override for documentation topics (comma-separated)")
        print("                        If not specified, topics are auto-detected from issue (TAC-9)")
        print("  --skip-e2e           Skip E2E test execution")
        print("  --skip-resolution    Skip test failure resolution")
        print("  --no-experts         Disable TAC-13 expert consultation (enabled by default)")
        print("  --no-expert-learn    Disable TAC-13 self-improve (enabled by default)")
        print("\n🧠 TAC-13 Expert System: ENABLED BY DEFAULT for complete workflows")
        print(f"\n⚠️  WARNING: This will automatically merge to {target_branch} if all phases pass!")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else None

    # Ensure ADW ID exists with initialized state
    adw_id = ensure_adw_id(issue_number, adw_id)
    print(f"Using ADW ID: {adw_id}")

    # Set up logger for detection phase
    logger = setup_logger(adw_id, "adw_sdlc_zte_iso")

    # Detect or use manual docs (TAC-9 hybrid approach)
    docs_to_load = None
    if manual_docs:
        # User specified manual override
        docs_to_load = manual_docs
        logger.info(f"Using manual documentation override: {docs_to_load}")
        print(f"📚 Loading documentation (manual): {docs_to_load}")
    else:
        # Automatic detection
        try:
            github_repo_url = get_repo_url()
            repo_path = extract_repo_path(github_repo_url)
            issue = fetch_issue(issue_number, repo_path)

            detected_topics = detect_relevant_docs(issue)
            if detected_topics:
                docs_to_load = ",".join(detected_topics)
                logger.info(f"Auto-detected relevant documentation topics: {detected_topics}")
                print(f"📚 Auto-detected documentation topics: {', '.join(detected_topics)}")
            else:
                logger.info("No relevant documentation topics detected")
                print("📚 No relevant documentation topics detected")
        except Exception as e:
            logger.warning(f"Failed to detect documentation topics: {e}")
            print(f"⚠️  Warning: Could not auto-detect documentation topics: {e}")

    # Post initial ZTE message
    try:
        make_issue_comment(
            issue_number,
            f"{adw_id}_ops: 🚀 **Starting Zero Touch Execution (ZTE)**\n\n"
            "This workflow will automatically:\n"
            "1. ✍️ Plan the implementation\n"
            "2. 🔨 Build the solution\n"
            "3. 🧪 Test the code\n"
            "4. 👀 Review the implementation\n"
            "5. 📚 Generate documentation\n"
            "6. 🚢 **Ship to production** (approve & merge PR)\n\n"
            "⚠️ Code will be automatically merged if all phases pass!",
        )
    except Exception as e:
        print(f"Warning: Failed to post initial comment: {e}")

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Run isolated plan with the ADW ID
    plan_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_plan_iso.py"),
        issue_number,
        adw_id,
    ]

    # Add documentation loading if detected or manually specified (TAC-9)
    if docs_to_load:
        plan_cmd.extend(["--load-docs", docs_to_load])
        logger.info(f"Passing documentation to planning phase: {docs_to_load}")

    # Add TAC-13 expert flags if enabled
    if use_experts:
        plan_cmd.append("--use-experts")
        logger.info("TAC-13: Expert consultation enabled for plan phase")
    if expert_learn:
        plan_cmd.append("--expert-learn")
        logger.info("TAC-13: Expert learning enabled for plan phase")

    print(f"\n=== ISOLATED PLAN PHASE ===")
    print(f"Running: {' '.join(plan_cmd)}")
    plan = subprocess.run(plan_cmd)
    if plan.returncode == 2:
        # Exit code 2 = paused for clarifications
        print("⏸️  Plan phase paused - awaiting user clarifications")
        print("Please answer the clarification questions on the GitHub issue,")
        print("then re-run this workflow to continue.")
        try:
            make_issue_comment(
                issue_number,
                f"{adw_id}_ops: ⏸️ **ZTE Paused** - Awaiting clarifications\n\n"
                "The planning phase found ambiguities that need user input.\n"
                "Please answer the questions above, then re-run the workflow.",
            )
        except:
            pass
        sys.exit(2)  # Propagate paused state
    elif plan.returncode != 0:
        print("Isolated plan phase failed")
        sys.exit(1)

    # Run isolated build with the ADW ID
    build_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_build_iso.py"),
        issue_number,
        adw_id,
    ]

    # Add TAC-13 expert flags if enabled
    if use_experts:
        build_cmd.append("--use-experts")
    if expert_learn:
        build_cmd.append("--expert-learn")

    print(f"\n=== ISOLATED BUILD PHASE ===")
    print(f"Running: {' '.join(build_cmd)}")
    build = subprocess.run(build_cmd)
    if build.returncode != 0:
        print("Isolated build phase failed")
        sys.exit(1)

    # Run isolated test with the ADW ID
    test_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_test_iso.py"),
        issue_number,
        adw_id,
        "--skip-e2e",  # Always skip E2E tests in SDLC workflows
    ]

    print(f"\n=== ISOLATED TEST PHASE ===")
    print(f"Running: {' '.join(test_cmd)}")
    test = subprocess.run(test_cmd)
    if test.returncode != 0:
        print("Isolated test phase failed")
        # For ZTE, we should stop if tests fail
        try:
            make_issue_comment(
                issue_number,
                f"{adw_id}_ops: ❌ **ZTE Aborted** - Test phase failed\n\n"
                "Automatic shipping cancelled due to test failures.\n"
                "Please fix the tests and run the workflow again.",
            )
        except:
            pass
        sys.exit(1)

    # Run isolated review with the ADW ID
    review_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_review_iso.py"),
        issue_number,
        adw_id,
    ]
    if skip_resolution:
        review_cmd.append("--skip-resolution")

    # Add TAC-13 expert flags if enabled
    if use_experts:
        review_cmd.append("--use-experts")
    if expert_learn:
        review_cmd.append("--expert-learn")

    print(f"\n=== ISOLATED REVIEW PHASE ===")
    print(f"Running: {' '.join(review_cmd)}")
    review = subprocess.run(review_cmd)
    if review.returncode != 0:
        print("Isolated review phase failed")
        try:
            make_issue_comment(
                issue_number,
                f"{adw_id}_ops: ❌ **ZTE Aborted** - Review phase failed\n\n"
                "Automatic shipping cancelled due to review failures.\n"
                "Please address the review issues and run the workflow again.",
            )
        except:
            pass
        sys.exit(1)

    # Run isolated documentation with the ADW ID
    document_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_document_iso.py"),
        issue_number,
        adw_id,
    ]

    # Add TAC-13 expert flags if enabled
    if use_experts:
        document_cmd.append("--use-experts")
    if expert_learn:
        document_cmd.append("--expert-learn")

    print(f"\n=== ISOLATED DOCUMENTATION PHASE ===")
    print(f"Running: {' '.join(document_cmd)}")
    document = subprocess.run(document_cmd)
    if document.returncode != 0:
        print("Isolated documentation phase failed")
        # Documentation failure shouldn't block shipping
        print("WARNING: Documentation phase failed but continuing with shipping")

    # Run isolated ship with the ADW ID
    ship_cmd = [
        "uv",
        "run",
        os.path.join(script_dir, "adw_ship_iso.py"),
        issue_number,
        adw_id,
    ]
    print(f"\n=== ISOLATED SHIP PHASE (APPROVE & MERGE) ===")
    print(f"Running: {' '.join(ship_cmd)}")
    ship = subprocess.run(ship_cmd)
    if ship.returncode != 0:
        print("Isolated ship phase failed")
        try:
            make_issue_comment(
                issue_number,
                f"{adw_id}_ops: ❌ **ZTE Failed** - Ship phase failed\n\n"
                "Could not automatically approve and merge the PR.\n"
                "Please check the ship logs and merge manually if needed.",
            )
        except:
            pass
        sys.exit(1)

    print(f"\n=== 🎉 ZERO TOUCH EXECUTION COMPLETED ===")
    print(f"ADW ID: {adw_id}")
    print(f"All phases completed successfully!")
    print(f"✅ Code has been shipped to production!")
    print(f"\nWorktree location: trees/{adw_id}/")
    print(f"To clean up: ./scripts/purge_tree.sh {adw_id}")

    # Load final state to get token summary
    token_summary = ""
    try:
        state = ADWState.load(adw_id)
        if state:
            token_summary = "\n\n" + state.get_token_summary()
            # Print token summary to console
            print(f"\n{state.get_token_summary()}")
    except Exception as e:
        print(f"Warning: Failed to load token summary: {e}")

    try:
        make_issue_comment(
            issue_number,
            f"{adw_id}_ops: 🎉 **Zero Touch Execution Complete!**\n\n"
            "✅ Plan phase completed\n"
            "✅ Build phase completed\n"
            "✅ Test phase completed\n"
            "✅ Review phase completed\n"
            "✅ Documentation phase completed\n"
            "✅ Ship phase completed\n\n"
            "🚢 **Code has been automatically shipped to production!**"
            f"{token_summary}",
        )
    except:
        pass


if __name__ == "__main__":
    main()
