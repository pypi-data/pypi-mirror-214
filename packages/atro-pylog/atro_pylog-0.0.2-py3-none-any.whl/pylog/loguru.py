from loguru import logger as loguru_logger

from pylog.logger import Logger


class LoguruLogger(Logger):
    def __init__(self):
        self.logger = loguru_logger

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def shutdown(self):
        pass
