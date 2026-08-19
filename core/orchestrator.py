"""
orchestrator.py

Coordinates the pipeline: raw text -> (for now, hardcoded routing) ->
executor -> response text.

TEMPORARY: routing is hardcoded here instead of using an LLM planner, so we
can prove the rest of the pipeline works in isolation first. This entire
_route() method gets replaced by cognition/planner.py later -- nothing else
in this file, or in executor.py, will need to change when that happens.
"""

from action.executor import Executor, ToolCall
from core.context import Context
from core.logger import get_logger

log = get_logger("orchestrator")


class Orchestrator:
    def __init__(self):
        self.executor = Executor()

    def _route(self, text: str) -> list[ToolCall]:
        """TEMPORARY hardcoded routing. Replaced by the LLM planner later."""
        text_lower = text.lower().strip()

        if text_lower.startswith("note "):
            note_text = text[len("note "):].strip()
            return [ToolCall(skill_name="notes", arguments={"action": "create", "text": note_text})]

        if text_lower in ("list notes", "show notes"):
            return [ToolCall(skill_name="notes", arguments={"action": "list"})]

        return []

    def handle_text(self, text: str) -> str:
        context = Context(raw_text=text)
        log.info(f"[{context.request_id}] Received: {text}")

        tool_calls = self._route(text)
        if not tool_calls:
            return "Sorry, I don't understand that yet."

        results = self.executor.run(tool_calls)
        context.skill_results = results

        # Turn results into a simple response string (real response_generator.py comes later)
        parts = []
        for result in results:
            if result.success:
                parts.append(str(result.data))
            else:
                parts.append(f"Error: {result.error}")

        context.response_text = " | ".join(parts)
        log.info(f"[{context.request_id}] Response: {context.response_text}")
        return context.response_text