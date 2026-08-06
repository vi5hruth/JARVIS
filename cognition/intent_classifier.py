"""
intent_classifier.py

RESPONSIBILITY:
    - Fast-path classifier for simple, common commands ("what time is it",
      "stop", "volume up") that don't need a full LLM planning round-trip.
    - Chain of Responsibility: tries to match first; if no confident match,
      falls through to the full Planner. Saves latency and API cost.

TODO (future days):
    - class IntentClassifier: classify(text: str) -> Intent | None
"""
