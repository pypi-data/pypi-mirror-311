import os
import logging
import time
from functools import wraps

class CustomLogger(logging.Logger):
    # Logging levels encapsulated
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    def __init__(self, name, log_filename="./Logs/simple_log_helper.log", level=logging.INFO):
        super().__init__(name, level)
        self.log_filename = log_filename
        self.__initialize_logger__()

    def __initialize_logger__(self):
        folder = os.path.dirname(self.log_filename)
        if not os.path.exists(folder):
            os.makedirs(folder)
        if not self.log_filename.endswith('.log'):
            self.log_filename = os.path.join(folder, 'default.log')
        
        handler_file = logging.FileHandler(self.log_filename)
        handler_console = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] "%(name)s" (%(filename)s:%(lineno)d) %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler_file.setFormatter(formatter)
        handler_console.setFormatter(formatter)
        self.addHandler(handler_file)
        self.addHandler(handler_console)

    def setLevel(self, level: str) -> None:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), None)
        if not isinstance(level, int):
            raise ValueError(f"Invalid log level: {level}")
        super().setLevel(level)

    def show_progress(self, progress, bar_length=50):
        filled_length = int(round(bar_length * progress / 100))
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        self.info(f"Processing: [{bar}] {progress}%")

    def log_function_call(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.info(f"Called function: {func.__name__} with args: {args} and kwargs: {kwargs}")
            self.info(f"Execution time: {end_time - start_time:.4f} seconds")
            return result
        return wrapper

class LoggerManager:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.loggers = {}

    def get_logger(self, name: str) -> CustomLogger:
        if name not in self.loggers:
            logger = CustomLogger(name, level=self.config.get('level', logging.INFO))
            self.loggers[name] = logger
        return self.loggers[name]

    def set_log_level(self, level: str) -> None:
        for logger in self.loggers.values():
            logger.setLevel(level)

    def configure(self, config: dict) -> None:
        self.config = config
        for logger in self.loggers.values():
            logger.setLevel(config.get('level', logging.INFO))
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
