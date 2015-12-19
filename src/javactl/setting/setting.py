from __future__ import division, print_function, absolute_import, unicode_literals

import subprocess
from itertools import chain
import yaml
import six
from mog_commons.case_class import CaseClass
from mog_commons.functional import oget
from javactl.setting import arg_parser
from javactl.setting.app_setting import AppSetting
from javactl.setting.java_setting import JavaSetting
from javactl.setting.log_setting import LogSetting
from javactl.setting.os_setting import OSSetting


class Setting(CaseClass):
    """Manages all settings."""

    def __init__(self,
                 config_path=None,
                 extra_args=None,
                 dry_run=False,
                 debug=False,
                 app_setting=None,
                 java_setting=None,
                 log_setting=None,
                 os_setting=None,
                 pre_commands=None,
                 post_commands=None):
        """
        :param config_path:
        :param extra_args: arguments for Java application
        :param dry_run:
        :param debug: debug mode if true
        :param app_setting:
        :param java_setting:
        :param log_setting:
        :param os_setting:
        :param pre_commands:
        :param post_commands:
        :return:
        """
        CaseClass.__init__(
            self,
            ('config_path', config_path),
            ('extra_args', oget(extra_args, [])),
            ('dry_run', dry_run),
            ('debug', debug),
            ('app_setting', app_setting),
            ('java_setting', java_setting),
            ('log_setting', log_setting),
            ('os_setting', os_setting),
            ('pre_commands', oget(pre_commands, [])),
            ('post_commands', oget(post_commands, []))
        )

    def parse_args(self, argv):
        option, args = arg_parser.parser.parse_args(argv[1:])
        if not args:
            arg_parser.parser.print_help()
            arg_parser.parser.exit(2)

        return self.copy(config_path=args[0], extra_args=args[1:], dry_run=option.dry_run, debug=option.debug)

    def load_config(self):
        if not self.config_path:
            return self

        with open(self.config_path, 'rb') as f:
            data = yaml.load(f.read().decode('utf-8'))

        app_setting = AppSetting(**data.get('app', {}))
        java_setting = JavaSetting(**data.get('java', {}))
        log_setting = LogSetting(app_setting.home, **data.get('log', {}))
        os_setting = OSSetting(**data.get('os', {}))

        pre_commands = data.get('pre', [])
        post_commands = data.get('post', [])

        for commands in [pre_commands, post_commands]:
            assert isinstance(commands, list), 'pre/post must be lists or empty'
            assert all(isinstance(s, six.string_types) for s in commands), 'each element of pre/post must be a string'

        return self.copy(app_setting=app_setting, java_setting=java_setting, log_setting=log_setting,
                         os_setting=os_setting, pre_commands=pre_commands, post_commands=post_commands)

    def get_args(self, now):
        return list(chain.from_iterable([
            self.app_setting.get_args(self.java_setting.get_args() + self.log_setting.get_opts(now)),
            self.extra_args,
        ]))

    def get_environ(self, now):
        d = {
            'JAVA_HOME': self.java_setting.home,
            'JAVA_OPTS': subprocess.list2cmdline(self.java_setting.get_opts() + self.log_setting.get_opts(now))
        }
        d.update(self.os_setting.env)
        return d
