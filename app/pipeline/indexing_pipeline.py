from app.ingestion.service import IngestionService
from app.rag.chunker import DocumentChunker
from app.rag.chunk_service import ChunkService
from app.rag.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.database.mongo_service import MongoService


class IndexingPipeline:

    def __init__(self):

        self.ingestion = IngestionService()

        self.chunker = DocumentChunker()

        self.chunk_service = ChunkService()

        self.embedding = EmbeddingService()

        self.vector_store = VectorStore()

        self.mongo = MongoService()

    def index_document(self, file_path, tenant_id="hr_dept"):
        # document
        document = self.ingestion.ingest(file_path)

        # chunking
        chunk_strings = self.chunker.split(document.content)
        chunks = self.chunk_service.create_chunk(document, chunk_strings)

        # save in mongo db
        self.mongo.save_document(document, chunks)

        # Generating Dense Vectors
        dense_vectors = self.embedding.embed_chunks([chunk.text for chunk in chunks])

        # Generating Sparse Vectors
        sparse_vectors = self.embedding.compute_sparse_vector(
            [chunk.text for chunk in chunks]
        )

        self.vector_store.create_collection(len(dense_vectors[0]))

        self.vector_store.insert_chunks(
            chunks, dense_vectors, sparse_vectors, tenant_id
        )

        return document
