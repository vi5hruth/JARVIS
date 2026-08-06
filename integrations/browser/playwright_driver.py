"""
playwright_driver.py

RESPONSIBILITY:
    - Wraps Playwright for real browser control (navigate, click, fill forms,
      scrape). This is where actual browser session management lives --
      skills/browser_automation/skill.py just calls into this.

TODO (future days):
    - class BrowserDriver: open(url), click(selector), fill(selector, text), close()
"""
