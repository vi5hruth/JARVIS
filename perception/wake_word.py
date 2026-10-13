"""
wake_word.py

Continuously listens to the microphone for the "hey jarvis" wake phrase
using openWakeWord's pretrained model. Blocks until detected, then returns
-- the caller (orchestrator/CLI) decides what to do next (start STT).
"""

import numpy as np
import sounddevice as sd
from openwakeword.model import Model
from core.config_manager import get_settings
from core.logger import get_logger

log = get_logger("wake_word")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # openWakeWord expects 80ms chunks at 16kHz
THRESHOLD = 0.35


class WakeWordDetector:
    def __init__(self, keyword: str | None = None):
        keyword = keyword or get_settings().wake_word.keyword
        self._model = Model(wakeword_models=[keyword])
        self._keyword = keyword
        log.info(f"Wake word model loaded: {keyword}")

    def listen_for_wake_word(self) -> None:
        """Blocks until the wake word is detected, then returns."""
        log.info("Listening for wake word...")

        with sd.InputStream(
               device=1,
               samplerate=SAMPLE_RATE,
               blocksize=CHUNK_SIZE,
               dtype="int16",
               channels=1,
        ) as stream:
            while True:
                audio_chunk, _ = stream.read(CHUNK_SIZE)
                audio_data = np.squeeze(audio_chunk)

                predictions = self._model.predict(audio_data)
                score = predictions.get(self._keyword, 0.0)

                if score > THRESHOLD:
                    print(f"\nWake word detected! Score: {score:.2f}", flush=True)
                    log.info(f"Wake word detected! (score={score:.2f})")
                    return