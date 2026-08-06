"""
logger.py

RESPONSIBILITY:
    - Configures loguru sinks based on config/logging.yaml (console + rotating
      file). Provides a `get_logger(name)` helper so every module logs with
      consistent formatting and a correlation ID per request.

TODO (future days):
    - setup_logging() -> called once at app startup
    - get_logger(module_name: str)
"""
