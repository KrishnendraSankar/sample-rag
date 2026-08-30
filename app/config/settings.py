from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Knowledge Platform"
    app_version: str = "1.0.0"
    app_env: str = "development"

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "knowledge_db"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""

    # GitHub Models
    OPENAI_API_KEY: SecretStr = SecretStr("")
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = ""
    EMBEDDING_MODEL: str = ""

    # ====================================================
    # model configuration
    # ====================================================

    LLM_PROVIDER: str = ""
    LLM_MODEL: str = ""
    LLM_API_KEY: str = ""
    LLM_BASE_URL: str = ""

    #################################
    # EMBEDDINGS
    #################################

    EMBEDDING_PROVIDER: str = ""

    EMBEDDING_MODEL: str = ""
    EMBEDDING_API_KEY: str = ""
    EMBEDDING_BASE_URL: str = ""

    # MongoDB
    MONGO_URI: str = ""
    MONGO_DB: str = "knowledge_db"

    # Qdrant
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    COLLECTION_NAME: str = "documents"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()
