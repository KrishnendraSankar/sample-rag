from app.database.mongo_service import MongoService
from app.models.retrieved_chunk import RetrievedChunk
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore

class RetrievalPipeline:
    def __init__(self):
        self.mongo_service = MongoService()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
    def retrieve(self, question: str, top_k: int = 5, score_threshold: float | None = None,) -> list[RetrievedChunk]:
        # Step 1: Embed the question
        question_vector = self.embedding_service.embed_query(question)
        # print("Question Vector:", question_vector)
        # Step 2: Search for similar chunks in the vector store
        similar_chunks = self.vector_store.search(question_vector, top_k, score_threshold=score_threshold)
        # Step 3: Retrieve the full chunk text from MongoDB
        retrieved_chunks = []
        for chunk in similar_chunks:
            payload = getattr(chunk, 'payload', {}) or {}
            chunk_id = payload.get('chunk_id') or getattr(chunk, 'id', None)
            if not chunk_id:
                continue
            
            mongodata = self.mongo_service.get_chunk(str(chunk_id))
            mongo_chunk = mongodata.get('chunks') if mongodata else None
            document_name = mongodata.get('filename') if mongodata else "Unknown"
            
            if mongo_chunk:
                retrieved_chunks.append(
                    RetrievedChunk(
                        chunk_id=chunk_id,
                        sequence=payload.get('sequence', 0),
                        text=mongo_chunk['text'],
                        document_name=document_name if document_name else "Unknown",
                        score=float(getattr(chunk, 'score', 0.0) or 0.0)
                    )
                )
        return retrieved_chunks