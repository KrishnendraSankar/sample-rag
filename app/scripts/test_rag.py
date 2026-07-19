# app/scripts/test_rag.py

from app.pipeline.rag_pipeline import RAGPipeline


pipeline = RAGPipeline()

question = "How many ANNUAL PAID LEAVE are allowed?"


result = pipeline.ask(
    question=question,
    top_k=3,
)


print("=" * 80)
print("QUESTION")
print("=" * 80)

print(result["question"])


print()

print("=" * 80)
print("ANSWER")
print("=" * 80)

print(result["answer"])


print()

print("=" * 80)
print("RETRIEVED SOURCES")
print("=" * 80)


for index, source in enumerate(
    result["sources"],
    start=1,
):

    print(f"Source       : {index}")

    print(
        f"Score        : "
        f"{source.score:.4f}"
    )

    print(
        f"Document Name: "
        f"{source.document_name}"
    )

    print(
        f"Chunk ID     : "
        f"{source.chunk_id}"
    )

    print(
        f"Sequence     : "
        f"{source.sequence}"
    )

    print()

    print("Text:")

    print(source.text)

    print()

    print("-" * 80)