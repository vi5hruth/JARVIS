
"""
vosk_engine.py

Offline speech recognition using Vosk.
Captures audio from the selected microphone at 16 kHz.
"""

import json
import queue

import sounddevice as sd
import vosk

from core.config_manager import get_settings, resolve_path
from core.logger import get_logger
from perception.stt.base import STTEngine

log = get_logger("stt")

SAMPLE_RATE = 16000
MICROPHONE_DEVICE = 1
BLOCK_SIZE = 4000


class VoskEngine(STTEngine):
    def __init__(self):
        settings = get_settings()
        vosk.SetLogLevel(-1)
        self._model = vosk.Model(
            str(resolve_path(settings.stt.model_path))
        )
        log.info("Vosk model loaded.")

    def listen_and_transcribe(self, duration_seconds: float = 4.0) -> str:
        recognizer = vosk.KaldiRecognizer(self._model, SAMPLE_RATE)
        audio_queue: queue.Queue[bytes] = queue.Queue()

        def callback(indata, frames, time_info, status):
            if status:
                log.debug(f"Audio status: {status}")
            audio_queue.put(bytes(indata))

        log.info(f"Listening for {duration_seconds} seconds...")

        with sd.RawInputStream(
            device=MICROPHONE_DEVICE,
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            sd.sleep(int(duration_seconds * 1000))

        while not audio_queue.empty():
            data = audio_queue.get()
            recognizer.AcceptWaveform(data)

        result = json.loads(recognizer.FinalResult())
        text = result.get("text", "")
        log.info(f"Transcribed: {text!r}")
        return text
