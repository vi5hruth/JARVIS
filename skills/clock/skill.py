"""
clock/skill.py

Tells the current local time ("what time is it?"). Implements BaseSkill and
registers itself -- the executor needed no changes to pick it up.
"""

from datetime import datetime

from skills.base_skill import BaseSkill, SkillResult
from skills.registry import register_skill


def _now() -> datetime:
    """Current local system time. A separate function so tests can fake the clock."""
    return datetime.now()


@register_skill
class TimeSkill(BaseSkill):
    name = "time"
    description = "Tell the current local time."
    parameters_schema = {}

    def execute(self) -> SkillResult:
        spoken = _now().strftime("%I:%M %p").lstrip("0")  # e.g. "3:05 PM"
        return SkillResult(success=True, data=f"It's {spoken}.")
