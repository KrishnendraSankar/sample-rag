from app.ingestion.service import IngestionService
from app.rag.chunker import DocumentChunker
from app.rag.chunk_service import ChunkService
from app.rag.embedding_service import EmbeddingService


document = IngestionService().ingest("app/uploads/employee_policy.pdf")
text_chunks = DocumentChunker().split(document.content)
chunks = ChunkService().create_chunk(document, text_chunks)

print("TOTAL CHUNKS:", len(chunks))
print("First 10 chunks:")
for chunk in chunks[:10]:
    print(f"Chunk ID: {chunk.id}, Text: {chunk.text[:50]}...")  # Print first 50 characters of each chunk

