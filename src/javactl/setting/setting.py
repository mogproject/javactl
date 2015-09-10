from __future__ import division, print_function, absolute_import, unicode_literals

import yaml
from javactl.setting import arg_parser
from javactl.util.case_class import CaseClass


class Setting(CaseClass):
    """Manages all settings."""

    def __init__(self, config_path=None, config_data=None, dry_run=False):
        CaseClass.__init__(
            self,
            ('config_path', config_path),
            ('config_data', {} if config_data is None else config_data),
            ('dry_run', dry_run)
        )

    def copy(self, **args):
        return Setting(
            config_path=args.get('config_path', self.config_path),
            config_data=args.get('config_data', self.config_data),
            dry_run=args.get('dry_run', self.dry_run),
        )

    def parse_args(self, argv):
        option, args = arg_parser.parser.parse_args(argv[1:])

        if not len(args) == 1:
            arg_parser.parser.print_help()
            arg_parser.parser.exit(2)

        return self.copy(config_path=args[0], dry_run=option.dry_run)

    def load_config(self):
        if not self.config_path:
            return self

        with open(self.config_path, 'rb') as f:
            data = yaml.load(f.read().decode('utf-8'))

        return self.copy(config_data=data)
