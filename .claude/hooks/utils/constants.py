#!/usr/bin/env python3
"""
Constants for Claude Code Hooks in tac-bootstrap.

This module provides shared constants and utilities for all hooks.
All values are derived from the project configuration.
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT METADATA
# ============================================================================

PROJECT_NAME = "tac-bootstrap"
LANGUAGE = "Language.PYTHON"
PACKAGE_MANAGER = "PackageManager.UV"

# ============================================================================
# DIRECTORY PATHS
# ============================================================================

LOG_DIR = "logs"
SPECS_DIR = "specs"
ADWS_DIR = "adws"
SCRIPTS_DIR = "scripts"
PROMPTS_DIR = "prompts"
WORKTREES_DIR = "trees"

# ============================================================================
# SAFETY CONFIGURATION
# ============================================================================

# Paths that agents are forbidden from modifying
FORBIDDEN_PATHS = [    ".env",    "secrets/",]

# Paths that agents are allowed to modify
ALLOWED_PATHS = [    "tac_bootstrap_cli/",    "adws/",    "scripts/",    "specs/",    "tests/",]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_session_log_dir(session_id: str) -> Path:
    """
    Get the log directory for a specific session.

    Args:
        session_id: The Claude session ID

    Returns:
        Path object for the session's log directory
    """
    return Path(LOG_DIR) / session_id

def ensure_session_log_dir(session_id: str) -> Path:
    """
    Ensure the log directory for a session exists.

    Args:
        session_id: The Claude session ID

    Returns:
        Path object for the session's log directory
    """
    log_dir = get_session_log_dir(session_id)
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
