# app/pipeline/markdown_indexing_pipeline.py

from pathlib import Path
from uuid import uuid4

from app.database.mongo_service import MongoService
from app.ingestion.markdown_loader import MarkdownLoader
from app.rag.embedding_service import EmbeddingService
from app.rag.markdown_chunker import MarkdownChunker
from app.rag.vector_store import VectorStore


class MarkdownIndexingPipeline:

    def __init__(self):
        self.loader = MarkdownLoader()
        self.chunker = MarkdownChunker()
        self.embedding_service = EmbeddingService()
        self.mongo = MongoService()
        self.vector_store = VectorStore()

    def index(self, file_path: str) -> dict:
        path = Path(file_path)

        # 1. Extract Markdown document
        document = self.loader.load(file_path)

        if not document.sections:
            raise ValueError("No extractable content was found in the Markdown file.")

        # 2. Chunking
        chunks = self.chunker.chunk(document=document)

        if not chunks:
            raise ValueError("No chunks were generated from the Markdown file.")

        # 3. Build embedding text
        embedding_texts = [self.chunker.build_embedding_text(chunk) for chunk in chunks]

        # 4. Generate embeddings
        vectors = self.embedding_service.embed_chunks(embedding_texts)

        # 5. Ensure Qdrant collection exists
        vector_size = len(vectors[0])
        self.vector_store.create_collection(vector_size=vector_size)

        # 6. Store document + chunks in MongoDB
        # Note: We pass a simple adapter or the document object with required attributes for MongoDB
        self.mongo.save_document(
            document=document,
            chunks=chunks,
        )

        # 7. Store vectors + references in Qdrant
        self.vector_store.insert_chunks(
            chunks=chunks,
            vectors=vectors,
        )

        return {
            "document_id": str(document.document_id),
            "filename": path.name,
            "sections": len(document.sections),
            "chunks": len(chunks),
            "vector_dimension": vector_size,
        }
