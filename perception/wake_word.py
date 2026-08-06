"""
wake_word.py

RESPONSIBILITY:
    - Continuously listens to the microphone (lightweight, low CPU) for the
      wake phrase ("Hey Jarvis") and publishes a "WakeWordDetected" event
      when triggered. This is the ONLY module running at all times; everything
      else activates on demand.

BACKEND: openWakeWord (config-driven, see config/config.yaml -> perception.wake_word)

TODO (future days):
    - class WakeWordDetector: start(), stop(), _on_trigger()
"""
