"""Utility functions for ADW system."""

import json
import logging
import os
import re
import sys
import uuid
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar, Type, Union, Dict, Optional

T = TypeVar('T')


def make_adw_id() -> str:
    """Generate a short 8-character UUID for ADW tracking."""
    return str(uuid.uuid4())[:8]


def strip_code_fences(text: str) -> str:
    """Strip markdown code fences from LLM output that should be a plain value."""
    text = text.strip()
    text = re.sub(r"^```\w*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()


def get_target_branch(config_path: str = None) -> str:
    """Get target branch from config.yml, default to 'main'.

    Args:
        config_path: Path to config.yml file. If None, searches in project root.

    Returns:
        Target branch name (e.g., 'main', 'master', 'develop')
    """
    try:
        import yaml
        if config_path is None:
            # Find config.yml in project root (parent of adws/adw_modules/)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            config_path = os.path.join(project_root, "config.yml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get("agentic", {}).get("target_branch", "main")
    except Exception:
        return "main"


def setup_logger(adw_id: str, trigger_type: str = "adw_plan_build") -> logging.Logger:
    """Set up logger that writes to both console and file using adw_id.
    
    Args:
        adw_id: The ADW workflow ID
        trigger_type: Type of trigger (adw_plan_build, trigger_webhook, etc.)
    
    Returns:
        Configured logger instance
    """
    # Create log directory: agents/{adw_id}/adw_plan_build/
    # __file__ is in adws/adw_modules/, so we need to go up 3 levels to get to project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_dir = os.path.join(project_root, "agents", adw_id, trigger_type)
    os.makedirs(log_dir, exist_ok=True)
    
    # Log file path: agents/{adw_id}/adw_plan_build/execution.log
    log_file = os.path.join(log_dir, "execution.log")
    
    # Create logger with unique name using adw_id
    logger = logging.getLogger(f"adw_{adw_id}")
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # File handler - captures everything
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler - INFO and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Format with timestamp for file
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Simpler format for console (similar to current print statements)
    console_formatter = logging.Formatter('%(message)s')
    
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log initial setup message
    logger.info(f"ADW Logger initialized - ID: {adw_id}")
    logger.debug(f"Log file: {log_file}")
    
    return logger


def get_logger(adw_id: str) -> logging.Logger:
    """Get existing logger by ADW ID.
    
    Args:
        adw_id: The ADW workflow ID
        
    Returns:
        Logger instance
    """
    return logging.getLogger(f"adw_{adw_id}")


def parse_json(text: str, target_type: Type[T] = None) -> Union[T, Any]:
    """Parse JSON that may be wrapped in markdown code blocks.
    
    Handles various formats:
    - Raw JSON
    - JSON wrapped in ```json ... ```
    - JSON wrapped in ``` ... ```
    - JSON with extra whitespace or newlines
    
    Args:
        text: String containing JSON, possibly wrapped in markdown
        target_type: Optional type to validate/parse the result into (e.g., List[TestResult])
        
    Returns:
        Parsed JSON object, optionally validated as target_type
        
    Raises:
        ValueError: If JSON cannot be parsed from the text
    """
    # Try to extract JSON from markdown code blocks
    # Pattern matches ```json\n...\n``` or ```\n...\n```
    code_block_pattern = r'```(?:json)?\s*\n(.*?)\n```'
    match = re.search(code_block_pattern, text, re.DOTALL)
    
    if match:
        json_str = match.group(1).strip()
    else:
        # No code block found, try to parse the entire text
        json_str = text.strip()
    
    # Try to find JSON array or object boundaries if not already clean
    if not (json_str.startswith('[') or json_str.startswith('{')):
        # Look for JSON array
        array_start = json_str.find('[')
        array_end = json_str.rfind(']')
        
        # Look for JSON object
        obj_start = json_str.find('{')
        obj_end = json_str.rfind('}')
        
        # Determine which comes first and extract accordingly
        if array_start != -1 and (obj_start == -1 or array_start < obj_start):
            if array_end != -1:
                json_str = json_str[array_start:array_end + 1]
        elif obj_start != -1:
            if obj_end != -1:
                json_str = json_str[obj_start:obj_end + 1]
    
    try:
        result = json.loads(json_str)
        
        # If target_type is provided and has from_dict/parse_obj/model_validate methods (Pydantic)
        if target_type and hasattr(target_type, '__origin__'):
            # Handle List[SomeType] case
            if target_type.__origin__ == list:
                item_type = target_type.__args__[0]
                # Try Pydantic v2 first, then v1
                if hasattr(item_type, 'model_validate'):
                    result = [item_type.model_validate(item) for item in result]
                elif hasattr(item_type, 'parse_obj'):
                    result = [item_type.parse_obj(item) for item in result]
        elif target_type:
            # Handle single Pydantic model
            if hasattr(target_type, 'model_validate'):
                result = target_type.model_validate(result)
            elif hasattr(target_type, 'parse_obj'):
                result = target_type.parse_obj(result)
            
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}. Text was: {json_str[:200]}...")


