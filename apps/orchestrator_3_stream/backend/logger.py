"""Orchestrator structured logger.

Provides centralized logging for the orchestrator backend.
Uses Python stdlib logging with optional file output.
"""

import logging
import os
from pathlib import Path
from datetime import datetime

from config import LOG_LEVEL, LOG_DIR


def setup_logger(name: str = "orchestrator") -> logging.Logger:
    """Create and configure the orchestrator logger."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

    if not logger.handlers:
        # Console handler
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        ))
        logger.addHandler(console)

        # File handler (optional - only if LOG_DIR exists or can be created)
        try:
            log_dir = Path(LOG_DIR)
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"orchestrator_{datetime.now():%Y%m%d}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            ))
            logger.addHandler(file_handler)
        except OSError:
            pass  # Skip file logging if directory can't be created

    return logger


# Module-level logger instance
logger = setup_logger()
