from app.pipeline.pdf_indexing_pipeline import (
    PDFIndexingPipeline,
)


file_path = (
    "app/uploads/employee_policy.pdf"
)


pipeline = PDFIndexingPipeline()


print("=" * 80)

print(
    "STARTING PDF INDEXING"
)

print("=" * 80)


result = pipeline.index(
    file_path
)


print()

print("=" * 80)

print(
    "INDEXING COMPLETE"
)

print("=" * 80)


print(
    f"Document ID      : "
    f"{result['document_id']}"
)

print(
    f"Filename         : "
    f"{result['filename']}"
)

print(
    f"Pages            : "
    f"{result['pages']}"
)

print(
    f"Chunks           : "
    f"{result['chunks']}"
)

print(
    f"Vector Dimension : "
    f"{result['vector_dimension']}"
)