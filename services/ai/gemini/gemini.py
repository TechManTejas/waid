import google.generativeai as genai
from services.ai.ai_provider import AIProvider


class GeminiAI(AIProvider):
    _model = None
    _configurations = {}

    @classmethod
    def _configure_gemini(cls):
        """
        Configure Gemini AI with API key and model name.
        """
        api_key = cls._configurations.get("api_key")
        model_name = cls._configurations.get("model")

        if api_key:
            genai.configure(api_key=api_key)
        if model_name:
            cls._model = genai.GenerativeModel(model_name)

    @classmethod
    def set_configuration(cls, config_obj: dict):
        """
        Set and apply configuration parameters for GeminiAI.
        """
        cls._configurations.update(config_obj)
        cls._configure_gemini()

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Get current configuration settings for GeminiAI.
        """
        return cls._configurations

    @classmethod
    def generate_text(cls, prompt: str) -> str:
        """
        Generate text using the configured Gemini AI model.
        """
        if not cls._model:
            return "[Error: Model not configured]"
        response = cls._model.generate_content(prompt)
        return response.text if response and hasattr(response, 'text') else "[Error: No response from GeminiAI]"
