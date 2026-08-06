"""
models.py (memory)

RESPONSIBILITY:
    - Data models for conversation turns and long-term facts, shared by both
      short_term.py and long_term.py so the rest of the app has one schema
      to depend on.

TODO (future days):
    - @dataclass ConversationTurn: role, text, timestamp
    - @dataclass MemoryFact: key, value, source, timestamp
"""
