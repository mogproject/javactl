from __future__ import division, print_function, absolute_import, unicode_literals

import logging
from logging.handlers import RotatingFileHandler
from javactl.logger.logger_wrapper import LoggerWrapper


def get_console_logger(path, max_bytes, backup_count):
    logger = logging.getLogger('ConsoleLogger')
    logger.setLevel(logging.INFO)

    # add a handler
    handler = RotatingFileHandler(path, 'a', max_bytes, backup_count)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(handler)

    return LoggerWrapper(logger, logging.INFO)
