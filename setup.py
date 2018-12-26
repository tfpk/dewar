from setuptools import setup

setup(
    name='dewar',
    version='0.1.1',
    description='Static Site Generator, like flask',
    url='http://github.com/tfpk/dewar',
    download_url='http://github.com/tfpk/dewar/archive/v0.1.1.tar.gz',
    author='tfpk',
    author_email='tomkunc0@gmail.org',
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

