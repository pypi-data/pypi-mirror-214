"""
Copyright (C) 2022-2023 Stella Technologies (UK) Limited.

This software is the proprietary information of Stella Technologies (UK) Limited.
Use, reproduction, or redistribution of this software is strictly prohibited without
the express written permission of Stella Technologies (UK) Limited.
All rights reserved.
"""

import click
import configparser
import os

from .commands.configure import configure_cmd
from .commands.generate import generate_cmd
from .commands.plan import plan_cmd
from .commands.events import events_cmd
from ._version import __version__


@click.group(chain=True)
@click.version_option(version=__version__, message="%(version)s")
@click.pass_context
def cli(ctx):
    """Command-line interface for the StellaNow SDK code generation and comparison tool."""
    # Create a new configparser object
    config = configparser.ConfigParser()

    # Get the home directory
    home = os.path.expanduser("~")

    # Read the configuration from a file in the .stellanow directory
    config.read(os.path.join(home, ".stellanow", "config.ini"))

    # Store the configuration in the context, so it can be accessed by other commands
    ctx.obj = config


cli.add_command(configure_cmd)
cli.add_command(generate_cmd)
cli.add_command(plan_cmd)
cli.add_command(events_cmd)
