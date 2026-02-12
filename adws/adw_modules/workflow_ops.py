"""Shared AI Developer Workflow (ADW) operations."""

import glob
import json
import logging
import os
import subprocess
import re
import yaml
from typing import Tuple, Optional, Dict, Any
from adw_modules.data_types import (
    AgentTemplateRequest,
    GitHubIssue,
    AgentPromptResponse,
    IssueClassSlashCommand,
    ADWExtractionResult,
    ClarificationQuestion,
    ClarificationResponse,
)
from adw_modules.agent import execute_template
from adw_modules.github import get_repo_url, extract_repo_path, ADW_BOT_IDENTIFIER
from adw_modules.state import ADWState
from adw_modules.utils import parse_json, get_target_branch, strip_code_fences

# ============================================================================
# Configuration Loading
# ============================================================================

_CONFIG_CACHE: Optional[Dict[str, Any]] = None


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yml file.

    Caches the configuration in memory for performance.

    Returns:
        Dictionary with configuration values
    """
    global _CONFIG_CACHE

    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    # Find config.yml in project root
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config.yml"
    )

    if not os.path.exists(config_path):
        # Fallback to defaults if config not found
        return {
            "agentic": {
                "token_optimization": {
                    "max_issue_body_length": 2000,
                    "max_file_reference_size": 5000,
                    "max_clarification_length": 1000,
                    "max_docs_planning": 2,
                    "max_summary_tokens_planning": 200,
                    "max_file_references": 3,
                    "max_screenshots": 3,
                }
            }
        }

    with open(config_path, 'r', encoding='utf-8') as f:
        _CONFIG_CACHE = yaml.safe_load(f)

    return _CONFIG_CACHE


def get_token_optimization_config() -> Dict[str, int]:
    """Get token optimization configuration values.

    Returns:
        Dictionary with token optimization settings
    """
    config = load_config()
    defaults = {
        "max_issue_body_length": 2000,
        "max_file_reference_size": 5000,
        "max_clarification_length": 1000,
        "max_docs_planning": 2,
        "max_summary_tokens_planning": 200,
        "max_file_references": 3,
        "max_screenshots": 3,
    }

    token_opt = config.get("agentic", {}).get("token_optimization", {})

    # Merge with defaults
    return {**defaults, **token_opt}


# Token optimization constants - loaded from config.yml
_token_config = get_token_optimization_config()
MAX_ISSUE_BODY_LENGTH = _token_config["max_issue_body_length"]
MAX_FILE_REFERENCE_SIZE = _token_config["max_file_reference_size"]
MAX_CLARIFICATION_LENGTH = _token_config["max_clarification_length"]


# Agent name constants
AGENT_PLANNER = "sdlc_planner"
AGENT_IMPLEMENTOR = "sdlc_implementor"
AGENT_CLASSIFIER = "issue_classifier"
AGENT_BRANCH_GENERATOR = "branch_generator"
AGENT_PR_CREATOR = "pr_creator"

# Available ADW workflows for runtime validation
AVAILABLE_ADW_WORKFLOWS = [
    # Isolated workflows (all workflows are now iso-based)
    "adw_plan_iso",
    "adw_patch_iso",
    "adw_build_iso",
    "adw_test_iso",
    "adw_review_iso",
    "adw_document_iso",
    "adw_ship_iso",
    "adw_sdlc_zte_iso",  # Zero Touch Execution workflow
    "adw_plan_build_iso",
    "adw_plan_build_test_iso",
    "adw_plan_build_test_review_iso",
    "adw_plan_build_document_iso",
    "adw_plan_build_review_iso",
    "adw_sdlc_iso",
]


def get_model_id(model_type: str) -> str:
    """Get fully qualified model ID with 3-tier resolution.

    Resolution order:
    1. Environment variable (ANTHROPIC_DEFAULT_{TYPE}_MODEL)
    2. Config file (config.yml: agentic.model_policy.{type}_model)
    3. Hardcoded default

    Args:
        model_type: One of "opus", "sonnet", or "haiku"

    Returns:
        Fully qualified model ID string
    """
    # Tier 1: Environment variable
    env_var = f"ANTHROPIC_DEFAULT_{model_type.upper()}_MODEL"
    env_value = os.getenv(env_var)
    if env_value:
        return env_value

    # Tier 2: Config file
    config = load_config()
    model_policy = config.get("agentic", {}).get("model_policy", {})
    config_value = model_policy.get(f"{model_type}_model")
    if config_value and not (isinstance(config_value, str) and config_value.startswith("${")):
        return config_value

    # Tier 3: Hardcoded defaults
    defaults = {
        "opus": "claude-opus-4-5-20251101",
        "sonnet": "claude-sonnet-4-5-20250929",
        "haiku": "claude-haiku-4-5-20251001",
    }
    return defaults.get(model_type, "claude-sonnet-4-5-20250929")


def format_issue_message(
    adw_id: str, agent_name: str, message: str, session_id: Optional[str] = None
) -> str:
    """Format a message for issue comments with ADW tracking and bot identifier."""
    # Always include ADW_BOT_IDENTIFIER to prevent webhook loops
    if session_id:
        return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}_{session_id}: {message}"
    return f"{ADW_BOT_IDENTIFIER} {adw_id}_{agent_name}: {message}"


def get_minimal_issue_json(issue: GitHubIssue, max_body_length: int = MAX_ISSUE_BODY_LENGTH) -> str:
    """Create minimal issue JSON with truncated body to reduce token usage.

    Args:
        issue: GitHubIssue object
        max_body_length: Maximum length for body text (default 2000 chars)

    Returns:
        JSON string with only number, title, and truncated body
    """
    body = issue.body or ""
    if len(body) > max_body_length:
        body = body[:max_body_length] + "\n\n[TRUNCATED - body exceeds 2000 chars]"

    minimal_data = {
        "number": issue.number,
        "title": issue.title,
        "body": body
    }
    return json.dumps(minimal_data)


def extract_adw_info(text: str, temp_adw_id: str) -> ADWExtractionResult:
    """Extract ADW workflow, ID, and model_set from text using classify_adw agent.
    Returns ADWExtractionResult with workflow_command, adw_id, and model_set."""

    # Use classify_adw to extract structured info
    request = AgentTemplateRequest(
        agent_name="adw_classifier",
        slash_command="/classify_adw",
        args=[text],
        adw_id=temp_adw_id,
    )

    try:
        response = execute_template(request)  # No logger available in this function

        if not response.success:
            print(f"Failed to classify ADW: {response.output}")
            return ADWExtractionResult()  # Empty result

        # Parse JSON response using utility that handles markdown
        try:
            data = parse_json(response.output, dict)
            adw_command = data.get("adw_slash_command", "").replace(
                "/", ""
            )  # Remove slash
            adw_id = data.get("adw_id")
            model_set = data.get("model_set", "base")  # Default to "base"

            # Validate command
            if adw_command and adw_command in AVAILABLE_ADW_WORKFLOWS:
                return ADWExtractionResult(
                    workflow_command=adw_command,
                    adw_id=adw_id,
                    model_set=model_set
                )

            return ADWExtractionResult()  # Empty result

        except ValueError as e:
            print(f"Failed to parse classify_adw response: {e}")
            return ADWExtractionResult()  # Empty result

    except Exception as e:
        print(f"Error calling classify_adw: {e}")
        return ADWExtractionResult()  # Empty result


def classify_issue(
    issue: GitHubIssue,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[IssueClassSlashCommand], Optional[str]]:
    """Classify GitHub issue and return appropriate slash command.
    Returns (command, error_message) tuple."""

    # Use the classify_issue slash command template with minimal payload
    # Only include the essential fields: number, title, body
    minimal_issue_json = get_minimal_issue_json(issue)

    request = AgentTemplateRequest(
        agent_name=AGENT_CLASSIFIER,
        slash_command="/classify_issue",
        args=[minimal_issue_json],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(f"Classifying issue: {issue.title}")

    response = execute_template(request)

    logger.debug(
        f"Classification response: {response.model_dump_json(indent=2, by_alias=True)}"
    )

    if not response.success:
        return None, response.output

    # Extract the classification from the response
    output = response.output.strip()

    # Look for the classification pattern in the output
    # Claude might add explanation, so we need to extract just the command
    classification_match = re.search(r"(/chore|/bug|/feature|0)", output)

    if classification_match:
        issue_command = classification_match.group(1)
    else:
        issue_command = output

    if issue_command == "0":
        return None, f"No command selected: {response.output}"

    if issue_command not in ["/chore", "/bug", "/feature"]:
        return None, f"Invalid command selected: {response.output}"

    return issue_command, None  # type: ignore


def clarify_issue(
    issue: GitHubIssue,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[ClarificationResponse], Optional[str]]:
    """Analyze GitHub issue for ambiguities and generate clarification questions.
    Returns (ClarificationResponse, error_message) tuple."""

    logger.info("Analyzing issue for ambiguities...")

    # Construct the analysis prompt
    prompt = f"""You are an expert software requirements analyst. Analyze the following GitHub issue and identify any ambiguities, missing information, or unclear decisions.

