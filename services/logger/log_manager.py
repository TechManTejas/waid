import threading
import time
import os

LOG_DIR = os.path.expanduser("~/waid_logs")
os.makedirs(LOG_DIR, exist_ok=True)

class LogManager:
    """Manages multiple loggers and provides a centralized logging mechanism."""

    loggers = []
    running = False

    @staticmethod
    def log(message: str) -> None:
        """Write logs to a dated file inside the waid_logs folder."""
        log_filename = f"{time.strftime('%Y-%m-%d')}.log"
        log_file_path = os.path.join(LOG_DIR, log_filename)

        with open(log_file_path, "a") as f:
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
