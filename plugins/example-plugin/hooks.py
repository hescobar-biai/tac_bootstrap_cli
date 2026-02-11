"""
Example plugin hooks for TAC Bootstrap.

This module demonstrates how to implement plugin hooks for the TAC Bootstrap
plugin system. Each function name must match a valid HookType value.

Available hooks:
  - post_project_create: Called after a new project is created
  - pre_scaffold: Called before scaffolding begins
  - post_scaffold: Called after scaffolding completes
  - on_command: Called when a CLI command is executed
  - on_error: Called when an error occurs during scaffolding
"""

from pathlib import Path
from typing import Any, Dict, Optional


def post_project_create(
    project_path: Optional[Path] = None,
    project_name: Optional[str] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Called after a new project is created.

    Args:
        project_path: Path where the project was created
        project_name: Name of the project

    Returns:
        Dictionary with hook execution data
    """
    return {
        "message": f"Example plugin: project '{project_name}' created at {project_path}",
        "action": "post_project_create",
    }


def pre_scaffold(
    config: Any = None,
    target_dir: Optional[Path] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Called before scaffolding begins.

    Args:
        config: TACConfig instance
        target_dir: Target directory for scaffolding

    Returns:
        Dictionary with hook execution data
    """
    return {
        "message": "Example plugin: pre-scaffold hook executed",
        "action": "pre_scaffold",
    }


def post_scaffold(
    config: Any = None,
    target_dir: Optional[Path] = None,
    files_created: int = 0,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Called after scaffolding completes.

    Args:
        config: TACConfig instance
        target_dir: Target directory for scaffolding
        files_created: Number of files created

    Returns:
        Dictionary with hook execution data
    """
    return {
        "message": f"Example plugin: scaffold complete, {files_created} files created",
        "action": "post_scaffold",
        "files_created": files_created,
    }
