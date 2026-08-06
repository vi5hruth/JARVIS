"""
Unit tests for core plumbing: exceptions, config_manager, context, event_bus.
"""

from core.config_manager import get_settings
from core.context import Context
from core.event_bus import EventBus
from core.exceptions import JarvisError, SkillExecutionError


def test_settings_load_correctly():
    settings = get_settings()
    assert settings.stt.model_path == "models/vosk-model-small-en-us"
    assert settings.llm.backend == "ollama"


def test_context_has_request_id():
    ctx = Context(raw_text="hello jarvis")
    assert ctx.raw_text == "hello jarvis"
    assert len(ctx.request_id) == 8


def test_skill_execution_error_includes_skill_name():
    err = SkillExecutionError("notes", "something broke")
    assert "notes" in str(err)
    assert isinstance(err, JarvisError)


def test_event_bus_delivers_to_subscriber():
    bus = EventBus()
    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("test_event", handler)
    bus.publish("test_event", {"value": 42})

    assert received == [{"value": 42}]