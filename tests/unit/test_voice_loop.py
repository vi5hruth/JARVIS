
"""Tests for the voice loop and wake-word configuration."""

import sys
import types

import pytest

HARDWARE_MODULES = [
    "pyttsx3",
    "sounddevice",
    "vosk",
    "openwakeword",
    "openwakeword.model",
]

OUR_HARDWARE_MODULES = [
    "interfaces.cli",
    "perception.wake_word",
    "perception.stt.vosk_engine",
    "action.tts.pyttsx3_engine",
]


class FakeModel:
    """Fake model that records the requested wake-word."""

    last_models = None

    def __init__(self, wakeword_models):
        FakeModel.last_models = wakeword_models


@pytest.fixture
def hardware_stubbed(monkeypatch):
    for name in OUR_HARDWARE_MODULES:
        sys.modules.pop(name, None)

    for name in HARDWARE_MODULES:
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))

    sys.modules["openwakeword.model"].Model = FakeModel

    yield

    for name in OUR_HARDWARE_MODULES:
        sys.modules.pop(name, None)


class ScriptedWakeWord:
    """Fires a fixed number of times, then simulates Ctrl+C."""

    def __init__(self, turns):
        self.turns = turns

    def listen_for_wake_word(self):
        if self.turns == 0:
            raise KeyboardInterrupt
        self.turns -= 1


class ScriptedSTT:
    """Returns or raises the next scripted item."""

    def __init__(self, *items):
        self.items = list(items)

    def listen_and_transcribe(self):
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class FakeOrchestrator:
    def __init__(self, error=None):
        self.error = error

    def handle_text(self, text):
        if self.error:
            raise self.error
        return f"reply to {text}"


class FakeTTS:
    def __init__(self):
        self.spoken = []

    def speak(self, text):
        self.spoken.append(text)

    def wait_until_done(self):
        pass


def run_main(cli, monkeypatch, wake_word, stt, orchestrator, tts):
    monkeypatch.setattr(cli, "setup_logging", lambda: None)
    monkeypatch.setattr(cli, "discover", lambda: None)
    monkeypatch.setattr(cli.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(cli, "WakeWordDetector", lambda: wake_word)
    monkeypatch.setattr(cli, "VoskEngine", lambda: stt)
    monkeypatch.setattr(cli, "Orchestrator", lambda: orchestrator)
    monkeypatch.setattr(cli, "Pyttsx3Engine", lambda: tts)

    try:
        cli.main()
    except KeyboardInterrupt:
        pytest.fail("KeyboardInterrupt escaped main() instead of exiting cleanly")


def test_normal_turn_speaks_the_response(hardware_stubbed, monkeypatch):
    from interfaces import cli

    tts = FakeTTS()
    run_main(
        cli, monkeypatch, ScriptedWakeWord(1),
        ScriptedSTT("list notes"), FakeOrchestrator(), tts
    )
    assert tts.spoken == ["reply to list notes"]


def test_error_in_a_turn_does_not_kill_the_loop(hardware_stubbed, monkeypatch):
    from interfaces import cli

    tts = FakeTTS()
    stt = ScriptedSTT(RuntimeError("mic exploded"), "hello")
    run_main(
        cli, monkeypatch, ScriptedWakeWord(2),
        stt, FakeOrchestrator(), tts
    )
    assert tts.spoken == ["reply to hello"]


def test_ctrl_c_while_processing_exits_cleanly(hardware_stubbed, monkeypatch):
    from interfaces import cli

    tts = FakeTTS()
    run_main(
        cli, monkeypatch, ScriptedWakeWord(5),
        ScriptedSTT("hello"),
        FakeOrchestrator(error=KeyboardInterrupt()),
        tts,
    )
    assert tts.spoken == []


def test_wake_word_keyword_comes_from_config(hardware_stubbed, monkeypatch):
    from core.config_manager import get_settings
    from perception.wake_word import WakeWordDetector

    monkeypatch.setattr(get_settings().wake_word, "keyword", "custom_word")
    detector = WakeWordDetector()

    assert detector._keyword == "custom_word"
    assert FakeModel.last_models == ["custom_word"]


def test_explicit_keyword_overrides_config(hardware_stubbed):
    from perception.wake_word import WakeWordDetector

    WakeWordDetector(keyword="other_word")
    assert FakeModel.last_models == ["other_word"]
