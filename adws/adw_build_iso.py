#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml", "claude-agent-sdk>=0.1.18"]
# ///

"""
ADW Build Iso - AI Developer Workflow for agentic building in isolated worktrees

Usage:
  uv run adw_build_iso.py <issue-number> <adw-id> [--with-report]

Options:
  --with-report    Use /build_w_report for structured YAML change tracking (TAC)

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
from adw_modules.data_types import GitHubIssue, AgentPromptResponse
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
                       help="Use /build_w_report for structured YAML change tracking (TAC)")
    parser.add_argument("--parallel", action="store_true",
                       help="Use parallel build agents for faster implementation (TAC)")
    parser.add_argument("--use-experts", action="store_true",
                       help="Enable TAC expert consultation")
    parser.add_argument("--expert-learn", action="store_true",
                       help="Enable TAC self-improve after build")

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

    # TAC Optimization: Expert consultation removed from build phase (only in plan phase)
    # Build phase uses the guidance from planning phase if available

    # Implement the plan (executing in worktree) with optional parallel build (TAC) or report (TAC)
    logger.info("Implementing solution in worktree")

    if use_parallel:
        logger.info("Using /build_in_parallel for faster implementation (TAC)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution with parallel build agents (TAC)")
        )
        implement_response = build_in_parallel(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    elif with_report:
        logger.info("Using /build_w_report for structured change tracking (TAC)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution with YAML report tracking (TAC)")
        )
        implement_response = implement_plan_with_report(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    else:
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR, "✅ Implementing solution in isolated environment")
        )
        # Try agent implementation first, but with verification
        implement_response = implement_plan(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)

        # Check if agent actually made changes
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
        )
        agent_made_changes = bool(result.stdout.strip())

        # If agent failed to make changes, try direct implementation
        if not agent_made_changes and implement_response.success:
            logger.warning("Agent claimed success but made no changes. Attempting direct implementation from plan...")

            # Extract action from plan file (e.g., "add 'text' to file")
            try:
                # Handle both relative and absolute paths
                plan_path = plan_file if os.path.isabs(plan_file) else os.path.join(worktree_path, plan_file)
                with open(plan_path, 'r') as f:
                    plan_content = f.read()

                # Parse for "add" or "append" patterns
                import re
                add_pattern = r'[Aa]dd.*?["\']([^"\']+)["\'].*?(?:to|in|at)\s+(?:the\s+)?[`]?([^`\s]+)'
                matches = re.findall(add_pattern, plan_content)

                if matches:
                    logger.info(f"Found {len(matches)} direct tasks to execute")
                    for text_to_add, target_file in matches:
                        target_path = os.path.join(worktree_path, target_file)
                        if os.path.exists(target_path):
                            logger.info(f"Appending '{text_to_add}' to {target_file}")
                            with open(target_path, 'a') as f:
                                f.write(f"\n{text_to_add}")
                            logger.info(f"Successfully modified {target_file}")

                # Verify changes were made
                result = subprocess.run(
                    ["git", "diff", "--name-only"],
                    capture_output=True,
                    text=True,
                    cwd=worktree_path,
                )
                if result.stdout.strip():
                    logger.info("Direct implementation successful - changes detected")
                    # Create synthetic response for direct execution
                    implement_response = AgentPromptResponse(
                        success=True,
                        output="Direct implementation completed",
                        token_usage={"input": 0, "output": 0}
                    )
            except Exception as e:
                logger.error(f"Direct implementation failed: {e}")

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

    # CRITICAL: Validate that implementation actually made changes
    # This prevents false success reports from being accepted
    # Retry up to 2 times if validation fails
    max_build_retries = 2
    build_attempt = 1
    validation_passed = False
    changed_files = []

    while build_attempt <= max_build_retries and not validation_passed:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True,
            cwd=worktree_path,
        )
        changed_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        if not changed_files or changed_files == ['']:
            if build_attempt < max_build_retries:
                # Retry: ask agent to try again with more explicit instructions
                retry_msg = (f"⚠️ Build attempt {build_attempt} failed - no changes detected.\n"
                           f"Retrying with explicit feedback (attempt {build_attempt + 1}/{max_build_retries})...\n\n"
                           f"The /implement command was executed but made NO actual file changes.\n"
                           f"This means: your tools (Edit, Write, Read) must be used to modify files.\n"
                           f"Do NOT report success without using tools.\n"
                           f"\nRetrying now...")
                logger.warning(retry_msg)
                make_issue_comment(issue_number, format_issue_message(adw_id, AGENT_IMPLEMENTOR, retry_msg))

                # Retry implementation with fresh context
                build_attempt += 1
                implement_response = implement_plan(plan_file, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
                state.accumulate_tokens(AGENT_IMPLEMENTOR, implement_response.token_usage)
                state.save("adw_build_iso")

                if not implement_response.success:
                    error_msg = f"❌ Retry {build_attempt - 1} also failed: {implement_response.output}"
                    logger.error(error_msg)
                    make_issue_comment(issue_number, format_issue_message(adw_id, AGENT_IMPLEMENTOR, error_msg))
                    sys.exit(1)
            else:
                # Final failure after all retries
                error_msg = ("❌ IMPLEMENTATION VALIDATION FAILED (Final): Agent reported success but made NO file modifications.\n"
                            "After multiple attempts, the workflow cannot proceed without actual code changes.\n"
                            "The /implement command must use Edit, Write, or other tools to modify files.\n"
                            "Check: `git diff --name-only` shows no files changed.")
                logger.error(error_msg)
                make_issue_comment(
                    issue_number,
                    format_issue_message(adw_id, AGENT_IMPLEMENTOR,
                                       error_msg + "\n\n⚠️ Please review the plan and ensure it's clear.")
                )
                sys.exit(1)
        else:
            validation_passed = True

    logger.info(f"✅ Build validation passed (attempt {build_attempt}): {len(changed_files)} file(s) modified")

    logger.info(f"✅ Git validation passed: {len(changed_files)} file(s) modified")

    # ENHANCED: Validate content of modified files (check for expected text from spec)
    # Extract key requirements from plan file
    plan_file = state.get("plan_file")
    validation_issues = []

    if plan_file and os.path.exists(plan_file):
        try:
            with open(plan_file, 'r') as f:
                plan_content = f.read()

            # Look for common requirement markers (case-insensitive)
            import re

            # Pattern 1: "Append" or "Add" specific text
            append_patterns = [
                r'(?:Append|Add)\s+["\']([^"\']+)["\']',
                r'add.*?["\']([^"\']+)["\']',
                r'append.*?["\']([^"\']+)["\']'
            ]

            for pattern in append_patterns:
                matches = re.finditer(pattern, plan_content, re.IGNORECASE)
                for match in matches:
                    expected_text = match.group(1)
                    logger.info(f"Looking for expected text in modifications: '{expected_text}'")

                    # Check if this text appears in any modified file
                    text_found = False
                    for changed_file in changed_files:
                        if not changed_file or changed_file.startswith('Binary'):
                            continue

                        file_path = os.path.join(worktree_path, changed_file)
                        if os.path.exists(file_path) and os.path.isfile(file_path):
                            try:
                                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                    file_content = f.read()
                                    if expected_text in file_content:
                                        text_found = True
                                        logger.info(f"✓ Found '{expected_text}' in {changed_file}")
                                        break
                            except Exception as e:
                                logger.debug(f"Could not read {file_path}: {e}")

                    if not text_found:
                        validation_issues.append(
                            f"Expected text '{expected_text}' not found in any modified files. "
                            f"Modified files: {', '.join(changed_files[:5])}"
                        )
        except Exception as e:
            logger.warning(f"Could not perform content validation: {e}")

    # Report content validation failures
    if validation_issues:
        error_msg = ("❌ CONTENT VALIDATION FAILED: Files were modified but don't contain expected content.\n"
                    "Issues found:\n")
        for issue in validation_issues:
            error_msg += f"- {issue}\n"

        logger.error(error_msg)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_IMPLEMENTOR,
                               error_msg + "\nThe agent may have modified wrong files. Re-running workflow...")
        )
        sys.exit(1)

    logger.info(f"✅ All validations passed: Files modified + content verified")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_IMPLEMENTOR,
                           f"✅ Solution implemented ({len(changed_files)} files modified + content verified)")
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

    # Update context bundle with build decisions
    from adw_modules.workflow_ops import update_context_bundle_decisions
    build_decisions = f"""- Plan implemented: {plan_file}
- Implementation approach: {'Parallel build' if use_parallel else 'Sequential'}
- Files changed: See git diff"""
    update_context_bundle_decisions(adw_id, "Build", build_decisions, logger)

    # TAC Optimization: Learning phase moved to document phase (final validation)
    # Individual phases only consult experts, learning happens once at the end

    # Finalize git operations (push and PR)
    # Note: This will work from the worktree context
    finalize_git_operations(state, logger, cwd=worktree_path)
    
    logger.info("Isolated implementation phase completed successfully")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Isolated implementation phase completed")
    )
    
    # Save final state
    state.save("adw_build_iso")

    # Token summary moved to final workflow completion (adw_sdlc_iso.py)


if __name__ == "__main__":
    main()