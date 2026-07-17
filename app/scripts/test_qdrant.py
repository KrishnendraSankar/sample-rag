from qdrant_client import QdrantClient

from app.config.settings import settings


client = QdrantClient(url=settings.QDRANT_URL)

# Get collection information
collection = client.get_collection(settings.COLLECTION_NAME)

print("=" * 60)
print("Collection Information")
print("=" * 60)
print(f"Name           : {settings.COLLECTION_NAME}")
print(f"Vector Count   : {collection.points_count}")
print(f"Vector Size    : {collection.config.params.vectors.size}")
print()

# Retrieve the first point
points, _ = client.scroll(
    collection_name=settings.COLLECTION_NAME,
    limit=1,
    with_payload=True,
    with_vectors=False,
)

if not points:
    print("No vectors found.")
    exit()

point = points[0]

print("=" * 60)
print("Sample Stored Vector")
print("=" * 60)
print(f"Point ID       : {point.id}")
print(f"Document ID    : {point.payload['document_id']}")
print(f"Chunk ID       : {point.payload['chunk_id']}")