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

                    id=chunk.chunk_id,

                    vector=vector,

                    payload={

                        "document_id": chunk.document_id,

                        "chunk_id": chunk.chunk_id,

                    }

                )

            )

        self.client.upsert(

            collection_name=settings.COLLECTION_NAME,

            points=points

        )