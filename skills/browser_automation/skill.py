"""
browser_automation/skill.py

RESPONSIBILITY:
    - Thin skill wrapper around integrations/browser (Playwright). This file
      stays thin -- actual browser driving logic lives in the integrations
      layer so it can be reused/tested independently of the skill interface.

TODO (future days):
    - class BrowserAutomationSkill(BaseSkill): name="browser_automation", execute(action, url, ...)
"""