Issue Title: {issue.title}
Issue Body: {issue.body}

Analyze the issue for:
1. **Requirements**: Are the functional requirements clear and complete? Are success criteria defined?
2. **Technical Decisions**: Are technology choices, architectural patterns, or implementation approaches specified?
3. **Edge Cases**: Are error scenarios, boundary conditions, or special cases considered?
4. **Missing Information**: Is any critical context, data, or specification missing?

For each ambiguity found, generate a specific question categorized as:
- "requirements" - unclear functional requirements
- "technical_decision" - unspecified technical choices
- "edge_case" - unhandled scenarios
- "missing_info" - absent critical information

Rate severity as: "critical", "important", or "nice_to_have"

If NO ambiguities are found, explain why the issue is sufficiently clear.

Return your analysis as JSON:
{{
  "has_ambiguities": boolean,
  "questions": [
    {{"question": "...", "category": "...", "severity": "..."}}
  ],
  "assumptions": ["assumption if continuing without answer"],
  "analysis": "brief explanation"
}}
IMPORTANT: Return ONLY the JSON object, no markdown formatting or code blocks."""

    # Execute the agent with inline prompt (using AgentPromptRequest would be cleaner, but we'll use execute_template)
    from adw_modules.agent import execute_prompt
    from adw_modules.data_types import AgentPromptRequest

    request = AgentPromptRequest(
        prompt=prompt,
        adw_id=adw_id,
        agent_name="clarifier",
        model="sonnet",
        dangerously_skip_permissions=False,
        output_file=f"agents/{adw_id}/clarifier/clarification.txt",
        working_dir=working_dir,
    )

    try:
        response = execute_prompt(request, logger)

        if not response.success:
            logger.warning(f"Clarification analysis failed: {response.output}")
            return None, response.output

        # Parse the JSON response
        output = response.output.strip()

        # Remove markdown code blocks if present
        if output.startswith("```"):
            lines = output.split("\n")
            # Find first and last code fence
            start_idx = 0
            end_idx = len(lines)
            for i, line in enumerate(lines):
                if line.startswith("```"):
                    if start_idx == 0:
                        start_idx = i + 1
                    else:
                        end_idx = i
                        break
            output = "\n".join(lines[start_idx:end_idx])

        data = parse_json(output, dict)

        # Parse into ClarificationResponse
        clarification = ClarificationResponse(
            has_ambiguities=data.get("has_ambiguities", False),
            questions=[
                ClarificationQuestion(**q) for q in data.get("questions", [])
            ],
            assumptions=data.get("assumptions", []),
            analysis=data.get("analysis", ""),
        )

        if clarification.has_ambiguities:
            logger.info(f"Found {len(clarification.questions)} ambiguities in issue")
        else:
            logger.info("No ambiguities detected - issue is sufficiently clear")

        return clarification, None

    except Exception as e:
        error_msg = f"Error during clarification analysis: {str(e)}"
        logger.error(error_msg)
        return None, error_msg


def resolve_clarifications(
    issue: GitHubIssue,
    clarification: ClarificationResponse,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    ai_docs_context: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """Auto-resolve clarification questions using AI with optional ai_docs context.

    Args:
        issue: GitHub issue object
        clarification: ClarificationResponse with questions
        adw_id: ADW identifier
        logger: Logger instance
        working_dir: Working directory path
        ai_docs_context: Optional AI documentation context to help with decisions

    Returns (resolved_text, error_message) tuple.
    """
    logger.info("Auto-resolving clarifications...")

    questions_text = "\n".join([
        f"- [{q.category}] {q.question} (severity: {q.severity})"
        for q in clarification.questions
    ])
    assumptions_text = "\n".join([f"- {a}" for a in clarification.assumptions])

    # Build context section if ai_docs are available
    context_section = ""
    if ai_docs_context:
        context_section = f"""
## Available Documentation Context
The following documentation has been loaded and should inform your decisions:

{ai_docs_context}

Use this documentation to make informed decisions aligned with project standards and best practices.
"""

    # Token optimization: Use truncated issue body (Task #13)
    issue_body_truncated = issue.body or ""
    if len(issue_body_truncated) > MAX_ISSUE_BODY_LENGTH:
        issue_body_truncated = issue_body_truncated[:MAX_ISSUE_BODY_LENGTH] + f"\n\n[TRUNCATED - full body exceeds {MAX_ISSUE_BODY_LENGTH} chars]"

    prompt = f"""You are a senior software architect making implementation decisions.

## Issue
Title: {issue.title}
Body: {issue_body_truncated}
{context_section}
## Questions to Resolve
{questions_text}

## Current Assumptions
{assumptions_text}

For EACH question: make a clear decision with brief rationale.
Choose the simplest reasonable approach that aligns with the documentation (if provided).

