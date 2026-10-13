"""Unit tests for the time skill (skills/clock/skill.py)."""

from datetime import datetime

import pytest

from skills import registry
from skills.clock import skill as clock_skill


@pytest.mark.parametrize(
    "hour, minute, expected",
    [
        (15, 5, "It's 3:05 PM."),
        (9, 30, "It's 9:30 AM."),
        (0, 7, "It's 12:07 AM."),
        (12, 0, "It's 12:00 PM."),
    ],
)
def test_time_is_spoken_in_12_hour_format(monkeypatch, hour, minute, expected):
    monkeypatch.setattr(clock_skill, "_now", lambda: datetime(2026, 10, 13, hour, minute))
    result = clock_skill.TimeSkill().execute()
    assert result.success is True
    assert result.data == expected


def test_uses_the_real_clock_by_default():
    result = clock_skill.TimeSkill().execute()
    assert result.success is True
    assert result.data.startswith("It's ")
    assert result.data.endswith(".")


def test_time_skill_is_registered_under_the_name_time():
    assert isinstance(registry.get("time"), clock_skill.TimeSkill)
