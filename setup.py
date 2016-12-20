#!/usr/bin/env python


from setuptools import setup
from codecs import open
from os import path
from mango import __version__


long_description = None
current_path = path.abspath(path.dirname(__file__))


with open(path.join(current_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup_info = dict(name='python-mango',
                  version=__version__,
                  description='Mango: simple MongoDb wrapper',
                  long_description=long_description,
                  author='laminko',
                  author_email='lminko.lmk@gmail.com',
                  url='https://laminko.github.io/mango/',
                  license="MIT",
                  py_modules=['mango'],
                  platforms=('Any',),
                  classifiers=[
                      'Development Status :: 3 - Alpha',
                      'Environment :: Console',
                      'Intended Audience :: Developers',
                      'Intended Audience :: System Administrators',
                      'License :: OSI Approved :: MIT License',
                      'Operating System :: MacOS :: MacOS X',
                      'Operating System :: Microsoft :: Windows',
                      'Operating System :: POSIX',
                      'Programming Language :: Python',
                      'Topic :: Utilities',
                      'Topic :: Software Development :: Libraries'
                  ],
                  install_requires=['pymongo'])

setup(**setup_info)
