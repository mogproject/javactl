import sys
from setuptools import setup, find_packages

try:
    # Work around a traceback on Python < 2.7.4 and < 3.3.1
    # http://bugs.python.org/issue15881#msg170215
    import multiprocessing  # unused
except ImportError:
    pass

SRC_DIR = 'src'


def get_version():
    sys.path[:0] = [SRC_DIR]
    return __import__('javactl').__version__


setup(
    name='javactl',
    version=get_version(),
    description='YAML-Configurable Java Application Wrapper',
    author='mogproject',
    author_email='mogproj@gmail.com',
    license='Apache 2.0 License',
    url='https://github.com/mogproject/javactl',
    install_requires=[
        'pyyaml',
        'six',
        'mog-commons',
    ],
    tests_require=[
        'mock == 1.0.1',  # lock version for older version of setuptools
        'jinja2' + (' == 2.6' if sys.version_info[:2] == (3, 2) else ''),
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    javactl = javactl.javactl:main
    """,
)
