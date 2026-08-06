"""
long_term.py

RESPONSIBILITY:
    - Persistent memory backed by SQLite (data/memory.db). Replaces the old
      JSON-file-with-Lock approach entirely -- SQLite handles concurrent
      access natively, so the RLock workaround from the old jarvis.py is no
      longer needed.

TODO (future days):
    - class LongTermMemory: remember(fact), recall(query) -> list[MemoryFact]
    - Consider a vector store (Chroma) later for semantic recall
"""
