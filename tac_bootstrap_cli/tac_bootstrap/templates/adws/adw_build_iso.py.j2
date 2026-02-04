#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Build Iso - AI Developer Workflow for agentic building in isolated worktrees

Usage:
  uv run adw_build_iso.py <issue-number> <adw-id> [--with-report]

Options:
  --with-report    Use /build_w_report for structured YAML change tracking (TAC-10)

Workflow:
1. Load state and validate worktree exists
2. Find existing plan (from state)
3. Implement the solution based on plan in worktree
4. Commit implementation in worktree
5. Push and update PR

This workflow REQUIRES that adw_plan_iso.py or adw_patch_iso.py has been run first
to create the worktree. It cannot create worktrees itself.
"""

import sys
import os
import logging
import json
import subprocess
from typing import Optional
from dotenv import load_dotenv

from adw_modules.state import ADWState
from adw_modules.git_ops import commit_changes, finalize_git_operations, get_current_branch
from adw_modules.github import fetch_issue, make_issue_comment, get_repo_url, extract_repo_path
from adw_modules.workflow_ops import (
    implement_plan,
    implement_plan_with_report,
    build_in_parallel,
    create_commit,
    format_issue_message,
    consult_expert,
    improve_expert_knowledge,
    AGENT_IMPLEMENTOR,
)
from adw_modules.utils import setup_logger, check_env_vars
from adw_modules.data_types import GitHubIssue
from adw_modules.worktree_ops import validate_worktree




def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line args
    import argparse
    parser = argparse.ArgumentParser(description="ADW Build Iso - Agentic building in isolated worktrees")
    parser.add_argument("issue_number", help="GitHub issue number")
    parser.add_argument("adw_id", help="ADW ID (required to locate worktree)")
    parser.add_argument("--with-report", action="store_true",
                       help="Use /build_w_report for structured YAML change tracking (TAC-10)")
    parser.add_argument("--parallel", action="store_true",
                       help="Use parallel build agents for faster implementation (TAC-12)")
    parser.add_argument("--use-experts", action="store_true",
                       help="Enable TAC-13 expert consultation")
    parser.add_argument("--expert-learn", action="store_true",
                       help="Enable TAC-13 self-improve after build")

    args = parser.parse_args()

    issue_number = args.issue_number
    adw_id = args.adw_id
    with_report = args.with_report
    use_parallel = args.parallel
    use_experts = args.use_experts
    expert_learn = args.expert_learn

    # Try to load existing state
    temp_logger = setup_logger(adw_id, "adw_build_iso")
    state = ADWState.load(adw_id, temp_logger)
    if state:
        # Found existing state - use the issue number from state if available
        issue_number = state.get("issue_number", issue_number)
        make_issue_comment(
            issue_number,
            f"{adw_id}_ops: 🔍 Found existing state - resuming isolated build\n```json\n{json.dumps(state.data, indent=2)}\n```"
        )
    else:
        # No existing state found
        logger = setup_logger(adw_id, "adw_build_iso")
        logger.error(f"No state found for ADW ID: {adw_id}")
        logger.error("Run adw_plan_iso.py first to create the worktree and state")
        print(f"\nError: No state found for ADW ID: {adw_id}")
        print("Run adw_plan_iso.py first to create the worktree and state")
        sys.exit(1)
    
    # Track that this ADW workflow has run
    state.append_adw_id("adw_build_iso")
    
    # Set up logger with ADW ID from command line
    logger = setup_logger(adw_id, "adw_build_iso")
    logger.info(f"ADW Build Iso starting - ID: {adw_id}, Issue: {issue_number}")
    
    # Validate environment
    check_env_vars(logger)
    
    # Validate worktree exists
    valid, error = validate_worktree(adw_id, state)
    if not valid:
        logger.error(f"Worktree validation failed: {error}")
        logger.error("Run adw_plan_iso.py or adw_patch_iso.py first")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ Worktree validation failed: {error}\n"
                               "Run adw_plan_iso.py or adw_patch_iso.py first")
        )
        sys.exit(1)
    
    # Get worktree path for explicit context
    worktree_path = state.get("worktree_path")
    logger.info(f"Using worktree at: {worktree_path}")
    
    # Get repo information
    try:
        github_repo_url = get_repo_url()
        repo_path = extract_repo_path(github_repo_url)
    except ValueError as e:
        logger.error(f"Error getting repository URL: {e}")
        sys.exit(1)
    
    # Ensure we have required state fields
    if not state.get("branch_name"):
        error_msg = "No branch name in state - run adw_plan_iso.py first"
        logger.error(error_msg)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ {error_msg}")
        )
        sys.exit(1)
    
    if not state.get("plan_file"):
        error_msg = "No plan file in state - run adw_plan_iso.py first"
        logger.error(error_msg)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ {error_msg}")
        )
        sys.exit(1)
    
    # Checkout the branch in the worktree
    branch_name = state.get("branch_name")
    result = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True, cwd=worktree_path)
    if result.returncode != 0:
        logger.error(f"Failed to checkout branch {branch_name} in worktree: {result.stderr}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ Failed to checkout branch {branch_name} in worktree")
        )
        sys.exit(1)
    logger.info(f"Checked out branch in worktree: {branch_name}")
    
    # Get the plan file from state
    plan_file = state.get("plan_file")
    logger.info(f"Using plan file: {plan_file}")

    # Get AI docs context from state if available (TAC-9)
    ai_docs_context = state.get("ai_docs_context")
    if ai_docs_context:
        logger.info("Using AI documentation context from planning phase")
    else:
        logger.debug("No AI documentation context available")

    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, "ops", f"✅ Starting isolated implementation phase\n"
                           f"🏠 Worktree: {worktree_path}")
    )

    # TAC-13 REUSE: Consultar expertise antes de build
    if use_experts:
        logger.info("TAC-13: Consulting ADW expert for build patterns")

        planning_guidance = state.get("expert_planning_guidance", "")

        expert_question = f"""I'm implementing this plan: {plan_file}

