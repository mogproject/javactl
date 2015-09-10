from setuptools import setup, find_packages

SRC_DIR = 'src'


def get_version():
    import sys

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
    ],
    tests_require=[
        'unittest2',
        'mock',
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
