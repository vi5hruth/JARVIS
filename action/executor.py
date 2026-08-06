"""
executor.py

RESPONSIBILITY:
    - Takes a `Plan` from the cognition layer and executes each ToolCall step
      in order via the skill registry. Collects results, handles per-step
      errors (via core.exceptions), and passes results to the response
      generator.
    - This is the ONLY module that actually invokes skills. It looks skills
      up by name in the registry -- it never imports a specific skill module.

TODO (future days):
    - class Executor: run(plan: Plan, context: Context) -> list[SkillResult]
"""
