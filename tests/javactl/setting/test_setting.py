from __future__ import division, print_function, absolute_import, unicode_literals

from datetime import datetime
from tests.universal import TestCase
from javactl.setting.setting import Setting


class TestSetting(TestCase):
    def test_get_args(self):
        self.maxDiff = None
        s = Setting('tests/resources/example.yml').load_config()
        result = s.get_args(datetime(2015, 9, 10, 12, 34, 56, 789))
        self.assertEqual(result, [
            '/usr/java/latest/bin/java',
            '-server',
            '-Xms64M',
            '-Xmx2G',
            '-XX:MetaspaceSize=1G',
            '-XX:MaxMetaspaceSize=2G',
            '-Xmn256M',
            '-XX:MaxNewSize=256M',
            '-XX:SurvivorRatio=8',
            '-XX:TargetSurvivorRatio=50',
            '-Dcom.sun.management.jmxremote',
            '-Dcom.sun.management.jmxremote.port=20001',
            '-Dcom.sun.management.jmxremote.ssl=false',
            '-Dcom.sun.management.jmxremote.authenticate=false',
            '-Dcom.amazonaws.sdk.disableCertChecking=True',
            '-Dfile.encoding=UTF-8',
            '-Dhttp.netty.maxInitialLineLength=8192',
            '-Dhttp.port=9000',
            '-XX:+UseConcMarkSweepGC',
            '-XX:+CMSParallelRemarkEnabled',
            '-XX:+UseCMSInitiatingOccupancyOnly',
            '-XX:CMSInitiatingOccupancyFraction=70',
            '-XX:+ScavengeBeforeFullGC',
            '-XX:+CMSScavengeBeforeRemark',
            '-verbose:gc',
            '-XX:+PrintGCDateStamps',
            '-XX:+PrintGCDetails',
            '-Xloggc:/path/to/your-app/logs/gc/gc_20150910_123456.log',
            '-XX:+UseGCLogFileRotation',
            '-XX:GCLogFileSize=10M',
            '-XX:NumberOfGCLogFiles=10',
            '-XX:+HeapDumpOnOutOfMemoryError',
            '-XX:HeapDumpPath=/path/to/your-app/logs/dump',
            '-XX:ErrorFile=/path/to/your-app/logs/hs_error_pid%p.log',
            '-jar',
            '/path/to/your-app/bin/your-app-assembly-0.1.0.jar'
        ])
