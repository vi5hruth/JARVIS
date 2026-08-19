"""
base_skill.py

Abstract base class every skill must implement (Command pattern). A skill
declares its name, a description (used by the LLM planner to know when to
invoke it), a schema for its arguments, and an execute() method.

As long as a new skill subclasses BaseSkill and registers itself, the
orchestrator/executor/planner need zero code changes to use it.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class SkillResult:
    success: bool
    data: Any = None
    error: str | None = None


class BaseSkill(ABC):
    name: str = ""
    description: str = ""
    parameters_schema: dict = {}

    @abstractmethod
    def execute(self, **kwargs) -> SkillResult:
        """Run the skill with the given arguments, return a SkillResult."""
        raise NotImplementedError