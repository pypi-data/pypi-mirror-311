import logging
import threading
from typing import Dict, Optional

from custom_logger import CustomLogger


class LoggerManager:
    """
    Manages multiple loggers with individual configurations.
    """

    def __init__(self, config: Optional[dict] = None):
        """
        Initialize the LoggerManager with optional configuration.

        Args:
            config (dict, optional): Configuration dictionary for the logger manager.
        """
        self._lock = threading.Lock()
        self.config = config or {}
        self.logger_folder = self.config.get('log_folder', './Logs')
        self.global_log_level = self.config.get('level', 'INFO').upper()
        self.loggers: Dict[str, CustomLogger] = {}

        # Set the custom logger class for the logging module
        logging.setLoggerClass(CustomLogger)

        if config:
            self.configure(config)

    def get_logger(self, name: str) -> CustomLogger:
        """
        Retrieve a logger by name, creating it if it doesn't exist.

        Args:
            name (str): The name of the logger.

        Returns:
            CustomLogger: The logger instance.
        """
        with self._lock:
            if name not in self.loggers:
                logger = logging.getLogger(name)
                log_filename = f"{self.logger_folder}/{name}.log"
                logger.log_filename = log_filename
                logger_specific_level = self.config.get('logger_levels', {}).get(name, self.global_log_level).upper()
                effective_level = self._get_effective_level(logger_specific_level)
                logger.setLevel(effective_level)
                logger._initialize_logger()
                self.loggers[name] = logger
            return self.loggers[name]

    def set_log_level(self, level: str) -> None:
        """
        Set the logging level for all managed loggers.

        Args:
            level (str): The logging level to set.
        """
        log_level = level.upper()
        for logger in self.loggers.values():
            logger.setLevel(log_level)

    def configure(self, config: dict) -> None:
        """
        Configure the LoggerManager with a configuration dictionary.

        Args:
            config (dict): The configuration dictionary.
        """
        self.config = config
        self.logger_folder = self.config.get('log_folder', './Logs')
        self.global_log_level = self.config.get('level', 'INFO').upper()
        for name in config.get('loggers', []):
            self.get_logger(name)
        for logger in self.loggers.values():
            logger_specific_level = self.config.get('logger_levels', {}).get(logger.name, self.global_log_level).upper()
            effective_level = self._get_effective_level(logger_specific_level)
            logger.setLevel(effective_level)

    def shutdown(self) -> None:
        """
        Cleanly shut down all managed loggers by closing their handlers.
        """
        for logger in self.loggers.values():
            handlers = logger.handlers[:]
            for handler in handlers:
                handler.close()
                logger.removeHandler(handler)

    def _get_effective_level(self, logger_specific_level: str) -> int:
        """
        Determine the effective logging level between global and logger-specific levels.

        Args:
            logger_specific_level (str): The logger-specific logging level.

        Returns:
            int: The effective logging level as an integer.
        """
        global_level = self._get_log_level(self.global_log_level)
        specific_level = self._get_log_level(logger_specific_level)
        # Use the least verbose (higher numeric value) level
        return max(global_level, specific_level)

    @staticmethod
    def _get_log_level(level_name: str) -> int:
        """
        Convert a logging level name to its corresponding numeric value.

        Args:
            level_name (str): The name of the logging level.

        Returns:
            int: The numeric value of the logging level.

        Raises:
            ValueError: If the logging level name is invalid.
        """
        level = getattr(logging, level_name.upper(), None)
        if level is None or not isinstance(level, int):
            raise ValueError(f"Invalid log level: {level_name}")
        return level

if __name__ == "__main__":
    # Example configuration
    config = {
        'log_folder': './Logs',
        'level': 'INFO',
        'loggers': ['app', 'db'],
        'logger_levels': {
            'db': 'WARNING',
        }
    }

    # Initialize the LoggerManager with the configuration
    logger_manager = LoggerManager(config)

    # Get loggers
    app_logger = logger_manager.get_logger('app')
    db_logger = logger_manager.get_logger('db')
    db_logger.info('This is an info message from db logger.')

    # Use the loggers
    app_logger.info('This is an info message from app logger.')
    db_logger.warning('This is a warning message from db logger.')

    # Use the custom methods
    @app_logger.log_function_call
    def sample_function(x, y):
        return x + y

    result = sample_function(5, 7)
    app_logger.show_progress(75)

    # Shutdown the loggers when done
    logger_manager.shutdown()
