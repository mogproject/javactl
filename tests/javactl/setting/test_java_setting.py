from __future__ import division, print_function, absolute_import, unicode_literals

from mog_commons.unittest import TestCase
from javactl.setting.java_setting import JavaSetting


class TestJavaSetting(TestCase):

    def test_py_to_java_str(self):
        self.assertEqual(JavaSetting.py_to_java_str(True), 'true')
        self.assertEqual(JavaSetting.py_to_java_str(False), 'false')
        self.assertEqual(JavaSetting.py_to_java_str(None), 'None')
        self.assertEqual(JavaSetting.py_to_java_str(0), '0')
        self.assertEqual(JavaSetting.py_to_java_str(1000000000), '1000000000')
        self.assertEqual(JavaSetting.py_to_java_str(10000000000), '10000000000')
        self.assertEqual(JavaSetting.py_to_java_str(-10000000000), '-10000000000')
        self.assertEqual(JavaSetting.py_to_java_str('abc'), 'abc')
