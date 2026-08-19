"""
Unit tests for response_generator.py -- ensures skill results become
speakable, natural-language text instead of raw Python data structures.
"""

from action.response_generator import ResponseGenerator
from skills.base_skill import SkillResult


def test_notes_list_becomes_natural_language():
    gen = ResponseGenerator()
    results = [
        SkillResult(
            success=True,
            data=[
                {"id": 1, "text": "buy milk", "created_at": "now"},
                {"id": 2, "text": "buy groceries", "created_at": "now"},
            ],
        )
    ]
    response = gen.generate(results)
    assert "buy milk" in response
    assert "buy groceries" in response
    assert "{" not in response  # no raw dict syntax leaking into speech


def test_empty_notes_list():
    gen = ResponseGenerator()
    results = [SkillResult(success=True, data=[])]
    response = gen.generate(results)
    assert "don't have any notes" in response


def test_failed_result_reports_error():
    gen = ResponseGenerator()
    results = [SkillResult(success=False, error="something broke")]
    response = gen.generate(results)
    assert "something broke" in response