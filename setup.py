from setuptools import setup
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dewar',
    version='0.1.2',
    
    description='Static Site Generator, like flask',
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    url='http://github.com/tfpk/dewar',
    download_url='http://github.com/tfpk/dewar/archive/v0.1.2.tar.gz',

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
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='dewar static site flask web',
)

