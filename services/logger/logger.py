import os
import time
from abc import ABC, abstractmethod


class Logger(ABC):
    """Abstract base class for all loggers."""

    LOG_DIR = os.path.expanduser("~/waid_logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    @staticmethod
    def get_log_filename() -> str:
        """Returns the log filename for the current date."""
        return f"{time.strftime('%Y-%m-%d')}.log"

    @staticmethod
    def get_log_filepath() -> str:
        """Returns the full path of the current log file."""
        return os.path.join(Logger.LOG_DIR, Logger.get_log_filename())

    @staticmethod
    def log(message: str) -> None:
        """Write logs to a dated file inside the waid_logs folder."""
        log_file_path = Logger.get_log_filepath()

        with open(log_file_path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

    @abstractmethod
    def start(self) -> None:
        """Start logging activity."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop logging activity."""
        pass
