"""
executor.py

Takes a plan (a list of tool calls) and executes each one via the skill
registry, collecting results. This is the ONLY module that actually calls
skill.execute() -- it looks skills up by name, never imports one directly.
"""

from dataclasses import dataclass, field
from typing import Any

from core.logger import get_logger
from skills import registry

log = get_logger("executor")


@dataclass
class ToolCall:
    skill_name: str
    arguments: dict = field(default_factory=dict)


class Executor:
    def run(self, tool_calls: list[ToolCall]) -> list[Any]:
        results = []
        for call in tool_calls:
            log.debug(f"Executing skill '{call.skill_name}' with {call.arguments}")
            try:
                skill = registry.get(call.skill_name)
                result = skill.execute(**call.arguments)
            except KeyError as e:
                from skills.base_skill import SkillResult
                result = SkillResult(success=False, error=str(e))
            results.append(result)
        return results