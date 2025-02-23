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
    FILE_CHUNK_SIZE : int

    # Ensure Pydantic loads the correct .env file dynamically
    model_config = SettingsConfigDict(env_file=str(ENV_PATH), env_file_encoding="utf-8")

def get_settings():
    return Settings()

