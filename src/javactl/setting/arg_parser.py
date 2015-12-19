from __future__ import division, print_function, absolute_import, unicode_literals

from optparse import OptionParser

VERSION = 'javactl %s' % __import__('javactl').__version__

USAGE = """%prog [options...] <config_path> [args...]"""


def _get_parser():
    p = OptionParser(usage=USAGE, version=VERSION)
    p.allow_interspersed_args = False

    p.add_option(
        '--check', action='store_true', dest='dry_run', default=False, help='dry-run mode'
    )

    p.add_option(
        '--debug', action='store_true', dest='debug', default=False, help='debug mode'
    )

    return p


parser = _get_parser()
