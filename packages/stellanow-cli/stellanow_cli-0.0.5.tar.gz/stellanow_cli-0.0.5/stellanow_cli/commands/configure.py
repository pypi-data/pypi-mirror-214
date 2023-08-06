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
import re

from ..validate import is_valid_uuid
from ..logger import logger
from ..config import Env


@click.command(name='configure')
@click.option('--profile', default='DEFAULT', prompt=False,
              help="The profile name for storing a particular set of configurations. "
                   "If no profile is specified, the configurations will be stored under the 'DEFAULT' profile.")
@click.option('--env', hidden=True, type=click.Choice([e.value for e in Env], case_sensitive=False))
@click.pass_context
def configure(ctx, profile, env):
    """Sets up the necessary credentials and configurations for a specific profile or for the DEFAULT profile if none
    is specified."""

    print(f'Provide configuration for profile: {profile}')

    config = ctx.obj

    access_key = config.get(profile, "access_key", fallback=None)
    access_token = config.get(profile, "access_token", fallback=None)
    organization_id = config.get(profile, "organization_id", fallback=None)
    project_id = config.get(profile, "project_id", fallback=None)

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    string_regex = r'^[a-zA-Z0-9_-]+$'
    while True:
        access_key = click.prompt(f'Access Key', default=access_key)
        if re.match(email_regex, access_key) or re.match(string_regex, access_key):
            break
        else:
            logger.error("Invalid access key format. It should be a valid email address or a string containing only "
                         "alphanumeric characters, dashes, and underscores.")

    while True:
        access_token = click.prompt('Access Token', hide_input=True, default=access_token, show_default=False)
        if re.match("^\S{8,64}$", access_token):
            break
        else:
            logger.error("Invalid access token format. It should contain no whitespace and be 8-64 characters long.")

    while True:
        organization_id = click.prompt(f'Organization ID', default=organization_id)
        if is_valid_uuid(organization_id):
            break
        else:
            logger.error("Invalid organization ID. It should be a valid UUID.")

    while True:
        project_id = click.prompt(f'Project ID', default=project_id)
        if is_valid_uuid(project_id):
            break
        else:
            logger.error("Invalid organization ID. It should be a valid UUID.")

    # Get the home directory
    home = os.path.expanduser("~")

    # Create the .stellanow directory if it does not exist
    os.makedirs(os.path.join(home, ".stellanow"), exist_ok=True)

    # Create a new configparser object
    config = configparser.ConfigParser()

    # If a config file already exists, read it first to preserve existing profiles
    config_file = os.path.join(home, ".stellanow", "config.ini")
    if os.path.exists(config_file):
        config.read(config_file)

    # Set the configuration values for the chosen profile
    config[profile] = {
        "access_key": access_key,
        "access_token": access_token,
        "organization_id": organization_id,
        "project_id": project_id
    }

    # add the env value from a hidden option
    if env is not None:
        config[profile]['env'] = env

    # Write the updated configuration to the file
    with open(config_file, "w") as configfile:
        config.write(configfile)

    logger.error(f"Configuration for profile '{profile}' saved successfully")


configure_cmd = configure
