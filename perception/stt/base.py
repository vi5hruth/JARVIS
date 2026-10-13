"""
base.py (STT)

Abstract interface every speech-to-text backend must implement. Strategy
pattern -- callers depend on this interface only, never on VoskEngine
directly, so swapping to a different STT backend later is a config change.
"""

from abc import ABC, abstractmethod


class STTEngine(ABC):
    @abstractmethod
    def listen_and_transcribe(self) -> str:
        """Record audio from the microphone and return the transcribed text."""
        raise NotImplementedError