"""
short_term.py

RESPONSIBILITY:
    - In-memory rolling buffer of the last N conversation turns (config:
      cognition.memory.short_term_max_turns), used to give the Planner
      immediate context without hitting the database.

TODO (future days):
    - class ShortTermMemory: add_turn(), get_recent(n) -> list[ConversationTurn]
"""
