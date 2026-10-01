import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from common.utils import getAbsPathLocatedFromCurFile


class Settings(BaseSettings):
    app_name: str = "Conversational RAG Assistant"
    env: str = os.getenv("PY_ENV", "local")

    openai_api_key: str = ""
    redis_url: str = "redis://localhost:6379"

    # Only required when env != 'local' (Cassandra/Astra DB vector store)
    astra_db_id: str = ""
    astra_db_token: str = ""

    model_config = SettingsConfigDict(
        env_file=getAbsPathLocatedFromCurFile(__file__, "./.env." + os.getenv("PY_ENV", "local")),
        env_file_encoding="utf-8",
        extra="ignore",
    )


SETTINGS = Settings()
