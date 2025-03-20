from abc import ABC, abstractmethod

class Logger(ABC):
    """Abstract base class for all loggers."""

    @abstractmethod
    def start(self) -> None:
        """Start logging activity."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop logging activity."""
        pass
