from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
        "env_ignore_empty": True,
    }

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    LEAN_EXPLORE_BASE_URL: str = "http://localhost:8000/api/v1"

    GEMINI_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str | None = "https://openrouter.ai/api/v1"
    MODEL_NAME: str | None = "google/gemini-2.5-flash"


settings = Settings()
