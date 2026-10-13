
"""
orchestrator.py

Coordinates command routing, skill execution, and response generation.
"""

import re

from action.response_generator import ResponseGenerator
from action.executor import Executor, ToolCall
from core.context import Context
from core.logger import get_logger

log = get_logger("orchestrator")


TIME_PHRASES = {
    "what time is it",
    "what time is it now",
    "what is the time",
    "what is the time now",
    "what is the current time",
    "whats the time",
    "whats the time now",
    "whats the current time",
    "tell me the time",
    "tell me the current time",
    "current time",
}


def _normalize(text: str) -> str:
    """Normalize spoken commands for reliable matching."""
    text = text.lower().replace("’", "'")
    text = text.replace("you tube", "youtube")
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if text.endswith(" please"):
        text = text[:-7].strip()

    return text


class Orchestrator:
    def __init__(self):
        self.executor = Executor()
        self.response_generator = ResponseGenerator()

    def _route(self, text: str) -> list[ToolCall]:
        """Route normalized commands to the appropriate skill."""
        command = _normalize(text)

        # Create a note.
        if command.startswith("note "):
            note_text = command[len("note "):].strip()
            return [
                ToolCall(
                    skill_name="notes",
                    arguments={
                        "action": "create",
                        "text": note_text,
                    },
                )
            ]

        # List saved notes.
        if command in ("list notes", "show notes"):
            return [
                ToolCall(
                    skill_name="notes",
                    arguments={"action": "list"},
                )
            ]

        # Tell the current time.
        if command in TIME_PHRASES:
            return [
                ToolCall(
                    skill_name="time",
                    arguments={},
                )
            ]

        # Open YouTube.
        if command in (
            "open youtube",
            "open up youtube",
            "launch youtube",
            "go to youtube",
            "youtube",
        ):
            return [
                ToolCall(
                    skill_name="open_website",
                    arguments={"site": "youtube"},
                )
            ]

        # Unknown command.
        return []

    def handle_text(self, text: str) -> str:
        """Execute a command and return Jarvis's response."""
        context = Context(raw_text=text)
        log.info(f"[{context.request_id}] Received: {text}")

        tool_calls = self._route(text)

        if not tool_calls:
            return "Sorry, I don't understand that yet."

        results = self.executor.run(tool_calls)
        context.skill_results = results

        context.response_text = self.response_generator.generate(results)

        log.info(
            f"[{context.request_id}] Response: {context.response_text}"
        )

        return context.response_text
