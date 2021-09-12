#!/usr/bin/env python
import os

from setuptools import setup, find_packages

current_dir = os.path.abspath(os.path.dirname(__file__))

# Read properties from PACKAGE.properties
with open(os.path.join(current_dir, "PACKAGE.properties")) as f:
    properties = dict(line.strip().split('=') for line in f)

# Get the long description from the README file
with open(os.path.join(current_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name=properties["NAME"],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'space_radar': 'space_radar'},
    install_requires=[],
    include_package_data=True,
    version=properties["VERSION"],
    license=properties["LICENSE"],
    description=properties["DESCRIPTION"],
    long_description=long_description,
    author=properties["MAINTAINER"],
    author_email=properties["MAINTAINER"],
    url=properties["URL"],
    test_suite="tests",

    entry_points={
        'console_scripts': [
            'space_radar = space_radar.cli:main'
        ]
    }
)
