"""
config_manager.py

RESPONSIBILITY:
    - Loads config/config.yaml + .env into a validated, typed settings object
      using pydantic-settings. Fails fast at startup if config is invalid
      (e.g. missing API key for the selected LLM backend).
    - Exposed as a singleton so every module gets the same config without
      re-parsing YAML.

TODO (future days):
    - class Settings(BaseSettings): nested models mirroring config.yaml
    - get_settings() -> Settings  (cached singleton accessor)
"""
