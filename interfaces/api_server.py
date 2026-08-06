"""
api_server.py

RESPONSIBILITY:
    - FastAPI app exposing the orchestrator over HTTP/WebSocket so your
      future React UI is just another client -- it talks to the exact same
      orchestrator as the CLI and voice pipeline, nothing is duplicated.

TODO (future days):
    - POST /message  (text-based interaction, for typed chat in the UI)
    - WS /stream     (live conversation + streaming responses)
"""
