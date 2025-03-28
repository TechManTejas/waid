from enum import Enum
from services.ai.gemini.gemini import GeminiAI
from services.config.config_manager import ConfigManager


class AIManagerConfig(Enum):
    SELECTED_PROVIDER = "selected_ai_provider"


class AIManager:
    _providers = {
        "gemini": GeminiAI(),
        # Add more AI providers here, e.g., "openai": OpenAI()
    }

    @classmethod
    def set_provider(cls, name: str):
        """
        Set the AI provider and persist it in the config.
        """
        if name in cls._providers:
            ConfigManager.set(AIManagerConfig.SELECTED_PROVIDER.value, name)
        else:
            raise ValueError(f"AI provider '{name}' not available.")

    @classmethod
    def get_provider(cls) -> str:
        """
        Get the currently selected AI provider from config.
        """
        return ConfigManager.get(AIManagerConfig.SELECTED_PROVIDER.value) or ""

    @classmethod
    def send_prompt(cls, prompt: str) -> str:
        """
        Send a prompt to the selected AI provider and get the response.
        """
        provider = cls._providers.get(cls.get_provider())
        if not provider:
            raise ValueError("No valid AI provider selected.")
        return provider.generate_text(prompt)

    @classmethod
    def set_configuration(cls, config_obj: dict):
        """
        Set configuration for the currently selected AI provider.
        """
        provider = cls._providers.get(cls.get_provider())
        if not provider:
            raise ValueError("No valid AI provider selected.")
        provider.set_configuration(config_obj)

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Get the configuration of the currently selected AI provider.
        """
        provider = cls._providers.get(cls.get_provider())
        if not provider:
            raise ValueError("No valid AI provider selected.")
        return provider.get_configuration()

    @classmethod
    def get_required_configuration(cls) -> list:
        """
        Get the required configuration of the currently selected AI provider.
        """
        provider = cls._providers.get(cls.get_provider())
        if not provider:
            raise ValueError("No valid AI provider selected.")
        return provider.get_required_configuration()

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of all available AI providers.
        """
        return list(cls._providers.keys())
