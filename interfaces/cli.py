
"""
Jarvis hands-free assistant:
wake word -> activation prompt -> multiple commands -> standby after silence.
Supports voice commands to exit cleanly.
"""

import re
import time

from action.tts.pyttsx3_engine import Pyttsx3Engine
from core.logger import setup_logging, get_logger
from core.orchestrator import Orchestrator
from perception.stt.vosk_engine import VoskEngine
from perception.wake_word import WakeWordDetector
from skills.registry import discover

log = get_logger("cli")

COMMAND_DURATION = 4.0
MAX_SILENT_WINDOWS = 3

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


def main():
    setup_logging()
    discover()

    orchestrator = Orchestrator()
    tts = Pyttsx3Engine()
    stt = VoskEngine()
    wake_word = WakeWordDetector()

    print("Jarvis is running. Say 'Hey Jarvis' to activate.")
    print("Say 'Goodbye Jarvis' to exit, or press Ctrl+C.\n")

    should_exit = False

    while not should_exit:
        try:
            # Standby: wait for the wake word.
            wake_word.listen_for_wake_word()

            print("\nJarvis: I'm listening. Go ahead!")
            tts.speak("I'm listening. Go ahead!")
            tts.wait_until_done()

            silent_windows = 0

            # Accept multiple commands after one activation.
            while silent_windows < MAX_SILENT_WINDOWS:
                print("Listening for your command...")

                try:
                    text = stt.listen_and_transcribe()

                except KeyboardInterrupt:
                    raise

                except IndexError:
                    # Allows scripted tests to finish when inputs run out.
                    log.debug("No more scripted input; ending this session.")
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

                # Speech was detected; reset the silence counter.
                silent_windows = 0

                print(f"You said: {text}")

                # Handle exit commands before normal command routing.
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

                    if response:
                        tts.speak(response)
                        tts.wait_until_done()

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
