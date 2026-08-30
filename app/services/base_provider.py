"""
Abstract base class for LLM and embedding providers.

All provider implementations must inherit from this class
and implement the generate, embed, and embed_batch methods.
"""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Base provider interface for LLM generation and text embedding."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt for the LLM.
            temperature: Sampling temperature for generation.

        Returns:
            The generated text response.
        """

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text input.

        Args:
            text: The input text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for multiple text inputs.

        Args:
            texts: A list of input texts to embed.

        Returns:
            A list of embedding vectors, one per input text.
        """
