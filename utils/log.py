# coding: utf-8
import os
import logging
from logging.handlers import RotatingFileHandler
import utils.settings


class _LoggingFilter(logging.Filter):
    """日志过滤器"""

    def __init__(self, name="", level=logging.DEBUG):
        super(_LoggingFilter, self).__init__(name)
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter(fmt="%(asctime)s, %(levelname)s, %(filename)s[line: %(lineno)d], %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

    for level, name in logging._levelToName.items():
        if level in (logging.NOTSET, logging.CRITICAL):
            continue

        log_dir = _create_log_dir(utils.settings.PROJECT_DIR, "logs", name.lower())
        log_handler = RotatingFileHandler(os.path.join(log_dir, "{}.log".format(name.lower())), maxBytes=1024 * 1000 * 10, backupCount=10, encoding="utf-8")
        log_handler.setLevel(level)
        log_handler.setFormatter(log_formatter)
        log_handler.addFilter(_LoggingFilter(level=level))
        logger.addHandler(log_handler)

    return logger


def _create_log_dir(path, *args):
    log_dir = os.path.join(path, *args)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    return log_dir
