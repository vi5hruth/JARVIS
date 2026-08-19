"""
Unit tests for the notes skill and the plugin registry mechanism.
"""

import os
import tempfile

import pytest

from skills.notes.skill import NotesSkill


@pytest.fixture
def temp_db(monkeypatch):
    """Point the notes skill at a throwaway SQLite file for this test only."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    from core.config_manager import get_settings
    settings = get_settings()
    original_path = settings.memory.db_path
    settings.memory.db_path = path

    yield path

    settings.memory.db_path = original_path
    os.remove(path)


def test_create_note(temp_db):
    skill = NotesSkill()
    result = skill.execute(action="create", text="Test note")
    assert result.success is True
    assert "Test note" in result.data


def test_list_notes(temp_db):
    skill = NotesSkill()
    skill.execute(action="create", text="First note")
    skill.execute(action="create", text="Second note")
    result = skill.execute(action="list")
    assert result.success is True
    assert len(result.data) == 2


def test_create_note_without_text_fails(temp_db):
    skill = NotesSkill()
    result = skill.execute(action="create", text="")
    assert result.success is False
    assert result.error is not None


def test_unknown_action_fails(temp_db):
    skill = NotesSkill()
    result = skill.execute(action="delete_everything")
    assert result.success is False