"""
notes/skill.py

RESPONSIBILITY:
    - Create/read/search text notes, persisted via cognition.memory.long_term
      or its own small SQLite table.
    - Implements BaseSkill; registers itself with @register_skill so the
      Planner and Executor pick it up automatically.

TODO (future days):
    - class NotesSkill(BaseSkill): name="notes", execute(action, text=None, query=None)
"""
