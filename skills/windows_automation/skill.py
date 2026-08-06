"""
windows_automation/skill.py

RESPONSIBILITY:
    - Thin skill wrapper around integrations/windows (pywinauto/pyautogui).
      Ports your existing desktop-automation commands here, one at a time,
      as properly isolated skills instead of inline functions in jarvis.py.

TODO (future days):
    - class WindowsAutomationSkill(BaseSkill): name="windows_automation", execute(action, target, ...)
"""
