"""
registry.py

RESPONSIBILITY:
    - Plugin/Registry pattern: discovers and holds every registered
      BaseSkill subclass. Skills register themselves via a decorator
      (e.g. @register_skill) at import time -- core code just calls
      registry.get(skill_name) or registry.all() and never hardcodes
      a list of skills.
    - The Planner uses registry.all() to build its LLM prompt (so the LLM
      always knows about every currently available skill, including ones
      added after this architecture doc was written).

TODO (future days):
    - _SKILLS: dict[str, type[BaseSkill]] = {}
    - def register_skill(cls): decorator, adds cls to _SKILLS
    - def get(name: str) -> BaseSkill
    - def all() -> list[BaseSkill]
    - def discover(package="skills"): auto-import all skill modules at startup
"""
