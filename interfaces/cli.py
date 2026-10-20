
"""
Jarvis hands-free assistant:
wake word -> activation prompt -> multiple commands -> standby after silence.
Supports voice interruption while Jarvis is speaking.
"""

import re
import time
import threading

import numpy as np
import sounddevice as sd

from action.tts.pyttsx3_engine import Pyttsx3Engine
from core.logger import setup_logging, get_logger
from core.orchestrator import Orchestrator
from perception.stt.vosk_engine import VoskEngine
from perception.wake_word import WakeWordDetector
from skills.registry import discover

log = get_logger("cli")

COMMAND_DURATION = 4.0
MAX_SILENT_WINDOWS = 3

MICROPHONE_DEVICE = 1
SAMPLE_RATE = 16000
BLOCK_SIZE = 1600
VOLUME_THRESHOLD = 1400
LOUD_BLOCKS_REQUIRED = 3

EXIT_COMMANDS = {
    "goodbye",
    "goodbye jarvis",
    "bye jarvis",
    "stop listening",
    "jarvis stop listening",
    "go to sleep",
    "jarvis go to sleep",
    "exit jarvis",
    "quit jarvis",
}


def normalize_command(text: str) -> str:
    """Normalize speech before checking for exit commands."""
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def stop_tts(tts):
    """Stop speech when supported by the TTS engine."""
    stop = getattr(tts, "stop", None)
    if callable(stop):
        try:
            stop()
        except Exception:
            log.exception("Could not stop TTS playback")


def speak_with_interrupt(tts, stt, text):
    """
    Speak while monitoring the microphone.

    Returns transcribed interruption text, or None if uninterrupted.
    The interruption audio is not buffered, so the user may need
    to repeat the command after Jarvis stops speaking.
    """
    if not text:
        return None

    # Unit-test fakes and alternative TTS engines may not support
    # live interruption. Speak normally without opening the microphone.
    if not all(
        hasattr(tts, attr)
        for attr in ("is_speaking", "_queue", "stop")
    ):
        tts.speak(text)
        tts.wait_until_done()
        return None

    tts.speak(text)

    loud_blocks = 0
    interrupted = threading.Event()
    finished = threading.Event()

    def monitor_microphone():
        nonlocal loud_blocks

        try:
            with sd.RawInputStream(
                device=MICROPHONE_DEVICE,
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                dtype="int16",
                channels=1,
            ) as stream:
                while not finished.is_set():
                    audio, _ = stream.read(BLOCK_SIZE)

                    if finished.is_set():
                        break

                    samples = np.frombuffer(audio, dtype=np.int16)
                    if samples.size == 0:
                        continue

                    volume = float(
                        np.sqrt(
                            np.mean(samples.astype(np.float32) ** 2)
                        )
                    )

                    if volume >= VOLUME_THRESHOLD:
                        loud_blocks += 1
                    else:
                        loud_blocks = 0

                    if loud_blocks >= LOUD_BLOCKS_REQUIRED:
                        interrupted.set()
                        stop_tts(tts)
                        return

        except Exception:
            log.exception("Microphone interruption monitor failed")

    monitor = threading.Thread(
        target=monitor_microphone,
        daemon=True,
        name="Jarvis-Interrupt-Monitor",
    )
    monitor.start()

    try:
        while tts.is_speaking() or not tts._queue.empty():
            if interrupted.wait(timeout=0.03):
                break

        if interrupted.is_set():
            print(
                "\nJarvis: I heard you. "
                "Listening for your command..."
            )
        else:
            tts.wait_until_done()

    except KeyboardInterrupt:
        stop_tts(tts)
        raise

    finally:
        finished.set()
        monitor.join(timeout=1.0)

    if not interrupted.is_set():
        return None

    try:
        # The monitor releases the microphone before Vosk opens it.
        return stt.listen_and_transcribe()

    except KeyboardInterrupt:
        raise

    except Exception:
        log.exception("Could not transcribe interruption")
        print("Jarvis: I couldn't catch that. Please try again.")
        return None


def main():
    setup_logging()
    discover()

    orchestrator = Orchestrator()
    tts = Pyttsx3Engine()
    stt = VoskEngine()
    wake_word = WakeWordDetector()

    print("Jarvis is running. Say 'Hey Jarvis' to activate.")
    print("Speak while Jarvis responds to interrupt it.")
    print("Say 'Goodbye Jarvis' to exit, or press Ctrl+C.\n")

    should_exit = False

    while not should_exit:
        try:
            wake_word.listen_for_wake_word()

            print("\nJarvis: I'm listening. Go ahead!")
            tts.speak("I'm listening. Go ahead!")
            tts.wait_until_done()

            silent_windows = 0

            while silent_windows < MAX_SILENT_WINDOWS:
                print("Listening for your command...")

                try:
                    text = stt.listen_and_transcribe()

                except KeyboardInterrupt:
                    raise

                except IndexError:
                    log.debug(
                        "No more scripted input; ending this session."
                    )
                    break

                except Exception:
                    log.exception("Error while listening for a command")
                    print(
                        "Jarvis: Microphone error. Please try again.\n"
                    )
                    continue

                if not text or not text.strip():
                    silent_windows += 1
                    remaining = (
                        MAX_SILENT_WINDOWS - silent_windows
                    ) * COMMAND_DURATION

                    if remaining > 0:
                        print(
                            "No speech detected. Standby in about "
                            f"{remaining:g} seconds if silence continues."
                        )
                    continue

                silent_windows = 0
                print(f"You said: {text}")

                command = normalize_command(text)

                if command in EXIT_COMMANDS:
                    print("Jarvis: Goodbye, boss!")
                    tts.speak("Goodbye, boss!")
                    tts.wait_until_done()
                    should_exit = True
                    break

                try:
                    response = orchestrator.handle_text(text)
                    print(f"Jarvis: {response}\n")

                    while response:
                        interrupted_text = speak_with_interrupt(
                            tts, stt, response
                        )

                        if (
                            not interrupted_text
                            or not interrupted_text.strip()
                        ):
                            break

                        print(f"You said: {interrupted_text}")
                        command = normalize_command(interrupted_text)

                        if command in EXIT_COMMANDS:
                            stop_tts(tts)
                            print("Jarvis: Goodbye, boss!")
                            tts.speak("Goodbye, boss!")
                            tts.wait_until_done()
                            should_exit = True
                            break

                        response = orchestrator.handle_text(
                            interrupted_text
                        )
                        print(f"Jarvis: {response}\n")

                    if should_exit:
                        break

                except KeyboardInterrupt:
                    raise

                except Exception:
                    log.exception("Error while processing the command")
                    print(
                        "Jarvis: Something went wrong while "
                        "processing that command.\n"
                    )

            if should_exit:
                break

            print(
                "\nJarvis is returning to standby. "
                "Say 'Hey Jarvis' to activate again.\n"
            )

        except KeyboardInterrupt:
            stop_tts(tts)
            print("\nGoodbye.")
            break

        except Exception:
            log.exception("Error while handling a voice turn")
            print(
                "Jarvis: Something went wrong. "
                "Check the log for details.\n"
            )
            time.sleep(1)

    print("Jarvis has shut down.")


if __name__ == "__main__":
    main()
