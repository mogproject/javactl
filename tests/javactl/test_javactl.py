from __future__ import division, print_function, absolute_import, unicode_literals

import os
import io
import jinja2
import tempfile
import getpass
import time
from mog_commons.unittest import TestCase
from javactl import javactl


class TestJavaCtl(TestCase):
    @staticmethod
    def _remove_dirs(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    def test_main(self):
        self.maxDiff = None

        curdir = os.path.abspath(os.path.curdir)
        template_file = os.path.join(curdir, 'tests', 'resources', 'test_01.yml.j2')

        tempdir = tempfile.mkdtemp()

        try:
            # create configuration file
            conf_file = os.path.join(tempdir, 'test_01.yml')

            with io.open(conf_file, 'w') as fout:
                with io.open(template_file) as fin:
                    template_data = fin.read()
                s = jinja2.Environment().from_string(template_data).render(
                    tempdir=tempdir, curdir=curdir, os_user=getpass.getuser())
                fout.write(s)

            # do the work
            log_dir = os.path.join(tempdir, 'logs')
            log_dirs = [os.path.join(log_dir, name) for name in ['console', 'gc', 'dump']]
            expected = '\n'.join('Creating directory: %s' % s for s in log_dirs) + '\n'
            self.assertOutput(expected, '', lambda: javactl.main(['javactl', conf_file]))

            # there should be directories
            self.assertTrue(all(os.path.exists(s) for s in log_dirs))

            # there should be a console log
            logs = [os.path.join(tempdir, 'logs', 'console', f) for f in os.listdir(log_dirs[0])]
            self.assertEqual(len(logs), 1)

            time.sleep(1)

            with io.open(logs[0]) as f:
                log_content = f.read()
            self.assertNotEqual(len(log_content), 0)
            log_dir_len = len(log_dir)

            expected1 = ''.join([
                ' -server -Xms64M -Xmx2G -XX:MetaspaceSize=1G -XX:MaxMetaspaceSize=2G -Xmn256M -XX:MaxNewSize=256M ',
                '-XX:SurvivorRatio=8 -XX:TargetSurvivorRatio=50 -Dcom.sun.management.jmxremote ',
                '-Dcom.sun.management.jmxremote.port=20001 -Dcom.sun.management.jmxremote.ssl=false ',
                '-Dcom.sun.management.jmxremote.authenticate=false -Dcom.amazonaws.sdk.disableCertChecking=True ',
                '-Dfile.encoding=UTF-8 -Dhttp.netty.maxInitialLineLength=8192 -Dhttp.port=9000 ',
                '-XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSInitiatingOccupancyOnly ',
                '-XX:CMSInitiatingOccupancyFraction=70 -XX:+ScavengeBeforeFullGC -XX:+CMSScavengeBeforeRemark ',
                '-verbose:gc -XX:+PrintGCDateStamps -XX:+PrintGCDetails ',
                '-Xloggc:%s/gc_' % log_dirs[1],

            ])
            expected2 = ''.join([
                ' -XX:+UseGCLogFileRotation -XX:GCLogFileSize=10M -XX:NumberOfGCLogFiles=10 ',
                '-XX:+HeapDumpOnOutOfMemoryError ',
                '-XX:HeapDumpPath=%s ' % log_dirs[2],
                '-XX:ErrorFile=%s/hs_error_pid%%p.log ' % log_dir,
                '-jar %s/bin/your-app-assembly-0.1.0.jar\n' % tempdir,
            ])
            self.assertEqual(log_content[25:709 + log_dir_len], expected1)
            self.assertEqual(log_content[728 + log_dir_len:], expected2)

        finally:
            # clean up temporary files
            self._remove_dirs(tempdir)
