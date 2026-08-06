"""
config_manager.py

Loads config/config.yaml and .env into a validated, typed settings object.
Exposed as a singleton via get_settings() so every module reads the same
config without re-parsing YAML each time.
"""

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


class WakeWordConfig(BaseModel):
    backend: str
    keyword: str


class STTConfig(BaseModel):
    backend: str
    model_path: str


class TTSConfig(BaseModel):
    backend: str
    rate: int


class LLMConfig(BaseModel):
    backend: str
    model: str


class PlannerConfig(BaseModel):
    fast_path_enabled: bool


class MemoryConfig(BaseModel):
    short_term_max_turns: int
    db_path: str


class LoggingConfig(BaseModel):
    level: str
    log_path: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Secrets / environment-specific values (from .env)
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    ollama_host: str = "http://localhost:11434"
    jarvis_env: str = "development"

    # Values loaded from config.yaml (populated in load_settings, not from env)
    wake_word: WakeWordConfig = None
    stt: STTConfig = None
    tts: TTSConfig = None
    llm: LLMConfig = None
    planner: PlannerConfig = None
    memory: MemoryConfig = None
    logging: LoggingConfig = None


@lru_cache
def get_settings() -> Settings:
    """Load config.yaml + .env once, cache the result for the app's lifetime."""
    with open(CONFIG_PATH, "r") as f:
        raw = yaml.safe_load(f)

    settings = Settings(
        wake_word=WakeWordConfig(**raw["perception"]["wake_word"]),
        stt=STTConfig(**raw["perception"]["stt"]),
        tts=TTSConfig(**raw["action"]["tts"]),
        llm=LLMConfig(**raw["cognition"]["llm"]),
        planner=PlannerConfig(**raw["cognition"]["planner"]),
        memory=MemoryConfig(**raw["cognition"]["memory"]),
        logging=LoggingConfig(**raw["logging"]),
    )
    return settings