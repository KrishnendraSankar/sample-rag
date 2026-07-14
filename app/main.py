from app.config.settings import settings
from langchain.globals import set_verbose
import logging


def main():
    set_verbose(True)
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