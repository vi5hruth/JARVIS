"""
coding_assistant/skill.py

RESPONSIBILITY:
    - Handles coding-related requests: explain code, generate a snippet, run
      a script, or read a repo (optionally via GitPython). Delegates actual
      reasoning to integrations/llm.

TODO (future days):
    - class CodingAssistantSkill(BaseSkill): name="coding_assistant", execute(action, prompt, ...)
"""
