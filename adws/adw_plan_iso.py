#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic", "pyyaml", "claude-agent-sdk>=0.1.18"]
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
    consult_expert,
    improve_expert_knowledge,
    extract_file_references_from_issue,
    format_file_references_for_context,
    extract_issue_parameters,
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
                       help="Scout codebase before planning for better context (TAC)")
    parser.add_argument("--scout-scale", type=str, default="quick",
                       choices=["quick", "medium", "very_thorough"],
                       help="Scale of codebase exploration: quick (default), medium, or very_thorough (TAC)")
    parser.add_argument("--use-experts", action="store_true",
                       help="Enable TAC expert consultation (default: disabled)")
    parser.add_argument("--expert-learn", action="store_true",
                       help="Enable TAC self-improve after planning")

    args = parser.parse_args()

    issue_number = args.issue_number
    adw_id = args.adw_id
    skip_clarify = args.skip_clarify
    load_docs_topic = args.load_docs
    use_scout = args.scout
    scout_scale = args.scout_scale
    use_experts = args.use_experts
    expert_learn = args.expert_learn

    # Get repo information early to fetch issue details
    try:
        github_repo_url = get_repo_url()
        repo_path = extract_repo_path(github_repo_url)
    except ValueError as e:
        print(f"Error getting repository URL: {e}")
        sys.exit(1)

    # Fetch issue details to extract parameters from body
    issue: GitHubIssue = fetch_issue(issue_number, repo_path)

    # Extract parameters from issue body (e.g., /adw_id: feature_Tac_14_Task_5)
    issue_params = extract_issue_parameters(issue.body)

    # Use adw_id from issue body if provided, otherwise use command line arg
    if "adw_id" in issue_params and issue_params["adw_id"]:
        extracted_adw_id = issue_params["adw_id"]
        print(f"Found /adw_id in issue body: {extracted_adw_id}")
        if not adw_id:
            adw_id = extracted_adw_id
        elif adw_id != extracted_adw_id:
            print(f"Warning: Command line adw_id ({adw_id}) differs from issue body ({extracted_adw_id})")
            print(f"Using command line value: {adw_id}")

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

    logger.debug(f"Fetched issue: {issue.model_dump_json(indent=2, by_alias=True)}")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Starting isolated planning phase")
    )

    # CRITICAL: Create worktree FIRST, before any slow operations (docs loading, etc.)
    # This ensures isolation even if script is canceled during setup
    worktree_path = None
    valid, error = validate_worktree(adw_id, state)
    if valid:
        logger.info(f"Using existing worktree for {adw_id}")
        worktree_path = state.get("worktree_path")
        logger.info(f"Worktree path: {worktree_path}")
    else:
        logger.info(f"Worktree validation failed or missing: {error}")
        # Need to create worktree, but first need branch name
        # Check if we have a cached branch name
        cached_branch_name = state.get("branch_name")
        if cached_branch_name:
            logger.info(f"Using cached branch name: {cached_branch_name}")
            branch_name = cached_branch_name
        else:
            # Generate branch name early
            logger.info("Generating branch name...")
            from adw_modules.workflow_ops import classify_issue, generate_branch_name

            # Quick classification for branch naming
            issue_command, class_error = classify_issue(issue, adw_id, logger)
            if class_error:
                logger.error(f"Error classifying issue: {class_error}")
                issue_command = "/feature"  # Default to feature

            branch_name, gen_error = generate_branch_name(issue, issue_command, adw_id, logger)
            if gen_error:
                logger.error(f"Error generating branch name: {gen_error}")
                sys.exit(1)

            state.update(branch_name=branch_name, issue_class=issue_command)
            state.save("adw_plan_iso")
            logger.info(f"Generated branch name: {branch_name}")

        # Now create the worktree
        logger.info(f"Creating worktree for {adw_id} on branch {branch_name}")
        worktree_path, wt_error = create_worktree(adw_id, branch_name, logger)

        if wt_error:
            logger.error(f"Error creating worktree: {wt_error}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"❌ Error creating worktree: {wt_error}"),
            )
            sys.exit(1)

        state.update(worktree_path=worktree_path)
        state.save("adw_plan_iso")
        logger.info(f"Created worktree at {worktree_path}")

        # Run setup_worktree.sh
        logger.info("Setting up isolated environment via bash script")
        script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "scripts", "setup_worktree.sh"
        )
        result = subprocess.run(
            ["bash", script_path, worktree_path],
            capture_output=True,
            text=True,
            cwd=worktree_path
        )

        if result.returncode != 0:
            logger.error(f"Worktree setup failed: {result.stderr}")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", f"❌ Worktree setup failed: {result.stderr}"),
            )
            sys.exit(1)

        logger.info("Worktree setup completed")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"✅ Isolated worktree created: {worktree_path}"),
        )

    # Create context bundle for token optimization (avoid re-sending full issue to each phase)
    from adw_modules.workflow_ops import create_context_bundle, load_context_bundle
    bundle_created = create_context_bundle(adw_id, issue, logger)
    if bundle_created:
        logger.info("Context bundle created successfully")
        state.update(context_bundle_created=True)
        state.save("adw_plan_iso")

    # Load AI documentation if requested (TAC-9)
    # Token optimization: Limits configured in config.yml
    from adw_modules.workflow_ops import get_token_optimization_config
    token_config = get_token_optimization_config()
    MAX_DOCS_PLANNING = token_config["max_docs_planning"]
    MAX_SUMMARY_TOKENS_PLANNING = token_config["max_summary_tokens_planning"]

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
                # Includes section extraction based on issue context
                doc_content = docs_response.output
                summarized_content = summarize_doc_content(
                    doc_content,
                    topic,
                    adw_id,
                    logger,
                    max_summary_tokens=MAX_SUMMARY_TOKENS_PLANNING,
                    issue=issue  # Enable section extraction
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

    # Scout codebase if requested (TAC)
    if use_scout:
        logger.info(f"Scouting codebase with scale: {scout_scale}")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", f"🔍 Scouting codebase for context (scale: {scout_scale}) (TAC)"),
        )

        scout_response = scout_codebase(issue.body, adw_id, logger, scale=scout_scale)

        if scout_response.success:
            logger.info("Codebase scouting completed successfully")
            make_issue_comment(
                issue_number,
                format_issue_message(adw_id, "ops", "✅ Codebase scouting completed (TAC)"),
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

    # Classify the issue - skip if already cached in state (MOVED BEFORE clarification for better context)
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

    # TAC REUSE: Consultar expertise antes de clarificaciones (MOVED for better context)
    expert_guidance = None
    if use_experts and not skip_clarify:
        logger.info("TAC: Consulting ADW expert for planning guidance")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", "🧠 Consulting ADW expert (TAC)"),
        )

        expert_question = f"""Given this issue:
Title: {issue.title}
Type: {issue_command}
Body (truncated): {issue.body[:500]}...

What planning patterns should I apply from ADW expertise?
Focus on: state management, worktree isolation, GitHub integration patterns."""

        expert_response = consult_expert(
            domain="adw",
            question=expert_question,
            adw_id=adw_id,
            logger=logger,
            working_dir=worktree_path
        )

        if expert_response.success:
            expert_guidance = expert_response.output
            state.update(expert_planning_guidance=expert_response.output)
            state.accumulate_tokens("adw_expert", expert_response.token_usage)
            state.save("adw_plan_iso")
            logger.info("Expert guidance stored in state")

    # Clarification phase (optional) - NOW WITH MAXIMUM CONTEXT (docs + scout + classification + expert)
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
        logger.info("Starting clarification phase with full context (docs + scout + classification + expert)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, "ops", "🔍 Analyzing issue for ambiguities (with full context)..."),
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

            # Pass ai_docs context AND expert guidance if available to help with decision-making
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

    # Worktree is now ready (created earlier)
    # Get branch_name and issue_command from state (set during worktree creation)
    branch_name = state.get("branch_name")
    issue_command = state.get("issue_class")

    # Build the implementation plan (now executing in worktree)
    logger.info("Building implementation plan in worktree")
    make_issue_comment(
        issue_number,
        format_issue_message(adw_id, AGENT_PLANNER, "✅ Building implementation plan in isolated environment"),
    )

    # Use scout-enhanced planning if scouting was done (TAC)
    if state.get("scouting_results"):
        logger.info("Using scout-enhanced planning with /plan_w_scouters (TAC)")
        make_issue_comment(
            issue_number,
            format_issue_message(adw_id, AGENT_PLANNER, "🔍 Using scout-enhanced planning (TAC)"),
        )

        # Extract and load files referenced in issue body (e.g., plan_tasks_Tac_14.md)
        logger.info("Checking for file references in issue body...")
        file_references = extract_file_references_from_issue(issue, logger, working_dir=worktree_path)
        file_context = format_file_references_for_context(file_references)

        if file_references:
            make_issue_comment(
                issue_number,
                format_issue_message(
                    adw_id,
                    AGENT_PLANNER,
                    f"📎 Loaded {len(file_references)} referenced file(s): {', '.join(file_references.keys())}"
                ),
            )

        # plan_with_scouts takes just the description, not the full issue object
        plan_description = f"{issue.title}\n\n{issue.body}"
        if clarification_text:
            plan_description += f"\n\n{clarification_text}"
        if file_context:
            plan_description += file_context

        plan_response = plan_with_scouts(plan_description, adw_id, logger, working_dir=worktree_path, ai_docs_context=ai_docs_context)
    else:
        # Extract and load files referenced in issue body (e.g., plan_tasks_Tac_14.md)
        logger.info("Checking for file references in issue body...")
        file_references = extract_file_references_from_issue(issue, logger, working_dir=worktree_path)
        file_context = format_file_references_for_context(file_references)

        if file_references:
            make_issue_comment(
                issue_number,
                format_issue_message(
                    adw_id,
                    AGENT_PLANNER,
                    f"📎 Loaded {len(file_references)} referenced file(s): {', '.join(file_references.keys())}"
                ),
            )

        # Add file references to ai_docs_context
        if file_context:
            ai_docs_context = (ai_docs_context or "") + file_context

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

    # Update context bundle with planning decisions
    from adw_modules.workflow_ops import update_context_bundle_decisions
    planning_decisions = f"""- Plan file: {plan_file_path}
- Issue classified as: {issue_command}
- Branch: {branch_name}
- Worktree: {worktree_path}"""
    if clarification_text:
        planning_decisions += f"\n- Clarifications resolved"
    if ai_docs_context:
        planning_decisions += f"\n- Documentation loaded: {load_docs_topic}"

    update_context_bundle_decisions(adw_id, "Planning", planning_decisions, logger)

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

    # TAC Optimization: Learning phase moved to document phase (final validation)
    # Individual phases only consult experts, learning happens once at the end

    # Finalize git operations (push and PR)
    # Note: This will work from the worktree context
    finalize_git_operations(state, logger, cwd=worktree_path)

    logger.info("Isolated planning phase completed successfully")
    make_issue_comment(
        issue_number, format_issue_message(adw_id, "ops", "✅ Isolated planning phase completed")
    )

    # Save final state
    state.save("adw_plan_iso")

    # Token summary moved to final workflow completion (adw_sdlc_iso.py)


if __name__ == "__main__":
    main()