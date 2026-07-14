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
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = ""
    OPENAI_MODEL: str = ""
    EMBEDDING_MODEL: str = ""

    # MongoDB
    MONGO_URI: str = ""
    MONGO_DB: str = "knowledge_db"

    # Qdrant
    QDRANT_URL: str = ""
    COLLECTION_NAME: str = "documents"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

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