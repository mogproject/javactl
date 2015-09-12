from javactl.util.case_class import CaseClass

import six


class DataSize(CaseClass):
    _scales = {'k': 2 ** 10, 'm': 2 ** 20, 'g': 2 ** 30}

    def __init__(self, size):
        assert isinstance(size, int) or isinstance(size, six.string_types)

        if isinstance(size, int) or size.isdigit():
            value = int(size)
            scale = ''
        else:
            val, last = size[:-1], size[-1:]
            assert last.lower() in self._scales.keys(), 'Unknown scale: %s' % last
            assert val.isdigit(), 'Size must be an integer: %s' % val

            value = int(val)
            scale = last
        CaseClass.__init__(self, ('value', value), ('scale', scale))

    def bytes(self):
        return self.value * self._scales.get(self.scale.lower(), 1)

    def __str__(self):
        return '%d%s' % (self.value, self.scale)
