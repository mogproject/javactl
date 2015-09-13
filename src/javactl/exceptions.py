from __future__ import division, print_function, absolute_import, unicode_literals


class JavaCtlError(Exception):
    """Base class of application specific exceptions"""


class DuplicateError(JavaCtlError):
    """Application is already running."""
