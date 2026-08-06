"""
logger.py

Configures loguru for consistent logging across all modules: console output
+ rotating file output, based on settings from config.yaml.
"""

import sys
from pathlib import Path

from loguru import logger

from core.config_manager import get_settings

_configured = False


def setup_logging() -> None:
    """Call once at app startup, before any other module logs anything."""
    global _configured
    if _configured:
        return

    settings = get_settings()
    log_path = Path(settings.logging.log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.remove()  # remove loguru's default handler
    logger.add(sys.stderr, level=settings.logging.level)
    logger.add(
        log_path,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
    )

    _configured = True


def get_logger(module_name: str):
    """Get a logger bound with the calling module's name, for clearer log lines."""
    return logger.bind(module=module_name)