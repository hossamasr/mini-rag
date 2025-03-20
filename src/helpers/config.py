from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the absolute path of the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent.parent  # The script's directory

# Point to the .env file inside the 'src' folder
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_CHUNK_SIZE: int
    MONGODB_URL: str
    MONGODB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    from typing import Optional

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_API_URL: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None

    GENERATION_MODEL_ID: Optional[str] = None

    EMBEDDING_MODEL_ID: Optional[str] = None
    EMBEDDING_MODEL_SIZE: Optional[str] = None

    INPUT_DEFAULT_MAX_CHARACTERS: Optional[int] = None
    GENERATION_DEFAULT_MAX_TOKENS: Optional[int] = None
    GENERATION_DEFAULT_TEMPERATURE: Optional[float] = None

    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: Optional[str] = None

    # Ensure Pydantic loads the correct .env file dynamically
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH), env_file_encoding="utf-8")


def get_settings():
    return Settings()
