"""Shared AI Developer Workflow (ADW) operations."""

import glob
import json
import logging
import os
import subprocess
import re
from typing import Tuple, Optional
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
from adw_modules.utils import parse_json, get_target_branch

# Token optimization constants
MAX_ISSUE_BODY_LENGTH = 2000  # Truncate issue body to reduce token usage


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

    prompt = f"""You are a senior software architect making implementation decisions.

## Issue
Title: {issue.title}
Body: {issue.body}
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
    """Implement the plan using /build_w_report command (TAC-10).

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


def detect_relevant_docs(issue: GitHubIssue) -> list[str]:
    """Detect which documentation topics are relevant to a GitHub issue (TAC-9).

    Analyzes the issue title and body to identify relevant documentation topics
    based on keyword matching. This enables automatic context loading for workflows.

    Uses hybrid approach:
    1. Static keyword mapping for common topics
    2. Dynamic scanning of all .md files in ai_docs/ directory

    Args:
        issue: GitHub issue to analyze

    Returns:
        List of detected documentation topic names (e.g., ["authentication", "testing"])

    Example:
        >>> issue = GitHubIssue(title="Add JWT authentication", body="...")
        >>> detect_relevant_docs(issue)
        ["authentication", "api"]
    """
    text = f"{issue.title} {issue.body}".lower()
    topics = []
    topics = []

    # Keyword mapping: doc_topic -> list of keywords that indicate relevance
    doc_keywords = {
        # Technical domains
        "authentication": ["auth", "login", "jwt", "oauth", "session", "credential", "password", "token"],
        "testing": ["test", "pytest", "e2e", "unit test", "integration test", "coverage", "mock"],
        "deployment": ["deploy", "ci/cd", "docker", "kubernetes", "k8s", "container", "helm"],
        "database": ["db", "sql", "postgres", "mysql", "migration", "schema", "query", "orm"],
        "api": ["api", "endpoint", "rest", "graphql", "request", "response", "route"],
        "frontend": ["ui", "component", "react", "vue", "frontend", "css", "html", "tailwind"],
        "backend": ["backend", "server", "microservice", "service", "handler"],
        "security": ["security", "xss", "csrf", "sanitize", "vulnerability", "cve"],
        "performance": ["performance", "optimize", "cache", "latency", "throughput", "bottleneck"],
        "monitoring": ["monitor", "observability", "logging", "metrics", "tracing", "alert"],
        "documentation": ["docs", "documentation", "readme", "guide", "tutorial"],
        "configuration": ["config", "environment", "settings", "variables", ".env"],
        "error_handling": ["error", "exception", "handling", "validation", "retry"],
        "workflows": ["workflow", "pipeline", "automation", "ci", "github action"],
        "data_processing": ["etl", "pipeline", "stream", "batch", "processing", "transform"],

        # Architecture & Design
        "ddd": ["ddd", "domain-driven", "domain driven", "aggregate", "entity", "value object", "bounded context", "ubiquitous language"],
        "ddd_lite": ["ddd lite", "lightweight ddd", "simplified domain", "domain model"],
        "design_patterns": ["pattern", "singleton", "factory", "observer", "strategy", "decorator", "adapter", "facade"],
        "solid": ["solid", "single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion"],

        # AI & SDK
        "anthropic_quick_start": ["anthropic", "claude api", "anthropic api", "claude sdk"],
        "openai_quick_start": ["openai", "gpt", "openai api", "chatgpt"],
        "claude_code_cli_reference": ["claude code", "cli", "command line", "claude cli"],
        "claude_code_sdk": ["claude code sdk", "sdk", "agent sdk"],
        "claude-code-hooks": ["hooks", "claude hooks", "pre-commit", "post-commit", "hook script"],
        "mcp-python-sdk": ["mcp", "model context protocol", "mcp sdk", "mcp server"],

        # Tools & Utilities
        "uv-scripts": ["uv", "uv run", "uv script", "python script", "dependencies"],
        "e2b": ["e2b", "sandbox", "code execution", "environment"],
        "fractal_docs": ["fractal", "fractal documentation", "recursive docs", "documentation structure"],
    }

    # Check each topic's keywords against the issue text
    for doc_topic, keywords in doc_keywords.items():
        if any(keyword in text for keyword in keywords):
            topics.append(doc_topic)

    # DYNAMIC DETECTION: Scan all .md files in ai_docs/ directory
    # This allows detection of custom documentation not in the hardcoded mapping
    try:
        # Find ai_docs directory (should be at project root)
        # Assuming this file is in adws/adw_modules/, go up to project root
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        ai_docs_dir = os.path.join(project_root, "ai_docs")

        if os.path.exists(ai_docs_dir):
            # Scan for all .md files recursively
            for root, dirs, files in os.walk(ai_docs_dir):
                for file in files:
                    if file.endswith(".md"):
                        # Get topic name from filename (without .md extension)
                        topic_name = file[:-3]

                        # Skip if already detected via keyword mapping
                        if topic_name in topics:
                            continue

                        # Check if filename (converted to lowercase with spaces/underscores)
                        # appears in the issue text
                        # Convert: "plan_tasks_Tac_12" -> "plan tasks tac 12"
                        searchable_name = topic_name.lower().replace("_", " ").replace("-", " ")

                        # Also check without common prefixes
                        name_variants = [
                            searchable_name,
                            topic_name.lower(),
                            # Remove common prefixes for matching
                            searchable_name.replace("plan ", "").replace("tac ", ""),
                        ]

                        if any(variant in text for variant in name_variants if variant):
                            topics.append(topic_name)

    except Exception as e:
        # If dynamic scanning fails, just use static keywords
        # Don't fail the whole detection
        pass

    # Remove duplicates and sort for consistency
    return sorted(list(set(topics)))


def scout_codebase(
    query: str,
    adw_id: str,
    logger: logging.Logger,
    scale: str = "medium",
    working_dir: Optional[str] = None,
) -> AgentPromptResponse:
    """Scout codebase using /scout command (TAC-12).

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
    """Create enhanced plan with parallel codebase exploration using /plan_w_scouters (TAC-12).

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
    """Build implementation in parallel using /build_in_parallel (TAC-12).

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
    """Find and summarize code using /find_and_summarize (TAC-12).

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
    patch_file_path = response.output.strip()

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
