import signal
from services.signal.shutdown.shutdown_handler import ShutdownHandler

class SignalHandler:
    """Handles system signals."""

    @staticmethod
    def register_signals() -> None:
        """Register signals for handling system termination requests."""
        signal.signal(signal.SIGTERM, ShutdownHandler.handle_shutdown)
