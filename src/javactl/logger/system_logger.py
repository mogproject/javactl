from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
try:
    import syslog
    SYSLOG_AVAILABLE = True
except ImportError:
    SYSLOG_AVAILABLE = False
from javactl.logger.logger import Logger
from mog_commons.string import to_str


class SystemLogger(Logger):
    def __init__(self, dry_run=False):
        self.name = os.path.basename(sys.argv[0])
        self.dry_run = dry_run
        super(SystemLogger, self).__init__('SystemLogger[%s]' % self.name)

    def _log(self, priority, message):
        if SYSLOG_AVAILABLE:
            if self.dry_run:
                print('Would write to syslog: priority=%s, message=%s' % (priority, message))
            else:
                syslog.openlog(self.name, syslog.LOG_PID)
                syslog.syslog(priority, to_str(message, 'utf-8', 'ignore'))
                syslog.closelog()
