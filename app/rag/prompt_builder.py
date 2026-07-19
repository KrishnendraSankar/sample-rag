from app.models.retrieved_chunk import RetrievedChunk


class PromptBuilder:

    def build(
        self,
        question: str,
        chunks: list[RetrievedChunk],
    ) -> str:
        context_parts = []
        for index, chunk in enumerate(chunks):
            context_part = f""" [chunk {index}]
            Document name: {chunk.document_name}
            Chunk ID: {chunk.chunk_id}
            Sequence: {chunk.sequence}
            {chunk.text}""".strip()
            context_parts.append(context_part)

        context = "\n\n".join(context_parts)

        prompt = f"""
        You are a helpful AI assistant.

        Answer the user's question using ONLY the information provided
        in the context below.

        Rules:
        1. Do not use outside knowledge.
        2. Do not invent or assume information.
        3. If the context does not contain enough information to answer
        the question, respond exactly:
        "I couldn't find that information."
        4. Give a clear and concise answer based on the context.

        Context
        -------
        {context}

        Question
        --------
        {question}

        Answer
        ------
        """.strip()

        return prompt