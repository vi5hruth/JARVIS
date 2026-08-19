"""
registry.py

Plugin/Registry pattern: discovers and holds every registered BaseSkill
subclass. Skills register themselves via @register_skill at import time --
core code never hardcodes a list of skills, it just asks this registry.
"""

import importlib
import pkgutil

from core.logger import get_logger
from skills.base_skill import BaseSkill

log = get_logger("registry")

_SKILLS: dict[str, BaseSkill] = {}


def register_skill(cls):
    """Class decorator: instantiates the skill and adds it to the registry."""
    instance = cls()
    if not instance.name:
        raise ValueError(f"{cls.__name__} must set a non-empty 'name'")
    _SKILLS[instance.name] = instance
    log.debug(f"Registered skill: {instance.name}")
    return cls


def get(name: str) -> BaseSkill:
    """Look up a single skill by name."""
    if name not in _SKILLS:
        raise KeyError(f"No skill registered with name '{name}'")
    return _SKILLS[name]


def all() -> list[BaseSkill]:
    """Return every registered skill (used by the planner to build its prompt)."""
    return list(_SKILLS.values())


def discover() -> None:
    """
    Auto-import every module under skills/ so their @register_skill
    decorators run. Call this once at app startup, before anything tries
    to look up a skill.
    """
    import skills

    for _, module_name, is_pkg in pkgutil.walk_packages(skills.__path__, prefix="skills."):
        if module_name.endswith(".skill"):
            importlib.import_module(module_name)
    log.debug(f"Discovered {len(_SKILLS)} skill(s): {list(_SKILLS.keys())}")