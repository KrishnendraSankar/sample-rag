"""
Embedding service that delegates embedding operations to the configured provider.

Provides a unified interface for embedding single texts and batches of chunks,
abstracting away the underlying provider implementation.
"""

import logging

from app.config.settings import settings
from app.services.huggingface_provider import HuggingfaceProvider

logger = logging.getLogger(__name__)

# Registry mapping provider names to their implementation classes
_PROVIDER_REGISTRY = {
    "huggingface": HuggingfaceProvider,
}


class EmbeddingService:
    """Service for generating text embeddings via a configurable provider.

    The provider is selected based on the ``EMBEDDING_PROVIDER`` setting.
    Currently supports:
        - ``huggingface``: Uses sentence-transformers/all-MiniLM-L6-v2
          locally for 384-dimensional embeddings.
    """

    def __init__(self) -> None:
        provider_name = settings.EMBEDDING_PROVIDER.lower()

        if provider_name not in _PROVIDER_REGISTRY:
            raise ValueError(
                f"Unknown embedding provider: '{provider_name}'. "
                f"Available providers: {list(_PROVIDER_REGISTRY.keys())}"
            )

        provider_class = _PROVIDER_REGISTRY[provider_name]
        self._client = provider_class()
        logger.info("EmbeddingService initialized with provider: %s", provider_name)

    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        return self._client.embed(text)

    def embed_chunks(self, chunks: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of text chunks.

        Uses batch encoding for efficiency when the provider supports it.

        Args:
            chunks: A list of text strings to embed.

        Returns:
            A list of embedding vectors, one per chunk.
        """
        return self._client.embed_batch(chunks)

    def embed_query(self, question: str) -> list[float]:
        """Generate an embedding vector for a search query.

        Args:
            question: The query text to embed.

        Returns:
            A list of floats representing the query embedding.
        """
        return self._client.embed(question)
