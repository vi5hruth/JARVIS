"""
executor.py

Executes tool calls through the skill registry.
Errors are returned as failed SkillResult objects instead of
crashing the assistant.
"""

from dataclasses import dataclass, field

from core.logger import get_logger
from skills import registry
from skills.base_skill import SkillResult

log = get_logger("executor")


@dataclass
class ToolCall:
    skill_name: str
    arguments: dict = field(default_factory=dict)


class Executor:
    def run(self, tool_calls: list[ToolCall]) -> list[SkillResult]:
        return [self._run_one(call) for call in tool_calls]

    def _run_one(self, call: ToolCall) -> SkillResult:
        log.debug(
            f"Executing skill '{call.skill_name}' with {call.arguments}"
        )

        # Look up the skill separately so an internal KeyError
        # is not mistaken for an unknown skill.
        try:
            skill = registry.get(call.skill_name)
        except KeyError:
            log.warning(
                f"Unknown skill requested: '{call.skill_name}'"
            )
            return SkillResult(
                success=False,
                error=f"No skill registered with name '{call.skill_name}'",
            )

        try:
            return skill.execute(**call.arguments)
        except Exception as e:
            log.exception(
                f"Skill '{call.skill_name}' raised an error"
            )
            return SkillResult(
                success=False,
                error=f"The '{call.skill_name}' skill failed: {e}",
            )