"""
reminders/skill.py

RESPONSIBILITY:
    - Schedule and trigger reminders using APScheduler. On trigger, publishes
      an event that the orchestrator turns into a spoken (TTS) notification
      even outside an active conversation turn.

TODO (future days):
    - class RemindersSkill(BaseSkill): name="reminders", execute(action, message, when)
"""
