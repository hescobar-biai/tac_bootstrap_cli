"""Claude Code agent module for executing prompts programmatically."""

import subprocess
import sys
import os
import json
import re
import logging
import time
import asyncio
from typing import Optional, List, Dict, Any, Tuple, Final
from dotenv import load_dotenv
from .data_types import (
    AgentPromptRequest,
    AgentPromptResponse,
    AgentTemplateRequest,
    ClaudeCodeResultMessage,
    SlashCommand,
    ModelSet,
    RetryCode,
    TokenUsage,
)

# Load environment variables
load_dotenv()


def _get_use_sdk_from_config() -> bool:
    """Load USE_SDK setting from config.yml.

    Reads agentic.use_sdk from config.yml file.
    Falls back to False if config not found or field missing.

    Returns:
        True if SDK mode is enabled, False otherwise
    """
    import yaml

    # Find config.yml in project root (parent of adws/adw_modules/)
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    config_path = os.path.join(project_root, "config.yml")

    if not os.path.exists(config_path):
        return False

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config.get("agentic", {}).get("use_sdk", False)
    except Exception:
        return False


# SDK Feature Flag - enables direct SDK execution instead of subprocess
# Loaded from config.yml agentic.use_sdk (TAC-15)
USE_SDK = _get_use_sdk_from_config()

# Get Claude Code CLI path from environment
CLAUDE_PATH = os.getenv("CLAUDE_CODE_PATH", "claude")

# Model selection mapping for slash commands
# Maps each command to its model configuration for base and heavy model sets
SLASH_COMMAND_MODEL_MAP: Final[Dict[SlashCommand, Dict[ModelSet, str]]] = {
    # Classification and generation (lightweight)
    "/classify_issue": {"base": "sonnet", "heavy": "sonnet"},
    "/classify_adw": {"base": "sonnet", "heavy": "sonnet"},
    "/generate_branch_name": {"base": "sonnet", "heavy": "sonnet"},
    # Implementation (can benefit from opus for complex tasks)
    "/implement": {"base": "sonnet", "heavy": "opus"},
    "/build_w_report": {"base": "sonnet", "heavy": "opus"},  # TAC: Build with YAML report
    # Testing
    "/test": {"base": "sonnet", "heavy": "sonnet"},
    "/resolve_failed_test": {"base": "sonnet", "heavy": "opus"},
    "/test_e2e": {"base": "sonnet", "heavy": "sonnet"},
    "/resolve_failed_e2e_test": {"base": "sonnet", "heavy": "opus"},
    # Review and documentation
    "/review": {"base": "sonnet", "heavy": "sonnet"},
    "/document": {"base": "sonnet", "heavy": "opus"},
    "/in_loop_review": {"base": "sonnet", "heavy": "sonnet"},  # TAC-9: Quick review
    # Git operations (lightweight)
    "/commit": {"base": "sonnet", "heavy": "sonnet"},
    "/pull_request": {"base": "sonnet", "heavy": "sonnet"},
    # Planning (can benefit from opus for complex planning)
    "/chore": {"base": "sonnet", "heavy": "opus"},
    "/bug": {"base": "sonnet", "heavy": "opus"},
    "/feature": {"base": "sonnet", "heavy": "opus"},
    "/patch": {"base": "sonnet", "heavy": "opus"},
    "/quick-plan": {"base": "sonnet", "heavy": "opus"},  # TAC: Rapid planning
    # Worktree and utilities
    "/install_worktree": {"base": "sonnet", "heavy": "sonnet"},
    "/track_agentic_kpis": {"base": "sonnet", "heavy": "sonnet"},
    "/health_check": {"base": "sonnet", "heavy": "sonnet"},  # TAC-9: Health check
    # TAC-9/10: Context and documentation loading
    "/load_ai_docs": {"base": "sonnet", "heavy": "sonnet"},  # TAC-9: Load AI docs
    "/load_bundle": {"base": "sonnet", "heavy": "sonnet"},  # TAC-9: Load context bundle
    "/prime_cc": {"base": "sonnet", "heavy": "sonnet"},  # TAC-9: Claude Code priming
    # TAC: Agent delegation (opus for complex orchestration)
    "/background": {"base": "sonnet", "heavy": "opus"},  # TAC: Background delegation
    "/parallel_subagents": {"base": "sonnet", "heavy": "opus"},  # TAC: Parallel agents
    # TAC: Meta-prompting (opus for prompt generation)
    "/t_metaprompt_workflow": {"base": "sonnet", "heavy": "opus"},  # TAC: Meta-prompt
    # TAC: Exploration and clarification (lightweight)
    "/scout": {"base": "sonnet", "heavy": "sonnet"},  # TAC: Scout command for exploration
    "/question": {"base": "sonnet", "heavy": "sonnet"},  # TAC: Question command for clarification
    # TAC: Planning and orchestration
    "/all_tools": {"base": "haiku", "heavy": "haiku"},
    "/build": {"base": "sonnet", "heavy": "sonnet"},
    "/build_in_parallel": {"base": "sonnet", "heavy": "opus"},
    "/find_and_summarize": {"base": "sonnet", "heavy": "sonnet"},
    "/load_ai_docs": {"base": "sonnet", "heavy": "sonnet"},
    "/load_bundle": {"base": "haiku", "heavy": "sonnet"},
    "/parallel_subagents": {"base": "sonnet", "heavy": "opus"},
    "/plan": {"base": "opus", "heavy": "opus"},
    "/plan_w_docs": {"base": "sonnet", "heavy": "opus"},
    "/plan_w_scouters": {"base": "sonnet", "heavy": "opus"},
    "/prime_3": {"base": "sonnet", "heavy": "sonnet"},
    "/prime_cc": {"base": "sonnet", "heavy": "sonnet"},
    "/scout_plan_build": {"base": "sonnet", "heavy": "opus"},
}


