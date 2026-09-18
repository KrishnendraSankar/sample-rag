from pydantic import BaseModel, Field

from app.rag.llm_service import LLMService
from app.rag.prompt_builder import PromptBuilder


class RewrittenQuery(BaseModel):
    reasoning: str = Field(
        description="Brief explanation of why the query needs to be rewritten and what domain keywords are missing."
    )
    optimized_query: str = Field(
        description="The final, keyword-optimized search query stripped of conversational fluff."
    )


class ReWriteQuery:
    def __init__(self):
        self.llm = LLMService()
        self.prompt_builder = PromptBuilder()

    def rewrite_query(self, user_query: str) -> str:
        """Takes a messy user query and transforms it into a vector-search optimized query."""

        system_prompt = (
            "You are an expert search engine optimizer inside a RAG pipeline.\n"
            "The knowledge base contains company HR and Finance policy documents, "
            "including topics like leave policies, payroll, reimbursements, "
            "employee benefits, hiring, and compliance.\n\n"
            "Your job is to transform conversational, vague, or grammatically poor user queries "
            "into highly targeted, keyword-rich search strings designed for a vector database.\n\n"
            "Rules:\n"
            "1. Remove conversational elements like 'Can you tell me', 'please', 'I want to know'.\n"
            "2. Infer missing domain terms from the HR/Finance context "
            "(e.g., 'days off' → 'annual leave entitlement', 'leaving the company' → 'employee resignation policy').\n"
            "3. Keep the optimized query concise (ideally under 10 words).\n"
            "4. Do not alter the core intent or meaning of the query.\n"
            "5. Return ONLY the rewritten query string. No explanation, no extra text."
        )

        print("SYSTEM PROMPT", system_prompt)

        answer = self.llm.ask(user_query, system_prompt)

        # 2. Call the LLM with structured parsing enabled
        # completion = client.beta.chat.completions.parse(
        #     model="gpt-4o-mini",  # Use a fast, cost-efficient model for parsing tasks
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_query}
        #     ],
        #     response_format=RewrittenQuery,
        # )

        # Return the strongly-typed parsed object
        # return completion.choices[0].message.parsed
        print("REWRITE QUERY===============================", answer)
        return answer
