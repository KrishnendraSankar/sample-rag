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
        top_k: int = 5
    ) ->dict:
        
        # -----------------------------------------
        # Step 1: Retrieve relevant chunks
        # -----------------------------------------
        
        retrieved_chunks = self.retriever.retrieve(
            question=question,
            top_k=top_k
        )

        # -----------------------------------------
        # Step 2: Handle empty retrieval
        # -----------------------------------------
        if not retrieved_chunks:
            return {
                "question": question,
                "answer": "I couldn't find that information.",
                "sources": [],
            }

        # texts = [chunk.text for chunk in retrieved_chunks]

        # -----------------------------------------
        # Step 3: Build prompt
        #
        # Pass complete chunk objects instead of
        # only passing their text.
        # -----------------------------------------

        prompt = self.prompt_builder.build(
            question=question,
            chunks=retrieved_chunks,
        )

        answer = self.llm.ask(prompt)

        return {
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks
        }