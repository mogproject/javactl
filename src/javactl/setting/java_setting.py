from __future__ import division, print_function, absolute_import, unicode_literals

import os
from mog_commons.case_class import CaseClass
from mog_commons.functional import omap, oget


class JavaSetting(CaseClass):
    class Memory(CaseClass):
        def __init__(self,
                     java_version,  # just use for assertion
                     heap_min=None,
                     heap_max=None,
                     perm_min=None,
                     perm_max=None,
                     metaspace_min=None,
                     metaspace_max=None,
                     new_min=None,
                     new_max=None,
                     survivor_ratio=None,
                     target_survivor_ratio=None):
            # constraints
            assert perm_min is None or java_version < 1.8, 'java.memory.perm_min is not applicable to java >= 1.8'
            assert perm_max is None or java_version < 1.8, 'java.memory.perm_max is not applicable to java >= 1.8'
            assert metaspace_min is None or java_version >= 1.8, \
                'java.memory.metaspace_min is not applicable to java < 1.8'
            assert metaspace_max is None or java_version >= 1.8, \
                'java.memory.metaspace_max is not applicable to java < 1.8'

            CaseClass.__init__(
                self,
                ('heap_min', heap_min),
                ('heap_max', heap_max),
                ('perm_min', perm_min),
                ('perm_max', perm_max),
                ('metaspace_min', metaspace_min),
                ('metaspace_max', metaspace_max),
                ('new_min', new_min),
                ('new_max', new_max),
                ('survivor_ratio', survivor_ratio),
                ('target_survivor_ratio', target_survivor_ratio)
            )

        def get_opts(self):
            xs = [
                omap(lambda s: '-Xms%s' % s, self.heap_min),
                omap(lambda s: '-Xmx%s' % s, self.heap_max),
                omap(lambda s: '-XX:PermSize=%s' % s, self.perm_min),
                omap(lambda s: '-XX:MaxPermSize=%s' % s, self.perm_max),
                omap(lambda s: '-XX:MetaspaceSize=%s' % s, self.metaspace_min),
                omap(lambda s: '-XX:MaxMetaspaceSize=%s' % s, self.metaspace_max),
                omap(lambda s: '-Xmn%s' % s, self.new_min),
                omap(lambda s: '-XX:MaxNewSize=%s' % s, self.new_max),
                omap(lambda x: '-XX:SurvivorRatio=%d' % x, self.survivor_ratio),
                omap(lambda x: '-XX:TargetSurvivorRatio=%d' % x, self.target_survivor_ratio),
            ]
            return [x for x in xs if x is not None]

    class JMX(CaseClass):
        def __init__(self, port=None, ssl=None, authenticate=None):
            CaseClass.__init__(self, ('port', port), ('ssl', ssl), ('authenticate', authenticate))

        def get_opts(self):
            if self.port is None:
                return []
            xs = [
                '-Dcom.sun.management.jmxremote',
                omap(lambda x: '-Dcom.sun.management.jmxremote.port=%d' % x, self.port),
                omap(lambda b: '-Dcom.sun.management.jmxremote.ssl=%s' % JavaSetting.py_to_java_str(b), self.ssl),
                omap(lambda b: '-Dcom.sun.management.jmxremote.authenticate=%s' % JavaSetting.py_to_java_str(b), self.authenticate),
            ]
            return [x for x in xs if x is not None]

    def __init__(self,
                 home=None,
                 version=None,
                 server=None,
                 memory=None,
                 jmx=None,
                 prop=None,
                 option=None):
        # constraints
        assert home is not None and os.path.isabs(home), 'java.home is required and must be an absolute path'
        assert version is not None, 'java.version is required'

        # TODO: check value types and format
        assert prop is None or isinstance(prop, dict), 'java.prop must be a dict'
        assert option is None or isinstance(option, list), 'java.option must be a list'

        CaseClass.__init__(
            self,
            ('home', home),
            ('version', version),
            ('server', server),
            ('memory', JavaSetting.Memory(version, **oget(memory, {}))),
            ('jmx', JavaSetting.JMX(**oget(jmx, {}))),
            ('prop', oget(prop, {})),
            ('option', oget(option, [])),
        )

    def get_executable(self):
        return os.path.join(self.home, 'bin', 'java')

    def get_opts(self):
        sv = ['-server'] if self.server else []
        pr = ['-D%s=%s' % (k, JavaSetting.py_to_java_str(v)) for k, v in sorted(self.prop.items())]
        return sv + self.memory.get_opts() + self.jmx.get_opts() + pr + self.option

    def get_args(self):
        return [self.get_executable()] + self.get_opts()

    @staticmethod
    def py_to_java_str(value):
        """Convert python data to Java-like string"""
        if isinstance(value, bool):
            return str(value).lower()
        else:
            return str(value)
