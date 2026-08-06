"""
planner.py

RESPONSIBILITY:
    - Takes recognized text + conversation memory and produces a `Plan`:
      an ordered list of ToolCall steps (skill_name + arguments).
    - This is where "AI planning" (breaking a goal into multiple steps) lives.
      Uses an LLM (via integrations/llm) with a system prompt describing all
      currently-registered skills (pulled from skills/registry.py so the
      planner always knows about new skills automatically).

DEPENDS ON:
    - integrations.llm.base.LLMClient (interface, not a specific provider)
    - skills.registry (to enumerate available tools/skills for the LLM prompt)
    - cognition.memory (for conversation context)

TODO (future days):
    - class Planner: create_plan(text: str, context: Context) -> Plan
    - @dataclass Plan: list[ToolCall]
    - @dataclass ToolCall: skill_name: str, arguments: dict
"""
