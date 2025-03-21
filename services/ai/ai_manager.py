from services.ai.gemini.gemini import GeminiAI


class AIManager:
    _providers = {"gemini": GeminiAI}
    _selected_provider = "gemini"

    @classmethod
    def set_provider(cls, name: str):
        if name in cls._providers:
            cls._selected_provider = name
        else:
            raise ValueError(f"AI provider '{name}' not available.")

    @classmethod
    def get_provider(cls) -> str:
        """
        Get the currently selected AI provider.
        """
        return cls._selected_provider

    @classmethod
    def send_prompt(cls, prompt: str) -> str:
        """
        Send a prompt to the selected AI provider and get the response.
        """
        provider = cls._providers.get(cls._selected_provider)
        if not provider:
            raise ValueError("No valid AI provider selected.")
        return provider.generate_text(prompt)

    @classmethod
    def set_configuration(cls, config_obj: dict):
        """
        Set configuration for the currently selected AI provider.
        """
        provider = cls._providers.get(cls._selected_provider)
        if not provider:
            raise ValueError("No valid AI provider selected.")
        provider.set_configuration(config_obj)

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Get the configuration of the currently selected AI provider.
        """
        provider = cls._providers.get(cls._selected_provider)
        if not provider:
            raise ValueError("No valid AI provider selected.")
        return provider.get_configuration()

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get a list of all available AI providers.
        """
        return list(cls._providers.keys())
