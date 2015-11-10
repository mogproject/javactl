# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import sys
import os
import subprocess
import time
from mog_commons.string import to_str
from mog_commons.unittest import TestCase, base_unittest
from javactl.logger import console_logger


class TestConsoleLogger(TestCase):
    @staticmethod
    def _clear(path_list):
        for path in path_list:
            if os.path.exists(path):
                os.remove(path)

    @base_unittest.skipUnless(os.environ.get('CI', '').lower() == 'true', 'run only in CI')
    def test_get_logger(self):
        path = '/tmp/__test_console_logger_1.log'
        self._clear([path + suffix for suffix in ['', '.1', '.2', '.3']])

        out = console_logger.get_console_logger(path, 100, 2)

        for args in ['0' * 10, '1' * 20, '2' * 100, '3' * 10, '4' * 20, '5' * 100]:
            subprocess.call(
                args='echo %s' % args, shell=True, cwd='/tmp', stdin=sys.stdin, stdout=out, stderr=sys.stderr)

        time.sleep(1)

        self.assertFalse(os.path.exists(path + '.3'))
        with open(path) as f:
            self.assertEqual([l[26:] for l in f.readlines()], ['5' * 100 + '\n'])
        with open(path + '.1') as f:
            self.assertEqual([l[26:] for l in f.readlines()], ['3' * 10 + '\n', '4' * 20 + '\n'])
        with open(path + '.2') as f:
            self.assertEqual([l[26:] for l in f.readlines()], ['2' * 100 + '\n'])
        self._clear([path + suffix for suffix in ['', '.1', '.2', '.3']])

    @base_unittest.skipUnless(os.environ.get('CI', '').lower() == 'true', 'run only in CI')
    def test_get_logger_unicode(self):
        path = '/tmp/__test_console_logger_2.log'
        self._clear([path])

        out = console_logger.get_console_logger(path, 10000, 1)
        args = ['/bin/sh', '-c', to_str('echo "あいうえお"')]

        # Note: set shell=False to avoid a Python 3.2 bug
        subprocess.call(args=args, shell=False, cwd='/tmp', stdin=sys.stdin, stdout=out, stderr=sys.stderr)

        time.sleep(1)

        self.assertFalse(os.path.exists(path + '.1'))
        with open(path) as f:
            self.assertEqual([l[26:] for l in f.readlines()], [to_str('あいうえお\n')])
        self._clear([path])
