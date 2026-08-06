"""
pyttsx3_engine.py

RESPONSIBILITY:
    - Concrete TTSEngine using pyttsx3. Formalizes the dedicated-worker-thread
      + queue pattern you already built to solve the pyttsx3/COM threading
      issues on Windows -- that fix becomes this class's internal design,
      not a workaround bolted onto a script.

TODO (future days):
    - class Pyttsx3Engine(TTSEngine): internal queue + worker thread, speak()
"""
