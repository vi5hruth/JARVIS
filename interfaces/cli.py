"""
cli.py

Entry point for running Jarvis from the terminal. Composition root: wires up
logging, skill discovery, and the orchestrator, then runs a simple input
loop. Contains no business logic of its own.
"""

from core.logger import setup_logging, get_logger
from core.orchestrator import Orchestrator
from skills.registry import discover

log = get_logger("cli")


def main():
    setup_logging()
    discover()
    orchestrator = Orchestrator()

    print("Jarvis (text mode) -- type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye.")
            break

        response = orchestrator.handle_text(user_input)
        print(f"Jarvis: {response}\n")


if __name__ == "__main__":
    main()