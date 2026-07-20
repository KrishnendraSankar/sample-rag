from qdrant_client import QdrantClient

from app.config.settings import settings


if settings.QDRANT_API_KEY:
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )
else:
    client = QdrantClient(url=settings.QDRANT_URL)

collections = client.get_collections()

print("Connected to Qdrant")
print(collections)