class PromptBuilder:

    def build(
        self,
        question: str,
        chunks: list[str],
    ) -> str:

        context = "\n\n".join(chunks)

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the provided context.

If the answer is not present,
reply exactly:

I couldn't find that information.

Context
-------
{context}

Question
--------
{question}

Answer
------
"""

        return prompt