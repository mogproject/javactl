from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import os
import re
import time
import getpass
import glob
from datetime import datetime, timedelta
from mog_commons.command import execute_command, capture_command, execute_command_with_pid, pid_exists
from mog_commons.case_class import CaseClass
from mog_commons.functional import omap, oget
from mog_commons.types import *
from mog_commons.string import to_unicode
from javactl.logger.logger import Logger
from javactl.logger.console_logger import get_console_logger
from javactl.setting.setting import Setting
from javactl.exceptions import DuplicateError


class Executor(CaseClass):
    @types(setting=Setting, logger=Logger, failed=bool)
    def __init__(self, setting, logger, failed=False):
        CaseClass.__init__(self, ('setting', setting), ('logger', logger), ('failed', failed))

    def check_requirement(self):
        return self._check_user()._check_java_version()._check_duplicate()

    def _check_user(self):
        actual = getpass.getuser()
        expect = self.setting.os_setting.user
        assert actual == expect, "This application must be run as '%s', but you are '%s'." % (expect, actual)
        return self

    def _check_java_version(self):
        ret, stdout, stderr = capture_command([self.setting.java_setting.get_executable(), '-version'])
        assert ret == 0, 'Failed to get java version: ret=%d, stderr=%s' % (ret, stderr)

        first_line = ''.join(to_unicode(stderr).splitlines()[:1])
        m = re.compile(r"""java version \"(\d+[.]\d+)[.]\d+_\d+\"""").match(first_line)
        if m:
            actual = float(m.group(1))
        else:
            raise AssertionError('Unexpected java version: %s' % first_line)

        expect = self.setting.java_setting.version
        assert actual == expect, "Unexpected Java version: expect='%s', actual='%s'." % (expect, actual)
        return self

    def _check_duplicate(self):
        p = self.setting.app_setting.pid_file
        if p is not None:
            if os.path.exists(self.setting.app_setting.pid_file):
                with open(p) as f:
                    pid = int(f.read())
                if pid_exists(pid):
                    self.logger.info('%s is already running. Skipped: config=%s' % (
                        self.setting.app_setting.name, self.setting.config_path))
                    raise DuplicateError
        return self

    def create_directories(self):
        dirs = [d for d in [
            omap(os.path.dirname, self.setting.log_setting.console.prefix),
            omap(os.path.dirname, self.setting.log_setting.gc.prefix),
            self.setting.log_setting.dump.prefix,
            omap(os.path.dirname, self.setting.log_setting.error.path),
        ] if d is not None]

        for d in dirs:
            if not os.path.exists(d):
                self._create_directory(d)
        return self

    # OS operations
    def _create_directory(self, path):
        if self.setting.dry_run:
            print('Would create directory: %s' % path)
        else:
            print('Creating directory: %s' % path)
            os.makedirs(path)

    def _delete_file(self, path):
        if self.setting.dry_run:
            print('Would delete file: %s' % path)
        else:
            print('Deleting file: %s' % path)
            os.remove(path)

    def clean_old_logs(self, now):
        for setting in [self.setting.log_setting.console, self.setting.log_setting.gc]:
            if setting.prefix is None or setting.preserve is None:
                continue
            for path in glob.iglob(setting.prefix + '*'):
                mtime = datetime.fromtimestamp(os.path.getmtime(path))
                if mtime < now - timedelta(days=setting.preserve):
                    self._delete_file(path)
        return self

    def execute(self, now):
        return self._execute_commands(self.setting.pre_commands, now)._execute_application(now)._execute_commands(
            self.setting.post_commands, now)

    def _execute_application(self, now):
        if self.failed:
            return self

        failed = False
        self.logger.info(
            '%s started: config=%s, args=%s' % (
                self.setting.app_setting.name, self.setting.config_path, self.setting.extra_args))

        time_start = time.time()
        if self.setting.dry_run:
            print('Would execute: cwd=%s, cmd=[\n%s\n], env={\n%s\n}, output=%s' % (
                self.setting.app_setting.home,
                '\n'.join('  %s' % s for s in self.setting.get_args(now)),
                '\n'.join('  %s: %s' % kv for kv in self.setting.get_environ(now).items()),
                oget(self.setting.log_setting.console.get_path(now), 'stdout')
            ))
            ret = 0
        else:
            out_path = self.setting.log_setting.console.get_path(now)
            if out_path is None:
                stdout = sys.stdout
                stderr = sys.stderr
            else:
                stdout = get_console_logger(
                    out_path,
                    self.setting.log_setting.console.max_size.bytes(),
                    self.setting.log_setting.console.backup)
                stderr = stdout
            ret = execute_command_with_pid(
                self.setting.get_args(now),
                self.setting.app_setting.pid_file,
                shell=False,
                cwd=self.setting.app_setting.home,
                env=dict(os.environ, **(oget(self.setting.get_environ(now), {}))),
                stdin=sys.stdin, stdout=stdout, stderr=stderr)

        elapsed = time.time() - time_start

        if ret == 0:
            self.logger.info('%s ended successfully: elapsed=%ds' % (self.setting.app_setting.name, elapsed))
        else:
            self.logger.error(
                '%s ended with error: return_code=%d, elapsed=%ds' % (self.setting.app_setting.name, ret, elapsed))
            failed = True
        return self.copy(failed=failed)

    def _execute_commands(self, commands, now):
        failed = self.failed
        for cmd in commands:
            if self.setting.dry_run:
                print('Would execute: %s' % cmd)
            else:
                ret = execute_command(cmd, shell=True, cwd=self.setting.app_setting.home,
                                      env=self.setting.get_environ(now))
                if ret != 0:
                    self.logger.error('Failed to execute: app=%s, cmd=%s, return_code=%d' % (
                        self.setting.app_setting.name, cmd, ret))
                    failed = True
        return self.copy(failed=failed)
