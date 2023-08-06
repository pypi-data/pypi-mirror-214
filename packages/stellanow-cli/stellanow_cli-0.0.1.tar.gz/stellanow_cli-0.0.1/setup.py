from setuptools import setup, find_packages

setup(
    name='stellanow_cli',
    version='0.0.1',
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
