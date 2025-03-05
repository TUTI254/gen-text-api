from .openai_provider import OpenAIProvider
from .gemini_provider import GeminiProvider
class AIProviderFactory:
    providers = {
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,    # Add when available
        # "deepSeek": DeepSeekProvider,  # Add when available
        # "claude": ClaudeProvider,      # Add when available
    }

    @staticmethod
    def get_provider(provider_name: str, **kwargs):
        provider_name = provider_name.lower()
        provider_class = AIProviderFactory.providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unsupported AI provider: {provider_name}")
        return provider_class(**kwargs)
