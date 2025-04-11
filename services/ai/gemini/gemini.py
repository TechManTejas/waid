import google.generativeai as genai
from enum import Enum
from services.ai.ai_provider import AIProvider
from services.secret.secret_manager import SecretManager

class GeminiSecret(Enum):
    API_KEY = "gemini_api_key"
    MODEL = "gemini_model"

class GeminiAI(AIProvider):
    _model = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """
        Ensure GeminiAI is initialized upon first instantiation.
        """
        if not cls._initialized:
            cls._configure_gemini()
        return super().__new__(cls)

    @classmethod
    def _configure_gemini(cls):
        """
        Configure Gemini AI with stored API key and model name.
        """
        api_key = SecretManager.get_secret(GeminiSecret.API_KEY.value)
        model_name = SecretManager.get_secret(GeminiSecret.MODEL.value)

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
        for key in GeminiSecret:
            if key.value in config_obj:
                SecretManager.set_secret(key.value, config_obj[key.value])
        cls._configure_gemini()

    @classmethod
    def get_configuration(cls) -> dict:
        """
        Retrieve stored Gemini AI configuration securely.
        """
        return {key.value: SecretManager.get_secret(key.value) for key in GeminiSecret}

    @classmethod
    def get_required_configuration(cls) -> list:
        """
        Return a list of required configurations to configure this AI provider.
        """
        return [key.value for key in GeminiSecret]

    @classmethod
    def generate_text(cls, prompt: str) -> str:
        """
        Generate text using the configured Gemini AI model.
        """
        if not cls._model:
            return "[Error: Model not configured]"
        response = cls._model.generate_content(prompt)
        return response.text if response and hasattr(response, 'text') else "[Error: No response from GeminiAI]"
