from app.pipeline.rag_pipeline import RAGPipeline

pipeline = RAGPipeline()

question = "How many ANNUAL PAID LEAVE are allowed?"

result = pipeline.ask(question)

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
print("SOURCES")
print("=" * 80)

for source in result["sources"]:

    print(source.score)

    print(source.text)

    print("-" * 80)