def get_model_for_slash_command(
    request: AgentTemplateRequest, default: str = "sonnet"
) -> str:
    """Get the appropriate model for a template request based on ADW state and slash command.

    This function loads the ADW state to determine the model set (base or heavy)
    and returns the appropriate model for the slash command.

    Args:
        request: The template request containing the slash command and adw_id
        default: Default model if not found in mapping

    Returns:
        Model name to use (e.g., "sonnet" or "opus")
    """
    # Import here to avoid circular imports
    from .state import ADWState

    # Load state to get model_set
    model_set: ModelSet = "base"  # Default model set
    state = ADWState.load(request.adw_id)
    if state:
        model_set = state.get("model_set", "base")

    # Get the model configuration for the command
    command_config = SLASH_COMMAND_MODEL_MAP.get(request.slash_command)

    if command_config:
        # Get the model for the specified model set, defaulting to base if not found
        return command_config.get(model_set, command_config.get("base", default))

    return default


def truncate_output(
    output: str, max_length: int = 500, suffix: str = "... (truncated)"
) -> str:
    """Truncate output to a reasonable length for display.

    Special handling for JSONL data - if the output appears to be JSONL,
    try to extract just the meaningful part.

    Args:
        output: The output string to truncate
        max_length: Maximum length before truncation (default: 500)
        suffix: Suffix to add when truncated (default: "... (truncated)")

    Returns:
        Truncated string if needed, original if shorter than max_length
    """
    # Check if this looks like JSONL data
    if output.startswith('{"type":') and '\n{"type":' in output:
        # This is likely JSONL output - try to extract the last meaningful message
        lines = output.strip().split("\n")
        for line in reversed(lines):
            try:
                data = json.loads(line)
                # Look for result message
                if data.get("type") == "result":
                    result = data.get("result", "")
                    if result:
                        return truncate_output(result, max_length, suffix)
                # Look for assistant message
                elif data.get("type") == "assistant" and data.get("message"):
                    content = data["message"].get("content", [])
                    if isinstance(content, list) and content:
                        text = content[0].get("text", "")
                        if text:
                            return truncate_output(text, max_length, suffix)
            except:
                pass
        # If we couldn't extract anything meaningful, just show that it's JSONL
        return f"[JSONL output with {len(lines)} messages]{suffix}"

    # Regular truncation logic
    if len(output) <= max_length:
        return output

    # Try to find a good break point (newline or space)
    truncate_at = max_length - len(suffix)

    # Look for newline near the truncation point
    newline_pos = output.rfind("\n", truncate_at - 50, truncate_at)
    if newline_pos > 0:
        return output[:newline_pos] + suffix

    # Look for space near the truncation point
    space_pos = output.rfind(" ", truncate_at - 20, truncate_at)
    if space_pos > 0:
        return output[:space_pos] + suffix

    # Just truncate at the limit
    return output[:truncate_at] + suffix


def check_claude_installed() -> Optional[str]:
    """Check if Claude Code CLI is installed. Return error message if not."""
    try:
        result = subprocess.run(
            [CLAUDE_PATH, "--version"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return (
                f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
            )
    except FileNotFoundError:
        return f"Error: Claude Code CLI is not installed. Expected at: {CLAUDE_PATH}"
    return None


def parse_jsonl_output(
    output_file: str,
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]], Optional[TokenUsage]]:
    """Parse JSONL output file and return all messages, result message, and token usage.

    Returns:
        Tuple of (all_messages, result_message, token_usage) where result_message and
        token_usage are None if not found
    """
    try:
        with open(output_file, "r") as f:
            # Read all lines and parse each as JSON
            messages = [json.loads(line) for line in f if line.strip()]

            # Find the result message (should be the last one)
            result_message = None
            token_usage = None
            for message in reversed(messages):
                if message.get("type") == "result":
                    result_message = message
                    # Extract token usage from result message
                    usage = message.get("usage", {})
                    model_usage = message.get("modelUsage", {})
                    token_usage = TokenUsage(
                        input_tokens=usage.get("input_tokens", 0),
                        output_tokens=usage.get("output_tokens", 0),
                        cache_creation_input_tokens=usage.get("cache_creation_input_tokens", 0),
                        cache_read_input_tokens=usage.get("cache_read_input_tokens", 0),
                        total_cost_usd=message.get("total_cost_usd", 0.0),
                        duration_ms=message.get("duration_ms", 0),
                        model_usage=model_usage,
                    )
                    break

            return messages, result_message, token_usage
    except Exception as e:
        return [], None, None


def convert_jsonl_to_json(jsonl_file: str) -> str:
    """Convert JSONL file to JSON array file.

    Creates a .json file with the same name as the .jsonl file,
    containing all messages as a JSON array.

    Returns:
        Path to the created JSON file
    """
    # Create JSON filename by replacing .jsonl with .json
    json_file = jsonl_file.replace(".jsonl", ".json")

    # Parse the JSONL file
    messages, _, _ = parse_jsonl_output(jsonl_file)

    # Write as JSON array
    with open(json_file, "w") as f:
        json.dump(messages, f, indent=2)

    return json_file


