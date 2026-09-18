from typing import List

from langchain_core.documents import Document
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from app.config.settings import settings
from app.models.retrieved_chunk import RetrievedChunk


class RerankerService:
    def __init__(self):
        # Initialize the HuggingFace CrossEncoder model for reranking
        model_name = settings.RERANKER_MODEL
        try:
            self.model = HuggingFaceCrossEncoder(model_name=model_name)
            self.compressor = CrossEncoderReranker(model=self.model, top_n=5)
        except Exception as e:
            print(f"Failed to initialize reranker model {model_name}: {e}")
            self.model = None
            self.compressor = None

    def rerank(
        self, query: str, chunks: List[RetrievedChunk], top_k: int = 5
    ) -> List[RetrievedChunk]:
        """
        Reranks a list of RetrievedChunk objects based on their relevance to the query.
        """
        if not chunks:
            return []

        if not self.compressor:
            # If initialization failed, return original chunks (fallback)
            return chunks[:top_k]

        # Temporarily update top_n based on the requested top_k
        self.compressor.top_n = top_k

        # Convert RetrievedChunk to Langchain Document
        documents = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk.text,
                metadata={
                    "chunk_id": str(chunk.chunk_id),
                    "sequence": chunk.sequence,
                    "document_name": chunk.document_name,
                    "original_score": chunk.score,
                },
            )
            documents.append(doc)

        # Rerank
        try:
            reranked_docs = self.compressor.compress_documents(
                documents=documents, query=query
            )
        except Exception as e:
            print(f"Error during reranking: {e}")
            return chunks[:top_k]

        # Convert back to RetrievedChunk
        reranked_chunks = []
        for doc in reranked_docs:
            chunk_id = doc.metadata.get("chunk_id")
            # In Python, UUID handles string initialization correctly if needed, but we used str() above.
            # Convert back to UUID if chunk_id is a string. We'll import UUID if needed,
            # but since we already have RetrievedChunk, let's keep it as is.
            # retrieved_chunk.py uses UUID from uuid.
            from uuid import UUID

            reranked_chunks.append(
                RetrievedChunk(
                    chunk_id=UUID(chunk_id),
                    sequence=doc.metadata.get("sequence", 0),
                    text=doc.page_content,
                    document_name=doc.metadata.get("document_name", "Unknown"),
                    score=float(
                        doc.metadata.get(
                            "relevance_score", doc.metadata.get("original_score", 0.0)
                        )
                    ),
                )
            )

        return reranked_chunks
