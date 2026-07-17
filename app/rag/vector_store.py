from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct

from app.config.settings import settings


class VectorStore:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
        )
    
    def create_collection(self, vector_size: int):
        collections = self.client.get_collections()

        existing_collections = {collection.name for collection in collections.collections}

        if settings.COLLECTION_NAME in existing_collections:
            return

        self.client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        return
    
    def insert_chunks(self, chunks, vectors ):
        points = []
        for chunk, vector in zip(chunks, vectors):
            points.append(
                PointStruct(
                    id=str(chunk.id),
                    vector=vector,
                    payload={
                        "document_id": str(chunk.document_id),
                        "chunk_id": str(chunk.id),
                        "sequence": chunk.sequence,
                    }
                )
            )
        self.client.upsert(
            collection_name=settings.COLLECTION_NAME,
            points=points
        )
    def search(self, query_vector: list[float], limit: int=5):
        """Search Similar vectors in Qdrant Collection."""
        result = self.client.query_points(
            collection_name=settings.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )
        return result.points