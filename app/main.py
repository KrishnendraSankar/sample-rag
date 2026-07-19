from fastapi import FastAPI

from app.api.router import api_router
from app.config.settings import settings
import logging

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(api_router)


def main():
    logging.basicConfig(level=logging.DEBUG)
    print("=" * 60)
    print("RAG Learning Project")
    print("=" * 60)

    print(f"Model: {settings.OPENAI_MODEL}")
    print(f"Embedding Model: {settings.EMBEDDING_MODEL}")
    print(f"Qdrant URL: {settings.QDRANT_URL}")
    print(f"MongoDB: {settings.MONGO_DB}")
    print(f"PostgreSQL: {settings.POSTGRES_DB}")


if __name__ == "__main__":
    main()