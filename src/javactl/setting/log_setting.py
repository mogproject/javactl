from __future__ import division, print_function, absolute_import, unicode_literals

from mog_commons.case_class import CaseClass
from mog_commons.functional import omap, oget
from javactl.util import normalize_path, DataSize


class LogSetting(CaseClass):
    class Console(CaseClass):
        def __init__(self, home, prefix=None, max_size=None, backup=None, preserve=None):
            # constraints
            assert backup is None or isinstance(backup, int), 'log.console.backup must be an integer'
            assert preserve is None or isinstance(backup, int), 'log.console.preserve must be an integer'

            CaseClass.__init__(
                self,
                ('prefix', omap(lambda p: normalize_path(p, home), prefix)),
                ('max_size', omap(DataSize, max_size)),
                ('backup', backup),
                ('preserve', preserve))

        def get_path(self, now):
            return omap(lambda p: p + now.strftime('_%Y%m%d_%H%M%S.log'), self.prefix)

    class GC(CaseClass):
        def __init__(self, home, prefix=None, max_size=None, backup=None, preserve=None):
            # constraints
            assert backup is None or isinstance(backup, int), 'log.gc.backup must be an integer'
            assert preserve is None or isinstance(backup, int), 'log.gc.preserve must be an integer'

            CaseClass.__init__(
                self,
                ('prefix', omap(lambda p: normalize_path(p, home), prefix)),
                ('max_size', omap(DataSize, max_size)),
                ('backup', backup),
                ('preserve', preserve))

        def get_path(self, now):
            return omap(lambda p: p + now.strftime('_%Y%m%d_%H%M%S.log'), self.prefix)

        def get_opts(self, now):
            xs = []
            if self.prefix is not None:
                xs.extend([
                    '-verbose:gc',
                    '-XX:+PrintGCDateStamps',
                    '-XX:+PrintGCDetails',
                    '-Xloggc:%s' % self.get_path(now),
                ])
                if self.max_size is not None:
                    xs.extend([
                        '-XX:+UseGCLogFileRotation',
                        '-XX:GCLogFileSize=%s' % self.max_size])
                    if self.backup is not None:
                        xs.append('-XX:NumberOfGCLogFiles=%s' % self.backup)
            return xs

    class Dump(CaseClass):
        def __init__(self, home, prefix=None):
            CaseClass.__init__(self, ('prefix', omap(lambda p: normalize_path(p, home), prefix)))

        def get_opts(self):
            return [] if self.prefix is None else [
                '-XX:+HeapDumpOnOutOfMemoryError',
                '-XX:HeapDumpPath=%s' % self.prefix,
            ]

    class Error(CaseClass):
        def __init__(self, home, path=None):
            CaseClass.__init__(self, ('path', omap(lambda p: normalize_path(p, home), path)))

        def get_opts(self):
            return [] if self.path is None else [
                '-XX:ErrorFile=%s' % self.path,
            ]

    def __init__(self, home, console=None, gc=None, dump=None, error=None):
        CaseClass.__init__(
            self,
            ('console', LogSetting.Console(home, **oget(console, {}))),
            ('gc', LogSetting.GC(home, **oget(gc, {}))),
            ('dump', LogSetting.Dump(home, **oget(dump, {}))),
            ('error', LogSetting.Error(home, **oget(error, {}))),
        )

    def get_opts(self, now):
        return self.gc.get_opts(now) + self.dump.get_opts() + self.error.get_opts()
