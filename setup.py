from setuptools import setup

setup(
    name='dewar',
    version='0.1',
    description='Static Site Generator, like flask',
    url='http://github.com/tfpk/dewar',
     author='tfpk',
    author_email='tom.kunc@kinesis.org',
    license='All Rights Reserved',
    packages=['dewar'],
    install_requires=[
        'markdown',
    ],

    test_suite='',
    tests_require=[
        'pytest'
    ]
)

