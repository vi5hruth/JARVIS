"""
base.py (LLM)

RESPONSIBILITY:
    - Abstract interface for LLM providers, used by cognition/planner.py and
      any skill that needs reasoning (coding_assistant). Strategy pattern --
      switching Ollama -> Anthropic -> OpenAI is a config change.

TODO (future days):
    - class LLMClient(ABC): abstractmethod complete(prompt, tools=None) -> LLMResponse
"""
