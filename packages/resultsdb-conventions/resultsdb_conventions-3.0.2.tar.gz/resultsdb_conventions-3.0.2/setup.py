#!/usr/bin/env python
# Copyright Red Hat
#
# resultsdb_conventions is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Adam Williamson <awilliam@redhat.com>

"""Setuptools script."""

from os import path
from setuptools import setup

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
        LONGDESC = f.read()
except TypeError:
    with open(path.join(HERE, 'README.md')) as f:
        LONGDESC = f.read()

setup(
    name="resultsdb_conventions",
    version="3.0.2",
    packages=['resultsdb_conventions'],
    package_dir={"": "src"},
    author="Adam Williamson",
    author_email="awilliam@redhat.com",
    description="Module for conveniently reporting to ResultsDB following conventions",
    license="GPLv3+",
    keywords="fedora rhel epel resultsdb test taskotron",
    url="https://pagure.io/fedora-qa/resultsdb_conventions",
    setup_requires=[
        'setuptools_git',
    ],
    install_requires=open('install.requires').read().splitlines(),
    tests_require=open('tests.requires').read().splitlines(),
    extras_require={
        'fedora': ['fedfind'],
    },
    long_description=LONGDESC,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
)

# vim: set textwidth=120 ts=8 et sw=4:
