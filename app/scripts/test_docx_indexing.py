# app/scripts/test_docx_indexing.py

from app.pipeline.docx_indexing_pipeline import (
    DOCXIndexingPipeline,
)

file_path = "app/uploads/onboarding.docx"


pipeline = DOCXIndexingPipeline()


print("=" * 80)

print("STARTING DOCX INDEXING")

print("=" * 80)


result = pipeline.index(file_path)


print()

print("=" * 80)

print("INDEXING COMPLETE")

print("=" * 80)


print(f"Document ID      : " f"{result['document_id']}")

print(f"Filename         : " f"{result['filename']}")

print(f"Elements         : " f"{result['elements']}")

print(f"Chunks           : " f"{result['chunks']}")

print(f"Vector Dimension : " f"{result['vector_dimension']}")
