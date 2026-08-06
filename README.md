# Jarvis — AI Desktop Assistant

Modular, plugin-based AI agent. See the architecture write-up from Day 1 for
full rationale. Quick orientation:

```
jarvis/
├── core/            # orchestrator, event bus, config, logging — the nervous system
├── perception/      # wake word + speech-to-text (audio -> text)
├── cognition/        # intent classification, LLM planning, memory (text -> plan)
├── action/           # executes plans, generates responses, speaks (plan -> speech)
├── skills/           # pluggable capabilities (notes, reminders, file mgmt, browser,
│                        windows automation, coding assistant) — add new ones here
│                        WITHOUT modifying core/
├── integrations/     # adapters to external systems (Playwright, pywinauto, LLM APIs)
├── interfaces/       # entry points: CLI today, FastAPI/WebSocket for the React UI later
├── config/           # config.yaml + logging.yaml — the only place hardcoded values live
├── data/             # SQLite memory db + logs
└── tests/            # unit + integration tests, mirroring the module layout
```

## Core rule
`core/` and `action/executor.py` never import a specific skill. Skills
register themselves in `skills/registry.py`. This is what lets you keep
adding capabilities without editing the pipeline.

## Status
Day 1: architecture + scaffold only. No feature implementation yet.
