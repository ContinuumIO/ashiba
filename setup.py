#!/usr/bin/env python
"""Ashiba"""

import sys

if "develop" in sys.argv[1:]:
    import setuptools

from distutils.core import setup

from os.path import join, dirname
from distutils.sysconfig import get_python_lib
from distutils.dir_util import copy_tree

import ashiba

# Make sure I have the right Python version.
if sys.version_info[:2] < (2, 7):
    print("SymPy requires Python 2.7 or newer. Python %d.%d detected" %
          sys.version_info[:2])
    sys.exit(-1)

classifiers = [
    # License?
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    # TODO: Add some topics
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
]

long_description = "App building framework for Wakari and Anaconda."

# http://stackoverflow.com/a/11262389/161801
# I couldn't figure out how to put this in the setup function below

if 'install' in sys.argv[1:]:
    copy_tree(join(dirname(__file__), 'ashiba', 'share'), join(get_python_lib(), 'ashiba', 'share'))

setup(
    name='ashiba',
    version=ashiba.__version__,
    description=long_description,
    long_description=long_description,
    packages=['ashiba'],
    author='Continuum Analytics, Inc.',
    author_email='support@continuum.io',
    url='https://github.com/ContinuumIO/ashiba',
    scripts=['bin/ashiba'],
    classifiers=classifiers,
)
