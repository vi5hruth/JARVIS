"""Tests proving the Executor handles skill failures safely."""

import pytest

from action.executor import Executor, ToolCall
from skills import registry
from skills.base_skill import BaseSkill, SkillResult


class EchoSkill(BaseSkill):
    name = "echo"

    def execute(self, text: str = "") -> SkillResult:
        return SkillResult(success=True, data=text)


class ExplodingSkill(BaseSkill):
    name = "boom"

    def execute(self) -> SkillResult:
        raise RuntimeError("kaboom")


class KeyErrorSkill(BaseSkill):
    name = "keyerror"

    def execute(self) -> SkillResult:
        return {}["missing"]


@pytest.fixture(autouse=True)
def fake_skills(monkeypatch):
    """Register temporary skills for these tests."""
    for skill in (EchoSkill(), ExplodingSkill(), KeyErrorSkill()):
        monkeypatch.setitem(registry._SKILLS, skill.name, skill)


def test_successful_call_returns_skill_result():
    results = Executor().run([ToolCall("echo", {"text": "hi"})])
    assert results[0].success is True
    assert results[0].data == "hi"


def test_unknown_skill_returns_failure():
    results = Executor().run([ToolCall("does_not_exist")])
    assert results[0].success is False
    assert "does_not_exist" in results[0].error


def test_bad_arguments_return_failure_instead_of_crashing():
    results = Executor().run([ToolCall("echo", {"bogus": 1})])
    assert results[0].success is False
    assert "echo" in results[0].error


def test_skill_exception_returns_failure():
    results = Executor().run([ToolCall("boom")])
    assert results[0].success is False
    assert "kaboom" in results[0].error


def test_keyerror_inside_skill_is_not_reported_as_unknown_skill():
    results = Executor().run([ToolCall("keyerror")])
    assert results[0].success is False
    assert "No skill registered" not in results[0].error
    assert "keyerror" in results[0].error


def test_one_failure_does_not_stop_later_calls():
    results = Executor().run([
        ToolCall("boom"),
        ToolCall("echo", {"text": "still ran"}),
    ])
    assert len(results) == 2
    assert results[0].success is False
    assert results[1].success is True
    assert results[1].data == "still ran"