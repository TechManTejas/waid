import threading
import time
import os

LOG_FILE = os.path.expanduser("~/waid.log") 

class LogManager:
    """Manages multiple loggers and provides a centralized logging mechanism."""

    loggers = []
    running = False

    @staticmethod
    def log(message: str) -> None:
        """Write logs to a central file."""
        with open(LOG_FILE, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    def __init__(self) -> None:
        from services.logger.window.window_logger import WindowLogger 
        self.loggers = [WindowLogger()]
    
    def start(self) -> None:
        """Start all loggers in separate threads."""
        if not self.running:
            self.running = True
            for logger in self.loggers:
                threading.Thread(target=logger.start, daemon=True).start()

    def stop(self) -> None:
        """Stop all loggers gracefully."""
        if self.running:
            self.running = False
            for logger in self.loggers:
                logger.stop()
