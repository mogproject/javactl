from __future__ import division, print_function, absolute_import, unicode_literals

import sys
from datetime import datetime
from javactl.setting.setting import Setting
from javactl.logger import SystemLogger
from javactl.executor.executor import Executor
from javactl.exceptions import DuplicateError


def main():
    """
    Main function
    """

    return_code = 0
    try:
        setting = Setting().parse_args(sys.argv).load_config()
        now = datetime.now()
        ex = Executor(setting, SystemLogger(setting.dry_run))
        result = ex.check_requirement().create_directories().clean_old_logs(now).execute(now)
        if result.failed:
            return_code = 1
    except DuplicateError:
        return 0
    except Exception as e:
        print('%s: %s' % (e.__class__.__name__, e))
        import traceback
        print(traceback.print_exc())
        return 2
    return return_code
