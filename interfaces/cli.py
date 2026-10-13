
"""
cli.py

Entry point for running Jarvis hands-free:
wake word -> speech -> orchestrator -> spoken response.
"""

import time

from action.tts.pyttsx3_engine import Pyttsx3Engine
from core.logger import setup_logging, get_logger
from core.orchestrator import Orchestrator
from perception.stt.vosk_engine import VoskEngine
from perception.wake_word import WakeWordDetector
from skills.registry import discover

log = get_logger("cli")


def main():
    setup_logging()
    discover()
    orchestrator = Orchestrator()
    tts = Pyttsx3Engine()
    stt = VoskEngine()
    wake_word = WakeWordDetector()

    print("Jarvis is running. Say 'hey jarvis' to activate. Ctrl+C to exit.\n")

    while True:
        try:
            wake_word.listen_for_wake_word()

            print("Listening...")
            text = stt.listen_and_transcribe()

            if not text:
                print("Jarvis: I didn't catch that.\n")
                continue

            print(f"You said: {text}")
            response = orchestrator.handle_text(text)
            print(f"Jarvis: {response}\n")
            tts.speak(response)
            tts.wait_until_done()

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

        except Exception:
            log.exception("Error while handling a voice turn")
            print("Jarvis: Something went wrong. Check the log for details.\n")
            time.sleep(1)


if __name__ == "__main__":
    main()
