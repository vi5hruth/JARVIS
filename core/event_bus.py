"""
event_bus.py

Simple in-process publish/subscribe system (Observer pattern).

RESPONSIBILITY:
    - Decouples every module from every other module. Modules publish events
      ("SpeechRecognized", "PlanReady", "SkillExecuted", "ResponseReady") and
      subscribe to the ones they care about. No module should ever import
      another module's internals just to call it directly.

WHY THIS MATTERS FOR SCALABILITY:
    - Adding a new skill or module never requires modifying an existing
      module's imports -- it just subscribes to existing events.

TODO (future days):
    - class EventBus: subscribe(event_name, handler), publish(event_name, payload)
    - Consider asyncio.Queue-backed implementation for true async dispatch
"""
