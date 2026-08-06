"""
base_skill.py

RESPONSIBILITY:
    - Abstract base class every skill must implement (Command pattern).
    - Defines the contract: a skill declares its name, a description (used by
      the Planner's LLM prompt to know when to invoke it), a JSON schema for
      its arguments, and an execute() method.
    - THIS is the file that makes "add skills without touching core" possible:
      as long as a new skill subclasses BaseSkill and registers itself
      (see registry.py), the orchestrator/executor/planner need zero changes.

TODO (future days):
    - class BaseSkill(ABC):
        name: str
        description: str
        parameters_schema: dict
        abstractmethod execute(self, **kwargs) -> SkillResult
    - @dataclass SkillResult: success: bool, data: Any, error: str | None
"""
