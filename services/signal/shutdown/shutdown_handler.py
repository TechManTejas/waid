class ShutdownHandler:
    """Manages cleanup operations before shutting down the application."""

    @staticmethod
    def handle_shutdown(signum, frame) -> None:
        """Perform necessary cleanup actions before shutting down."""
        pass