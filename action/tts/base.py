"""
base.py (TTS)

Abstract interface every text-to-speech backend must implement. Strategy
pattern -- orchestrator/cli code depends on this interface only, never on
Pyttsx3Engine directly, so swapping to a different TTS backend later is a
config change, not a rewrite.
"""

from abc import ABC, abstractmethod


class TTSEngine(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        """Speak the given text out loud (blocking or queued, up to the implementation)."""
        raise NotImplementedError