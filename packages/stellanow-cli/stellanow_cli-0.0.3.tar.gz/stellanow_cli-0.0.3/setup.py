"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

from setuptools import setup, find_packages

from stellanow_cli._version import __version__


setup(
    name='stellanow_cli',
    description="A comprehensive Python package for data analysis and visualization.",
    long_description=open('README.public').read(),
    version=__version__,
    packages=find_packages(),
    python_requires='==3.10.*',
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'jinja2',
        'urllib3<2.0',
        'prettytable'
    ],
    entry_points='''
        [console_scripts]
        stellanow=stellanow_cli.cli:cli
    ''',
)
