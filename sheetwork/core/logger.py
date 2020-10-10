import logging
from pathlib import Path


class LogManager:
    def __init__(
        self,
        log_file_path: Path = Path(Path.cwd(), "sheetwork_logs"),
        log_to_console: bool = True,
    ):
        Path(log_file_path).mkdir(parents=True, exist_ok=True)
        log_filename = Path(log_file_path, "sheetwork_log.log")
        logger = logging.getLogger("Sheetwork Logger")
        logger.setLevel(logging.INFO)
        # Create handlers
        f_handler = logging.FileHandler(log_filename)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        f_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
        )
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(f_handler)

        # if we want to print the log to console we're going to add a streamhandler
        if log_to_console:
            c_handler = logging.StreamHandler()
            c_handler.setLevel(logging.INFO)
            c_format = logging.Formatter("%(message)s")
            c_handler.setFormatter(c_format)
            logger.addHandler(c_handler)

        self.logger = logger

    def set_debug(self):
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            handler.setLevel(logging.DEBUG)


log_manager = LogManager()

GLOBAL_LOGGER = log_manager.logger
