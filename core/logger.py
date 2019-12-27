import logging

from data_tools.logging import LoggerFactory


class LogManager:
    def __init__(self, logger: LoggerFactory):
        self.logger = logger.get_logger(level=getattr(logging, "info".upper()))

    def set_debug(self):
        self.logger = self.logger.setLevel(logging.DEBUG)


log_manager = LogManager(LoggerFactory)

GLOBAL_LOGGER = log_manager.logger
