from services.cleanup.cleanup import Cleanup
from services.notification.notification import Notification
from services.signal.signal_handler import SignalHandler
from services.logger.log_manager import LogManager
from ui.system_tray import SystemTray

def main() -> None:
    """Entry point for the application."""
    # Register signals and clean old logs
    SignalHandler.register_signals()
    Cleanup.cleanup_logs(days=7)

    # Start logging
    LogManager.start()

    # Send startup notification
    Notification.send("I am tracking you ;)")

    # Start system tray
    SystemTray.start()

if __name__ == "__main__":
    main()
