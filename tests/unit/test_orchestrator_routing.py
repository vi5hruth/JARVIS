"""
Unit tests for command routing in core/orchestrator.py: spoken phrases must
reach the right skill, existing commands must keep working, and anything
unsupported must get a sensible reply.
"""

from datetime import datetime

import pytest

from action.executor import ToolCall
from core.orchestrator import Orchestrator
from skills.clock import skill as clock_skill  # importing these registers the skills
from skills.open_website import skill as web_skill

TIME_CALL = [ToolCall(skill_name="time")]
YOUTUBE_CALL = [ToolCall(skill_name="open_website", arguments={"site": "youtube"})]
NOT_UNDERSTOOD = "Sorry, I don't understand that yet."


@pytest.mark.parametrize(
    "spoken",
    [
        "what time is it",
        "What time is it?",
        "What's the time?",
        "what\u2019s the time",
        "Tell me the time.",
        "what is the time please",
        "WHAT IS THE CURRENT TIME",
    ],
)
def test_time_phrases_route_to_the_time_skill(spoken):
    assert Orchestrator()._route(spoken) == TIME_CALL


@pytest.mark.parametrize(
    "spoken",
    ["open youtube", "Open YouTube.", "open you tube", "OPEN YOUTUBE please", "launch youtube", "go to youtube"],
)
def test_youtube_phrases_route_to_open_website(spoken):
    assert Orchestrator()._route(spoken) == YOUTUBE_CALL


def test_existing_note_commands_still_route_to_notes():
    orchestrator = Orchestrator()
    assert orchestrator._route("note buy milk") == [
        ToolCall(skill_name="notes", arguments={"action": "create", "text": "buy milk"})
    ]
    assert orchestrator._route("list notes") == [ToolCall(skill_name="notes", arguments={"action": "list"})]
    assert orchestrator._route("show notes") == [ToolCall(skill_name="notes", arguments={"action": "list"})]


def test_a_note_about_time_or_youtube_is_still_a_note():
    orchestrator = Orchestrator()
    assert orchestrator._route("note what time is it")[0].skill_name == "notes"
    assert orchestrator._route("note open youtube")[0].skill_name == "notes"


@pytest.mark.parametrize(
    "spoken",
    ["open your job", "what is the weather", "open facebook", "time travel", "what time", ""],
)
def test_unsupported_commands_get_a_sensible_reply(spoken):
    orchestrator = Orchestrator()
    assert orchestrator._route(spoken) == []
    assert orchestrator.handle_text(spoken) == NOT_UNDERSTOOD


def test_time_command_end_to_end(monkeypatch):
    monkeypatch.setattr(clock_skill, "_now", lambda: datetime(2026, 10, 13, 15, 5))
    assert Orchestrator().handle_text("What's the time?") == "It's 3:05 PM."


def test_youtube_command_end_to_end(monkeypatch):
    opened = []
    monkeypatch.setattr(web_skill.webbrowser, "open", lambda url, new=0: opened.append(url) or True)
    assert Orchestrator().handle_text("Open YouTube.") == "Opening YouTube."
    assert opened == ["https://www.youtube.com"]


def test_youtube_failure_is_reported_not_hidden(monkeypatch):
    monkeypatch.setattr(web_skill.webbrowser, "open", lambda url, new=0: False)
    response = Orchestrator().handle_text("open youtube")
    assert response.startswith("Something went wrong")
    assert "couldn't open YouTube" in response
    assert "Opening YouTube" not in response
