from services.cleanup.cleanup import Cleanup
from services.notification.notification import Notification
from services.signal.signal_handler import SignalHandler

class StartupManager:
    """Manages all startup tasks, including signal registration."""

    @classmethod
    def run(cls) -> None:
        """Execute all startup tasks."""
        SignalHandler.register_signals()
        Cleanup.cleanup_logs(days=49) 
        Notification.send("WAID Service has started successfully.")
