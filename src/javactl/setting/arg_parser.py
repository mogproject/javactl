from __future__ import division, print_function, absolute_import, unicode_literals

from optparse import OptionParser

VERSION = 'javactl %s' % __import__('javactl').__version__

USAGE = """%prog [options...] <config_path>"""


def __get_parser():
    p = OptionParser(version=VERSION, usage=USAGE)

    p.add_option(
        '--check', action='store_true', dest='width', default=False, help='dry run mode'
    )

    return p


parser = __get_parser()
