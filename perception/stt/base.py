"""
base.py (STT)

RESPONSIBILITY:
    - Abstract interface every speech-to-text backend must implement.
    - Strategy pattern: orchestrator/cognition code depends on this interface
      only, never on VoskEngine directly, so swapping to Whisper later is a
      config change, not a rewrite.

TODO (future days):
    - class STTEngine(ABC): abstractmethod transcribe(audio_bytes) -> str
"""
