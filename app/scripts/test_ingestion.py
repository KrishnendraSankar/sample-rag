from app.ingestion.service import IngestionService
from app.rag.chunker import DocumentChunker
from app.rag.chunk_service import ChunkService

document = IngestionService().ingest("app/uploads/employee_policy.pdf")
text_chunks = DocumentChunker().split(document.content)
chunks = ChunkService().create_chunk(document, text_chunks)

print("TOTAL CHUNKS:", len(chunks))

for index, chunk in enumerate(chunks, start=1):

    print("=" * 80)

    print(f"Chunk {index}")

    print("=" * 80)

    print(chunk.text)

    print()