def get_claude_env() -> Dict[str, str]:
    """Get only the required environment variables for Claude Code execution.

    This is a wrapper around get_safe_subprocess_env() from utils.py for
    backward compatibility. New code should use get_safe_subprocess_env() directly.

    Returns a dictionary containing only the necessary environment variables
    based on .env.sample configuration.
    """
    # Import here to avoid circular imports
    from .utils import get_safe_subprocess_env

    # Use the shared function
    return get_safe_subprocess_env()


def save_prompt(prompt: str, adw_id: str, agent_name: str = "ops") -> None:
    """Save a prompt to the appropriate logging directory."""
    # Extract slash command from prompt
    match = re.match(r"^(/\w+)", prompt)
    if not match:
        return

    slash_command = match.group(1)
    # Remove leading slash for filename
    command_name = slash_command[1:]

    # Create directory structure at project root (parent of adws)
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    prompt_dir = os.path.join(project_root, "agents", adw_id, agent_name, "prompts")
    os.makedirs(prompt_dir, exist_ok=True)

    # Save prompt to file
    prompt_file = os.path.join(prompt_dir, f"{command_name}.txt")
    with open(prompt_file, "w") as f:
        f.write(prompt)


def get_retry_logger(adw_id: str) -> logging.Logger:
    """Get or create a logger for retry operations."""
    logger = logging.getLogger(f"adw.{adw_id}.retry")
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def calculate_backoff_delay(
    attempt: int,
    base_delay: int = 5,
    max_delay: int = 120,
    retry_code: RetryCode = RetryCode.NONE
) -> int:
    """Calculate exponential backoff delay with jitter.

    Args:
        attempt: Current retry attempt number (1-based)
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap in seconds
        retry_code: The error type to adjust delays for

    Returns:
        Delay in seconds before next retry
    """
    import random

    # For rate limiting, use longer base delays
    if retry_code == RetryCode.RATE_LIMITED:
        base_delay = 30  # Start with 30 seconds for rate limiting
        max_delay = 300  # Cap at 5 minutes

    # Exponential backoff: base * 2^attempt
    delay = base_delay * (2 ** (attempt - 1))

    # Add jitter (±20%) to prevent thundering herd
    jitter = delay * 0.2 * (random.random() * 2 - 1)
    delay = int(delay + jitter)

    # Cap at max delay
    return min(delay, max_delay)


def is_rate_limited_error(error_msg: str) -> bool:
    """Check if an error message indicates rate limiting."""
    rate_limit_indicators = [
        "overloaded",
        "rate limit",
        "rate_limit",
        "429",
        "too many requests",
        "throttl",
        "capacity",
        "try again later",
    ]
    error_lower = error_msg.lower()
    return any(indicator in error_lower for indicator in rate_limit_indicators)


def is_connection_error(error_msg: str) -> bool:
    """Check if an error message indicates a connection problem."""
    connection_indicators = [
        "connection",
        "network",
        "timeout",
        "timed out",
        "unreachable",
        "dns",
        "socket",
        "econnrefused",
        "econnreset",
        "enotfound",
    ]
    error_lower = error_msg.lower()
    return any(indicator in error_lower for indicator in connection_indicators)


def is_quota_exhausted_error(error_msg: str) -> bool:
    """Check if an error message indicates quota/usage limit exhausted.

    This is different from rate limiting - quota exhausted means the user
    has hit their usage limit and needs to wait for reset or use a different model.
    """
    error_lower = error_msg.lower()

    # Specific quota exhaustion patterns
    quota_indicators = [
        "hit your limit",
        "limit reached",
        "usage limit",
        "quota exceeded",
        "quota exhausted",
        "monthly limit",
        "daily limit",
        "credit balance",
        "insufficient credits",
    ]

    # Check for basic indicators
    if any(indicator in error_lower for indicator in quota_indicators):
        return True

    # Check for "resets" only when accompanied by "limit" or "quota"
    if "resets" in error_lower and ("limit" in error_lower or "quota" in error_lower):
        return True

    return False


# =============================================================================
# SDK BRIDGE FUNCTIONS
# =============================================================================


def _classify_sdk_error(error_msg: str) -> RetryCode:
    """Classify an SDK error message to determine retry behavior.

    Reuses existing error classification functions to maintain consistency
    between subprocess and SDK execution paths.

    Args:
        error_msg: The error message from SDK execution

    Returns:
        Appropriate RetryCode for the error type
    """
    if is_quota_exhausted_error(error_msg):
        return RetryCode.QUOTA_EXHAUSTED
    elif is_rate_limited_error(error_msg):
        return RetryCode.RATE_LIMITED
    elif is_connection_error(error_msg):
        return RetryCode.CONNECTION_ERROR
    elif "api" in error_msg.lower() and "error" in error_msg.lower():
        return RetryCode.API_ERROR
    elif "timeout" in error_msg.lower():
        return RetryCode.TIMEOUT_ERROR
    else:
        return RetryCode.EXECUTION_ERROR