Previous guidance: {planning_guidance[:200] if planning_guidance else "None"}

What build patterns should I follow?
Focus on: module composition, git operations, error recovery."""

        expert_response = consult_expert(
            domain="adw",
            question=expert_question,
            adw_id=adw_id,
            logger=logger,
            working_dir=worktree_path
        )

        if expert_response.success:
            state.update(expert_build_guidance=expert_response.output)
            state.accumulate_tokens("adw_expert", expert_response.token_usage)
            state.save("adw_build_iso")

    # Implement the plan (executing in worktree) with optional parallel build (TAC-12) or report (TAC-10)
    logger.info("Implementing solution in worktree")

    if use_parallel:
        logger.info("Using /build_in_parallel for faster implementation (TAC-12)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution with parallel build agents (TAC-12)")
        )
        implement_response = build_in_parallel(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    elif with_report:
        logger.info("Using /build_w_report for structured change tracking (TAC-10)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution with YAML report tracking (TAC-10)")
        )
        implement_response = implement_plan_with_report(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    else:
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution in isolated environment")
        )
        implement_response = implement_plan(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)

    # Track token usage from implementation
    state.accumulate_tokens(AGENT_IMPLEMENTOR, implement_response.token_usage)
    state.save("adw_build_iso")

    if not implement_response.success:
        logger.error(f"Error implementing solution: {implement_response.output}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error implementing solution: {implement_response.output}")
        )
        sys.exit(1)
    
    logger.debug(f"Implementation response: {implement_response.output}")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Solution implemented")
    )
    
    # Fetch issue data for commit message generation
    logger.info("Fetching issue data for commit message")
    issue = fetch_issue(issue_number, repo_path)
    
    # Get issue classification from state or classify if needed
    issue_command = state.get("issue_class")
    if not issue_command:
        logger.info("No issue classification in state, running classify_issue")
        from adw_modules.workflow_ops import classify_issue
        issue_command, error = classify_issue(issue, adw_id, logger)
        if error:
            logger.error(f"Error classifying issue: {error}")
            # Default to feature if classification fails
            issue_command = "/feature"
            logger.warning("Defaulting to /feature after classification error")
        else:
            # Save the classification for future use
            state.update(issue_class=issue_command)
            state.save("adw_build_iso")
    
    # Create commit message
    logger.info("Creating implementation commit")
    commit_msg, error = create_commit(AGENT_IMPLEMENTOR, issue, issue_command, adw_id, logger, worktree_path)
    
    if error:
        logger.error(f"Error creating commit message: {error}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error creating commit message: {error}")
        )
        sys.exit(1)
    
    # Commit the implementation (in worktree)
    success, error = commit_changes(commit_msg, cwd=worktree_path)
    
    if not success:
        logger.error(f"Error committing implementation: {error}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, f"❌ Error committing implementation: {error}")
        )
        sys.exit(1)
    
    logger.info(f"Committed implementation: {commit_msg}")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementation committed")
    )

    # TAC-13 LEARN: Actualizar expertise con patrones de build
    if expert_learn:
        logger.info("TAC-13: Learning from build execution")

        improve_response = improve_expert_knowledge(
            domain="adw",
            check_git_diff=True,
            focus_area="implementation_phase",
            adw_id=adw_id,
            logger=logger,
            working_dir=worktree_path
        )

        if improve_response.success:
            state.accumulate_tokens("adw_expert_improver", improve_response.token_usage)
            state.save("adw_build_iso")

    # Finalize git operations (push and PR)
    # Note: This will work from the worktree context
    finalize_git_operations(state, logger, cwd=worktree_path)
    
    logger.info("Isolated implementation phase completed successfully")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Isolated implementation phase completed")
    )
    
    # Save final state
    state.save("adw_build_iso")

    # Post final state summary with token usage to issue
    token_summary = state.get_token_summary()
    make_issue_comment(
        issue_number,
        f"{adw_id}_ops: 📋 Build phase completed\n\n{token_summary}"
    )


if __name__ == "__main__":
    main()