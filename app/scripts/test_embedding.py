from app.ingestion.service import IngestionService
from app.rag.chunker import DocumentChunker
from app.rag.chunk_service import ChunkService
from app.rag.embedding_service import EmbeddingService


document = IngestionService().ingest("app/uploads/employee_policy.pdf")
text_chunks = DocumentChunker().split(document.content)
chunks = ChunkService().create_chunk(document, text_chunks)

print("TOTAL CHUNKS:", len(chunks))

texts = [chunk.text for chunk in chunks]
vectors = EmbeddingService().embed_chunks(texts)

print()

print("TOTAL VECTORS:", len(vectors))

print()


print("First 10 values:")

print(vectors[0][:10])
