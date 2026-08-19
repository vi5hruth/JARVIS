"""
response_generator.py

Converts raw skill results into natural-language response strings. This is
where "list of dicts" becomes "you have 3 notes: ..." instead of the
orchestrator dumping raw Python data structures at the TTS engine.
"""

from skills.base_skill import SkillResult


class ResponseGenerator:
    def generate(self, results: list[SkillResult]) -> str:
        parts = []
        for result in results:
            if not result.success:
                parts.append(f"Something went wrong: {result.error}")
                continue

            data = result.data

            # Notes-list shape: a list of dicts with 'text' keys
            if isinstance(data, list) and all(isinstance(d, dict) and "text" in d for d in data):
                if not data:
                    parts.append("You don't have any notes yet.")
                else:
                    note_texts = [d["text"] for d in data]
                    parts.append(f"You have {len(note_texts)} notes: " + "; ".join(note_texts))

            # Everything else: just speak it as-is (e.g. "Note saved: buy milk")
            else:
                parts.append(str(data))

        return " ".join(parts)