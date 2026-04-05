from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    OPENAI_API_KEY: str
    database_url: PostgresDsn
    redis_url: RedisDsn
    jwt_secret: str
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    prometheus_disable: bool = False
    chunk_size: int = 800
    chunk_overlap: int = 80
    llm_model: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    DATABASE_URL: str
    openai_api_key: Optional[str] = None
    prometheus_disable_metrics: bool = False
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # Allows unknown env vars
    }

settings = Settings()