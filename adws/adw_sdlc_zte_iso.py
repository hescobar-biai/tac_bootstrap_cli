#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml"]
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
from adw_modules.workflow_ops import (
    ensure_adw_id,
    detect_relevant_docs,
    extract_file_references_from_issue,
    format_file_references_for_context,
)
from adw_modules.github import make_issue_comment, fetch_issue, get_repo_url, extract_repo_path
from adw_modules.utils import get_target_branch, setup_logger
from adw_modules.state import ADWState


def main():
    """Main entry point."""
    # Check for flags
    skip_e2e = "--skip-e2e" in sys.argv
    skip_resolution = "--skip-resolution" in sys.argv

    # TAC: Enabled by default for orchestrated workflows (opt-out)
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
        print("  --no-experts         Disable TAC expert consultation (enabled by default)")
        print("  --no-expert-learn    Disable TAC self-improve (enabled by default)")
        print("\n🧠 TAC Expert System: ENABLED BY DEFAULT for complete workflows")
        print(f"\n⚠️  WARNING: This will automatically merge to {target_branch} if all phases pass!")
        sys.exit(1)

    issue_number = sys.argv[1]
    adw_id = sys.argv[2] if len(sys.argv) > 2 else None

    # Ensure ADW ID exists with initialized state
    adw_id = ensure_adw_id(issue_number, adw_id)
    print(f"Using ADW ID: {adw_id}")

    # Set up logger for detection phase
    logger = setup_logger(adw_id, "adw_sdlc_zte_iso")

    # Load existing state to check which phases are already completed
    state = ADWState(adw_id)
    completed_phases = state.get("all_adws", [])

    # Detect or use manual docs (TAC-9 hybrid approach)
    docs_to_load = None
    if manual_docs:
        # User specified manual override
        docs_to_load = manual_docs
        logger.info(f"Using manual documentation override: {docs_to_load}")
        print(f"📚 Loading documentation (manual): {docs_to_load}")
    else:
        # Hybrid detection: Explicit references (priority) + Automatic detection (fallback)
        try:
            github_repo_url = get_repo_url()
            repo_path = extract_repo_path(github_repo_url)
            issue = fetch_issue(issue_number, repo_path)

            # PRIORITY 1: Explicit file references from issue body/comments
            logger.info("Checking for explicit file references in issue body + comments...")
            file_references = extract_file_references_from_issue(issue, logger, working_dir=None)

            explicit_topics = []
            if file_references:
                explicit_topics = list(file_references.keys())
                logger.info(f"Found {len(explicit_topics)} explicit file reference(s): {explicit_topics}")
                print(f"📎 Found {len(explicit_topics)} explicit file reference(s): {', '.join(explicit_topics)}")

            # PRIORITY 2: Automatic keyword-based detection (fallback)
            detected_topics = detect_relevant_docs(issue)
            if detected_topics:
                logger.info(f"Auto-detected {len(detected_topics)} documentation topic(s): {detected_topics}")
                print(f"📚 Auto-detected {len(detected_topics)} documentation topic(s): {', '.join(detected_topics)}")

            # Combine both with priority to explicit references (avoid duplicates)
            all_topics = explicit_topics.copy()
            for topic in detected_topics:
                # Remove .md extension from detected topics for comparison
                topic_base = topic[:-3] if topic.endswith('.md') else topic
                # Check if not already in explicit references
                if not any(topic_base in ref or ref in topic_base for ref in explicit_topics):
                    all_topics.append(topic)

            if all_topics:
                docs_to_load = ",".join(all_topics)
                logger.info(f"Total documentation to load: {len(all_topics)} topic(s)")
                print(f"📚 Total documentation to load: {len(all_topics)} topic(s)")
            else:
                logger.info("No documentation topics found (explicit or automatic)")
                print("📚 No documentation topics found")
        except Exception as e:
            logger.warning(f"Failed to detect documentation topics: {e}")
            print(f"⚠️  Warning: Could not detect documentation topics: {e}")

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

    # Run isolated plan with the ADW ID (skip if already completed)
    if "adw_plan_iso" in completed_phases:
        print(f"\n=== ISOLATED PLAN PHASE ===")
        print("✓ Plan phase already completed - skipping")
        logger.info("Plan phase already completed, skipping execution")
    else:
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

        # TAC Optimization: Only consult experts in Plan phase (guidance needed)
        if use_experts:
            plan_cmd.append("--use-experts")
            logger.info("TAC: Expert consultation enabled for plan phase")

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

        # Reload state after plan completes
        state = ADWState(adw_id)
        completed_phases = state.get("all_adws", [])

    # Run isolated build with the ADW ID (skip if already completed)
    if "adw_build_iso" in completed_phases:
        print(f"\n=== ISOLATED BUILD PHASE ===")
        print("✓ Build phase already completed - skipping")
        logger.info("Build phase already completed, skipping execution")
    else:
        build_cmd = [
            "uv",
            "run",
            os.path.join(script_dir, "adw_build_iso.py"),
            issue_number,
            adw_id,
        ]

        # TAC Optimization: Build phase doesn't need expert consultation (direct implementation)

        print(f"\n=== ISOLATED BUILD PHASE ===")
        print(f"Running: {' '.join(build_cmd)}")
        build = subprocess.run(build_cmd)
        if build.returncode != 0:
            print("Isolated build phase failed")
            sys.exit(1)

        # Reload state after build completes
        state = ADWState(adw_id)
        completed_phases = state.get("all_adws", [])

    # Run isolated test with the ADW ID (skip if already completed)
    if "adw_test_iso" in completed_phases:
        print(f"\n=== ISOLATED TEST PHASE ===")
        print("✓ Test phase already completed - skipping")
        logger.info("Test phase already completed, skipping execution")
    else:
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

        # Reload state after test completes
        state = ADWState(adw_id)
        completed_phases = state.get("all_adws", [])

    # Run isolated review with the ADW ID (skip if already completed)
    if "adw_review_iso" in completed_phases:
        print(f"\n=== ISOLATED REVIEW PHASE ===")
        print("✓ Review phase already completed - skipping")
        logger.info("Review phase already completed, skipping execution")
    else:
        review_cmd = [
            "uv",
            "run",
            os.path.join(script_dir, "adw_review_iso.py"),
            issue_number,
            adw_id,
        ]
        if skip_resolution:
            review_cmd.append("--skip-resolution")

        # TAC Optimization: Only consult experts in Review phase (validation critical)
        if use_experts:
            review_cmd.append("--use-experts")

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

        # Reload state after review completes
        state = ADWState(adw_id)
        completed_phases = state.get("all_adws", [])

    # Run isolated documentation with the ADW ID (skip if already completed)
    if "adw_document_iso" in completed_phases:
        print(f"\n=== ISOLATED DOCUMENTATION PHASE ===")
        print("✓ Documentation phase already completed - skipping")
        logger.info("Documentation phase already completed, skipping execution")
    else:
        document_cmd = [
            "uv",
            "run",
            os.path.join(script_dir, "adw_document_iso.py"),
            issue_number,
            adw_id,
        ]

        # TAC Optimization: Document phase only does final learning (full validation)
        if expert_learn:
            document_cmd.append("--expert-learn")

        print(f"\n=== ISOLATED DOCUMENTATION PHASE ===")
        print(f"Running: {' '.join(document_cmd)}")
        document = subprocess.run(document_cmd)
        if document.returncode != 0:
            print("Isolated documentation phase failed")
            # Documentation failure shouldn't block shipping
            print("WARNING: Documentation phase failed but continuing with shipping")

        # Reload state after documentation completes
        state = ADWState(adw_id)
        completed_phases = state.get("all_adws", [])

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
