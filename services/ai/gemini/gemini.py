import google.generativeai as genai
from services.ai.ai_provider import AIProvider
from services.secret.secret_manager import SecretManager


class GeminiAI(AIProvider):
    _model = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Class constructor to ensure initialization at class level.
        """
        if not cls._initialized:
            cls._configure_gemini()
        return super().__new__(cls)

    @classmethod
    def _configure_gemini(cls):
        """
        Configure Gemini AI with API key and model name stored in SecretManager.
        """
        api_key = SecretManager.get_secret("api_key")
        model_name = SecretManager.get_secret("model")

        if api_key:
            genai.configure(api_key=api_key)
        if model_name:
            cls._model = genai.GenerativeModel(model_name)

        cls._initialized = True 

    @classmethod
    def set_configuration(cls, config_obj: dict):
        """
        Securely store the configuration parameters for GeminiAI.
        """
        for key, value in config_obj.items():
            SecretManager.set_secret(key, value)
        cls._configure_gemini()

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Retrieve stored Gemini AI configuration securely.
        """
        return {
            key: SecretManager.get_secret(key)
            for key in cls.get_required_configurations()
        }

    @classmethod
    def get_required_configuration(cls) -> list:
        """
        Return a list of required configuration to configure this AI provider.
        """
        return ["api_key", "model"]

    @classmethod
    def generate_text(cls, prompt: str) -> str:
        """
        Generate text using the configured Gemini AI model.
        """
        if not cls._model:
            return "[Error: Model not configured]"
        response = cls._model.generate_content(prompt)
        return response.text if response and hasattr(response, 'text') else "[Error: No response from GeminiAI]"
