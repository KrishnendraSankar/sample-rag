from pprint import pprint

from app.pipeline.retrieval_pipeline import RetrievalPipeline

pipeline = RetrievalPipeline()

question = "How many casual leaves are allowed?"

results = pipeline.retrieve(

    question=question,

    top_k=3

)

print("=" * 80)
print("QUESTION")
print("=" * 80)

print(question)

print()

print("=" * 80)
print("TOP MATCHES")
print("=" * 80)

for index, chunk in enumerate(results, start=1):

    print(f"Rank : {index}")

    print(f"Score : {chunk.score:.4f}")

    print(f"Chunk UUID : {chunk.chunk_id}")

    print(f"Sequence : {chunk.sequence}")

    print()

    pprint(chunk.text)

    print()

    print("-" * 80)