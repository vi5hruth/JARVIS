
"""
Wake-word detection for Jarvis.
Requires consecutive high-confidence scores to reduce false triggers.
"""

import numpy as np
import sounddevice as sd
from openwakeword.model import Model

from core.config_manager import get_settings
from core.logger import get_logger

log = get_logger("wake_word")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280  # 80 ms of audio at 16 kHz
MICROPHONE_DEVICE = 1


class WakeWordDetector:
    def __init__(
        self,
        keyword: str | None = None,
        threshold: float | None = None,
        consecutive_frames: int | None = None,
    ):
        config = get_settings().wake_word

        self._keyword = keyword or config.keyword
        self._threshold = (
            config.threshold if threshold is None else threshold
        )
        self._consecutive_frames = (
            config.consecutive_frames
            if consecutive_frames is None
            else consecutive_frames
        )

        self._model = Model(
            wakeword_models=[self._keyword],
            inference_framework="onnx",
        )

        self._hits = 0
        self._last_score = 0.0

        log.info(
            f"Wake-word model loaded: {self._keyword} "
            f"(threshold={self._threshold}, "
            f"consecutive_frames={self._consecutive_frames})"
        )

    def process_chunk(self, audio_chunk) -> bool:
        """Return True when enough consecutive chunks detect the wake word."""
        score = float(
            self._model.predict(audio_chunk).get(self._keyword, 0.0)
        )
        self._last_score = score

        if score >= self._threshold:
            self._hits += 1
        else:
            self._hits = 0

        return self._hits >= self._consecutive_frames

    def listen_for_wake_word(self) -> None:
        """Wait until the wake word is detected."""
        # Clear the model's previous audio state before listening again.
        self._model.reset()
        self._hits = 0

        log.info("Listening for wake word...")

        with sd.InputStream(
            device=MICROPHONE_DEVICE,
            samplerate=SAMPLE_RATE,
            blocksize=CHUNK_SIZE,
            dtype="int16",
            channels=1,
        ) as stream:
            while True:
                audio_chunk, _ = stream.read(CHUNK_SIZE)

                if self.process_chunk(np.squeeze(audio_chunk)):
                    print(
                        f"\nWake word detected! Score: "
                        f"{self._last_score:.2f}",
                        flush=True,
                    )
                    log.info(
                        f"Wake word detected! "
                        f"(score={self._last_score:.2f})"
                    )
                    return
