"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import toml

from setuptools import setup, find_packages
from stellanow_cli._version import __version__


def get_install_requirements():
    try:
        # read my pipfile
        with open('Pipfile', 'r') as fh:
            pipfile = fh.read()
        # parse the toml
        pipfile_toml = toml.loads(pipfile)
    except FileNotFoundError:
        return []
    # if the package's key isn't there then just return an empty list
    try:
        required_packages = pipfile_toml['packages'].items()
    except KeyError:
        return []
    # If a version/range is specified in the Pipfile honor it otherwise just list the package
    return ["{0}{1}".format(pkg, ver) if ver != "*"
            else pkg for pkg, ver in required_packages]


setup(
    name='stellanow_cli',
    description="Command-line interface for the StellaNow SDK code generation and comparison tool.",
    long_description=open('README.public').read(),
    version=__version__,
    packages=find_packages(),
    python_requires='>=3.10',
    include_package_data=True,
    install_requires=get_install_requirements(),
    entry_points='''
        [console_scripts]
        stellanow=stellanow_cli.cli:cli
    ''',
)
