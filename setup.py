#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import sys

if sys.argv[-1] == 'cheeseit!':
    os.system('python setup.py sdist upload')
    sys.exit()

elif sys.argv[-1] == 'testit!':
    os.system('python setup.py sdist upload -r test')
    sys.exit()

with open("README.rst") as f:
    readme = f.read()

setup(
    name='psforms',
    version='0.2.0',
    description='Hassle free PySide forms.',
    long_description=readme,
    author='Dan Bradham',
    author_email='danielbradham@gmail.com',
    url='http://github.com/danbradham/psforms.git',
    license='MIT',
    packages=find_packages(),
    package_data={
        '': ['LICENSE', 'README.rst'],
        'psforms': ['style.css']
    },
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
