# app/scripts/test_md_indexing.py

from app.pipeline.markdown_indexing_pipeline import (
    MarkdownIndexingPipeline,
)

file_path = "app/uploads/Global_Employee_Policy_Manual.md"


pipeline = MarkdownIndexingPipeline()


print("=" * 80)

print("STARTING MARKDOWN INDEXING")

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
