"""
file_manager/skill.py

RESPONSIBILITY:
    - File operations (find, move, rename, summarize, open) scoped to safe,
      configured directories. Uses pathlib + watchdog for monitoring where
      needed.

TODO (future days):
    - class FileManagerSkill(BaseSkill): name="file_manager", execute(action, path, ...)
"""
