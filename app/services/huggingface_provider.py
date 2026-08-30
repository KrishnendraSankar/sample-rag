"""
Hugging Face provider for LLM generation and local embedding.

Uses the Hugging Face Inference API for LLM generation and the
sentence-transformers library for local embedding with the
all-MiniLM-L6-v2 model (384-dimensional vectors).
"""

import logging
from typing import ClassVar

from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer

from app.config.settings import settings
from app.services.base_provider import BaseProvider

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
_EMBEDDING_DIMENSION: int = 384


class HuggingfaceProvider(BaseProvider):
    """Provider that uses Hugging Face services for LLM and embeddings.

    LLM generation is handled via the Hugging Face Inference API.
    Text embedding is performed locally using the sentence-transformers
    all-MiniLM-L6-v2 model for fast, accurate semantic embeddings.

    The SentenceTransformer model is loaded once as a class-level singleton
    to avoid repeated model loading across multiple provider instances.
    """

    # Class-level singleton for the embedding model to avoid reloading
    _embedding_model: ClassVar[SentenceTransformer | None] = None

    def __init__(self) -> None:
        # ---- LLM Client (remote via Inference API) ----
        self._llm_client = InferenceClient(
            provider="novita",
            api_key=settings.LLM_API_KEY,
        )
        self._llm_model = settings.LLM_MODEL

        # ---- Embedding Model (local via sentence-transformers) ----
        if HuggingfaceProvider._embedding_model is None:
            logger.info(
                "Loading sentence-transformers model: %s",
                _EMBEDDING_MODEL_NAME,
            )
            HuggingfaceProvider._embedding_model = SentenceTransformer(
                _EMBEDDING_MODEL_NAME,
            )
            logger.info(
                "Model loaded successfully (dimension=%d)",
                _EMBEDDING_DIMENSION,
            )

    # ------------------------------------------------------------------
    # LLM Generation
    # ------------------------------------------------------------------

    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate a response from the Hugging Face LLM.

        Args:
            prompt: The user prompt to send to the LLM.
            temperature: Sampling temperature for response generation.

        Returns:
            The generated text response from the model.
        """
        response = self._llm_client.chat.completions.create(
            model=self._llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return response.choices[0].message.content or ""

    # ------------------------------------------------------------------
    # Embedding
    # ------------------------------------------------------------------

    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text input.

        Uses sentence-transformers/all-MiniLM-L6-v2 locally to produce
        a 384-dimensional dense vector.

        Args:
            text: The input text to embed.

        Returns:
            A list of 384 floats representing the embedding vector.
        """
        if self._embedding_model is None:
            raise RuntimeError("Embedding model is not initialized.")

        embedding = self._embedding_model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for multiple texts in a single batch.

        Batch encoding is more efficient than encoding texts one by one
        because it leverages GPU/CPU parallelism internally.

        Args:
            texts: A list of input texts to embed.

        Returns:
            A list of embedding vectors (each 384-dimensional).
        """
        if not texts:
            return []

        if self._embedding_model is None:
            raise RuntimeError("Embedding model is not initialized.")

        embeddings = self._embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def get_embedding_dimension() -> int:
        """Return the embedding vector dimension for the current model.

        Returns:
            The embedding dimension (384 for all-MiniLM-L6-v2).
        """
        return _EMBEDDING_DIMENSION
