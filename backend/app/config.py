from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_NAME: str = "DocuLens"
    APP_VERSION: str = "1.0.0"

    API_PREFIX: str = "/api"

    DATABASE_URL: str = "sqlite+aiosqlite:///./doculens.db"

    UPLOAD_DIR: str = str(BASE_DIR / "uploads")
    CHROMA_DB_DIR: str = str(BASE_DIR / "chroma_db")

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    EMBEDDING_MODEL: str = "sentence-transformers/LaBSE"

    MAX_UPLOAD_SIZE_MB: int = 50

    class Config:
        env_file = ".env"


settings = Settings()