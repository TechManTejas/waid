import os
import time

class LogManager:
    """Manages multiple loggers and provides a centralized logging mechanism."""

    LOG_DIR = os.path.expanduser("~/waid_logs")
    os.makedirs(LOG_DIR, exist_ok=True) 

    loggers = []
    running = False

    @staticmethod
    def log(message: str) -> None:
        """Write logs to a dated file inside the waid_logs folder."""
        log_filename = f"{time.strftime('%Y-%m-%d')}.log"
        log_file_path = os.path.join(LogManager.LOG_DIR, log_filename)

        with open(log_file_path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    @classmethod
    def initialize(cls) -> None:
        """Initialize loggers if not already initialized."""
        if not cls.loggers:
            from services.logger.window.window_logger import WindowLogger 
            cls.loggers = [WindowLogger()]

    @classmethod
    def start(cls) -> None:
        """Start all loggers."""
        if not cls.running:
            cls.running = True
            cls.initialize()
            for logger in cls.loggers:
                logger.start()

    @classmethod
    def stop(cls) -> None:
        """Stop all loggers gracefully."""
        if cls.running:
            cls.running = False
            for logger in cls.loggers:
                logger.stop()
