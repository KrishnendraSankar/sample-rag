from uuid import uuid4

from app.ingestion.docx_loader import (
    DOCXLoader,
)

from app.rag.docx_chunker import (
    DOCXChunker,
)

file_path = "app/uploads/onboarding.docx"


loader = DOCXLoader()

chunker = DOCXChunker()


elements = loader.load(file_path)


chunks = chunker.chunk(
    document_id=uuid4(),
    filename="employee_handbook.docx",
    elements=elements,
)


for chunk in chunks[:5]:

    print("=" * 80)

    print(f"Chunk ID: {chunk.id}")

    print(f"Sequence: {chunk.sequence}")

    print()

    print("METADATA")

    print(chunk.metadata)

    print()

    print("STORED TEXT")

    print(chunk.text)

    print()

    print("EMBEDDING TEXT")

    print(chunker.build_embedding_text(chunk))

    print()
