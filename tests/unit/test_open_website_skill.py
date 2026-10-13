"""Unit tests for the open-website skill (skills/open_website/skill.py)."""

import pytest

from skills import registry
from skills.open_website import skill as web_skill


class FakeBrowser:
    """Stands in for webbrowser.open so no real browser is ever launched."""

    def __init__(self, result=True, error=None):
        self.result = result
        self.error = error
        self.calls = []

    def open(self, url, new=0):
        self.calls.append(url)
        if self.error:
            raise self.error
        return self.result


def use_browser(monkeypatch, **kwargs):
    fake = FakeBrowser(**kwargs)
    monkeypatch.setattr(web_skill.webbrowser, "open", fake.open)
    return fake


def test_opens_youtube_and_reports_success(monkeypatch):
    browser = use_browser(monkeypatch)
    result = web_skill.OpenWebsiteSkill().execute(site="youtube")
    assert result.success is True
    assert result.data == "Opening YouTube."
    assert browser.calls == ["https://www.youtube.com"]


def test_site_name_is_not_case_sensitive(monkeypatch):
    browser = use_browser(monkeypatch)
    result = web_skill.OpenWebsiteSkill().execute(site=" YouTube ")
    assert result.success is True
    assert browser.calls == ["https://www.youtube.com"]


def test_no_fake_success_when_no_browser_can_be_launched(monkeypatch):
    use_browser(monkeypatch, result=False)
    result = web_skill.OpenWebsiteSkill().execute(site="youtube")
    assert result.success is False
    assert "couldn't open YouTube" in result.error
    assert result.data is None


def test_no_fake_success_when_the_browser_call_raises(monkeypatch):
    use_browser(monkeypatch, error=OSError("access denied"))
    result = web_skill.OpenWebsiteSkill().execute(site="youtube")
    assert result.success is False
    assert "access denied" in result.error


def test_unknown_site_is_refused_without_opening_anything(monkeypatch):
    browser = use_browser(monkeypatch)
    result = web_skill.OpenWebsiteSkill().execute(site="example.com")
    assert result.success is False
    assert "example.com" in result.error
    assert browser.calls == []


def test_open_website_skill_is_registered():
    assert isinstance(registry.get("open_website"), web_skill.OpenWebsiteSkill)
