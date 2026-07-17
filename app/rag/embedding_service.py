from langchain_openai import OpenAIEmbeddings

from app.config.settings import settings

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL
        )
    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        return self.embeddings.embed_documents(chunks)
    
    def embed_query(self, question: str) -> list[float]:
        return self.embeddings.embed_query(question)