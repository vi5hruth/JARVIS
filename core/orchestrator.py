"""
orchestrator.py

The single coordinator of the full pipeline:
    audio -> wake word -> STT -> intent/planning -> execution -> response -> TTS

RESPONSIBILITY:
    - Owns the high-level `run()` loop / `handle_utterance()` entry point.
    - Wires together perception, cognition, and action modules via the event bus
      and the shared Context object.
    - Contains ZERO feature-specific logic. If you find yourself adding
      "if intent == 'set_reminder'" here, that logic belongs in a skill instead.

DEPENDS ON (interfaces only, never concrete skill code):
    - core.event_bus.EventBus
    - core.context.Context
    - perception.stt.base.STTEngine
    - cognition.planner.Planner
    - action.executor.Executor
    - action.tts.base.TTSEngine

TODO (future days):
    - class Orchestrator
    - async def handle_utterance(raw_text: str) -> None
    - async def run_forever() -> None  (wake word loop)
"""
