from qdrant_client import QdrantClient
from qdrant_client.models import Distance
from qdrant_client.models import VectorParams
from qdrant_client.models import PointStruct
from qdrant_client.models import Filter
from qdrant_client.models import FieldCondition
from qdrant_client.models import MatchValue
from qdrant_client.models import PayloadSchemaType

from app.config.settings import settings
from app.models.chunk import Chunk
from app.models.metadata_config import (
    QDRANT_FILTERABLE_FIELDS,
)


class VectorStore:
    def __init__(self):
        if settings.QDRANT_API_KEY:
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
            )
        else:
            self.client = QdrantClient(url=settings.QDRANT_URL)

    def create_collection(self, vector_size: int):
        collections = self.client.get_collections()

        existing_collections = {
            collection.name for collection in collections.collections
        }

        if settings.COLLECTION_NAME not in existing_collections:
            self.client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

        # Create payload index for filtering by tenant
        self.client.create_payload_index(
            collection_name=settings.COLLECTION_NAME,
            field_name="tenant",
            field_schema=PayloadSchemaType.KEYWORD,
        )
        return

    def build_qdrant_payload(self, chunk: Chunk, tenant_id: str) -> dict:
        """
        Build payload that will be stored
        in Qdrant.

        Large metadata stays in MongoDB.

        Only searchable/filterable metadata
        is copied into Qdrant.
        """

        payload = {
            "document_id": str(chunk.document_id),
            "chunk_id": str(chunk.id),
            "sequence": chunk.sequence,
            "tenant": tenant_id,
        }

        for key, value in chunk.metadata.items():

            if key in QDRANT_FILTERABLE_FIELDS:

                payload[key] = value

        return payload

    # ---------------------------------------------------------

    def insert_chunks(self, chunks, vectors, tenant_id):

        if len(chunks) != len(vectors):

            raise ValueError("Chunks and vectors count mismatch.")

        points = []

        for chunk, vector in zip(
            chunks,
            vectors,
        ):

            payload = self.build_qdrant_payload(chunk, tenant_id)

            points.append(
                PointStruct(
                    id=str(chunk.id),
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=settings.COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
        score_threshold: float | None = None,
    ):
        """Search Similar vectors in Qdrant Collection."""
        result = self.client.query_points(
            collection_name=settings.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
            with_vectors=False,
            score_threshold=score_threshold,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="tenant",
                        match=MatchValue(value="finance_dept"),
                    )
                ]
            ),
        )
        return result.points
