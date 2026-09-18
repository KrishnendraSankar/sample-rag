from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.rag.prompt_builder import PromptBuilder
from app.rag.llm_service import LLMService
from app.rag.query_rewriting_service import ReWriteQuery
from app.rag.reranker_service import RerankerService


class RAGPipeline:

    def __init__(self):
        self.retriever = RetrievalPipeline()
        self.prompt_builder = PromptBuilder()
        self.llm = LLMService()
        self.reranker = RerankerService()
        self.query_rewriter = ReWriteQuery()

    def ask(
        self,
        question: str,
        tenant: str,
        top_k: int = 5,
        score_threshold: float | None = None,
    ) -> dict:

        # QUERY REWRITER
        # --------------
        rewritten_query = self.query_rewriter.rewrite_query(question)

        # -----------------------------------------
        # Step 1: Retrieve relevant chunks
        # Retrieve more chunks initially for reranking (e.g. top_k * 3)
        # -----------------------------------------
        initial_top_k = top_k * 3

        retrieved_chunks = self.retriever.retrieve(
            question=rewritten_query,
            tenant=tenant,
            top_k=initial_top_k,
            score_threshold=score_threshold,
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

        # -----------------------------------------
        # Step 3: Rerank the retrieved chunks
        # -----------------------------------------
        reranked_chunks = self.reranker.rerank(
            query=rewritten_query, chunks=retrieved_chunks, top_k=top_k
        )

        # -----------------------------------------
        # Step 4: Build prompt
        #
        # Pass complete chunk objects instead of
        # only passing their text.
        # -----------------------------------------

        prompt = self.prompt_builder.build(
            question=rewritten_query,
            chunks=reranked_chunks,
        )

        answer = self.llm.ask(prompt)

        return {"question": question, "answer": answer, "sources": reranked_chunks}
