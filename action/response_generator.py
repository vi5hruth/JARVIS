"""
response_generator.py

RESPONSIBILITY:
    - Converts raw skill execution results into a natural-language response
      string (optionally via a lightweight LLM call for phrasing, or simple
      templates for deterministic skills like "what time is it").

TODO (future days):
    - class ResponseGenerator: generate(results: list[SkillResult]) -> str
"""
