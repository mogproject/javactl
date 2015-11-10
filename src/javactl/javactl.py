from __future__ import division, print_function, absolute_import, unicode_literals

import sys
from datetime import datetime
from javactl.setting.setting import Setting
from javactl.logger import SystemLogger
from javactl.executor.executor import Executor
from javactl.exceptions import DuplicateError


def main(args=sys.argv):
    """
    Main function
    """

    return_code = 0
    base_setting = Setting().parse_args(args)
    try:
        setting = base_setting.load_config()
        now = datetime.now()
        ex = Executor(setting, SystemLogger(setting.dry_run))
        result = ex.check_requirement().create_directories().clean_old_logs(now).execute(now)
        if result.failed:
            return_code = 1
    except DuplicateError:
        return 0
    except Exception as e:
        print('%s: %s' % (e.__class__.__name__, e))
        if base_setting.debug:
            import traceback
            traceback.print_exc()
        return 2
    return return_code
