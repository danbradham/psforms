#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import os
import sys
import psforms

if sys.argv[-1] == 'cheeseit!':
    os.system('python setup.py sdist upload')
    sys.exit()

elif sys.argv[-1] == 'testit!':
    os.system('python setup.py sdist upload -r test')
    sys.exit()


packages = (
    'psforms',
)

package_data = {
    '': ['LICENSE', 'README.rst'],
    'psforms': [],
}

with open("README.rst") as f:
    readme = f.read()

setup(
    name=psforms.__title__,
    version=psforms.__version__,
    description=psforms.__description__,
    long_description=readme,
    author=psforms.__author__,
    author_email=psforms.__email__,
    url=psforms.__url__,
    license=psforms.__version__,
    packages=packages,
    package_data=package_data,
    package_dir={'psforms': 'psforms'},
    include_package_data=True,
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ),
)
