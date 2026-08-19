"""
notes/skill.py

Create, list, and search simple text notes, persisted to SQLite.
Implements BaseSkill and registers itself -- the planner and executor will
pick this up automatically via skills/registry.py, with zero changes to
either of those files.
"""

import sqlite3
from pathlib import Path

from core.config_manager import get_settings
from skills.base_skill import BaseSkill, SkillResult
from skills.registry import register_skill


def _get_db_path() -> Path:
    settings = get_settings()
    return Path(settings.memory.db_path)


def _ensure_table():
    db_path = _get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


@register_skill
class NotesSkill(BaseSkill):
    name = "notes"
    description = "Create a note, or list all existing notes."
    parameters_schema = {
        "action": "str: 'create' or 'list'",
        "text": "str: the note content (required if action is 'create')",
    }

    def execute(self, action: str, text: str = "") -> SkillResult:
        conn = None
        try:
            _ensure_table()
            db_path = _get_db_path()
            conn = sqlite3.connect(db_path)

            if action == "create":
                if not text:
                    return SkillResult(success=False, error="No text provided for note.")
                conn.execute("INSERT INTO notes (text) VALUES (?)", (text,))
                conn.commit()
                return SkillResult(success=True, data=f"Note saved: {text}")

            elif action == "list":
                rows = conn.execute("SELECT id, text, created_at FROM notes ORDER BY id DESC").fetchall()
                notes = [{"id": r[0], "text": r[1], "created_at": r[2]} for r in rows]
                return SkillResult(success=True, data=notes)

            else:
                return SkillResult(success=False, error=f"Unknown action '{action}'")

        except Exception as e:
            return SkillResult(success=False, error=str(e))

        finally:
            if conn:
                conn.close()