def check_env_vars(logger: Optional[logging.Logger] = None) -> None:
    """Check that all required environment variables are set.
    
    Args:
        logger: Optional logger instance for error reporting
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    required_vars = [
        # "ANTHROPIC_API_KEY",
        "CLAUDE_CODE_PATH",
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        error_msg = "Error: Missing required environment variables:"
        if logger:
            logger.error(error_msg)
            for var in missing_vars:
                logger.error(f"  - {var}")
        else:
            print(error_msg, file=sys.stderr)
            for var in missing_vars:
                print(f"  - {var}", file=sys.stderr)
        sys.exit(1)


def _load_model_policy() -> Dict[str, Any]:
    """Load model_policy from config.yml (Tier 2 fallback).

    Returns:
        Dictionary with model_policy fields, or empty dict if not found.
    """
    try:
        config_path = Path(__file__).parent.parent.parent / "config.yml"
        if not config_path.exists():
            config_path = Path.cwd() / "config.yml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return data.get("agentic", {}).get("model_policy", {})
    except Exception:
        pass
    return {}


def _resolve(env_var: str, config_key: str = None, policy: Dict[str, Any] = None) -> Optional[str]:
    """Resolve a value with 2-tier: env var -> config.yml. Skips ${VAR} literals."""
    value = os.getenv(env_var)
    if value:
        return value
    if config_key and policy:
        cfg_value = policy.get(config_key)
        if cfg_value and not (isinstance(cfg_value, str) and cfg_value.startswith("${")):
            return cfg_value
    return None


def get_safe_subprocess_env() -> Dict[str, str]:
    """Get filtered environment variables safe for subprocess execution.

    Resolves values with 2-tier priority: env var -> config.yml.
    This prevents accidental exposure of sensitive credentials to subprocesses
    while ensuring config.yml fallbacks reach Claude Code subprocesses.

    Returns:
        Dictionary containing only required environment variables
    """
    policy = _load_model_policy()

    safe_env_vars = {
        # Anthropic Configuration (required - supports non-Anthropic providers)
        # Credentials: env-only (no config.yml fallback for security)
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "ANTHROPIC_AUTH_TOKEN": os.getenv("ANTHROPIC_AUTH_TOKEN"),

        # Anthropic API Base URL: env -> config.yml
        "ANTHROPIC_BASE_URL": _resolve("ANTHROPIC_BASE_URL", "base_url", policy),

        # Claude Model Overrides: env -> config.yml
        "ANTHROPIC_MODEL": os.getenv("ANTHROPIC_MODEL"),
        "ANTHROPIC_DEFAULT_OPUS_MODEL": _resolve("ANTHROPIC_DEFAULT_OPUS_MODEL", "opus_model", policy),
        "ANTHROPIC_DEFAULT_SONNET_MODEL": _resolve("ANTHROPIC_DEFAULT_SONNET_MODEL", "sonnet_model", policy),
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": _resolve("ANTHROPIC_DEFAULT_HAIKU_MODEL", "haiku_model", policy),
        "CLAUDE_CODE_SUBAGENT_MODEL": _resolve("CLAUDE_CODE_SUBAGENT_MODEL", "subagent_model", policy),

        # GitHub Configuration (optional)
        # GITHUB_PAT is optional - if not set, will use default gh auth
        "GITHUB_PAT": os.getenv("GITHUB_PAT"),

        # Claude Code Configuration
        "CLAUDE_CODE_PATH": os.getenv("CLAUDE_CODE_PATH", "claude"),
        "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR": os.getenv(
            "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR", "true"
        ),

        # Agent Cloud Sandbox Environment (optional)
        "E2B_API_KEY": os.getenv("E2B_API_KEY"),

        # Cloudflare tunnel token (optional)
        "CLOUDFLARED_TUNNEL_TOKEN": os.getenv("CLOUDFLARED_TUNNEL_TOKEN"),

        # Essential system environment variables
        "HOME": os.getenv("HOME"),
        "USER": os.getenv("USER"),
        "PATH": os.getenv("PATH"),
        "SHELL": os.getenv("SHELL"),
        "TERM": os.getenv("TERM"),
        "LANG": os.getenv("LANG"),
        "LC_ALL": os.getenv("LC_ALL"),

        # Python-specific variables that subprocesses might need
        "PYTHONPATH": os.getenv("PYTHONPATH"),
        "PYTHONUNBUFFERED": "1",  # Useful for subprocess output

        # Working directory tracking
        "PWD": os.getcwd(),
    }
    
    # Add GH_TOKEN as alias for GITHUB_PAT if it exists
    github_pat = os.getenv("GITHUB_PAT")
    if github_pat:
        safe_env_vars["GH_TOKEN"] = github_pat
    
    # Filter out None values
    return {k: v for k, v in safe_env_vars.items() if v is not None}