"""
cli.py

RESPONSIBILITY:
    - Thin entry point for running Jarvis from the terminal (today's client).
    - Wires up config, logging, and the orchestrator, then starts the wake
      word loop. Contains NO business logic -- it's purely composition root.

TODO (future days):
    - def main(): load config, setup_logging(), build Orchestrator, run_forever()
"""
