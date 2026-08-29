# app/pipeline/docx_indexing_pipeline.py

from pathlib import Path
from uuid import uuid4

from app.database.mongo_service import (
    MongoService,
)

from app.ingestion.docx_loader import (
    DOCXLoader,
)

from app.models.document import (
    Document,
)

from app.rag.docx_chunker import (
    DOCXChunker,
)

from app.rag.embedding_service import (
    EmbeddingService,
)

from app.rag.vector_store import (
    VectorStore,
)


class DOCXIndexingPipeline:

    def __init__(self):

        self.loader = DOCXLoader()

        self.chunker = DOCXChunker()

        self.embedding_service = EmbeddingService()

        self.mongo = MongoService()

        self.vector_store = VectorStore()

    def index(
        self,
        file_path: str,
    ) -> dict:

        path = Path(file_path)

        # -------------------------------------
        # 1. Extract structured DOCX elements
        # -------------------------------------

        elements = self.loader.load(file_path)

        if not elements:

            raise ValueError("No extractable content " "was found in the DOCX file.")

        # -------------------------------------
        # 2. Build raw document text
        #
        # This is only for storing the complete
        # extracted document in MongoDB.
        # -------------------------------------

        full_text = "\n\n".join(element["text"] for element in elements)

        # -------------------------------------
        # 3. Create document
        # -------------------------------------

        document = Document(
            id=uuid4(),
            filename=path.name,
            content=full_text,
        )

        # -------------------------------------
        # 4. Heading-aware chunking
        # -------------------------------------

        chunks = self.chunker.chunk(
            document_id=document.id,
            filename=document.filename,
            elements=elements,
        )

        if not chunks:

            raise ValueError("No chunks were generated " "from the DOCX file.")

        # -------------------------------------
        # 5. Build embedding representations
        #
        # IMPORTANT:
        #
        # We don't necessarily embed only:
        #
        # chunk.text
        #
        # We enrich it with heading context.
        # -------------------------------------

        embedding_texts = [self.chunker.build_embedding_text(chunk) for chunk in chunks]

        # -------------------------------------
        # 6. Generate embeddings
        # -------------------------------------

        vectors = self.embedding_service.embed_chunks(embedding_texts)

        # -------------------------------------
        # 7. Ensure Qdrant collection exists
        # -------------------------------------

        vector_size = len(vectors[0])

        self.vector_store.create_collection(vector_size=vector_size)

        # -------------------------------------
        # 8. Store original chunk text +
        # metadata in MongoDB
        # -------------------------------------

        self.mongo.save_document(
            document=document,
            chunks=chunks,
        )

        # -------------------------------------
        # 9. Store vectors + references
        # in Qdrant
        # -------------------------------------

        self.vector_store.insert_chunks(
            chunks=chunks,
            vectors=vectors,
        )

        # -------------------------------------
        # 10. Return summary
        # -------------------------------------

        return {
            "document_id": str(document.id),
            "filename": document.filename,
            "elements": len(elements),
            "chunks": len(chunks),
            "vector_dimension": vector_size,
        }
