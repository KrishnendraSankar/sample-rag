"""
LLM service that delegates text generation to the configured provider.

Provides a unified interface for querying a large language model,
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


class LLMService:
    """Service for generating text responses from a large language model.

    The provider is selected based on the ``LLM_PROVIDER`` setting.
    Currently supports:
        - ``huggingface``: Uses Hugging Face Inference API with
          configurable model (e.g., Llama-3.1-8B-Instruct).
    """

    def __init__(self) -> None:
        provider_name = settings.LLM_PROVIDER.lower()

        if provider_name not in _PROVIDER_REGISTRY:
            raise ValueError(
                f"Unknown LLM provider: '{provider_name}'. "
                f"Available providers: {list(_PROVIDER_REGISTRY.keys())}"
            )

        provider_class = _PROVIDER_REGISTRY[provider_name]
        self._client = provider_class()
        logger.info("LLMService initialized with provider: %s", provider_name)

    def ask(self, prompt: str) -> str:
        """Send a prompt to the LLM and return the generated response.

        Args:
            prompt: The input prompt for the LLM.

        Returns:
            The generated text response.
        """
        return self._client.generate(prompt)
