from __future__ import division, print_function, absolute_import, unicode_literals

from optparse import OptionParser
from javactl.util import oget

VERSION = 'javactl %s' % __import__('javactl').__version__

USAGE = """%prog [options...] <config_path> [args...]"""


class Parser(OptionParser):
    def parse_args(self, args=None, values=None):
        """
        Parse manually since args can contain arguments for Java application.
        :param args: [string]
        :return: (option : dict, config_path : string, args : [string])
        """

        # find the first non-optional arg
        args = oget(args, [])

        i = 0
        for i in range(len(args)):
            if not args[i].startswith('-'):
                break
        ls, rs = args[:i + 1], args[i + 1:]

        option, largs = OptionParser.parse_args(self, oget(ls, []))
        rargs = largs + rs

        if not rargs:
            self.print_help()
            self.exit(2)
            return

        return option, rargs[0], rargs[1:]


def _get_parser():
    p = Parser(usage=USAGE, version=VERSION)

    p.add_option(
        '--check', action='store_true', dest='dry_run', default=False, help='dry run mode'
    )

    return p


parser = _get_parser()