def _convert_sdk_token_usage(sdk_usage: Any, duration_seconds: float) -> TokenUsage:
    """Convert SDK TokenUsage to our data_types.TokenUsage format.

    Args:
        sdk_usage: TokenUsage from adw_agent_sdk (Pydantic model)
        duration_seconds: Duration of the query in seconds

    Returns:
        Our TokenUsage dataclass with mapped fields
    """
    if sdk_usage is None:
        return TokenUsage(
            input_tokens=0,
            output_tokens=0,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            total_cost_usd=0.0,
            duration_ms=int(duration_seconds * 1000),
            model_usage={},
        )

    return TokenUsage(
        input_tokens=getattr(sdk_usage, "input_tokens", 0),
        output_tokens=getattr(sdk_usage, "output_tokens", 0),
        cache_creation_input_tokens=getattr(sdk_usage, "cache_creation_input_tokens", 0),
        cache_read_input_tokens=getattr(sdk_usage, "cache_read_input_tokens", 0),
        total_cost_usd=getattr(sdk_usage, "total_cost_usd", 0.0) or 0.0,
        duration_ms=int(duration_seconds * 1000),
        model_usage={},  # SDK doesn't provide per-model breakdown
    )


def _prompt_claude_code_sdk(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Claude Code via SDK instead of subprocess.

    This function provides an alternative execution path using the
    adw_agent_sdk module for direct SDK integration. It produces
    exactly the same AgentPromptResponse type as the subprocess path.

    Features (TAC-15 improvements):
    - max_turns=50 to prevent infinite loops
    - working_dir validation with parity to subprocess path
    - Transcript saving for debugging (sdk_transcript.json)
    - POST_TOOL_USE logging hook for tool visibility

    Args:
        request: The prompt request configuration

    Returns:
        AgentPromptResponse with output or error, matching subprocess behavior
    """
    # Lazy import to avoid loading SDK when not needed
    from .adw_agent_sdk import (
        QueryInput,
        QueryOptions,
        ModelName,
        SettingSource,
        MessageHandlers,
        HookEventName,
        HooksConfig,
        HookMatcher,
        HookResponse,
        query_to_completion,
    )

    logger = get_retry_logger(request.adw_id)

    # TAC-15: Validate working_dir (parity with subprocess path)
    # Read-only agents that don't create files - no warning needed
    read_only_agents = {
        "clarifier",
        "resolver",
        "classifier",
        "branch_generator",
        "branch_name_generator",
        "issue_classifier",
        "adw_classifier",
        "docs_loader",
        "doc_summarizer",
        "codebase_scout",
    }

    effective_cwd = request.working_dir
    if effective_cwd:
        if not os.path.isdir(effective_cwd):
            return AgentPromptResponse(
                output=f"Error: working_dir does not exist: {effective_cwd}",
                success=False,
                session_id=None,
                retry_code=RetryCode.NONE,
            )
    else:
        # Only warn for agents that create files (not read-only agents)
        if request.agent_name not in read_only_agents:
            logger.warning(
                f"⚠️ SDK: No working_dir provided for {request.agent_name} - "
                f"executing in current directory. This may cause files to be created in main repo!"
            )

    # Map model string to ModelName enum
    model_map = {
        "opus": ModelName.OPUS,
        "sonnet": ModelName.SONNET,
        "haiku": ModelName.HAIKU,
    }
    sdk_model = model_map.get(request.model.lower(), ModelName.SONNET)

    # TAC-15: Optional POST_TOOL_USE logging hook for tool visibility
    # Disabled by default as it may cause issues with some SDK versions
    # Enable with SDK_ENABLE_HOOKS=1 environment variable
    hooks_config = None
    if os.getenv("SDK_ENABLE_HOOKS", "").lower() in ("1", "true", "yes"):
        async def log_tool_use(hook_input, tool_use_id, context):
            """Log tool usage for debugging and visibility."""
            tool_name = getattr(hook_input, 'tool_name', 'unknown')
            tool_input = getattr(hook_input, 'tool_input', {})
            tool_response = getattr(hook_input, 'tool_response', None)

            # Truncate response for logging
            response_preview = str(tool_response)[:200] if tool_response else "N/A"
            if len(str(tool_response or "")) > 200:
                response_preview += "..."

            logger.debug(f"🔧 SDK Tool: {tool_name}")
            logger.debug(f"   Input: {str(tool_input)[:100]}")
            logger.debug(f"   Response: {response_preview}")

            return HookResponse.allow()

        hooks_config = HooksConfig.from_callbacks({
            HookEventName.POST_TOOL_USE: [log_tool_use],
        })

    # Build QueryOptions matching subprocess behavior
    # Include resume session ID if provided for context persistence
    # TAC-15: Add max_turns=50 to prevent infinite loops
    options = QueryOptions(
        model=sdk_model,
        cwd=effective_cwd,
        bypass_permissions=request.dangerously_skip_permissions,
        setting_sources=[SettingSource.PROJECT],
        resume=request.resume_session_id if request.resume_session_id else None,
        max_turns=50,  # TAC-15: Prevent infinite loops
        hooks=hooks_config,  # TAC-15: Tool visibility logging (optional)
    )

    # Create QueryInput
    query_input = QueryInput(
        prompt=request.prompt,
        options=options,
    )

    try:
        # Execute via SDK with timeout
        result = asyncio.run(
            asyncio.wait_for(
                query_to_completion(query_input),
                timeout=request.timeout_seconds
            )
        )

        # Convert SDK result to AgentPromptResponse
        duration_seconds = result.duration_seconds or 0.0
        token_usage = _convert_sdk_token_usage(result.usage, duration_seconds)

        # TAC-15: Save SDK transcript to agents/{adw_id}/{agent_name}/sdk_transcript.json
        if result.messages:
            try:
                # __file__ is in adws/adw_modules/, go up 3 levels to project root
                project_root = os.path.dirname(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
                transcript_dir = os.path.join(
                    project_root, "agents", request.adw_id, request.agent_name
                )
                os.makedirs(transcript_dir, exist_ok=True)
                transcript_path = os.path.join(transcript_dir, "sdk_transcript.json")

                # Convert messages to JSON-serializable format
                messages_data = [
                    msg.model_dump() if hasattr(msg, "model_dump") else str(msg)
                    for msg in result.messages
                ]
                with open(transcript_path, "w") as f:
                    json.dump(messages_data, f, indent=2, default=str)
            except Exception:
                # Transcript saving is optional - don't fail the request
                pass

        if result.success:
            return AgentPromptResponse(
                output=result.result or "",
                success=True,
                session_id=result.session_id,
                retry_code=RetryCode.NONE,
                token_usage=token_usage,
            )
        else:
            # Classify the error for retry logic
            # TAC-15: SDK puts error message in result.result when success=False
            # result.error may be None even when there's an error
            error_msg = result.error or result.result or "Unknown SDK error"
            retry_code = _classify_sdk_error(error_msg)

            return AgentPromptResponse(
                output=truncate_output(error_msg, max_length=800),
                success=False,
                session_id=result.session_id,
                retry_code=retry_code,
                token_usage=token_usage,
            )

    except asyncio.TimeoutError:
        timeout_mins = request.timeout_seconds // 60
        error_msg = f"Error: SDK query timed out after {timeout_mins} minutes ({request.timeout_seconds}s)"
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None,
            retry_code=RetryCode.TIMEOUT_ERROR,
        )
    except Exception as e:
        error_msg = f"SDK execution error: {e}"
        retry_code = _classify_sdk_error(str(e))
        return AgentPromptResponse(
            output=truncate_output(error_msg, max_length=800),
            success=False,
            session_id=None,
            retry_code=retry_code,
        )


# Model fallback chain: opus -> sonnet -> haiku -> retry_with_degradation
# When all models exhausted, implements intelligent degradation strategies:
# 1. Exponential backoff (30s, 60s, 120s, 300s)
# 2. Context reduction (strip non-critical fields)
# 3. Aggressive caching (reuse previous results)
# 4. Return best-effort result instead of failing
MODEL_FALLBACK_CHAIN: Final[Dict[str, Optional[str]]] = {
    "opus": "sonnet",
    "sonnet": "haiku",
    "haiku": "haiku",  # Try haiku again with degradation (not None)
}


def get_fallback_model(current_model: str) -> Optional[str]:
    """Get the fallback model for the current model.

    Returns None if there's no fallback available (already at lowest tier).
    """
    return MODEL_FALLBACK_CHAIN.get(current_model)


def prompt_claude_code_with_retry(
    request: AgentPromptRequest,
    max_retries: int = 15,
    base_delay: int = 5,
) -> AgentPromptResponse:
    """Execute Claude Code with intelligent retry logic and model fallback.

    Features:
    - Exponential backoff with jitter for transient errors
    - Longer delays for rate limiting (starts at 30s)
    - Automatic model fallback when quota is exhausted (opus -> sonnet -> haiku)
    - Fast fail when ALL models are quota-exhausted (no pointless waiting)
    - Detailed logging during retries

    Args:
        request: The prompt request configuration
        max_retries: Maximum number of retry attempts for transient errors (default: 15)
        base_delay: Base delay in seconds for exponential backoff (default: 5)

    Returns:
        AgentPromptResponse with output or error
    """
    logger = get_retry_logger(request.adw_id)
    original_model = request.model
    current_model = request.model
    current_request = request

    # Track which models have been quota-exhausted to avoid pointless retries
    exhausted_models: set = set()

    # Retryable error codes (not including QUOTA_EXHAUSTED - that triggers model fallback)
    retryable_codes = [
        RetryCode.CLAUDE_CODE_ERROR,
        RetryCode.TIMEOUT_ERROR,
        RetryCode.EXECUTION_ERROR,
        RetryCode.ERROR_DURING_EXECUTION,
        RetryCode.RATE_LIMITED,
        RetryCode.CONNECTION_ERROR,
        RetryCode.API_ERROR,
    ]

    attempt = 0

    while attempt <= max_retries:
        # Execute the request
        response = prompt_claude_code(current_request)

        # Success - return immediately
        if response.success:
            if attempt > 0 or current_model != original_model:
                logger.info(f"✅ Succeeded on attempt {attempt + 1} with model {current_model}")
            return response

        # Non-retryable error
        if response.retry_code == RetryCode.NONE:
            logger.error(f"❌ Non-retryable error: {response.output[:200]}")
            return response

        # Quota exhausted - try fallback model or fail fast
        if response.retry_code == RetryCode.QUOTA_EXHAUSTED:
            logger.warning(f"📋 Quota exhausted (model={current_model}): {response.output[:300]}")
            exhausted_models.add(current_model)

            fallback_model = get_fallback_model(current_model)

            # Try next model in fallback chain (only if not already exhausted)
            if fallback_model and fallback_model != current_model and fallback_model not in exhausted_models:
                logger.warning(
                    f"🔄 Model {current_model} quota exhausted, falling back to {fallback_model}"
                )
                current_model = fallback_model
                current_request = current_request.model_copy(update={"model": current_model})
                logger.info(f"🎯 Request model updated to: {current_request.model}")
                time.sleep(2)
                # Don't increment attempt - model switch is free
                continue

            # ALL models exhausted - fail fast with clear message
            all_models = set(MODEL_FALLBACK_CHAIN.keys())
            logger.error(
                f"❌ All models quota exhausted: {exhausted_models}. "
                f"Cannot continue - quota reset needed."
            )
            logger.error(f"   Error: {response.output[:500]}")
            return AgentPromptResponse(
                output=response.output,
                success=False,
                session_id=response.session_id,
                retry_code=RetryCode.QUOTA_EXHAUSTED,
                token_usage=response.token_usage,
            )

        # Check if this is a retryable error (transient)
        if response.retry_code in retryable_codes:
            attempt += 1
            if attempt > max_retries:
                logger.error(
                    f"❌ Max retries ({max_retries}) exhausted. "
                    f"Last error: {response.retry_code.value}"
                )
                return response

            # Calculate delay based on error type
            delay = calculate_backoff_delay(
                attempt,
                base_delay,
                retry_code=response.retry_code
            )

            logger.warning(
                f"⚠️ Retryable error ({response.retry_code.value}): "
                f"{response.output[:100]}..."
            )
            logger.warning(
                f"⏳ Retry {attempt}/{max_retries} in {delay}s (model: {current_model})"
            )

            # Log progress during long waits
            if delay > 30:
                for waited in range(0, delay, 30):
                    remaining = delay - waited
                    if remaining > 30:
                        logger.info(f"   Waiting... {remaining}s remaining")
                        time.sleep(30)
                    else:
                        time.sleep(remaining)
                        break
            else:
                time.sleep(delay)

            logger.info(f"🔄 Retrying attempt {attempt + 1} with model {current_model}...")
            continue

        # Unknown error code - return as-is
        return response

    # Should not reach here, but return last response just in case
    return response


def prompt_claude_code(request: AgentPromptRequest) -> AgentPromptResponse:
    """Execute Claude Code with the given prompt configuration."""

    # Check if Claude Code CLI is installed
    error_msg = check_claude_installed()
    if error_msg:
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None,
            retry_code=RetryCode.NONE,  # Installation error is not retryable
        )

    # Save prompt before execution
    save_prompt(request.prompt, request.adw_id, request.agent_name)

    # SDK dispatch: use SDK execution path if feature flag is enabled
    if USE_SDK:
        return _prompt_claude_code_sdk(request)

    # TAC-15: Subprocess path requires output_file for JSONL output
    if request.output_file is None:
        return AgentPromptResponse(
            output="Error: output_file is required when USE_SDK=False (subprocess path)",
            success=False,
            session_id=None,
            retry_code=RetryCode.NONE,
        )

    # Create output directory if needed
    output_dir = os.path.dirname(request.output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Build command - always use stream-json format and verbose
    cmd = [CLAUDE_PATH, "-p", request.prompt]
    cmd.extend(["--model", request.model])
    cmd.extend(["--output-format", "stream-json"])
    cmd.append("--no-session-persistence")  # Avoid session state issues with model switching

    # Generate unique session ID to avoid any state caching between requests
    import uuid
    unique_session_id = str(uuid.uuid4())
    cmd.extend(["--session-id", unique_session_id])

    # Debug: log the model being used
    logging.debug(f"🎯 Executing with model: {request.model}")
    cmd.append("--verbose")
    
    # Check for MCP config in working directory
    if request.working_dir:
        mcp_config_path = os.path.join(request.working_dir, ".mcp.json")
        if os.path.exists(mcp_config_path):
            cmd.extend(["--mcp-config", mcp_config_path])

    # Add dangerous skip permissions flag if enabled
    if request.dangerously_skip_permissions:
        cmd.append("--dangerously-skip-permissions")

    # Set up environment with only required variables
    env = get_claude_env()

    # CRITICAL: Validate working_dir to prevent accidental writes to main repo
    effective_cwd = request.working_dir

    # Read-only agents that don't create files - no warning needed
    read_only_agents = {
        "clarifier",
        "resolver",
        "classifier",
        "branch_generator",
        "branch_name_generator",
        "issue_classifier",
        "adw_classifier",
        "docs_loader",  # TAC-9: AI docs loader (read-only)
        "doc_summarizer",  # TAC-9: Documentation summarizer (read-only)
        "codebase_scout",  # TAC: Codebase scout (read-only)
    }

    if effective_cwd:
        if not os.path.isdir(effective_cwd):
            return AgentPromptResponse(
                output=f"Error: working_dir does not exist: {effective_cwd}",
                success=False,
                session_id=None,
                retry_code=RetryCode.NONE,
            )
    else:
        # Only warn for agents that create files (not read-only agents)
        if request.agent_name not in read_only_agents:
            logger = get_retry_logger(request.adw_id)
            logger.warning(
                f"⚠️ No working_dir provided for {request.agent_name} - "
                f"executing in current directory. This may cause files to be created in main repo!"
            )

    try:
        # Open output file for streaming
        with open(request.output_file, "w") as output_f:
            # Execute Claude Code and stream output to file
            # Use timeout from request (default 10 minutes)
            result = subprocess.run(
                cmd,
                stdout=output_f,  # Stream directly to file
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                cwd=effective_cwd,  # Use working_dir if provided
                timeout=request.timeout_seconds,  # Add timeout!
            )

        if result.returncode == 0:

            # Parse the JSONL file
            messages, result_message, token_usage = parse_jsonl_output(request.output_file)

            # Convert JSONL to JSON array file
            json_file = convert_jsonl_to_json(request.output_file)

            if result_message:
                # Extract session_id from result message
                session_id = result_message.get("session_id")

                # Check if there was an error in the result
                is_error = result_message.get("is_error", False)
                subtype = result_message.get("subtype", "")

                # Handle error_during_execution case where there's no result field
                if subtype == "error_during_execution":
                    error_msg = "Error during execution: Agent encountered an error and did not return a result"
                    return AgentPromptResponse(
                        output=error_msg,
                        success=False,
                        session_id=session_id,
                        retry_code=RetryCode.ERROR_DURING_EXECUTION,
                        token_usage=token_usage,
                    )

                result_text = result_message.get("result", "")

                # For error cases, truncate the output to prevent JSONL blobs
                if is_error and len(result_text) > 1000:
                    result_text = truncate_output(result_text, max_length=800)

                # Classify error for retry logic when is_error is True
                # CRITICAL: CLI can return exit code 0 with is_error=true for quota/rate limits
                retry_code = RetryCode.NONE
                if is_error:
                    retry_code = RetryCode.CLAUDE_CODE_ERROR
                    if is_quota_exhausted_error(result_text):
                        retry_code = RetryCode.QUOTA_EXHAUSTED
                    elif is_rate_limited_error(result_text):
                        retry_code = RetryCode.RATE_LIMITED
                    elif is_connection_error(result_text):
                        retry_code = RetryCode.CONNECTION_ERROR

                return AgentPromptResponse(
                    output=result_text,
                    success=not is_error,
                    session_id=session_id,
                    retry_code=retry_code,
                    token_usage=token_usage,
                )
            else:
                # No result message found, try to extract meaningful error
                error_msg = "No result message found in Claude Code output"

                # Try to get the last few lines of output for context
                try:
                    with open(request.output_file, "r") as f:
                        lines = f.readlines()
                        if lines:
                            # Get last 5 lines or less
                            last_lines = lines[-5:] if len(lines) > 5 else lines
                            # Try to parse each as JSON to find any error messages
                            for line in reversed(last_lines):
                                try:
                                    data = json.loads(line.strip())
                                    if data.get("type") == "assistant" and data.get(
                                        "message"
                                    ):
                                        # Extract text from assistant message
                                        content = data["message"].get("content", [])
                                        if isinstance(content, list) and content:
                                            text = content[0].get("text", "")
                                            if text:
                                                error_msg = f"Claude Code output: {text[:500]}"  # Truncate
                                                break
                                except:
                                    pass
                except:
                    pass

                return AgentPromptResponse(
                    output=truncate_output(error_msg, max_length=800),
                    success=False,
                    session_id=None,
                    retry_code=RetryCode.NONE,
                )
        else:
            # Error occurred - stderr is captured, stdout went to file
            stderr_msg = result.stderr.strip() if result.stderr else ""

            # Try to read the output file to check for errors in stdout
            stdout_msg = ""
            error_from_jsonl = None
            try:
                if os.path.exists(request.output_file):
                    # Parse JSONL to find error message
                    messages, result_message, _ = parse_jsonl_output(request.output_file)

                    if result_message and result_message.get("is_error"):
                        # Found error in result message
                        error_from_jsonl = result_message.get("result", "Unknown error")
                    elif messages:
                        # Look for error in last few messages
                        for msg in reversed(messages[-5:]):
                            if msg.get("type") == "assistant" and msg.get(
                                "message", {}
                            ).get("content"):
                                content = msg["message"]["content"]
                                if isinstance(content, list) and content:
                                    text = content[0].get("text", "")
                                    if text and (
                                        "error" in text.lower()
                                        or "failed" in text.lower()
                                    ):
                                        error_from_jsonl = text[:500]  # Truncate
                                        break

                    # If no structured error found, get last line only
                    if not error_from_jsonl:
                        with open(request.output_file, "r") as f:
                            lines = f.readlines()
                            if lines:
                                # Just get the last line instead of entire file
                                stdout_msg = lines[-1].strip()[
                                    :200
                                ]  # Truncate to 200 chars
            except:
                pass

            if error_from_jsonl:
                error_msg = f"Claude Code error: {error_from_jsonl}"
            elif stdout_msg and not stderr_msg:
                error_msg = f"Claude Code error: {stdout_msg}"
            elif stderr_msg and not stdout_msg:
                error_msg = f"Claude Code error: {stderr_msg}"
            elif stdout_msg and stderr_msg:
                error_msg = f"Claude Code error: {stderr_msg}\nStdout: {stdout_msg}"
            else:
                error_msg = f"Claude Code error: Command failed with exit code {result.returncode}"

            # Determine the appropriate retry code based on error content
            retry_code = RetryCode.CLAUDE_CODE_ERROR

            # Check for quota exhausted (user hit their usage limit)
            if is_quota_exhausted_error(error_msg):
                retry_code = RetryCode.QUOTA_EXHAUSTED
                # Debug: log error message for quota detection verification
                logging.debug(f"Quota exhausted detected from error: {error_msg[:200]}")
            # Check for rate limiting (temporary, can retry)
            elif is_rate_limited_error(error_msg):
                retry_code = RetryCode.RATE_LIMITED
            # Check for connection errors
            elif is_connection_error(error_msg):
                retry_code = RetryCode.CONNECTION_ERROR
            # Check for API errors
            elif "api" in error_msg.lower() and "error" in error_msg.lower():
                retry_code = RetryCode.API_ERROR

            # Always truncate error messages to prevent huge outputs
            return AgentPromptResponse(
                output=truncate_output(error_msg, max_length=800),
                success=False,
                session_id=None,
                retry_code=retry_code,
            )

    except subprocess.TimeoutExpired:
        timeout_mins = request.timeout_seconds // 60
        error_msg = f"Error: Claude Code command timed out after {timeout_mins} minutes ({request.timeout_seconds}s)"
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None,
            retry_code=RetryCode.TIMEOUT_ERROR,
        )
    except OSError as e:
        # OSError often indicates connection/network issues
        error_msg = f"OS/Network error executing Claude Code: {e}"
        retry_code = RetryCode.CONNECTION_ERROR if is_connection_error(str(e)) else RetryCode.EXECUTION_ERROR
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None,
            retry_code=retry_code,
        )
    except Exception as e:
        error_msg = f"Error executing Claude Code: {e}"
        # Try to classify the error
        error_str = str(e)
        if is_quota_exhausted_error(error_str):
            retry_code = RetryCode.QUOTA_EXHAUSTED
        elif is_rate_limited_error(error_str):
            retry_code = RetryCode.RATE_LIMITED
        elif is_connection_error(error_str):
            retry_code = RetryCode.CONNECTION_ERROR
        else:
            retry_code = RetryCode.EXECUTION_ERROR
        return AgentPromptResponse(
            output=error_msg,
            success=False,
            session_id=None,
            retry_code=retry_code,
        )


def execute_prompt(
    request: AgentPromptRequest,
    logger: Optional[logging.Logger] = None,
) -> AgentPromptResponse:
    """Execute a raw prompt through Claude Code (not a slash command).

    This is useful for custom prompts that don't map to a slash command,
    such as the clarification analysis prompt.

    Args:
        request: The prompt request configuration
        logger: Optional logger for debug output

    Returns:
        AgentPromptResponse with the result
    """
    if logger:
        logger.debug(f"Executing prompt for {request.agent_name}")

    # TAC-15: Create output directory only if output_file is provided
    if request.output_file:
        output_dir = os.path.dirname(request.output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    # Execute with retry logic
    return prompt_claude_code_with_retry(request)


def execute_template(request: AgentTemplateRequest) -> AgentPromptResponse:
    """Execute a Claude Code template with slash command and arguments.

    This function automatically selects the appropriate model based on:
    1. The model explicitly set in the request (takes priority)
    2. The slash command being executed
    3. The model_set stored in the ADW state (base or heavy)

    Example:
        request = AgentTemplateRequest(
            agent_name="planner",
            slash_command="/implement",
            args=["plan.md"],
            adw_id="abc12345"
        )
        # If state has model_set="heavy", this will use "opus"
        # If state has model_set="base" or missing, this will use "sonnet"
        response = execute_template(request)
    """
    # Get the appropriate model for this request
    # IMPORTANT: If model is already explicitly set, respect it
    if request.model:
        mapped_model = request.model
    else:
        mapped_model = get_model_for_slash_command(request)
    request = request.model_copy(update={"model": mapped_model})

    # Construct prompt from slash command and args
    prompt = f"{request.slash_command} {' '.join(request.args)}"

    # Inject AI docs context if available (TAC-9)
    # CRITICAL: Append docs AFTER command to ensure command instructions take priority
    if request.ai_docs_context:
        docs_suffix = f"""

---

# 📚 Available Project Documentation

The following documentation has been loaded to inform your decisions.
Use it to align your work with project standards, patterns, and best practices.

{request.ai_docs_context}

---

**REMINDER**: Follow the command instructions above. The documentation is for reference only.
"""
        prompt = prompt + docs_suffix

    # CRITICAL: Add worktree reminder at the VERY END if working_dir is specified
    # This ensures it's the last thing the agent reads before execution
    if request.working_dir:
        worktree_reminder = f"""

---

# 🚨 CRITICAL WORKING DIRECTORY INSTRUCTION

**YOU ARE WORKING IN AN ISOLATED WORKTREE, NOT THE MAIN REPOSITORY**

- **Working Directory**: `{request.working_dir}`
- **DO NOT make changes to the main repository**
- **ALL file operations (Read, Write, Edit, Glob, Grep) happen in the worktree**
- **The worktree is a separate directory - changes here do NOT affect main**
- **Git operations (status, add, commit) will be run in this worktree**

**When you see relative paths like `specs/plan.md`, they resolve to `{request.working_dir}/specs/plan.md`**

This is a safety feature to isolate development work. All your changes will be reviewed before merging to main.

---
"""
        prompt = prompt + worktree_reminder

    # TAC-15: Conditionally set output_file based on USE_SDK
    if USE_SDK:
        # SDK path: no JSONL output file needed
        output_file = None
    else:
        # Subprocess path: create output directory with adw_id at project root
        # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        output_dir = os.path.join(
            project_root, "agents", request.adw_id, request.agent_name
        )
        os.makedirs(output_dir, exist_ok=True)

        # Build output file path
        output_file = os.path.join(output_dir, "raw_output.jsonl")

    # Create prompt request with specific parameters
    prompt_request = AgentPromptRequest(
        prompt=prompt,
        adw_id=request.adw_id,
        agent_name=request.agent_name,
        model=request.model,
        dangerously_skip_permissions=True,
        output_file=output_file,
        working_dir=request.working_dir,  # Pass through working_dir
        resume_session_id=request.resume_session_id,  # TAC-15: SDK session persistence
    )

    # Execute with retry logic and return response (prompt_claude_code now handles all parsing)
    return prompt_claude_code_with_retry(prompt_request)
