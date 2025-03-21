from abc import ABC, abstractmethod

class AIProvider(ABC):
    @classmethod
    @abstractmethod
    def set_configuration(cls, config_obj: dict):
        """
        Set and apply configuration parameters.
        Must be implemented by subclasses.
        """
        pass

    @classmethod
    @abstractmethod
    def get_configuration(cls) -> dict:
        """
        Get current configuration settings.
        Must be implemented by subclasses.
        """
        pass

    @classmethod
    @abstractmethod
    def generate_text(cls, prompt: str) -> str:
        """
        Generate text using the configured AI model.
        Must be implemented by subclasses.
        """
        pass
