import logging
from pathlib import Path


class LogManager:
    def __init__(self, log_file_path: Path = Path(Path.cwd(), "sheetload_logs")):
        Path(log_file_path).mkdir(parents=True, exist_ok=True)
        log_filename = Path(log_file_path, "sheetload_log.log")
        logger = logging.getLogger("Sheetload Logger")
        logger.setLevel(logging.INFO)
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(log_filename)
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        c_format = logging.Formatter("%(name)s - %(levelname)s - %(funcName)s - %(message)s")
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
        )
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        self.logger = logger

    def set_debug(self):
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            handler.setLevel(logging.DEBUG)


log_manager = LogManager()

GLOBAL_LOGGER = log_manager.logger