Return JSON:
{{
  "decisions": [{{"question": "...", "decision": "...", "rationale": "..."}}],
  "summary": "brief overall approach"
}}"""

    from adw_modules.agent import execute_prompt
    from adw_modules.data_types import AgentPromptRequest

    request = AgentPromptRequest(
        prompt=prompt,
        adw_id=adw_id,
        agent_name="resolver",
        model="sonnet",
        dangerously_skip_permissions=False,
        output_file=f"agents/{adw_id}/resolver/decisions.txt",
        working_dir=working_dir,
    )

    try:
        response = execute_prompt(request, logger)
        if not response.success:
            return None, response.output

        output = response.output.strip()
        # Remove markdown if present
        if output.startswith("```"):
            lines = output.split("\n")
            start_idx, end_idx = 0, len(lines)
            for i, line in enumerate(lines):
                if line.startswith("```"):
                    if start_idx == 0:
                        start_idx = i + 1
                    else:
                        end_idx = i
                        break
            output = "\n".join(lines[start_idx:end_idx])

        data = parse_json(output, dict)

        resolved_md = "## Auto-Resolved Clarifications\n\n"
        resolved_md += f"**Summary:** {data.get('summary', 'N/A')}\n\n"
        for d in data.get("decisions", []):
            resolved_md += f"**Q:** {d.get('question', 'N/A')}\n"
            resolved_md += f"**A:** {d.get('decision', 'N/A')}\n"
            resolved_md += f"*{d.get('rationale', 'N/A')}*\n\n"

        # Token optimization: Limit clarification text size (Task #13)
        if len(resolved_md) > MAX_CLARIFICATION_LENGTH:
            original_len = len(resolved_md)
            resolved_md = resolved_md[:MAX_CLARIFICATION_LENGTH] + f"\n\n[TRUNCATED - clarifications exceed {MAX_CLARIFICATION_LENGTH} chars, showing first {MAX_CLARIFICATION_LENGTH} of {original_len}]"
            logger.info(f"Truncated clarifications: {original_len} → {len(resolved_md)} chars")

        logger.info(f"Auto-resolved {len(data.get('decisions', []))} clarifications")
        return resolved_md, None
    except Exception as e:
        return None, f"Error auto-resolving: {str(e)}"


def build_plan(
    issue: GitHubIssue,
    command: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    clarifications: Optional[str] = None,
    ai_docs_context: Optional[str] = None,  # TAC-9: Documentation context
) -> AgentPromptResponse:
    """Build implementation plan for the issue using the specified command."""
    # Use minimal payload like classify_issue does
    minimal_issue_json = get_minimal_issue_json(issue)

    # If clarifications are provided, add them to the args
    args = [str(issue.number), adw_id, minimal_issue_json]
    if clarifications:
        args.append(clarifications)

    issue_plan_template_request = AgentTemplateRequest(
        agent_name=AGENT_PLANNER,
        slash_command=command,
        args=args,
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,  # TAC-9: Pass docs to planning
    )

    logger.debug(
        f"issue_plan_template_request: {issue_plan_template_request.model_dump_json(indent=2, by_alias=True)}"
    )

    issue_plan_response = execute_template(issue_plan_template_request)

    logger.debug(
        f"issue_plan_response: {issue_plan_response.model_dump_json(indent=2, by_alias=True)}"
    )

    return issue_plan_response


def implement_plan(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    agent_name: Optional[str] = None,
    working_dir: Optional[str] = None,
    ai_docs_context: Optional[str] = None,  # TAC-9: Documentation context
) -> AgentPromptResponse:
    """Implement the plan using the /implement command."""
    # Use provided agent_name or default to AGENT_IMPLEMENTOR
    implementor_name = agent_name or AGENT_IMPLEMENTOR

    implement_template_request = AgentTemplateRequest(
        agent_name=implementor_name,
        slash_command="/implement",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,  # TAC-9: Pass docs to implementation
    )

    logger.debug(
        f"implement_template_request: {implement_template_request.model_dump_json(indent=2, by_alias=True)}"
    )

    implement_response = execute_template(implement_template_request)

    logger.debug(
        f"implement_response: {implement_response.model_dump_json(indent=2, by_alias=True)}"
    )

    return implement_response


def implement_plan_with_report(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    agent_name: Optional[str] = None,
    working_dir: Optional[str] = None,
    ai_docs_context: Optional[str] = None,  # TAC-9: Documentation context
) -> AgentPromptResponse:
    """Implement the plan using /build_w_report command (TAC).

    This variant generates a structured YAML report of all changes made,
    useful for tracking and documentation purposes.

    Returns:
        AgentPromptResponse with output containing YAML work_changes report
    """
    implementor_name = agent_name or AGENT_IMPLEMENTOR

    implement_template_request = AgentTemplateRequest(
        agent_name=implementor_name,
        slash_command="/build_w_report",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,  # TAC-9: Pass docs to implementation
    )

    logger.debug(
        f"implement_with_report_request: {implement_template_request.model_dump_json(indent=2, by_alias=True)}"
    )

    implement_response = execute_template(implement_template_request)

    logger.debug(
        f"implement_with_report_response: {implement_response.model_dump_json(indent=2, by_alias=True)}"
    )

    return implement_response


def load_ai_docs(
    topic: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Load AI documentation for a topic using /load_ai_docs command (TAC-9).

    This fetches and integrates external documentation into project context
    before planning or implementation phases.

    Args:
        topic: Documentation topic to load (e.g., "FastAPI authentication")
        adw_id: ADW session ID
        logger: Logger instance
        working_dir: Optional working directory

    Returns:
        AgentPromptResponse with loaded documentation summary
    """
    request = AgentTemplateRequest(
        agent_name="docs_loader",
        slash_command="/load_ai_docs",
        args=[topic],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(f"Loading AI docs for topic: {topic}")

    response = execute_template(request)

    logger.debug(f"load_ai_docs response: {response.output[:200] if response.output else 'empty'}")

    return response


def _get_doc_cache_index_path() -> str:
    """Get path to documentation cache index file.

    The index tracks which documentation has been cached and is reused across workflows.
    This enables smart caching of common documentation (e.g., TAC-14 docs used by all tasks).

    Returns:
        Path to cache index JSON file
    """
    cache_dir = os.path.join("agents", "doc_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "index.json")


def _load_cache_index() -> Dict[str, Any]:
    """Load the documentation cache index.

    Returns:
        Dictionary with cache metadata for smart reuse
    """
    index_path = _get_doc_cache_index_path()
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {"topics": {}, "stats": {"hits": 0, "saves": 0, "tokens_saved": 0}}
    return {"topics": {}, "stats": {"hits": 0, "saves": 0, "tokens_saved": 0}}


def _save_cache_index(index: Dict[str, Any]):
    """Save the documentation cache index.

    Args:
        index: Cache index dictionary to save
    """
    index_path = _get_doc_cache_index_path()
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
    except Exception:
        pass  # Silent fail for cache index updates


def _get_summary_cache_path(topic: str, content_hash: str) -> str:
    """Get cache file path for a documentation summary.

    Args:
        topic: Documentation topic name
        content_hash: Hash of the documentation content

    Returns:
        Path to cache file
    """
    cache_dir = os.path.join("agents", "doc_cache")
    os.makedirs(cache_dir, exist_ok=True)
    safe_topic = topic.replace('/', '_').replace(' ', '_')
    return os.path.join(cache_dir, f"{safe_topic}_{content_hash[:12]}.txt")


def _load_cached_summary(topic: str, content: str, logger: logging.Logger) -> Optional[str]:
    """Load cached summary if available and update cache statistics.

    Smart caching system that:
    1. Checks for cached summaries by topic + content hash
    2. Tracks cache hits and token savings in global index
    3. Enables automatic reuse of common docs (e.g., TAC-14 across all tasks)

    Args:
        topic: Documentation topic name
        content: Full documentation content
        logger: Logger instance

    Returns:
        Cached summary or None if not found
    """
    import hashlib
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    cache_path = _get_summary_cache_path(topic, content_hash)

    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = f.read()

            # Update cache statistics
            index = _load_cache_index()
            if topic not in index["topics"]:
                index["topics"][topic] = {}
            index["topics"][topic][content_hash[:12]] = {
                "hits": index["topics"][topic].get(content_hash[:12], {}).get("hits", 0) + 1,
                "cached_size": len(cached),
                "original_size": len(content),
                "tokens_saved_estimate": (len(content) - len(cached)) // 4,  # Rough estimate
            }
            index["stats"]["hits"] += 1
            index["stats"]["tokens_saved"] += (len(content) - len(cached)) // 4
            _save_cache_index(index)

            tokens_saved = (len(content) - len(cached)) // 4
            logger.info(f"✓ Using cached summary for '{topic}' (saved ~{tokens_saved} tokens, hash: {content_hash[:12]})")
            return cached
        except Exception as e:
            logger.debug(f"Failed to load cache for {topic}: {e}")

    return None


def _save_summary_cache(topic: str, content: str, summary: str, logger: logging.Logger):
    """Save summary to cache and update global index for smart reuse.

    Smart caching that enables automatic reuse of common documentation across workflows.
    For example, TAC-14 documentation is cached once and reused by all TAC-14 tasks.

    Args:
        topic: Documentation topic name
        content: Full documentation content
        summary: Summarized content
        logger: Logger instance
    """
    import hashlib
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    cache_path = _get_summary_cache_path(topic, content_hash)

    try:
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(summary)

        # Update cache index for smart reuse across workflows
        index = _load_cache_index()
        if topic not in index["topics"]:
            index["topics"][topic] = {}

        index["topics"][topic][content_hash[:12]] = {
            "hits": 0,
            "cached_size": len(summary),
            "original_size": len(content),
            "tokens_saved_estimate": (len(content) - len(summary)) // 4,
            "created_at": str(os.path.getmtime(cache_path) if os.path.exists(cache_path) else 0),
        }
        index["stats"]["saves"] += 1
        index["stats"]["tokens_saved"] += (len(content) - len(summary)) // 4
        _save_cache_index(index)

        reduction_pct = ((len(content) - len(summary)) / len(content) * 100) if len(content) > 0 else 0
        logger.debug(f"✓ Cached summary for '{topic}' ({reduction_pct:.1f}% reduction, {content_hash[:12]})")
    except Exception as e:
        logger.warning(f"Failed to cache summary for '{topic}': {e}")


def get_cache_statistics() -> Dict[str, Any]:
    """Get documentation cache statistics for reporting.

    Returns summary of cache efficiency, hits, and savings.

    Returns:
        Dictionary with cache stats including:
        - total_hits: Number of cache hits across all workflows
        - total_saves: Number of cache saves
        - tokens_saved: Estimated tokens saved by caching
        - cached_topics: Number of unique documentation topics cached
    """
    index = _load_cache_index()
    stats = index.get("stats", {})
    return {
        "total_hits": stats.get("hits", 0),
        "total_saves": stats.get("saves", 0),
        "tokens_saved": stats.get("tokens_saved", 0),
        "cached_topics": len(index.get("topics", {})),
        "cache_index_path": _get_doc_cache_index_path(),
    }


def extract_relevant_sections(
    content: str,
    issue: GitHubIssue,
    topic: str,
    logger: logging.Logger,
) -> str:
    """Extract only relevant sections from documentation based on issue context.

    Reduces token consumption by ~60-80% by extracting only sections that match
    keywords from the issue title/body, rather than summarizing entire document.

    Args:
        content: Full documentation content
        issue: GitHub issue to match against
        topic: Documentation topic name
        logger: Logger instance

    Returns:
        Extracted relevant sections or full content if extraction fails
    """
    if not content or len(content) < 500:
        # Too short to extract sections, return as-is
        return content

    # Extract keywords from issue
    issue_text = f"{issue.title} {issue.body or ''}".lower()
    keywords = set()

    # Common technical keywords to prioritize
    for word in issue_text.split():
        word = word.strip('.,;:!?()[]{}')
        if len(word) > 3 and word.isalnum():  # Skip short words and non-alphanumeric
            keywords.add(word)

    if not keywords:
        return content

    # Split content into sections (by headers)
    sections = []
    current_section = []

    for line in content.split('\n'):
        # Detect markdown headers
        if line.startswith('#'):
            if current_section:
                sections.append('\n'.join(current_section))
                current_section = []
        current_section.append(line)

    if current_section:
        sections.append('\n'.join(current_section))

    # Score sections based on keyword matches
    scored_sections = []
    for section in sections:
        section_lower = section.lower()
        score = sum(1 for kw in keywords if kw in section_lower)
        if score > 0:
            scored_sections.append((score, section))

    if not scored_sections:
        logger.debug(f"No keyword matches in '{topic}', using full content")
        return content

    # Sort by score and take top sections (max 40% of original)
    scored_sections.sort(reverse=True, key=lambda x: x[0])
    max_chars = int(len(content) * 0.4)  # Max 40% of original size

    extracted = []
    total_chars = 0
    for score, section in scored_sections:
        if total_chars + len(section) > max_chars:
            break
        extracted.append(section)
        total_chars += len(section)

    if extracted:
        result = '\n\n'.join(extracted)
        reduction_pct = ((len(content) - len(result)) / len(content) * 100)
        logger.info(f"Extracted sections from '{topic}': {len(content)} → {len(result)} chars ({reduction_pct:.1f}% reduction)")
        return result

    return content


def summarize_doc_content(
    content: str,
    topic: str,
    adw_id: str,
    logger: logging.Logger,
    max_summary_tokens: int = 200,
    issue: Optional[GitHubIssue] = None,
) -> str:
    """Summarize documentation content using haiku model for token optimization (TAC-9).

    Creates concise summaries of documentation to reduce token consumption
    by 70-85% while preserving essential information for agents.

    Optimizations:
    1. Cache system - Reuses summaries for identical content
    2. Section extraction - Extracts only relevant sections before summarizing
    3. Aggressive summarization - Reduced default from 300 to 200 tokens

    Args:
        content: Full documentation content to summarize
        topic: Documentation topic name
        adw_id: ADW session ID
        logger: Logger instance
        max_summary_tokens: Target max tokens for summary (default 200)
        issue: Optional GitHub issue for section extraction

    Returns:
        Summarized documentation content
    """
    if not content or len(content.strip()) < 200:
        # Content too short to summarize, return as-is
        return content

    # Check cache first
    cached_summary = _load_cached_summary(topic, content, logger)
    if cached_summary:
        return cached_summary

    # Extract relevant sections if issue provided (saves 60-80% tokens)
    if issue:
        content = extract_relevant_sections(content, issue, topic, logger)

    logger.debug(f"Summarizing documentation for topic: {topic}")

    # Import here to avoid circular dependencies
    from adw_modules.data_types import AgentPromptRequest
    from adw_modules.agent import execute_prompt

    # Improved summarization prompt - more aggressive
    summarization_prompt = f"""Create an ultra-concise summary for an AI agent.

**Topic:** {topic}

**Rules:**
- ONLY essential facts and patterns needed for implementation
- Use bullets, no prose
- Max {max_summary_tokens} tokens total
- Keep code snippets minimal (1-2 lines max)
- Skip: intro, background, explanations
- Include: API signatures, gotchas, constraints

**Content:**
{content}

**Summary:**"""

    # Create output file for the summarization
    output_file = f"/tmp/adw_doc_summary_{adw_id}_{topic.replace('/', '_')}.txt"

    request = AgentPromptRequest(
        prompt=summarization_prompt,
        agent_name="doc_summarizer",
        adw_id=adw_id,
        model="haiku",  # Use haiku for fast, cost-effective summarization
        output_file=output_file,
        dangerously_skip_permissions=True,  # Safe for read-only summarization
    )

    response = execute_prompt(request, logger=logger)

    if response.success and response.output:
        summary = response.output.strip()
        original_len = len(content)
        summary_len = len(summary)
        reduction_pct = ((original_len - summary_len) / original_len * 100) if original_len > 0 else 0
        logger.info(f"Summarized '{topic}': {original_len} → {summary_len} chars ({reduction_pct:.1f}% reduction)")

        # Cache the summary for future use
        _save_summary_cache(topic, content, summary, logger)

        return summary
    else:
        logger.warning(f"Failed to summarize '{topic}', using original content")
        return content


def detect_relevant_docs(issue: GitHubIssue) -> list[str]:
    """Detect which documentation topics are relevant to a GitHub issue (TAC-9).

    Analyzes the issue title and body to identify relevant documentation topics
    based on keyword matching. This enables automatic context loading for workflows.

    Optimized for speed and relevance:
    1. Prioritizes exact matches in title (highest weight)
    2. Uses strict keyword matching (requires specific terms)
    3. Limits total documents to prevent slowdowns
    4. Dynamic file scanning only for exact filename matches

    Args:
        issue: GitHub issue to analyze

    Returns:
        List of detected documentation topic names (max 8 topics for performance)

    Example:
        >>> issue = GitHubIssue(title="Add JWT authentication", body="...")
        >>> detect_relevant_docs(issue)
        ["authentication", "api"]
    """
    title = issue.title.lower()
    body = (issue.body or "").lower()
    text = f"{title} {body}"

    # Score-based detection: title matches are higher priority
    topic_scores = {}
    MAX_TOPICS = 8  # Limit to prevent loading too many docs

    # Strict keyword mapping - only specific, non-generic keywords
    doc_keywords = {
        # Technical domains - using stricter keywords
        "authentication": ["jwt", "oauth", "authentication", "login flow", "auth system"],
        "testing": ["pytest", "unit test", "integration test", "e2e test", "test coverage"],
        "deployment": ["deployment", "docker", "kubernetes", "k8s", "ci/cd pipeline"],
        "database": ["database", "postgres", "mysql", "migration", "schema design"],
        "api": ["api endpoint", "rest api", "graphql", "api design"],

        # Architecture & Design - stricter matching
        "ddd_lite": ["domain-driven design", "ddd lite", "lightweight ddd", "tactical ddd"],
        "ddd": ["domain-driven", "ddd", "aggregate", "bounded context", "ubiquitous language"],
        "solid": ["solid principles", "single responsibility", "open-closed", "liskov substitution"],
        "design_patterns": ["design pattern", "singleton pattern", "factory pattern", "observer pattern"],

        # Documentation - project-specific
        "fractal_docs": ["fractal documentation", "fractal docs", "documentation structure"],

        # AI & SDK - specific terms only
        "anthropic_quick_start": ["anthropic api", "claude api", "anthropic sdk"],
        "claude_code_cli_reference": ["claude code cli", "claude-code", "claude code reference"],

        # TAC Course Topics - Framework-specific
        "Tac-14": ["agent definition", "custom agent", "yaml frontmatter", "jinja2 template", "class-2", "orchestration"],
        "Tac-13": ["agent expert", "expertise file", "self-improving", "mental model", "act learn reuse"],
        "Tac-12": ["scout", "codebase exploration", "parallel scouting", "scout agent"],
        "Tac-11": ["hook", "automation", "pre-commit", "post-commit", "event trigger"],
        "Tac-10": ["documentation loading", "ai docs", "context loading"],
        "Tac-9": ["token optimization", "cost reduction", "summarization"],
        "Tac-1": ["adw workflow", "sdlc", "isolated worktree", "zero touch"],

        # Legacy TAC specific docs
        "Tac-13-agent-experts": ["expertise-driven development"],
        "expertise-file-structure": ["expertise yaml", "expertise structure", "expertise schema"],
        "meta-skill-pattern": ["meta-skill", "progressive disclosure", "skill levels"],
    }

    # Check strict keywords - only add if multiple keywords match or title match
    for doc_topic, keywords in doc_keywords.items():
        title_matches = sum(1 for kw in keywords if kw in title)
        body_matches = sum(1 for kw in keywords if kw in body)

        if title_matches > 0:
            topic_scores[doc_topic] = 10 + title_matches  # Title match = high priority
        elif body_matches >= 2:  # Require at least 2 keyword matches in body
            topic_scores[doc_topic] = body_matches

    # DYNAMIC DETECTION: Only for exact filename matches (fast)
    # Prioritizes TAC docs, PLAN docs, and exact name matches
    try:
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        ai_docs_dir = os.path.join(project_root, "ai_docs")

        if os.path.exists(ai_docs_dir):
            # Only scan for exact matches - much faster than checking variants
            for root, dirs, files in os.walk(ai_docs_dir):
                for file in files:
                    if not file.endswith(".md"):
                        continue

                    topic_name = file[:-3]
                    topic_lower = topic_name.lower()

                    # Skip if already detected
                    if topic_name in topic_scores:
                        continue

                    # HIGH PRIORITY: Exact TAC number match (e.g., "tac-13" matches "Tac-13_1")
                    if "tac-" in title or "tac " in title:
                        # Extract TAC number from title
                        import re
                        tac_match = re.search(r'tac[-\s]?(\d+)', title)
                        if tac_match:
                            tac_num = tac_match.group(1)
                            # Check if this file is for that TAC
                            if f"tac-{tac_num}" in topic_lower or f"tac_{tac_num}" in topic_lower or f"tac{tac_num}" in topic_lower:
                                topic_scores[topic_name] = 20  # Highest priority
                                continue

                    # MEDIUM PRIORITY: PLAN documents (check title OR body)
                    if ("plan" in title or "plan" in body) and "plan" in topic_lower:
                        topic_scores[topic_name] = 15
                        continue

                    # LOW PRIORITY: Exact filename in title OR body (case-insensitive)
                    if topic_lower in title or topic_lower in body:
                        topic_scores[topic_name] = 5

    except Exception:
        # If scanning fails, continue with keyword-based topics
        pass

    # Sort by score and take top N topics
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)
    top_topics = [topic for topic, score in sorted_topics[:MAX_TOPICS]]

    return sorted(top_topics)  # Return sorted for consistency


def scout_codebase(
    query: str,
    adw_id: str,
    logger: logging.Logger,
    scale: str = "medium",
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Scout codebase using /scout command (TAC).

    Executes parallel scouting to explore codebases and find relevant files.

    Args:
        query: Search query describing what to find in the codebase
        adw_id: ADW session ID
        logger: Logger instance
        scale: Scale of exploration ("quick", "medium", "very thorough") - default "medium"
        working_dir: Optional working directory

    Returns:
        AgentPromptResponse with exploration results
    """
    request = AgentTemplateRequest(
        agent_name="codebase_scout",
        slash_command="/scout",
        args=[query, scale],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(f"Scouting codebase with query: {query}, scale: {scale}")

    response = execute_template(request)

    logger.debug(f"scout_codebase response: {response.output[:200] if response.output else 'empty'}")

    return response


def plan_with_scouts(
    description: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    ai_docs_context: Optional[str] = None,  # TAC-9: Documentation context
) -> AgentPromptResponse:
    """Create enhanced plan with parallel codebase exploration using /plan_w_scouters (TAC).

    This command performs parallel scouting before planning, providing comprehensive codebase
    context for better implementation plans.

    Args:
        description: Feature or task description for planning
        adw_id: ADW session ID
        logger: Logger instance
        working_dir: Optional working directory
        ai_docs_context: Optional AI documentation context (TAC-9)

    Returns:
        AgentPromptResponse with enhanced plan
    """
    request = AgentTemplateRequest(
        agent_name="scout_planner",
        slash_command="/plan_w_scouters",
        args=[description],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,  # TAC-9: Pass docs to scout planning
    )

    logger.debug(f"Planning with scouts for: {description}")

    response = execute_template(request)

    logger.debug(f"plan_with_scouts response: {response.output[:200] if response.output else 'empty'}")

    return response


def build_in_parallel(
    plan_file: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    ai_docs_context: Optional[str] = None,  # TAC-9: Documentation context
) -> AgentPromptResponse:
    """Build implementation in parallel using /build_in_parallel (TAC).

    This command delegates file creation to parallel build-agents for faster implementation.

    Args:
        plan_file: Path to the plan file to implement
        adw_id: ADW session ID
        logger: Logger instance
        working_dir: Optional working directory
        ai_docs_context: Optional AI documentation context (TAC-9)

    Returns:
        AgentPromptResponse with build results
    """
    request = AgentTemplateRequest(
        agent_name="parallel_builder",
        slash_command="/build_in_parallel",
        args=[plan_file],
        adw_id=adw_id,
        working_dir=working_dir,
        ai_docs_context=ai_docs_context,  # TAC-9: Pass docs to parallel builders
    )

    logger.debug(f"Building in parallel from plan: {plan_file}")

    response = execute_template(request)

    logger.debug(f"build_in_parallel response: {response.output[:200] if response.output else 'empty'}")

    return response


def find_and_summarize(
    search_term: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Find and summarize code using /find_and_summarize (TAC).

    This command searches for code matching a term and provides a summary of findings.

    Args:
        search_term: Term or pattern to search for in codebase
        adw_id: ADW session ID
        logger: Logger instance
        working_dir: Optional working directory

    Returns:
        AgentPromptResponse with search and summary results
    """
    request = AgentTemplateRequest(
        agent_name="code_finder",
        slash_command="/find_and_summarize",
        args=[search_term],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(f"Finding and summarizing code for: {search_term}")

    response = execute_template(request)

    logger.debug(f"find_and_summarize response: {response.output[:200] if response.output else 'empty'}")

    return response


def clean_model_output(output: str) -> str:
    """Clean model output by removing markdown code blocks and extra whitespace.

    Models sometimes wrap their output in markdown code blocks like:
    ```
    actual_content
    ```

    This function removes those wrappers to get the clean content.
    For branch names, it also extracts just the branch name from explanatory text.
    """
    import re

    cleaned = output.strip()

    # Remove markdown code blocks (``` or ```language)
    # Pattern matches: ``` optionally followed by language name, then content, then ```
    code_block_pattern = r'^```(?:\w+)?\s*\n?(.*?)\n?```$'
    match = re.match(code_block_pattern, cleaned, re.DOTALL)
    if match:
        cleaned = match.group(1).strip()

    # Also handle case where ``` appears on separate lines
    if cleaned.startswith('```'):
        lines = cleaned.split('\n')
        # Remove first line if it's just ``` or ```language
        if lines[0].strip().startswith('```'):
            lines = lines[1:]
        # Remove last line if it's just ```
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]
        cleaned = '\n'.join(lines).strip()

    # Extract branch name from explanatory text
    # Look for common patterns like "The branch name is:" or "Generated branch name:"
    # Or extract the last line that looks like a valid branch name
    branch_name_pattern = r'(?:branch name.*?:[\s]*)?([a-z][a-z0-9-]+(?:-issue-\d+)?(?:-adw-[a-zA-Z0-9_]+)?(?:-[a-z0-9-]+)?)\s*$'
    match = re.search(branch_name_pattern, cleaned, re.IGNORECASE | re.MULTILINE)
    if match:
        potential_branch = match.group(1).strip()
        # Validate it looks like a branch name (contains hyphens, no spaces, lowercase)
        if '-' in potential_branch and ' ' not in potential_branch and '\n' not in potential_branch:
            cleaned = potential_branch

    return cleaned


def generate_branch_name(
    issue: GitHubIssue,
    issue_class: IssueClassSlashCommand,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    """Generate a git branch name for the issue.
    Returns (branch_name, error_message) tuple."""
    # Remove the leading slash from issue_class for the branch name
    issue_type = issue_class.replace("/", "")

    # Use minimal payload like classify_issue does
    minimal_issue_json = get_minimal_issue_json(issue)

    request = AgentTemplateRequest(
        agent_name=AGENT_BRANCH_GENERATOR,
        slash_command="/generate_branch_name",
        args=[issue_type, adw_id, minimal_issue_json],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    # Clean the output to remove markdown code blocks that models sometimes add
    branch_name = clean_model_output(response.output)
    logger.info(f"Generated branch name: {branch_name}")
    return branch_name, None


def create_commit(
    agent_name: str,
    issue: GitHubIssue,
    issue_class: IssueClassSlashCommand,
    adw_id: str,
    logger: logging.Logger,
    working_dir: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Create a git commit with a properly formatted message.
    Returns (commit_message, error_message) tuple."""
    # Remove the leading slash from issue_class
    issue_type = issue_class.replace("/", "")

    # Create unique committer agent name by suffixing '_committer'
    unique_agent_name = f"{agent_name}_committer"

    # Use minimal payload like classify_issue does
    minimal_issue_json = get_minimal_issue_json(issue)

    request = AgentTemplateRequest(
        agent_name=unique_agent_name,
        slash_command="/commit",
        args=[agent_name, issue_type, minimal_issue_json],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    commit_message = response.output.strip()
    logger.info(f"Created commit message: {commit_message}")
    return commit_message, None


def create_pull_request(
    branch_name: str,
    issue: Optional[GitHubIssue],
    state: ADWState,
    logger: logging.Logger,
    working_dir: str,
) -> Tuple[Optional[str], Optional[str]]:
    """Create a pull request for the implemented changes.
    Returns (pr_url, error_message) tuple."""

    # Get plan file from state (may be None for test runs)
    plan_file = state.get("plan_file") or "No plan file (test run)"
    adw_id = state.get("adw_id")

    # If we don't have issue data, try to construct minimal data
    if not issue:
        issue_data = state.get("issue", {})
        issue_json = json.dumps(issue_data) if issue_data else "{}"
    elif isinstance(issue, dict):
        # Try to reconstruct as GitHubIssue model which handles datetime serialization
        from adw_modules.data_types import GitHubIssue

        try:
            issue_model = GitHubIssue(**issue)
            # Use minimal payload like classify_issue does
            issue_json = issue_model.model_dump_json(
                by_alias=True, include={"number", "title", "body"}
            )
        except Exception:
            # Fallback: use json.dumps with default str converter for datetime
            issue_json = json.dumps(issue, default=str)
    else:
        # Use minimal payload like classify_issue does
        issue_json = issue.model_dump_json(
            by_alias=True, include={"number", "title", "body"}
        )

    request = AgentTemplateRequest(
        agent_name=AGENT_PR_CREATOR,
        slash_command="/pull_request",
        args=[branch_name, issue_json, plan_file, adw_id],
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if not response.success:
        return None, response.output

    pr_url = response.output.strip()
    logger.info(f"Created pull request: {pr_url}")
    return pr_url, None


def ensure_plan_exists(state: ADWState, issue_number: str) -> str:
    """Find or error if no plan exists for issue.
    Used by isolated build workflows in standalone mode."""
    # Check if plan file is in state
    if state.get("plan_file"):
        return state.get("plan_file")

    # Check current branch
    from adw_modules.git_ops import get_current_branch

    branch = get_current_branch()

    # Look for plan in branch name
    if f"-{issue_number}-" in branch:
        # Look for plan file
        plans = glob.glob(f"specs/*{issue_number}*.md")
        if plans:
            return plans[0]

    # No plan found
    raise ValueError(
        f"No plan found for issue {issue_number}. Run adw_plan_iso.py first."
    )


def ensure_adw_id(
    issue_number: str,
    adw_id: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> str:
    """Get ADW ID or create a new one and initialize state.

    Args:
        issue_number: The issue number to find/create ADW ID for
        adw_id: Optional existing ADW ID to use
        logger: Optional logger instance

    Returns:
        The ADW ID (existing or newly created)
    """
    # If ADW ID provided, check if state exists
    if adw_id:
        state = ADWState.load(adw_id, logger)
        if state:
            if logger:
                logger.info(f"Found existing ADW state for ID: {adw_id}")
            else:
                print(f"Found existing ADW state for ID: {adw_id}")
            return adw_id
        # ADW ID provided but no state exists, create state
        state = ADWState(adw_id)
        state.update(adw_id=adw_id, issue_number=issue_number)
        state.save("ensure_adw_id")
        if logger:
            logger.info(f"Created new ADW state for provided ID: {adw_id}")
        else:
            print(f"Created new ADW state for provided ID: {adw_id}")
        return adw_id

    # No ADW ID provided, create new one with state
    from adw_modules.utils import make_adw_id

    new_adw_id = make_adw_id()
    state = ADWState(new_adw_id)
    state.update(adw_id=new_adw_id, issue_number=issue_number)
    state.save("ensure_adw_id")
    if logger:
        logger.info(f"Created new ADW ID and state: {new_adw_id}")
    else:
        print(f"Created new ADW ID and state: {new_adw_id}")
    return new_adw_id


def find_existing_branch_for_issue(
    issue_number: str, adw_id: Optional[str] = None, cwd: Optional[str] = None
) -> Optional[str]:
    """Find an existing branch for the given issue number.
    Returns branch name if found, None otherwise."""
    # List all branches
    result = subprocess.run(
        ["git", "branch", "-a"], capture_output=True, text=True, cwd=cwd
    )

    if result.returncode != 0:
        return None

    branches = result.stdout.strip().split("\n")

    # Look for branch with standardized pattern: *-issue-{issue_number}-adw-{adw_id}-*
    for branch in branches:
        branch = branch.strip().replace("* ", "").replace("remotes/origin/", "")
        # Check for the standardized pattern
        if f"-issue-{issue_number}-" in branch:
            if adw_id and f"-adw-{adw_id}-" in branch:
                return branch
            elif not adw_id:
                # Return first match if no adw_id specified
                return branch

    return None


def find_plan_for_issue(
    issue_number: str, adw_id: Optional[str] = None
) -> Optional[str]:
    """Find plan file for the given issue number and optional adw_id.
    Returns path to plan file if found, None otherwise."""
    import os

    # Get project root
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    agents_dir = os.path.join(project_root, "agents")

    if not os.path.exists(agents_dir):
        return None

    # If adw_id is provided, check specific directory first
    if adw_id:
        plan_path = os.path.join(agents_dir, adw_id, AGENT_PLANNER, "plan.md")
        if os.path.exists(plan_path):
            return plan_path

    # Otherwise, search all agent directories
    for agent_id in os.listdir(agents_dir):
        agent_path = os.path.join(agents_dir, agent_id)
        if os.path.isdir(agent_path):
            plan_path = os.path.join(agent_path, AGENT_PLANNER, "plan.md")
            if os.path.exists(plan_path):
                # Check if this plan is for our issue by reading branch info or checking commits
                # For now, return the first plan found (can be improved)
                return plan_path

    return None


def create_or_find_branch(
    issue_number: str,
    issue: GitHubIssue,
    state: ADWState,
    logger: logging.Logger,
    cwd: Optional[str] = None,
) -> Tuple[str, Optional[str]]:
    """Create or find a branch for the given issue.

    1. First checks state for existing branch name
    2. Then looks for existing branches matching the issue
    3. If none found, classifies the issue and creates a new branch

    Returns (branch_name, error_message) tuple.
    """
    # 1. Check state for branch name
    branch_name = state.get("branch_name") or state.get("branch", {}).get("name")
    if branch_name:
        logger.info(f"Found branch in state: {branch_name}")
        # Check if we need to checkout
        from adw_modules.git_ops import get_current_branch

        current = get_current_branch(cwd=cwd)
        if current != branch_name:
            result = subprocess.run(
                ["git", "checkout", branch_name],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            if result.returncode != 0:
                # Branch might not exist locally, try to create from remote
                result = subprocess.run(
                    ["git", "checkout", "-b", branch_name, f"origin/{branch_name}"],
                    capture_output=True,
                    text=True,
                    cwd=cwd,
                )
                if result.returncode != 0:
                    return "", f"Failed to checkout branch: {result.stderr}"
        return branch_name, None

    # 2. Look for existing branch
    adw_id = state.get("adw_id")
    existing_branch = find_existing_branch_for_issue(issue_number, adw_id, cwd=cwd)
    if existing_branch:
        logger.info(f"Found existing branch: {existing_branch}")
        # Checkout the branch
        result = subprocess.run(
            ["git", "checkout", existing_branch],
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode != 0:
            return "", f"Failed to checkout branch: {result.stderr}"
        state.update(branch_name=existing_branch)
        return existing_branch, None

    # 3. Create new branch - classify issue first
    logger.info("No existing branch found, creating new one")

    # Classify the issue
    issue_command, error = classify_issue(issue, adw_id, logger, working_dir=cwd)
    if error:
        return "", f"Failed to classify issue: {error}"

    state.update(issue_class=issue_command)

    # Generate branch name
    branch_name, error = generate_branch_name(issue, issue_command, adw_id, logger, working_dir=cwd)
    if error:
        return "", f"Failed to generate branch name: {error}"

    # Create the branch
    from adw_modules.git_ops import create_branch

    success, error = create_branch(branch_name, cwd=cwd)
    if not success:
        return "", f"Failed to create branch: {error}"

    state.update(branch_name=branch_name)
    logger.info(f"Created and checked out new branch: {branch_name}")

    return branch_name, None


def find_spec_file(state: ADWState, logger: logging.Logger) -> Optional[str]:
    """Find the spec file from state or by examining git diff.

    For isolated workflows, automatically uses worktree_path from state.
    """
    # Get worktree path if in isolated workflow
    worktree_path = state.get("worktree_path")

    # Check if spec file is already in state (from plan phase)
    spec_file = state.get("plan_file")
    if spec_file:
        # If worktree_path exists and spec_file is relative, make it absolute
        if worktree_path and not os.path.isabs(spec_file):
            spec_file = os.path.join(worktree_path, spec_file)

        if os.path.exists(spec_file):
            logger.info(f"Using spec file from state: {spec_file}")
            return spec_file

    # Otherwise, try to find it from git diff
    target_branch = get_target_branch()
    logger.info(f"Looking for spec file in git diff against origin/{target_branch}")
    result = subprocess.run(
        ["git", "diff", f"origin/{target_branch}", "--name-only"],
        capture_output=True,
        text=True,
        cwd=worktree_path,
    )

    if result.returncode == 0:
        files = result.stdout.strip().split("\n")
        spec_files = [f for f in files if f.startswith("specs/") and f.endswith(".md")]

        if spec_files:
            # Use the first spec file found
            spec_file = spec_files[0]
            if worktree_path:
                spec_file = os.path.join(worktree_path, spec_file)
            logger.info(f"Found spec file: {spec_file}")
            return spec_file

    # If still not found, try to derive from branch name
    branch_name = state.get("branch_name")
    if branch_name:
        # Extract issue number from branch name
        import re

        match = re.search(r"issue-(\d+)", branch_name)
        if match:
            issue_num = match.group(1)
            adw_id = state.get("adw_id")

            # Look for spec files matching the pattern
            import glob

            # Use worktree_path if provided, otherwise current directory
            search_dir = worktree_path if worktree_path else os.getcwd()
            pattern = os.path.join(
                search_dir, f"specs/issue-{issue_num}-adw-{adw_id}*.md"
            )
            spec_files = glob.glob(pattern)

            if spec_files:
                spec_file = spec_files[0]
                logger.info(f"Found spec file by pattern: {spec_file}")
                return spec_file

    logger.warning("No spec file found")
    return None


def create_and_implement_patch(
    adw_id: str,
    review_change_request: str,
    logger: logging.Logger,
    agent_name_planner: str,
    agent_name_implementor: str,
    spec_path: Optional[str] = None,
    issue_screenshots: Optional[str] = None,
    working_dir: Optional[str] = None,
) -> Tuple[Optional[str], AgentPromptResponse]:
    """Create a patch plan and implement it.
    Returns (patch_file_path, implement_response) tuple."""

    # Create patch plan using /patch command
    args = [adw_id, review_change_request]

    # Add optional arguments in the correct order
    if spec_path:
        args.append(spec_path)
    else:
        args.append("")  # Empty string for optional spec_path

    args.append(agent_name_planner)

    if issue_screenshots:
        args.append(issue_screenshots)

    request = AgentTemplateRequest(
        agent_name=agent_name_planner,
        slash_command="/patch",
        args=args,
        adw_id=adw_id,
        working_dir=working_dir,
    )

    logger.debug(
        f"Patch plan request: {request.model_dump_json(indent=2, by_alias=True)}"
    )

    response = execute_template(request)

    logger.debug(
        f"Patch plan response: {response.model_dump_json(indent=2, by_alias=True)}"
    )

    if not response.success:
        logger.error(f"Error creating patch plan: {response.output}")
        # Return None and a failed response
        return None, AgentPromptResponse(
            output=f"Failed to create patch plan: {response.output}", success=False
        )

    # Extract the patch plan file path from the response
    patch_file_path = strip_code_fences(response.output)

    # Validate that it looks like a file path
    if "specs/patch/" not in patch_file_path or not patch_file_path.endswith(".md"):
        logger.error(f"Invalid patch plan path returned: {patch_file_path}")
        return None, AgentPromptResponse(
            output=f"Invalid patch plan path: {patch_file_path}", success=False
        )

    logger.info(f"Created patch plan: {patch_file_path}")

    # Now implement the patch plan using the provided implementor agent name
    implement_response = implement_plan(
        patch_file_path, adw_id, logger, agent_name_implementor, working_dir=working_dir
    )

    return patch_file_path, implement_response


# ============================================================================
# TAC: Expert System Integration
# ============================================================================

def consult_expert(
    domain: str,
    question: str,
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None
) -> AgentPromptResponse:
    """Consult domain expert using expertise.yaml before making decisions.

    This is the REUSE phase of the Act → Learn → Reuse loop.

    Args:
        domain: Expert domain (adw, cli, commands)
        question: Question to ask the expert
        adw_id: ADW workflow identifier
        logger: Logger instance
        working_dir: Working directory for agent execution

    Returns:
        AgentPromptResponse with expert's answer
    """
    logger.info(f"TAC: Consulting {domain} expert")

    request = AgentTemplateRequest(
        agent_name=f"{domain}_expert",
        slash_command=f"/experts:{domain}:question",
        args=[question],
        adw_id=adw_id,
        model="haiku",  # TAC Optimization: Use Haiku for Q&A (10x cheaper, sufficient for guidance)
        working_dir=working_dir,
    )

    response = execute_template(request)

    if response.success:
        logger.info(f"Expert consultation successful ({len(response.output)} chars)")
    else:
        logger.warning(f"Expert consultation failed: {response.output}")

    return response


def improve_expert_knowledge(
    domain: str,
    check_git_diff: bool,
    focus_area: Optional[str],
    adw_id: str,
    logger: logging.Logger,
    working_dir: Optional[str] = None,
    summary_mode: bool = True
) -> AgentPromptResponse:
    """Update domain expert's expertise.yaml based on code changes.

    This is the LEARN phase of the Act → Learn → Reuse loop.

    Args:
        domain: Expert domain (adw, cli, commands)
        check_git_diff: If True, focus on recently changed files
        focus_area: Optional area to focus validation
        adw_id: ADW workflow identifier
        logger: Logger instance
        working_dir: Working directory for agent execution
        summary_mode: If True, use summarized diffs and selective file reading (default: True)

    Returns:
        AgentPromptResponse with self-improve report
    """
    logger.info(f"TAC: Running self-improve for {domain} expert (summary_mode={summary_mode})")

    # Build args for self-improve command
    args = []
    if check_git_diff:
        args.append("true")
    else:
        args.append("false")

    if focus_area:
        args.append(focus_area)
    else:
        args.append("")  # Placeholder for focus_area

    # Add summary_mode as third argument
    args.append("true" if summary_mode else "false")

    request = AgentTemplateRequest(
        agent_name=f"{domain}_expert_improver",
        slash_command=f"/experts:{domain}:self-improve",
        args=args,
        adw_id=adw_id,
        working_dir=working_dir,
    )

    response = execute_template(request)

    if response.success:
        logger.info(f"Expert self-improve completed successfully")
    else:
        logger.warning(f"Expert self-improve failed: {response.output}")

    return response


def extract_file_references_from_issue(
    issue: GitHubIssue,
    logger: logging.Logger,
    working_dir: Optional[str] = None
) -> dict[str, str]:
    """Extract and load files referenced in issue body AND comments (hybrid approach).

    Detects references like:
    - plan_tasks_Tac_14.md
    - specs/feature-auth.md
    - ai_docs/architecture.md
    - Any .md file path

    Searches in:
    1. Issue body
    2. All issue comments (newest to oldest)

    Args:
        issue: GitHub issue object with body and comments
        logger: Logger instance
        working_dir: Working directory to search for files (default: current dir)

    Returns:
        Dictionary mapping file paths to their content
        Example: {"plan_tasks_Tac_14.md": "# Plan...", "specs/auth.md": "# Spec..."}
    """
    search_dir = working_dir or os.getcwd()
    loaded_files = {}

    # Patterns to detect file references
    # Matches: plan_tasks_*.md, specs/*.md, ai_docs/*.md, any/path.md
    patterns = [
        r'plan_tasks_[A-Za-z0-9_-]+\.md',  # plan_tasks_Tac_14.md
        r'specs/[A-Za-z0-9_/-]+\.md',       # specs/feature-auth.md
        r'ai_docs/[A-Za-z0-9_/-]+\.md',     # ai_docs/architecture.md
        r'app_docs/[A-Za-z0-9_/-]+\.md',    # app_docs/setup.md
        r'[A-Za-z0-9_/-]+\.md',             # any-file.md or path/to/file.md
    ]

    # Collect all text to search: body + comments
    texts_to_search = []

    # 1. Issue body
    if issue.body:
        texts_to_search.append(("body", issue.body))

    # 2. Issue comments (newest first, skip ADW bot comments)
    from adw_modules.github import ADW_BOT_IDENTIFIER
    if hasattr(issue, 'comments') and issue.comments:
        sorted_comments = sorted(issue.comments, key=lambda c: c.created_at, reverse=True)
        for i, comment in enumerate(sorted_comments):
            # Skip ADW bot comments to prevent loops
            if ADW_BOT_IDENTIFIER not in comment.body:
                texts_to_search.append((f"comment #{i+1}", comment.body))

    # Extract all potential file references from all sources
    file_references = set()
    for source, text in texts_to_search:
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                logger.info(f"Found {len(matches)} file reference(s) in {source}")
                file_references.update(matches)

    logger.info(f"Total: {len(file_references)} unique file reference(s) from issue body + comments")

    # Token optimization: Limit files (configured in config.yml)
    max_file_refs = get_token_optimization_config()["max_file_references"]
    if len(file_references) > max_file_refs:
        logger.info(f"Limiting file references from {len(file_references)} to {max_file_refs} for token optimization")
        file_references = set(list(file_references)[:max_file_refs])

    # Try to load each file
    for file_ref in file_references:
        # Try multiple locations
        possible_paths = [
            os.path.join(search_dir, file_ref),              # Direct path
            os.path.join(search_dir, "specs", file_ref),     # In specs/
            os.path.join(search_dir, "ai_docs", file_ref),   # In ai_docs/
            os.path.join(search_dir, "ai_docs/doc", file_ref),  # In ai_docs/doc/ ← ADDED
            os.path.join(search_dir, "app_docs", file_ref),  # In app_docs/
        ]

        for file_path in possible_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Token optimization: Limit file size (Task #13)
                        if len(content) > MAX_FILE_REFERENCE_SIZE:
                            original_size = len(content)
                            content = content[:MAX_FILE_REFERENCE_SIZE] + f"\n\n[TRUNCATED - file exceeds {MAX_FILE_REFERENCE_SIZE} chars, showing first {MAX_FILE_REFERENCE_SIZE} of {original_size}]"
                            logger.info(f"✓ Loaded referenced file (truncated): {file_ref} ({original_size} → {len(content)} chars)")
                        else:
                            logger.info(f"✓ Loaded referenced file: {file_ref} ({len(content)} chars)")

                        loaded_files[file_ref] = content
                        break  # Found and loaded, skip other paths
                except Exception as e:
                    logger.warning(f"Failed to read {file_path}: {e}")
        else:
            # File not found in any location
            logger.warning(f"✗ Referenced file not found: {file_ref}")

    if loaded_files:
        logger.info(f"Successfully loaded {len(loaded_files)} files from issue references")
    else:
        logger.info("No files loaded from issue references")

    return loaded_files


def format_file_references_for_context(file_references: dict[str, str]) -> str:
    """Format loaded file references as context for agent prompts.

    Args:
        file_references: Dict mapping file paths to content

    Returns:
        Formatted string to append to agent context
    """
    if not file_references:
        return ""

    context_parts = ["\n\n## Referenced Files from Issue\n"]

    for file_path, content in file_references.items():
        context_parts.append(f"\n### {file_path}\n")
        context_parts.append(f"```markdown\n{content}\n```\n")

    return "".join(context_parts)


# ============================================================================
# Context Bundles - Token Optimization (TAC)
# ============================================================================

def get_context_bundle_path(adw_id: str) -> str:
    """Get path to context bundle directory for an ADW execution."""
    return os.path.join("agents", "context_bundles", adw_id)


def create_context_bundle(
    adw_id: str,
    issue: GitHubIssue,
    logger: logging.Logger
) -> bool:
    """Create initial context bundle with issue facts."""
    bundle_dir = get_context_bundle_path(adw_id)

    try:
        os.makedirs(bundle_dir, exist_ok=True)

        issue_facts = f"""# Issue Facts (ADW: {adw_id})

**Issue #:** {issue.number}
**Title:** {issue.title}
**Type:** {issue.labels if hasattr(issue, 'labels') else 'N/A'}

## Requirements Summary
{issue.body[:500] if issue.body else 'No description'}...

*Full issue available in GitHub - reference by ID #{issue.number}*
"""
        with open(os.path.join(bundle_dir, "issue_facts.md"), 'w', encoding='utf-8') as f:
            f.write(issue_facts)

        decisions = f"""# Phase Decisions (ADW: {adw_id})

## Planning Phase
- TBD

## Build Phase
- TBD

## Review Phase
- TBD

## Document Phase
- TBD
"""
        with open(os.path.join(bundle_dir, "decisions.md"), 'w', encoding='utf-8') as f:
            f.write(decisions)

        constraints_content = """# Repository Constraints

## Architecture
- Follow existing patterns
- Keep changes minimal
- Test before committing

## Code Standards
- Run linter before commit
- Include tests for new features
- Update docs when needed
"""
        with open(os.path.join(bundle_dir, "repo_constraints.md"), 'w', encoding='utf-8') as f:
            f.write(constraints_content)

        logger.info(f"Created context bundle at: {bundle_dir}")
        return True

    except Exception as e:
        logger.error(f"Failed to create context bundle: {e}")
        return False


def update_context_bundle_decisions(
    adw_id: str,
    phase: str,
    decisions: str,
    logger: logging.Logger
) -> bool:
    """Update context bundle with phase-specific decisions."""
    bundle_dir = get_context_bundle_path(adw_id)
    decisions_path = os.path.join(bundle_dir, "decisions.md")

    try:
        if not os.path.exists(decisions_path):
            logger.warning("Decisions file not found, creating new one")
            create_context_bundle(adw_id, None, logger)

        with open(decisions_path, 'r', encoding='utf-8') as f:
            content = f.read()

        phase_marker = f"## {phase.title()} Phase"
        if phase_marker in content:
            content = content.replace(
                f"{phase_marker}\n- TBD",
                f"{phase_marker}\n{decisions}"
            )
        else:
            content += f"\n\n{phase_marker}\n{decisions}\n"

        with open(decisions_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Updated decisions for {phase} phase")
        return True

    except Exception as e:
        logger.error(f"Failed to update context bundle: {e}")
        return False


def load_context_bundle(
    adw_id: str,
    logger: logging.Logger
) -> Optional[str]:
    """Load context bundle as formatted string for agent consumption."""
    bundle_dir = get_context_bundle_path(adw_id)

    if not os.path.exists(bundle_dir):
        logger.warning(f"Context bundle not found: {bundle_dir}")
        return None

    try:
        parts = []
        for filename in ["issue_facts.md", "decisions.md", "repo_constraints.md"]:
            filepath = os.path.join(bundle_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    parts.append(f.read())

        if not parts:
            return None

        bundle_content = "\n\n---\n\n".join(parts)
        logger.info(f"Loaded context bundle ({len(bundle_content)} chars)")
        return bundle_content

    except Exception as e:
        logger.error(f"Failed to load context bundle: {e}")
        return None


# Agent name constants for TAC
AGENT_EXPERT_ADW = "adw_expert"
AGENT_EXPERT_CLI = "cli_expert"
AGENT_EXPERT_COMMANDS = "commands_expert"
