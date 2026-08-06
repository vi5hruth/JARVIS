"""
context.py

Defines Context: the object that flows through the entire pipeline for a
single user request. Every stage (STT, planner, executor, TTS) reads from
and writes to the same Context instead of passing around loose variables.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Context:
    # Set automatically when a Context is created
    request_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: datetime = field(default_factory=datetime.now)

    # Populated by perception (STT)
    raw_text: str = ""

    # Populated by cognition (intent classifier / planner)
    intent: str | None = None
    plan: Any = None  # will become a proper Plan type once planner.py exists

    # Populated by action (executor)
    skill_results: list = field(default_factory=list)
    response_text: str = ""

    def __repr__(self) -> str:
        return f"Context(request_id={self.request_id}, raw_text={self.raw_text!r})"