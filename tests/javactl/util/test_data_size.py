from __future__ import division, print_function, absolute_import, unicode_literals

from javactl.util.data_size import DataSize
from tests.universal import TestCase


class TestDataSize(TestCase):
    def test_init(self):
        self.assertEqual(DataSize(0).value, 0)
        self.assertEqual(DataSize(0).scale, '')
        self.assertEqual(DataSize(123).value, 123)
        self.assertEqual(DataSize(123).scale, '')
        self.assertEqual(DataSize('0').value, 0)
        self.assertEqual(DataSize('0').scale, '')
        self.assertEqual(DataSize('123').value, 123)
        self.assertEqual(DataSize('123').scale, '')
        self.assertEqual(DataSize('123k').value, 123)
        self.assertEqual(DataSize('123k').scale, 'k')
        self.assertEqual(DataSize('123m').value, 123)
        self.assertEqual(DataSize('123m').scale, 'm')
        self.assertEqual(DataSize('123g').value, 123)
        self.assertEqual(DataSize('123g').scale, 'g')
        self.assertEqual(DataSize('123G').value, 123)
        self.assertEqual(DataSize('123G').scale, 'G')

    def test_init_error(self):
        self.assertRaisesRegexp(AssertionError, '^Unknown scale: $', DataSize, '')
        self.assertRaisesRegexp(AssertionError, '^Unknown scale: 3$', DataSize, '1.23')
        self.assertRaisesRegexp(AssertionError, '^Unknown scale: p$', DataSize, 'p')

        self.assertRaisesRegexp(AssertionError, '^Size must be an integer: g$', DataSize, 'gg')
        self.assertRaisesRegexp(AssertionError, '^Size must be an integer: 1[.]23$', DataSize, '1.23k')

    def test_bytes(self):
        self.assertEqual(DataSize('0m').bytes(), 0)
        self.assertEqual(DataSize(123).bytes(), 123)
        self.assertEqual(DataSize('123').bytes(), 123)
        self.assertEqual(DataSize('10k').bytes(), 10240)
        self.assertEqual(DataSize('10m').bytes(), 10 * 1024 * 1024)
        self.assertEqual(DataSize('10G').bytes(), 10 * 1024 * 1024 * 1024)

    def test_str(self):
        self.assertEqual(str(DataSize('0')), '0')
        self.assertEqual(str(DataSize(0)), '0')
        self.assertEqual(str(DataSize('123m')), '123m')
        self.assertEqual(str(DataSize('123G')), '123G')
