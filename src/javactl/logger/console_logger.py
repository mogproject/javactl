from __future__ import division, print_function, absolute_import, unicode_literals

import logging
from logging.handlers import RotatingFileHandler
from javactl.logger.logger_wrapper import LoggerWrapper
from javactl.util import util


def get_console_logger(path, max_bytes, backup_count, encoding='utf-8'):
    logger = logging.getLogger('ConsoleLogger')
    logger.setLevel(logging.INFO)

    # add a handler
    handler = RotatingFileHandler(path, 'a', max_bytes, backup_count)
    handler.setFormatter(logging.Formatter(util.to_str('[%(asctime)s] %(message)s', encoding, 'ignore')))
    logger.addHandler(handler)

    return LoggerWrapper(logger, logging.INFO)
