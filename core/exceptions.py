"""
exceptions.py

Central exception hierarchy for Jarvis. Every module raises these instead of
bare Exception, so the orchestrator can catch and handle errors consistently
(e.g. decide whether to retry, fall back, or just speak an error message).
"""


class JarvisError(Exception):
    """Base class for all Jarvis-specific errors."""
    pass


class ConfigError(JarvisError):
    """Raised when configuration is missing, invalid, or fails validation."""
    pass


class STTError(JarvisError):
    """Raised when speech-to-text transcription fails."""
    pass


class TTSError(JarvisError):
    """Raised when text-to-speech synthesis fails."""
    pass


class PlanningError(JarvisError):
    """Raised when the LLM planner fails to produce a valid plan."""
    pass


class SkillExecutionError(JarvisError):
    """Raised when a skill fails during execution."""

    def __init__(self, skill_name: str, message: str):
        self.skill_name = skill_name
        super().__init__(f"[{skill_name}] {message}")