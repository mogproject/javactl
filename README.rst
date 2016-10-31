=======
javactl
=======

YAML-Configurable Java Application Wrapper

.. image:: https://badge.fury.io/py/javactl.svg
   :target: http://badge.fury.io/py/javactl
   :alt: PyPI version

.. image:: https://travis-ci.org/mogproject/javactl.svg?branch=master
   :target: https://travis-ci.org/mogproject/javactl
   :alt: Build Status

.. image:: https://coveralls.io/repos/mogproject/javactl/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/mogproject/javactl?branch=master
   :alt: Coverage Status

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: http://choosealicense.com/licenses/apache-2.0/
   :alt: License

.. image:: https://badge.waffle.io/mogproject/javactl.svg?label=ready&title=Ready
   :target: https://waffle.io/mogproject/javactl
   :alt: 'Stories in Ready'

--------
Features
--------

*Launch your Java application more safely, explicitly, and flexibly!*

This script does ...

* (before the launch)
   * Load settings from a YAML file
   * Verify the OS user name and Java version
   * Check if the application has already been running when duplicate running is prohibited
   * Execute pre-launch commands
   * Log to syslog
* Launch the Java application with the proper options
* (after the launch)
   * Log to syslog
   * Execute post-launch commands

------------
Dependencies
------------

* Python: 2.6 / 2.7 / 3.2 / 3.3 / 3.4
* pyyaml
* six

------------
Installation
------------

* ``pip`` command may require ``sudo``

+-------------------------+-------------------------------------+
| Operation               | Command                             |
+=========================+=====================================+
| Install                 |``pip install javactl``              |
+-------------------------+-------------------------------------+
| Upgrade                 |``pip install --upgrade javactl``    |
+-------------------------+-------------------------------------+
| Uninstall               |``pip uninstall javactl``            |
+-------------------------+-------------------------------------+
| Check installed version |``javactl --version``                |
+-------------------------+-------------------------------------+
| Help                    |``javactl -h``                       |
+-------------------------+-------------------------------------+

* Then, write your configuration to the file ``your-app.yml``.

See the example below.

---------------------
Configuration Example
---------------------

See this `example <https://github.com/mogproject/javactl/blob/master/tests/resources/example.yml>`_.

---------------------------
Now Launch Your Application
---------------------------

* Dry-run mode

::

    javactl --check /path/to/your-app.yml

* Launch the java application

::

    javactl /path/to/your-app.yml


* Launch with arguments

::

    javactl /path/to/your-app.yml --option-for-your-app arg1 arg2


That's it!

