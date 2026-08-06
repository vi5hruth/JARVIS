"""
exceptions.py

RESPONSIBILITY:
    - Central exception hierarchy so every module raises/catches consistent,
      typed errors instead of bare Exception. Lets the orchestrator apply
      uniform retry/fallback policy.

TODO (future days):
    - class JarvisError(Exception): base class
    - class SkillExecutionError(JarvisError)
    - class STTError(JarvisError)
    - class TTSError(JarvisError)
    - class PlanningError(JarvisError)
    - class ConfigError(JarvisError)
"""
