#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Plan Iso - AI Developer Workflow for agentic planning in isolated worktrees

Usage:
  uv run adw_plan_iso.py <issue-number> [adw-id] [--load-docs TOPIC] [--skip-clarify]

Options:
  --load-docs TOPIC   Load AI documentation for topic before planning (TAC-9)
  --skip-clarify      Skip clarification phase

Workflow:
1. Fetch GitHub issue details
2. (Optional) Load AI documentation for relevant topics
3. Check/create worktree for isolated execution
4. Classify issue type (/chore, /bug, /feature)
5. Create feature branch in worktree
6. Generate implementation plan in worktree
7. Commit plan in worktree
8. Push and create/update PR

This workflow creates an isolated git worktree under trees/<adw_id>/ for
parallel execution without interference.
"""

import subprocess
import sys
import os
import logging
import json
from typing import Optional
from dotenv import load_dotenv

from adw_modules.state import ADWState
from adw_modules.git_ops import commit_changes, finalize_git_operations
from adw_modules.github import (
    fetch_issue,
    make_issue_comment,
    get_repo_url,
    extract_repo_path,
)
from adw_modules.workflow_ops import (
    classify_issue,
    clarify_issue,
    build_plan,
    generate_branch_name,
    create_commit,
    format_issue_message,
    ensure_adw_id,
    load_ai_docs,
    summarize_doc_content,
    scout_codebase,
    plan_with_scouts,
    AGENT_PLANNER,
)
from adw_modules.utils import setup_logger, check_env_vars
from adw_modules.data_types import GitHubIssue, IssueClassSlashCommand
from adw_modules.worktree_ops import (
    create_worktree,
    validate_worktree,
)




def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line args
    import argparse
    parser = argparse.ArgumentParser(description="ADW Plan Iso - Agentic planning in isolated worktrees")
    parser.add_argument("issue_number", help="GitHub issue number")
    parser.add_argument("adw_id", nargs="?", default=None, help="ADW ID (optional, will be generated if not provided)")
    parser.add_argument("--skip-clarify", action="store_true", help="Skip clarification phase")
    parser.add_argument("--load-docs", type=str, default=None,
                       help="Load AI documentation for topic before planning (TAC-9)")
    parser.add_argument("--scout", action="store_true",
                       help="Scout codebase before planning for better context (TAC-12)")
    parser.add_argument("--scout-scale", type=str, default="medium",
                       choices=["quick", "medium", "very_thorough"],
                       help="Scale of codebase exploration: quick, medium, or very_thorough (TAC-12)")

    args = parser.parse_args()

    issue_number = args.issue_number
    adw_id = args.adw_id
    skip_clarify = args.skip_clarify
    load_docs_topic = args.load_docs
    use_scout = args.scout
    scout_scale = args.scout_scale

    # Ensure ADW ID exists with initialized state
    temp_logger = setup_logger(adw_id, "adw_plan_iso") if adw_id else None
    adw_id = ensure_adw_id(issue_number, adw_id, temp_logger)

    # Load the state that was created/found by ensure_adw_id
    state = ADWState.load(adw_id, temp_logger)

    # Ensure state has the adw_id field
    if not state.get("adw_id"):
        state.update(adw_id=adw_id)
    
    # Track that this ADW workflow has run
    state.append_adw_id("adw_plan_iso")

    # Set up logger with ADW ID
    logger = setup_logger(adw_id, "adw_plan_iso")
    logger.info(f"ADW Plan Iso starting - ID: {adw_id}, Issue: {issue_number}")

    # Validate environment
    check_env_vars(logger)

    # Get repo information
    try:
        github_repo_url = get_repo_url()
        repo_path = extract_repo_path(github_repo_url)
    except ValueError as e:
        logger.error(f"Error getting repository URL: {e}")
        sys.exit(1)

    # Check if worktree already exists
    valid, error = validate_worktree(adw_id, state)
    if valid:
        logger.info(f"Using existing worktree for {adw_id}")
        worktree_path = state.get("worktree_path")

    # Fetch issue details
    issue: GitHubIssue = fetch_issue(issue_number, repo_path)

    logger.debug(f"Fetched issue: {issue.model_dump_json(indent=2, by_alias=True)}")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Starting isolated planning phase")
    )

    make_issue_comment(
        issue_number,
        f"{adw_id}_ops: 🔍 Using state\n```json\n{json.dumps(state.data, indent=2)}\n```",
    )

    # Load AI documentation if requested (TAC-9)
    # Token optimization: Planning phase uses max 3 docs with 300 token summaries
    MAX_DOCS_PLANNING = 3
    MAX_SUMMARY_TOKENS_PLANNING = 300

    ai_docs_context = None
    if load_docs_topic:
        # Support multiple topics separated by comma (TAC-9 hybrid)
        topics = [t.strip() for t in load_docs_topic.split(",")]

        # Phase-aware doc limit (TAC-9 optimization)
        if len(topics) > MAX_DOCS_PLANNING:
            logger.info(f"Limiting docs for planning phase: {len(topics)} → {MAX_DOCS_PLANNING}")
            topics = topics[:MAX_DOCS_PLANNING]

        logger.info(f"Loading AI documentation for {len(topics)} topic(s): {', '.join(topics)}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"📚 Loading AI documentation: {', '.join(topics)} (TAC-9 optimized)"),
        )

        # Load each topic and concatenate results
        all_docs = []
        loaded_topics = []
        failed_topics = []

        for topic in topics:
            logger.info(f"Loading documentation topic: {topic}")
            docs_response = load_ai_docs(topic, adw_id, logger)

            if docs_response.success:
                # Summarize documentation content for token optimization (TAC-9)
                doc_content = docs_response.output
                summarized_content = summarize_doc_content(
                    doc_content,
                    topic,
                    adw_id,
                    logger,
                    max_summary_tokens=MAX_SUMMARY_TOKENS_PLANNING
                )

                all_docs.append(f"# Documentation: {topic}\n\n{summarized_content}")
                loaded_topics.append(topic)
                logger.info(f"Successfully loaded: {topic}")
            else:
                failed_topics.append(topic)
                logger.warning(f"Failed to load topic '{topic}': {docs_response.output}")

        # Combine all loaded documentation
        if all_docs:
            ai_docs_context = "\n\n---\n\n".join(all_docs)
            logger.info(f"Successfully loaded {len(loaded_topics)} of {len(topics)} topics")

            status_msg = f"✅ AI documentation loaded ({len(loaded_topics)}/{len(topics)} topics)"
            if failed_topics:
                status_msg += f"\n⚠️  Failed to load: {', '.join(failed_topics)}"

            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", status_msg),
            )
            state.update(loaded_docs_topic=load_docs_topic, ai_docs_context=ai_docs_context)
            state.save("adw_plan_iso")
        else:
            logger.warning(f"Failed to load any AI docs (continuing anyway)")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"⚠️  Failed to load documentation topics: {', '.join(failed_topics)}"),
            )
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"⚠️ AI docs loading failed (continuing): {docs_response.output[:200]}"),
            )

    # Scout codebase if requested (TAC-12)
    if use_scout:
        logger.info(f"Scouting codebase with scale: {scout_scale}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"🔍 Scouting codebase for context (scale: {scout_scale}) (TAC-12)"),
        )

        scout_response = scout_codebase(issue.body, adw_id, logger, scale=scout_scale)

        if scout_response.success:
            logger.info("Codebase scouting completed successfully")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", "✅ Codebase scouting completed (TAC-12)"),
            )
            state.update(scouting_results=scout_response.output, scout_scale=scout_scale)
            state.accumulate_tokens("scout", scout_response.token_usage)
            state.save("adw_plan_iso")
        else:
            logger.warning(f"Scouting failed (continuing anyway): {scout_response.output}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"⚠️ Scouting failed (continuing): {scout_response.output[:200]}"),
            )

    # Clarification phase (optional) - skip if already cached in state
    clarification_text = None
    cached_clarification = state.get("clarification")
    if cached_clarification and not skip_clarify:
        logger.info("Using cached clarification from state (saving tokens)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", "♻️ Using cached clarification (token optimization)"),
        )
        # Reconstruct clarification text from cached data
        if cached_clarification.get("has_ambiguities"):
            clarification_text = "## Cached Clarifications\n\n"
            for a in cached_clarification.get("assumptions", []):
                clarification_text += f"- {a}\n"
        skip_clarify = True  # Skip API call since we have cached data

    if not skip_clarify:
        logger.info("Starting clarification phase")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", "🔍 Analyzing issue for ambiguities..."),
        )

        clarification_response, clarify_error = clarify_issue(issue, adw_id, logger, working_dir=None)

        if clarify_error:
            logger.warning(f"Clarification analysis failed: {clarify_error}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"⚠️ Clarification analysis failed (continuing anyway): {clarify_error}"),
            )
        elif clarification_response and clarification_response.has_ambiguities:
            logger.info(f"Found {len(clarification_response.questions)} ambiguities")

            # Format questions in markdown
            questions_md = "## 🤔 Clarification Needed\n\n"
            questions_md += f"**Analysis:** {clarification_response.analysis}\n\n"
            questions_md += "### Questions:\n\n"

            for i, q in enumerate(clarification_response.questions, 1):
                severity_emoji = {"critical": "🔴", "important": "🟡", "nice_to_have": "🟢"}
                emoji = severity_emoji.get(q.severity, "⚪")
                questions_md += f"{i}. {emoji} **[{q.category}]** {q.question}\n"

            if clarification_response.assumptions:
                questions_md += "\n### Assumptions (if proceeding without answers):\n\n"
                for assumption in clarification_response.assumptions:
                    questions_md += f"- {assumption}\n"

            # Post questions to issue
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", questions_md),
            )

            # Save clarification to state
            state.update(
                clarification=clarification_response.model_dump(),
                awaiting_clarification=False,
            )
            state.save("adw_plan_iso")

            # Auto-resolve clarifications instead of pausing
            from adw_modules.workflow_ops import resolve_clarifications

            # Pass ai_docs context if available to help with decision-making
            resolved_text, resolve_error = resolve_clarifications(
                issue, clarification_response, adw_id, logger, working_dir=None,
                ai_docs_context=ai_docs_context
            )

            if resolve_error:
                logger.warning(f"Auto-resolution failed: {resolve_error}")
                make_issue_comment(
                    issue_number,
                    format_issue_message(adw_id, "ops",
                        f"⚠️ Auto-resolution failed, using assumptions: {resolve_error}"),
                )
                clarification_text = f"## Assumptions\n\n" + "\n".join([
                    f"- {a}" for a in clarification_response.assumptions
                ])
            else:
                clarification_text = resolved_text
                make_issue_comment(
                    issue_number,
                    format_issue_message(adw_id, "ops",
                        "🤖 Auto-resolved clarifications:\n\n" + resolved_text),
                )

            logger.info("Continuing with auto-resolved decisions")
        else:
            logger.info("No ambiguities detected - issue is sufficiently clear")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", "✅ No ambiguities detected - proceeding with planning"),
            )

    # Classify the issue - skip if already cached in state
    cached_issue_class = state.get("issue_class")
    if cached_issue_class:
        logger.info(f"Using cached classification from state: {cached_issue_class} (saving tokens)")
        issue_command = cached_issue_class
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"♻️ Using cached classification: {issue_command} (token optimization)"),
        )
    else:
        issue_command, error = classify_issue(issue, adw_id, logger)

        if error:
            logger.error(f"Error classifying issue: {error}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"❌ Error classifying issue: {error}"),
            )
            sys.exit(1)

        state.update(issue_class=issue_command)
        state.save("adw_plan_iso")
        logger.info(f"Issue classified as: {issue_command}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"✅ Issue classified as: {issue_command}"),
        )

    # Generate branch name - skip if already cached in state
    cached_branch_name = state.get("branch_name")
    if cached_branch_name:
        logger.info(f"Using cached branch name from state: {cached_branch_name} (saving tokens)")
        branch_name = cached_branch_name
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"♻️ Using cached branch: {branch_name} (token optimization)"),
        )
    else:
        branch_name, error = generate_branch_name(issue, issue_command, adw_id, logger)

        if error:
            logger.error(f"Error generating branch name: {error}")
            make_issue_comment(
                issue_number,
                format_issue_message(
                    adw_id, "ops", f"❌ Error generating branch name: {error}"
                ),
            )
            sys.exit(1)

    # Don't create branch here - let worktree create it
    # The worktree command will create the branch when we specify -b
    state.update(branch_name=branch_name)
    state.save("adw_plan_iso")
    logger.info(f"Will create branch in worktree: {branch_name}")

    # Create worktree if it doesn't exist
    if not valid:
        logger.info(f"Creating worktree for {adw_id}")
        worktree_path, error = create_worktree(adw_id, branch_name, logger)
        
        if error:
            logger.error(f"Error creating worktree: {error}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"❌ Error creating worktree: {error}"),
            )
            sys.exit(1)
        
        state.update(worktree_path=worktree_path)
        state.save("adw_plan_iso")
        logger.info(f"Created worktree at {worktree_path}")

        # Run setup_worktree.sh directly (no API call needed - avoids rate limiting/hanging)
        logger.info("Setting up isolated environment via bash script")
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "setup_worktree.sh"
        )
        result = subprocess.run(
            ["bash", script_path, worktree_path],
            capture_output=True,
            text=True,
            timeout=120,  # 2 min max for file ops + dependency install
        )
        if result.returncode != 0:
            error_msg = result.stderr.strip() or result.stdout.strip() or "Unknown error"
            logger.error(f"Error setting up worktree: {error_msg}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"❌ Error setting up worktree: {error_msg}"),
            )
            sys.exit(1)

        logger.info(f"Worktree environment setup complete: {result.stdout.strip()}")

    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, "ops", f"✅ Working in isolated worktree: {worktree_path}"),
    )

    # Build the implementation plan (now executing in worktree)
    logger.info("Building implementation plan in worktree")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_PLANNER, "✅ Building implementation plan in isolated environment"),
    )

    # Use scout-enhanced planning if scouting was done (TAC-12)
    if state.get("scouting_results"):
        logger.info("Using scout-enhanced planning with /plan_w_scouters (TAC-12)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_PLANNER, "🔍 Using scout-enhanced planning (TAC-12)"),
        )
        # plan_with_scouts takes just the description, not the full issue object
        plan_description = f"{issue.title}\n\n{issue.body}"
        if clarification_text:
            plan_description += f"\n\n{clarification_text}"
        plan_response = plan_with_scouts(plan_description, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    else:
        plan_response = build_plan(issue, issue_command, adw_id, logger, working_dir=worktree_path, clarifications=clarification_text, ai_docs_context=ai_docs_context)

    # Track token usage from planning
    state.accumulate_tokens(AGENT_PLANNER, plan_response.token_usage)
    state.save("adw_plan_iso")

    if not plan_response.success:
        logger.error(f"Error building plan: {plan_response.output}")
        make_issue_comment(
            issue_number,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error building plan: {plan_response.output}"
            ),
        )
        sys.exit(1)

    logger.debug(f"Plan response: {plan_response.output}")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_PLANNER, "✅ Implementation plan created"),
    )

    # Get the plan file path directly from response
    logger.info("Getting plan file path")
    plan_file_path = plan_response.output.strip()
    
    # Validate the path exists (within worktree)
    if not plan_file_path:
        error = "No plan file path returned from planning agent"
        logger.error(error)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ {error}"),
        )
        sys.exit(1)
    
    # Check if file exists in worktree
    worktree_plan_path = os.path.join(worktree_path, plan_file_path)
    if not os.path.exists(worktree_plan_path):
        error = f"Plan file does not exist in worktree: {plan_file_path}"
        logger.error(error)
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"❌ {error}"),
        )
        sys.exit(1)

    state.update(plan_file=plan_file_path)
    state.save("adw_plan_iso")
    logger.info(f"Plan file created: {plan_file_path}")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, "ops", f"✅ Plan file created: {plan_file_path}"),
    )

    # Create commit message
    logger.info("Creating plan commit")
    commit_msg, error = create_commit(
        AGENT_PLANNER, issue, issue_command, adw_id, logger, worktree_path
    )

    if error:
        logger.error(f"Error creating commit message: {error}")
        make_issue_comment(
            issue_number,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error creating commit message: {error}"
            ),
        )
        sys.exit(1)

    # Commit the plan (in worktree)
    success, error = commit_changes(commit_msg, cwd=worktree_path)

    if not success:
        logger.error(f"Error committing plan: {error}")
        make_issue_comment(
            issue_number,
            format_issue_message(
                adw_id, AGENT_PLANNER, f"❌ Error committing plan: {error}"
            ),
        )
        sys.exit(1)

    logger.info(f"Committed plan: {commit_msg}")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, AGENT_PLANNER, "✅ Plan committed")
    )

    # Finalize git operations (push and PR)
    # Note: This will work from the worktree context
    finalize_git_operations(state, logger, cwd=worktree_path)

    logger.info("Isolated planning phase completed successfully")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Isolated planning phase completed")
    )

    # Save final state
    state.save("adw_plan_iso")

    # Post final state summary with token usage to issue
    token_summary = state.get_token_summary()
    make_issue_comment(
        issue_number,
        f"{adw_id}_ops: 📋 Planning phase completed\n\n{token_summary}"
    )


if __name__ == "__main__":
    main()