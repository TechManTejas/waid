import os
from datetime import datetime, timedelta
from services.logger.logger import Logger

class Cleanup:
    """Handles cleanup tasks like removing old log files."""

    @classmethod
    def cleanup_logs(cls, days: int = None) -> None:
        """
        Delete log files older than `days` days.
        If `days` is None, deletes all log files.
        """
        if not os.path.exists(Logger.LOG_DIR):
            return

        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
        
        for filename in os.listdir(Logger.LOG_DIR):
            file_path = os.path.join(Logger.LOG_DIR, filename)
            if os.path.isfile(file_path):
                if days is None or datetime.fromtimestamp(os.path.getmtime(file_path)) < cutoff_date:
                    os.remove(file_path)
