
import pytest

from interfaces import cli


class FakeTTS:
    def __init__(self):
        self.spoken = []

    def speak(self, text):
        self.spoken.append(text)

    def wait_until_done(self):
        pass


class ScriptedWakeWord:
    def __init__(self, activations):
        self.activations = activations

    def listen_for_wake_word(self):
        if self.activations <= 0:
            raise KeyboardInterrupt()

        self.activations -= 1


class ScriptedSTT:
    def __init__(self, *items):
        self.items = list(items)

    def listen_and_transcribe(self):
        if not self.items:
            raise IndexError("No more scripted input")

        item = self.items.pop(0)

        if isinstance(item, BaseException):
            raise item

        return item


class FakeOrchestrator:
    def __init__(self, error=None):
        self.error = error

    def handle_text(self, text):
        if self.error:
            raise self.error

        return f"reply to {text}"


@pytest.fixture
def hardware_stubbed(monkeypatch):
    monkeypatch.setattr(cli, "setup_logging", lambda: None)
    monkeypatch.setattr(cli, "discover", lambda: None)


def run_main(
    cli_module,
    monkeypatch,
    wake_word,
    stt,
    orchestrator,
    tts,
):
    monkeypatch.setattr(
        cli_module,
        "WakeWordDetector",
        lambda: wake_word,
    )
    monkeypatch.setattr(
        cli_module,
        "VoskEngine",
        lambda: stt,
    )
    monkeypatch.setattr(
        cli_module,
        "Pyttsx3Engine",
        lambda: tts,
    )
    monkeypatch.setattr(
        cli_module,
        "Orchestrator",
        lambda: orchestrator,
    )

    cli_module.main()


def test_normal_turn_speaks_the_response(
    hardware_stubbed,
    monkeypatch,
):
    tts = FakeTTS()

    run_main(
        cli,
        monkeypatch,
        ScriptedWakeWord(1),
        ScriptedSTT("list notes"),
        FakeOrchestrator(),
        tts,
    )

    assert tts.spoken == [
        "I'm listening. Go ahead!",
        "reply to list notes",
    ]


def test_error_in_a_turn_does_not_kill_the_loop(
    hardware_stubbed,
    monkeypatch,
):
    tts = FakeTTS()

    stt = ScriptedSTT(
        RuntimeError("mic exploded"),
        "hello",
    )

    run_main(
        cli,
        monkeypatch,
        ScriptedWakeWord(1),
        stt,
        FakeOrchestrator(),
        tts,
    )

    assert tts.spoken == [
        "I'm listening. Go ahead!",
        "reply to hello",
    ]


def test_ctrl_c_while_processing_exits_cleanly(
    hardware_stubbed,
    monkeypatch,
):
    tts = FakeTTS()

    run_main(
        cli,
        monkeypatch,
        ScriptedWakeWord(1),
        ScriptedSTT("hello"),
        FakeOrchestrator(error=KeyboardInterrupt()),
        tts,
    )

    assert tts.spoken == [
        "I'm listening. Go ahead!",
    ]
