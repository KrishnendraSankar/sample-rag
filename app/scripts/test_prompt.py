# app/scripts/test_prompt.py

from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.rag.prompt_builder import PromptBuilder


question = "How many casual leaves are allowed?"


# -----------------------------------------
# Retrieve chunks
# -----------------------------------------

retriever = RetrievalPipeline()

chunks = retriever.retrieve(
    question=question,
    top_k=3,
)


# -----------------------------------------
# Build prompt
# -----------------------------------------

prompt_builder = PromptBuilder()

prompt = prompt_builder.build(
    question=question,
    chunks=chunks,
)


# -----------------------------------------
# Print final prompt
# -----------------------------------------

print("=" * 80)

print("FINAL PROMPT SENT TO LLM")

print("=" * 80)

print()

print(prompt)