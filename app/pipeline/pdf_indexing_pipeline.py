from pathlib import Path
from uuid import uuid4

from app.database.mongo_service import (
    MongoService,
)
from app.ingestion.pdf_loader import (
    PDFLoader,
)
from app.models.document import Document
from app.rag.embedding_service import (
    EmbeddingService,
)
from app.rag.pdf_chunker import (
    PDFChunker,
)
from app.rag.vector_store import (
    VectorStore,
)


class PDFIndexingPipeline:

    def __init__(self):

        self.loader = PDFLoader()

        self.chunker = PDFChunker()

        self.embedding_service = EmbeddingService()

        self.mongo = MongoService()

        self.vector_store = VectorStore()

    def index(
        self,
        file_path: str,
    ) -> dict:

        path = Path(
            file_path
        )

        # -------------------------------------
        # 1. Extract PDF page-by-page
        # -------------------------------------

        pages = self.loader.load(
            file_path
        )

        if not pages:

            raise ValueError(
                "No extractable text "
                "was found in the PDF."
            )

        # -------------------------------------
        # 2. Build complete raw text
        #
        # MongoDB still stores the original
        # extracted document content.
        # -------------------------------------

        full_text = "\n\n".join(

            page["text"]

            for page in pages

        )

        # -------------------------------------
        # 3. Create document
        # -------------------------------------

        document = Document(

            id=uuid4(),

            filename=path.name,

            content=full_text,
        )

        # -------------------------------------
        # 4. Create page-aware chunks
        # -------------------------------------

        chunks = self.chunker.chunk(

            document_id=document.id,

            filename=document.filename,

            pages=pages,
        )

        if not chunks:

            raise ValueError(
                "No chunks were generated."
            )

        # -------------------------------------
        # 5. Generate embeddings
        #
        # IMPORTANT:
        # We embed only chunk text.
        #
        # UUID, page number, etc.
        # are metadata, not embedding input.
        # -------------------------------------

        texts = [chunk.text for chunk in chunks]

        vectors = self.embedding_service.embed_chunks(texts)

        # -------------------------------------
        # 6. Ensure Qdrant collection exists
        # -------------------------------------

        vector_size = len(
            vectors[0]
        )

        self.vector_store.create_collection(
            vector_size=vector_size
        )

        # -------------------------------------
        # 7. Store document + chunks
        # in MongoDB
        # -------------------------------------

        self.mongo.save_document(

            document=document,

            chunks=chunks,
        )

        # -------------------------------------
        # 8. Store vectors + references
        # in Qdrant
        # -------------------------------------

        self.vector_store.insert_chunks(

            chunks=chunks,

            vectors=vectors,
        )

        # -------------------------------------
        # 9. Return indexing summary
        # -------------------------------------

        return {

            "document_id":
                str(document.id),

            "filename":
                document.filename,

            "pages":
                len(pages),

            "chunks":
                len(chunks),

            "vector_dimension":
                vector_size,
        }