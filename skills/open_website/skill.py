"""
open_website/skill.py

Opens a well-known website in the user's default browser using Python's
built-in webbrowser module. Only sites listed in SITES can be opened, so a
future LLM planner can't be tricked into opening arbitrary addresses.

Success means the operating system accepted the request to open the browser.
It cannot confirm that the page finished loading.
"""

import webbrowser

from core.logger import get_logger
from skills.base_skill import BaseSkill, SkillResult
from skills.registry import register_skill

log = get_logger("open_website")

# key (what the router asks for) -> (name to speak, address to open)
SITES = {
    "youtube": ("YouTube", "https://www.youtube.com"),
}


@register_skill
class OpenWebsiteSkill(BaseSkill):
    name = "open_website"
    description = "Open a well-known website in the default browser."
    parameters_schema = {"site": "str: which site to open, e.g. 'youtube'"}

    def execute(self, site: str) -> SkillResult:
        entry = SITES.get(site.lower().strip())
        if entry is None:
            return SkillResult(success=False, error=f"I don't know how to open '{site}'.")

        label, url = entry
        try:
            opened = webbrowser.open(url, new=2)
        except Exception as e:
            log.exception(f"webbrowser.open failed for {url}")
            return SkillResult(success=False, error=f"I couldn't open {label}: {e}")

        if not opened:
            log.warning(f"webbrowser.open returned False for {url}")
            return SkillResult(
                success=False,
                error=f"I couldn't open {label}: no web browser could be launched.",
            )

        return SkillResult(success=True, data=f"Opening {label}.")
