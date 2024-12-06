import logging
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional


class CustomLogger(logging.Logger):
    """
    A custom logger class that extends the standard logging.Logger with additional features.
    """

    # Class-level formatter to ensure consistency across all logger instances
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] "%(name)s" (%(filename)s:%(lineno)d) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    def __init__(self, name: str, log_filename: str = "./Logs/default.log", level: int = logging.INFO):
        """
        Initialize a CustomLogger instance.

        Args:
            name (str): The name of the logger.
            log_filename (str): The file path for logging output.
            level (int): The logging level.
        """
        super().__init__(name, level)
        self.log_filename = log_filename
        self._initialize_logger()

    def _initialize_logger(self) -> None:
        """
        Initialize the logger by setting up file and console handlers.
        """
        # Prevent adding duplicate handlers
        if not self.handlers:
            try:
                log_path = Path(self.log_filename)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                # Ensure the log file has a .log extension
                if not log_path.suffix == '.log':
                    log_path = log_path.with_suffix('.log')
                    self.log_filename = str(log_path)

                # File handler
                handler_file = logging.FileHandler(self.log_filename, mode='a')
                handler_file.setFormatter(self.formatter)
                self.addHandler(handler_file)

                # Console handler
                handler_console = logging.StreamHandler()
                handler_console.setFormatter(self.formatter)
                self.addHandler(handler_console)
            except OSError as e:
                self.error(f"Failed to initialize logger: {e}")
                raise

    def setLevel(self, level: Any) -> None:
        """
        Set the logging level.

        Args:
            level (Any): The logging level as an integer or string.

        Raises:
            ValueError: If the provided level is invalid.
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), None)
            if level is None or not isinstance(level, int):
                raise ValueError(f"Invalid log level: {level}")
        super().setLevel(level)

    def show_progress(self, progress: float, bar_length: int = 50) -> None:
        """
        Display a progress bar in the logs.

        Args:
            progress (float): Progress percentage between 0 and 100.
            bar_length (int): The length of the progress bar.
        """
        progress = int(progress)
        filled_length = int(round(bar_length * progress / 100))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        self.info(f"Processing: [{bar}] {progress}%")

    def log_function_call(self, func: Callable) -> Callable:
        """
        Decorator to log function calls and execution time.

        Args:
            func (Callable): The function to be decorated.

        Returns:
            Callable: The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.info(f"Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}")
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.info(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds")
            return result
        return wrapper

if __name__ == "__main__":
    logger = CustomLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    logger.show_progress(50)
    @logger.log_function_call
    def test_function():
        time.sleep(1)
    test_function()
    config = {
        'log_folder': './Logs',
        'level': 'DEBUG',
        'loggers': ['app', 'database', 'security'],
        'logger_levels': {
            'database': 'ERROR',
            'security': 'WARNING'
        }
    }
