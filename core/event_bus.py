"""
event_bus.py

Simple in-process publish/subscribe system. Modules publish events
(e.g. "speech_recognized", "plan_ready") and other modules subscribe to the
ones they care about, without ever importing each other directly.
"""

from collections import defaultdict
from typing import Callable

from core.logger import get_logger

log = get_logger("event_bus")


class EventBus:
    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Callable) -> None:
        """Register a handler to be called whenever event_name is published."""
        self._subscribers[event_name].append(handler)
        log.debug(f"Subscribed {handler.__name__} to '{event_name}'")

    def publish(self, event_name: str, payload=None) -> None:
        """Call every handler subscribed to event_name, passing it payload."""
        handlers = self._subscribers.get(event_name, [])
        log.debug(f"Publishing '{event_name}' to {len(handlers)} subscriber(s)")
        for handler in handlers:
            handler(payload)


# Singleton instance — every module imports this same bus, not the class.
event_bus = EventBus()