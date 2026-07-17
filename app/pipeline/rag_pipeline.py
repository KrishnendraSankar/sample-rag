from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.rag.prompt_builder import PromptBuilder
from app.rag.llm_service import LLMService


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalPipeline()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()

    def ask(
        self,
        question: str,
    ):
        retrieved_chunks = self.retriever.retrieve(
            question=question,
            top_k=5
        )

        texts = [chunk.text for chunk in retrieved_chunks]
        prompt = self.prompt_builder.build(
            question,
            texts
        )

        answer = self.llm.ask(prompt)

        return {
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks
        }