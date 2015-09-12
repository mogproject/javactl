from __future__ import division, print_function, absolute_import, unicode_literals

from javactl.logger.logger import Logger


class MockLogger(Logger):
    def __init__(self):
        Logger.__init__(self, 'MockLogger')
        self.buffer = []

    def _log(self, priority, message):
        self.buffer.append((priority, message))
