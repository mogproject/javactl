from __future__ import division, print_function, absolute_import, unicode_literals

import logging
import sys
if sys.version_info < (2, 7):
    # use backported logging module in Python 2.6
    from backported.logging.handlers.handlers import RotatingFileHandler
else:
    from logging.handlers import RotatingFileHandler
from javactl.logger.logger_wrapper import LoggerWrapper
from mog_commons.string import to_str


def get_console_logger(path, max_bytes, backup_count, encoding='utf-8'):
    """

    Note: RotatingFileHandler in Python 2.6 sometimes cause a weird issue. see https://bugs.python.org/issue4749

    :param path:
    :param max_bytes:
    :param backup_count:
    :param encoding:
    :return:
    """
    logger = logging.getLogger('ConsoleLogger')
    logger.setLevel(logging.INFO)

    # add a handler
    handler = RotatingFileHandler(path, 'a', max_bytes, backup_count)
    handler.setFormatter(logging.Formatter(to_str('[%(asctime)s] %(message)s', encoding, 'ignore')))
    logger.addHandler(handler)

    return LoggerWrapper(logger, logging.INFO)
