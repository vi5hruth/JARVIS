"""
context.py

RESPONSIBILITY:
    - Defines the `Context` object that flows through the entire pipeline for
      a single user request: raw audio/text, recognized intent, conversation
      history reference, the evolving Plan, intermediate skill results, and
      the final response text.
    - This is the "shared state" that gets passed between pipeline stages
      INSTEAD OF modules reaching into each other's internals.

TODO (future days):
    - @dataclass Context: request_id, timestamp, raw_text, intent, plan,
      skill_results, response_text, correlation_id (for logging)
"""
