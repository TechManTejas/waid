import os
from services.logger.window.window_logger import WindowLogger  
from services.logger.logger import Logger


class LogManager:
    """Manages multiple loggers and provides a centralized logging mechanism."""

    _available_loggers = {
        "window_logger": WindowLogger(),
        # Add more loggers here, e.g., "keyboard_logger": KeyboardLogger()
    }
    
    active_loggers = set(_available_loggers.keys())

    @classmethod
    def get_loggers(cls) -> dict:
        """
        Get all available loggers and their active status.
        :return: Dictionary of logger names with their active state.
        """
        return {name: name in cls.active_loggers for name in cls._available_loggers}

    @classmethod
    def set_active_loggers(cls, logger_names: list) -> None:
        """
        Set which loggers should be active and restart logging.
        :param logger_names: List of logger names to activate.
        """
        cls.active_loggers = set(logger_names)
        cls.restart()

    @classmethod
    def get_active_loggers(cls) -> list:
        """
        Get the currently active loggers.
        :return: List of active logger names.
        """
        return list(cls.active_loggers)

    @classmethod
    def start(cls) -> None:
        """Start only the loggers selected by the user (all by default)."""
        for logger_name in cls.active_loggers:
            logger = cls._available_loggers.get(logger_name)
            if logger:
                logger.start()

    @classmethod
    def stop(cls) -> None:
        """Stop only the loggers that were started."""
        for logger_name in cls.active_loggers:
            logger = cls._available_loggers.get(logger_name)
            if logger:
                logger.stop()

    @classmethod
    def restart(cls) -> None:
        """Restart all active loggers (stop and start again)."""
        cls.stop()
        cls.start()

    @classmethod
    def get_all_logs(cls) -> list:
        """
        Fetch all logs from the latest log file.
        :return: List of log messages.
        """
        log_file_path = Logger.get_log_filepath()

        if not os.path.exists(log_file_path):
            return []

        with open(log_file_path, "r") as f:
            return f.readlines()
