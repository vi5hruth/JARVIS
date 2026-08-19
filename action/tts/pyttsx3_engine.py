"""
pyttsx3_engine.py

TTSEngine implementation using pyttsx3. Uses a dedicated worker thread with
a queue, and creates a fresh pyttsx3 engine instance per spoken utterance --
this is the fix for the COM threading issues pyttsx3 has on Windows (engine
instances aren't safe to reuse across threads/calls).
"""

import queue
import threading

import pyttsx3

from action.tts.base import TTSEngine
from core.config_manager import get_settings
from core.logger import get_logger

log = get_logger("tts")


class Pyttsx3Engine(TTSEngine):
    def __init__(self):
        settings = get_settings()
        self._rate = settings.tts.rate
        self._queue: queue.Queue[str] = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def _worker(self):
        while True:
            text = self._queue.get()
            if text is None:
                break
            try:
                engine = pyttsx3.init()
                engine.setProperty("rate", self._rate)
                engine.say(text)
                engine.runAndWait()
                del engine
            except Exception as e:
                log.error(f"TTS failed: {e}")
            finally:
                self._queue.task_done()

    def speak(self, text: str) -> None:
        log.debug(f"Queueing speech: {text}")
        self._queue.put(text)

    def wait_until_done(self) -> None:
        """Block until all queued speech has finished playing."""
        self._queue.join()